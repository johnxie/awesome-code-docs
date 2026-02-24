---
layout: default
title: "Chapter 6: Process Management"
parent: "CrewAI Tutorial"
nav_order: 6
---

# Chapter 6: Process Management

Welcome to **Chapter 6: Process Management**. In this part of **CrewAI Tutorial: Building Collaborative AI Agent Teams**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Different tasks require different execution approaches. This chapter explores various process management patterns in CrewAI, from sequential workflows to complex parallel processing and adaptive execution strategies.

## Process Types

### Sequential Processing

```python
from crewai import Crew, Process
from typing import List, Dict, Any

class SequentialProcessor:
    def __init__(self, crew: Crew):
        self.crew = crew
        self.crew.process = Process.sequential

    async def execute_sequential(self, tasks: List[Task]) -> Dict[str, Any]:
        """Execute tasks in strict sequential order"""
        results = []
        context = {}

        for i, task in enumerate(tasks):
            print(f"Executing task {i+1}/{len(tasks)}: {task.description}")

            # Add context from previous tasks
            task.context = context

            # Execute task
            result = await self.crew.execute_task(task)
            results.append(result)

            # Update context for next task
            context[f"task_{i}_result"] = result

            # Check if we should continue
            if self._should_stop_execution(result):
                break

        return {
            "process_type": "sequential",
            "total_tasks": len(tasks),
            "completed_tasks": len(results),
            "results": results,
            "final_context": context
        }

    def _should_stop_execution(self, result: Any) -> bool:
        """Determine if execution should stop based on result"""
        if isinstance(result, dict) and result.get("status") == "error":
            return True
        if isinstance(result, dict) and result.get("stop_execution"):
            return True
        return False
```

### Parallel Processing

```python
class ParallelProcessor:
    def __init__(self, crew: Crew):
        self.crew = crew
        self.max_concurrent = 5  # Limit concurrent executions

    async def execute_parallel(self, tasks: List[Task]) -> Dict[str, Any]:
        """Execute independent tasks in parallel"""
        # Group tasks by dependencies
        independent_tasks = self._identify_independent_tasks(tasks)

        # Execute independent tasks in parallel
        parallel_results = await self._execute_parallel_batch(independent_tasks)

        # Execute dependent tasks sequentially
        dependent_tasks = [t for t in tasks if t not in independent_tasks]
        sequential_results = []

        if dependent_tasks:
            sequential_processor = SequentialProcessor(self.crew)
            sequential_result = await sequential_processor.execute_sequential(dependent_tasks)
            sequential_results = sequential_result["results"]

        return {
            "process_type": "parallel",
            "parallel_tasks": len(independent_tasks),
            "sequential_tasks": len(dependent_tasks),
            "parallel_results": parallel_results,
            "sequential_results": sequential_results
        }

    def _identify_independent_tasks(self, tasks: List[Task]) -> List[Task]:
        """Identify tasks that can be executed independently"""
        independent = []

        for task in tasks:
            # Check if task has dependencies on other tasks in the list
            has_local_dependency = any(
                dep in [t.id for t in tasks if t != task]
                for dep in (task.dependencies or [])
            )

            if not has_local_dependency:
                independent.append(task)

        return independent

    async def _execute_parallel_batch(self, tasks: List[Task]) -> List[Any]:
        """Execute a batch of tasks in parallel with concurrency control"""
        import asyncio
        from asyncio import Semaphore

        semaphore = Semaphore(self.max_concurrent)
        results = []

        async def execute_with_semaphore(task: Task):
            async with semaphore:
                return await self.crew.execute_task(task)

        # Create tasks
        parallel_tasks = [execute_with_semaphore(task) for task in tasks]

        # Execute in parallel
        results = await asyncio.gather(*parallel_tasks, return_exceptions=True)

        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {tasks[i].description} failed: {result}")
                processed_results.append({"error": str(result)})
            else:
                processed_results.append(result)

        return processed_results
```

### Hierarchical Processing

```python
class HierarchicalProcessor:
    def __init__(self, manager_crew: Crew, worker_crews: List[Crew]):
        self.manager_crew = manager_crew
        self.worker_crews = worker_crews

    async def execute_hierarchical(self, complex_task: Task) -> Dict[str, Any]:
        """Execute complex task using hierarchical approach"""
        # Manager decomposes the task
        subtasks = await self._decompose_task(complex_task)

        # Assign subtasks to worker crews
        assignments = await self._assign_to_workers(subtasks)

        # Execute assignments in parallel
        results = await self._execute_assignments(assignments)

        # Manager synthesizes results
        final_result = await self._synthesize_results(results)

        return {
            "process_type": "hierarchical",
            "manager_decomposition": len(subtasks),
            "worker_assignments": len(assignments),
            "execution_results": results,
            "final_result": final_result
        }

    async def _decompose_task(self, task: Task) -> List[Task]:
        """Manager crew decomposes complex task"""
        decomposition_task = Task(
            description=f"Decompose this complex task: {task.description}",
            agent=self.manager_crew.agents[0],  # Manager agent
            expected_output="List of subtasks with assignments"
        )

        result = await self.manager_crew.execute_task(decomposition_task)
        return self._parse_subtasks(result)

    async def _assign_to_workers(self, subtasks: List[Task]) -> Dict[str, List[Task]]:
        """Assign subtasks to appropriate worker crews"""
        assignments = {}

        for subtask in subtasks:
            worker_id = self._select_worker_for_subtask(subtask)

            if worker_id not in assignments:
                assignments[worker_id] = []

            assignments[worker_id].append(subtask)

        return assignments

    def _select_worker_for_subtask(self, subtask: Task) -> str:
        """Select appropriate worker crew for subtask"""
        # Simple assignment logic (could be enhanced with ML)
        subtask_desc = subtask.description.lower()

        if "research" in subtask_desc:
            return "research_worker"
        elif "analysis" in subtask_desc:
            return "analysis_worker"
        elif "writing" in subtask_desc:
            return "content_worker"
        else:
            return "general_worker"
```

## Adaptive Process Management

### Dynamic Process Selection

```python
class AdaptiveProcessor:
    def __init__(self):
        self.process_history = []
        self.performance_metrics = {}

    async def execute_adaptive(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptively select and execute appropriate process"""
        # Analyze task characteristics
        task_analysis = await self._analyze_task(task)

        # Select optimal process
        selected_process = await self._select_process(task_analysis, context)

        # Execute with selected process
        result = await self._execute_with_process(selected_process, task)

        # Record execution for learning
        await self._record_execution(task_analysis, selected_process, result)

        return {
            "process_type": "adaptive",
            "selected_process": selected_process,
            "task_analysis": task_analysis,
            "result": result
        }

    async def _analyze_task(self, task: Task) -> Dict[str, Any]:
        """Analyze task to determine optimal execution approach"""
        return {
            "complexity": self._assess_complexity(task),
            "dependencies": len(task.dependencies or []),
            "estimated_duration": task.estimated_duration or 30,
            "required_skills": self._extract_required_skills(task),
            "urgency": task.priority
        }

    async def _select_process(self, task_analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Select optimal process based on task analysis and context"""
        # Simple decision tree (could be enhanced with ML)
        if task_analysis["complexity"] == "high" and task_analysis["dependencies"] > 2:
            return "hierarchical"
        elif task_analysis["dependencies"] == 0 and context.get("parallel_execution", True):
            return "parallel"
        else:
            return "sequential"

    def _assess_complexity(self, task: Task) -> str:
        """Assess task complexity"""
        desc_length = len(task.description)
        has_dependencies = len(task.dependencies or []) > 0

        if desc_length > 500 or has_dependencies:
            return "high"
        elif desc_length > 200:
            return "medium"
        else:
            return "low"

    def _extract_required_skills(self, task: Task) -> List[str]:
        """Extract required skills from task description"""
        skills = []
        desc = task.description.lower()

        skill_keywords = {
            "research": ["research", "investigate", "analyze"],
            "writing": ["write", "create", "draft"],
            "coding": ["code", "develop", "implement"],
            "design": ["design", "visual", "layout"]
        }

        for skill, keywords in skill_keywords.items():
            if any(keyword in desc for keyword in keywords):
                skills.append(skill)

        return skills

    async def _record_execution(self, task_analysis: Dict[str, Any], process: str, result: Any):
        """Record execution for continuous learning"""
        execution_record = {
            "task_analysis": task_analysis,
            "selected_process": process,
            "result": result,
            "timestamp": self._get_timestamp()
        }

        self.process_history.append(execution_record)

        # Update performance metrics
        if process not in self.performance_metrics:
            self.performance_metrics[process] = []

        self.performance_metrics[process].append(execution_record)
```

### Process Optimization

```python
class ProcessOptimizer:
    def __init__(self, adaptive_processor: AdaptiveProcessor):
        self.adaptive_processor = adaptive_processor

    async def optimize_processes(self) -> Dict[str, Any]:
        """Analyze and optimize process performance"""
        # Analyze historical performance
        analysis = await self._analyze_performance()

        # Identify optimization opportunities
        opportunities = await self._identify_opportunities(analysis)

        # Generate optimization recommendations
        recommendations = await self._generate_recommendations(opportunities)

        # Apply optimizations
        optimizations = await self._apply_optimizations(recommendations)

        return {
            "analysis": analysis,
            "opportunities": opportunities,
            "recommendations": recommendations,
            "applied_optimizations": optimizations
        }

    async def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze historical process performance"""
        performance_data = {}

        for process_type, executions in self.adaptive_processor.performance_metrics.items():
            success_rate = len([e for e in executions if e["result"].get("success")]) / len(executions)
            avg_duration = sum([e["result"].get("duration", 0) for e in executions]) / len(executions)

            performance_data[process_type] = {
                "executions": len(executions),
                "success_rate": success_rate,
                "average_duration": avg_duration
            }

        return performance_data

    async def _identify_opportunities(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        opportunities = []

        for process_type, metrics in analysis.items():
            if metrics["success_rate"] < 0.8:
                opportunities.append({
                    "type": "reliability",
                    "process": process_type,
                    "issue": "Low success rate",
                    "improvement_potential": 0.2 - (1 - metrics["success_rate"])
                })

            if metrics["average_duration"] > 60:  # 1 minute
                opportunities.append({
                    "type": "performance",
                    "process": process_type,
                    "issue": "Slow execution",
                    "improvement_potential": 0.3
                })

        return opportunities
```

## Process Monitoring and Control

### Execution Monitoring

```python
class ProcessMonitor:
    def __init__(self):
        self.active_processes = {}
        self.process_metrics = {}

    async def monitor_execution(self, process_id: str, process_type: str):
        """Monitor process execution"""
        self.active_processes[process_id] = {
            "type": process_type,
            "start_time": self._get_timestamp(),
            "status": "running",
            "checkpoints": []
        }

        # Start monitoring loop
        await self._start_monitoring_loop(process_id)

    async def _start_monitoring_loop(self, process_id: str):
        """Monitor process continuously"""
        import asyncio

        while process_id in self.active_processes:
            process_info = self.active_processes[process_id]

            # Check process health
            health = await self._check_process_health(process_id)

            # Record checkpoint
            checkpoint = {
                "timestamp": self._get_timestamp(),
                "health": health,
                "metrics": await self._collect_metrics(process_id)
            }

            process_info["checkpoints"].append(checkpoint)

            # Check for issues
            if health["status"] == "unhealthy":
                await self._handle_unhealthy_process(process_id, health)

            await asyncio.sleep(30)  # Check every 30 seconds

    async def _check_process_health(self, process_id: str) -> Dict[str, Any]:
        """Check process health status"""
        # Implementation would check various health indicators
        return {
            "status": "healthy",
            "cpu_usage": 45,
            "memory_usage": 60,
            "error_rate": 0.02
        }

    async def _collect_metrics(self, process_id: str) -> Dict[str, Any]:
        """Collect process metrics"""
        return {
            "tasks_completed": 5,
            "tasks_pending": 3,
            "average_task_duration": 45,
            "success_rate": 0.95
        }

    async def stop_monitoring(self, process_id: str):
        """Stop monitoring process"""
        if process_id in self.active_processes:
            process_info = self.active_processes[process_id]
            process_info["end_time"] = self._get_timestamp()
            process_info["status"] = "completed"

            # Calculate final metrics
            await self._calculate_final_metrics(process_id)
```

### Process Control

```python
class ProcessController:
    def __init__(self, monitor: ProcessMonitor):
        self.monitor = monitor
        self.control_policies = {}

    async def control_process(self, process_id: str, action: str, parameters: Dict[str, Any] = None):
        """Control running process"""
        if action == "pause":
            await self._pause_process(process_id)
        elif action == "resume":
            await self._resume_process(process_id)
        elif action == "stop":
            await self._stop_process(process_id)
        elif action == "scale":
            await self._scale_process(process_id, parameters)
        elif action == "restart":
            await self._restart_process(process_id)

    async def _pause_process(self, process_id: str):
        """Pause process execution"""
        # Implementation would send pause signal to process
        print(f"Pausing process {process_id}")
        await self.monitor.update_process_status(process_id, "paused")

    async def _resume_process(self, process_id: str):
        """Resume process execution"""
        print(f"Resuming process {process_id}")
        await self.monitor.update_process_status(process_id, "running")

    async def _scale_process(self, process_id: str, parameters: Dict[str, Any]):
        """Scale process resources"""
        scale_type = parameters.get("type", "up")
        scale_factor = parameters.get("factor", 2)

        print(f"Scaling process {process_id} {scale_type} by factor {scale_factor}")
        await self.monitor.record_scaling_event(process_id, scale_type, scale_factor)
```

## What We've Accomplished

✅ **Implemented sequential processing** for dependent tasks
✅ **Built parallel processing** for independent tasks
✅ **Created hierarchical processing** for complex task decomposition
✅ **Developed adaptive processing** that learns and optimizes
✅ **Established process monitoring** and health checking
✅ **Implemented process control** for runtime management

## Next Steps

Ready for advanced multi-crew systems? In [Chapter 7: Advanced Crew Patterns](07-advanced-patterns.md), we'll explore complex multi-crew architectures, hierarchies, and specialized crew formations.

---

**Key Takeaway:** Different tasks require different execution approaches. Understanding when to use sequential, parallel, hierarchical, or adaptive processing is crucial for building efficient and effective AI crew systems.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `task`, `process_id` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Process Management` as an operating subsystem inside **CrewAI Tutorial: Building Collaborative AI Agent Teams**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `process`, `result`, `tasks` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Process Management` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `process_id`.
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
- [Previous Chapter: Chapter 5: Crew Communication](05-crew-communication.md)
- [Next Chapter: Chapter 7: Advanced Crew Patterns](07-advanced-patterns.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
