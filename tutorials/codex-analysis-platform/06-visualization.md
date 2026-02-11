---
layout: default
title: "Chapter 6: Visualization"
parent: "Codex Analysis Platform"
nav_order: 6
---

# Chapter 6: Visualization

> Build interactive code exploration and visualization dashboards.

## Overview

Visualization transforms analysis data into actionable insights. This chapter covers building dependency graphs, code maps, and interactive exploration interfaces.

## Visualization Architecture

### Dashboard Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Visualization Dashboard                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Navigation Bar                        │    │
│  │  [Dependency Graph] [Call Graph] [Metrics] [Search]     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌───────────────────┐  ┌───────────────────────────────────┐  │
│  │   File Explorer    │  │        Main View                  │  │
│  │   ───────────────  │  │   ┌─────────────────────────┐    │  │
│  │   📁 src/          │  │   │                         │    │  │
│  │    ├── 📄 index.ts │  │   │   Interactive Graph     │    │  │
│  │    ├── 📁 engine/  │  │   │   or Code View          │    │  │
│  │    │   ├── Engine  │  │   │                         │    │  │
│  │    │   └── Store   │  │   │                         │    │  │
│  │    └── 📁 lsp/     │  │   └─────────────────────────┘    │  │
│  │        └── server  │  │                                   │  │
│  └───────────────────┘  │   ┌─────────────────────────┐    │  │
│                         │   │     Details Panel        │    │  │
│  ┌───────────────────┐  │   │   Symbol: MyClass       │    │  │
│  │   Symbol Outline   │  │   │   Type: Class           │    │  │
│  │   ───────────────  │  │   │   References: 42        │    │  │
│  │   ○ MyClass        │  │   │   Complexity: Medium    │    │  │
│  │     ○ constructor  │  │   └─────────────────────────┘    │  │
│  │     ○ doSomething  │  └───────────────────────────────────┘  │
│  │   ○ helper()       │                                         │
│  └───────────────────┘                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Dependency Graph Visualization

### Graph Data Model

```typescript
// src/visualization/GraphModel.ts
export interface GraphNode {
  id: string;
  label: string;
  type: 'file' | 'module' | 'class' | 'function';
  size: number;       // Based on LOC or complexity
  color: string;      // Based on type or metrics
  metadata: {
    path?: string;
    symbolCount?: number;
    complexity?: number;
  };
}

export interface GraphEdge {
  source: string;
  target: string;
  type: 'import' | 'call' | 'extend' | 'implement';
  weight: number;     // Strength of relationship
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export class DependencyGraphBuilder {
  private store: AnalysisStore;

  constructor(store: AnalysisStore) {
    this.store = store;
  }

  // Build file dependency graph
  buildFileDependencies(): GraphData {
    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];
    const fileMap = new Map<string, GraphNode>();

    // Create nodes for each file
    for (const [filePath, result] of this.store.getAllResults()) {
      const node: GraphNode = {
        id: filePath,
        label: this.getFileName(filePath),
        type: 'file',
        size: result.symbols.length,
        color: this.getColorForFile(filePath),
        metadata: {
          path: filePath,
          symbolCount: result.symbols.length,
        },
      };
      nodes.push(node);
      fileMap.set(filePath, node);
    }

    // Create edges for imports
    for (const [filePath, result] of this.store.getAllResults()) {
      for (const ref of result.references) {
        if (ref.kind === 'import') {
          const target = this.store.getSymbolById(ref.targetId);
          if (target && target.location.filePath !== filePath) {
            edges.push({
              source: filePath,
              target: target.location.filePath,
              type: 'import',
              weight: 1,
            });
          }
        }
      }
    }

    return { nodes, edges };
  }

  // Build module/package dependency graph
  buildModuleDependencies(): GraphData {
    const fileGraph = this.buildFileDependencies();

    // Group files by directory/module
    const modules = new Map<string, GraphNode[]>();

    for (const node of fileGraph.nodes) {
      const modulePath = this.getModulePath(node.metadata.path!);
      const existing = modules.get(modulePath) || [];
      existing.push(node);
      modules.set(modulePath, existing);
    }

    const nodes: GraphNode[] = [];
    const edges: GraphEdge[] = [];

    // Create module nodes
    for (const [modulePath, files] of modules) {
      const totalSymbols = files.reduce((sum, f) => sum + f.size, 0);
      nodes.push({
        id: modulePath,
        label: this.getModuleName(modulePath),
        type: 'module',
        size: totalSymbols,
        color: this.getColorForModule(modulePath),
        metadata: {
          path: modulePath,
          symbolCount: totalSymbols,
        },
      });
    }

    // Aggregate edges between modules
    const edgeMap = new Map<string, number>();
    for (const edge of fileGraph.edges) {
      const sourceModule = this.getModulePath(edge.source);
      const targetModule = this.getModulePath(edge.target);

      if (sourceModule !== targetModule) {
        const key = `${sourceModule}->${targetModule}`;
        edgeMap.set(key, (edgeMap.get(key) || 0) + 1);
      }
    }

    for (const [key, weight] of edgeMap) {
      const [source, target] = key.split('->');
      edges.push({
        source,
        target,
        type: 'import',
        weight,
      });
    }

    return { nodes, edges };
  }

  private getFileName(path: string): string {
    return path.split('/').pop() || path;
  }

  private getModulePath(filePath: string): string {
    const parts = filePath.split('/');
    return parts.slice(0, -1).join('/') || '/';
  }

  private getModuleName(modulePath: string): string {
    return modulePath.split('/').pop() || 'root';
  }

  private getColorForFile(path: string): string {
    const ext = path.split('.').pop();
    const colors: Record<string, string> = {
      'ts': '#3178c6',
      'tsx': '#61dafb',
      'js': '#f7df1e',
      'jsx': '#61dafb',
      'py': '#3776ab',
      'go': '#00add8',
    };
    return colors[ext || ''] || '#888888';
  }

  private getColorForModule(path: string): string {
    // Color based on depth or type
    const depth = path.split('/').length;
    const hue = (depth * 60) % 360;
    return `hsl(${hue}, 70%, 50%)`;
  }
}
```

### React Visualization Component

```tsx
// src/visualization/components/DependencyGraph.tsx
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { GraphData, GraphNode, GraphEdge } from '../GraphModel';

interface DependencyGraphProps {
  data: GraphData;
  width: number;
  height: number;
  onNodeClick?: (node: GraphNode) => void;
  onEdgeClick?: (edge: GraphEdge) => void;
}

export const DependencyGraph: React.FC<DependencyGraphProps> = ({
  data,
  width,
  height,
  onNodeClick,
  onEdgeClick,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    if (!svgRef.current || !data.nodes.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes as any)
      .force('link', d3.forceLink(data.edges as any)
        .id((d: any) => d.id)
        .distance(100)
        .strength((d: any) => d.weight * 0.1))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius((d: any) => d.size + 10));

    // Create container for zoom
    const container = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        container.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Create edges
    const edges = container.append('g')
      .selectAll('line')
      .data(data.edges)
      .enter()
      .append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', (d) => Math.sqrt(d.weight))
      .on('click', (event, d) => {
        if (onEdgeClick) onEdgeClick(d);
      });

    // Create nodes
    const nodes = container.append('g')
      .selectAll('g')
      .data(data.nodes)
      .enter()
      .append('g')
      .call(d3.drag<SVGGElement, GraphNode>()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded));

    // Node circles
    nodes.append('circle')
      .attr('r', (d) => Math.max(5, Math.sqrt(d.size) * 2))
      .attr('fill', (d) => d.color)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .on('click', (event, d) => {
        setSelectedNode(d.id);
        if (onNodeClick) onNodeClick(d);
      });

    // Node labels
    nodes.append('text')
      .text((d) => d.label)
      .attr('x', (d) => Math.max(5, Math.sqrt(d.size) * 2) + 5)
      .attr('y', 4)
      .attr('font-size', '12px')
      .attr('fill', '#333');

    // Update positions on tick
    simulation.on('tick', () => {
      edges
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      nodes.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragStarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnded(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [data, width, height]);

  return (
    <svg
      ref={svgRef}
      width={width}
      height={height}
      style={{ border: '1px solid #ddd', borderRadius: '4px' }}
    />
  );
};
```

## Code Metrics Dashboard

### Metrics Calculator

```typescript
// src/visualization/MetricsCalculator.ts
export interface FileMetrics {
  filePath: string;
  loc: number;              // Lines of code
  symbolCount: number;
  functionCount: number;
  classCount: number;
  complexity: number;       // Cyclomatic complexity
  dependencies: number;     // Import count
  dependents: number;       // Files that import this
  maintainability: number;  // 0-100 score
}

export interface ProjectMetrics {
  totalFiles: number;
  totalLOC: number;
  totalSymbols: number;
  avgComplexity: number;
  avgMaintainability: number;
  fileMetrics: FileMetrics[];
  hotspots: FileMetrics[];  // High complexity files
}

export class MetricsCalculator {
  private store: AnalysisStore;

  constructor(store: AnalysisStore) {
    this.store = store;
  }

  calculateProjectMetrics(): ProjectMetrics {
    const fileMetrics: FileMetrics[] = [];

    for (const [filePath, result] of this.store.getAllResults()) {
      const metrics = this.calculateFileMetrics(filePath, result);
      fileMetrics.push(metrics);
    }

    // Sort by complexity to find hotspots
    const hotspots = [...fileMetrics]
      .sort((a, b) => b.complexity - a.complexity)
      .slice(0, 10);

    const totalLOC = fileMetrics.reduce((sum, m) => sum + m.loc, 0);
    const totalSymbols = fileMetrics.reduce((sum, m) => sum + m.symbolCount, 0);
    const avgComplexity = fileMetrics.reduce((sum, m) => sum + m.complexity, 0) / fileMetrics.length;
    const avgMaintainability = fileMetrics.reduce((sum, m) => sum + m.maintainability, 0) / fileMetrics.length;

    return {
      totalFiles: fileMetrics.length,
      totalLOC,
      totalSymbols,
      avgComplexity,
      avgMaintainability,
      fileMetrics,
      hotspots,
    };
  }

  private calculateFileMetrics(filePath: string, result: AnalysisResult): FileMetrics {
    const symbols = result.symbols;
    const functionCount = symbols.filter(s => s.kind === 'function' || s.kind === 'method').length;
    const classCount = symbols.filter(s => s.kind === 'class').length;
    const dependencies = result.references.filter(r => r.kind === 'import').length;
    const dependents = this.countDependents(filePath);

    // Estimate complexity (simplified)
    const complexity = functionCount * 2 + classCount * 3;

    // Calculate maintainability index (simplified)
    const maintainability = Math.max(0, Math.min(100,
      171 - 5.2 * Math.log(result.symbols.length || 1) - 0.23 * complexity
    ));

    return {
      filePath,
      loc: this.estimateLOC(result),
      symbolCount: symbols.length,
      functionCount,
      classCount,
      complexity,
      dependencies,
      dependents,
      maintainability,
    };
  }

  private countDependents(filePath: string): number {
    let count = 0;
    for (const [, result] of this.store.getAllResults()) {
      for (const ref of result.references) {
        const target = this.store.getSymbolById(ref.targetId);
        if (target && target.location.filePath === filePath && ref.kind === 'import') {
          count++;
          break;
        }
      }
    }
    return count;
  }

  private estimateLOC(result: AnalysisResult): number {
    if (result.symbols.length === 0) return 0;

    const lastSymbol = result.symbols.reduce((max, s) =>
      s.location.range.end.line > max.location.range.end.line ? s : max
    );

    return lastSymbol.location.range.end.line;
  }
}
```

### Metrics Dashboard Component

```tsx
// src/visualization/components/MetricsDashboard.tsx
import React from 'react';
import { ProjectMetrics, FileMetrics } from '../MetricsCalculator';

interface MetricsDashboardProps {
  metrics: ProjectMetrics;
  onFileSelect?: (filePath: string) => void;
}

export const MetricsDashboard: React.FC<MetricsDashboardProps> = ({
  metrics,
  onFileSelect,
}) => {
  return (
    <div className="metrics-dashboard">
      {/* Overview Cards */}
      <div className="metrics-grid">
        <MetricCard
          title="Total Files"
          value={metrics.totalFiles}
          icon="📁"
        />
        <MetricCard
          title="Lines of Code"
          value={metrics.totalLOC.toLocaleString()}
          icon="📝"
        />
        <MetricCard
          title="Total Symbols"
          value={metrics.totalSymbols.toLocaleString()}
          icon="🔣"
        />
        <MetricCard
          title="Avg Complexity"
          value={metrics.avgComplexity.toFixed(1)}
          icon="📊"
          status={metrics.avgComplexity > 20 ? 'warning' : 'good'}
        />
        <MetricCard
          title="Maintainability"
          value={`${metrics.avgMaintainability.toFixed(0)}%`}
          icon="🔧"
          status={metrics.avgMaintainability < 50 ? 'warning' : 'good'}
        />
      </div>

      {/* Hotspots */}
      <div className="hotspots-section">
        <h3>🔥 Complexity Hotspots</h3>
        <table className="hotspots-table">
          <thead>
            <tr>
              <th>File</th>
              <th>Complexity</th>
              <th>LOC</th>
              <th>Maintainability</th>
            </tr>
          </thead>
          <tbody>
            {metrics.hotspots.map((file) => (
              <tr
                key={file.filePath}
                onClick={() => onFileSelect?.(file.filePath)}
                className="hotspot-row"
              >
                <td>{getFileName(file.filePath)}</td>
                <td>
                  <span className={`complexity-badge ${getComplexityLevel(file.complexity)}`}>
                    {file.complexity}
                  </span>
                </td>
                <td>{file.loc}</td>
                <td>
                  <MaintainabilityBar value={file.maintainability} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Charts */}
      <div className="charts-section">
        <ComplexityDistribution files={metrics.fileMetrics} />
        <DependencyMatrix files={metrics.fileMetrics} />
      </div>
    </div>
  );
};

const MetricCard: React.FC<{
  title: string;
  value: string | number;
  icon: string;
  status?: 'good' | 'warning' | 'bad';
}> = ({ title, value, icon, status = 'good' }) => (
  <div className={`metric-card ${status}`}>
    <span className="metric-icon">{icon}</span>
    <div className="metric-content">
      <span className="metric-value">{value}</span>
      <span className="metric-title">{title}</span>
    </div>
  </div>
);

const MaintainabilityBar: React.FC<{ value: number }> = ({ value }) => (
  <div className="maintainability-bar">
    <div
      className="maintainability-fill"
      style={{
        width: `${value}%`,
        backgroundColor: value > 70 ? '#4caf50' : value > 40 ? '#ff9800' : '#f44336',
      }}
    />
    <span className="maintainability-value">{value.toFixed(0)}%</span>
  </div>
);

function getFileName(path: string): string {
  return path.split('/').pop() || path;
}

function getComplexityLevel(complexity: number): string {
  if (complexity > 30) return 'high';
  if (complexity > 15) return 'medium';
  return 'low';
}
```

## Summary

In this chapter, you've learned:

- **Graph Visualization**: Building dependency and call graphs
- **D3.js Integration**: Interactive force-directed layouts
- **Metrics Calculation**: LOC, complexity, maintainability
- **Dashboard Design**: Presenting analysis data effectively
- **React Components**: Reusable visualization components

## Key Takeaways

1. **Visualization reveals patterns**: See what code can't show
2. **Interactivity is key**: Let users explore and drill down
3. **Metrics guide decisions**: Identify where to focus effort
4. **Performance matters**: Handle large codebases gracefully
5. **Context is everything**: Show relevant details on demand

## Next Steps

You now have strong visualization foundations and are ready to operationalize the platform.

Continue with [Chapter 7: Automation Pipelines](07-automation-pipelines.md) to integrate analysis outputs into CI and reporting workflows.

## Further Reading

- [Babel Documentation](https://babeljs.io/docs/en/)
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [D3.js Documentation](https://d3js.org/)
- [TypeScript Compiler API](https://github.com/microsoft/TypeScript/wiki/Using-the-Compiler-API)

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
