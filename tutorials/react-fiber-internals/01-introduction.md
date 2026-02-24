---
layout: default
title: "Chapter 1: Introduction to Fiber"
parent: "React Fiber Internals"
nav_order: 1
---

# Chapter 1: Introduction to Fiber

Welcome to **Chapter 1: Introduction to Fiber**. In this part of **React Fiber Internals**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understand why React needed Fiber, the problems it solves, and how it fundamentally changed React's architecture.

## Overview

React Fiber is a complete rewrite of React's core algorithm, introduced in React 16. It replaced the Stack reconciler with a new architecture that enables incremental rendering—the ability to split rendering work into chunks and spread it out over multiple frames.

## The Stack Reconciler Problem

### Before Fiber (React 15)

```
┌─────────────────────────────────────────────────────────────────┐
│                Stack Reconciler (Synchronous)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  setState() called                                              │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SYNCHRONOUS RECONCILIATION                  │   │
│  │                                                          │   │
│  │  Component 1 → Component 2 → Component 3 → ... → Done   │   │
│  │                                                          │   │
│  │  ⚠️ CANNOT BE INTERRUPTED                                │   │
│  │  ⚠️ BLOCKS MAIN THREAD                                   │   │
│  │  ⚠️ NO PRIORITIZATION                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  DOM Updates (all at once)                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Problems

```javascript
// Problem 1: Long updates block everything
function LargeList({ items }) {
  // Rendering 10,000 items blocks the main thread
  return (
    <ul>
      {items.map(item => (
        <ListItem key={item.id} data={item} />
      ))}
    </ul>
  );
}

// Problem 2: High-priority updates can't interrupt low-priority
// User typing while a large list renders = janky experience
function SearchableList({ items }) {
  const [query, setQuery] = useState('');

  // Low priority: filtering/rendering list
  const filtered = items.filter(i => i.name.includes(query));

  // High priority: user input - but gets blocked!
  return (
    <div>
      <input onChange={e => setQuery(e.target.value)} />
      <LargeList items={filtered} />
    </div>
  );
}
```

## What is Fiber?

### The Fiber Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 Fiber Architecture (Incremental)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  setState() called                                              │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               INCREMENTAL RECONCILIATION                 │   │
│  │                                                          │   │
│  │  Work Unit 1                                             │   │
│  │       ↓                                                  │   │
│  │  Check: Should yield? ──── Yes ──→ Yield to browser     │   │
│  │       │ No                              │                │   │
│  │       ↓                                 │                │   │
│  │  Work Unit 2                            │                │   │
│  │       ↓                                 │                │   │
│  │  Check: Should yield? ←─────────────────┘                │   │
│  │       │                                                  │   │
│  │       ↓                                                  │   │
│  │  ... continues ...                                       │   │
│  │                                                          │   │
│  │  ✅ CAN BE INTERRUPTED                                   │   │
│  │  ✅ YIELDS TO BROWSER                                    │   │
│  │  ✅ PRIORITY-BASED                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│  Commit Phase (synchronous, can't be interrupted)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Capabilities

1. **Pause work** and come back to it later
2. **Assign priority** to different types of work
3. **Reuse** previously completed work
4. **Abort** work if it's no longer needed

## Fiber: The Unit of Work

### What is a Fiber?

```javascript
// A Fiber is a JavaScript object that contains information about a component,
// its input, and its output.

// Simplified Fiber structure
const fiber = {
  // Instance
  tag: 'FunctionComponent',    // Type of fiber
  type: MyComponent,           // Component function/class
  key: null,                   // React key

  // Fiber tree structure
  return: parentFiber,         // Parent fiber
  child: firstChildFiber,      // First child
  sibling: nextSiblingFiber,   // Next sibling

  // Work tracking
  pendingProps: { ... },       // New props
  memoizedProps: { ... },      // Props used in last render
  memoizedState: { ... },      // State used in last render

  // Effects
  flags: 'Update',             // Side effects to perform
  nextEffect: nextEffectFiber, // Next fiber with effects

  // Scheduling
  lanes: 0b0001,               // Priority lanes
  childLanes: 0b0011,          // Combined child priorities

  // Alternate (double buffering)
  alternate: workInProgressFiber
};
```

### Fiber vs React Element

```javascript
// React Element (immutable, describes what you want)
const element = {
  type: 'div',
  props: {
    children: 'Hello'
  }
};

// Fiber (mutable, represents work to be done)
const fiber = {
  type: 'div',
  stateNode: actualDOMNode,  // Reference to real DOM
  memoizedProps: { children: 'Hello' },
  // ... plus all the scheduling/tree info
};
```

## Two Phases of Rendering

### Phase 1: Render (Reconciliation)

```javascript
// The render phase:
// - Builds the work-in-progress tree
// - Calculates changes
// - Can be interrupted

// Conceptually:
function renderPhase(fiber) {
  // Process this fiber
  const next = beginWork(fiber);

  if (next !== null) {
    // Has children, process them
    return next;
  }

  // No more children, complete this fiber
  completeWork(fiber);

  // Move to sibling or parent
  return fiber.sibling || fiber.return;
}
```

### Phase 2: Commit

```javascript
// The commit phase:
// - Applies changes to the DOM
// - Runs effects
// - Cannot be interrupted (synchronous)

// Conceptually:
function commitPhase(finishedWork) {
  // Phase 1: Before mutation (getSnapshotBeforeUpdate)
  commitBeforeMutationEffects(finishedWork);

  // Phase 2: Mutation (actual DOM changes)
  commitMutationEffects(finishedWork);

  // Phase 3: Layout (componentDidMount/Update, useLayoutEffect)
  commitLayoutEffects(finishedWork);
}
```

## Work Loop

### The Core Algorithm

```javascript
// Simplified work loop
function workLoop(deadline) {
  // Keep working while there's work and we have time
  while (workInProgress !== null && !shouldYield()) {
    workInProgress = performUnitOfWork(workInProgress);
  }

  // If we finished all work, commit
  if (workInProgress === null && finishedWork !== null) {
    commitRoot(finishedWork);
  }

  // If there's more work, schedule it
  if (workInProgress !== null) {
    requestIdleCallback(workLoop);
  }
}

function performUnitOfWork(fiber) {
  // Step 1: Begin work on this fiber
  const next = beginWork(fiber);

  if (next !== null) {
    // Has children, process them next
    return next;
  }

  // Step 2: Complete work on this fiber
  return completeUnitOfWork(fiber);
}

function completeUnitOfWork(fiber) {
  while (fiber !== null) {
    completeWork(fiber);

    // If there's a sibling, process it next
    if (fiber.sibling !== null) {
      return fiber.sibling;
    }

    // Move up to parent
    fiber = fiber.return;
  }

  return null;
}
```

## Time Slicing

### Yielding to the Browser

```javascript
// React yields control back to the browser regularly
function shouldYield() {
  // Check if we've used up our time slice (typically 5ms)
  return performance.now() >= deadline;
}

// This allows:
// 1. User input to be processed
// 2. Animations to remain smooth
// 3. Browser to do its own work

// Without time slicing:
// [=============REACT WORK==============][Browser Paint]

// With time slicing:
// [React][Paint][React][Paint][React][Paint]
```

## Priority Lanes

### Update Priorities

```javascript
// Different updates have different priorities
const Lanes = {
  SyncLane:         0b0000000000000000000000000000001,  // Highest
  InputContinuous:  0b0000000000000000000000000000100,
  DefaultLane:      0b0000000000000000000000000010000,
  TransitionLane:   0b0000000000000000000001000000000,
  IdleLane:         0b0100000000000000000000000000000,  // Lowest
};

// User typing: SyncLane (highest priority)
// setState from effect: DefaultLane
// startTransition: TransitionLane (can be interrupted)
```

## Practical Impact

### Before Fiber

```javascript
// Large list causes jank
function App() {
  const [items, setItems] = useState(largeArray);
  const [input, setInput] = useState('');

  // Typing is janky because list render blocks
  return (
    <div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      {items.map(item => <ExpensiveComponent key={item.id} />)}
    </div>
  );
}
```

### After Fiber (with Concurrent Features)

```javascript
// Using transitions for smooth experience
function App() {
  const [items, setItems] = useState(largeArray);
  const [input, setInput] = useState('');
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // High priority: update input immediately
    setInput(e.target.value);

    // Low priority: filter can be interrupted
    startTransition(() => {
      setItems(filterItems(e.target.value));
    });
  };

  return (
    <div>
      <input value={input} onChange={handleChange} />
      {isPending && <Spinner />}
      {items.map(item => <ExpensiveComponent key={item.id} />)}
    </div>
  );
}
```

## Summary

In this chapter, you've learned:

- **Stack Reconciler Problems**: Synchronous, blocking, no priorities
- **Fiber Solution**: Incremental rendering with interruptible work
- **Fiber Node**: The unit of work in React's tree
- **Two Phases**: Render (interruptible) and Commit (synchronous)
- **Work Loop**: How React processes the fiber tree
- **Time Slicing**: Yielding to the browser for responsiveness
- **Priority Lanes**: Different priorities for different updates

## Key Takeaways

1. **Fiber enables incremental rendering** - work can be paused and resumed
2. **React has two trees** - current and work-in-progress (double buffering)
3. **Render phase is interruptible** - commit phase is not
4. **Priority matters** - user input beats background updates
5. **Understanding Fiber** helps write better React code

## Next Steps

Now that you understand why Fiber exists, let's dive deep into the Fiber data structure in Chapter 2.

---

**Ready for Chapter 2?** [Fiber Data Structure](02-fiber-structure.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `fiber`, `input`, `items` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Introduction to Fiber` as an operating subsystem inside **React Fiber Internals**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `work`, `next`, `item` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Introduction to Fiber` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `fiber`.
2. **Input normalization**: shape incoming data so `input` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `items`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `fiber` and `input` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Fiber Data Structure](02-fiber-structure.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
