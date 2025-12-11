---
layout: default
title: "Chapter 2: AST Processing and Manipulation"
nav_order: 2
has_children: false
parent: "Codex Code Analysis Platform"
---

# Chapter 2: AST Processing and Manipulation

> Deep dive into Abstract Syntax Tree processing, transformation, and analysis techniques

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- AST structure and traversal patterns
- Code transformation and rewriting techniques
- Static analysis algorithms and patterns
- AST-based code generation
- Performance optimization for AST processing

## 🌳 AST Fundamentals

### **Understanding AST Structure**

Abstract Syntax Trees represent the syntactic structure of source code:

```typescript
// JavaScript code
function greet(name) {
  return `Hello, ${name}!`;
}

// Corresponding AST (simplified)
{
  "type": "Program",
  "body": [
    {
      "type": "FunctionDeclaration",
      "id": {
        "type": "Identifier",
        "name": "greet"
      },
      "params": [
        {
          "type": "Identifier",
          "name": "name"
        }
      ],
      "body": {
        "type": "BlockStatement",
        "body": [
          {
            "type": "ReturnStatement",
            "argument": {
              "type": "TemplateLiteral",
              "quasis": [
                {
                  "type": "TemplateElement",
                  "value": { "raw": "Hello, ", "cooked": "Hello, " }
                },
                {
                  "type": "TemplateElement",
                  "value": { "raw": "!", "cooked": "!" }
                }
              ],
              "expressions": [
                {
                  "type": "Identifier",
                  "name": "name"
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
```

### **AST Node Types and Properties**

```typescript
// Common AST node interface
interface ASTNode {
  type: string;
  loc?: SourceLocation;
  range?: [number, number];
  [key: string]: any;
}

// Source location for error reporting
interface SourceLocation {
  start: Position;
  end: Position;
  source?: string;
}

interface Position {
  line: number;
  column: number;
}

// JavaScript/TypeScript AST node types
type JSNodeType =
  // Declarations
  | 'FunctionDeclaration'
  | 'VariableDeclaration'
  | 'ClassDeclaration'
  | 'ImportDeclaration'
  | 'ExportDeclaration'

  // Expressions
  | 'CallExpression'
  | 'MemberExpression'
  | 'BinaryExpression'
  | 'AssignmentExpression'
  | 'ArrowFunctionExpression'

  // Statements
  | 'BlockStatement'
  | 'IfStatement'
  | 'ForStatement'
  | 'WhileStatement'
  | 'TryStatement'

  // Literals
  | 'StringLiteral'
  | 'NumericLiteral'
  | 'BooleanLiteral'
  | 'NullLiteral'

  // Other
  | 'Identifier'
  | 'Program'
  | 'ExpressionStatement';
```

## 🔄 AST Traversal Patterns

### **Visitor Pattern Implementation**

```typescript
// AST visitor pattern for traversal
class ASTVisitor {
  private visitors: Map<string, VisitorFunction> = new Map();

  // Register visitor for specific node type
  on(nodeType: string, visitor: VisitorFunction): void {
    this.visitors.set(nodeType, visitor);
  }

  // Traverse AST starting from root
  traverse(node: ASTNode, context?: TraversalContext): void {
    if (!node || typeof node !== 'object') return;

    const context = context || { path: [], parent: null, scope: this.createScope() };

    // Call enter visitor if registered
    const visitor = this.visitors.get(node.type);
    if (visitor) {
      visitor(node, context);
    }

    // Recursively traverse child nodes
    this.traverseChildren(node, context);

    // Call exit visitor if implemented
    if (visitor && typeof visitor === 'object' && visitor.exit) {
      visitor.exit(node, context);
    }
  }

  private traverseChildren(node: ASTNode, context: TraversalContext): void {
    // Handle different node structures
    switch (node.type) {
      case 'Program':
        this.traverseNodeList(node.body, context, node);
        break;

      case 'FunctionDeclaration':
        this.traverseNode(node.id, { ...context, path: [...context.path, 'id'], parent: node });
        this.traverseNodeList(node.params, context, node);
        this.traverseNode(node.body, { ...context, path: [...context.path, 'body'], parent: node });
        break;

      case 'VariableDeclaration':
        this.traverseNodeList(node.declarations, context, node);
        break;

      case 'VariableDeclarator':
        this.traverseNode(node.id, { ...context, path: [...context.path, 'id'], parent: node });
        if (node.init) {
          this.traverseNode(node.init, { ...context, path: [...context.path, 'init'], parent: node });
        }
        break;

      case 'CallExpression':
        this.traverseNode(node.callee, { ...context, path: [...context.path, 'callee'], parent: node });
        this.traverseNodeList(node.arguments, context, node);
        break;

      case 'BinaryExpression':
        this.traverseNode(node.left, { ...context, path: [...context.path, 'left'], parent: node });
        this.traverseNode(node.right, { ...context, path: [...context.path, 'right'], parent: node });
        break;

      // Add cases for other node types as needed
      default:
        // Generic traversal for unknown node types
        this.traverseGeneric(node, context);
        break;
    }
  }

  private traverseNodeList(nodes: ASTNode[], context: TraversalContext, parent: ASTNode): void {
    if (!Array.isArray(nodes)) return;

    nodes.forEach((node, index) => {
      this.traverseNode(node, { ...context, path: [...context.path, index], parent });
    });
  }

  private traverseNode(node: ASTNode | null, context: TraversalContext): void {
    if (node) {
      this.traverse(node, context);
    }
  }

  private traverseGeneric(node: ASTNode, context: TraversalContext): void {
    // Generic traversal for nodes with unknown structure
    for (const [key, value] of Object.entries(node)) {
      if (key !== 'type' && key !== 'loc' && key !== 'range') {
        if (Array.isArray(value)) {
          this.traverseNodeList(value, context, node);
        } else if (this.isASTNode(value)) {
          this.traverseNode(value, { ...context, path: [...context.path, key], parent: node });
        }
      }
    }
  }

  private isASTNode(value: any): boolean {
    return value && typeof value === 'object' && 'type' in value;
  }

  private createScope(): Scope {
    return {
      variables: new Map(),
      functions: new Map(),
      classes: new Map(),
      parent: null
    };
  }
}

// Visitor function types
type VisitorFunction = ((node: ASTNode, context: TraversalContext) => void) | {
  enter?: (node: ASTNode, context: TraversalContext) => void;
  exit?: (node: ASTNode, context: TraversalContext) => void;
};

interface TraversalContext {
  path: (string | number)[];
  parent: ASTNode | null;
  scope: Scope;
}

interface Scope {
  variables: Map<string, VariableInfo>;
  functions: Map<string, FunctionInfo>;
  classes: Map<string, ClassInfo>;
  parent: Scope | null;
}
```

### **Tree Traversal Algorithms**

```typescript
// Depth-first traversal
class DepthFirstTraverser extends ASTVisitor {
  private results: TraversalResult[] = [];

  traverse(node: ASTNode, context?: TraversalContext): TraversalResult[] {
    this.results = [];
    super.traverse(node, context);
    return this.results;
  }

  // Override to collect results
  on(nodeType: string, visitor: VisitorFunction): void {
    const originalVisitor = this.visitors.get(nodeType);

    const wrappedVisitor: VisitorFunction = (node, context) => {
      // Call original visitor
      if (originalVisitor) {
        if (typeof originalVisitor === 'function') {
          originalVisitor(node, context);
        } else if (originalVisitor.enter) {
          originalVisitor.enter(node, context);
        }
      }

      // Collect result
      this.results.push({
        node,
        path: context.path,
        parent: context.parent,
        depth: context.path.length
      });

      // Call exit visitor
      if (originalVisitor && typeof originalVisitor === 'object' && originalVisitor.exit) {
        originalVisitor.exit(node, context);
      }
    };

    this.visitors.set(nodeType, wrappedVisitor);
  }
}

// Breadth-first traversal
class BreadthFirstTraverser {
  traverse(node: ASTNode): TraversalResult[] {
    const results: TraversalResult[] = [];
    const queue: Array<{ node: ASTNode; path: (string | number)[]; parent: ASTNode | null; depth: number }> = [];

    queue.push({ node, path: [], parent: null, depth: 0 });

    while (queue.length > 0) {
      const current = queue.shift()!;
      results.push({
        node: current.node,
        path: current.path,
        parent: current.parent,
        depth: current.depth
      });

      // Add children to queue
      const children = this.getChildNodes(current.node);
      children.forEach((child, index) => {
        queue.push({
          node: child,
          path: [...current.path, index],
          parent: current.node,
          depth: current.depth + 1
        });
      });
    }

    return results;
  }

  private getChildNodes(node: ASTNode): ASTNode[] {
    const children: ASTNode[] = [];

    // Extract child nodes based on node type
    switch (node.type) {
      case 'Program':
        if (node.body) children.push(...node.body);
        break;
      case 'FunctionDeclaration':
        if (node.id) children.push(node.id);
        if (node.params) children.push(...node.params);
        if (node.body) children.push(node.body);
        break;
      case 'CallExpression':
        if (node.callee) children.push(node.callee);
        if (node.arguments) children.push(...node.arguments);
        break;
      // Add more cases as needed
    }

    return children;
  }
}

// Query-based traversal
class QueryTraverser extends ASTVisitor {
  private queries: TraversalQuery[] = [];

  addQuery(query: TraversalQuery): void {
    this.queries.push(query);
  }

  find(query: TraversalQuery): ASTNode[] {
    const results: ASTNode[] = [];
    this.addQuery(query);

    this.on('Program', () => {}); // Register base visitor

    // Custom traversal that applies queries
    const customVisitor: VisitorFunction = (node, context) => {
      for (const query of this.queries) {
        if (this.matchesQuery(node, query, context)) {
          results.push(node);
        }
      }
    };

    // Temporarily replace visitor
    const originalVisitor = this.visitors.get('Program');
    this.visitors.set('Program', customVisitor);

    // Note: This is a simplified implementation
    // In practice, you'd need to traverse the entire tree

    return results;
  }

  private matchesQuery(node: ASTNode, query: TraversalQuery, context: TraversalContext): boolean {
    // Check node type
    if (query.type && node.type !== query.type) return false;

    // Check properties
    if (query.properties) {
      for (const [key, value] of Object.entries(query.properties)) {
        if (node[key] !== value) return false;
      }
    }

    // Check path
    if (query.path && !this.matchesPath(context.path, query.path)) return false;

    // Check custom predicate
    if (query.predicate && !query.predicate(node, context)) return false;

    return true;
  }

  private matchesPath(actualPath: (string | number)[], queryPath: PathPattern): boolean {
    if (queryPath.length !== actualPath.length) return false;

    for (let i = 0; i < queryPath.length; i++) {
      const querySegment = queryPath[i];
      const actualSegment = actualPath[i];

      if (typeof querySegment === 'string' && querySegment !== actualSegment) return false;
      if (typeof querySegment === 'number' && querySegment !== actualSegment) return false;
      // Handle wildcards and patterns if needed
    }

    return true;
  }
}

interface TraversalResult {
  node: ASTNode;
  path: (string | number)[];
  parent: ASTNode | null;
  depth: number;
}

interface TraversalQuery {
  type?: string;
  properties?: Record<string, any>;
  path?: PathPattern;
  predicate?: (node: ASTNode, context: TraversalContext) => boolean;
}

type PathPattern = (string | number | symbol)[];
```

## 🔄 AST Transformation and Rewriting

### **Code Transformation Framework**

```typescript
// AST transformation system
class ASTTransformer {
  private transforms: Map<string, TransformFunction> = new Map();

  // Register transformation for node type
  on(nodeType: string, transform: TransformFunction): void {
    this.transforms.set(nodeType, transform);
  }

  // Transform AST
  transform(ast: ASTNode): ASTNode {
    return this.transformNode(ast);
  }

  private transformNode(node: ASTNode): ASTNode {
    if (!node || typeof node !== 'object') return node;

    // Apply transformation if registered
    const transform = this.transforms.get(node.type);
    if (transform) {
      const transformedNode = transform(node, this.transformNode.bind(this));

      // If transformation returns null/undefined, remove the node
      if (!transformedNode) return null;

      // Continue transforming the result
      return this.transformNode(transformedNode);
    }

    // Recursively transform child nodes
    return this.transformChildren(node);
  }

  private transformChildren(node: ASTNode): ASTNode {
    const transformed = { ...node };

    // Transform based on node structure
    switch (node.type) {
      case 'Program':
        transformed.body = node.body.map(child => this.transformNode(child)).filter(Boolean);
        break;

      case 'FunctionDeclaration':
        if (node.id) transformed.id = this.transformNode(node.id);
        transformed.params = node.params.map(param => this.transformNode(param));
        transformed.body = this.transformNode(node.body);
        break;

      case 'CallExpression':
        transformed.callee = this.transformNode(node.callee);
        transformed.arguments = node.arguments.map(arg => this.transformNode(arg));
        break;

      case 'BinaryExpression':
        transformed.left = this.transformNode(node.left);
        transformed.operator = node.operator; // Don't transform operators
        transformed.right = this.transformNode(node.right);
        break;

      default:
        // Generic transformation for unknown nodes
        for (const [key, value] of Object.entries(node)) {
          if (Array.isArray(value)) {
            transformed[key] = value.map(item => this.transformNode(item)).filter(Boolean);
          } else if (this.isASTNode(value)) {
            transformed[key] = this.transformNode(value);
          }
        }
        break;
    }

    return transformed;
  }

  private isASTNode(value: any): boolean {
    return value && typeof value === 'object' && 'type' in value;
  }
}

// Transformation function type
type TransformFunction = (node: ASTNode, transformChild: (node: ASTNode) => ASTNode) => ASTNode | null;
```

### **Common Transformation Patterns**

```typescript
// Example transformations
class CommonTransformations {
  // Remove console.log statements
  static removeConsoleLogs(): TransformFunction {
    return (node, transformChild) => {
      if (node.type === 'CallExpression' &&
          node.callee.type === 'MemberExpression' &&
          node.callee.object.type === 'Identifier' &&
          node.callee.object.name === 'console') {
        // Remove console.log calls
        return null;
      }

      return transformChild(node);
    };
  }

  // Convert var to let/const
  static modernizeVariableDeclarations(): TransformFunction {
    return (node, transformChild) => {
      if (node.type === 'VariableDeclaration' && node.kind === 'var') {
        // Analyze usage to determine if should be let or const
        const isConst = this.analyzeVariableUsage(node);
        return {
          ...node,
          kind: isConst ? 'const' : 'let'
        };
      }

      return transformChild(node);
    };
  }

  // Add JSDoc comments
  static addJSDocComments(): TransformFunction {
    return (node, transformChild) => {
      if (node.type === 'FunctionDeclaration' && !this.hasJSDoc(node)) {
        const jsdoc = this.generateJSDoc(node);
        // Insert JSDoc comment before function
        return {
          type: 'Program',
          body: [
            {
              type: 'CommentBlock',
              value: `*\n${jsdoc}\n `,
              loc: node.loc
            },
            node
          ]
        };
      }

      return transformChild(node);
    };
  }

  // Convert promises to async/await
  static asyncifyPromises(): TransformFunction {
    return (node, transformChild) => {
      if (node.type === 'CallExpression' &&
          node.callee.type === 'MemberExpression' &&
          node.callee.property.name === 'then') {
        // Convert .then() chains to async/await
        return this.convertToAsyncAwait(node);
      }

      return transformChild(node);
    };
  }

  private static analyzeVariableUsage(node: ASTNode): boolean {
    // Analyze if variable is reassigned to determine const vs let
    // This is a simplified implementation
    return false; // Assume let for simplicity
  }

  private static hasJSDoc(node: ASTNode): boolean {
    // Check if function already has JSDoc
    return false; // Simplified
  }

  private static generateJSDoc(node: ASTNode): string {
    // Generate JSDoc comment
    return '* Function description'; // Simplified
  }

  private static convertToAsyncAwait(node: ASTNode): ASTNode {
    // Convert promise chains to async/await
    // This is complex and would require scope analysis
    return node; // Simplified
  }
}
```

## 🔍 Static Analysis Algorithms

### **Control Flow Analysis**

```typescript
// Control flow graph construction
class ControlFlowAnalyzer {
  analyze(ast: ASTNode): ControlFlowGraph {
    const graph = new ControlFlowGraph();
    this.buildCFG(ast, graph);
    return graph;
  }

  private buildCFG(node: ASTNode, graph: ControlFlowGraph): void {
    switch (node.type) {
      case 'Program':
        const entryBlock = graph.createBlock('entry');
        graph.setEntry(entryBlock);

        for (const stmt of node.body) {
          this.buildCFG(stmt, graph);
        }

        const exitBlock = graph.createBlock('exit');
        graph.setExit(exitBlock);
        break;

      case 'FunctionDeclaration':
        const funcBlock = graph.createBlock(`function_${node.id.name}`);
        this.buildCFG(node.body, graph);
        break;

      case 'IfStatement':
        const ifBlock = graph.createBlock('if_condition');
        const thenBlock = graph.createBlock('if_then');
        const elseBlock = node.alternate ? graph.createBlock('if_else') : null;

        // Connect condition to branches
        graph.addEdge(ifBlock, thenBlock, 'true');
        if (elseBlock) {
          graph.addEdge(ifBlock, elseBlock, 'false');
        }

        // Analyze branch bodies
        this.buildCFG(node.consequent, graph);
        if (node.alternate) {
          this.buildCFG(node.alternate, graph);
        }
        break;

      case 'ForStatement':
      case 'WhileStatement':
        const loopHeader = graph.createBlock('loop_header');
        const loopBody = graph.createBlock('loop_body');

        graph.addEdge(loopHeader, loopBody, 'enter');
        graph.addEdge(loopBody, loopHeader, 'continue');

        this.buildCFG(node.body, graph);
        break;

      case 'TryStatement':
        const tryBlock = graph.createBlock('try');
        const catchBlock = node.handler ? graph.createBlock('catch') : null;
        const finallyBlock = node.finalizer ? graph.createBlock('finally') : null;

        if (catchBlock) {
          graph.addEdge(tryBlock, catchBlock, 'exception');
        }
        if (finallyBlock) {
          graph.addEdge(tryBlock, finallyBlock, 'always');
          if (catchBlock) {
            graph.addEdge(catchBlock, finallyBlock, 'always');
          }
        }

        this.buildCFG(node.block, graph);
        if (node.handler) {
          this.buildCFG(node.handler.body, graph);
        }
        if (node.finalizer) {
          this.buildCFG(node.finalizer, graph);
        }
        break;

      default:
        // For other statements, create a basic block
        const block = graph.createBlock(`${node.type}_${node.loc?.start?.line || 'unknown'}`);
        graph.addStatement(block, node);
        break;
    }
  }
}

class ControlFlowGraph {
  private blocks: Map<string, BasicBlock> = new Map();
  private edges: CFEdge[] = [];
  private entryBlock: BasicBlock | null = null;
  private exitBlock: BasicBlock | null = null;

  createBlock(name: string): BasicBlock {
    const block = new BasicBlock(name);
    this.blocks.set(name, block);
    return block;
  }

  addEdge(from: BasicBlock, to: BasicBlock, label?: string): void {
    this.edges.push({ from: from.name, to: to.name, label });
  }

  setEntry(block: BasicBlock): void {
    this.entryBlock = block;
  }

  setExit(block: BasicBlock): void {
    this.exitBlock = block;
  }

  getBlocks(): BasicBlock[] {
    return Array.from(this.blocks.values());
  }

  getEdges(): CFEdge[] {
    return this.edges;
  }

  // Analysis methods
  computeDominators(): Map<string, Set<string>> {
    // Implement dominator analysis
    const dominators = new Map<string, Set<string>>();

    // Simplified implementation
    for (const block of this.getBlocks()) {
      dominators.set(block.name, new Set([block.name]));
    }

    return dominators;
  }

  findLoops(): Loop[] {
    // Implement loop detection using dominators
    const loops: Loop[] = [];
    // Simplified implementation
    return loops;
  }
}

class BasicBlock {
  constructor(public name: string) {}

  statements: ASTNode[] = [];

  addStatement(stmt: ASTNode): void {
    this.statements.push(stmt);
  }

  getStatements(): ASTNode[] {
    return this.statements;
  }
}

interface CFEdge {
  from: string;
  to: string;
  label?: string;
}

interface Loop {
  header: string;
  body: string[];
}
```

### **Data Flow Analysis**

```typescript
// Data flow analysis
class DataFlowAnalyzer {
  analyze(ast: ASTNode): DataFlowResult {
    const cfg = new ControlFlowAnalyzer().analyze(ast);

    return {
      reachingDefinitions: this.computeReachingDefinitions(cfg),
      liveVariables: this.computeLiveVariables(cfg),
      availableExpressions: this.computeAvailableExpressions(cfg),
      definiteAssignment: this.computeDefiniteAssignment(cfg)
    };
  }

  private computeReachingDefinitions(cfg: ControlFlowGraph): Map<string, Set<Definition>> {
    // Reaching definitions analysis
    const reachingDefs = new Map<string, Set<Definition>>();

    // Initialize
    for (const block of cfg.getBlocks()) {
      reachingDefs.set(block.name, new Set());
    }

    // Iterative data flow analysis
    let changed = true;
    while (changed) {
      changed = false;

      for (const block of cfg.getBlocks()) {
        const inSet = this.computeInSet(block, cfg, reachingDefs);
        const outSet = this.computeOutSet(block, inSet);

        if (!this.setsEqual(reachingDefs.get(block.name)!, outSet)) {
          reachingDefs.set(block.name, outSet);
          changed = true;
        }
      }
    }

    return reachingDefs;
  }

  private computeLiveVariables(cfg: ControlFlowGraph): Map<string, Set<string>> {
    // Live variables analysis (backward)
    const liveVars = new Map<string, Set<string>>();

    // Initialize
    for (const block of cfg.getBlocks()) {
      liveVars.set(block.name, new Set());
    }

    // Iterative analysis (backward)
    let changed = true;
    while (changed) {
      changed = false;

      for (const block of cfg.getBlocks().reverse()) {
        const outSet = this.computeLiveOutSet(block, cfg, liveVars);
        const inSet = this.computeLiveInSet(block, outSet);

        if (!this.setsEqual(liveVars.get(block.name)!, inSet)) {
          liveVars.set(block.name, inSet);
          changed = true;
        }
      }
    }

    return liveVars;
  }

  private computeAvailableExpressions(cfg: ControlFlowGraph): Map<string, Set<Expression>> {
    // Available expressions analysis
    const availableExprs = new Map<string, Set<Expression>>();

    // Initialize with all expressions available
    const allExpressions = this.extractExpressions(cfg);

    for (const block of cfg.getBlocks()) {
      availableExprs.set(block.name, new Set(allExpressions));
    }

    // Iterative analysis
    let changed = true;
    while (changed) {
      changed = false;

      for (const block of cfg.getBlocks()) {
        const inSet = this.computeExprInSet(block, cfg, availableExprs);
        const outSet = this.computeExprOutSet(block, inSet);

        if (!this.setsEqual(availableExprs.get(block.name)!, outSet)) {
          availableExprs.set(block.name, outSet);
          changed = true;
        }
      }
    }

    return availableExprs;
  }

  private computeDefiniteAssignment(cfg: ControlFlowGraph): Map<string, Set<string>> {
    // Definite assignment analysis
    const definiteAssignments = new Map<string, Set<string>>();

    // Initialize
    for (const block of cfg.getBlocks()) {
      definiteAssignments.set(block.name, new Set());
    }

    // Iterative analysis
    let changed = true;
    while (changed) {
      changed = false;

      for (const block of cfg.getBlocks()) {
        const inSet = this.computeDefInSet(block, cfg, definiteAssignments);
        const outSet = this.computeDefOutSet(block, inSet);

        if (!this.setsEqual(definiteAssignments.get(block.name)!, outSet)) {
          definiteAssignments.set(block.name, outSet);
          changed = true;
        }
      }
    }

    return definiteAssignments;
  }

  // Helper methods for data flow computations
  private computeInSet(block: BasicBlock, cfg: ControlFlowGraph, reachingDefs: Map<string, Set<Definition>>): Set<Definition> {
    const predecessors = this.getPredecessors(block, cfg);
    if (predecessors.length === 0) return new Set();

    const result = new Set(predecessors[0]);
    for (let i = 1; i < predecessors.length; i++) {
      this.setIntersection(result, predecessors[i]);
    }
    return result;
  }

  private computeOutSet(block: BasicBlock, inSet: Set<Definition>): Set<Definition> {
    const outSet = new Set(inSet);
    // Apply block's definitions and kills
    // This is simplified - real implementation would track definitions
    return outSet;
  }

  private setsEqual(a: Set<any>, b: Set<any>): boolean {
    if (a.size !== b.size) return false;
    for (const item of a) {
      if (!b.has(item)) return false;
    }
    return true;
  }

  private setIntersection(a: Set<any>, b: Set<any>): void {
    for (const item of a) {
      if (!b.has(item)) {
        a.delete(item);
      }
    }
  }

  private getPredecessors(block: BasicBlock, cfg: ControlFlowGraph): Set<Definition>[] {
    // Get predecessor blocks and their OUT sets
    return []; // Simplified
  }

  private extractExpressions(cfg: ControlFlowGraph): Expression[] {
    // Extract all expressions from the CFG
    return []; // Simplified
  }

  // Additional helper methods for other analyses...
}

interface Definition {
  variable: string;
  block: string;
  statement: number;
}

interface Expression {
  type: string;
  operands: string[];
}

interface DataFlowResult {
  reachingDefinitions: Map<string, Set<Definition>>;
  liveVariables: Map<string, Set<string>>;
  availableExpressions: Map<string, Set<Expression>>;
  definiteAssignment: Map<string, Set<string>>;
}
```

## 🚀 AST-Based Code Generation

### **Code Generation Framework**

```typescript
// AST to code generation
class CodeGenerator {
  private generators: Map<string, CodeGeneratorFunction> = new Map();

  registerGenerator(nodeType: string, generator: CodeGeneratorFunction): void {
    this.generators.set(nodeType, generator);
  }

  generate(node: ASTNode, options?: CodeGenOptions): string {
    const generator = this.generators.get(node.type);
    if (!generator) {
      throw new Error(`No code generator for node type: ${node.type}`);
    }

    return generator(node, this.generate.bind(this), options);
  }

  // Utility methods for code generation
  indent(code: string, level: number = 1): string {
    const indentStr = '  '.repeat(level);
    return code.split('\n').map(line => indentStr + line).join('\n');
  }

  joinCodeBlocks(blocks: string[], separator: string = '\n'): string {
    return blocks.filter(block => block.trim()).join(separator);
  }

  wrapInBraces(code: string): string {
    return `{\n${this.indent(code)}\n}`;
  }
}

// Default JavaScript code generators
class JavaScriptGenerators {
  static registerDefaults(generator: CodeGenerator): void {
    generator.registerGenerator('Program', JavaScriptGenerators.generateProgram);
    generator.registerGenerator('FunctionDeclaration', JavaScriptGenerators.generateFunctionDeclaration);
    generator.registerGenerator('VariableDeclaration', JavaScriptGenerators.generateVariableDeclaration);
    generator.registerGenerator('CallExpression', JavaScriptGenerators.generateCallExpression);
    generator.registerGenerator('BinaryExpression', JavaScriptGenerators.generateBinaryExpression);
    generator.registerGenerator('Identifier', JavaScriptGenerators.generateIdentifier);
    generator.registerGenerator('StringLiteral', JavaScriptGenerators.generateStringLiteral);
    generator.registerGenerator('NumericLiteral', JavaScriptGenerators.generateNumericLiteral);
  }

  static generateProgram(node: ASTNode, generateChild: CodeGeneratorFunction): string {
    const body = node.body.map(stmt => generateChild(stmt)).join('\n');
    return body;
  }

  static generateFunctionDeclaration(node: ASTNode, generateChild: CodeGeneratorFunction): string {
    const name = generateChild(node.id);
    const params = node.params.map(param => generateChild(param)).join(', ');
    const body = generateChild(node.body);

    return `function ${name}(${params}) ${body}`;
  }

  static generateVariableDeclaration(node: ASTNode, generateChild: CodeGeneratorFunction): string {
    const kind = node.kind;
    const declarations = node.declarations.map(decl => generateChild(decl)).join(', ');

    return `${kind} ${declarations};`;
  }

  static generateCallExpression(node: ASTNode, generateChild: CodeGeneratorFunction): string {
    const callee = generateChild(node.callee);
    const args = node.arguments.map(arg => generateChild(arg)).join(', ');

    return `${callee}(${args})`;
  }

  static generateBinaryExpression(node: ASTNode, generateChild: CodeGeneratorFunction): string {
    const left = generateChild(node.left);
    const operator = node.operator;
    const right = generateChild(node.right);

    return `${left} ${operator} ${right}`;
  }

  static generateIdentifier(node: ASTNode): string {
    return node.name;
  }

  static generateStringLiteral(node: ASTNode): string {
    return `"${node.value}"`;
  }

  static generateNumericLiteral(node: ASTNode): string {
    return node.value.toString();
  }
}

type CodeGeneratorFunction = (node: ASTNode, generateChild: CodeGeneratorFunction, options?: CodeGenOptions) => string;

interface CodeGenOptions {
  minify?: boolean;
  sourceMap?: boolean;
  target?: 'es5' | 'es6' | 'es2020';
  module?: 'commonjs' | 'esm';
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 90 minutes**

1. **AST Traversal**: Implement a visitor pattern to traverse JavaScript AST and collect all function declarations
2. **Code Transformation**: Create a transformer that converts `var` declarations to `let`/`const`
3. **Static Analysis**: Build a simple linter that detects unused variables
4. **Code Generation**: Implement a code generator that converts a simple AST back to JavaScript code
5. **Control Flow Analysis**: Create a tool that builds a control flow graph for a given function

---

**Ready for Language Server Protocol?** Continue to [Chapter 3: Language Server Protocol Implementation](03-language-server.md)