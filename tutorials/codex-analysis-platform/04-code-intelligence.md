---
layout: default
title: "Chapter 4: Code Intelligence"
parent: "Codex Analysis Platform"
nav_order: 4
---

# Chapter 4: Code Intelligence

> Build cross-references, code search, and intelligent navigation features.

## Overview

Code intelligence features transform raw analysis data into actionable insights. This chapter covers building the features developers rely on daily: find references, go to definition, symbol search, and impact analysis.

## Cross-Reference System

### Reference Tracker

```typescript
// src/intelligence/ReferenceTracker.ts
import { Symbol, Reference, Location } from '../types';
import { AnalysisStore } from '../engine/store/AnalysisStore';

export interface ReferenceResult {
  symbol: Symbol;
  definition: Location;
  references: ReferenceLocation[];
  totalCount: number;
}

export interface ReferenceLocation {
  location: Location;
  kind: ReferenceKind;
  context: string;  // Line of code containing reference
}

type ReferenceKind = 'read' | 'write' | 'call' | 'import' | 'export' | 'type';

export class ReferenceTracker {
  private store: AnalysisStore;
  private referenceIndex: Map<string, Reference[]> = new Map();

  constructor(store: AnalysisStore) {
    this.store = store;
    this.buildIndex();
  }

  // Build index of all references by target symbol
  private buildIndex(): void {
    for (const result of this.store.getAllResults()) {
      for (const ref of result.references) {
        const existing = this.referenceIndex.get(ref.targetId) || [];
        existing.push(ref);
        this.referenceIndex.set(ref.targetId, existing);
      }
    }
  }

  // Find all references to a symbol
  findReferences(symbolId: string): ReferenceResult | null {
    const symbol = this.store.getSymbolById(symbolId);
    if (!symbol) return null;

    const refs = this.referenceIndex.get(symbolId) || [];

    const references: ReferenceLocation[] = refs.map(ref => ({
      location: ref.location,
      kind: ref.kind as ReferenceKind,
      context: this.getLineContext(ref.location),
    }));

    return {
      symbol,
      definition: symbol.location,
      references,
      totalCount: references.length,
    };
  }

  // Find references at a specific position
  findReferencesAtPosition(filePath: string, line: number, column: number): ReferenceResult | null {
    // Find symbol at position
    const symbol = this.store.findSymbolAtPosition(filePath, line, column);
    if (!symbol) {
      // Check if position is a reference itself
      const ref = this.findReferenceAtPosition(filePath, line, column);
      if (ref) {
        return this.findReferences(ref.targetId);
      }
      return null;
    }

    return this.findReferences(symbol.id);
  }

  // Get definition of symbol at position
  goToDefinition(filePath: string, line: number, column: number): Location | null {
    // First check if we're on a reference
    const ref = this.findReferenceAtPosition(filePath, line, column);
    if (ref) {
      const symbol = this.store.getSymbolById(ref.targetId);
      return symbol?.location || null;
    }

    // Check if we're on a symbol definition
    const symbol = this.store.findSymbolAtPosition(filePath, line, column);
    return symbol?.location || null;
  }

  // Find implementations (for interfaces/abstract classes)
  findImplementations(symbolId: string): Location[] {
    const symbol = this.store.getSymbolById(symbolId);
    if (!symbol || (symbol.kind !== 'interface' && symbol.kind !== 'class')) {
      return [];
    }

    const implementations: Location[] = [];

    // Find classes that implement/extend this symbol
    const refs = this.referenceIndex.get(symbolId) || [];
    for (const ref of refs) {
      if (ref.kind === 'implement' || ref.kind === 'extend') {
        // Find the class/interface that contains this reference
        const containingSymbol = this.store.findSymbolContaining(ref.location);
        if (containingSymbol) {
          implementations.push(containingSymbol.location);
        }
      }
    }

    return implementations;
  }

  private findReferenceAtPosition(filePath: string, line: number, column: number): Reference | null {
    const result = this.store.get(filePath);
    if (!result) return null;

    for (const ref of result.references) {
      if (this.positionInRange(line, column, ref.location.range)) {
        return ref;
      }
    }

    return null;
  }

  private positionInRange(line: number, column: number, range: Range): boolean {
    if (line < range.start.line || line > range.end.line) return false;
    if (line === range.start.line && column < range.start.column) return false;
    if (line === range.end.line && column > range.end.column) return false;
    return true;
  }

  private getLineContext(location: Location): string {
    // Get the line of code at this location
    return this.store.getLineContent(location.filePath, location.range.start.line);
  }
}
```

## Code Search

### Symbol Search Engine

```typescript
// src/intelligence/SearchEngine.ts
import Fuse from 'fuse.js';
import { Symbol, SymbolKind } from '../types';
import { AnalysisStore } from '../engine/store/AnalysisStore';

export interface SearchOptions {
  query: string;
  kinds?: SymbolKind[];
  files?: string[];
  limit?: number;
  fuzzy?: boolean;
}

export interface SearchResult {
  symbol: Symbol;
  score: number;
  matches: SearchMatch[];
}

export interface SearchMatch {
  field: string;
  indices: [number, number][];
}

export class SearchEngine {
  private store: AnalysisStore;
  private symbolIndex: Fuse<Symbol>;
  private lastIndexUpdate: number = 0;

  constructor(store: AnalysisStore) {
    this.store = store;
    this.buildIndex();

    // Rebuild index when store changes
    store.on('updated', () => this.buildIndex());
  }

  private buildIndex(): void {
    const symbols = this.store.getAllSymbols();

    this.symbolIndex = new Fuse(symbols, {
      keys: [
        { name: 'name', weight: 2 },
        { name: 'kind', weight: 0.5 },
        { name: 'documentation', weight: 1 },
        { name: 'signature', weight: 1 },
      ],
      threshold: 0.4,
      includeScore: true,
      includeMatches: true,
      minMatchCharLength: 2,
    });

    this.lastIndexUpdate = Date.now();
  }

  // Search for symbols
  search(options: SearchOptions): SearchResult[] {
    let results = this.symbolIndex.search(options.query);

    // Filter by kinds
    if (options.kinds && options.kinds.length > 0) {
      results = results.filter(r => options.kinds!.includes(r.item.kind));
    }

    // Filter by files
    if (options.files && options.files.length > 0) {
      results = results.filter(r =>
        options.files!.some(f => r.item.location.filePath.includes(f))
      );
    }

    // Apply limit
    const limit = options.limit || 50;
    results = results.slice(0, limit);

    return results.map(r => ({
      symbol: r.item,
      score: 1 - (r.score || 0),
      matches: r.matches?.map(m => ({
        field: m.key || '',
        indices: m.indices as [number, number][],
      })) || [],
    }));
  }

  // Search by exact name
  findByName(name: string, kind?: SymbolKind): Symbol[] {
    return this.store.querySymbols({ name, kind });
  }

  // Search by pattern (glob-like)
  findByPattern(pattern: string): Symbol[] {
    const regex = this.patternToRegex(pattern);
    const symbols = this.store.getAllSymbols();
    return symbols.filter(s => regex.test(s.name));
  }

  // Workspace symbol search (for LSP)
  workspaceSymbols(query: string): Symbol[] {
    if (query.length < 2) {
      return [];
    }

    const results = this.search({ query, limit: 100 });
    return results.map(r => r.symbol);
  }

  // Document symbols (for outline view)
  documentSymbols(filePath: string): Symbol[] {
    return this.store.querySymbols({ file: filePath });
  }

  private patternToRegex(pattern: string): RegExp {
    // Convert glob pattern to regex
    const escaped = pattern
      .replace(/[.+^${}()|[\]\\]/g, '\\$&')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');

    return new RegExp(`^${escaped}$`, 'i');
  }
}
```

### Full-Text Code Search

```typescript
// src/intelligence/CodeSearch.ts
export interface CodeSearchResult {
  filePath: string;
  line: number;
  column: number;
  content: string;
  matchStart: number;
  matchEnd: number;
}

export interface CodeSearchOptions {
  query: string;
  regex?: boolean;
  caseSensitive?: boolean;
  wholeWord?: boolean;
  includePatterns?: string[];
  excludePatterns?: string[];
  maxResults?: number;
}

export class CodeSearch {
  private fileContents: Map<string, string[]> = new Map();

  constructor() {}

  // Index file content for searching
  indexFile(filePath: string, content: string): void {
    this.fileContents.set(filePath, content.split('\n'));
  }

  // Remove file from index
  removeFile(filePath: string): void {
    this.fileContents.delete(filePath);
  }

  // Search across all indexed files
  search(options: CodeSearchOptions): CodeSearchResult[] {
    const results: CodeSearchResult[] = [];
    const maxResults = options.maxResults || 1000;

    const pattern = this.buildPattern(options);
    if (!pattern) return results;

    for (const [filePath, lines] of this.fileContents) {
      // Check include/exclude patterns
      if (!this.shouldSearch(filePath, options)) continue;

      for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
        const line = lines[lineIndex];
        let match: RegExpExecArray | null;

        // Reset regex for each line
        pattern.lastIndex = 0;

        while ((match = pattern.exec(line)) !== null) {
          results.push({
            filePath,
            line: lineIndex + 1,
            column: match.index + 1,
            content: line,
            matchStart: match.index,
            matchEnd: match.index + match[0].length,
          });

          if (results.length >= maxResults) {
            return results;
          }

          // Prevent infinite loop for zero-width matches
          if (match[0].length === 0) {
            pattern.lastIndex++;
          }
        }
      }
    }

    return results;
  }

  // Replace across files (preview)
  replacePreview(
    options: CodeSearchOptions,
    replacement: string
  ): { filePath: string; original: string; replaced: string }[] {
    const results = this.search(options);
    const pattern = this.buildPattern(options);
    if (!pattern) return [];

    const previews = new Map<string, { original: string; replaced: string }>();

    for (const result of results) {
      if (!previews.has(result.filePath)) {
        const lines = this.fileContents.get(result.filePath) || [];
        const original = lines.join('\n');
        const replaced = original.replace(pattern, replacement);
        previews.set(result.filePath, { original, replaced });
      }
    }

    return Array.from(previews.entries()).map(([filePath, content]) => ({
      filePath,
      ...content,
    }));
  }

  private buildPattern(options: CodeSearchOptions): RegExp | null {
    try {
      let pattern = options.query;

      if (!options.regex) {
        // Escape special regex characters
        pattern = pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      }

      if (options.wholeWord) {
        pattern = `\\b${pattern}\\b`;
      }

      const flags = options.caseSensitive ? 'g' : 'gi';
      return new RegExp(pattern, flags);
    } catch {
      return null;
    }
  }

  private shouldSearch(filePath: string, options: CodeSearchOptions): boolean {
    // Check exclude patterns
    if (options.excludePatterns) {
      for (const pattern of options.excludePatterns) {
        if (this.matchGlob(filePath, pattern)) {
          return false;
        }
      }
    }

    // Check include patterns
    if (options.includePatterns && options.includePatterns.length > 0) {
      for (const pattern of options.includePatterns) {
        if (this.matchGlob(filePath, pattern)) {
          return true;
        }
      }
      return false;
    }

    return true;
  }

  private matchGlob(path: string, pattern: string): boolean {
    const regex = new RegExp(
      '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$'
    );
    return regex.test(path);
  }
}
```

## Call Hierarchy

### Call Graph Builder

```typescript
// src/intelligence/CallHierarchy.ts
import { Symbol, Reference, Location } from '../types';
import { AnalysisStore } from '../engine/store/AnalysisStore';

export interface CallHierarchyItem {
  symbol: Symbol;
  calls: CallHierarchyItem[];      // Outgoing calls
  calledBy: CallHierarchyItem[];   // Incoming calls
}

export class CallHierarchy {
  private store: AnalysisStore;
  private callGraph: Map<string, Set<string>> = new Map();  // caller -> callees
  private reverseGraph: Map<string, Set<string>> = new Map();  // callee -> callers

  constructor(store: AnalysisStore) {
    this.store = store;
    this.buildCallGraph();
  }

  private buildCallGraph(): void {
    for (const result of this.store.getAllResults()) {
      for (const ref of result.references) {
        if (ref.kind !== 'call') continue;

        // Find the function containing this call
        const caller = this.store.findSymbolContaining(ref.location);
        if (!caller || (caller.kind !== 'function' && caller.kind !== 'method')) {
          continue;
        }

        // Add to call graph
        const callees = this.callGraph.get(caller.id) || new Set();
        callees.add(ref.targetId);
        this.callGraph.set(caller.id, callees);

        // Add to reverse graph
        const callers = this.reverseGraph.get(ref.targetId) || new Set();
        callers.add(caller.id);
        this.reverseGraph.set(ref.targetId, callers);
      }
    }
  }

  // Get outgoing calls from a function
  getOutgoingCalls(symbolId: string, depth: number = 1): CallHierarchyItem | null {
    const symbol = this.store.getSymbolById(symbolId);
    if (!symbol) return null;

    return this.buildOutgoingTree(symbol, depth, new Set());
  }

  // Get incoming calls to a function
  getIncomingCalls(symbolId: string, depth: number = 1): CallHierarchyItem | null {
    const symbol = this.store.getSymbolById(symbolId);
    if (!symbol) return null;

    return this.buildIncomingTree(symbol, depth, new Set());
  }

  private buildOutgoingTree(
    symbol: Symbol,
    depth: number,
    visited: Set<string>
  ): CallHierarchyItem {
    const item: CallHierarchyItem = {
      symbol,
      calls: [],
      calledBy: [],
    };

    if (depth <= 0 || visited.has(symbol.id)) {
      return item;
    }

    visited.add(symbol.id);

    const callees = this.callGraph.get(symbol.id) || new Set();
    for (const calleeId of callees) {
      const callee = this.store.getSymbolById(calleeId);
      if (callee) {
        item.calls.push(this.buildOutgoingTree(callee, depth - 1, visited));
      }
    }

    return item;
  }

  private buildIncomingTree(
    symbol: Symbol,
    depth: number,
    visited: Set<string>
  ): CallHierarchyItem {
    const item: CallHierarchyItem = {
      symbol,
      calls: [],
      calledBy: [],
    };

    if (depth <= 0 || visited.has(symbol.id)) {
      return item;
    }

    visited.add(symbol.id);

    const callers = this.reverseGraph.get(symbol.id) || new Set();
    for (const callerId of callers) {
      const caller = this.store.getSymbolById(callerId);
      if (caller) {
        item.calledBy.push(this.buildIncomingTree(caller, depth - 1, visited));
      }
    }

    return item;
  }
}
```

## Impact Analysis

### Change Impact Analyzer

```typescript
// src/intelligence/ImpactAnalyzer.ts
import { Symbol, Location } from '../types';
import { ReferenceTracker } from './ReferenceTracker';
import { CallHierarchy } from './CallHierarchy';

export interface ImpactResult {
  symbol: Symbol;
  directImpact: Location[];     // Direct references
  transitiveImpact: Location[]; // Through call hierarchy
  affectedFiles: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

export class ImpactAnalyzer {
  private refs: ReferenceTracker;
  private calls: CallHierarchy;

  constructor(refs: ReferenceTracker, calls: CallHierarchy) {
    this.refs = refs;
    this.calls = calls;
  }

  // Analyze impact of changing a symbol
  analyzeImpact(symbolId: string): ImpactResult | null {
    const refResult = this.refs.findReferences(symbolId);
    if (!refResult) return null;

    const directImpact = refResult.references.map(r => r.location);
    const transitiveImpact = this.getTransitiveImpact(symbolId);

    const allLocations = [...directImpact, ...transitiveImpact];
    const affectedFiles = [...new Set(allLocations.map(l => l.filePath))];

    return {
      symbol: refResult.symbol,
      directImpact,
      transitiveImpact,
      affectedFiles,
      riskLevel: this.calculateRisk(directImpact.length, transitiveImpact.length, affectedFiles.length),
    };
  }

  private getTransitiveImpact(symbolId: string): Location[] {
    const locations: Location[] = [];
    const visited = new Set<string>();

    const collectCallers = (id: string) => {
      if (visited.has(id)) return;
      visited.add(id);

      const hierarchy = this.calls.getIncomingCalls(id, 1);
      if (!hierarchy) return;

      for (const caller of hierarchy.calledBy) {
        locations.push(caller.symbol.location);
        collectCallers(caller.symbol.id);
      }
    };

    collectCallers(symbolId);
    return locations;
  }

  private calculateRisk(direct: number, transitive: number, files: number): 'low' | 'medium' | 'high' {
    const total = direct + transitive;

    if (total > 50 || files > 10) return 'high';
    if (total > 20 || files > 5) return 'medium';
    return 'low';
  }
}
```

## Summary

In this chapter, you've learned:

- **Reference Tracking**: Finding all uses of a symbol
- **Go to Definition**: Navigating from usage to declaration
- **Symbol Search**: Fast fuzzy search across codebase
- **Code Search**: Full-text search with regex support
- **Call Hierarchy**: Building and querying call graphs
- **Impact Analysis**: Assessing change impact

## Key Takeaways

1. **Indexing is crucial**: Build indexes for fast lookups
2. **Bidirectional references**: Track both directions
3. **Fuzzy search**: Users expect forgiving search
4. **Transitive analysis**: Follow the chain of dependencies
5. **Risk assessment**: Help developers understand impact

## Next Steps

Now that we have code intelligence, let's build an LSP server to integrate with editors in Chapter 5: LSP Implementation.

---

**Ready for Chapter 5?** [LSP Implementation](05-lsp-implementation.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
