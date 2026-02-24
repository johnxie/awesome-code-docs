---
layout: default
title: "Chapter 3: Tree Data Structures"
nav_order: 3
has_children: false
parent: "Obsidian Outliner Plugin"
---

# Chapter 3: Tree Data Structures

Welcome to **Chapter 3: Tree Data Structures**. In this part of **Obsidian Outliner Plugin: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Efficient hierarchical content management with advanced tree algorithms

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- Tree data structures for representing hierarchical content
- Efficient tree traversal and manipulation algorithms
- Performance optimization for large outlines
- Serialization and persistence of tree structures
- Conflict resolution for concurrent modifications

## 🌳 Tree Data Structure Fundamentals

### **Outline Tree Representation**

The Outliner plugin uses a tree structure to represent hierarchical content, where each node represents a list item and edges represent parent-child relationships.

```typescript
// Core tree node structure
class OutlineNode {
  id: string;
  content: string;
  level: number;
  children: OutlineNode[] = [];
  parent: OutlineNode | null = null;
  collapsed: boolean = false;
  metadata: NodeMetadata = {};

  constructor(content: string = '', level: number = 0) {
    this.id = generateId();
    this.content = content;
    this.level = level;
  }

  // Tree navigation methods
  getRoot(): OutlineNode {
    let node: OutlineNode = this;
    while (node.parent) {
      node = node.parent;
    }
    return node;
  }

  getDepth(): number {
    let depth = 0;
    let node: OutlineNode = this;
    while (node.parent) {
      depth++;
      node = node.parent;
    }
    return depth;
  }

  getSiblings(): OutlineNode[] {
    if (!this.parent) return [];
    return this.parent.children.filter(child => child !== this);
  }

  getPreviousSibling(): OutlineNode | null {
    if (!this.parent) return null;
    const index = this.parent.children.indexOf(this);
    return index > 0 ? this.parent.children[index - 1] : null;
  }

  getNextSibling(): OutlineNode | null {
    if (!this.parent) return null;
    const index = this.parent.children.indexOf(this);
    return index < this.parent.children.length - 1 ? this.parent.children[index + 1] : null;
  }

  // Tree modification methods
  addChild(child: OutlineNode, index: number = -1): void {
    child.parent = this;
    child.level = this.level + 1;

    if (index === -1) {
      this.children.push(child);
    } else {
      this.children.splice(index, 0, child);
    }

    // Update levels recursively
    this.updateChildLevels(child);
  }

  removeChild(child: OutlineNode): boolean {
    const index = this.children.indexOf(child);
    if (index === -1) return false;

    this.children.splice(index, 1);
    child.parent = null;
    return true;
  }

  moveTo(newParent: OutlineNode, index: number = -1): void {
    if (this.parent) {
      this.parent.removeChild(this);
    }

    newParent.addChild(this, index);
  }

  private updateChildLevels(node: OutlineNode): void {
    for (const child of node.children) {
      child.level = node.level + 1;
      this.updateChildLevels(child);
    }
  }
}

interface NodeMetadata {
  created?: Date;
  modified?: Date;
  tags?: string[];
  priority?: number;
  dueDate?: Date;
  completed?: boolean;
  [key: string]: any;
}
```

### **Tree Builder and Parser**

```typescript
// Tree construction from markdown content
class OutlineTreeBuilder {
  buildTree(content: string): OutlineNode {
    const lines = content.split('\n');
    const root = new OutlineNode('root', -1);

    let currentPath: OutlineNode[] = [root];
    let currentLevel = -1;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      const listInfo = ListParser.getListInfo(line);
      if (!listInfo) continue;

      const level = Math.floor(listInfo.indent / 2);
      const node = new OutlineNode(listInfo.content, level);

      // Add metadata from parsing
      if (listInfo.type === 'checkbox') {
        node.metadata.completed = listInfo.checked;
      }

      // Find correct parent
      while (currentPath.length > level + 1) {
        currentPath.pop();
      }

      const parent = currentPath[currentPath.length - 1];
      parent.addChild(node);

      // Update path
      currentPath = currentPath.slice(0, level + 1);
      currentPath.push(node);
    }

    return root;
  }

  serializeTree(root: OutlineNode): string {
    const lines: string[] = [];

    function traverse(node: OutlineNode) {
      if (node.level >= 0) { // Skip root
        const indent = '  '.repeat(node.level);
        let marker = '-';

        // Add checkbox if completed status exists
        if (node.metadata.completed !== undefined) {
          marker = `- [${node.metadata.completed ? 'x' : ' '}]`;
        }

        lines.push(`${indent}${marker} ${node.content}`);
      }

      for (const child of node.children) {
        traverse(child);
      }
    }

    traverse(root);
    return lines.join('\n');
  }
}
```

## 🔍 Tree Traversal Algorithms

### **Depth-First Traversal**

```typescript
// Depth-first tree traversal
class TreeTraverser {
  // Pre-order traversal: root, then children
  traversePreOrder(node: OutlineNode, callback: (node: OutlineNode) => void): void {
    callback(node);
    for (const child of node.children) {
      this.traversePreOrder(child, callback);
    }
  }

  // Post-order traversal: children, then root
  traversePostOrder(node: OutlineNode, callback: (node: OutlineNode) => void): void {
    for (const child of node.children) {
      this.traversePostOrder(child, callback);
    }
    callback(node);
  }

  // In-order traversal for binary trees (adapted for outlines)
  traverseInOrder(node: OutlineNode, callback: (node: OutlineNode) => void): void {
    if (node.children.length > 0) {
      // Visit first child
      this.traverseInOrder(node.children[0], callback);
    }

    // Visit current node
    callback(node);

    // Visit remaining children
    for (let i = 1; i < node.children.length; i++) {
      this.traverseInOrder(node.children[i], callback);
    }
  }

  // Level-order traversal (breadth-first)
  traverseLevelOrder(root: OutlineNode, callback: (node: OutlineNode) => void): void {
    const queue: OutlineNode[] = [root];

    while (queue.length > 0) {
      const node = queue.shift()!;
      callback(node);

      for (const child of node.children) {
        queue.push(child);
      }
    }
  }

  // Find node by criteria
  findNode(root: OutlineNode, predicate: (node: OutlineNode) => boolean): OutlineNode | null {
    let result: OutlineNode | null = null;

    this.traversePreOrder(root, (node) => {
      if (!result && predicate(node)) {
        result = node;
      }
    });

    return result;
  }

  // Find all nodes matching criteria
  findAllNodes(root: OutlineNode, predicate: (node: OutlineNode) => boolean): OutlineNode[] {
    const results: OutlineNode[] = [];

    this.traversePreOrder(root, (node) => {
      if (predicate(node)) {
        results.push(node);
      }
    });

    return results;
  }

  // Get path from root to node
  getPathToNode(root: OutlineNode, targetNode: OutlineNode): OutlineNode[] {
    const path: OutlineNode[] = [];

    function findPath(current: OutlineNode): boolean {
      path.push(current);

      if (current === targetNode) {
        return true;
      }

      for (const child of current.children) {
        if (findPath(child)) {
          return true;
        }
      }

      path.pop();
      return false;
    }

    findPath(root);
    return path;
  }
}
```

### **Tree Query and Search**

```typescript
// Advanced tree querying
class TreeQueryEngine {
  constructor(private tree: OutlineTree) {}

  // Find nodes by content
  searchByContent(query: string, caseSensitive: boolean = false): OutlineNode[] {
    const flags = caseSensitive ? 'g' : 'gi';
    const regex = new RegExp(query, flags);

    return this.tree.findAllNodes(node => regex.test(node.content));
  }

  // Find nodes by metadata
  searchByMetadata(key: string, value: any): OutlineNode[] {
    return this.tree.findAllNodes(node =>
      node.metadata && node.metadata[key] === value
    );
  }

  // Find nodes by level
  getNodesAtLevel(level: number): OutlineNode[] {
    return this.tree.findAllNodes(node => node.level === level);
  }

  // Find leaf nodes (nodes with no children)
  getLeafNodes(): OutlineNode[] {
    return this.tree.findAllNodes(node => node.children.length === 0);
  }

  // Find nodes with specific child count
  getNodesWithChildCount(count: number): OutlineNode[] {
    return this.tree.findAllNodes(node => node.children.length === count);
  }

  // Complex query with multiple conditions
  query(conditions: QueryCondition[]): OutlineNode[] {
    return this.tree.findAllNodes(node => {
      return conditions.every(condition => {
        switch (condition.type) {
          case 'content':
            return this.matchContent(node.content, condition);
          case 'level':
            return this.matchLevel(node.level, condition);
          case 'metadata':
            return this.matchMetadata(node.metadata, condition);
          case 'children':
            return this.matchChildren(node.children, condition);
          default:
            return false;
        }
      });
    });
  }

  private matchContent(content: string, condition: QueryCondition): boolean {
    const { operator, value } = condition;
    const query = value.toString();

    switch (operator) {
      case 'contains':
        return content.toLowerCase().includes(query.toLowerCase());
      case 'startsWith':
        return content.toLowerCase().startsWith(query.toLowerCase());
      case 'endsWith':
        return content.toLowerCase().endsWith(query.toLowerCase());
      case 'equals':
        return content === query;
      default:
        return false;
    }
  }

  private matchLevel(level: number, condition: QueryCondition): boolean {
    const { operator, value } = condition;

    switch (operator) {
      case 'equals':
        return level === value;
      case 'greaterThan':
        return level > value;
      case 'lessThan':
        return level < value;
      default:
        return false;
    }
  }

  private matchMetadata(metadata: NodeMetadata, condition: QueryCondition): boolean {
    const { key, operator, value } = condition;

    if (!metadata || !(key in metadata)) return false;

    const metaValue = metadata[key];

    switch (operator) {
      case 'equals':
        return metaValue === value;
      case 'contains':
        return String(metaValue).toLowerCase().includes(String(value).toLowerCase());
      default:
        return false;
    }
  }

  private matchChildren(children: OutlineNode[], condition: QueryCondition): boolean {
    const { operator, value } = condition;

    switch (operator) {
      case 'count':
        return children.length === value;
      case 'greaterThan':
        return children.length > value;
      case 'lessThan':
        return children.length < value;
      default:
        return false;
    }
  }
}

interface QueryCondition {
  type: 'content' | 'level' | 'metadata' | 'children';
  operator: string;
  value: any;
  key?: string; // For metadata queries
}
```

## ⚡ Performance Optimization

### **Efficient Tree Operations**

```typescript
// Optimized tree operations
class OptimizedTreeOperations {
  private nodeMap: Map<string, OutlineNode> = new Map();
  private contentIndex: Map<string, OutlineNode[]> = new Map();

  // Build indexes for fast lookups
  buildIndexes(root: OutlineNode): void {
    this.nodeMap.clear();
    this.contentIndex.clear();

    const traverser = new TreeTraverser();
    traverser.traversePreOrder(root, (node) => {
      this.nodeMap.set(node.id, node);

      // Index by words in content
      const words = node.content.toLowerCase().split(/\s+/);
      for (const word of words) {
        if (!this.contentIndex.has(word)) {
          this.contentIndex.set(word, []);
        }
        this.contentIndex.get(word)!.push(node);
      }
    });
  }

  // Fast node lookup by ID
  getNodeById(id: string): OutlineNode | null {
    return this.nodeMap.get(id) || null;
  }

  // Fast content search using index
  searchContentIndexed(query: string): OutlineNode[] {
    const queryWords = query.toLowerCase().split(/\s+/);
    if (queryWords.length === 0) return [];

    // Start with first word results
    let results = this.contentIndex.get(queryWords[0]) || [];

    // Intersect with subsequent word results
    for (let i = 1; i < queryWords.length; i++) {
      const wordResults = this.contentIndex.get(queryWords[i]) || [];
      const wordSet = new Set(wordResults);
      results = results.filter(node => wordSet.has(node));
    }

    return results;
  }

  // Lazy loading for large trees
  class LazyOutlineNode extends OutlineNode {
    private loaded: boolean = false;
    private loadChildren: () => Promise<OutlineNode[]>;

    constructor(content: string, level: number, loadChildren: () => Promise<OutlineNode[]>) {
      super(content, level);
      this.loadChildren = loadChildren;
    }

    async getChildren(): Promise<OutlineNode[]> {
      if (!this.loaded) {
        this.children = await this.loadChildren();
        this.loaded = true;

        // Set parent references
        for (const child of this.children) {
          child.parent = this;
        }
      }
      return this.children;
    }

    // Override children getter
    get children(): OutlineNode[] {
      if (!this.loaded) {
        throw new Error('Children not loaded. Call getChildren() first.');
      }
      return super.children;
    }
  }

  // Memory-efficient tree building for large documents
  buildLargeTree(content: string, chunkSize: number = 1000): OutlineNode {
    const lines = content.split('\n');
    const root = new OutlineNode('root', -1);

    // Process in chunks to avoid memory spikes
    for (let i = 0; i < lines.length; i += chunkSize) {
      const chunk = lines.slice(i, i + chunkSize);
      this.processChunk(chunk, root);
    }

    return root;
  }

  private processChunk(chunk: string[], root: OutlineNode): void {
    let currentPath: OutlineNode[] = [root];
    let currentLevel = -1;

    for (const line of chunk) {
      if (!line.trim()) continue;

      const listInfo = ListParser.getListInfo(line);
      if (!listInfo) continue;

      const level = Math.floor(listInfo.indent / 2);
      const node = new OutlineNode(listInfo.content, level);

      // Find correct parent
      while (currentPath.length > level + 1) {
        currentPath.pop();
      }

      const parent = currentPath[currentPath.length - 1];
      parent.children.push(node);
      node.parent = parent;

      // Update path
      currentPath = currentPath.slice(0, level + 1);
      currentPath.push(node);
    }
  }
}
```

### **Tree Balancing and Optimization**

```typescript
// Tree balancing for performance
class TreeBalancer {
  // Check if tree needs balancing
  needsBalancing(node: OutlineNode, maxChildren: number = 10): boolean {
    return node.children.length > maxChildren ||
           node.children.some(child => this.needsBalancing(child, maxChildren));
  }

  // Balance tree by redistributing children
  balanceTree(node: OutlineNode, maxChildren: number = 10): void {
    if (node.children.length <= maxChildren) {
      // Balance children recursively
      for (const child of node.children) {
        this.balanceTree(child, maxChildren);
      }
      return;
    }

    // Split children into balanced groups
    const groups = this.createBalancedGroups(node.children, maxChildren);

    // Replace children with group nodes
    node.children = groups.map((group, index) => {
      const groupNode = new OutlineNode(`Group ${index + 1}`, node.level + 1);
      groupNode.children = group;
      group.forEach(child => child.parent = groupNode);
      return groupNode;
    });
  }

  private createBalancedGroups(nodes: OutlineNode[], maxSize: number): OutlineNode[][] {
    const groups: OutlineNode[][] = [];
    let currentGroup: OutlineNode[] = [];

    for (const node of nodes) {
      currentGroup.push(node);

      if (currentGroup.length >= maxSize) {
        groups.push(currentGroup);
        currentGroup = [];
      }
    }

    if (currentGroup.length > 0) {
      groups.push(currentGroup);
    }

    return groups;
  }

  // Optimize tree for search operations
  optimizeForSearch(node: OutlineNode): void {
    // Sort children by content for binary search
    node.children.sort((a, b) => a.content.localeCompare(b.content));

    // Recursively optimize children
    for (const child of node.children) {
      this.optimizeForSearch(child);
    }
  }

  // Compress tree by merging similar nodes
  compressTree(node: OutlineNode, similarityThreshold: number = 0.8): void {
    for (let i = 0; i < node.children.length - 1; i++) {
      for (let j = i + 1; j < node.children.length; j++) {
        const similarity = this.calculateSimilarity(
          node.children[i].content,
          node.children[j].content
        );

        if (similarity >= similarityThreshold) {
          // Merge similar nodes
          this.mergeNodes(node.children[i], node.children[j]);
          node.children.splice(j, 1);
          j--; // Adjust index after removal
        }
      }
    }

    // Recursively compress children
    for (const child of node.children) {
      this.compressTree(child, similarityThreshold);
    }
  }

  private calculateSimilarity(text1: string, text2: string): number {
    // Simple Jaccard similarity
    const words1 = new Set(text1.toLowerCase().split(/\s+/));
    const words2 = new Set(text2.toLowerCase().split(/\s+/));

    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);

    return intersection.size / union.size;
  }

  private mergeNodes(node1: OutlineNode, node2: OutlineNode): void {
    // Combine content
    node1.content = `${node1.content} / ${node2.content}`;

    // Merge children
    node1.children.push(...node2.children);
    node2.children.forEach(child => child.parent = node1);

    // Merge metadata
    node1.metadata = { ...node1.metadata, ...node2.metadata };
  }
}
```

## 🔄 Serialization and Persistence

### **Tree Serialization Formats**

```typescript
// Multiple serialization formats
class TreeSerializer {
  // JSON serialization
  toJSON(root: OutlineNode): string {
    return JSON.stringify(this.nodeToObject(root), null, 2);
  }

  fromJSON(json: string): OutlineNode {
    const obj = JSON.parse(json);
    return this.objectToNode(obj);
  }

  private nodeToObject(node: OutlineNode): any {
    return {
      id: node.id,
      content: node.content,
      level: node.level,
      collapsed: node.collapsed,
      metadata: node.metadata,
      children: node.children.map(child => this.nodeToObject(child))
    };
  }

  private objectToNode(obj: any): OutlineNode {
    const node = new OutlineNode(obj.content, obj.level);
    node.id = obj.id;
    node.collapsed = obj.collapsed || false;
    node.metadata = obj.metadata || {};

    node.children = obj.children.map((childObj: any) => {
      const child = this.objectToNode(childObj);
      child.parent = node;
      return child;
    });

    return node;
  }

  // Markdown serialization (optimized)
  toMarkdown(root: OutlineNode): string {
    const lines: string[] = [];

    function serializeNode(node: OutlineNode, prefix: string = '') {
      if (node.level < 0) { // Skip root
        node.children.forEach(child => serializeNode(child));
        return;
      }

      const indent = '  '.repeat(node.level);
      let marker = '-';

      if (node.metadata.completed !== undefined) {
        marker = `- [${node.metadata.completed ? 'x' : ' '}]`;
      }

      lines.push(`${indent}${marker} ${node.content}`);

      if (!node.collapsed) {
        node.children.forEach(child => serializeNode(child));
      }
    }

    serializeNode(root);
    return lines.join('\n');
  }

  // Compact binary serialization for large trees
  toBinary(root: OutlineNode): Uint8Array {
    const encoder = new TextEncoder();
    const data: Uint8Array[] = [];

    function serializeNode(node: OutlineNode) {
      // Node header: [level (1 byte)] [flags (1 byte)] [content length (2 bytes)]
      const flags = (node.collapsed ? 1 : 0) |
                   ((node.metadata.completed ? 1 : 0) << 1);

      const contentBytes = encoder.encode(node.content);
      const header = new Uint8Array(4);
      header[0] = node.level;
      header[1] = flags;
      new DataView(header.buffer).setUint16(2, contentBytes.length, true);

      data.push(header);
      data.push(contentBytes);

      // Serialize children count
      const childrenCount = new Uint8Array(2);
      new DataView(childrenCount.buffer).setUint16(0, node.children.length, true);
      data.push(childrenCount);

      // Serialize children
      node.children.forEach(child => serializeNode(child));
    }

    serializeNode(root);

    // Combine all data
    const totalLength = data.reduce((sum, arr) => sum + arr.length, 0);
    const result = new Uint8Array(totalLength);
    let offset = 0;

    for (const chunk of data) {
      result.set(chunk, offset);
      offset += chunk.length;
    }

    return result;
  }

  fromBinary(data: Uint8Array): OutlineNode {
    const decoder = new TextDecoder();
    let offset = 0;

    function deserializeNode(): OutlineNode {
      // Read header
      const level = data[offset++];
      const flags = data[offset++];
      const contentLength = new DataView(data.buffer, offset).getUint16(0, true);
      offset += 2;

      // Read content
      const contentBytes = data.slice(offset, offset + contentLength);
      const content = decoder.decode(contentBytes);
      offset += contentLength;

      // Create node
      const node = new OutlineNode(content, level);
      node.collapsed = (flags & 1) !== 0;
      node.metadata.completed = (flags & 2) !== 0;

      // Read children count
      const childrenCount = new DataView(data.buffer, offset).getUint16(0, true);
      offset += 2;

      // Read children
      for (let i = 0; i < childrenCount; i++) {
        const child = deserializeNode();
        node.addChild(child);
      }

      return node;
    }

    return deserializeNode();
  }
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 60 minutes**

1. **Implement Tree Operations**:
   - Build a tree from markdown content
   - Implement move, delete, and reorder operations
   - Add search and filtering capabilities

2. **Performance Optimization**:
   - Implement indexing for fast lookups
   - Add lazy loading for large trees
   - Profile and optimize traversal algorithms

3. **Advanced Features**:
   - Implement tree balancing and compression
   - Add serialization and persistence
   - Create a query engine for complex searches

---

**Ready for advanced features?** Continue to [Chapter 4: Advanced Features](04-advanced-features.md)

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `node`, `OutlineNode`, `children` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Tree Data Structures` as an operating subsystem inside **Obsidian Outliner Plugin: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `child`, `content`, `level` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Tree Data Structures` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `node`.
2. **Input normalization**: shape incoming data so `OutlineNode` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `children`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Obsidian Outliner](https://github.com/vslinko/obsidian-outliner)
  Why it matters: authoritative reference on `Obsidian Outliner` (github.com).

Suggested trace strategy:
- search upstream code for `node` and `OutlineNode` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Text Editing Implementation](02-text-editing.md)
- [Next Chapter: Chapter 4: Advanced Features](04-advanced-features.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
