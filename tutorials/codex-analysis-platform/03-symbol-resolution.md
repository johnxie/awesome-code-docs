---
layout: default
title: "Chapter 3: Symbol Resolution"
parent: "Codex Analysis Platform"
nav_order: 3
---

# Chapter 3: Symbol Resolution

> Implement symbol tables, scope analysis, and type resolution for semantic understanding.

## Overview

Symbol resolution is the process of connecting identifiers in code to their definitions. This enables features like "go to definition," "find references," and type checking.

## Symbol Table Architecture

### Multi-Scope Symbol Table

```
┌─────────────────────────────────────────────────────────────────┐
│                    Symbol Table Hierarchy                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Global Scope                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  console, Math, Object, Array, Promise, fetch...        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│   Module Scope            ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  imports: { React, useState, useEffect }                │   │
│   │  exports: { MyComponent, helper }                       │   │
│   │  declarations: { MyComponent, helper, CONSTANT }        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│   Function Scope          ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  parameters: { props }                                  │   │
│   │  locals: { state, handler, result }                     │   │
│   └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│   Block Scope             ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  locals: { item, index }                                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Symbol Table Implementation

### Core Symbol Table

```typescript
// src/symbols/SymbolTable.ts
import { Symbol, SymbolKind, Location, Type } from '../types';

interface SymbolEntry {
  symbol: Symbol;
  type?: Type;
  declarations: Location[];
  references: Location[];
  exported: boolean;
}

export class SymbolTable {
  private entries: Map<string, SymbolEntry> = new Map();
  private parent: SymbolTable | null;
  private children: SymbolTable[] = [];
  private scopeType: ScopeType;
  private scopeLocation: Location;

  constructor(
    scopeType: ScopeType,
    location: Location,
    parent: SymbolTable | null = null
  ) {
    this.scopeType = scopeType;
    this.scopeLocation = location;
    this.parent = parent;

    if (parent) {
      parent.children.push(this);
    }
  }

  // Define a new symbol in this scope
  define(symbol: Symbol, options: DefineOptions = {}): SymbolEntry {
    const key = this.getKey(symbol.name, symbol.kind);
    const existing = this.entries.get(key);

    if (existing) {
      // Add additional declaration location
      existing.declarations.push(symbol.location);
      return existing;
    }

    const entry: SymbolEntry = {
      symbol,
      type: options.type,
      declarations: [symbol.location],
      references: [],
      exported: options.exported ?? false,
    };

    this.entries.set(key, entry);
    return entry;
  }

  // Look up a symbol, searching parent scopes
  lookup(name: string, kind?: SymbolKind): SymbolEntry | undefined {
    const key = this.getKey(name, kind);

    // Check current scope
    const local = this.entries.get(key);
    if (local) return local;

    // Check without kind
    if (kind) {
      const withoutKind = this.findByNameOnly(name);
      if (withoutKind) return withoutKind;
    }

    // Search parent scopes
    if (this.parent) {
      return this.parent.lookup(name, kind);
    }

    return undefined;
  }

  // Look up in current scope only
  lookupLocal(name: string, kind?: SymbolKind): SymbolEntry | undefined {
    const key = this.getKey(name, kind);
    return this.entries.get(key) || this.findByNameOnly(name);
  }

  // Add reference to a symbol
  addReference(name: string, location: Location): void {
    const entry = this.lookup(name);
    if (entry) {
      entry.references.push(location);
    }
  }

  // Get all symbols in this scope
  getSymbols(): Symbol[] {
    return Array.from(this.entries.values()).map(e => e.symbol);
  }

  // Get all symbols including child scopes
  getAllSymbols(): Symbol[] {
    const symbols = this.getSymbols();
    for (const child of this.children) {
      symbols.push(...child.getAllSymbols());
    }
    return symbols;
  }

  // Get exported symbols
  getExports(): SymbolEntry[] {
    return Array.from(this.entries.values()).filter(e => e.exported);
  }

  // Create child scope
  createChild(scopeType: ScopeType, location: Location): SymbolTable {
    return new SymbolTable(scopeType, location, this);
  }

  // Find containing scope of a location
  findScopeAt(location: Location): SymbolTable | null {
    // Check if location is within this scope
    if (!this.containsLocation(location)) {
      return null;
    }

    // Check children for more specific scope
    for (const child of this.children) {
      const childScope = child.findScopeAt(location);
      if (childScope) return childScope;
    }

    return this;
  }

  private containsLocation(location: Location): boolean {
    const scopeStart = this.scopeLocation.range.start;
    const scopeEnd = this.scopeLocation.range.end;
    const targetStart = location.range.start;

    return (
      targetStart.line >= scopeStart.line &&
      targetStart.line <= scopeEnd.line &&
      (targetStart.line !== scopeStart.line || targetStart.column >= scopeStart.column) &&
      (targetStart.line !== scopeEnd.line || targetStart.column <= scopeEnd.column)
    );
  }

  private getKey(name: string, kind?: SymbolKind): string {
    return kind ? `${kind}:${name}` : name;
  }

  private findByNameOnly(name: string): SymbolEntry | undefined {
    for (const [key, entry] of this.entries) {
      if (key.endsWith(`:${name}`) || key === name) {
        return entry;
      }
    }
    return undefined;
  }
}

type ScopeType = 'global' | 'module' | 'function' | 'block' | 'class';

interface DefineOptions {
  type?: Type;
  exported?: boolean;
}
```

### Scope Builder

```typescript
// src/symbols/ScopeBuilder.ts
import traverse, { NodePath } from '@babel/traverse';
import * as t from '@babel/types';
import { SymbolTable } from './SymbolTable';
import { Symbol, SymbolKind, Location } from '../types';

export class ScopeBuilder {
  private rootScope: SymbolTable;
  private currentScope: SymbolTable;
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
    this.rootScope = new SymbolTable('module', {
      filePath,
      range: { start: { line: 0, column: 0 }, end: { line: Infinity, column: 0 } }
    });
    this.currentScope = this.rootScope;
  }

  build(ast: t.File): SymbolTable {
    traverse(ast, {
      enter: (path) => this.handleEnter(path),
      exit: (path) => this.handleExit(path),
    });

    return this.rootScope;
  }

  private handleEnter(path: NodePath): void {
    const node = path.node;

    // Create new scopes
    if (this.createsScope(path)) {
      const scopeType = this.getScopeType(path);
      const location = this.getLocation(node);
      this.currentScope = this.currentScope.createChild(scopeType, location);
    }

    // Define symbols
    this.defineSymbols(path);
  }

  private handleExit(path: NodePath): void {
    if (this.createsScope(path) && this.currentScope.parent) {
      this.currentScope = this.currentScope.parent;
    }
  }

  private createsScope(path: NodePath): boolean {
    return (
      path.isFunctionDeclaration() ||
      path.isFunctionExpression() ||
      path.isArrowFunctionExpression() ||
      path.isClassDeclaration() ||
      path.isClassExpression() ||
      path.isBlockStatement() ||
      path.isForStatement() ||
      path.isForInStatement() ||
      path.isForOfStatement() ||
      path.isSwitchStatement()
    );
  }

  private getScopeType(path: NodePath): ScopeType {
    if (path.isClassDeclaration() || path.isClassExpression()) return 'class';
    if (path.isFunctionDeclaration() || path.isFunctionExpression() || path.isArrowFunctionExpression()) {
      return 'function';
    }
    return 'block';
  }

  private defineSymbols(path: NodePath): void {
    const node = path.node;

    // Function declarations
    if (t.isFunctionDeclaration(node) && node.id) {
      this.defineInParentScope(this.createSymbol(node.id, 'function'));
      this.defineParameters(node.params);
    }

    // Variable declarations
    if (t.isVariableDeclaration(node)) {
      const kind: SymbolKind = node.kind === 'const' ? 'constant' : 'variable';
      for (const declarator of node.declarations) {
        if (t.isIdentifier(declarator.id)) {
          this.currentScope.define(this.createSymbol(declarator.id, kind));
        }
        // Handle destructuring patterns
        if (t.isObjectPattern(declarator.id) || t.isArrayPattern(declarator.id)) {
          this.defineDestructuringPattern(declarator.id, kind);
        }
      }
    }

    // Class declarations
    if (t.isClassDeclaration(node) && node.id) {
      this.defineInParentScope(this.createSymbol(node.id, 'class'));
    }

    // Class members
    if (t.isClassMethod(node) && t.isIdentifier(node.key)) {
      this.currentScope.define(this.createSymbol(node.key, 'method'));
    }
    if (t.isClassProperty(node) && t.isIdentifier(node.key)) {
      this.currentScope.define(this.createSymbol(node.key, 'property'));
    }

    // Import declarations
    if (t.isImportDeclaration(node)) {
      for (const specifier of node.specifiers) {
        const symbol = this.createSymbol(specifier.local, 'variable');
        symbol.modifiers = ['imported'];
        this.currentScope.define(symbol, { exported: false });
      }
    }

    // Export declarations
    if (t.isExportNamedDeclaration(node)) {
      // Mark the declaration as exported
      if (node.declaration) {
        if (t.isFunctionDeclaration(node.declaration) && node.declaration.id) {
          this.currentScope.define(
            this.createSymbol(node.declaration.id, 'function'),
            { exported: true }
          );
        }
        // Similar for classes, variables...
      }
    }

    // TypeScript interfaces
    if (t.isTSInterfaceDeclaration(node)) {
      this.currentScope.define(this.createSymbol(node.id, 'interface'));
    }

    // TypeScript type aliases
    if (t.isTSTypeAliasDeclaration(node)) {
      this.currentScope.define(this.createSymbol(node.id, 'type'));
    }
  }

  private defineParameters(params: t.FunctionDeclaration['params']): void {
    for (const param of params) {
      if (t.isIdentifier(param)) {
        this.currentScope.define(this.createSymbol(param, 'parameter'));
      }
      if (t.isAssignmentPattern(param) && t.isIdentifier(param.left)) {
        this.currentScope.define(this.createSymbol(param.left, 'parameter'));
      }
      if (t.isRestElement(param) && t.isIdentifier(param.argument)) {
        this.currentScope.define(this.createSymbol(param.argument, 'parameter'));
      }
    }
  }

  private defineDestructuringPattern(pattern: t.ObjectPattern | t.ArrayPattern, kind: SymbolKind): void {
    if (t.isObjectPattern(pattern)) {
      for (const prop of pattern.properties) {
        if (t.isObjectProperty(prop) && t.isIdentifier(prop.value)) {
          this.currentScope.define(this.createSymbol(prop.value, kind));
        }
        if (t.isRestElement(prop) && t.isIdentifier(prop.argument)) {
          this.currentScope.define(this.createSymbol(prop.argument, kind));
        }
      }
    }

    if (t.isArrayPattern(pattern)) {
      for (const element of pattern.elements) {
        if (t.isIdentifier(element)) {
          this.currentScope.define(this.createSymbol(element, kind));
        }
        if (t.isRestElement(element) && t.isIdentifier(element.argument)) {
          this.currentScope.define(this.createSymbol(element.argument, kind));
        }
      }
    }
  }

  private defineInParentScope(symbol: Symbol): void {
    // Functions and classes are hoisted to parent scope
    if (this.currentScope.parent) {
      this.currentScope.parent.define(symbol);
    } else {
      this.currentScope.define(symbol);
    }
  }

  private createSymbol(node: t.Identifier, kind: SymbolKind): Symbol {
    return {
      id: `${this.filePath}:${node.loc?.start.line}:${node.loc?.start.column}`,
      name: node.name,
      kind,
      location: this.getLocation(node),
    };
  }

  private getLocation(node: t.Node): Location {
    return {
      filePath: this.filePath,
      range: {
        start: {
          line: node.loc?.start.line || 0,
          column: node.loc?.start.column || 0,
        },
        end: {
          line: node.loc?.end.line || 0,
          column: node.loc?.end.column || 0,
        },
      },
    };
  }
}

type ScopeType = 'global' | 'module' | 'function' | 'block' | 'class';
```

## Type Resolution

### Basic Type Inference

```typescript
// src/types/TypeResolver.ts
import * as t from '@babel/types';
import { SymbolTable } from '../symbols/SymbolTable';

export interface Type {
  kind: TypeKind;
  name: string;
  parameters?: Type[];  // For generics
  properties?: Map<string, Type>;  // For objects
  returnType?: Type;  // For functions
  elementType?: Type;  // For arrays
}

type TypeKind =
  | 'primitive'
  | 'object'
  | 'array'
  | 'function'
  | 'class'
  | 'interface'
  | 'union'
  | 'intersection'
  | 'generic'
  | 'unknown';

export class TypeResolver {
  private symbolTable: SymbolTable;
  private typeCache: Map<string, Type> = new Map();

  constructor(symbolTable: SymbolTable) {
    this.symbolTable = symbolTable;
    this.initializePrimitives();
  }

  private initializePrimitives(): void {
    const primitives = ['string', 'number', 'boolean', 'null', 'undefined', 'symbol', 'bigint'];
    for (const name of primitives) {
      this.typeCache.set(name, { kind: 'primitive', name });
    }
  }

  // Infer type from an expression
  inferType(node: t.Expression | t.TSType): Type {
    // TypeScript type annotations
    if (t.isTSType(node)) {
      return this.resolveTypeAnnotation(node);
    }

    // Literal types
    if (t.isStringLiteral(node)) {
      return { kind: 'primitive', name: 'string' };
    }
    if (t.isNumericLiteral(node)) {
      return { kind: 'primitive', name: 'number' };
    }
    if (t.isBooleanLiteral(node)) {
      return { kind: 'primitive', name: 'boolean' };
    }
    if (t.isNullLiteral(node)) {
      return { kind: 'primitive', name: 'null' };
    }

    // Array expressions
    if (t.isArrayExpression(node)) {
      const elementTypes = node.elements
        .filter((e): e is t.Expression => e !== null && t.isExpression(e))
        .map(e => this.inferType(e));

      const elementType = this.unifyTypes(elementTypes);
      return { kind: 'array', name: 'Array', elementType };
    }

    // Object expressions
    if (t.isObjectExpression(node)) {
      const properties = new Map<string, Type>();
      for (const prop of node.properties) {
        if (t.isObjectProperty(prop) && t.isIdentifier(prop.key) && t.isExpression(prop.value)) {
          properties.set(prop.key.name, this.inferType(prop.value));
        }
      }
      return { kind: 'object', name: 'Object', properties };
    }

    // Function expressions
    if (t.isFunctionExpression(node) || t.isArrowFunctionExpression(node)) {
      return this.inferFunctionType(node);
    }

    // Identifier - lookup in symbol table
    if (t.isIdentifier(node)) {
      const entry = this.symbolTable.lookup(node.name);
      if (entry?.type) {
        return entry.type;
      }
    }

    // Call expressions
    if (t.isCallExpression(node)) {
      return this.inferCallType(node);
    }

    // Member expressions
    if (t.isMemberExpression(node)) {
      return this.inferMemberType(node);
    }

    // Binary expressions
    if (t.isBinaryExpression(node)) {
      return this.inferBinaryType(node);
    }

    return { kind: 'unknown', name: 'unknown' };
  }

  // Resolve TypeScript type annotations
  private resolveTypeAnnotation(typeNode: t.TSType): Type {
    if (t.isTSStringKeyword(typeNode)) {
      return { kind: 'primitive', name: 'string' };
    }
    if (t.isTSNumberKeyword(typeNode)) {
      return { kind: 'primitive', name: 'number' };
    }
    if (t.isTSBooleanKeyword(typeNode)) {
      return { kind: 'primitive', name: 'boolean' };
    }
    if (t.isTSVoidKeyword(typeNode)) {
      return { kind: 'primitive', name: 'void' };
    }
    if (t.isTSNullKeyword(typeNode)) {
      return { kind: 'primitive', name: 'null' };
    }
    if (t.isTSUndefinedKeyword(typeNode)) {
      return { kind: 'primitive', name: 'undefined' };
    }
    if (t.isTSAnyKeyword(typeNode)) {
      return { kind: 'primitive', name: 'any' };
    }

    // Array type
    if (t.isTSArrayType(typeNode)) {
      return {
        kind: 'array',
        name: 'Array',
        elementType: this.resolveTypeAnnotation(typeNode.elementType),
      };
    }

    // Union type
    if (t.isTSUnionType(typeNode)) {
      const types = typeNode.types.map(t => this.resolveTypeAnnotation(t));
      return { kind: 'union', name: types.map(t => t.name).join(' | '), parameters: types };
    }

    // Intersection type
    if (t.isTSIntersectionType(typeNode)) {
      const types = typeNode.types.map(t => this.resolveTypeAnnotation(t));
      return { kind: 'intersection', name: types.map(t => t.name).join(' & '), parameters: types };
    }

    // Type reference
    if (t.isTSTypeReference(typeNode) && t.isIdentifier(typeNode.typeName)) {
      const name = typeNode.typeName.name;

      // Check for generic parameters
      if (typeNode.typeParameters) {
        const parameters = typeNode.typeParameters.params.map(p =>
          this.resolveTypeAnnotation(p)
        );
        return { kind: 'generic', name, parameters };
      }

      // Look up type in symbol table
      const entry = this.symbolTable.lookup(name, 'type');
      if (entry?.type) {
        return entry.type;
      }

      return { kind: 'unknown', name };
    }

    // Function type
    if (t.isTSFunctionType(typeNode)) {
      const returnType = typeNode.typeAnnotation
        ? this.resolveTypeAnnotation(typeNode.typeAnnotation.typeAnnotation)
        : { kind: 'unknown' as const, name: 'unknown' };

      return { kind: 'function', name: 'Function', returnType };
    }

    return { kind: 'unknown', name: 'unknown' };
  }

  private inferFunctionType(node: t.FunctionExpression | t.ArrowFunctionExpression): Type {
    let returnType: Type = { kind: 'unknown', name: 'unknown' };

    // Check return type annotation
    if (node.returnType && t.isTSTypeAnnotation(node.returnType)) {
      returnType = this.resolveTypeAnnotation(node.returnType.typeAnnotation);
    }

    return { kind: 'function', name: 'Function', returnType };
  }

  private inferCallType(node: t.CallExpression): Type {
    if (t.isIdentifier(node.callee)) {
      const entry = this.symbolTable.lookup(node.callee.name);
      if (entry?.type?.returnType) {
        return entry.type.returnType;
      }
    }
    return { kind: 'unknown', name: 'unknown' };
  }

  private inferMemberType(node: t.MemberExpression): Type {
    const objectType = t.isExpression(node.object) ? this.inferType(node.object) : null;

    if (objectType?.properties && t.isIdentifier(node.property)) {
      const propType = objectType.properties.get(node.property.name);
      if (propType) return propType;
    }

    return { kind: 'unknown', name: 'unknown' };
  }

  private inferBinaryType(node: t.BinaryExpression): Type {
    const operator = node.operator;

    // Comparison operators return boolean
    if (['===', '!==', '==', '!=', '<', '>', '<=', '>='].includes(operator)) {
      return { kind: 'primitive', name: 'boolean' };
    }

    // Numeric operators
    if (['+', '-', '*', '/', '%'].includes(operator)) {
      const leftType = t.isExpression(node.left) ? this.inferType(node.left) : null;
      const rightType = this.inferType(node.right);

      // String concatenation
      if (operator === '+' && (leftType?.name === 'string' || rightType.name === 'string')) {
        return { kind: 'primitive', name: 'string' };
      }

      return { kind: 'primitive', name: 'number' };
    }

    return { kind: 'unknown', name: 'unknown' };
  }

  private unifyTypes(types: Type[]): Type {
    if (types.length === 0) return { kind: 'unknown', name: 'unknown' };
    if (types.length === 1) return types[0];

    // Check if all types are the same
    const first = types[0];
    const allSame = types.every(t => t.name === first.name);
    if (allSame) return first;

    // Return union type
    return {
      kind: 'union',
      name: types.map(t => t.name).join(' | '),
      parameters: types,
    };
  }
}
```

## Summary

In this chapter, you've learned:

- **Symbol Tables**: Hierarchical scope-based symbol storage
- **Scope Building**: Traversing AST to build scope structure
- **Symbol Lookup**: Resolving identifiers to definitions
- **Type Inference**: Determining types from expressions
- **Type Annotations**: Processing TypeScript type syntax

## Key Takeaways

1. **Scopes are hierarchical**: Child scopes inherit from parents
2. **Hoisting matters**: Functions and vars behave differently
3. **Type inference**: Derive types from usage context
4. **Caching helps**: Store resolved types for performance
5. **Unions and intersections**: Handle complex type combinations

## Next Steps

Now that we can resolve symbols and types, let's build cross-reference and code search features in Chapter 4: Code Intelligence.

---

**Ready for Chapter 4?** [Code Intelligence](04-code-intelligence.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
