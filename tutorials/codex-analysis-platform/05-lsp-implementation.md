---
layout: default
title: "Chapter 5: LSP Implementation"
parent: "Codex Analysis Platform"
nav_order: 5
---

# Chapter 5: LSP Implementation

Welcome to **Chapter 5: LSP Implementation**. In this part of **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build a Language Server Protocol server for editor integration.

## Overview

The Language Server Protocol (LSP) standardizes communication between editors and language tools. By implementing LSP, your analysis platform can integrate with VS Code, Vim, Emacs, and any LSP-compatible editor.

## LSP Architecture

### Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LSP Communication Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Editor (Client)                  Language Server              │
│   ┌─────────────────┐              ┌─────────────────┐         │
│   │                 │   Request    │                 │         │
│   │  textDocument/  │─────────────▶│  Handle         │         │
│   │  completion     │              │  Request        │         │
│   │                 │◀─────────────│                 │         │
│   │                 │   Response   │                 │         │
│   └─────────────────┘              └─────────────────┘         │
│                                                                 │
│   Common Messages:                                              │
│   ─────────────────                                             │
│   initialize           →  Server capabilities                   │
│   textDocument/didOpen →  Document opened                       │
│   textDocument/didChange → Content changed                      │
│   textDocument/hover   →  Hover information                     │
│   textDocument/definition → Go to definition                    │
│   textDocument/references → Find references                     │
│   textDocument/completion → Code completion                     │
│   textDocument/formatting → Format document                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Server Implementation

### Basic LSP Server

```typescript
// src/lsp/server.ts
import {
  createConnection,
  TextDocuments,
  ProposedFeatures,
  InitializeParams,
  InitializeResult,
  TextDocumentSyncKind,
  CompletionItem,
  CompletionItemKind,
  Hover,
  Definition,
  Location as LSPLocation,
  Range,
  Position,
  Diagnostic,
  DiagnosticSeverity,
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';
import { AnalysisEngine } from '../engine/AnalysisEngine';
import { SearchEngine } from '../intelligence/SearchEngine';
import { ReferenceTracker } from '../intelligence/ReferenceTracker';

// Create connection
const connection = createConnection(ProposedFeatures.all);

// Text document manager
const documents = new TextDocuments(TextDocument);

// Analysis components
let engine: AnalysisEngine;
let search: SearchEngine;
let refs: ReferenceTracker;

// Initialization
connection.onInitialize((params: InitializeParams): InitializeResult => {
  const workspaceFolder = params.workspaceFolders?.[0]?.uri;

  if (workspaceFolder) {
    const rootPath = new URL(workspaceFolder).pathname;

    // Initialize analysis engine
    engine = new AnalysisEngine({
      rootPath,
      languages: ['typescript', 'javascript'],
      excludePatterns: ['**/node_modules/**'],
      maxWorkers: 4,
      incrementalAnalysis: true,
    });

    search = new SearchEngine(engine.store);
    refs = new ReferenceTracker(engine.store);

    // Start engine
    engine.start().then(() => {
      connection.console.log('Analysis engine started');
    });
  }

  return {
    capabilities: {
      textDocumentSync: TextDocumentSyncKind.Incremental,
      completionProvider: {
        resolveProvider: true,
        triggerCharacters: ['.', '/', '@', '<'],
      },
      hoverProvider: true,
      definitionProvider: true,
      referencesProvider: true,
      documentSymbolProvider: true,
      workspaceSymbolProvider: true,
      codeActionProvider: true,
      renameProvider: {
        prepareProvider: true,
      },
      documentFormattingProvider: true,
      foldingRangeProvider: true,
    },
  };
});

// Document lifecycle
documents.onDidOpen((event) => {
  const filePath = uriToPath(event.document.uri);
  engine.analyzeFile(filePath);
});

documents.onDidChangeContent((change) => {
  const filePath = uriToPath(change.document.uri);
  const content = change.document.getText();

  // Re-analyze with new content
  engine.analyzeFileContent(filePath, content).then((result) => {
    if (result) {
      // Send diagnostics
      const diagnostics = result.diagnostics.map(d => toDiagnostic(d));
      connection.sendDiagnostics({
        uri: change.document.uri,
        diagnostics,
      });
    }
  });
});

documents.onDidClose((event) => {
  // Clear diagnostics when file closes
  connection.sendDiagnostics({
    uri: event.document.uri,
    diagnostics: [],
  });
});

// Start listening
documents.listen(connection);
connection.listen();
```

### Completion Provider

```typescript
// src/lsp/completion.ts
import {
  CompletionItem,
  CompletionItemKind,
  CompletionParams,
  InsertTextFormat,
} from 'vscode-languageserver/node';
import { Symbol, SymbolKind } from '../types';

connection.onCompletion((params: CompletionParams): CompletionItem[] => {
  const document = documents.get(params.textDocument.uri);
  if (!document) return [];

  const filePath = uriToPath(params.textDocument.uri);
  const position = params.position;

  // Get context around cursor
  const text = document.getText();
  const offset = document.offsetAt(position);
  const prefix = getWordAtPosition(text, offset);

  // Get symbols in scope
  const scope = engine.store.findScopeAt(filePath, position.line + 1, position.character);
  const symbols = scope ? scope.getAllSymbols() : [];

  // Filter by prefix
  const filtered = symbols.filter(s =>
    s.name.toLowerCase().startsWith(prefix.toLowerCase())
  );

  // Convert to completion items
  return filtered.map(s => symbolToCompletionItem(s));
});

connection.onCompletionResolve((item: CompletionItem): CompletionItem => {
  // Add additional details for selected item
  if (item.data?.symbolId) {
    const symbol = engine.store.getSymbolById(item.data.symbolId);
    if (symbol) {
      item.detail = symbol.signature || `${symbol.kind} ${symbol.name}`;
      item.documentation = symbol.documentation;
    }
  }
  return item;
});

function symbolToCompletionItem(symbol: Symbol): CompletionItem {
  return {
    label: symbol.name,
    kind: symbolKindToCompletionKind(symbol.kind),
    detail: symbol.signature,
    documentation: symbol.documentation,
    insertText: getInsertText(symbol),
    insertTextFormat: InsertTextFormat.Snippet,
    data: { symbolId: symbol.id },
  };
}

function symbolKindToCompletionKind(kind: SymbolKind): CompletionItemKind {
  switch (kind) {
    case 'class': return CompletionItemKind.Class;
    case 'interface': return CompletionItemKind.Interface;
    case 'function': return CompletionItemKind.Function;
    case 'method': return CompletionItemKind.Method;
    case 'property': return CompletionItemKind.Property;
    case 'variable': return CompletionItemKind.Variable;
    case 'constant': return CompletionItemKind.Constant;
    case 'enum': return CompletionItemKind.Enum;
    case 'type': return CompletionItemKind.TypeParameter;
    default: return CompletionItemKind.Text;
  }
}

function getInsertText(symbol: Symbol): string {
  if (symbol.kind === 'function' || symbol.kind === 'method') {
    // Add parameter placeholders
    return `${symbol.name}($1)$0`;
  }
  return symbol.name;
}

function getWordAtPosition(text: string, offset: number): string {
  let start = offset - 1;
  while (start >= 0 && /\w/.test(text[start])) {
    start--;
  }
  return text.substring(start + 1, offset);
}
```

### Hover Provider

```typescript
// src/lsp/hover.ts
import { Hover, HoverParams, MarkupContent, MarkupKind } from 'vscode-languageserver/node';

connection.onHover((params: HoverParams): Hover | null => {
  const document = documents.get(params.textDocument.uri);
  if (!document) return null;

  const filePath = uriToPath(params.textDocument.uri);
  const line = params.position.line + 1;
  const column = params.position.character;

  // Find symbol at position
  const symbol = engine.store.findSymbolAtPosition(filePath, line, column);

  if (!symbol) {
    // Check if it's a reference
    const ref = refs.findReferenceAtPosition(filePath, line, column);
    if (ref) {
      const targetSymbol = engine.store.getSymbolById(ref.targetId);
      if (targetSymbol) {
        return createHover(targetSymbol);
      }
    }
    return null;
  }

  return createHover(symbol);
});

function createHover(symbol: Symbol): Hover {
  const contents: MarkupContent = {
    kind: MarkupKind.Markdown,
    value: buildHoverContent(symbol),
  };

  return {
    contents,
    range: {
      start: {
        line: symbol.location.range.start.line - 1,
        character: symbol.location.range.start.column,
      },
      end: {
        line: symbol.location.range.end.line - 1,
        character: symbol.location.range.end.column,
      },
    },
  };
}

function buildHoverContent(symbol: Symbol): string {
  const parts: string[] = [];

  // Signature or declaration
  if (symbol.signature) {
    parts.push('```typescript');
    parts.push(symbol.signature);
    parts.push('```');
  } else {
    parts.push(`**${symbol.kind}** \`${symbol.name}\``);
  }

  // Documentation
  if (symbol.documentation) {
    parts.push('');
    parts.push(symbol.documentation);
  }

  // Location info
  parts.push('');
  parts.push(`*Defined in ${symbol.location.filePath}:${symbol.location.range.start.line}*`);

  return parts.join('\n');
}
```

### Definition and References

```typescript
// src/lsp/navigation.ts
import {
  Definition,
  DefinitionParams,
  Location as LSPLocation,
  ReferenceParams,
} from 'vscode-languageserver/node';

connection.onDefinition((params: DefinitionParams): Definition | null => {
  const filePath = uriToPath(params.textDocument.uri);
  const line = params.position.line + 1;
  const column = params.position.character;

  const location = refs.goToDefinition(filePath, line, column);

  if (!location) return null;

  return {
    uri: pathToUri(location.filePath),
    range: toRange(location.range),
  };
});

connection.onReferences((params: ReferenceParams): LSPLocation[] => {
  const filePath = uriToPath(params.textDocument.uri);
  const line = params.position.line + 1;
  const column = params.position.character;

  const result = refs.findReferencesAtPosition(filePath, line, column);

  if (!result) return [];

  const locations: LSPLocation[] = [];

  // Include definition if requested
  if (params.context.includeDeclaration) {
    locations.push({
      uri: pathToUri(result.definition.filePath),
      range: toRange(result.definition.range),
    });
  }

  // Add all references
  for (const ref of result.references) {
    locations.push({
      uri: pathToUri(ref.location.filePath),
      range: toRange(ref.location.range),
    });
  }

  return locations;
});

function toRange(range: Range): LSPRange {
  return {
    start: {
      line: range.start.line - 1,
      character: range.start.column,
    },
    end: {
      line: range.end.line - 1,
      character: range.end.column,
    },
  };
}
```

### Document Symbols

```typescript
// src/lsp/symbols.ts
import {
  DocumentSymbol,
  DocumentSymbolParams,
  SymbolKind as LSPSymbolKind,
  WorkspaceSymbolParams,
  SymbolInformation,
} from 'vscode-languageserver/node';

connection.onDocumentSymbol((params: DocumentSymbolParams): DocumentSymbol[] => {
  const filePath = uriToPath(params.textDocument.uri);
  const symbols = search.documentSymbols(filePath);

  // Build hierarchical structure
  return buildDocumentSymbolTree(symbols);
});

connection.onWorkspaceSymbol((params: WorkspaceSymbolParams): SymbolInformation[] => {
  const symbols = search.workspaceSymbols(params.query);

  return symbols.map(s => ({
    name: s.name,
    kind: symbolKindToLSPKind(s.kind),
    location: {
      uri: pathToUri(s.location.filePath),
      range: toRange(s.location.range),
    },
    containerName: s.parent ? engine.store.getSymbolById(s.parent)?.name : undefined,
  }));
});

function buildDocumentSymbolTree(symbols: Symbol[]): DocumentSymbol[] {
  const root: DocumentSymbol[] = [];
  const map = new Map<string, DocumentSymbol>();

  // First pass: create all symbols
  for (const symbol of symbols) {
    const docSymbol: DocumentSymbol = {
      name: symbol.name,
      kind: symbolKindToLSPKind(symbol.kind),
      range: toRange(symbol.location.range),
      selectionRange: toRange(symbol.location.range),
      children: [],
    };
    map.set(symbol.id, docSymbol);
  }

  // Second pass: build hierarchy
  for (const symbol of symbols) {
    const docSymbol = map.get(symbol.id)!;

    if (symbol.parent) {
      const parent = map.get(symbol.parent);
      if (parent) {
        parent.children!.push(docSymbol);
        continue;
      }
    }

    root.push(docSymbol);
  }

  return root;
}

function symbolKindToLSPKind(kind: SymbolKind): LSPSymbolKind {
  switch (kind) {
    case 'class': return LSPSymbolKind.Class;
    case 'interface': return LSPSymbolKind.Interface;
    case 'function': return LSPSymbolKind.Function;
    case 'method': return LSPSymbolKind.Method;
    case 'property': return LSPSymbolKind.Property;
    case 'variable': return LSPSymbolKind.Variable;
    case 'constant': return LSPSymbolKind.Constant;
    case 'enum': return LSPSymbolKind.Enum;
    case 'type': return LSPSymbolKind.TypeParameter;
    case 'module': return LSPSymbolKind.Module;
    default: return LSPSymbolKind.Variable;
  }
}
```

### Rename Support

```typescript
// src/lsp/rename.ts
import {
  PrepareRenameParams,
  RenameParams,
  WorkspaceEdit,
  TextEdit,
} from 'vscode-languageserver/node';

connection.onPrepareRename((params: PrepareRenameParams): Range | null => {
  const filePath = uriToPath(params.textDocument.uri);
  const line = params.position.line + 1;
  const column = params.position.character;

  // Check if position is on a renameable symbol
  const symbol = engine.store.findSymbolAtPosition(filePath, line, column);
  if (symbol) {
    return toRange(symbol.location.range);
  }

  const ref = refs.findReferenceAtPosition(filePath, line, column);
  if (ref) {
    return toRange(ref.location.range);
  }

  return null;
});

connection.onRenameRequest((params: RenameParams): WorkspaceEdit | null => {
  const filePath = uriToPath(params.textDocument.uri);
  const line = params.position.line + 1;
  const column = params.position.character;
  const newName = params.newName;

  // Find all locations to rename
  const result = refs.findReferencesAtPosition(filePath, line, column);
  if (!result) return null;

  const changes: { [uri: string]: TextEdit[] } = {};

  // Add definition location
  const defUri = pathToUri(result.definition.filePath);
  changes[defUri] = changes[defUri] || [];
  changes[defUri].push({
    range: toRange(result.definition.range),
    newText: newName,
  });

  // Add all reference locations
  for (const ref of result.references) {
    const uri = pathToUri(ref.location.filePath);
    changes[uri] = changes[uri] || [];
    changes[uri].push({
      range: toRange(ref.location.range),
      newText: newName,
    });
  }

  return { changes };
});
```

## VS Code Extension

### Package Configuration

```json
// package.json
{
  "name": "codex-analysis",
  "displayName": "Codex Analysis",
  "description": "Code analysis and intelligence",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.75.0"
  },
  "categories": ["Programming Languages"],
  "activationEvents": [
    "onLanguage:typescript",
    "onLanguage:javascript"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "configuration": {
      "title": "Codex Analysis",
      "properties": {
        "codex.maxWorkers": {
          "type": "number",
          "default": 4,
          "description": "Maximum number of analysis workers"
        },
        "codex.excludePatterns": {
          "type": "array",
          "default": ["**/node_modules/**"],
          "description": "Patterns to exclude from analysis"
        }
      }
    }
  },
  "dependencies": {
    "vscode-languageclient": "^8.0.0"
  }
}
```

### Extension Entry Point

```typescript
// src/extension.ts
import * as path from 'path';
import { workspace, ExtensionContext } from 'vscode';
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind,
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
  // Server module path
  const serverModule = context.asAbsolutePath(
    path.join('server', 'out', 'server.js')
  );

  // Server options
  const serverOptions: ServerOptions = {
    run: {
      module: serverModule,
      transport: TransportKind.ipc,
    },
    debug: {
      module: serverModule,
      transport: TransportKind.ipc,
      options: {
        execArgv: ['--nolazy', '--inspect=6009'],
      },
    },
  };

  // Client options
  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: 'file', language: 'typescript' },
      { scheme: 'file', language: 'javascript' },
    ],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher('**/*.{ts,js,tsx,jsx}'),
    },
  };

  // Create and start client
  client = new LanguageClient(
    'codexAnalysis',
    'Codex Analysis',
    serverOptions,
    clientOptions
  );

  client.start();
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
```

## Summary

In this chapter, you've learned:

- **LSP Protocol**: Communication between editors and servers
- **Server Implementation**: Building a complete LSP server
- **Core Features**: Completion, hover, definition, references
- **Document Symbols**: Outline and workspace symbol search
- **Rename Support**: Safe cross-file renaming
- **VS Code Extension**: Packaging for VS Code

## Key Takeaways

1. **LSP is standard**: Works with any compatible editor
2. **Incremental updates**: Handle document changes efficiently
3. **Hierarchical symbols**: Build proper outline trees
4. **Error handling**: Gracefully handle malformed input
5. **Performance**: Cache and index for fast responses

## Next Steps

Now that we have editor integration, let's build interactive visualization tools in Chapter 6: Visualization.

---

**Ready for Chapter 6?** [Visualization](06-visualization.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `symbol`, `engine`, `document` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: LSP Implementation` as an operating subsystem inside **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `CompletionItemKind`, `textDocument`, `connection` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: LSP Implementation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `symbol`.
2. **Input normalization**: shape incoming data so `engine` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `document`.
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
- search upstream code for `symbol` and `engine` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Code Intelligence](04-code-intelligence.md)
- [Next Chapter: Chapter 6: Visualization](06-visualization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
