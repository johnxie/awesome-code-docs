---
layout: default
title: "Chapter 3: Render Phase"
parent: "React Fiber Internals"
nav_order: 3
---

# Chapter 3: Render Phase

> Understanding how React builds the work-in-progress tree through beginWork and completeWork.

## Overview

The Render Phase is where React traverses the fiber tree, determines what changes need to be made, and builds the work-in-progress tree. This phase is interruptible and can be paused, aborted, or restarted by the scheduler.

## Render Phase Flow

### High-Level Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Render Phase Flow                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐                                               │
│   │   Update    │  setState, props change, context change       │
│   │  Triggered  │                                               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────┐                                               │
│   │ Schedule    │  Mark lanes, schedule callback                │
│   │   Work      │                                               │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────────────────────────────────────────────┐       │
│   │              Work Loop (Interruptible)               │       │
│   │  ┌─────────────┐    ┌─────────────────────────────┐ │       │
│   │  │ beginWork   │───▶│ Process fiber, create       │ │       │
│   │  │             │    │ children, reconcile         │ │       │
│   │  └─────────────┘    └─────────────────────────────┘ │       │
│   │         │                                           │       │
│   │         ▼                                           │       │
│   │  ┌─────────────┐    ┌─────────────────────────────┐ │       │
│   │  │completeWork │───▶│ Create DOM nodes,           │ │       │
│   │  │             │    │ bubble effects              │ │       │
│   │  └─────────────┘    └─────────────────────────────┘ │       │
│   └─────────────────────────────────────────────────────┘       │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────┐                                               │
│   │   Commit    │  Apply changes to DOM                         │
│   │   Phase     │                                               │
│   └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## The Work Loop

### performUnitOfWork

```javascript
// The core work loop processes one fiber at a time
function workLoopConcurrent() {
  // Check if we should yield to the browser
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}

function workLoopSync() {
  // Sync work doesn't yield
  while (workInProgress !== null) {
    performUnitOfWork(workInProgress);
  }
}

function performUnitOfWork(unitOfWork) {
  // The current fiber (already committed)
  const current = unitOfWork.alternate;

  // Phase 1: Begin work on this fiber
  // Returns the first child, or null if no children
  let next = beginWork(current, unitOfWork, renderLanes);

  // Memoize the props after processing
  unitOfWork.memoizedProps = unitOfWork.pendingProps;

  if (next === null) {
    // No children - complete this unit of work
    completeUnitOfWork(unitOfWork);
  } else {
    // Process the child next
    workInProgress = next;
  }
}
```

### completeUnitOfWork

```javascript
function completeUnitOfWork(unitOfWork) {
  let completedWork = unitOfWork;

  do {
    const current = completedWork.alternate;
    const returnFiber = completedWork.return;

    // Phase 2: Complete work on this fiber
    completeWork(current, completedWork, renderLanes);

    // Move to sibling if exists
    const siblingFiber = completedWork.sibling;
    if (siblingFiber !== null) {
      workInProgress = siblingFiber;
      return;
    }

    // No sibling - complete parent
    completedWork = returnFiber;
    workInProgress = completedWork;
  } while (completedWork !== null);
}
```

## beginWork

### Overview

```javascript
// beginWork is called for each fiber going DOWN the tree
function beginWork(current, workInProgress, renderLanes) {
  // Check if we can bail out (skip re-rendering)
  if (current !== null) {
    const oldProps = current.memoizedProps;
    const newProps = workInProgress.pendingProps;

    if (oldProps === newProps && !hasContextChanged()) {
      // Props haven't changed - check if there's pending work
      if (!includesSomeLane(renderLanes, updateLanes)) {
        // No pending updates - bail out
        return bailoutOnAlreadyFinishedWork(current, workInProgress, renderLanes);
      }
    }
  }

  // Process based on fiber type
  switch (workInProgress.tag) {
    case FunctionComponent:
      return updateFunctionComponent(current, workInProgress, renderLanes);
    case ClassComponent:
      return updateClassComponent(current, workInProgress, renderLanes);
    case HostRoot:
      return updateHostRoot(current, workInProgress, renderLanes);
    case HostComponent:
      return updateHostComponent(current, workInProgress, renderLanes);
    case HostText:
      return updateHostText(current, workInProgress);
    case SuspenseComponent:
      return updateSuspenseComponent(current, workInProgress, renderLanes);
    // ... other cases
  }
}
```

### Function Component Processing

```javascript
function updateFunctionComponent(current, workInProgress, renderLanes) {
  const Component = workInProgress.type;
  const props = workInProgress.pendingProps;

  // Render the function component
  // This is where hooks are executed
  let nextChildren = renderWithHooks(
    current,
    workInProgress,
    Component,
    props,
    renderLanes
  );

  // Check if we can bail out
  if (current !== null && !didReceiveUpdate) {
    // Hooks didn't change - bail out
    bailoutHooks(current, workInProgress, renderLanes);
    return bailoutOnAlreadyFinishedWork(current, workInProgress, renderLanes);
  }

  // Reconcile children (create child fibers)
  reconcileChildren(current, workInProgress, nextChildren, renderLanes);

  return workInProgress.child;
}

function renderWithHooks(current, workInProgress, Component, props, lanes) {
  // Set up hooks dispatcher
  ReactCurrentDispatcher.current =
    current === null
      ? HooksDispatcherOnMount  // First render
      : HooksDispatcherOnUpdate; // Re-render

  // Call the component function
  let children = Component(props);

  // Reset hooks state
  ReactCurrentDispatcher.current = ContextOnlyDispatcher;

  return children;
}
```

### Class Component Processing

```javascript
function updateClassComponent(current, workInProgress, renderLanes) {
  const instance = workInProgress.stateNode;

  if (instance === null) {
    // Mount: Create the instance
    constructClassInstance(workInProgress, Component, props);
    mountClassInstance(workInProgress, Component, props, renderLanes);
  } else if (current === null) {
    // Resume: Instance exists but never committed
    resumeMountClassInstance(workInProgress, Component, props, renderLanes);
  } else {
    // Update: Re-rendering
    shouldUpdate = updateClassInstance(
      current,
      workInProgress,
      Component,
      props,
      renderLanes
    );
  }

  // Render and reconcile children
  return finishClassComponent(current, workInProgress, shouldUpdate, renderLanes);
}

function finishClassComponent(current, workInProgress, shouldUpdate, renderLanes) {
  if (!shouldUpdate) {
    // shouldComponentUpdate returned false
    return bailoutOnAlreadyFinishedWork(current, workInProgress, renderLanes);
  }

  const instance = workInProgress.stateNode;

  // Call render method
  const nextChildren = instance.render();

  // Reconcile children
  reconcileChildren(current, workInProgress, nextChildren, renderLanes);

  return workInProgress.child;
}
```

### Host Component Processing

```javascript
function updateHostComponent(current, workInProgress, renderLanes) {
  const type = workInProgress.type;
  const nextProps = workInProgress.pendingProps;
  const prevProps = current !== null ? current.memoizedProps : null;

  let nextChildren = nextProps.children;

  // Check if children is just text
  const isDirectTextChild = shouldSetTextContent(type, nextProps);

  if (isDirectTextChild) {
    // Optimization: Don't create a separate text fiber
    nextChildren = null;
  }

  // Reconcile children
  reconcileChildren(current, workInProgress, nextChildren, renderLanes);

  return workInProgress.child;
}
```

## Reconciliation

### reconcileChildren

```javascript
function reconcileChildren(current, workInProgress, nextChildren, renderLanes) {
  if (current === null) {
    // Mount: No existing children
    workInProgress.child = mountChildFibers(
      workInProgress,
      null,
      nextChildren,
      renderLanes
    );
  } else {
    // Update: Diff with existing children
    workInProgress.child = reconcileChildFibers(
      workInProgress,
      current.child,
      nextChildren,
      renderLanes
    );
  }
}
```

### Child Reconciliation Algorithm

```javascript
function reconcileChildFibers(returnFiber, currentFirstChild, newChild, lanes) {
  // Handle different child types
  if (typeof newChild === 'object' && newChild !== null) {
    switch (newChild.$$typeof) {
      case REACT_ELEMENT_TYPE:
        return reconcileSingleElement(
          returnFiber,
          currentFirstChild,
          newChild,
          lanes
        );
      case REACT_PORTAL_TYPE:
        return reconcileSinglePortal(/* ... */);
    }

    if (isArray(newChild)) {
      return reconcileChildrenArray(
        returnFiber,
        currentFirstChild,
        newChild,
        lanes
      );
    }
  }

  if (typeof newChild === 'string' || typeof newChild === 'number') {
    return reconcileSingleTextNode(returnFiber, currentFirstChild, newChild, lanes);
  }

  // Empty children - delete all
  return deleteRemainingChildren(returnFiber, currentFirstChild);
}
```

### Single Element Reconciliation

```javascript
function reconcileSingleElement(returnFiber, currentFirstChild, element, lanes) {
  const key = element.key;
  let child = currentFirstChild;

  // Search for a matching fiber
  while (child !== null) {
    if (child.key === key) {
      // Key matches
      if (child.elementType === element.type) {
        // Type also matches - reuse fiber
        deleteRemainingChildren(returnFiber, child.sibling);
        const existing = useFiber(child, element.props);
        existing.return = returnFiber;
        return existing;
      }
      // Key matches but type doesn't - delete all
      deleteRemainingChildren(returnFiber, child);
      break;
    } else {
      // Key doesn't match - delete this child
      deleteChild(returnFiber, child);
    }
    child = child.sibling;
  }

  // No match found - create new fiber
  const created = createFiberFromElement(element, returnFiber.mode, lanes);
  created.return = returnFiber;
  return created;
}
```

### Array Reconciliation (Diffing)

```javascript
function reconcileChildrenArray(returnFiber, currentFirstChild, newChildren, lanes) {
  let resultingFirstChild = null;
  let previousNewFiber = null;
  let oldFiber = currentFirstChild;
  let lastPlacedIndex = 0;
  let newIdx = 0;

  // First pass: match by index
  for (; oldFiber !== null && newIdx < newChildren.length; newIdx++) {
    if (oldFiber.index > newIdx) {
      // Old fiber is ahead - there was a deletion
      break;
    }

    const newFiber = updateSlot(returnFiber, oldFiber, newChildren[newIdx], lanes);

    if (newFiber === null) {
      // Keys don't match - break to second pass
      break;
    }

    if (oldFiber && newFiber.alternate === null) {
      // Matched by index but not by key - delete old
      deleteChild(returnFiber, oldFiber);
    }

    lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);

    if (previousNewFiber === null) {
      resultingFirstChild = newFiber;
    } else {
      previousNewFiber.sibling = newFiber;
    }
    previousNewFiber = newFiber;
    oldFiber = oldFiber.sibling;
  }

  if (newIdx === newChildren.length) {
    // All new children processed - delete remaining old
    deleteRemainingChildren(returnFiber, oldFiber);
    return resultingFirstChild;
  }

  if (oldFiber === null) {
    // All old children processed - add remaining new
    for (; newIdx < newChildren.length; newIdx++) {
      const newFiber = createChild(returnFiber, newChildren[newIdx], lanes);
      if (newFiber === null) continue;

      lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);
      // Link siblings...
    }
    return resultingFirstChild;
  }

  // Second pass: Use map for remaining
  const existingChildren = mapRemainingChildren(returnFiber, oldFiber);

  for (; newIdx < newChildren.length; newIdx++) {
    const newFiber = updateFromMap(
      existingChildren,
      returnFiber,
      newIdx,
      newChildren[newIdx],
      lanes
    );

    if (newFiber !== null) {
      if (newFiber.alternate !== null) {
        // Reused - remove from map
        existingChildren.delete(newFiber.key ?? newIdx);
      }
      lastPlacedIndex = placeChild(newFiber, lastPlacedIndex, newIdx);
      // Link siblings...
    }
  }

  // Delete remaining unmatched
  existingChildren.forEach(child => deleteChild(returnFiber, child));

  return resultingFirstChild;
}
```

## completeWork

### Overview

```javascript
// completeWork is called for each fiber going UP the tree
function completeWork(current, workInProgress, renderLanes) {
  const newProps = workInProgress.pendingProps;

  switch (workInProgress.tag) {
    case FunctionComponent:
    case ClassComponent:
      // Components don't have DOM nodes
      bubbleProperties(workInProgress);
      return null;

    case HostRoot:
      // Root of the tree
      const fiberRoot = workInProgress.stateNode;
      // ... handle root completion
      bubbleProperties(workInProgress);
      return null;

    case HostComponent:
      return completeHostComponent(current, workInProgress, newProps);

    case HostText:
      return completeHostText(current, workInProgress, newProps);

    case SuspenseComponent:
      return completeSuspenseComponent(current, workInProgress);

    // ... other cases
  }
}
```

### Host Component Completion

```javascript
function completeHostComponent(current, workInProgress, newProps) {
  const type = workInProgress.type;

  if (current !== null && workInProgress.stateNode !== null) {
    // Update: Compare props and prepare update
    updateHostComponent(current, workInProgress, type, newProps);
  } else {
    // Mount: Create DOM node
    const instance = createInstance(type, newProps, workInProgress);

    // Append all children to this DOM node
    appendAllChildren(instance, workInProgress);

    // Store DOM reference
    workInProgress.stateNode = instance;

    // Initialize DOM properties
    finalizeInitialChildren(instance, type, newProps);
  }

  bubbleProperties(workInProgress);
  return null;
}

function appendAllChildren(parent, workInProgress) {
  let node = workInProgress.child;

  while (node !== null) {
    if (node.tag === HostComponent || node.tag === HostText) {
      // Direct DOM child - append
      appendInitialChild(parent, node.stateNode);
    } else if (node.child !== null) {
      // Component - look for DOM children
      node.child.return = node;
      node = node.child;
      continue;
    }

    if (node === workInProgress) {
      return;
    }

    // Move to sibling or parent's sibling
    while (node.sibling === null) {
      if (node.return === null || node.return === workInProgress) {
        return;
      }
      node = node.return;
    }
    node.sibling.return = node.return;
    node = node.sibling;
  }
}
```

### Bubbling Properties

```javascript
// Bubble child properties up to parent
function bubbleProperties(completedWork) {
  const didBailout = completedWork.alternate !== null &&
    completedWork.alternate.child === completedWork.child;

  let subtreeFlags = NoFlags;
  let newChildLanes = NoLanes;

  if (!didBailout) {
    // Accumulate flags from all children
    let child = completedWork.child;
    while (child !== null) {
      newChildLanes = mergeLanes(
        newChildLanes,
        mergeLanes(child.lanes, child.childLanes)
      );
      subtreeFlags |= child.subtreeFlags;
      subtreeFlags |= child.flags;
      child = child.sibling;
    }
  }

  completedWork.subtreeFlags = subtreeFlags;
  completedWork.childLanes = newChildLanes;
}
```

## Bailout Optimization

### When Can We Skip Work?

```javascript
function bailoutOnAlreadyFinishedWork(current, workInProgress, renderLanes) {
  // Check if children have pending work
  if (!includesSomeLane(renderLanes, workInProgress.childLanes)) {
    // No pending work in entire subtree - skip completely
    return null;
  }

  // Children have work but this fiber doesn't
  // Clone children and continue
  cloneChildFibers(current, workInProgress);
  return workInProgress.child;
}

function cloneChildFibers(current, workInProgress) {
  if (workInProgress.child === null) {
    return;
  }

  // Clone first child
  let currentChild = workInProgress.child;
  let newChild = createWorkInProgress(currentChild, currentChild.pendingProps);
  workInProgress.child = newChild;
  newChild.return = workInProgress;

  // Clone siblings
  while (currentChild.sibling !== null) {
    currentChild = currentChild.sibling;
    newChild = newChild.sibling = createWorkInProgress(
      currentChild,
      currentChild.pendingProps
    );
    newChild.return = workInProgress;
  }
}
```

## Effect Marking

### Flagging Side Effects

```javascript
// During reconciliation, effects are flagged
function markUpdate(workInProgress) {
  workInProgress.flags |= Update;
}

function markPlacement(fiber) {
  fiber.flags |= Placement;
}

function deleteChild(returnFiber, childToDelete) {
  // Add to deletions array
  const deletions = returnFiber.deletions;
  if (deletions === null) {
    returnFiber.deletions = [childToDelete];
    returnFiber.flags |= ChildDeletion;
  } else {
    deletions.push(childToDelete);
  }
}
```

## Visualizing Render Phase

### Example Traversal

```
Component Tree:                     Render Phase Order:

     App                           1. beginWork(App)
    /   \                          2. beginWork(Header)
Header   Main                      3. beginWork(h1)
  |       |                        4. completeWork(h1)
  h1     div                       5. completeWork(Header)
          |                        6. beginWork(Main)
       Content                     7. beginWork(div)
                                   8. beginWork(Content)
                                   9. completeWork(Content)
                                  10. completeWork(div)
                                  11. completeWork(Main)
                                  12. completeWork(App)

Work-in-Progress Tree Built:
├── App (WIP)
│   ├── Header (WIP, cloned)
│   │   └── h1 (WIP, cloned)
│   └── Main (WIP)
│       └── div (WIP)
│           └── Content (WIP, new)
```

## Summary

In this chapter, you've learned:

- **Work Loop**: How React processes fibers one at a time
- **beginWork**: Processes fiber going down, creates children
- **completeWork**: Completes fiber going up, creates DOM
- **Reconciliation**: Diffing algorithm for efficient updates
- **Bailout**: Optimization to skip unchanged subtrees
- **Effect Marking**: Flagging side effects for commit phase

## Key Takeaways

1. **Interruptible**: Render phase can be paused and resumed
2. **Two phases**: beginWork (down) and completeWork (up)
3. **Reconciliation**: Keys enable efficient list updates
4. **Bubbling**: Child flags bubble up for efficient commit
5. **Bailout**: Unchanged subtrees are skipped entirely

## Next Steps

Now that you understand how React builds the work-in-progress tree, let's explore how these changes are applied to the DOM in Chapter 4: Commit Phase.

---

**Ready for Chapter 4?** [Commit Phase](04-commit-phase.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
