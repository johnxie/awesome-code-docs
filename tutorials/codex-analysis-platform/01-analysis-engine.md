---
layout: default
title: "Chapter 1: Building the Analysis Engine"
parent: "Codex Analysis Platform"
nav_order: 1
---

# Chapter 1: Building the Analysis Engine

Welcome to **Chapter 1: Building the Analysis Engine**. In this part of **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Design and implement the core analysis engine for multi-language code analysis.

## Overview

The analysis engine is the heart of any code intelligence system. It coordinates parsing, symbol extraction, and analysis across multiple languages while maintaining performance and accuracy.

## Engine Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Analysis Engine Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    File Watcher                          │   │
│   │           (Monitors for file changes)                    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│                             ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                  Work Queue Manager                      │   │
│   │        (Prioritizes and schedules analysis)              │   │
│   └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│           ┌─────────────────┼─────────────────┐                │
│           ▼                 ▼                 ▼                │
│   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐       │
│   │   JS/TS       │ │   Python      │ │   Other       │       │
│   │   Analyzer    │ │   Analyzer    │ │   Analyzers   │       │
│   └───────────────┘ └───────────────┘ └───────────────┘       │
│           │                 │                 │                │
│           └─────────────────┼─────────────────┘                │
│                             ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                   Analysis Store                         │   │
│   │        (Caches results, indexes symbols)                 │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### Analysis Engine Class

```typescript
// src/engine/AnalysisEngine.ts
import { EventEmitter } from 'events';
import { FileWatcher } from './FileWatcher';
import { WorkQueue } from './WorkQueue';
import { AnalysisStore } from './store/AnalysisStore';
import { LanguageAnalyzer } from './analyzers/LanguageAnalyzer';

interface EngineConfig {
  rootPath: string;
  languages: string[];
  excludePatterns: string[];
  maxWorkers: number;
  incrementalAnalysis: boolean;
}

interface AnalysisResult {
  filePath: string;
  language: string;
  symbols: Symbol[];
  references: Reference[];
  diagnostics: Diagnostic[];
  timestamp: number;
}

export class AnalysisEngine extends EventEmitter {
  private config: EngineConfig;
  private watcher: FileWatcher;
  private workQueue: WorkQueue;
  private store: AnalysisStore;
  private analyzers: Map<string, LanguageAnalyzer>;
  private isRunning: boolean = false;

  constructor(config: EngineConfig) {
    super();
    this.config = config;
    this.analyzers = new Map();
    this.store = new AnalysisStore();
    this.workQueue = new WorkQueue(config.maxWorkers);
    this.watcher = new FileWatcher(config.rootPath, config.excludePatterns);

    this.initializeAnalyzers();
    this.setupWatcher();
  }

  // Initialize language-specific analyzers
  private initializeAnalyzers(): void {
    for (const lang of this.config.languages) {
      const analyzer = this.createAnalyzer(lang);
      if (analyzer) {
        this.analyzers.set(lang, analyzer);
      }
    }
  }

  private createAnalyzer(language: string): LanguageAnalyzer | null {
    switch (language) {
      case 'typescript':
      case 'javascript':
        return new TypeScriptAnalyzer();
      case 'python':
        return new PythonAnalyzer();
      default:
        console.warn(`No analyzer for language: ${language}`);
        return null;
    }
  }

  // Setup file watcher
  private setupWatcher(): void {
    this.watcher.on('change', (filePath: string) => {
      this.scheduleAnalysis(filePath, 'change');
    });

    this.watcher.on('add', (filePath: string) => {
      this.scheduleAnalysis(filePath, 'add');
    });

    this.watcher.on('unlink', (filePath: string) => {
      this.handleFileDelete(filePath);
    });
  }

  // Start the analysis engine
  async start(): Promise<void> {
    if (this.isRunning) return;

    this.isRunning = true;
    this.emit('started');

    // Initial full scan
    await this.performFullScan();

    // Start watching for changes
    this.watcher.start();

    this.emit('ready');
  }

  // Stop the analysis engine
  async stop(): Promise<void> {
    this.isRunning = false;
    this.watcher.stop();
    await this.workQueue.drain();
    this.emit('stopped');
  }

  // Perform initial full codebase scan
  private async performFullScan(): Promise<void> {
    this.emit('scan-started');

    const files = await this.watcher.getAllFiles();
    const total = files.length;
    let processed = 0;

    for (const file of files) {
      await this.analyzeFile(file);
      processed++;
      this.emit('scan-progress', { processed, total });
    }

    this.emit('scan-completed', { total: processed });
  }

  // Schedule file for analysis
  private scheduleAnalysis(filePath: string, reason: string): void {
    this.workQueue.enqueue({
      filePath,
      priority: this.getPriority(reason),
      task: () => this.analyzeFile(filePath)
    });
  }

  private getPriority(reason: string): number {
    switch (reason) {
      case 'user-request': return 1;  // Highest
      case 'change': return 2;
      case 'add': return 3;
      default: return 5;
    }
  }

  // Core analysis function
  async analyzeFile(filePath: string): Promise<AnalysisResult | null> {
    const language = this.detectLanguage(filePath);
    const analyzer = this.analyzers.get(language);

    if (!analyzer) {
      return null;
    }

    try {
      const startTime = Date.now();
      const content = await this.readFile(filePath);

      // Check cache for incremental analysis
      if (this.config.incrementalAnalysis) {
        const cached = this.store.get(filePath);
        if (cached && !this.hasChanged(content, cached)) {
          return cached;
        }
      }

      // Perform analysis
      const result = await analyzer.analyze(filePath, content);

      // Store results
      this.store.set(filePath, result);

      // Emit events
      this.emit('file-analyzed', {
        filePath,
        duration: Date.now() - startTime,
        symbolCount: result.symbols.length
      });

      return result;

    } catch (error) {
      this.emit('analysis-error', { filePath, error });
      return null;
    }
  }

  // Handle file deletion
  private handleFileDelete(filePath: string): void {
    this.store.delete(filePath);
    this.emit('file-removed', { filePath });
  }

  // Detect language from file extension
  private detectLanguage(filePath: string): string {
    const ext = filePath.split('.').pop()?.toLowerCase();
    const mapping: Record<string, string> = {
      'ts': 'typescript',
      'tsx': 'typescript',
      'js': 'javascript',
      'jsx': 'javascript',
      'py': 'python',
      'rb': 'ruby',
      'go': 'go',
      'rs': 'rust'
    };
    return mapping[ext || ''] || 'unknown';
  }

  // Query methods
  getSymbol(name: string): Symbol[] {
    return this.store.querySymbols({ name });
  }

  getReferences(symbol: Symbol): Reference[] {
    return this.store.queryReferences(symbol);
  }

  getDiagnostics(filePath?: string): Diagnostic[] {
    return this.store.queryDiagnostics(filePath);
  }
}
```

### Work Queue Management

```typescript
// src/engine/WorkQueue.ts
interface QueueItem {
  filePath: string;
  priority: number;
  task: () => Promise<any>;
}

export class WorkQueue {
  private queue: QueueItem[] = [];
  private activeWorkers: number = 0;
  private maxWorkers: number;
  private processing: boolean = false;

  constructor(maxWorkers: number = 4) {
    this.maxWorkers = maxWorkers;
  }

  enqueue(item: QueueItem): void {
    // Check for duplicate
    const existing = this.queue.findIndex(q => q.filePath === item.filePath);
    if (existing !== -1) {
      // Update priority if higher
      if (item.priority < this.queue[existing].priority) {
        this.queue[existing] = item;
      }
      return;
    }

    // Insert by priority
    const insertIndex = this.queue.findIndex(q => q.priority > item.priority);
    if (insertIndex === -1) {
      this.queue.push(item);
    } else {
      this.queue.splice(insertIndex, 0, item);
    }

    this.processQueue();
  }

  private async processQueue(): Promise<void> {
    if (this.processing) return;
    this.processing = true;

    while (this.queue.length > 0 && this.activeWorkers < this.maxWorkers) {
      const item = this.queue.shift();
      if (!item) continue;

      this.activeWorkers++;

      // Execute task without blocking
      item.task()
        .catch(error => console.error(`Task failed for ${item.filePath}:`, error))
        .finally(() => {
          this.activeWorkers--;
          this.processQueue();
        });
    }

    this.processing = false;
  }

  async drain(): Promise<void> {
    return new Promise(resolve => {
      const check = () => {
        if (this.queue.length === 0 && this.activeWorkers === 0) {
          resolve();
        } else {
          setTimeout(check, 100);
        }
      };
      check();
    });
  }

  get length(): number {
    return this.queue.length;
  }

  get active(): number {
    return this.activeWorkers;
  }
}
```

### File Watcher

```typescript
// src/engine/FileWatcher.ts
import * as chokidar from 'chokidar';
import * as glob from 'glob';
import * as path from 'path';
import { EventEmitter } from 'events';

export class FileWatcher extends EventEmitter {
  private watcher: chokidar.FSWatcher | null = null;
  private rootPath: string;
  private excludePatterns: string[];

  constructor(rootPath: string, excludePatterns: string[] = []) {
    super();
    this.rootPath = rootPath;
    this.excludePatterns = [
      '**/node_modules/**',
      '**/.git/**',
      '**/dist/**',
      '**/build/**',
      ...excludePatterns
    ];
  }

  start(): void {
    this.watcher = chokidar.watch(this.rootPath, {
      ignored: this.excludePatterns,
      persistent: true,
      ignoreInitial: true,
      awaitWriteFinish: {
        stabilityThreshold: 300,
        pollInterval: 100
      }
    });

    this.watcher
      .on('add', (filePath) => this.emit('add', filePath))
      .on('change', (filePath) => this.emit('change', filePath))
      .on('unlink', (filePath) => this.emit('unlink', filePath))
      .on('error', (error) => this.emit('error', error));
  }

  stop(): void {
    if (this.watcher) {
      this.watcher.close();
      this.watcher = null;
    }
  }

  async getAllFiles(): Promise<string[]> {
    const patterns = [
      '**/*.ts', '**/*.tsx',
      '**/*.js', '**/*.jsx',
      '**/*.py',
      '**/*.go',
      '**/*.rs'
    ];

    const files: string[] = [];

    for (const pattern of patterns) {
      const matches = await this.globAsync(
        path.join(this.rootPath, pattern),
        { ignore: this.excludePatterns }
      );
      files.push(...matches);
    }

    return [...new Set(files)]; // Deduplicate
  }

  private globAsync(pattern: string, options: glob.IOptions): Promise<string[]> {
    return new Promise((resolve, reject) => {
      glob(pattern, options, (err, matches) => {
        if (err) reject(err);
        else resolve(matches);
      });
    });
  }
}
```

## Analysis Store

### In-Memory Store with Indexing

```typescript
// src/engine/store/AnalysisStore.ts
import { Symbol, Reference, Diagnostic, AnalysisResult } from '../types';

interface SymbolIndex {
  byName: Map<string, Symbol[]>;
  byKind: Map<string, Symbol[]>;
  byFile: Map<string, Symbol[]>;
}

export class AnalysisStore {
  private results: Map<string, AnalysisResult> = new Map();
  private symbolIndex: SymbolIndex;

  constructor() {
    this.symbolIndex = {
      byName: new Map(),
      byKind: new Map(),
      byFile: new Map()
    };
  }

  set(filePath: string, result: AnalysisResult): void {
    // Remove old indexes
    const existing = this.results.get(filePath);
    if (existing) {
      this.removeFromIndexes(existing);
    }

    // Store result
    this.results.set(filePath, result);

    // Build indexes
    this.buildIndexes(result);
  }

  get(filePath: string): AnalysisResult | undefined {
    return this.results.get(filePath);
  }

  delete(filePath: string): void {
    const existing = this.results.get(filePath);
    if (existing) {
      this.removeFromIndexes(existing);
      this.results.delete(filePath);
    }
  }

  private buildIndexes(result: AnalysisResult): void {
    for (const symbol of result.symbols) {
      // Index by name
      const byName = this.symbolIndex.byName.get(symbol.name) || [];
      byName.push(symbol);
      this.symbolIndex.byName.set(symbol.name, byName);

      // Index by kind
      const byKind = this.symbolIndex.byKind.get(symbol.kind) || [];
      byKind.push(symbol);
      this.symbolIndex.byKind.set(symbol.kind, byKind);

      // Index by file
      const byFile = this.symbolIndex.byFile.get(result.filePath) || [];
      byFile.push(symbol);
      this.symbolIndex.byFile.set(result.filePath, byFile);
    }
  }

  private removeFromIndexes(result: AnalysisResult): void {
    for (const symbol of result.symbols) {
      // Remove from name index
      const byName = this.symbolIndex.byName.get(symbol.name);
      if (byName) {
        const filtered = byName.filter(s => s.id !== symbol.id);
        if (filtered.length > 0) {
          this.symbolIndex.byName.set(symbol.name, filtered);
        } else {
          this.symbolIndex.byName.delete(symbol.name);
        }
      }

      // Similar for other indexes...
    }

    this.symbolIndex.byFile.delete(result.filePath);
  }

  // Query methods
  querySymbols(query: { name?: string; kind?: string; file?: string }): Symbol[] {
    if (query.name) {
      return this.symbolIndex.byName.get(query.name) || [];
    }
    if (query.kind) {
      return this.symbolIndex.byKind.get(query.kind) || [];
    }
    if (query.file) {
      return this.symbolIndex.byFile.get(query.file) || [];
    }
    return [];
  }

  queryReferences(symbol: Symbol): Reference[] {
    const references: Reference[] = [];

    for (const [, result] of this.results) {
      for (const ref of result.references) {
        if (ref.targetId === symbol.id) {
          references.push(ref);
        }
      }
    }

    return references;
  }

  queryDiagnostics(filePath?: string): Diagnostic[] {
    if (filePath) {
      return this.results.get(filePath)?.diagnostics || [];
    }

    const allDiagnostics: Diagnostic[] = [];
    for (const [, result] of this.results) {
      allDiagnostics.push(...result.diagnostics);
    }
    return allDiagnostics;
  }

  // Statistics
  getStats(): { files: number; symbols: number; references: number } {
    let symbols = 0;
    let references = 0;

    for (const [, result] of this.results) {
      symbols += result.symbols.length;
      references += result.references.length;
    }

    return {
      files: this.results.size,
      symbols,
      references
    };
  }
}
```

## Type Definitions

```typescript
// src/engine/types.ts
export interface Position {
  line: number;
  column: number;
}

export interface Range {
  start: Position;
  end: Position;
}

export interface Location {
  filePath: string;
  range: Range;
}

export interface Symbol {
  id: string;
  name: string;
  kind: SymbolKind;
  location: Location;
  documentation?: string;
  signature?: string;
  modifiers?: string[];
  parent?: string;  // Parent symbol ID
  children?: string[];  // Child symbol IDs
}

export type SymbolKind =
  | 'class'
  | 'interface'
  | 'function'
  | 'method'
  | 'property'
  | 'variable'
  | 'constant'
  | 'parameter'
  | 'type'
  | 'enum'
  | 'module';

export interface Reference {
  id: string;
  targetId: string;  // The symbol being referenced
  location: Location;
  kind: ReferenceKind;
}

export type ReferenceKind =
  | 'read'
  | 'write'
  | 'call'
  | 'extend'
  | 'implement'
  | 'import'
  | 'type';

export interface Diagnostic {
  filePath: string;
  range: Range;
  message: string;
  severity: 'error' | 'warning' | 'info' | 'hint';
  code?: string;
  source?: string;
}

export interface AnalysisResult {
  filePath: string;
  language: string;
  symbols: Symbol[];
  references: Reference[];
  diagnostics: Diagnostic[];
  timestamp: number;
  contentHash: string;
}
```

## Summary

In this chapter, you've learned:

- **Engine Architecture**: Core components and their responsibilities
- **Work Queue**: Priority-based task scheduling
- **File Watching**: Efficient file change detection
- **Analysis Store**: In-memory storage with indexing
- **Type System**: Foundational types for analysis results

## Key Takeaways

1. **Modular design**: Separate concerns for maintainability
2. **Incremental analysis**: Only re-analyze what changed
3. **Priority scheduling**: User requests get processed first
4. **Efficient indexing**: Fast lookups for symbols and references
5. **Event-driven**: Components communicate via events

## Next Steps

Now that we have the core engine, let's dive into AST processing and manipulation in Chapter 2: AST Processing.

---

**Ready for Chapter 2?** [AST Processing](02-ast-processing.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `filePath`, `result`, `symbol` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Building the Analysis Engine` as an operating subsystem inside **Codex Analysis Platform Tutorial: Build Code Intelligence Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `void`, `watcher`, `symbolIndex` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Building the Analysis Engine` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `filePath`.
2. **Input normalization**: shape incoming data so `result` receives stable contracts.
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
- search upstream code for `filePath` and `result` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: AST Processing](02-ast-processing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
