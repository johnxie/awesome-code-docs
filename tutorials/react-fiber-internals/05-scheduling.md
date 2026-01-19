---
layout: default
title: "Chapter 5: Scheduling and Lanes"
parent: "React Fiber Internals"
nav_order: 5
---

# Chapter 5: Scheduling and Lanes

> Understanding React's priority system, the Scheduler, and how lanes enable concurrent rendering.

## Overview

React's Scheduler and Lane system work together to prioritize updates and enable concurrent rendering. Lanes replaced the older "expiration time" system and provide more granular control over update priorities.

## The Scheduler

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Scheduler Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────┐      ┌─────────────────────────────────┐  │
│   │  React Updates  │      │         Scheduler                │  │
│   │  (setState,     │─────▶│  ┌──────────────────────────┐   │  │
│   │   dispatch)     │      │  │   Priority Queues        │   │  │
│   └─────────────────┘      │  │                          │   │  │
│                            │  │  Immediate  ■■■          │   │  │
│   ┌─────────────────┐      │  │  UserBlock  ■■■■         │   │  │
│   │  Browser APIs   │      │  │  Normal     ■■■■■■       │   │  │
│   │  (setTimeout,   │◀────▶│  │  Low        ■■           │   │  │
│   │   requestIdle)  │      │  │  Idle       ■            │   │  │
│   └─────────────────┘      │  └──────────────────────────┘   │  │
│                            │              │                   │  │
│   ┌─────────────────┐      │              ▼                   │  │
│   │    Browser      │      │  ┌──────────────────────────┐   │  │
│   │   Event Loop    │◀─────│  │   Work Loop              │   │  │
│   │                 │      │  │   (time-sliced)          │   │  │
│   └─────────────────┘      │  └──────────────────────────┘   │  │
│                            └─────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Scheduler Priority Levels

```javascript
// Scheduler priority levels (from scheduler package)
const ImmediatePriority = 1;    // Sync, must happen now
const UserBlockingPriority = 2; // User interactions (click, input)
const NormalPriority = 3;       // Default (setState from effects)
const LowPriority = 4;          // Data fetching, background work
const IdlePriority = 5;         // Deferred, low-importance work

// Timeout for each priority (when it expires)
const IMMEDIATE_PRIORITY_TIMEOUT = -1;          // Never yields
const USER_BLOCKING_PRIORITY_TIMEOUT = 250;     // 250ms
const NORMAL_PRIORITY_TIMEOUT = 5000;           // 5s
const LOW_PRIORITY_TIMEOUT = 10000;             // 10s
const IDLE_PRIORITY_TIMEOUT = maxSigned31BitInt; // Never expires
```

### Scheduling Work

```javascript
// React schedules work using the Scheduler
import {
  scheduleCallback,
  cancelCallback,
  shouldYield,
} from 'scheduler';

function ensureRootIsScheduled(root) {
  const existingCallbackPriority = root.callbackPriority;
  const newCallbackPriority = getHighestPriorityLane(root.pendingLanes);

  if (existingCallbackPriority === newCallbackPriority) {
    // Already scheduled at this priority
    return;
  }

  // Cancel existing lower-priority callback
  if (existingCallbackPriority !== NoLane) {
    cancelCallback(root.callbackNode);
  }

  let schedulerPriorityLevel;
  if (newCallbackPriority === SyncLane) {
    // Sync work - flush immediately
    scheduleSyncCallback(performSyncWorkOnRoot.bind(null, root));
    schedulerPriorityLevel = ImmediatePriority;
  } else {
    // Concurrent work
    schedulerPriorityLevel = lanesToSchedulerPriority(newCallbackPriority);
  }

  const newCallbackNode = scheduleCallback(
    schedulerPriorityLevel,
    performConcurrentWorkOnRoot.bind(null, root)
  );

  root.callbackNode = newCallbackNode;
  root.callbackPriority = newCallbackPriority;
}
```

### Time Slicing

```javascript
// The scheduler yields to the browser periodically
function workLoopConcurrent() {
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}

// shouldYield checks if we've used our time slice
function shouldYield() {
  const currentTime = getCurrentTime();
  return currentTime >= deadline;
}

// Time slices are typically 5ms
function requestHostCallback(callback) {
  scheduledHostCallback = callback;

  if (!isMessageLoopRunning) {
    isMessageLoopRunning = true;
    schedulePerformWorkUntilDeadline();
  }
}

function performWorkUntilDeadline() {
  if (scheduledHostCallback !== null) {
    const currentTime = getCurrentTime();
    // Set deadline for this time slice (5ms)
    deadline = currentTime + yieldInterval;

    const hasMoreWork = scheduledHostCallback(true, currentTime);

    if (!hasMoreWork) {
      isMessageLoopRunning = false;
      scheduledHostCallback = null;
    } else {
      // More work - schedule another time slice
      schedulePerformWorkUntilDeadline();
    }
  }
}
```

## Lanes

### What Are Lanes?

```javascript
// Lanes are bit flags representing update priorities
// Each bit position represents a different priority level

//                            31 bits
//                            ▼
const TotalLanes = 31;

// Lane definitions (bit positions)
const NoLane =                   0b0000000000000000000000000000000;
const SyncLane =                 0b0000000000000000000000000000001;
const InputContinuousLane =      0b0000000000000000000000000000100;
const DefaultLane =              0b0000000000000000000000000010000;
const TransitionLane1 =          0b0000000000000000000001000000000;
const TransitionLane2 =          0b0000000000000000000010000000000;
// ... more transition lanes
const IdleLane =                 0b0100000000000000000000000000000;
const OffscreenLane =            0b1000000000000000000000000000000;
```

### Lane Groups

```
┌─────────────────────────────────────────────────────────────────┐
│                    Lane Priority Levels                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Highest Priority                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  SyncLane (bit 0)                                        │    │
│  │  - Discrete events: click, keydown                       │    │
│  │  - Legacy sync mode                                      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  InputContinuousLane (bits 2-3)                         │    │
│  │  - Continuous events: mousemove, scroll                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  DefaultLane (bits 4-5)                                  │    │
│  │  - Normal setState, useEffect updates                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  TransitionLanes (bits 6-21)                            │    │
│  │  - startTransition updates                               │    │
│  │  - Can be interrupted by higher priority                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  IdleLane / OffscreenLane (bits 29-30)                  │    │
│  │  - Background work, prerendering                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│  Lowest Priority                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Lane Operations

```javascript
// Bitwise operations for lane manipulation

// Merge lanes (combine priorities)
function mergeLanes(a, b) {
  return a | b;
}

// Check if lanes include a specific lane
function includesSomeLane(set, subset) {
  return (set & subset) !== NoLanes;
}

// Get highest priority lane
function getHighestPriorityLane(lanes) {
  return lanes & -lanes; // Isolates rightmost bit
}

// Remove a lane from set
function removeLanes(set, subset) {
  return set & ~subset;
}

// Check if lane is subset
function isSubsetOfLanes(set, subset) {
  return (set & subset) === subset;
}

// Example usage:
const pendingLanes = SyncLane | DefaultLane | TransitionLane1;
// Binary: 0b0000000000000000000001000010001

getHighestPriorityLane(pendingLanes); // Returns SyncLane (0b1)
includeSomeLane(pendingLanes, TransitionLanes); // Returns true
```

### Request Update Lane

```javascript
// Determine which lane an update should use
function requestUpdateLane(fiber) {
  const mode = fiber.mode;

  // Legacy mode - always sync
  if ((mode & ConcurrentMode) === NoMode) {
    return SyncLane;
  }

  // Inside a transition
  if (currentUpdateLanePriority !== NoLane) {
    return currentUpdateLanePriority;
  }

  // Get lane from current event priority
  const eventLane = getCurrentEventPriority();

  if (eventLane !== NoLane) {
    return eventLane;
  }

  // Default lane
  return DefaultLane;
}

// Event priority mapping
function getCurrentEventPriority() {
  const currentEvent = window.event;

  if (currentEvent === undefined) {
    return DefaultLane;
  }

  // Discrete events (click, keydown)
  if (isDiscreteEventType(currentEvent.type)) {
    return SyncLane;
  }

  // Continuous events (mousemove, scroll)
  if (isContinuousEventType(currentEvent.type)) {
    return InputContinuousLane;
  }

  return DefaultLane;
}
```

## Transitions

### startTransition

```javascript
// Mark updates as low-priority transitions
function startTransition(scope) {
  const prevTransition = ReactCurrentBatchConfig.transition;
  ReactCurrentBatchConfig.transition = {};

  try {
    // Updates inside scope get TransitionLane
    scope();
  } finally {
    ReactCurrentBatchConfig.transition = prevTransition;
  }
}

// Usage:
function handleSearch(query) {
  // High priority - update input immediately
  setInputValue(query);

  // Low priority - can be interrupted
  startTransition(() => {
    setSearchResults(filterResults(query));
  });
}
```

### Transition Lane Selection

```javascript
// React uses multiple transition lanes to batch related updates
function claimNextTransitionLane() {
  const lane = nextTransitionLane;

  // Cycle through transition lanes
  nextTransitionLane <<= 1;
  if ((nextTransitionLane & TransitionLanes) === NoLanes) {
    nextTransitionLane = TransitionLane1;
  }

  return lane;
}

// This allows multiple independent transitions to render separately
// Each startTransition call gets its own lane
```

## Batching Updates

### Automatic Batching

```javascript
// React 18 automatically batches all updates
function dispatchSetState(fiber, queue, action) {
  const lane = requestUpdateLane(fiber);

  const update = {
    lane,
    action,
    hasEagerState: false,
    eagerState: null,
    next: null,
  };

  // Enqueue the update
  enqueueUpdate(fiber, queue, update, lane);

  // Schedule work
  const root = scheduleUpdateOnFiber(fiber, lane);

  if (root !== null) {
    entangleTransitionUpdate(root, queue, lane);
  }
}

// Multiple setState calls in same event = batched
function handleClick() {
  setCount(1);    // Batched
  setFlag(true);  // Batched
  setText('hi');  // Batched
  // Only one re-render!
}

// Even in async code (React 18):
setTimeout(() => {
  setCount(1);    // Batched
  setFlag(true);  // Batched
  // Still only one re-render!
}, 1000);
```

### flushSync

```javascript
// Force synchronous flush
import { flushSync } from 'react-dom';

function handleClick() {
  flushSync(() => {
    setCount(c => c + 1);
  });
  // DOM is updated here

  flushSync(() => {
    setFlag(true);
  });
  // DOM is updated again here

  // Two separate re-renders
}
```

## Entanglement

### Lane Entanglement

```javascript
// Some lanes must be rendered together
function entangleTransitionUpdate(root, queue, lane) {
  if (isTransitionLane(lane)) {
    let queueLanes = queue.lanes;

    // Include previous transition lanes
    queueLanes = intersectLanes(queueLanes, root.pendingLanes);

    const newQueueLanes = mergeLanes(queueLanes, lane);
    queue.lanes = newQueueLanes;

    // Entangle in root
    markRootEntangled(root, newQueueLanes);
  }
}

// Entangled lanes are rendered together to maintain consistency
const entangledLanes = root.entangledLanes;
if (entangledLanes !== NoLanes) {
  const entanglements = root.entanglements;
  let lanes = pendingLanes & entangledLanes;

  while (lanes > 0) {
    const index = pickArbitraryLaneIndex(lanes);
    const lane = 1 << index;

    // Include all entangled lanes
    pendingLanes |= entanglements[index];
    lanes &= ~lane;
  }
}
```

## Priority Inversion

### Handling Starvation

```javascript
// Lower priority work can starve if high-priority updates keep coming
// React prevents this by marking lanes as "expired"

function markStarvedLanesAsExpired(root, currentTime) {
  const pendingLanes = root.pendingLanes;
  const expirationTimes = root.expirationTimes;

  let lanes = pendingLanes;
  while (lanes > 0) {
    const index = pickArbitraryLaneIndex(lanes);
    const lane = 1 << index;
    const expirationTime = expirationTimes[index];

    if (expirationTime === NoTimestamp) {
      // Assign expiration time
      if ((lane & (pendingLanes & ~suspendedLanes)) !== NoLanes) {
        expirationTimes[index] = computeExpirationTime(lane, currentTime);
      }
    } else if (expirationTime <= currentTime) {
      // Lane has expired - mark as needing immediate attention
      root.expiredLanes |= lane;
    }

    lanes &= ~lane;
  }
}

// Expired lanes get SyncLane treatment
function getNextLanes(root, wipLanes) {
  const pendingLanes = root.pendingLanes;

  if (pendingLanes === NoLanes) {
    return NoLanes;
  }

  // Include expired lanes with highest priority
  const expiredLanes = root.expiredLanes;
  if (expiredLanes !== NoLanes) {
    return expiredLanes;
  }

  // Normal priority selection...
}
```

## Suspense and Lanes

### Suspended Lanes

```javascript
// When Suspense boundaries suspend, their lanes are tracked
function markRootSuspended(root, suspendedLanes) {
  root.suspendedLanes |= suspendedLanes;
  root.pingedLanes &= ~suspendedLanes;

  // Clear expiration times for suspended lanes
  const expirationTimes = root.expirationTimes;
  let lanes = suspendedLanes;
  while (lanes > 0) {
    const index = pickArbitraryLaneIndex(lanes);
    const lane = 1 << index;
    expirationTimes[index] = NoTimestamp;
    lanes &= ~lane;
  }
}

// When data resolves, ping the suspended lane
function pingSuspendedRoot(root, suspendedLane) {
  const pingedLanes = root.pingedLanes |= suspendedLane;

  // Schedule work if we're not already rendering
  if (workInProgressRoot !== root) {
    ensureRootIsScheduled(root);
  }
}
```

## Visualization

### Lane State Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Lane State Transitions                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    setState()     ┌──────────┐                  │
│   │  NoLane  │──────────────────▶│ Pending  │                  │
│   └──────────┘                   └────┬─────┘                  │
│        ▲                              │                         │
│        │                              │ render started          │
│        │                              ▼                         │
│        │                        ┌──────────┐    suspends       │
│        │                        │ Rendering │──────────┐       │
│        │                        └────┬─────┘           │       │
│        │                             │                 ▼       │
│        │                             │ commit    ┌──────────┐  │
│   committed                          │           │Suspended │  │
│        │                             │           └────┬─────┘  │
│        │                             ▼                │ ping   │
│        │                        ┌──────────┐          │        │
│        └────────────────────────│ Finished │◀─────────┘        │
│                                 └──────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

In this chapter, you've learned:

- **Scheduler**: How React yields to the browser with time slicing
- **Priority Levels**: Five scheduler priorities and their timeouts
- **Lanes**: Bit-based priority system for updates
- **Transitions**: Low-priority updates with startTransition
- **Batching**: Automatic batching of updates
- **Entanglement**: How related lanes render together

## Key Takeaways

1. **Time slicing**: Work is split into 5ms chunks
2. **Lanes replace expiration**: More granular priority control
3. **Transitions are interruptible**: Higher priority wins
4. **Batching is automatic**: Multiple updates = one render
5. **Starvation prevention**: Expired lanes get boosted

## Next Steps

Now that you understand scheduling and lanes, let's explore how hooks work internally in Chapter 6: Hooks Implementation.

---

**Ready for Chapter 6?** [Hooks Implementation](06-hooks.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
