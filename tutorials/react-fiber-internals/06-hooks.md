---
layout: default
title: "Chapter 6: Hooks Implementation"
parent: "React Fiber Internals"
nav_order: 6
---

# Chapter 6: Hooks Implementation

> Understanding how React implements hooks internally using linked lists and the fiber's memoizedState.

## Overview

Hooks are functions that let you "hook into" React state and lifecycle features from function components. Internally, hooks are stored as a linked list on the fiber's `memoizedState` property.

## Hook Architecture

### Hook Storage Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fiber and Hooks                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Fiber                                                         │
│   ┌─────────────────────────────────────────────────────┐       │
│   │  tag: FunctionComponent                             │       │
│   │  type: MyComponent                                  │       │
│   │  memoizedState: ─────────────────┐                  │       │
│   │  updateQueue: ─────────┐         │                  │       │
│   └────────────────────────┼─────────┼──────────────────┘       │
│                            │         │                          │
│                            ▼         ▼                          │
│   UpdateQueue          Hook Linked List                         │
│   ┌───────────┐        ┌─────────┐    ┌─────────┐               │
│   │lastEffect │───────▶│ Hook 1  │───▶│ Hook 2  │──▶ ...       │
│   └───────────┘        │useState │    │useEffect│               │
│                        └─────────┘    └─────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Hook Object Structure

```javascript
// Each hook is an object in the linked list
interface Hook {
  memoizedState: any;          // Current state value
  baseState: any;              // State before pending updates
  baseQueue: Update | null;    // First update in queue
  queue: UpdateQueue | null;   // Update queue for this hook
  next: Hook | null;           // Next hook in the list
}

// Example for useState:
const useStateHook = {
  memoizedState: 0,            // Current count value
  baseState: 0,                // Base state
  baseQueue: null,
  queue: {
    pending: null,             // Circular list of updates
    dispatch: boundDispatch,   // dispatch function
    lastRenderedReducer: basicStateReducer,
    lastRenderedState: 0,
  },
  next: null,                  // Points to next hook
};
```

## The Dispatcher

### Dispatcher Pattern

```javascript
// React uses different dispatchers for mount vs update
const HooksDispatcherOnMount = {
  useState: mountState,
  useEffect: mountEffect,
  useReducer: mountReducer,
  useCallback: mountCallback,
  useMemo: mountMemo,
  useRef: mountRef,
  useContext: readContext,
  // ... more hooks
};

const HooksDispatcherOnUpdate = {
  useState: updateState,
  useEffect: updateEffect,
  useReducer: updateReducer,
  useCallback: updateCallback,
  useMemo: updateMemo,
  useRef: updateRef,
  useContext: readContext,
  // ... more hooks
};

// The current dispatcher is switched during render
let ReactCurrentDispatcher = {
  current: null,
};

function renderWithHooks(current, workInProgress, Component, props, lanes) {
  currentlyRenderingFiber = workInProgress;
  workInProgress.memoizedState = null;
  workInProgress.updateQueue = null;

  // Select dispatcher based on mount vs update
  ReactCurrentDispatcher.current =
    current === null || current.memoizedState === null
      ? HooksDispatcherOnMount
      : HooksDispatcherOnUpdate;

  // Call the component
  let children = Component(props);

  // Cleanup
  ReactCurrentDispatcher.current = ContextOnlyDispatcher;
  currentlyRenderingFiber = null;

  return children;
}
```

## useState Implementation

### mountState (First Render)

```javascript
function mountState(initialState) {
  // Create a new hook
  const hook = mountWorkInProgressHook();

  // Initialize state
  if (typeof initialState === 'function') {
    initialState = initialState();
  }

  hook.memoizedState = hook.baseState = initialState;

  // Create update queue
  const queue = {
    pending: null,
    interleaved: null,
    lanes: NoLanes,
    dispatch: null,
    lastRenderedReducer: basicStateReducer,
    lastRenderedState: initialState,
  };
  hook.queue = queue;

  // Create dispatch function bound to this fiber and queue
  const dispatch = (queue.dispatch = dispatchSetState.bind(
    null,
    currentlyRenderingFiber,
    queue
  ));

  return [hook.memoizedState, dispatch];
}

// Helper to create a new hook
function mountWorkInProgressHook() {
  const hook = {
    memoizedState: null,
    baseState: null,
    baseQueue: null,
    queue: null,
    next: null,
  };

  if (workInProgressHook === null) {
    // First hook in the list
    currentlyRenderingFiber.memoizedState = workInProgressHook = hook;
  } else {
    // Append to the list
    workInProgressHook = workInProgressHook.next = hook;
  }

  return workInProgressHook;
}
```

### updateState (Re-renders)

```javascript
function updateState(initialState) {
  return updateReducer(basicStateReducer, initialState);
}

function updateReducer(reducer, initialArg) {
  // Get the corresponding hook from previous render
  const hook = updateWorkInProgressHook();
  const queue = hook.queue;

  queue.lastRenderedReducer = reducer;

  const current = currentHook;
  let baseQueue = current.baseQueue;

  // Check for pending updates
  const pendingQueue = queue.pending;
  if (pendingQueue !== null) {
    // Merge pending queue with base queue
    if (baseQueue !== null) {
      const baseFirst = baseQueue.next;
      const pendingFirst = pendingQueue.next;
      baseQueue.next = pendingFirst;
      pendingQueue.next = baseFirst;
    }
    current.baseQueue = baseQueue = pendingQueue;
    queue.pending = null;
  }

  if (baseQueue !== null) {
    // Process the queue
    const first = baseQueue.next;
    let newState = current.baseState;
    let update = first;

    do {
      // Apply each update
      const action = update.action;
      newState = reducer(newState, action);
      update = update.next;
    } while (update !== null && update !== first);

    hook.memoizedState = newState;
    hook.baseState = newState;
    queue.lastRenderedState = newState;
  }

  const dispatch = queue.dispatch;
  return [hook.memoizedState, dispatch];
}

function updateWorkInProgressHook() {
  // Get the next hook from the current tree
  let nextCurrentHook;
  if (currentHook === null) {
    const current = currentlyRenderingFiber.alternate;
    nextCurrentHook = current !== null ? current.memoizedState : null;
  } else {
    nextCurrentHook = currentHook.next;
  }

  // Create work-in-progress hook
  let nextWorkInProgressHook;
  if (workInProgressHook === null) {
    nextWorkInProgressHook = currentlyRenderingFiber.memoizedState;
  } else {
    nextWorkInProgressHook = workInProgressHook.next;
  }

  if (nextWorkInProgressHook !== null) {
    // Reuse existing work-in-progress hook
    workInProgressHook = nextWorkInProgressHook;
    currentHook = nextCurrentHook;
  } else {
    // Clone from current hook
    currentHook = nextCurrentHook;

    const newHook = {
      memoizedState: currentHook.memoizedState,
      baseState: currentHook.baseState,
      baseQueue: currentHook.baseQueue,
      queue: currentHook.queue,
      next: null,
    };

    if (workInProgressHook === null) {
      currentlyRenderingFiber.memoizedState = workInProgressHook = newHook;
    } else {
      workInProgressHook = workInProgressHook.next = newHook;
    }
  }

  return workInProgressHook;
}
```

### dispatchSetState

```javascript
function dispatchSetState(fiber, queue, action) {
  // Get the update lane
  const lane = requestUpdateLane(fiber);

  // Create update object
  const update = {
    lane,
    action,
    hasEagerState: false,
    eagerState: null,
    next: null,
  };

  // Optimization: compute state eagerly if possible
  if (fiber.lanes === NoLanes && (fiber.alternate === null || fiber.alternate.lanes === NoLanes)) {
    const lastRenderedReducer = queue.lastRenderedReducer;
    if (lastRenderedReducer !== null) {
      const currentState = queue.lastRenderedState;
      const eagerState = lastRenderedReducer(currentState, action);
      update.hasEagerState = true;
      update.eagerState = eagerState;

      if (Object.is(eagerState, currentState)) {
        // State didn't change - bail out early
        return;
      }
    }
  }

  // Enqueue the update (circular linked list)
  const pending = queue.pending;
  if (pending === null) {
    update.next = update; // Circular: points to itself
  } else {
    update.next = pending.next;
    pending.next = update;
  }
  queue.pending = update;

  // Schedule re-render
  scheduleUpdateOnFiber(fiber, lane);
}
```

## useEffect Implementation

### Effect Structure

```javascript
// Effects are stored differently from state hooks
interface Effect {
  tag: HookFlags;              // Effect type flags
  create: () => (() => void) | void;  // Setup function
  destroy: (() => void) | void;       // Cleanup function
  deps: Array<mixed> | null;          // Dependency array
  next: Effect;                       // Next effect (circular list)
}

// Effect flags
const HookPassive = 0b0001;    // useEffect
const HookLayout = 0b0010;     // useLayoutEffect
const HookInsertion = 0b0100;  // useInsertionEffect
const HasEffect = 0b1000;      // Effect should run
```

### mountEffect

```javascript
function mountEffect(create, deps) {
  return mountEffectImpl(
    PassiveEffect | PassiveStaticEffect,
    HookPassive,
    create,
    deps
  );
}

function mountEffectImpl(fiberFlags, hookFlags, create, deps) {
  const hook = mountWorkInProgressHook();

  const nextDeps = deps === undefined ? null : deps;

  // Mark fiber for passive effects
  currentlyRenderingFiber.flags |= fiberFlags;

  // Store effect on hook and in effect list
  hook.memoizedState = pushEffect(
    HookHasEffect | hookFlags,
    create,
    undefined, // No cleanup yet
    nextDeps
  );
}

function pushEffect(tag, create, destroy, deps) {
  const effect = {
    tag,
    create,
    destroy,
    deps,
    next: null,
  };

  let componentUpdateQueue = currentlyRenderingFiber.updateQueue;

  if (componentUpdateQueue === null) {
    // Create effect list
    componentUpdateQueue = { lastEffect: null };
    currentlyRenderingFiber.updateQueue = componentUpdateQueue;
    componentUpdateQueue.lastEffect = effect.next = effect; // Circular
  } else {
    // Append to existing effect list
    const lastEffect = componentUpdateQueue.lastEffect;
    if (lastEffect === null) {
      componentUpdateQueue.lastEffect = effect.next = effect;
    } else {
      const firstEffect = lastEffect.next;
      lastEffect.next = effect;
      effect.next = firstEffect;
      componentUpdateQueue.lastEffect = effect;
    }
  }

  return effect;
}
```

### updateEffect

```javascript
function updateEffect(create, deps) {
  return updateEffectImpl(PassiveEffect, HookPassive, create, deps);
}

function updateEffectImpl(fiberFlags, hookFlags, create, deps) {
  const hook = updateWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;
  let destroy = undefined;

  if (currentHook !== null) {
    const prevEffect = currentHook.memoizedState;
    destroy = prevEffect.destroy;

    if (nextDeps !== null) {
      const prevDeps = prevEffect.deps;
      if (areHookInputsEqual(nextDeps, prevDeps)) {
        // Dependencies haven't changed - skip effect
        hook.memoizedState = pushEffect(hookFlags, create, destroy, nextDeps);
        return;
      }
    }
  }

  // Dependencies changed - mark effect for execution
  currentlyRenderingFiber.flags |= fiberFlags;
  hook.memoizedState = pushEffect(
    HookHasEffect | hookFlags,
    create,
    destroy,
    nextDeps
  );
}

function areHookInputsEqual(nextDeps, prevDeps) {
  if (prevDeps === null) {
    return false;
  }

  for (let i = 0; i < prevDeps.length && i < nextDeps.length; i++) {
    if (Object.is(nextDeps[i], prevDeps[i])) {
      continue;
    }
    return false;
  }

  return true;
}
```

## useMemo and useCallback

### useMemo Implementation

```javascript
function mountMemo(nextCreate, deps) {
  const hook = mountWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;

  // Compute and store the value
  const nextValue = nextCreate();
  hook.memoizedState = [nextValue, nextDeps];

  return nextValue;
}

function updateMemo(nextCreate, deps) {
  const hook = updateWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;
  const prevState = hook.memoizedState;

  if (prevState !== null && nextDeps !== null) {
    const prevDeps = prevState[1];
    if (areHookInputsEqual(nextDeps, prevDeps)) {
      // Dependencies haven't changed - return cached value
      return prevState[0];
    }
  }

  // Dependencies changed - recompute
  const nextValue = nextCreate();
  hook.memoizedState = [nextValue, nextDeps];

  return nextValue;
}
```

### useCallback Implementation

```javascript
function mountCallback(callback, deps) {
  const hook = mountWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;

  // Store the callback itself (not the result)
  hook.memoizedState = [callback, nextDeps];

  return callback;
}

function updateCallback(callback, deps) {
  const hook = updateWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;
  const prevState = hook.memoizedState;

  if (prevState !== null && nextDeps !== null) {
    const prevDeps = prevState[1];
    if (areHookInputsEqual(nextDeps, prevDeps)) {
      // Dependencies haven't changed - return cached callback
      return prevState[0];
    }
  }

  // Dependencies changed - return new callback
  hook.memoizedState = [callback, nextDeps];

  return callback;
}
```

## useRef Implementation

```javascript
function mountRef(initialValue) {
  const hook = mountWorkInProgressHook();

  // Create ref object
  const ref = { current: initialValue };
  hook.memoizedState = ref;

  return ref;
}

function updateRef(initialValue) {
  const hook = updateWorkInProgressHook();
  // Just return the same ref object
  return hook.memoizedState;
}
```

## useContext Implementation

```javascript
// useContext doesn't use the hook linked list
function readContext(context) {
  const value = isPrimaryRenderer
    ? context._currentValue
    : context._currentValue2;

  // Track context dependency
  if (lastContextDependency === null) {
    const contextItem = {
      context,
      memoizedValue: value,
      next: null,
    };

    lastContextDependency = contextItem;
    currentlyRenderingFiber.dependencies = {
      lanes: NoLanes,
      firstContext: contextItem,
    };
  } else {
    const contextItem = {
      context,
      memoizedValue: value,
      next: null,
    };
    lastContextDependency = lastContextDependency.next = contextItem;
  }

  return value;
}
```

## Rules of Hooks

### Why Hooks Must Be Called in Order

```javascript
// This component has three hooks
function Counter() {
  const [count, setCount] = useState(0);      // Hook 1
  const [name, setName] = useState('React');   // Hook 2
  useEffect(() => { /* ... */ }, [count]);    // Hook 3

  // ...
}

// First render - hooks are mounted in order:
// Fiber.memoizedState:
//   Hook1(count) → Hook2(name) → Hook3(effect) → null

// On re-render, React walks the same list:
// Fiber.memoizedState:
//   Hook1(count) → Hook2(name) → Hook3(effect) → null
//     ↑              ↑              ↑
//   useState(0)  useState('React')  useEffect()

// If you conditionally call hooks:
function BrokenCounter({ condition }) {
  const [count, setCount] = useState(0);      // Hook 1

  if (condition) {
    const [name, setName] = useState('React'); // Hook 2 - SOMETIMES
  }

  useEffect(() => { /* ... */ }, [count]);    // Hook 2 or 3?

  // When condition changes from true to false:
  // React expects: Hook1 → Hook2 → Hook3
  // But gets:      Hook1 → Hook3 (useEffect)
  // Hook3 receives Hook2's state! BUG!
}
```

### Visualization of Hook Order

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hook Order Matters                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   CORRECT - Same order every render:                            │
│                                                                 │
│   Render 1:  useState(0) → useState('') → useEffect()          │
│   Render 2:  useState(0) → useState('') → useEffect()          │
│   Render 3:  useState(0) → useState('') → useEffect()          │
│                  ↓            ↓               ↓                 │
│              Hook 1       Hook 2          Hook 3                │
│                                                                 │
│   WRONG - Different order:                                      │
│                                                                 │
│   Render 1:  useState(0) → useState('') → useEffect()          │
│   Render 2:  useState(0) → useEffect()    ← SKIP!              │
│              Hook 1 gets  Hook 2 gets                          │
│              correct      WRONG STATE!                          │
│              state                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Custom Hooks

### How Custom Hooks Work

```javascript
// Custom hooks are just functions that call other hooks
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  const decrement = useCallback(() => {
    setCount(c => c - 1);
  }, []);

  return { count, increment, decrement };
}

// When used in a component:
function MyComponent() {
  const { count, increment } = useCounter(10);
  //       ↑
  // Under the hood, this creates 3 hooks:
  // 1. useState(10)
  // 2. useCallback(increment)
  // 3. useCallback(decrement)

  return <button onClick={increment}>{count}</button>;
}
```

## Summary

In this chapter, you've learned:

- **Hook Storage**: Linked list on fiber.memoizedState
- **Dispatcher Pattern**: Different implementations for mount/update
- **useState**: State stored in hook with update queue
- **useEffect**: Effects stored separately with dependency tracking
- **useMemo/useCallback**: Value caching with dependencies
- **Rules of Hooks**: Why order must be consistent

## Key Takeaways

1. **Linked list**: Hooks are stored as a linked list
2. **Order matters**: Hooks must be called in the same order
3. **Two phases**: Mount creates hooks, update reuses them
4. **Eager bailout**: useState can skip re-render if state unchanged
5. **Effect list**: Effects are tracked separately for commit phase

## Next Steps

Now that you understand hooks implementation, let's explore concurrent rendering features in Chapter 7: Concurrent Features.

---

**Ready for Chapter 7?** [Concurrent Features](07-concurrent.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
