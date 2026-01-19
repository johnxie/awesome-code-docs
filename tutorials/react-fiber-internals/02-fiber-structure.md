---
layout: default
title: "Chapter 2: Fiber Data Structure"
parent: "React Fiber Internals"
nav_order: 2
---

# Chapter 2: Fiber Data Structure

> Deep dive into the Fiber node structure, its properties, and how the tree is organized.

## Overview

A Fiber is a JavaScript object that represents a unit of work. Every React element has a corresponding Fiber, and these Fibers form a tree structure that React uses to track component state, schedule updates, and perform reconciliation.

## Fiber Node Properties

### Complete Fiber Structure

```typescript
interface Fiber {
  // ========== Instance ==========
  tag: WorkTag;                    // Type of fiber (FunctionComponent, HostComponent, etc.)
  key: null | string;              // React key for reconciliation
  elementType: any;                // Element type (function, class, or string)
  type: any;                       // Resolved type (same as elementType for most)
  stateNode: any;                  // DOM node, class instance, or null

  // ========== Fiber Tree Structure ==========
  return: Fiber | null;            // Parent fiber
  child: Fiber | null;             // First child fiber
  sibling: Fiber | null;           // Next sibling fiber
  index: number;                   // Index among siblings

  // ========== Input/Output ==========
  pendingProps: any;               // New props (input)
  memoizedProps: any;              // Props from last render
  memoizedState: any;              // State from last render
  updateQueue: UpdateQueue | null; // Queue of state updates

  // ========== Context ==========
  dependencies: Dependencies | null; // Context dependencies
  context: any;                      // Legacy context

  // ========== Effects ==========
  flags: Flags;                    // Side effects (Placement, Update, Deletion)
  subtreeFlags: Flags;             // Combined child flags
  deletions: Array<Fiber> | null;  // Children to delete

  // ========== Scheduling ==========
  lanes: Lanes;                    // Priority of this fiber's work
  childLanes: Lanes;               // Combined priority of children

  // ========== Alternate ==========
  alternate: Fiber | null;         // Work-in-progress or current version
}
```

## Fiber Tags (WorkTag)

### Component Types

```javascript
const WorkTag = {
  FunctionComponent: 0,        // function MyComponent() {}
  ClassComponent: 1,           // class MyComponent extends React.Component
  IndeterminateComponent: 2,   // Not yet determined (function or class)
  HostRoot: 3,                 // Root of the fiber tree
  HostPortal: 4,               // React portal
  HostComponent: 5,            // DOM elements like 'div', 'span'
  HostText: 6,                 // Text nodes
  Fragment: 7,                 // React.Fragment
  Mode: 8,                     // StrictMode, ConcurrentMode
  ContextConsumer: 9,          // Context.Consumer
  ContextProvider: 10,         // Context.Provider
  ForwardRef: 11,              // React.forwardRef
  Profiler: 12,                // React.Profiler
  SuspenseComponent: 13,       // Suspense
  MemoComponent: 14,           // React.memo
  SimpleMemoComponent: 15,     // Simple memo (no compare function)
  LazyComponent: 16,           // React.lazy
  OffscreenComponent: 22,      // For concurrent features
};
```

### Example Tags

```jsx
// FunctionComponent (tag: 0)
function MyFunc() { return <div />; }

// ClassComponent (tag: 1)
class MyClass extends React.Component {
  render() { return <div />; }
}

// HostComponent (tag: 5)
<div>Hello</div>

// HostText (tag: 6)
"Hello World"

// Fragment (tag: 7)
<React.Fragment>...</React.Fragment>

// SuspenseComponent (tag: 13)
<Suspense fallback={<Loading />}>...</Suspense>
```

## Tree Structure

### Parent-Child-Sibling Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fiber Tree Structure                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      ┌─────────────┐                            │
│                      │  HostRoot   │                            │
│                      │  (tag: 3)   │                            │
│                      └──────┬──────┘                            │
│                             │ child                              │
│                             ▼                                    │
│                      ┌─────────────┐                            │
│               ┌──────│    App      │                            │
│               │return│  (tag: 0)   │                            │
│               │      └──────┬──────┘                            │
│               │             │ child                              │
│               │             ▼                                    │
│               │      ┌─────────────┐  sibling  ┌─────────────┐  │
│               │      │   Header    │──────────▶│    Main     │  │
│               └─────▶│  (tag: 0)   │           │  (tag: 0)   │  │
│                      └──────┬──────┘           └──────┬──────┘  │
│                             │ child                    │ child   │
│                             ▼                          ▼         │
│                      ┌─────────────┐           ┌─────────────┐  │
│                      │  h1 "Logo"  │           │    div      │  │
│                      │  (tag: 5)   │           │  (tag: 5)   │  │
│                      └─────────────┘           └─────────────┘  │
│                                                                 │
│  Key relationships:                                             │
│  • child: First child only (linked list via siblings)          │
│  • sibling: Next sibling in the list                           │
│  • return: Parent fiber                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Traversal Order

```javascript
// React traverses fibers in a specific order:
// 1. Process current fiber (beginWork)
// 2. Go to first child if exists
// 3. If no child, complete current fiber (completeWork)
// 4. Go to sibling if exists
// 5. If no sibling, go back to parent and complete it
// 6. Repeat until reaching root

function traverse(fiber) {
  console.log('beginWork:', fiber.type);

  if (fiber.child) {
    traverse(fiber.child);
  }

  console.log('completeWork:', fiber.type);

  if (fiber.sibling) {
    traverse(fiber.sibling);
  }
}

// For tree: App -> Header -> Main
// Output:
// beginWork: App
// beginWork: Header
// completeWork: Header
// beginWork: Main
// completeWork: Main
// completeWork: App
```

## Double Buffering

### Current vs Work-In-Progress

```
┌─────────────────────────────────────────────────────────────────┐
│                    Double Buffering                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CURRENT TREE                     WORK-IN-PROGRESS TREE        │
│   (what's on screen)               (being built)                │
│                                                                 │
│   ┌─────────┐      alternate       ┌─────────┐                 │
│   │ Fiber A │◄────────────────────▶│ Fiber A'│                 │
│   │ (v1)    │                      │ (v2)    │                 │
│   └────┬────┘                      └────┬────┘                 │
│        │                                │                       │
│   ┌────▼────┐      alternate       ┌────▼────┐                 │
│   │ Fiber B │◄────────────────────▶│ Fiber B'│                 │
│   │ (v1)    │                      │ (v2)    │                 │
│   └─────────┘                      └─────────┘                 │
│                                                                 │
│   After commit:                                                 │
│   - Work-in-progress becomes current                            │
│   - Old current becomes the next work-in-progress               │
│   - Trees swap roles (double buffering)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Accessing Alternate

```javascript
// In React source code:
function createWorkInProgress(current, pendingProps) {
  let workInProgress = current.alternate;

  if (workInProgress === null) {
    // First render: create new fiber
    workInProgress = createFiber(current.tag, pendingProps, current.key);
    workInProgress.elementType = current.elementType;
    workInProgress.type = current.type;
    workInProgress.stateNode = current.stateNode;

    // Link alternates
    workInProgress.alternate = current;
    current.alternate = workInProgress;
  } else {
    // Reuse existing work-in-progress
    workInProgress.pendingProps = pendingProps;
    workInProgress.flags = NoFlags;
    workInProgress.subtreeFlags = NoFlags;
    workInProgress.deletions = null;
  }

  // Copy fields from current
  workInProgress.lanes = current.lanes;
  workInProgress.child = current.child;
  // ... copy other fields

  return workInProgress;
}
```

## State and Props

### Memoized Values

```javascript
// Fiber stores the results of the last render
const fiber = {
  // Input: props passed to this component
  pendingProps: { name: 'Alice', age: 30 },  // New props
  memoizedProps: { name: 'Alice', age: 25 }, // Last rendered props

  // State: internal component state
  memoizedState: {
    // For function components with hooks:
    // Linked list of hooks
    baseState: { count: 0 },
    next: { /* next hook */ }
  },

  // For class components:
  // memoizedState is the actual state object
};

// React compares pendingProps with memoizedProps
// to determine if the component needs to re-render
function shouldUpdate(fiber) {
  return !shallowEqual(fiber.pendingProps, fiber.memoizedProps);
}
```

### Update Queue

```javascript
// Updates are queued and processed during reconciliation
const updateQueue = {
  baseState: { count: 0 },           // State before updates
  firstBaseUpdate: null,             // First pending update
  lastBaseUpdate: null,              // Last pending update
  shared: {
    pending: null,                   // Circular list of new updates
    interleaved: null,               // Interleaved updates
    lanes: 0,                        // Combined update lanes
  },
  effects: null,                     // List of effects from updates
};

// An update object
const update = {
  eventTime: 0.0,                    // When update was created
  lane: DefaultLane,                 // Priority
  tag: UpdateState,                  // Type (UpdateState, ReplaceState, etc.)
  payload: { count: 1 },             // The new state or updater function
  callback: null,                    // Optional callback
  next: null,                        // Next update in list
};
```

## Effects and Flags

### Effect Flags

```javascript
// Flags indicate what side effects need to be performed
const Flags = {
  NoFlags:         0b00000000000000000000000,
  Placement:       0b00000000000000000000010,  // Insert into DOM
  Update:          0b00000000000000000000100,  // Update existing DOM
  Deletion:        0b00000000000000000001000,  // Remove from DOM
  ChildDeletion:   0b00000000000000000010000,  // Delete child
  ContentReset:    0b00000000000000000100000,  // Reset text content
  Callback:        0b00000000000000001000000,  // Has callback
  Ref:             0b00000000000000010000000,  // Has ref
  Snapshot:        0b00000000000000100000000,  // getSnapshotBeforeUpdate
  Passive:         0b00000000000001000000000,  // useEffect
  LayoutEffect:    0b00000000000010000000000,  // useLayoutEffect
};

// Using flags with bitwise operations
function hasEffect(fiber) {
  return (fiber.flags & Update) !== NoFlags;
}

function addEffect(fiber, flag) {
  fiber.flags |= flag;
}
```

### Effect List

```javascript
// During completeWork, fibers with effects are collected
// into a linked list for efficient processing during commit

// Before commit phase
const effectList = [
  fiber1,  // Has Update flag
  fiber2,  // Has Placement flag
  fiber3,  // Has Ref flag
];

// During commit, React iterates through this list
// instead of traversing the entire tree again
```

## FiberRoot

### Root Container

```javascript
// FiberRoot is the root of the entire React application
const fiberRoot = {
  containerInfo: document.getElementById('root'),  // DOM container
  current: hostRootFiber,                          // Current fiber tree
  finishedWork: null,                              // Completed work-in-progress
  pendingLanes: 0,                                 // Pending work priorities
  suspendedLanes: 0,                               // Suspended lanes
  pingedLanes: 0,                                  // Pinged lanes
  callbackNode: null,                              // Scheduled callback
  callbackPriority: NoLane,                        // Callback priority
};

// The HostRoot fiber
const hostRootFiber = {
  tag: HostRoot,
  stateNode: fiberRoot,  // Points back to FiberRoot
  child: appFiber,       // Your <App /> component
  // ...
};
```

## Visualizing Fiber

### Example Component Tree

```jsx
function App() {
  const [count, setCount] = useState(0);
  return (
    <div className="app">
      <h1>Count: {count}</h1>
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
    </div>
  );
}

// Resulting Fiber Tree:
// HostRoot
//   └── App (FunctionComponent)
//         └── div.app (HostComponent)
//               ├── h1 (HostComponent)
//               │     └── "Count: 0" (HostText)
//               └── button (HostComponent)
//                     └── "Increment" (HostText)
```

## Summary

In this chapter, you've learned:

- **Fiber Properties**: Tag, type, stateNode, and tree pointers
- **Tree Structure**: Parent-child-sibling relationships
- **Double Buffering**: Current and work-in-progress trees
- **State Storage**: MemoizedProps, memoizedState, updateQueue
- **Effect System**: Flags and effect lists
- **FiberRoot**: The root of the application

## Key Takeaways

1. **Fibers are objects** representing units of work
2. **Tree is linked list** - child, sibling, return pointers
3. **Double buffering** allows in-place updates without flickering
4. **Flags track effects** needed during commit phase
5. **Update queues** store pending state changes

## Next Steps

Now that you understand the Fiber structure, let's explore how React builds the tree during the Render Phase in Chapter 3.

---

**Ready for Chapter 3?** [Render Phase](03-render-phase.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
