---
layout: default
title: "Chapter 8: Debugging and Profiling"
parent: "React Fiber Internals"
nav_order: 8
---

# Chapter 8: Debugging and Profiling

> Tools and techniques for debugging React internals and profiling performance.

## Overview

Understanding React's debugging infrastructure helps you diagnose issues and optimize performance. This chapter covers React DevTools internals, the Profiler API, and techniques for debugging fiber trees.

## React DevTools Architecture

### How DevTools Connects

```
┌─────────────────────────────────────────────────────────────────┐
│                    DevTools Architecture                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Browser                              DevTools Extension       │
│   ┌─────────────────────────┐          ┌─────────────────────┐  │
│   │                         │          │                     │  │
│   │   React App             │          │   DevTools UI       │  │
│   │   ┌─────────────────┐   │          │   ┌─────────────┐   │  │
│   │   │  Fiber Tree     │   │          │   │ Components  │   │  │
│   │   │                 │   │          │   │ Profiler    │   │  │
│   │   └─────────────────┘   │   ◀───▶  │   └─────────────┘   │  │
│   │   ┌─────────────────┐   │  Bridge  │                     │  │
│   │   │  DevTools Hook  │   │  (JSON)  │                     │  │
│   │   │  (injected)     │   │          │                     │  │
│   │   └─────────────────┘   │          │                     │  │
│   │                         │          │                     │  │
│   └─────────────────────────┘          └─────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### DevTools Hook

```javascript
// DevTools injects a hook into the page
window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
  renderers: new Map(),
  supportsFiber: true,

  // Called when React renderer attaches
  inject(renderer) {
    const id = nextRendererID++;
    this.renderers.set(id, renderer);
    return id;
  },

  // Fiber operations
  onCommitFiberRoot(rendererID, root, priorityLevel) {
    // Notify DevTools of committed tree
    const current = root.current;
    walkFiberTree(current, (fiber) => {
      sendFiberToDevTools(fiber);
    });
  },

  onCommitFiberUnmount(rendererID, fiber) {
    // Notify DevTools of unmounted fiber
  },
};

// React connects during initialization
function injectInternals(internals) {
  const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
  if (hook === undefined) {
    return false;
  }

  hook.inject({
    bundleType: __DEV__ ? 1 : 0,
    version: ReactVersion,
    rendererPackageName: 'react-dom',
    findFiberByHostInstance,
    // ... more methods
  });

  return true;
}
```

### Fiber Inspection

```javascript
// DevTools extracts info from fibers
function getDisplayName(fiber) {
  const type = fiber.type;

  if (type === null) {
    return null;
  }

  if (typeof type === 'function') {
    return type.displayName || type.name || 'Anonymous';
  }

  if (typeof type === 'string') {
    return type;
  }

  switch (type) {
    case REACT_FRAGMENT_TYPE:
      return 'Fragment';
    case REACT_SUSPENSE_TYPE:
      return 'Suspense';
    case REACT_STRICT_MODE_TYPE:
      return 'StrictMode';
    // ... more cases
  }

  return null;
}

function getOwnersList(fiber) {
  const owners = [];
  let current = fiber;

  while (current !== null) {
    if (current._debugOwner !== null) {
      owners.push({
        displayName: getDisplayName(current._debugOwner),
        fiber: current._debugOwner,
      });
    }
    current = current._debugOwner;
  }

  return owners;
}
```

## Profiler API

### Built-in Profiler Component

```jsx
import { Profiler } from 'react';

function onRenderCallback(
  id,                   // Profiler id
  phase,                // "mount" | "update" | "nested-update"
  actualDuration,       // Time spent rendering
  baseDuration,         // Estimated time without memoization
  startTime,            // When React started rendering
  commitTime,           // When React committed
  interactions          // Set of interactions (deprecated)
) {
  console.log({
    id,
    phase,
    actualDuration,
    baseDuration,
    startTime,
    commitTime,
  });
}

function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <Navigation />
      <Main />
    </Profiler>
  );
}
```

### Profiler Implementation

```javascript
// During render, React tracks timing
function recordRender(workInProgress) {
  if (enableProfilerTimer) {
    workInProgress.actualDuration = 0;
    workInProgress.actualStartTime = now();
  }
}

function stopProfilerTimerIfRunning(fiber) {
  if (enableProfilerTimer) {
    const elapsedTime = now() - fiber.actualStartTime;
    fiber.actualDuration += elapsedTime;
  }
}

// Profiler fiber collects child timing
function updateProfiler(current, workInProgress, renderLanes) {
  if (enableProfilerTimer) {
    workInProgress.flags |= Update;

    // Reset timing for new render
    workInProgress.stateNode.effectDuration = 0;
    workInProgress.stateNode.passiveEffectDuration = 0;
  }

  const nextProps = workInProgress.pendingProps;
  const nextChildren = nextProps.children;

  reconcileChildren(current, workInProgress, nextChildren, renderLanes);

  return workInProgress.child;
}

// During commit, profiler callback is invoked
function commitProfilerUpdate(finishedWork) {
  const { onRender } = finishedWork.memoizedProps;

  if (typeof onRender === 'function') {
    onRender(
      finishedWork.memoizedProps.id,
      current === null ? 'mount' : 'update',
      finishedWork.actualDuration,
      finishedWork.treeBaseDuration,
      finishedWork.actualStartTime,
      commitTime,
      finishedWork.stateNode.interactions
    );
  }
}
```

## Performance Monitoring

### React's Internal Marks

```javascript
// React uses Performance API for detailed timing
function markRenderStarted(lanes) {
  if (enableSchedulingProfiler) {
    performance.mark(`--react-render-start-${lanes}`);
  }
}

function markRenderStopped() {
  if (enableSchedulingProfiler) {
    performance.mark('--react-render-stop');
  }
}

function markCommitStarted(lanes) {
  if (enableSchedulingProfiler) {
    performance.mark(`--react-commit-start-${lanes}`);
  }
}

function markCommitStopped() {
  if (enableSchedulingProfiler) {
    performance.mark('--react-commit-stop');
  }
}

// Lanes are also marked
function markLanesMeasure(lanes, label) {
  if (enableSchedulingProfiler) {
    performance.measure(label, {
      start: `--react-lane-${lanes}`,
      end: `--react-commit-stop`,
    });
  }
}
```

### Schedule Profiler

```
┌─────────────────────────────────────────────────────────────────┐
│                    Scheduling Profiler Timeline                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Time →                                                        │
│   0ms    10ms    20ms    30ms    40ms    50ms    60ms           │
│   │       │       │       │       │       │       │             │
│   ├───────┼───────┼───────┼───────┼───────┼───────┤             │
│   │ ████████████  │       │ ██████████████████   │             │
│   │ Sync Render   │       │ Concurrent Render    │             │
│   │               │       │                      │             │
│   │       │  ███  │       │       │  ████  │     │             │
│   │       │Commit │       │       │ Commit │     │             │
│   │       │       │       │       │        │     │             │
│   │       │       │       │       │        │     │             │
│   │       │       │  ↑    │       │        │     │             │
│   │       │       │ User  │       │        │     │             │
│   │       │       │ Input │       │        │     │             │
│   │       │       │       │       │        │     │             │
│   └───────┴───────┴───────┴───────┴────────┴─────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Debug Info in Development

### Component Stack

```javascript
// React tracks component stack in development
let currentDebugFiberInDEV = null;

function getCurrentFiberStackInDev() {
  if (__DEV__) {
    if (currentDebugFiberInDEV === null) {
      return '';
    }

    let stack = '';
    let workInProgress = currentDebugFiberInDEV;

    while (workInProgress !== null) {
      stack = describeFiber(workInProgress) + stack;
      workInProgress = workInProgress.return;
    }

    return stack;
  }
  return '';
}

function describeFiber(fiber) {
  const owner = fiber._debugOwner;
  const source = fiber._debugSource;

  let ownerName = null;
  if (owner !== null) {
    ownerName = getComponentName(owner.type);
  }

  let info = '';
  if (source) {
    info = ` (at ${source.fileName}:${source.lineNumber})`;
  } else if (ownerName) {
    info = ` (created by ${ownerName})`;
  }

  return '\n    in ' + (getComponentName(fiber.type) || 'Unknown') + info;
}
```

### Error Messages

```javascript
// React provides helpful error messages with component stacks
function createCapturedValue(value, source) {
  return {
    value,
    source,
    stack: getStackByFiberInDevAndProd(source),
  };
}

// Example error output:
// Error: Something went wrong
//     in ChildComponent (at App.js:15)
//     in ParentComponent (at App.js:10)
//     in App (at index.js:5)
```

## Debugging Techniques

### Accessing Fiber from DOM

```javascript
// Get fiber from DOM element
function findFiberByHostInstance(hostInstance) {
  const internalKey = Object.keys(hostInstance).find(
    key => key.startsWith('__reactFiber$')
  );

  if (internalKey) {
    return hostInstance[internalKey];
  }

  return null;
}

// Usage in browser console:
const element = document.querySelector('.my-component');
const fiber = findFiberByHostInstance(element);

console.log({
  type: fiber.type,
  props: fiber.memoizedProps,
  state: fiber.memoizedState,
  parent: fiber.return,
  children: fiber.child,
});
```

### Walking the Fiber Tree

```javascript
// Utility to walk and log fiber tree
function logFiberTree(fiber, depth = 0) {
  const indent = '  '.repeat(depth);
  const name = getDisplayName(fiber) || fiber.tag;

  console.log(`${indent}${name}`, {
    tag: fiber.tag,
    flags: fiber.flags.toString(2),
    lanes: fiber.lanes.toString(2),
  });

  if (fiber.child) {
    logFiberTree(fiber.child, depth + 1);
  }

  if (fiber.sibling) {
    logFiberTree(fiber.sibling, depth);
  }
}

// Get root fiber
const container = document.getElementById('root');
const rootFiber = container._reactRootContainer._internalRoot.current;
logFiberTree(rootFiber);
```

### Inspecting Hooks

```javascript
// Hooks are stored as linked list on memoizedState
function logHooks(fiber) {
  if (fiber.tag !== FunctionComponent) {
    console.log('Not a function component');
    return;
  }

  let hook = fiber.memoizedState;
  let index = 0;

  while (hook !== null) {
    console.log(`Hook ${index}:`, {
      memoizedState: hook.memoizedState,
      queue: hook.queue,
      baseState: hook.baseState,
    });

    hook = hook.next;
    index++;
  }
}
```

## Common Performance Issues

### Identifying Wasted Renders

```javascript
// Using Profiler to detect wasted renders
function WastedRenderDetector({ children }) {
  const renderCount = useRef(0);
  const prevProps = useRef();

  return (
    <Profiler
      id="WastedRenderDetector"
      onRender={(id, phase, actualDuration, baseDuration) => {
        renderCount.current++;

        if (phase === 'update' && actualDuration < 1) {
          console.warn('Potentially wasted render:', {
            renderCount: renderCount.current,
            duration: actualDuration,
          });
        }
      }}
    >
      {children}
    </Profiler>
  );
}
```

### Detecting Expensive Operations

```javascript
// Custom hook to warn about expensive renders
function useRenderTiming(componentName) {
  const startTime = performance.now();

  useEffect(() => {
    const endTime = performance.now();
    const duration = endTime - startTime;

    if (duration > 16) { // More than one frame
      console.warn(
        `${componentName} took ${duration.toFixed(2)}ms to render`
      );
    }
  });
}

// Usage
function ExpensiveComponent() {
  useRenderTiming('ExpensiveComponent');

  // ... expensive render logic
}
```

### Debugging Suspense

```javascript
// Track Suspense boundaries
function SuspenseDebugger({ name, children, fallback }) {
  const [suspenseCount, setSuspenseCount] = useState(0);

  useEffect(() => {
    console.log(`[${name}] Mounted`);
    return () => console.log(`[${name}] Unmounted`);
  }, [name]);

  return (
    <Suspense
      fallback={
        <SuspenseTracker
          name={name}
          onSuspend={() => {
            setSuspenseCount(c => c + 1);
            console.log(`[${name}] Suspended (count: ${suspenseCount + 1})`);
          }}
        >
          {fallback}
        </SuspenseTracker>
      }
    >
      {children}
    </Suspense>
  );
}

function SuspenseTracker({ name, onSuspend, children }) {
  useEffect(() => {
    onSuspend();
    return () => console.log(`[${name}] Resolved`);
  }, []);

  return children;
}
```

## Best Practices

### Development vs Production

```javascript
// Different behaviors in development
if (__DEV__) {
  // Extra validation
  // Component stack traces
  // Strict mode double rendering
  // Detailed error messages
}

// Production optimizations
if (!__DEV__) {
  // Minified error codes
  // No extra renders
  // Smaller bundle size
}
```

### Using React.StrictMode

```jsx
// StrictMode helps find common bugs
function App() {
  return (
    <React.StrictMode>
      <MyApp />
    </React.StrictMode>
  );
}

// StrictMode does:
// 1. Double-invokes render phase (mount/unmount/remount)
// 2. Warns about deprecated APIs
// 3. Warns about legacy context
// 4. Detects side effects in render
```

## Summary

In this chapter, you've learned:

- **DevTools Architecture**: How DevTools connects to React
- **Profiler API**: Measuring component render performance
- **Performance Marks**: React's internal timing system
- **Debug Techniques**: Accessing fibers and hooks
- **Common Issues**: Detecting wasted renders and performance problems

## Key Takeaways

1. **DevTools hook**: Global hook enables inspection
2. **Profiler**: Built-in component for timing
3. **Development extras**: Rich debugging in dev mode
4. **Fiber inspection**: Access via DOM elements
5. **StrictMode**: Catches common bugs early

## Tutorial Complete!

Congratulations! You've completed the React Fiber Internals tutorial. You now understand:

- How Fiber represents work units
- The render and commit phase architecture
- Scheduling and the lanes priority system
- Hooks implementation with linked lists
- Concurrent features like Suspense and transitions
- Debugging and profiling techniques

## Further Reading

- [React Source Code](https://github.com/facebook/react)
- [React Working Group Discussions](https://github.com/reactwg)
- [React Blog](https://react.dev/blog)

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
