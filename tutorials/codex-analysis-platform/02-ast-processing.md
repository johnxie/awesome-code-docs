---
layout: default
title: "Chapter 2: AST Processing"
parent: "Codex Analysis Platform"
nav_order: 2
---

# Chapter 2: AST Processing

Welcome to **Chapter 2: AST Processing**. In this part of **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master abstract syntax tree manipulation for code analysis and transformation.

## Overview

Abstract Syntax Trees (ASTs) are the foundation of code analysis. This chapter covers parsing source code into ASTs, traversing trees efficiently, and transforming code programmatically.

## Understanding ASTs

### AST Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    AST for: const add = (a, b) => a + b;        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌─────────────────┐                         │
│                     │    Program      │                         │
│                     │   (root node)   │                         │
│                     └────────┬────────┘                         │
│                              │                                  │
│                     ┌────────▼────────┐                         │
│                     │ VariableDecl    │                         │
│                     │  kind: "const"  │                         │
│                     └────────┬────────┘                         │
│                              │                                  │
│                     ┌────────▼────────┐                         │
│                     │ VariableDeclarator│                       │
│                     └───┬─────────┬───┘                         │
│                         │         │                             │
│              ┌──────────▼──┐  ┌───▼───────────────┐            │
│              │ Identifier  │  │ ArrowFunctionExpr │            │
│              │ name: "add" │  └───┬───────────┬───┘            │
│              └─────────────┘      │           │                 │
│                               ┌───▼───┐   ┌───▼──────────┐     │
│                               │params │   │BinaryExpr    │     │
│                               │[a, b] │   │operator: "+" │     │
│                               └───────┘   └──┬───────┬───┘     │
│                                              │       │         │
│                                     ┌────────▼──┐ ┌──▼───────┐ │
│                                     │Identifier │ │Identifier│ │
│                                     │name: "a"  │ │name: "b" │ │
│                                     └───────────┘ └──────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Parsing with Babel

### Basic Parsing

```typescript
// src/parsers/babel-parser.ts
import * as parser from '@babel/parser';
import type { ParseResult, ParserOptions } from '@babel/parser';
import type { File } from '@babel/types';

interface ParseConfig {
  language: 'javascript' | 'typescript' | 'jsx' | 'tsx';
  sourceType?: 'module' | 'script';
  allowImportExportEverywhere?: boolean;
}

export function parseCode(code: string, config: ParseConfig): ParseResult<File> {
  const options: ParserOptions = {
    sourceType: config.sourceType || 'module',
    allowImportExportEverywhere: config.allowImportExportEverywhere ?? true,

    plugins: getPlugins(config.language),

    // Error recovery - continue parsing despite errors
    errorRecovery: true,

    // Source ranges for precise locations
    ranges: true,

    // Comments for documentation extraction
    attachComment: true,
  };

  return parser.parse(code, options);
}

function getPlugins(language: string): ParserOptions['plugins'] {
  const base: ParserOptions['plugins'] = [
    'decorators-legacy',
    'classProperties',
    'classPrivateProperties',
    'classPrivateMethods',
    'exportDefaultFrom',
    'exportNamespaceFrom',
    'dynamicImport',
    'nullishCoalescingOperator',
    'optionalChaining',
    'optionalCatchBinding',
  ];

  switch (language) {
    case 'typescript':
    case 'tsx':
      return [...base, 'typescript', language === 'tsx' ? 'jsx' : null].filter(Boolean);
    case 'jsx':
      return [...base, 'jsx', 'flow'];
    default:
      return base;
  }
}
```

### Error-Tolerant Parsing

```typescript
// src/parsers/error-tolerant.ts
import * as parser from '@babel/parser';

interface ParseError {
  message: string;
  line: number;
  column: number;
  reasonCode: string;
}

interface TolerantParseResult {
  ast: any | null;
  errors: ParseError[];
  partial: boolean;
}

export function parseWithRecovery(code: string): TolerantParseResult {
  const errors: ParseError[] = [];

  try {
    const ast = parser.parse(code, {
      sourceType: 'module',
      errorRecovery: true,
      plugins: ['typescript', 'jsx'],
    });

    // Collect recovered errors
    if (ast.errors && ast.errors.length > 0) {
      for (const error of ast.errors) {
        errors.push({
          message: error.message,
          line: error.loc?.line || 0,
          column: error.loc?.column || 0,
          reasonCode: error.reasonCode || 'unknown',
        });
      }
    }

    return { ast, errors, partial: errors.length > 0 };

  } catch (error: any) {
    // Fatal parse error
    errors.push({
      message: error.message,
      line: error.loc?.line || 0,
      column: error.loc?.column || 0,
      reasonCode: 'fatal',
    });

    // Try to salvage partial AST
    const partialAst = attemptPartialParse(code);

    return { ast: partialAst, errors, partial: true };
  }
}

function attemptPartialParse(code: string): any | null {
  // Try parsing line by line to get partial results
  const lines = code.split('\n');
  const validStatements: any[] = [];

  for (let i = 0; i < lines.length; i++) {
    try {
      const partialCode = lines.slice(0, i + 1).join('\n');
      const ast = parser.parse(partialCode, {
        sourceType: 'module',
        errorRecovery: true,
      });
      // Store last successful parse
      if (ast.program.body.length > validStatements.length) {
        validStatements.push(...ast.program.body.slice(validStatements.length));
      }
    } catch {
      // Continue with next line
    }
  }

  if (validStatements.length > 0) {
    return {
      type: 'Program',
      body: validStatements,
      partial: true,
    };
  }

  return null;
}
```

## AST Traversal

### Using Babel Traverse

```typescript
// src/traversal/visitor.ts
import traverse, { NodePath, Visitor } from '@babel/traverse';
import * as t from '@babel/types';
import { Symbol, Reference, SymbolKind } from '../types';

interface TraversalContext {
  filePath: string;
  symbols: Symbol[];
  references: Reference[];
  scopes: ScopeStack;
}

class ScopeStack {
  private stack: Map<string, Symbol>[] = [];

  push(): void {
    this.stack.push(new Map());
  }

  pop(): void {
    this.stack.pop();
  }

  define(name: string, symbol: Symbol): void {
    const current = this.stack[this.stack.length - 1];
    if (current) {
      current.set(name, symbol);
    }
  }

  lookup(name: string): Symbol | undefined {
    for (let i = this.stack.length - 1; i >= 0; i--) {
      const symbol = this.stack[i].get(name);
      if (symbol) return symbol;
    }
    return undefined;
  }
}

export function extractSymbols(ast: t.File, filePath: string): TraversalContext {
  const context: TraversalContext = {
    filePath,
    symbols: [],
    references: [],
    scopes: new ScopeStack(),
  };

  context.scopes.push(); // Global scope

  traverse(ast, createVisitor(context));

  return context;
}

function createVisitor(ctx: TraversalContext): Visitor {
  return {
    // Function declarations
    FunctionDeclaration(path: NodePath<t.FunctionDeclaration>) {
      if (path.node.id) {
        const symbol = createSymbol(path.node.id, 'function', ctx, path);
        ctx.symbols.push(symbol);
        ctx.scopes.define(path.node.id.name, symbol);
      }

      // Enter function scope
      ctx.scopes.push();
    },

    'FunctionDeclaration|FunctionExpression|ArrowFunctionExpression': {
      exit() {
        ctx.scopes.pop();
      }
    },

    // Variable declarations
    VariableDeclarator(path: NodePath<t.VariableDeclarator>) {
      if (t.isIdentifier(path.node.id)) {
        const parent = path.parentPath.node as t.VariableDeclaration;
        const kind: SymbolKind = parent.kind === 'const' ? 'constant' : 'variable';

        const symbol = createSymbol(path.node.id, kind, ctx, path);
        ctx.symbols.push(symbol);
        ctx.scopes.define(path.node.id.name, symbol);
      }
    },

    // Class declarations
    ClassDeclaration(path: NodePath<t.ClassDeclaration>) {
      if (path.node.id) {
        const symbol = createSymbol(path.node.id, 'class', ctx, path);
        ctx.symbols.push(symbol);
        ctx.scopes.define(path.node.id.name, symbol);
      }
      ctx.scopes.push();
    },

    'ClassDeclaration|ClassExpression': {
      exit() {
        ctx.scopes.pop();
      }
    },

    // Class methods
    ClassMethod(path: NodePath<t.ClassMethod>) {
      if (t.isIdentifier(path.node.key)) {
        const symbol = createSymbol(path.node.key, 'method', ctx, path);
        ctx.symbols.push(symbol);
      }
    },

    // Class properties
    ClassProperty(path: NodePath<t.ClassProperty>) {
      if (t.isIdentifier(path.node.key)) {
        const symbol = createSymbol(path.node.key, 'property', ctx, path);
        ctx.symbols.push(symbol);
      }
    },

    // Identifier references
    Identifier(path: NodePath<t.Identifier>) {
      // Skip definitions (they're handled above)
      if (isDefinition(path)) return;

      const symbol = ctx.scopes.lookup(path.node.name);
      if (symbol) {
        const reference = createReference(path, symbol, ctx);
        ctx.references.push(reference);
      }
    },

    // Import declarations
    ImportDeclaration(path: NodePath<t.ImportDeclaration>) {
      for (const specifier of path.node.specifiers) {
        const symbol = createSymbol(specifier.local, 'variable', ctx, path);
        symbol.modifiers = ['imported'];
        ctx.symbols.push(symbol);
        ctx.scopes.define(specifier.local.name, symbol);
      }
    },

    // TypeScript interfaces
    TSInterfaceDeclaration(path: NodePath<t.TSInterfaceDeclaration>) {
      const symbol = createSymbol(path.node.id, 'interface', ctx, path);
      ctx.symbols.push(symbol);
      ctx.scopes.define(path.node.id.name, symbol);
    },

    // TypeScript type aliases
    TSTypeAliasDeclaration(path: NodePath<t.TSTypeAliasDeclaration>) {
      const symbol = createSymbol(path.node.id, 'type', ctx, path);
      ctx.symbols.push(symbol);
      ctx.scopes.define(path.node.id.name, symbol);
    },
  };
}

function createSymbol(
  node: t.Identifier,
  kind: SymbolKind,
  ctx: TraversalContext,
  path: NodePath
): Symbol {
  return {
    id: `${ctx.filePath}:${node.loc?.start.line}:${node.loc?.start.column}`,
    name: node.name,
    kind,
    location: {
      filePath: ctx.filePath,
      range: {
        start: { line: node.loc?.start.line || 0, column: node.loc?.start.column || 0 },
        end: { line: node.loc?.end.line || 0, column: node.loc?.end.column || 0 },
      },
    },
    documentation: extractDocumentation(path),
  };
}

function createReference(
  path: NodePath<t.Identifier>,
  target: Symbol,
  ctx: TraversalContext
): Reference {
  return {
    id: `ref:${ctx.filePath}:${path.node.loc?.start.line}:${path.node.loc?.start.column}`,
    targetId: target.id,
    location: {
      filePath: ctx.filePath,
      range: {
        start: { line: path.node.loc?.start.line || 0, column: path.node.loc?.start.column || 0 },
        end: { line: path.node.loc?.end.line || 0, column: path.node.loc?.end.column || 0 },
      },
    },
    kind: determineReferenceKind(path),
  };
}

function isDefinition(path: NodePath<t.Identifier>): boolean {
  const parent = path.parent;
  return (
    t.isVariableDeclarator(parent) && parent.id === path.node ||
    t.isFunctionDeclaration(parent) && parent.id === path.node ||
    t.isClassDeclaration(parent) && parent.id === path.node ||
    t.isImportSpecifier(parent) ||
    t.isImportDefaultSpecifier(parent)
  );
}

function determineReferenceKind(path: NodePath<t.Identifier>): string {
  const parent = path.parent;

  if (t.isCallExpression(parent) && parent.callee === path.node) {
    return 'call';
  }
  if (t.isAssignmentExpression(parent) && parent.left === path.node) {
    return 'write';
  }
  return 'read';
}

function extractDocumentation(path: NodePath): string | undefined {
  const node = path.node;
  if (node.leadingComments && node.leadingComments.length > 0) {
    const lastComment = node.leadingComments[node.leadingComments.length - 1];
    if (lastComment.type === 'CommentBlock' && lastComment.value.startsWith('*')) {
      return parseJSDoc(lastComment.value);
    }
  }
  return undefined;
}

function parseJSDoc(comment: string): string {
  // Simple JSDoc parsing - extract description
  const lines = comment.split('\n');
  const description: string[] = [];

  for (const line of lines) {
    const cleaned = line.replace(/^\s*\*\s?/, '').trim();
    if (cleaned.startsWith('@')) break; // Stop at first tag
    if (cleaned) description.push(cleaned);
  }

  return description.join(' ');
}
```

## Code Transformation

### AST Manipulation

```typescript
// src/transform/transformer.ts
import * as t from '@babel/types';
import traverse from '@babel/traverse';
import generate from '@babel/generator';
import { parse } from '@babel/parser';

interface TransformResult {
  code: string;
  map?: any;
  changes: TransformChange[];
}

interface TransformChange {
  type: 'rename' | 'add' | 'remove' | 'replace';
  location: { line: number; column: number };
  description: string;
}

// Rename all occurrences of a symbol
export function renameSymbol(
  code: string,
  oldName: string,
  newName: string
): TransformResult {
  const ast = parse(code, {
    sourceType: 'module',
    plugins: ['typescript', 'jsx'],
  });

  const changes: TransformChange[] = [];

  traverse(ast, {
    Identifier(path) {
      if (path.node.name === oldName) {
        path.node.name = newName;
        changes.push({
          type: 'rename',
          location: {
            line: path.node.loc?.start.line || 0,
            column: path.node.loc?.start.column || 0,
          },
          description: `Renamed "${oldName}" to "${newName}"`,
        });
      }
    },
  });

  const output = generate(ast, { sourceMaps: true }, code);

  return {
    code: output.code,
    map: output.map,
    changes,
  };
}

// Add import statement
export function addImport(
  code: string,
  importName: string,
  modulePath: string,
  isDefault: boolean = false
): TransformResult {
  const ast = parse(code, {
    sourceType: 'module',
    plugins: ['typescript', 'jsx'],
  });

  const changes: TransformChange[] = [];

  // Check if import already exists
  let importExists = false;
  traverse(ast, {
    ImportDeclaration(path) {
      if (path.node.source.value === modulePath) {
        importExists = true;
        // Add to existing import
        if (isDefault) {
          if (!path.node.specifiers.some(s => t.isImportDefaultSpecifier(s))) {
            path.node.specifiers.unshift(t.importDefaultSpecifier(t.identifier(importName)));
          }
        } else {
          if (!path.node.specifiers.some(s =>
            t.isImportSpecifier(s) && t.isIdentifier(s.imported) && s.imported.name === importName
          )) {
            path.node.specifiers.push(t.importSpecifier(
              t.identifier(importName),
              t.identifier(importName)
            ));
          }
        }
        path.stop();
      }
    },
  });

  if (!importExists) {
    // Create new import declaration
    const specifier = isDefault
      ? t.importDefaultSpecifier(t.identifier(importName))
      : t.importSpecifier(t.identifier(importName), t.identifier(importName));

    const importDecl = t.importDeclaration(
      [specifier],
      t.stringLiteral(modulePath)
    );

    // Add at the top of the file
    ast.program.body.unshift(importDecl);

    changes.push({
      type: 'add',
      location: { line: 1, column: 0 },
      description: `Added import for "${importName}" from "${modulePath}"`,
    });
  }

  const output = generate(ast, { sourceMaps: true }, code);

  return {
    code: output.code,
    map: output.map,
    changes,
  };
}

// Extract function to separate module
export function extractFunction(
  code: string,
  functionName: string
): { original: TransformResult; extracted: string } {
  const ast = parse(code, {
    sourceType: 'module',
    plugins: ['typescript', 'jsx'],
  });

  let extractedNode: t.FunctionDeclaration | null = null;
  const changes: TransformChange[] = [];

  traverse(ast, {
    FunctionDeclaration(path) {
      if (path.node.id?.name === functionName) {
        extractedNode = t.cloneNode(path.node, true);
        path.remove();
        changes.push({
          type: 'remove',
          location: {
            line: path.node.loc?.start.line || 0,
            column: path.node.loc?.start.column || 0,
          },
          description: `Extracted function "${functionName}"`,
        });
      }
    },
  });

  // Generate extracted module
  let extractedCode = '';
  if (extractedNode) {
    const extractedAst = t.program([
      t.exportNamedDeclaration(extractedNode),
    ]);
    extractedCode = generate(extractedAst).code;
  }

  const output = generate(ast, { sourceMaps: true }, code);

  return {
    original: {
      code: output.code,
      map: output.map,
      changes,
    },
    extracted: extractedCode,
  };
}
```

## Summary

In this chapter, you've learned:

- **AST Structure**: Understanding how code is represented as trees
- **Parsing**: Using Babel to parse JavaScript and TypeScript
- **Error Recovery**: Handling malformed code gracefully
- **Traversal**: Walking the AST with visitors
- **Symbol Extraction**: Building symbol tables from AST
- **Transformation**: Programmatically modifying code

## Key Takeaways

1. **ASTs represent structure**: Not just text, but meaning
2. **Visitors pattern**: Declarative way to process nodes
3. **Scope tracking**: Essential for accurate analysis
4. **Error tolerance**: Real-world code has errors
5. **Transformation**: ASTs enable safe code modifications

## Next Steps

Now that you understand AST processing, let's explore symbol resolution and type inference in Chapter 3: Symbol Resolution.

---

**Ready for Chapter 3?** [Symbol Resolution](03-symbol-resolution.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `path`, `node`, `symbol` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: AST Processing` as an operating subsystem inside **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `line`, `code`, `push` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: AST Processing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `path`.
2. **Input normalization**: shape incoming data so `node` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `symbol`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [TypeScript Compiler API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API)
  Why it matters: authoritative reference on `TypeScript Compiler API` (github.com).
- [Babel Parser](https://babeljs.io/docs/babel-parser)
  Why it matters: authoritative reference on `Babel Parser` (babeljs.io).
- [Tree-sitter](https://tree-sitter.github.io/tree-sitter/)
  Why it matters: authoritative reference on `Tree-sitter` (tree-sitter.github.io).
- [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)
  Why it matters: authoritative reference on `Language Server Protocol` (microsoft.github.io).

Suggested trace strategy:
- search upstream code for `path` and `node` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Building the Analysis Engine](01-analysis-engine.md)
- [Next Chapter: Chapter 3: Symbol Resolution](03-symbol-resolution.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
