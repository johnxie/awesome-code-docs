---
layout: default
title: "Chapter 3: Task Definition & Planning"
parent: "CrewAI Tutorial"
nav_order: 3
---

# Chapter 3: Task Definition & Planning

Welcome to **Chapter 3: Task Definition & Planning**. In this part of **CrewAI Tutorial: Building Collaborative AI Agent Teams**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Mastering task definition and planning is crucial for building effective AI crews. This chapter explores how to break down complex objectives into actionable tasks that agents can execute collaboratively.

## Task Definition Framework

### Task Structure

```python
from crewai import Task
from typing import List, Dict, Any, Optional

class CrewTask(Task):
    def __init__(self,
                 description: str,
                 agent: Agent,
                 expected_output: str,
                 context: Optional[List[Task]] = None,
                 dependencies: Optional[List[str]] = None,
                 priority: str = "medium",
                 complexity: str = "medium",
                 estimated_duration: int = 30):

        super().__init__(
            description=description,
            agent=agent,
            expected_output=expected_output,
            context=context or []
        )

        self.dependencies = dependencies or []
        self.priority = priority
        self.complexity = complexity
        self.estimated_duration = estimated_duration
        self.actual_duration = None
        self.status = "pending"
        self.subtasks = []
```

### Task Categories

```python
task_categories = {
    "research": {
        "description": "Information gathering and analysis tasks",
        "examples": ["market_research", "competitive_analysis", "data_collection"],
        "required_agents": ["researcher", "analyst"]
    },

    "analysis": {
        "description": "Data processing and insights generation",
        "examples": ["data_analysis", "trend_identification", "performance_review"],
        "required_agents": ["analyst", "specialist"]
    },

    "creation": {
        "description": "Content and asset creation tasks",
        "examples": ["content_writing", "design_creation", "code_development"],
        "required_agents": ["creator", "specialist"]
    },

    "coordination": {
        "description": "Planning and management tasks",
        "examples": ["project_planning", "resource_allocation", "team_coordination"],
        "required_agents": ["manager", "coordinator"]
    }
}
```

## Task Decomposition Strategies

### Hierarchical Decomposition

```python
class TaskDecomposer:
    def __init__(self):
        self.decomposition_rules = {
            "research": self._decompose_research_task,
            "analysis": self._decompose_analysis_task,
            "creation": self._decompose_creation_task,
            "coordination": self._decompose_coordination_task
        }

    def decompose_task(self, task: CrewTask) -> List[CrewTask]:
        """Decompose a complex task into manageable subtasks"""
        task_type = self._classify_task(task)

        if task_type in self.decomposition_rules:
            return self.decomposition_rules[task_type](task)
        else:
            return [task]  # Task is already simple enough

    def _decompose_research_task(self, task: CrewTask) -> List[CrewTask]:
        """Decompose research tasks"""
        return [
            CrewTask(
                description=f"Define research scope and objectives for: {task.description[:50]}...",
                agent=self._find_agent_by_role("researcher"),
                expected_output="Research plan with objectives and methodology",
                priority=task.priority,
                complexity="low"
            ),
            CrewTask(
                description=f"Gather information from multiple sources for: {task.description[:50]}...",
                agent=self._find_agent_by_role("researcher"),
                expected_output="Comprehensive data collection from relevant sources",
                priority=task.priority,
                complexity="medium"
            ),
            CrewTask(
                description=f"Analyze collected data and extract insights for: {task.description[:50]}...",
                agent=self._find_agent_by_role("analyst"),
                expected_output="Analysis report with key findings and insights",
                priority=task.priority,
                complexity="medium"
            )
        ]

    def _classify_task(self, task: CrewTask) -> str:
        """Classify task type based on content analysis"""
        description = task.description.lower()

        if any(word in description for word in ["research", "investigate", "study", "analyze data"]):
            return "research"
        elif any(word in description for word in ["write", "create", "design", "develop"]):
            return "creation"
        elif any(word in description for word in ["plan", "coordinate", "manage", "organize"]):
            return "coordination"
        else:
            return "analysis"
```

### Dependency Management

```python
class TaskDependencyManager:
    def __init__(self):
        self.task_graph = {}
        self.completed_tasks = set()

    def add_task(self, task: CrewTask):
        """Add task to dependency graph"""
        self.task_graph[task.id] = {
            "task": task,
            "dependencies": task.dependencies,
            "dependents": []
        }

        # Update dependents
        for dep_id in task.dependencies:
            if dep_id in self.task_graph:
                self.task_graph[dep_id]["dependents"].append(task.id)

    def get_executable_tasks(self) -> List[CrewTask]:
        """Get tasks that can be executed (all dependencies met)"""
        executable = []

        for task_id, task_info in self.task_graph.items():
            if task_id not in self.completed_tasks:
                deps_met = all(dep in self.completed_tasks for dep in task_info["dependencies"])
                if deps_met:
                    executable.append(task_info["task"])

        return executable

    def mark_completed(self, task_id: str):
        """Mark task as completed"""
        self.completed_tasks.add(task_id)

    def get_critical_path(self) -> List[str]:
        """Calculate critical path through task dependencies"""
        # Implementation of critical path algorithm
        return self._calculate_critical_path()
```

## Advanced Planning Techniques

### Task Prioritization

```python
class TaskPrioritizer:
    def __init__(self):
        self.priority_weights = {
            "urgent": 1.0,
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }

    def prioritize_tasks(self, tasks: List[CrewTask]) -> List[CrewTask]:
        """Prioritize tasks based on multiple factors"""
        scored_tasks = []

        for task in tasks:
            score = self._calculate_priority_score(task)
            scored_tasks.append((task, score))

        # Sort by score (highest first)
        scored_tasks.sort(key=lambda x: x[1], reverse=True)

        return [task for task, score in scored_tasks]

    def _calculate_priority_score(self, task: CrewTask) -> float:
        """Calculate priority score based on multiple factors"""
        base_score = self.priority_weights.get(task.priority, 0.5)

        # Factor in urgency (deadline proximity)
        urgency_multiplier = self._calculate_urgency_multiplier(task)

        # Factor in dependencies (tasks with more dependents are more important)
        dependency_multiplier = 1 + (len(self._get_dependents(task)) * 0.1)

        # Factor in complexity (simpler tasks might be prioritized for quick wins)
        complexity_multiplier = 1 - (self._get_complexity_weight(task) * 0.2)

        return base_score * urgency_multiplier * dependency_multiplier * complexity_multiplier
```

### Resource Allocation Planning

```python
class ResourcePlanner:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.agent_workload = {agent.id: 0 for agent in agents}

    def allocate_resources(self, tasks: List[CrewTask]) -> Dict[str, List[CrewTask]]:
        """Allocate tasks to agents based on capacity and expertise"""
        allocation = {agent.id: [] for agent in self.agents}

        # Sort tasks by priority
        prioritized_tasks = sorted(tasks, key=lambda t: self._get_task_priority(t), reverse=True)

        for task in prioritized_tasks:
            best_agent = self._find_best_agent_for_task(task)

            if best_agent:
                allocation[best_agent.id].append(task)
                self.agent_workload[best_agent.id] += task.estimated_duration

        return allocation

    def _find_best_agent_for_task(self, task: CrewTask) -> Optional[Agent]:
        """Find best agent for task based on expertise and workload"""
        best_agent = None
        best_score = 0

        for agent in self.agents:
            expertise_score = self._calculate_expertise_match(agent, task)
            workload_score = self._calculate_workload_score(agent)
            availability_score = self._check_agent_availability(agent, task)

            total_score = (expertise_score * 0.5) + (workload_score * 0.3) + (availability_score * 0.2)

            if total_score > best_score:
                best_score = total_score
                best_agent = agent

        return best_agent

    def _calculate_expertise_match(self, agent: Agent, task: CrewTask) -> float:
        """Calculate how well agent's expertise matches task requirements"""
        # Implementation would analyze agent's skills vs task requirements
        return 0.8  # Placeholder
```

## Task Execution Monitoring

### Progress Tracking

```python
class TaskMonitor:
    def __init__(self):
        self.task_status = {}
        self.execution_logs = []

    def track_task_execution(self, task: CrewTask, agent: Agent):
        """Monitor task execution progress"""
        self.task_status[task.id] = {
            "status": "in_progress",
            "agent": agent.id,
            "start_time": self._get_current_time(),
            "progress": 0,
            "milestones": self._define_milestones(task)
        }

    def update_progress(self, task_id: str, progress: float, notes: str = ""):
        """Update task progress"""
        if task_id in self.task_status:
            self.task_status[task_id]["progress"] = progress
            self.task_status[task_id]["last_update"] = self._get_current_time()

            self.execution_logs.append({
                "task_id": task_id,
                "timestamp": self._get_current_time(),
                "progress": progress,
                "notes": notes
            })

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get current task status"""
        return self.task_status.get(task_id, {})

    def get_overall_progress(self, tasks: List[CrewTask]) -> Dict[str, Any]:
        """Get overall crew progress"""
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == "completed"])
        in_progress_tasks = len([t for t in tasks if t.status == "in_progress"])

        return {
            "total_tasks": total_tasks,
            "completed": completed_tasks,
            "in_progress": in_progress_tasks,
            "completion_percentage": (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        }
```

## Adaptive Planning

### Dynamic Replanning

```python
class AdaptivePlanner:
    def __init__(self):
        self.original_plan = None
        self.execution_history = []
        self.performance_metrics = {}

    def create_adaptive_plan(self, tasks: List[CrewTask], agents: List[Agent]):
        """Create initial plan with adaptation capabilities"""
        self.original_plan = self._create_initial_plan(tasks, agents)
        return self.original_plan

    def adapt_plan(self, execution_feedback: Dict[str, Any]):
        """Adapt plan based on execution feedback"""
        self.execution_history.append(execution_feedback)

        # Analyze performance
        issues = self._identify_performance_issues()

        if issues:
            # Generate adaptation strategies
            adaptations = self._generate_adaptations(issues)

            # Apply adaptations
            updated_plan = self._apply_adaptations(self.original_plan, adaptations)

            self.original_plan = updated_plan
            return updated_plan

        return self.original_plan

    def _identify_performance_issues(self) -> List[str]:
        """Identify performance issues from execution history"""
        issues = []

        recent_executions = self.execution_history[-10:]  # Last 10 executions

        # Check for delays
        avg_duration = sum(e.get("duration", 0) for e in recent_executions) / len(recent_executions)
        if avg_duration > 1.5 * self._get_expected_duration():
            issues.append("performance_degradation")

        # Check for failures
        failure_rate = len([e for e in recent_executions if e.get("success") == False]) / len(recent_executions)
        if failure_rate > 0.2:
            issues.append("high_failure_rate")

        return issues

    def _generate_adaptations(self, issues: List[str]) -> List[Dict[str, Any]]:
        """Generate adaptation strategies"""
        adaptations = []

        for issue in issues:
            if issue == "performance_degradation":
                adaptations.append({
                    "type": "resource_reallocation",
                    "action": "redistribute_tasks_to_underutilized_agents"
                })
            elif issue == "high_failure_rate":
                adaptations.append({
                    "type": "quality_improvement",
                    "action": "add_additional_review_steps"
                })

        return adaptations
```

## Best Practices for Task Planning

### Planning Principles

1. **SMART Tasks**: Specific, Measurable, Achievable, Relevant, Time-bound
2. **Dependency Awareness**: Understand and manage task relationships
3. **Resource Optimization**: Match tasks to agent capabilities and availability
4. **Progress Monitoring**: Track execution and adapt as needed
5. **Quality Assurance**: Include validation and review steps

### Common Planning Patterns

```python
# Research-Development Pattern
research_dev_pattern = {
    "phases": ["research", "analysis", "development", "testing", "deployment"],
    "dependencies": {
        "analysis": ["research"],
        "development": ["analysis"],
        "testing": ["development"],
        "deployment": ["testing"]
    }
}

# Agile Sprint Pattern
agile_pattern = {
    "iterations": ["planning", "development", "review", "retrospective"],
    "timeboxed": True,
    "feedback_loops": ["daily_standup", "sprint_review", "retrospective"]
}

# Critical Path Pattern
critical_path_pattern = {
    "focus": "identify and prioritize critical path tasks",
    "optimization": "minimize critical path duration",
    "monitoring": "track critical path progress closely"
}
```

## What We've Accomplished

✅ **Mastered task definition** with structured frameworks
✅ **Implemented task decomposition** strategies for complex objectives
✅ **Built dependency management** systems
✅ **Created intelligent task prioritization** algorithms
✅ **Developed resource allocation** planning
✅ **Established progress monitoring** and tracking
✅ **Implemented adaptive planning** for changing conditions

## Next Steps

Ready to equip your agents with tools? In [Chapter 4: Tool Integration](04-tool-integration.md), we'll explore how to integrate external tools and APIs to extend agent capabilities.

---

**Key Takeaway:** Effective task planning is the foundation of successful AI crew execution. Well-planned tasks with clear dependencies, proper resource allocation, and continuous monitoring enable agents to work efficiently toward complex objectives.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `task`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Task Definition & Planning` as an operating subsystem inside **CrewAI Tutorial: Building Collaborative AI Agent Teams**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `CrewTask`, `tasks`, `List` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Task Definition & Planning` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/crewAIInc/crewAI)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Agent Roles & Specializations](02-agent-roles.md)
- [Next Chapter: Chapter 4: Tool Integration](04-tool-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
