---
layout: default
title: "Chapter 4: Commit Phase"
parent: "React Fiber Internals"
nav_order: 4
---

# Chapter 4: Commit Phase

> How React applies changes to the DOM and executes side effects.

## Overview

The Commit Phase is where React takes the work-in-progress tree built during the Render Phase and applies all changes to the actual DOM. Unlike the Render Phase, the Commit Phase is **synchronous and cannot be interrupted**.

## Commit Phase Structure

### Three Sub-Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                    Commit Phase Structure                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. Before Mutation Phase                                │    │
│  │     • getSnapshotBeforeUpdate (class components)        │    │
│  │     • Read DOM before changes                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  2. Mutation Phase                                       │    │
│  │     • Insert/Update/Delete DOM nodes                    │    │
│  │     • Update refs                                        │    │
│  │     • Call componentWillUnmount                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  3. Layout Phase                                         │    │
│  │     • componentDidMount/componentDidUpdate              │    │
│  │     • useLayoutEffect callbacks                         │    │
│  │     • Attach refs                                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  4. Passive Effects (async, after paint)                │    │
│  │     • useEffect callbacks                                │    │
│  │     • Scheduled via scheduler                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Starting the Commit

### commitRoot

```javascript
function commitRoot(root) {
  const finishedWork = root.finishedWork;
  const lanes = root.finishedLanes;

  if (finishedWork === null) {
    return null;
  }

  // Clear the finished work
  root.finishedWork = null;
  root.finishedLanes = NoLanes;

  // Check if there are any effects
  const subtreeHasEffects =
    (finishedWork.subtreeFlags & (BeforeMutationMask | MutationMask | LayoutMask | PassiveMask)) !== NoFlags;
  const rootHasEffect =
    (finishedWork.flags & (BeforeMutationMask | MutationMask | LayoutMask | PassiveMask)) !== NoFlags;

  if (subtreeHasEffects || rootHasEffect) {
    // Execute commit phases
    commitBeforeMutationEffects(root, finishedWork);
    commitMutationEffects(root, finishedWork, lanes);

    // Swap trees: work-in-progress becomes current
    root.current = finishedWork;

    commitLayoutEffects(finishedWork, root, lanes);
  } else {
    // No effects - just swap trees
    root.current = finishedWork;
  }

  // Schedule passive effects
  if (rootDoesHavePassiveEffects) {
    scheduleCallback(NormalSchedulerPriority, flushPassiveEffects);
  }

  // Check for remaining work
  ensureRootIsScheduled(root);
}
```

## Before Mutation Phase

### Purpose

This phase runs **before** any DOM mutations. It's used for:
- Reading DOM measurements
- `getSnapshotBeforeUpdate` lifecycle

```javascript
function commitBeforeMutationEffects(root, firstChild) {
  nextEffect = firstChild;
  commitBeforeMutationEffects_begin();
}

function commitBeforeMutationEffects_begin() {
  while (nextEffect !== null) {
    const fiber = nextEffect;
    const child = fiber.child;

    // Traverse to children with effects
    if ((fiber.subtreeFlags & BeforeMutationMask) !== NoFlags && child !== null) {
      child.return = fiber;
      nextEffect = child;
    } else {
      commitBeforeMutationEffects_complete();
    }
  }
}

function commitBeforeMutationEffects_complete() {
  while (nextEffect !== null) {
    const fiber = nextEffect;

    if ((fiber.flags & BeforeMutation) !== NoFlags) {
      commitBeforeMutationEffectsOnFiber(fiber);
    }

    const sibling = fiber.sibling;
    if (sibling !== null) {
      sibling.return = fiber.return;
      nextEffect = sibling;
      return;
    }

    nextEffect = fiber.return;
  }
}

function commitBeforeMutationEffectsOnFiber(fiber) {
  const current = fiber.alternate;

  switch (fiber.tag) {
    case ClassComponent: {
      if ((fiber.flags & Snapshot) !== NoFlags) {
        if (current !== null) {
          const prevProps = current.memoizedProps;
          const prevState = current.memoizedState;
          const instance = fiber.stateNode;

          // Call getSnapshotBeforeUpdate
          const snapshot = instance.getSnapshotBeforeUpdate(
            prevProps,
            prevState
          );
          instance.__reactInternalSnapshotBeforeUpdate = snapshot;
        }
      }
      break;
    }
    // ... other cases
  }
}
```

## Mutation Phase

### commitMutationEffects

```javascript
function commitMutationEffects(root, finishedWork, committedLanes) {
  nextEffect = finishedWork;
  commitMutationEffects_begin(root, committedLanes);
}

function commitMutationEffects_begin(root, lanes) {
  while (nextEffect !== null) {
    const fiber = nextEffect;

    // Handle deletions first (before processing children)
    const deletions = fiber.deletions;
    if (deletions !== null) {
      for (let i = 0; i < deletions.length; i++) {
        const childToDelete = deletions[i];
        commitDeletionEffects(root, fiber, childToDelete);
      }
    }

    const child = fiber.child;
    if ((fiber.subtreeFlags & MutationMask) !== NoFlags && child !== null) {
      child.return = fiber;
      nextEffect = child;
    } else {
      commitMutationEffects_complete(root, lanes);
    }
  }
}

function commitMutationEffects_complete(root, lanes) {
  while (nextEffect !== null) {
    const fiber = nextEffect;

    commitMutationEffectsOnFiber(fiber, root, lanes);

    const sibling = fiber.sibling;
    if (sibling !== null) {
      sibling.return = fiber.return;
      nextEffect = sibling;
      return;
    }

    nextEffect = fiber.return;
  }
}
```

### DOM Operations

```javascript
function commitMutationEffectsOnFiber(finishedWork, root, lanes) {
  const current = finishedWork.alternate;
  const flags = finishedWork.flags;

  switch (finishedWork.tag) {
    case HostComponent: {
      if (flags & Placement) {
        commitPlacement(finishedWork);
        finishedWork.flags &= ~Placement;
      }
      if (flags & Update) {
        commitUpdate(finishedWork);
      }
      break;
    }

    case HostText: {
      if (flags & Update) {
        const textInstance = finishedWork.stateNode;
        const newText = finishedWork.memoizedProps;
        commitTextUpdate(textInstance, newText);
      }
      break;
    }

    case FunctionComponent: {
      if (flags & Update) {
        // Run useInsertionEffect cleanup and setup
        commitHookEffectListUnmount(InsertionEffect, finishedWork);
        commitHookEffectListMount(InsertionEffect, finishedWork);
      }
      break;
    }

    // ... other cases
  }
}
```

### Placement (Inserting Nodes)

```javascript
function commitPlacement(finishedWork) {
  // Find the parent DOM node
  const parentFiber = getHostParentFiber(finishedWork);
  let parent;
  let isContainer;

  switch (parentFiber.tag) {
    case HostComponent:
      parent = parentFiber.stateNode;
      isContainer = false;
      break;
    case HostRoot:
      parent = parentFiber.stateNode.containerInfo;
      isContainer = true;
      break;
    case HostPortal:
      parent = parentFiber.stateNode.containerInfo;
      isContainer = true;
      break;
  }

  // Find the sibling to insert before
  const before = getHostSibling(finishedWork);

  if (isContainer) {
    insertOrAppendPlacementNodeIntoContainer(finishedWork, before, parent);
  } else {
    insertOrAppendPlacementNode(finishedWork, before, parent);
  }
}

function insertOrAppendPlacementNode(node, before, parent) {
  const tag = node.tag;

  if (tag === HostComponent || tag === HostText) {
    const stateNode = node.stateNode;
    if (before) {
      parent.insertBefore(stateNode, before);
    } else {
      parent.appendChild(stateNode);
    }
  } else {
    // For components, insert their children
    const child = node.child;
    if (child !== null) {
      insertOrAppendPlacementNode(child, before, parent);
      let sibling = child.sibling;
      while (sibling !== null) {
        insertOrAppendPlacementNode(sibling, before, parent);
        sibling = sibling.sibling;
      }
    }
  }
}
```

### Update (Modifying Nodes)

```javascript
function commitUpdate(finishedWork) {
  const instance = finishedWork.stateNode;
  const newProps = finishedWork.memoizedProps;
  const oldProps = finishedWork.alternate.memoizedProps;
  const type = finishedWork.type;

  // Calculate the diff
  const updatePayload = prepareUpdate(instance, type, oldProps, newProps);

  if (updatePayload !== null) {
    commitUpdateProperties(instance, updatePayload, type, oldProps, newProps);
  }
}

function commitUpdateProperties(domElement, updatePayload, type, oldProps, newProps) {
  // Update DOM properties
  for (let i = 0; i < updatePayload.length; i += 2) {
    const propKey = updatePayload[i];
    const propValue = updatePayload[i + 1];

    if (propKey === 'style') {
      setValueForStyles(domElement, propValue);
    } else if (propKey === 'children') {
      setTextContent(domElement, propValue);
    } else {
      setValueForProperty(domElement, propKey, propValue);
    }
  }
}
```

### Deletion (Removing Nodes)

```javascript
function commitDeletionEffects(root, returnFiber, deletedFiber) {
  // Recursively traverse and run cleanup
  commitDeletionEffectsOnFiber(root, returnFiber, deletedFiber);

  // Remove from DOM
  detachFiberFromParent(deletedFiber);
}

function commitDeletionEffectsOnFiber(root, nearestMountedAncestor, deletedFiber) {
  switch (deletedFiber.tag) {
    case HostComponent: {
      // Unmount refs
      safelyDetachRef(deletedFiber, nearestMountedAncestor);

      // Recursively delete children
      recursivelyTraverseDeletionEffects(root, nearestMountedAncestor, deletedFiber);

      // Remove from DOM
      removeChild(deletedFiber.stateNode);
      break;
    }

    case FunctionComponent: {
      // Run useEffect cleanup functions
      commitHookEffectListUnmount(PassiveEffect | HasEffect, deletedFiber);
      // Run useLayoutEffect cleanup
      commitHookEffectListUnmount(LayoutEffect | HasEffect, deletedFiber);

      recursivelyTraverseDeletionEffects(root, nearestMountedAncestor, deletedFiber);
      break;
    }

    case ClassComponent: {
      safelyDetachRef(deletedFiber, nearestMountedAncestor);

      const instance = deletedFiber.stateNode;
      if (typeof instance.componentWillUnmount === 'function') {
        safelyCallComponentWillUnmount(
          deletedFiber,
          nearestMountedAncestor,
          instance
        );
      }

      recursivelyTraverseDeletionEffects(root, nearestMountedAncestor, deletedFiber);
      break;
    }
  }
}
```

## Layout Phase

### Purpose

This phase runs **after** DOM mutations but **before** the browser paints. It's used for:
- `componentDidMount` / `componentDidUpdate`
- `useLayoutEffect`
- Ref attachment

```javascript
function commitLayoutEffects(finishedWork, root, committedLanes) {
  nextEffect = finishedWork;
  commitLayoutEffects_begin(finishedWork, root, committedLanes);
}

function commitLayoutEffects_begin(subtreeRoot, root, committedLanes) {
  while (nextEffect !== null) {
    const fiber = nextEffect;
    const firstChild = fiber.child;

    if ((fiber.subtreeFlags & LayoutMask) !== NoFlags && firstChild !== null) {
      firstChild.return = fiber;
      nextEffect = firstChild;
    } else {
      commitLayoutMountEffects_complete(subtreeRoot, root, committedLanes);
    }
  }
}

function commitLayoutEffectsOnFiber(finishedWork, root, committedLanes) {
  const flags = finishedWork.flags;

  switch (finishedWork.tag) {
    case FunctionComponent: {
      if (flags & LayoutEffect) {
        // Run useLayoutEffect setup
        commitHookEffectListMount(LayoutEffect | HasEffect, finishedWork);
      }
      break;
    }

    case ClassComponent: {
      const instance = finishedWork.stateNode;

      if (flags & Update) {
        if (finishedWork.alternate === null) {
          // Mount
          instance.componentDidMount();
        } else {
          // Update
          const prevProps = finishedWork.alternate.memoizedProps;
          const prevState = finishedWork.alternate.memoizedState;
          const snapshot = instance.__reactInternalSnapshotBeforeUpdate;
          instance.componentDidUpdate(prevProps, prevState, snapshot);
        }
      }
      break;
    }

    case HostComponent: {
      // Focus management, etc.
      if (flags & Update) {
        commitMount(finishedWork, finishedWork.stateNode);
      }
      break;
    }
  }

  // Attach refs
  if (flags & Ref) {
    commitAttachRef(finishedWork);
  }
}
```

### Ref Attachment

```javascript
function commitAttachRef(finishedWork) {
  const ref = finishedWork.ref;

  if (ref !== null) {
    const instance = finishedWork.stateNode;

    if (typeof ref === 'function') {
      ref(instance);
    } else {
      ref.current = instance;
    }
  }
}
```

## Passive Effects (useEffect)

### Scheduling

```javascript
// Passive effects are scheduled to run after paint
function commitPassiveMountEffects(root, finishedWork, committedLanes) {
  nextEffect = finishedWork;
  commitPassiveMountEffects_begin(finishedWork, root, committedLanes);
}

function flushPassiveEffects() {
  if (rootWithPendingPassiveEffects !== null) {
    const root = rootWithPendingPassiveEffects;

    // Run all cleanup effects first
    commitPassiveUnmountEffects(root.current);

    // Then run all setup effects
    commitPassiveMountEffects(root, root.current, lanes);

    rootWithPendingPassiveEffects = null;
  }
}
```

### Hook Effects

```javascript
function commitHookEffectListMount(flags, finishedWork) {
  const updateQueue = finishedWork.updateQueue;
  const lastEffect = updateQueue !== null ? updateQueue.lastEffect : null;

  if (lastEffect !== null) {
    const firstEffect = lastEffect.next;
    let effect = firstEffect;

    do {
      if ((effect.tag & flags) === flags) {
        // Run the effect
        const create = effect.create;
        effect.destroy = create();
      }
      effect = effect.next;
    } while (effect !== firstEffect);
  }
}

function commitHookEffectListUnmount(flags, finishedWork) {
  const updateQueue = finishedWork.updateQueue;
  const lastEffect = updateQueue !== null ? updateQueue.lastEffect : null;

  if (lastEffect !== null) {
    const firstEffect = lastEffect.next;
    let effect = firstEffect;

    do {
      if ((effect.tag & flags) === flags) {
        // Run the cleanup
        const destroy = effect.destroy;
        if (destroy !== undefined) {
          destroy();
        }
      }
      effect = effect.next;
    } while (effect !== firstEffect);
  }
}
```

## Effect Lifecycle

### Order of Operations

```
┌─────────────────────────────────────────────────────────────────┐
│                    Effect Execution Order                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  UNMOUNT (cleanup from previous render):                        │
│  1. useInsertionEffect cleanup                                  │
│  2. useLayoutEffect cleanup                                     │
│  3. useEffect cleanup (async, after paint)                     │
│                                                                 │
│  MOUNT (setup for current render):                              │
│  1. useInsertionEffect setup (mutation phase)                  │
│  2. DOM mutations applied                                       │
│  3. useLayoutEffect setup (before paint)                       │
│  4. Browser paints                                              │
│  5. useEffect setup (async, after paint)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Example Flow

```jsx
function Example({ id }) {
  useEffect(() => {
    console.log('5. useEffect setup');
    return () => console.log('3. useEffect cleanup');
  });

  useLayoutEffect(() => {
    console.log('4. useLayoutEffect setup');
    return () => console.log('2. useLayoutEffect cleanup');
  });

  useInsertionEffect(() => {
    console.log('1. useInsertionEffect setup');
    return () => console.log('0. useInsertionEffect cleanup');
  });

  return <div id={id}>Hello</div>;
}

// When id changes from "a" to "b":
// 0. useInsertionEffect cleanup (from "a")
// 1. useInsertionEffect setup (for "b")
// [DOM mutation: id="b"]
// 2. useLayoutEffect cleanup (from "a")
// 4. useLayoutEffect setup (for "b")
// [Browser paints]
// 3. useEffect cleanup (from "a")
// 5. useEffect setup (for "b")
```

## Tree Swapping

### Current ↔ Work-in-Progress

```javascript
// After mutation phase, trees are swapped
root.current = finishedWork;

// Before swap:
//   root.current → old tree (displayed)
//   finishedWork → new tree (ready)
//
// After swap:
//   root.current → new tree (now displayed)
//   old tree → becomes work-in-progress for next update
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tree Swap                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   BEFORE COMMIT                    AFTER COMMIT                 │
│                                                                 │
│   root.current ──▶ Tree A          root.current ──▶ Tree B     │
│                    (displayed)                      (displayed) │
│                                                                 │
│   finishedWork ──▶ Tree B                                       │
│                    (work-in-progress)                           │
│                                                                 │
│   Next update: Tree A becomes the new work-in-progress         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Error Handling

### Error Boundaries in Commit

```javascript
function safelyCallComponentWillUnmount(current, nearestMountedAncestor, instance) {
  try {
    instance.componentWillUnmount();
  } catch (error) {
    captureCommitPhaseError(current, nearestMountedAncestor, error);
  }
}

function captureCommitPhaseError(sourceFiber, nearestMountedAncestor, error) {
  // Find the nearest error boundary
  let fiber = nearestMountedAncestor;

  while (fiber !== null) {
    if (fiber.tag === ClassComponent) {
      const instance = fiber.stateNode;
      if (typeof instance.componentDidCatch === 'function') {
        // Schedule error recovery
        const errorInfo = { componentStack: getStackByFiberInDevAndProd(sourceFiber) };
        queueUpdate(fiber, createClassErrorUpdate(fiber, error, errorInfo));
        return;
      }
    }
    fiber = fiber.return;
  }

  // No error boundary found - fatal error
  throw error;
}
```

## Summary

In this chapter, you've learned:

- **Three Sub-Phases**: Before Mutation, Mutation, Layout
- **DOM Operations**: Placement, Update, Deletion
- **Effect Order**: useInsertionEffect → Mutation → useLayoutEffect → Paint → useEffect
- **Tree Swapping**: How current and work-in-progress trees exchange
- **Error Handling**: How errors during commit are caught

## Key Takeaways

1. **Synchronous**: Commit phase cannot be interrupted
2. **Ordered**: Effects run in specific, predictable order
3. **Cleanup first**: Cleanup runs before new effects
4. **useLayoutEffect**: Runs synchronously before paint
5. **useEffect**: Runs asynchronously after paint

## Next Steps

Now that you understand how changes are committed, let's explore how React schedules and prioritizes work in Chapter 5: Scheduling and Lanes.

---

**Ready for Chapter 5?** [Scheduling and Lanes](05-scheduling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
