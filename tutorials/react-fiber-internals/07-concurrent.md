---
layout: default
title: "Chapter 7: Concurrent Features"
parent: "React Fiber Internals"
nav_order: 7
---

# Chapter 7: Concurrent Features

Welcome to **Chapter 7: Concurrent Features**. In this part of **React Fiber Internals**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Understanding Suspense, transitions, and other concurrent rendering features in React.

## Overview

React's concurrent features allow the UI to remain responsive during expensive renders by splitting work into chunks and prioritizing urgent updates. This chapter covers the internal implementation of Suspense, transitions, and the concurrent rendering model.

## Concurrent Rendering Model

### Conceptual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Concurrent Rendering                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Without Concurrent:                                           │
│   ┌────────────────────────────────────────────┐                │
│   │         Long Render (blocking)              │                │
│   └────────────────────────────────────────────┘                │
│   User input waits... ──────────────────────────▶ Finally handled│
│                                                                 │
│   With Concurrent:                                              │
│   ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐                       │
│   │Rndr│  │Rndr│  │Rndr│  │Rndr│  │Rndr│                       │
│   └────┘  └────┘  └────┘  └────┘  └────┘                       │
│        ↑       ↑       ↑       ↑                                │
│        │       │       │       └── Continue render              │
│        │       │       └── Handle input, resume                 │
│        │       └── Yield to browser                             │
│        └── Yield to browser                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Render Modes

```javascript
// React tracks the current render mode
const NoMode = 0b000000;
const StrictMode = 0b000001;
const ConcurrentMode = 0b000010;

// Check if concurrent mode is enabled
function isConcurrentMode(fiber) {
  return (fiber.mode & ConcurrentMode) !== NoMode;
}

// Different work loops for different modes
function performWork(root, lanes) {
  if (includesSyncLane(lanes)) {
    // Synchronous rendering - cannot be interrupted
    workLoopSync();
  } else {
    // Concurrent rendering - can be interrupted
    workLoopConcurrent();
  }
}

function workLoopSync() {
  while (workInProgress !== null) {
    performUnitOfWork(workInProgress);
  }
}

function workLoopConcurrent() {
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

## Suspense Implementation

### How Suspense Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    Suspense Flow                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  <Suspense fallback={<Loading />}>                       │   │
│   │    <LazyComponent />                                     │   │
│   │  </Suspense>                                             │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   1. React renders LazyComponent                                │
│   2. LazyComponent throws a Promise (data not ready)           │
│   3. React catches the Promise at Suspense boundary            │
│   4. React shows fallback UI                                    │
│   5. Promise resolves                                           │
│   6. React re-renders, now data is available                   │
│   7. React shows actual content                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Suspense Fiber Structure

```javascript
// Suspense component creates a special fiber
const suspenseFiber = {
  tag: SuspenseComponent,
  memoizedState: {
    dehydrated: null,              // For server rendering
    treeContext: null,             // Context state
    retryLane: NoLane,             // Lane for retry
  },
  child: primaryChild,             // The main content
  // Offscreen child holds the fallback
};

// The primary child is wrapped in an Offscreen fiber
const offscreenFiber = {
  tag: OffscreenComponent,
  memoizedState: {
    baseLanes: NoLanes,
    cachePool: null,
  },
  mode: hidden ? 'hidden' : 'visible',
  child: actualContent,
};
```

### Throwing Promises

```javascript
// When a component suspends, it throws a Promise
function use(promise) {
  if (promise.status === 'fulfilled') {
    return promise.value;
  } else if (promise.status === 'rejected') {
    throw promise.reason;
  } else {
    // Not resolved - suspend
    throw promise;
  }
}

// React catches this in the work loop
function handleThrow(root, thrownValue) {
  if (
    thrownValue !== null &&
    typeof thrownValue === 'object' &&
    typeof thrownValue.then === 'function'
  ) {
    // It's a Promise - this is a Suspense throw
    const wakeable = thrownValue;

    // Mark the Suspense boundary
    const suspenseBoundary = getSuspenseHandler();

    if (suspenseBoundary !== null) {
      suspenseBoundary.flags |= ShouldCapture;

      // Track the Promise
      attachPingListener(root, wakeable, rootRenderLanes);
    }

    // Unwind to the Suspense boundary
    return;
  }

  // Not a Promise - treat as error
  // ...
}
```

### Suspense Boundary Handling

```javascript
function updateSuspenseComponent(current, workInProgress, renderLanes) {
  const nextProps = workInProgress.pendingProps;

  let showFallback = false;
  const didSuspend = (workInProgress.flags & DidCapture) !== NoFlags;

  if (didSuspend) {
    // A child suspended - show fallback
    showFallback = true;
    workInProgress.flags &= ~DidCapture;
  }

  const nextPrimaryChildren = nextProps.children;
  const nextFallbackChildren = nextProps.fallback;

  if (showFallback) {
    // Mount the fallback
    const fallbackFragment = mountSuspenseFallbackChildren(
      workInProgress,
      nextPrimaryChildren,
      nextFallbackChildren,
      renderLanes
    );
    workInProgress.child.memoizedState = { baseLanes: renderLanes };
    workInProgress.memoizedState = SUSPENDED_MARKER;
    return fallbackFragment;
  } else {
    // Mount the primary children
    return mountSuspensePrimaryChildren(
      workInProgress,
      nextPrimaryChildren,
      renderLanes
    );
  }
}

function mountSuspenseFallbackChildren(
  workInProgress,
  primaryChildren,
  fallbackChildren,
  renderLanes
) {
  // Primary children go into a hidden Offscreen
  const primaryChildFragment = createFiberFromOffscreen(
    { mode: 'hidden', children: primaryChildren },
    workInProgress.mode,
    NoLanes, // Don't render hidden content now
    null
  );

  // Fallback is visible
  const fallbackChildFragment = createFiberFromFragment(
    fallbackChildren,
    workInProgress.mode,
    renderLanes,
    null
  );

  primaryChildFragment.return = workInProgress;
  fallbackChildFragment.return = workInProgress;
  primaryChildFragment.sibling = fallbackChildFragment;
  workInProgress.child = primaryChildFragment;

  return fallbackChildFragment;
}
```

### Promise Resolution

```javascript
function attachPingListener(root, wakeable, lanes) {
  let pingCache = root.pingCache;

  if (pingCache === null) {
    pingCache = root.pingCache = new Map();
  }

  let threadIDs = pingCache.get(wakeable);
  if (threadIDs === undefined) {
    threadIDs = new Set();
    pingCache.set(wakeable, threadIDs);

    // Attach listener to Promise
    wakeable.then(
      () => pingSuspendedRoot(root, wakeable, lanes),
      () => pingSuspendedRoot(root, wakeable, lanes)
    );
  }

  threadIDs.add(lanes);
}

function pingSuspendedRoot(root, wakeable, lanes) {
  const pingCache = root.pingCache;

  if (pingCache !== null) {
    pingCache.delete(wakeable);
  }

  // Mark pinged lanes
  markRootPinged(root, lanes);

  // Schedule re-render
  ensureRootIsScheduled(root);
}
```

## Transitions

### startTransition Implementation

```javascript
// Track if we're inside a transition
let currentTransition = null;

function startTransition(scope) {
  const prevTransition = currentTransition;

  // Create transition context
  currentTransition = {};

  // Set low-priority lane
  const previousPriority = getCurrentUpdatePriority();
  setCurrentUpdatePriority(TransitionPriority);

  try {
    scope();
  } finally {
    setCurrentUpdatePriority(previousPriority);
    currentTransition = prevTransition;
  }
}

// When setState is called inside transition:
function requestUpdateLane(fiber) {
  if (currentTransition !== null) {
    // Inside transition - use transition lane
    return claimNextTransitionLane();
  }

  // Normal priority
  return getCurrentEventPriority();
}
```

### useTransition Hook

```javascript
function mountTransition() {
  const [isPending, setPending] = mountState(false);

  const start = (callback) => {
    setPending(true);

    startTransition(() => {
      setPending(false);
      callback();
    });
  };

  return [isPending, start];
}

function updateTransition() {
  const [isPending] = updateState(false);

  const hook = updateWorkInProgressHook();
  const start = hook.memoizedState;

  return [isPending, start];
}

// Usage:
function SearchResults() {
  const [isPending, startTransition] = useTransition();
  const [results, setResults] = useState([]);

  function handleSearch(query) {
    startTransition(() => {
      // This update is low priority
      setResults(searchDatabase(query));
    });
  }

  return (
    <div>
      {isPending && <Spinner />}
      <Results data={results} />
    </div>
  );
}
```

### useDeferredValue Implementation

```javascript
function mountDeferredValue(value) {
  const hook = mountWorkInProgressHook();
  hook.memoizedState = value;
  return value;
}

function updateDeferredValue(value) {
  const hook = updateWorkInProgressHook();
  const prevValue = hook.memoizedState;

  if (Object.is(value, prevValue)) {
    // No change
    return value;
  }

  // Check if we're in an urgent render
  if (isCurrentTreeHidden() || !isRenderLaneForTransition()) {
    // Return deferred (previous) value
    // Schedule transition to update later
    hook.memoizedState = prevValue;
    markDeferredValueHasPendingUpdate();
    return prevValue;
  }

  // In transition render - use new value
  hook.memoizedState = value;
  return value;
}

// Usage:
function List({ items }) {
  const deferredItems = useDeferredValue(items);
  // deferredItems updates with lower priority
  // allowing urgent updates to render first

  return <VirtualizedList items={deferredItems} />;
}
```

## Offscreen Rendering

### Offscreen Component

```javascript
// Offscreen is used internally for Suspense and future features
const OffscreenFiber = {
  tag: OffscreenComponent,
  memoizedState: {
    baseLanes: NoLanes,
    cachePool: null,
  },
  mode: 'visible' | 'hidden' | 'unstable-defer-without-hiding',
};

function updateOffscreenComponent(current, workInProgress, renderLanes) {
  const nextProps = workInProgress.pendingProps;
  const nextChildren = nextProps.children;
  const prevState = current !== null ? current.memoizedState : null;

  if (nextProps.mode === 'hidden') {
    // Don't render children
    if ((workInProgress.mode & ConcurrentMode) === NoMode) {
      // Legacy hidden - still render but hide
      workInProgress.memoizedState = { baseLanes: NoLanes, cachePool: null };
      pushRenderLanes(workInProgress, renderLanes);
    } else if (!includesSomeLane(renderLanes, OffscreenLane)) {
      // Skip rendering
      workInProgress.lanes = workInProgress.childLanes = OffscreenLane;
      return null;
    }
  }

  return reconcileChildren(current, workInProgress, nextChildren, renderLanes);
}
```

### Pre-rendering (Future Feature)

```javascript
// Offscreen enables pre-rendering content before it's visible
function Activity({ mode, children }) {
  return (
    <Offscreen mode={mode}>
      {children}
    </Offscreen>
  );
}

// Pre-render a route in the background
function App() {
  return (
    <>
      <VisibleRoute />
      <Activity mode="hidden">
        <PrerenderNextRoute />
      </Activity>
    </>
  );
}
```

## Selective Hydration

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    Selective Hydration                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Server HTML:                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  <div id="root">                                         │   │
│   │    <header>...</header>                                  │   │
│   │    <Suspense>                                            │   │
│   │      <main>Heavy content...</main>  ← Not hydrated yet  │   │
│   │    </Suspense>                                           │   │
│   │    <footer>...</footer>                                  │   │
│   │  </div>                                                  │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   User clicks on <main>:                                        │
│   1. Event is captured                                          │
│   2. React prioritizes hydrating <main>                         │
│   3. <main> becomes interactive                                 │
│   4. Event is replayed                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```javascript
function attemptHydrationAtCurrentPriority(fiber) {
  if (fiber.tag !== SuspenseComponent) {
    return;
  }

  const lanes = SyncLane;
  const root = enqueueConcurrentRenderForLane(fiber, lanes);

  if (root !== null) {
    // Priority boost for hydration
    const eventTime = requestEventTime();
    scheduleUpdateOnFiber(root, fiber, lanes, eventTime);
  }
}

// When user interacts with dehydrated content
function dispatchEventForDehydratedSuspenseBoundary(
  dehydratedSuspenseBoundary,
  domEventTarget,
  nativeEvent
) {
  // Queue the event for replay
  queueExplicitHydrationTarget(dehydratedSuspenseBoundary);

  // Store the event
  return {
    blockedOn: dehydratedSuspenseBoundary,
    domEventName,
    eventSystemFlags,
    nativeEvent,
    targetContainers: [domEventTarget],
  };
}
```

## Error Boundaries in Concurrent Mode

### Retry Logic

```javascript
// Concurrent mode enables smarter error recovery
function throwException(
  root,
  returnFiber,
  sourceFiber,
  value,
  rootRenderLanes
) {
  // Mark the source fiber as incomplete
  sourceFiber.flags |= Incomplete;

  if (
    value !== null &&
    typeof value === 'object' &&
    typeof value.then === 'function'
  ) {
    // Suspense - handled separately
    const wakeable = value;
    // ...
    return;
  }

  // It's an error
  const error = value;

  // Find the nearest error boundary
  let workInProgress = returnFiber;
  do {
    switch (workInProgress.tag) {
      case ClassComponent: {
        const errorInfo = value;
        if (typeof workInProgress.type.getDerivedStateFromError === 'function') {
          workInProgress.flags |= ShouldCapture;
          const update = createClassErrorUpdate(workInProgress, error, rootRenderLanes);
          enqueueCapturedUpdate(workInProgress, update);
          return;
        }
        break;
      }
    }
    workInProgress = workInProgress.return;
  } while (workInProgress !== null);
}
```

## Summary

In this chapter, you've learned:

- **Concurrent Rendering**: Time-sliced, interruptible rendering
- **Suspense**: Promise-based data loading with fallbacks
- **Transitions**: Low-priority updates that can be interrupted
- **Offscreen**: Hidden rendering for pre-loading
- **Selective Hydration**: Priority-based hydration

## Key Takeaways

1. **Interruptible**: Concurrent rendering yields to browser
2. **Promise-based**: Suspense catches thrown Promises
3. **Priority system**: Transitions use lower priority lanes
4. **Fallback handling**: Suspense shows fallback during loading
5. **Smart hydration**: User interactions prioritize hydration

## Next Steps

Now that you understand concurrent features, let's explore debugging and profiling React applications in Chapter 8: Debugging and Profiling.

---

**Ready for Chapter 8?** [Debugging and Profiling](08-debugging.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `workInProgress`, `root`, `mode` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Concurrent Features` as an operating subsystem inside **React Fiber Internals**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `lanes`, `Suspense`, `memoizedState` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Concurrent Features` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `workInProgress`.
2. **Input normalization**: shape incoming data so `root` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `mode`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `workInProgress` and `root` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Hooks Implementation](06-hooks.md)
- [Next Chapter: Chapter 8: Debugging and Profiling](08-debugging.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
