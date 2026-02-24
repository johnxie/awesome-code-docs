---
layout: default
title: "Chapter 5: Task Planning"
parent: "SuperAGI Tutorial"
nav_order: 5
---

# Chapter 5: Task Planning

Welcome to **Chapter 5: Task Planning**. In this part of **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master advanced planning techniques for goal decomposition, execution strategies, and adaptive replanning.

## Overview

Effective task planning is essential for autonomous agents to handle complex, multi-step objectives. This chapter covers hierarchical planning, dependency management, execution strategies, and techniques for handling uncertainty and failure.

## Goal Decomposition

### Hierarchical Task Network

```python
class HierarchicalTaskNetwork:
    """Decompose goals into hierarchical task structures."""

    def __init__(self, llm):
        self.llm = llm
        self.primitive_tasks = set()  # Tasks that can be executed directly
        self.decomposition_rules = {}

    def decompose(self, goal: str, context: dict) -> dict:
        """Decompose a goal into a task hierarchy."""
        hierarchy = self._build_hierarchy(goal, context, depth=0)
        return {
            "goal": goal,
            "hierarchy": hierarchy,
            "execution_order": self._flatten_to_execution_order(hierarchy)
        }

    def _build_hierarchy(self, task: str, context: dict, depth: int) -> dict:
        """Recursively build task hierarchy."""
        if depth > 5 or self._is_primitive(task):
            return {"task": task, "type": "primitive", "subtasks": []}

        subtasks = self._get_subtasks(task, context)

        return {
            "task": task,
            "type": "compound",
            "subtasks": [
                self._build_hierarchy(st, context, depth + 1)
                for st in subtasks
            ]
        }

    def _get_subtasks(self, task: str, context: dict) -> list:
        """Get subtasks for a compound task."""
        prompt = f"""
        Decompose this task into 3-5 subtasks:

        Task: {task}
        Context: {context}

        Return a JSON array of subtask descriptions.
        Each subtask should be specific and actionable.
        """

        response = self.llm.generate(prompt)
        return self._parse_subtasks(response)

    def _is_primitive(self, task: str) -> bool:
        """Check if task is primitive (directly executable)."""
        # Check against known primitive tasks
        for primitive in self.primitive_tasks:
            if primitive.lower() in task.lower():
                return True

        # Use LLM to determine
        prompt = f"""
        Is this task primitive (can be done in one step with a single tool)?
        Task: {task}
        Answer only: YES or NO
        """
        response = self.llm.generate(prompt).strip().upper()
        return response == "YES"

    def _flatten_to_execution_order(self, hierarchy: dict) -> list:
        """Flatten hierarchy to execution order respecting dependencies."""
        if hierarchy["type"] == "primitive":
            return [hierarchy["task"]]

        order = []
        for subtask in hierarchy["subtasks"]:
            order.extend(self._flatten_to_execution_order(subtask))
        return order
```

### SMART Goal Framework

```python
class SMARTGoalPlanner:
    """Plan tasks using SMART criteria."""

    def __init__(self, llm):
        self.llm = llm

    def refine_goal(self, vague_goal: str) -> dict:
        """Refine a vague goal into SMART criteria."""
        prompt = f"""
        Convert this goal into SMART format:

        Goal: {vague_goal}

        Return as JSON:
        {{
            "specific": "What exactly needs to be accomplished?",
            "measurable": "How will success be measured?",
            "achievable": "Is this realistic? What resources are needed?",
            "relevant": "Why is this important?",
            "time_bound": "What is the deadline or timeframe?",
            "refined_goal": "The refined, SMART goal statement",
            "success_criteria": ["List of specific success criteria"]
        }}
        """

        response = self.llm.generate(prompt)
        return self._parse_smart(response)

    def create_action_plan(self, smart_goal: dict) -> dict:
        """Create action plan from SMART goal."""
        prompt = f"""
        Create an action plan for this SMART goal:

        Goal: {smart_goal['refined_goal']}
        Success Criteria: {smart_goal['success_criteria']}
        Timeframe: {smart_goal['time_bound']}

        Return as JSON:
        {{
            "phases": [
                {{
                    "name": "Phase name",
                    "objective": "What this phase accomplishes",
                    "tasks": ["Task 1", "Task 2"],
                    "deliverables": ["Deliverable 1"],
                    "estimated_duration": "Duration"
                }}
            ],
            "milestones": [
                {{
                    "name": "Milestone name",
                    "criteria": "Completion criteria",
                    "target_date": "Relative date"
                }}
            ],
            "risks": ["Potential risk 1", "Potential risk 2"]
        }}
        """

        response = self.llm.generate(prompt)
        return self._parse_action_plan(response)
```

## Dependency Management

### Task Dependency Graph

```python
from collections import defaultdict, deque

class DependencyGraph:
    """Manage task dependencies."""

    def __init__(self):
        self.tasks = {}  # task_id -> task_info
        self.dependencies = defaultdict(set)  # task_id -> set of dependency task_ids
        self.dependents = defaultdict(set)  # task_id -> set of dependent task_ids

    def add_task(self, task_id: str, task_info: dict):
        """Add a task to the graph."""
        self.tasks[task_id] = task_info

    def add_dependency(self, task_id: str, depends_on: str):
        """Add a dependency: task_id depends on depends_on."""
        self.dependencies[task_id].add(depends_on)
        self.dependents[depends_on].add(task_id)

    def get_execution_order(self) -> list:
        """Get topologically sorted execution order."""
        # Kahn's algorithm for topological sort
        in_degree = {task_id: len(deps) for task_id, deps in self.dependencies.items()}

        # Add tasks with no dependencies
        for task_id in self.tasks:
            if task_id not in in_degree:
                in_degree[task_id] = 0

        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []

        while queue:
            task = queue.popleft()
            order.append(task)

            for dependent in self.dependents[task]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(self.tasks):
            raise ValueError("Circular dependency detected")

        return order

    def get_parallel_groups(self) -> list:
        """Get groups of tasks that can be executed in parallel."""
        order = self.get_execution_order()
        groups = []
        completed = set()

        while len(completed) < len(self.tasks):
            # Find all tasks whose dependencies are complete
            ready = []
            for task_id in order:
                if task_id in completed:
                    continue
                if self.dependencies[task_id].issubset(completed):
                    ready.append(task_id)

            if not ready:
                break

            groups.append(ready)
            completed.update(ready)

        return groups

    def get_critical_path(self) -> list:
        """Find the critical path (longest dependency chain)."""
        def longest_path_from(task_id: str, memo: dict) -> tuple:
            if task_id in memo:
                return memo[task_id]

            dependents = self.dependents[task_id]
            if not dependents:
                memo[task_id] = (1, [task_id])
                return memo[task_id]

            max_length = 0
            max_path = []

            for dep in dependents:
                length, path = longest_path_from(dep, memo)
                if length > max_length:
                    max_length = length
                    max_path = path

            result = (max_length + 1, [task_id] + max_path)
            memo[task_id] = result
            return result

        memo = {}
        max_length = 0
        critical_path = []

        # Find roots (tasks with no dependencies)
        roots = [t for t in self.tasks if not self.dependencies[t]]

        for root in roots:
            length, path = longest_path_from(root, memo)
            if length > max_length:
                max_length = length
                critical_path = path

        return critical_path
```

### Resource Constraints

```python
class ResourceConstrainedPlanner:
    """Plan tasks considering resource constraints."""

    def __init__(self, available_resources: dict):
        self.resources = available_resources  # resource_type -> capacity

    def schedule_tasks(self, tasks: list, dependency_graph: DependencyGraph) -> list:
        """Schedule tasks respecting resource constraints."""
        schedule = []
        current_time = 0
        completed = set()
        resource_usage = {r: 0 for r in self.resources}

        while len(completed) < len(tasks):
            # Find ready tasks
            ready = self._get_ready_tasks(tasks, completed, dependency_graph)

            # Filter by resource availability
            schedulable = self._filter_by_resources(ready, resource_usage)

            if not schedulable:
                # Wait for resources to free up
                current_time = self._advance_time(schedule, current_time)
                self._release_completed_resources(schedule, current_time, resource_usage)
                continue

            # Schedule task
            task = self._select_task(schedulable)
            self._allocate_resources(task, resource_usage)

            schedule.append({
                "task": task,
                "start_time": current_time,
                "end_time": current_time + task.get("duration", 1)
            })

            completed.add(task["id"])

        return schedule

    def _get_ready_tasks(self, tasks, completed, graph) -> list:
        """Get tasks whose dependencies are satisfied."""
        return [
            t for t in tasks
            if t["id"] not in completed and
            graph.dependencies[t["id"]].issubset(completed)
        ]

    def _filter_by_resources(self, tasks, current_usage) -> list:
        """Filter tasks that fit within available resources."""
        schedulable = []
        for task in tasks:
            required = task.get("resources", {})
            can_schedule = all(
                current_usage.get(r, 0) + amt <= self.resources.get(r, 0)
                for r, amt in required.items()
            )
            if can_schedule:
                schedulable.append(task)
        return schedulable
```

## Execution Strategies

### Sequential Execution

```python
class SequentialExecutor:
    """Execute tasks sequentially."""

    def __init__(self, agent):
        self.agent = agent

    def execute(self, plan: list) -> dict:
        """Execute plan sequentially."""
        results = []
        context = {}

        for task in plan:
            result = self._execute_task(task, context)
            results.append(result)

            if result["status"] == "failed":
                return {
                    "status": "failed",
                    "completed": results[:-1],
                    "failed_task": task,
                    "error": result.get("error")
                }

            # Update context with result
            context[task["id"]] = result

        return {
            "status": "success",
            "results": results
        }

    def _execute_task(self, task: dict, context: dict) -> dict:
        """Execute a single task."""
        try:
            result = self.agent.execute_task(task, context=context)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
```

### Parallel Execution

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelExecutor:
    """Execute independent tasks in parallel."""

    def __init__(self, agent, max_workers: int = 5):
        self.agent = agent
        self.max_workers = max_workers

    async def execute(self, plan: list, dependency_graph: DependencyGraph) -> dict:
        """Execute plan with parallelism where possible."""
        groups = dependency_graph.get_parallel_groups()
        results = {}

        for group in groups:
            group_results = await self._execute_group(group, results)
            results.update(group_results)

            # Check for failures
            failures = [r for r in group_results.values() if r["status"] == "failed"]
            if failures:
                return {
                    "status": "partial_failure",
                    "results": results,
                    "failures": failures
                }

        return {
            "status": "success",
            "results": results
        }

    async def _execute_group(self, task_ids: list, context: dict) -> dict:
        """Execute a group of tasks in parallel."""
        tasks = [
            self._execute_task_async(task_id, context)
            for task_id in task_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            task_id: result
            for task_id, result in zip(task_ids, results)
        }

    async def _execute_task_async(self, task_id: str, context: dict) -> dict:
        """Execute a task asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.agent.execute_task({"id": task_id}, context=context)
        )
```

## Adaptive Replanning

### Failure Recovery

```python
class AdaptiveReplanner:
    """Replan when execution fails or circumstances change."""

    def __init__(self, planner, executor):
        self.planner = planner
        self.executor = executor
        self.max_replans = 3

    async def execute_with_replanning(self, goal: str, context: dict) -> dict:
        """Execute goal with adaptive replanning."""
        replan_count = 0
        current_plan = self.planner.create_plan(goal, context)

        while replan_count < self.max_replans:
            result = await self.executor.execute(current_plan)

            if result["status"] == "success":
                return result

            # Analyze failure
            failure_analysis = self._analyze_failure(result)

            # Decide whether to replan
            if not failure_analysis["recoverable"]:
                return {
                    "status": "failed",
                    "reason": "Unrecoverable failure",
                    "analysis": failure_analysis
                }

            # Create new plan accounting for failure
            current_plan = self._create_recovery_plan(
                goal,
                context,
                result,
                failure_analysis
            )
            replan_count += 1

        return {
            "status": "failed",
            "reason": f"Exceeded maximum replans ({self.max_replans})"
        }

    def _analyze_failure(self, result: dict) -> dict:
        """Analyze why execution failed."""
        failed_task = result.get("failed_task")
        error = result.get("error")

        analysis = {
            "failed_task": failed_task,
            "error": error,
            "error_type": self._classify_error(error),
            "recoverable": True,
            "suggestions": []
        }

        # Determine recovery options
        if analysis["error_type"] == "resource_unavailable":
            analysis["suggestions"].append("Wait and retry")
            analysis["suggestions"].append("Use alternative resource")

        elif analysis["error_type"] == "invalid_input":
            analysis["suggestions"].append("Validate inputs before execution")
            analysis["suggestions"].append("Request clarification")

        elif analysis["error_type"] == "timeout":
            analysis["suggestions"].append("Break into smaller tasks")
            analysis["suggestions"].append("Increase timeout")

        elif analysis["error_type"] == "permission_denied":
            analysis["recoverable"] = False
            analysis["suggestions"].append("Request necessary permissions")

        return analysis

    def _create_recovery_plan(self, goal, context, failed_result, analysis) -> dict:
        """Create a new plan that addresses the failure."""
        completed = failed_result.get("completed", [])
        failed_task = failed_result.get("failed_task")

        # Update context with completed work
        recovery_context = {
            **context,
            "completed_tasks": completed,
            "failed_task": failed_task,
            "failure_reason": analysis["error"],
            "recovery_suggestions": analysis["suggestions"]
        }

        # Create recovery plan
        return self.planner.create_recovery_plan(
            goal,
            recovery_context,
            strategy=analysis["suggestions"][0] if analysis["suggestions"] else "retry"
        )
```

### Dynamic Reprioritization

```python
class DynamicPrioritizer:
    """Dynamically reprioritize tasks based on changing conditions."""

    def __init__(self):
        self.priority_factors = {
            "deadline_proximity": 0.3,
            "dependency_count": 0.2,
            "resource_availability": 0.2,
            "strategic_importance": 0.3
        }

    def reprioritize(self, tasks: list, context: dict) -> list:
        """Reprioritize tasks based on current conditions."""
        scored_tasks = []

        for task in tasks:
            score = self._calculate_priority_score(task, context)
            scored_tasks.append((score, task))

        # Sort by score (descending)
        scored_tasks.sort(key=lambda x: x[0], reverse=True)

        return [task for score, task in scored_tasks]

    def _calculate_priority_score(self, task: dict, context: dict) -> float:
        """Calculate priority score for a task."""
        score = 0

        # Deadline proximity
        if task.get("deadline"):
            time_remaining = self._time_until_deadline(task["deadline"])
            deadline_score = 1 / (1 + time_remaining.total_seconds() / 3600)
            score += deadline_score * self.priority_factors["deadline_proximity"]

        # Dependency count (more dependents = higher priority)
        dependent_count = len(context.get("dependents", {}).get(task["id"], []))
        dep_score = min(dependent_count / 5, 1)  # Normalize
        score += dep_score * self.priority_factors["dependency_count"]

        # Resource availability
        if self._resources_available(task, context):
            score += self.priority_factors["resource_availability"]

        # Strategic importance
        importance = task.get("importance", 0.5)
        score += importance * self.priority_factors["strategic_importance"]

        return score
```

## Plan Monitoring

```python
class PlanMonitor:
    """Monitor plan execution and detect issues."""

    def __init__(self):
        self.checkpoints = []
        self.alerts = []

    def add_checkpoint(self, task_id: str, expected_completion: datetime):
        """Add a checkpoint to monitor."""
        self.checkpoints.append({
            "task_id": task_id,
            "expected_completion": expected_completion,
            "actual_completion": None,
            "status": "pending"
        })

    def update_checkpoint(self, task_id: str, status: str):
        """Update checkpoint status."""
        for cp in self.checkpoints:
            if cp["task_id"] == task_id:
                cp["status"] = status
                cp["actual_completion"] = datetime.now()

                # Check for delays
                if cp["actual_completion"] > cp["expected_completion"]:
                    delay = cp["actual_completion"] - cp["expected_completion"]
                    self._raise_alert("delay", {
                        "task_id": task_id,
                        "delay": delay
                    })
                break

    def _raise_alert(self, alert_type: str, details: dict):
        """Raise an alert for plan issues."""
        alert = {
            "type": alert_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.alerts.append(alert)

    def get_plan_health(self) -> dict:
        """Get overall plan health status."""
        completed = sum(1 for cp in self.checkpoints if cp["status"] == "completed")
        failed = sum(1 for cp in self.checkpoints if cp["status"] == "failed")
        pending = sum(1 for cp in self.checkpoints if cp["status"] == "pending")

        return {
            "total_tasks": len(self.checkpoints),
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "completion_rate": completed / len(self.checkpoints) if self.checkpoints else 0,
            "alerts": self.alerts,
            "health": "good" if failed == 0 else "degraded" if failed < 3 else "critical"
        }
```

## Summary

In this chapter, you've learned:

- **Goal Decomposition**: HTN and SMART goal frameworks
- **Dependency Management**: Task graphs and resource constraints
- **Execution Strategies**: Sequential and parallel execution
- **Adaptive Replanning**: Failure recovery and dynamic prioritization
- **Plan Monitoring**: Checkpoints and health tracking

## Key Takeaways

1. **Hierarchical Decomposition**: Break complex goals into manageable tasks
2. **Dependency Awareness**: Respect task dependencies and resources
3. **Parallel When Possible**: Execute independent tasks concurrently
4. **Expect Failures**: Plan for replanning when things go wrong
5. **Monitor Progress**: Track execution and detect issues early

## Next Steps

Now that you can plan complex tasks, let's explore Multi-Agent Systems in Chapter 6 for coordinating multiple agents.

---

**Ready for Chapter 6?** [Multi-Agent Systems](06-multi-agent-systems.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `task`, `task_id` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Task Planning` as an operating subsystem inside **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `tasks`, `dict`, `context` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Task Planning` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `task_id`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/TransformerOptimus/SuperAGI)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Memory & Learning](04-memory-learning.md)
- [Next Chapter: Chapter 6: Multi-Agent Systems](06-multi-agent-systems.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
