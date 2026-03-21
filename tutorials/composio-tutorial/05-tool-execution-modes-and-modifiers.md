---
layout: default
title: "Chapter 5: Tool Execution Modes and Modifiers"
nav_order: 5
parent: Composio Tutorial
---


# Chapter 5: Tool Execution Modes and Modifiers

Welcome to **Chapter 5: Tool Execution Modes and Modifiers**. In this part of **Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how to choose execution mode and when to apply schema/before/after modifiers.

## Learning Goals

- compare chat-completion, agentic-framework, and direct execution paths
- understand where tool-call loops are owned in each path
- use modifiers to enforce safer inputs and cleaner outputs
- decide when proxy execution or custom tools are appropriate

## Execution Modes

| Mode | Best For |
|:-----|:---------|
| chat completion providers | explicit control over tool loop and response handling |
| agentic frameworks | framework-managed plan/act loops with Composio tool objects |
| direct execution | deterministic backend jobs and non-LLM automation |
| proxy execution | calling supported toolkit endpoints not exposed as predefined tools |

## Modifier Strategy

- schema modifiers: simplify tool inputs before the model sees schemas
- before modifiers: enforce runtime argument defaults/guards
- after modifiers: normalize outputs for downstream systems

## Source References

- [Executing Tools](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/executing-tools.mdx)
- [Schema Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/schema-modifiers.mdx)
- [Before Execution Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/before-execution-modifiers.mdx)
- [After Execution Modifiers](https://github.com/ComposioHQ/composio/blob/next/docs/content/docs/tools-direct/modify-tool-behavior/after-execution-modifiers.mdx)

## Summary

You now have an execution and modifier model that can be adapted to both agentic and deterministic workloads.

Next: [Chapter 6: MCP Server Patterns and Toolkit Control](06-mcp-server-patterns-and-toolkit-control.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `docs/components/custom-schema-ui.tsx`

The `isExpandable` function in [`docs/components/custom-schema-ui.tsx`](https://github.com/ComposioHQ/composio/blob/HEAD/docs/components/custom-schema-ui.tsx) handles a key part of this chapter's functionality:

```tsx
}: SchemaUIProps) {
  const schema = generated.refs[generated.$root];
  const isProperty = as === 'property' || !isExpandable(schema, generated.refs);

  return (
    <DataContext value={generated}>
      <ResponseContext value={isResponse}>
        {isProperty ? (
          <SchemaProperty
            name={name}
            $type={generated.$root}
            required={required}
            isRoot
          />
        ) : (
          <SchemaContent $type={generated.$root} />
        )}
      </ResponseContext>
    </DataContext>
  );
}

function SchemaContent({
  $type,
  parentPath = '',
}: {
  $type: string;
  parentPath?: string;
}) {
  const { refs } = useData();
  const schema = refs[$type];

```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `docs/components/custom-schema-ui.tsx`

The `getTypeDisplay` function in [`docs/components/custom-schema-ui.tsx`](https://github.com/ComposioHQ/composio/blob/HEAD/docs/components/custom-schema-ui.tsx) handles a key part of this chapter's functionality:

```tsx

  const hasChildren = isExpandable(schema, refs);
  const typeDisplay = getTypeDisplay(schema);

  return (
    <div className={cn('py-4', !isRoot && 'first:pt-0')}>
      {/* Property header */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-medium font-mono text-fd-foreground">
          {name}
        </span>
        <span className="text-sm font-mono text-fd-muted-foreground">
          {typeDisplay}
        </span>
        {required && !isResponse && (
          <span className="text-xs text-red-400 font-medium">Required</span>
        )}
        {schema.deprecated && (
          <span className="text-xs bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 px-1.5 py-0.5 rounded">
            Deprecated
          </span>
        )}
      </div>

      {/* Description */}
      {schema.description && (
        <div className="mt-2 text-sm text-fd-muted-foreground prose-no-margin">
          {schema.description}
        </div>
      )}

      {/* Info tags */}
```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `docs/components/custom-schema-ui.tsx`

The `getChildCount` function in [`docs/components/custom-schema-ui.tsx`](https://github.com/ComposioHQ/composio/blob/HEAD/docs/components/custom-schema-ui.tsx) handles a key part of this chapter's functionality:

```tsx
  const schema = refs[$type];

  const childCount = getChildCount(schema);
  const label = schema.type === 'array' ? 'item properties' : 'child attributes';

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="mt-3">
      <CollapsibleTrigger className="group flex items-center gap-1 px-2 py-1 text-xs text-fd-muted-foreground hover:text-fd-foreground font-medium rounded border border-fd-border hover:bg-fd-accent/30 transition-colors">
        {isOpen ? (
          <>
            <X className="h-3 w-3" />
            Hide {label}
          </>
        ) : (
          <>
            <Plus className="h-3 w-3" />
            Show {childCount > 0 ? `${childCount} ` : ''}{label}
          </>
        )}
      </CollapsibleTrigger>
      <CollapsibleContent>
        <div className="mt-2 pl-3 border-l border-fd-border">
          <SchemaContent $type={$type} parentPath={parentPath} />
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}

function isExpandable(
  schema: SchemaData,
  refs?: Record<string, SchemaData>,
```

This function is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.

### `docs/components/custom-schema-ui.tsx`

The `SchemaUIProps` interface in [`docs/components/custom-schema-ui.tsx`](https://github.com/ComposioHQ/composio/blob/HEAD/docs/components/custom-schema-ui.tsx) handles a key part of this chapter's functionality:

```tsx
import type { SchemaData, SchemaUIGeneratedData } from './schema-generator';

interface SchemaUIProps {
  name: string;
  required?: boolean;
  as?: 'property' | 'body';
  generated: SchemaUIGeneratedData;
  isResponse?: boolean;
}

const DataContext = createContext<SchemaUIGeneratedData | null>(null);
const ResponseContext = createContext(false);

function useData() {
  const ctx = use(DataContext);
  if (!ctx) throw new Error('Missing DataContext');
  return ctx;
}

function useIsResponse() {
  return use(ResponseContext);
}

export function CustomSchemaUI({
  name,
  required = false,
  as = 'property',
  generated,
  isResponse = false,
}: SchemaUIProps) {
  const schema = generated.refs[generated.$root];
  const isProperty = as === 'property' || !isExpandable(schema, generated.refs);
```

This interface is important because it defines how Composio Tutorial: Production Tool and Authentication Infrastructure for AI Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[isExpandable]
    B[getTypeDisplay]
    C[getChildCount]
    D[SchemaUIProps]
    E[name]
    A --> B
    B --> C
    C --> D
    D --> E
```
