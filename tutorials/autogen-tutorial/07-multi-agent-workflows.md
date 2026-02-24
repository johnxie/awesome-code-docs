---
layout: default
title: "Chapter 7: Multi-Agent Workflows"
parent: "Microsoft AutoGen Tutorial"
nav_order: 7
---

# Chapter 7: Multi-Agent Workflows

Welcome to multi-agent workflows! In this chapter, we'll explore how to orchestrate complex interactions between multiple AutoGen agents, create sophisticated workflow patterns, and build scalable multi-agent systems that can tackle complex real-world problems.

## Workflow Fundamentals

### Workflow Architecture

```python
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import asyncio
import time

class WorkflowType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    HIERARCHICAL = "hierarchical"

class WorkflowStep:
    def __init__(self, step_id: str, agent_name: str, task_template: str,
                 inputs: List[str] = None, outputs: List[str] = None):
        self.step_id = step_id
        self.agent_name = agent_name
        self.task_template = task_template
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.status = "pending"
        self.result = None
        self.execution_time = None

class Workflow:
    def __init__(self, workflow_id: str, name: str, workflow_type: WorkflowType):
        self.workflow_id = workflow_id
        self.name = name
        self.workflow_type = workflow_type
        self.steps: List[WorkflowStep] = []
        self.dependencies: Dict[str, List[str]] = {}
        self.context: Dict[str, Any] = {}
        self.status = "created"
        self.start_time = None
        self.end_time = None

    def add_step(self, step: WorkflowStep, dependencies: List[str] = None):
        """Add a step to the workflow"""
        self.steps.append(step)
        if dependencies:
            self.dependencies[step.step_id] = dependencies

    def get_executable_steps(self) -> List[WorkflowStep]:
        """Get steps that can be executed (all dependencies met)"""
        executable = []

        for step in self.steps:
            if step.status != "pending":
                continue

            deps = self.dependencies.get(step.step_id, [])
            if all(self._is_step_completed(dep) for dep in deps):
                executable.append(step)

        return executable

    def _is_step_completed(self, step_id: str) -> bool:
        """Check if a step is completed"""
        step = next((s for s in self.steps if s.step_id == step_id), None)
        return step and step.status == "completed"

    def update_step_result(self, step_id: str, result: Any):
        """Update the result of a completed step"""
        step = next((s for s in self.steps if s.step_id == step_id), None)
        if step:
            step.result = result
            step.status = "completed"
            step.execution_time = time.time()

            # Update context with step outputs
            if step.outputs:
                for output in step.outputs:
                    self.context[output] = result

class WorkflowExecutor:
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.active_workflows: Dict[str, Workflow] = {}

    async def execute_workflow(self, workflow: Workflow) -> Dict[str, Any]:
        """Execute a complete workflow"""
        workflow.status = "running"
        workflow.start_time = time.time()
        self.active_workflows[workflow.workflow_id] = workflow

        try:
            if workflow.workflow_type == WorkflowType.SEQUENTIAL:
                result = await self._execute_sequential(workflow)
            elif workflow.workflow_type == WorkflowType.PARALLEL:
                result = await self._execute_parallel(workflow)
            elif workflow.workflow_type == WorkflowType.CONDITIONAL:
                result = await self._execute_conditional(workflow)
            elif workflow.workflow_type == WorkflowType.HIERARCHICAL:
                result = await self._execute_hierarchical(workflow)
            else:
                raise ValueError(f"Unsupported workflow type: {workflow.workflow_type}")

            workflow.status = "completed"
            workflow.end_time = time.time()

            return {
                "success": True,
                "workflow_id": workflow.workflow_id,
                "result": result,
                "execution_time": workflow.end_time - workflow.start_time,
                "steps_completed": len([s for s in workflow.steps if s.status == "completed"])
            }

        except Exception as e:
            workflow.status = "failed"
            workflow.end_time = time.time()

            return {
                "success": False,
                "workflow_id": workflow.workflow_id,
                "error": str(e),
                "execution_time": workflow.end_time - workflow.start_time
            }

    async def _execute_sequential(self, workflow: Workflow) -> Any:
        """Execute steps sequentially"""
        for step in workflow.steps:
            await self._execute_step(workflow, step)
        return workflow.context

    async def _execute_parallel(self, workflow: Workflow) -> Any:
        """Execute executable steps in parallel"""
        while True:
            executable_steps = workflow.get_executable_steps()

            if not executable_steps:
                break

            # Execute steps in parallel
            tasks = [self._execute_step(workflow, step) for step in executable_steps]
            await asyncio.gather(*tasks)

        return workflow.context

    async def _execute_conditional(self, workflow: Workflow) -> Any:
        """Execute steps based on conditions"""
        for step in workflow.steps:
            # Check condition (simplified)
            condition_met = self._evaluate_condition(workflow, step)
            if condition_met:
                await self._execute_step(workflow, step)
        return workflow.context

    async def _execute_hierarchical(self, workflow: Workflow) -> Any:
        """Execute hierarchical workflow"""
        # Simplified hierarchical execution
        await self._execute_sequential(workflow)
        return workflow.context

    async def _execute_step(self, workflow: Workflow, step: WorkflowStep):
        """Execute a single workflow step"""
        agent = self.agents.get(step.agent_name)
        if not agent:
            raise ValueError(f"Agent {step.agent_name} not found")

        # Prepare task with context
        task = self._prepare_task(step, workflow.context)

        # Execute task
        start_time = time.time()
        result = await agent.generate_reply(
            messages=[{"role": "user", "content": task}]
        )
        execution_time = time.time() - start_time

        # Update step result
        workflow.update_step_result(step.step_id, result)

        print(f"Executed step {step.step_id} with agent {step.agent_name} in {execution_time:.2f}s")

    def _prepare_task(self, step: WorkflowStep, context: Dict[str, Any]) -> str:
        """Prepare task by filling template with context"""
        task = step.task_template

        # Replace placeholders with context values
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            task = task.replace(placeholder, str(value))

        return task

    def _evaluate_condition(self, workflow: Workflow, step: WorkflowStep) -> bool:
        """Evaluate condition for conditional execution"""
        # Simplified condition evaluation
        return True
```

## Sequential Workflows

### Research and Writing Pipeline

```python
class ResearchWritingWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_research_workflow(self, topic: str) -> Workflow:
        """Create a research and writing workflow"""
        workflow = Workflow("research_writing", "Research and Writing Pipeline", WorkflowType.SEQUENTIAL)

        # Step 1: Research phase
        research_step = WorkflowStep(
            step_id="research",
            agent_name="ResearchAgent",
            task_template=f"Research the topic: {topic}. Provide comprehensive information from reliable sources.",
            outputs=["research_findings"]
        )
        workflow.add_step(research_step)

        # Step 2: Analysis phase
        analysis_step = WorkflowStep(
            step_id="analysis",
            agent_name="AnalysisAgent",
            task_template="Analyze these research findings and extract key insights: {{research_findings}}",
            inputs=["research_findings"],
            outputs=["key_insights"]
        )
        workflow.add_step(analysis_step, dependencies=["research"])

        # Step 3: Writing phase
        writing_step = WorkflowStep(
            step_id="writing",
            agent_name="WritingAgent",
            task_template="Write a comprehensive article about {topic} based on these insights: {{key_insights}}",
            inputs=["key_insights"],
            outputs=["final_article"]
        )
        workflow.add_step(writing_step, dependencies=["analysis"])

        # Step 4: Review phase
        review_step = WorkflowStep(
            step_id="review",
            agent_name="ReviewAgent",
            task_template="Review this article for accuracy, clarity, and completeness: {{final_article}}",
            inputs=["final_article"],
            outputs=["review_feedback"]
        )
        workflow.add_step(review_step, dependencies=["writing"])

        return workflow

    async def execute_research_workflow(self, topic: str) -> Dict[str, Any]:
        """Execute the complete research workflow"""
        workflow = self.create_research_workflow(topic)
        result = await self.workflow_executor.execute_workflow(workflow)

        return {
            "topic": topic,
            "workflow_result": result,
            "final_article": workflow.context.get("final_article"),
            "review_feedback": workflow.context.get("review_feedback")
        }
```

### Software Development Pipeline

```python
class SoftwareDevelopmentWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_development_workflow(self, requirements: str) -> Workflow:
        """Create a software development workflow"""
        workflow = Workflow("software_dev", "Software Development Pipeline", WorkflowType.SEQUENTIAL)

        # Step 1: Requirements analysis
        analysis_step = WorkflowStep(
            step_id="requirements_analysis",
            agent_name="AnalysisAgent",
            task_template=f"Analyze these software requirements: {requirements}",
            outputs=["analyzed_requirements"]
        )
        workflow.add_step(analysis_step)

        # Step 2: Design phase
        design_step = WorkflowStep(
            step_id="design",
            agent_name="DesignAgent",
            task_template="Create a technical design based on: {{analyzed_requirements}}",
            inputs=["analyzed_requirements"],
            outputs=["technical_design"]
        )
        workflow.add_step(design_step, dependencies=["requirements_analysis"])

        # Step 3: Implementation
        implementation_step = WorkflowStep(
            step_id="implementation",
            agent_name="CodingAgent",
            task_template="Implement the solution based on this design: {{technical_design}}",
            inputs=["technical_design"],
            outputs=["implementation_code"]
        )
        workflow.add_step(implementation_step, dependencies=["design"])

        # Step 4: Testing
        testing_step = WorkflowStep(
            step_id="testing",
            agent_name="TestingAgent",
            task_template="Create tests for this implementation: {{implementation_code}}",
            inputs=["implementation_code"],
            outputs=["test_suite"]
        )
        workflow.add_step(testing_step, dependencies=["implementation"])

        # Step 5: Documentation
        documentation_step = WorkflowStep(
            step_id="documentation",
            agent_name="WritingAgent",
            task_template="Create documentation for: {{implementation_code}}",
            inputs=["implementation_code"],
            outputs=["documentation"]
        )
        workflow.add_step(documentation_step, dependencies=["implementation"])

        return workflow
```

## Parallel Workflows

### Multi-Perspective Analysis

```python
class MultiPerspectiveWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_analysis_workflow(self, topic: str) -> Workflow:
        """Create a multi-perspective analysis workflow"""
        workflow = Workflow("multi_perspective", "Multi-Perspective Analysis", WorkflowType.PARALLEL)

        perspectives = [
            ("technical", "TechnicalAgent", "Analyze from a technical perspective"),
            ("business", "BusinessAgent", "Analyze from a business perspective"),
            ("user_experience", "UXAgent", "Analyze from a user experience perspective"),
            ("ethical", "EthicsAgent", "Analyze from an ethical perspective")
        ]

        synthesis_inputs = []

        for perspective_name, agent_name, task_desc in perspectives:
            step = WorkflowStep(
                step_id=f"analysis_{perspective_name}",
                agent_name=agent_name,
                task_template=f"{task_desc}: {topic}",
                outputs=[f"{perspective_name}_analysis"]
            )
            workflow.add_step(step)
            synthesis_inputs.append(f"{perspective_name}_analysis")

        # Synthesis step (depends on all analysis steps)
        synthesis_step = WorkflowStep(
            step_id="synthesis",
            agent_name="SynthesisAgent",
            task_template=f"""Synthesize these analyses into a comprehensive report:

{chr(10).join([f"{p[0]}: {{{p[0]}_analysis}}" for p in perspectives])}

Topic: {topic}""",
            inputs=synthesis_inputs,
            outputs=["final_report"]
        )
        workflow.add_step(synthesis_step, dependencies=[f"analysis_{p[0]}" for p in perspectives])

        return workflow

    async def execute_analysis_workflow(self, topic: str) -> Dict[str, Any]:
        """Execute multi-perspective analysis"""
        workflow = self.create_analysis_workflow(topic)
        result = await self.workflow_executor.execute_workflow(workflow)

        return {
            "topic": topic,
            "analyses": {k: v for k, v in workflow.context.items() if k.endswith("_analysis")},
            "final_report": workflow.context.get("final_report"),
            "execution_time": result.get("execution_time")
        }
```

### Parallel Research Workflow

```python
class ParallelResearchWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_parallel_research_workflow(self, research_questions: List[str]) -> Workflow:
        """Create a workflow that researches multiple questions in parallel"""
        workflow = Workflow("parallel_research", "Parallel Research", WorkflowType.PARALLEL)

        research_outputs = []

        # Create parallel research steps
        for i, question in enumerate(research_questions):
            step = WorkflowStep(
                step_id=f"research_{i}",
                agent_name="ResearchAgent",
                task_template=f"Research this question: {question}",
                outputs=[f"research_result_{i}"]
            )
            workflow.add_step(step)
            research_outputs.append(f"research_result_{i}")

        # Synthesis step
        synthesis_step = WorkflowStep(
            step_id="synthesis",
            agent_name="SynthesisAgent",
            task_template=f"""Synthesize these research results into a comprehensive answer:

{chr(10).join([f"Research {i}: {{{research_outputs[i]}}}" for i in range(len(research_questions))])}""",
            inputs=research_outputs,
            outputs=["synthesized_answer"]
        )

        dependencies = [f"research_{i}" for i in range(len(research_questions))]
        workflow.add_step(synthesis_step, dependencies=dependencies)

        return workflow
```

## Conditional Workflows

### Adaptive Problem Solving

```python
class AdaptiveWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_adaptive_workflow(self, problem: str) -> Workflow:
        """Create an adaptive workflow that adjusts based on results"""
        workflow = Workflow("adaptive", "Adaptive Problem Solving", WorkflowType.CONDITIONAL)

        # Initial assessment
        assessment_step = WorkflowStep(
            step_id="assessment",
            agent_name="AnalysisAgent",
            task_template=f"Assess this problem and determine the approach needed: {problem}",
            outputs=["problem_assessment", "approach_type"]
        )
        workflow.add_step(assessment_step)

        # Conditional paths based on assessment
        technical_solution = WorkflowStep(
            step_id="technical_solution",
            agent_name="TechnicalAgent",
            task_template="Provide a technical solution for: {{problem_assessment}}",
            inputs=["problem_assessment"],
            outputs=["solution"]
        )
        workflow.add_step(technical_solution, dependencies=["assessment"])

        business_solution = WorkflowStep(
            step_id="business_solution",
            agent_name="BusinessAgent",
            task_template="Provide a business solution for: {{problem_assessment}}",
            inputs=["problem_assessment"],
            outputs=["solution"]
        )
        workflow.add_step(business_solution, dependencies=["assessment"])

        creative_solution = WorkflowStep(
            step_id="creative_solution",
            agent_name="CreativeAgent",
            task_template="Provide a creative solution for: {{problem_assessment}}",
            inputs=["problem_assessment"],
            outputs=["solution"]
        )
        workflow.add_step(creative_solution, dependencies=["assessment"])

        # Final review step
        review_step = WorkflowStep(
            step_id="review",
            agent_name="ReviewAgent",
            task_template="Review and refine this solution: {{solution}}",
            inputs=["solution"],
            outputs=["final_solution"]
        )
        workflow.add_step(review_step, dependencies=["technical_solution", "business_solution", "creative_solution"])

        return workflow

    async def execute_adaptive_workflow(self, problem: str) -> Dict[str, Any]:
        """Execute adaptive workflow with custom logic"""
        workflow = self.create_adaptive_workflow(problem)

        # Custom execution logic for conditional workflow
        result = await self._execute_adaptive_logic(workflow, problem)

        return result

    async def _execute_adaptive_logic(self, workflow: Workflow, problem: str) -> Dict[str, Any]:
        """Execute workflow with adaptive logic"""
        # Step 1: Assessment
        assessment_step = next(s for s in workflow.steps if s.step_id == "assessment")
        await self.workflow_executor._execute_step(workflow, assessment_step)

        # Get assessment result
        assessment = workflow.context.get("problem_assessment", "")
        approach = workflow.context.get("approach_type", "technical")

        # Step 2: Choose appropriate solution path
        if "technical" in approach.lower():
            solution_step = next(s for s in workflow.steps if s.step_id == "technical_solution")
        elif "business" in approach.lower():
            solution_step = next(s for s in workflow.steps if s.step_id == "business_solution")
        else:
            solution_step = next(s for s in workflow.steps if s.step_id == "creative_solution")

        await self.workflow_executor._execute_step(workflow, solution_step)

        # Step 3: Review
        review_step = next(s for s in workflow.steps if s.step_id == "review")
        await self.workflow_executor._execute_step(workflow, review_step)

        return {
            "problem": problem,
            "assessment": assessment,
            "approach": approach,
            "solution": workflow.context.get("solution"),
            "final_solution": workflow.context.get("final_solution")
        }
```

## Hierarchical Workflows

### Project Management Workflow

```python
class ProjectManagementWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_executor = WorkflowExecutor(agents)

    def create_project_workflow(self, project_description: str) -> Workflow:
        """Create a hierarchical project management workflow"""
        workflow = Workflow("project_mgmt", "Project Management", WorkflowType.HIERARCHICAL)

        # Phase 1: Planning
        planning_phase = self._create_planning_subworkflow()
        workflow.add_step(WorkflowStep(
            step_id="planning_phase",
            agent_name="ManagerAgent",
            task_template=f"Execute planning phase for: {project_description}",
            outputs=["planning_results"]
        ))

        # Phase 2: Execution
        execution_phase = self._create_execution_subworkflow()
        workflow.add_step(WorkflowStep(
            step_id="execution_phase",
            agent_name="ManagerAgent",
            task_template="Execute project based on planning: {{planning_results}}",
            inputs=["planning_results"],
            outputs=["execution_results"]
        ), dependencies=["planning_phase"])

        # Phase 3: Review
        review_step = WorkflowStep(
            step_id="review",
            agent_name="ReviewAgent",
            task_template="Review project execution: {{execution_results}}",
            inputs=["execution_results"],
            outputs=["review_results"]
        )
        workflow.add_step(review_step, dependencies=["execution_phase"])

        return workflow

    def _create_planning_subworkflow(self) -> Workflow:
        """Create planning sub-workflow"""
        planning = Workflow("planning", "Planning Phase", WorkflowType.SEQUENTIAL)

        planning.add_step(WorkflowStep(
            step_id="scope_definition",
            agent_name="AnalysisAgent",
            task_template="Define project scope and objectives",
            outputs=["scope"]
        ))

        planning.add_step(WorkflowStep(
            step_id="resource_planning",
            agent_name="PlanningAgent",
            task_template="Plan resources needed: {{scope}}",
            inputs=["scope"],
            outputs=["resources"]
        ), dependencies=["scope_definition"])

        return planning

    def _create_execution_subworkflow(self) -> Workflow:
        """Create execution sub-workflow"""
        execution = Workflow("execution", "Execution Phase", WorkflowType.PARALLEL)

        execution.add_step(WorkflowStep(
            step_id="development",
            agent_name="CodingAgent",
            task_template="Execute development tasks",
            outputs=["development_results"]
        ))

        execution.add_step(WorkflowStep(
            step_id="testing",
            agent_name="TestingAgent",
            task_template="Execute testing tasks",
            outputs=["testing_results"]
        ))

        execution.add_step(WorkflowStep(
            step_id="documentation",
            agent_name="WritingAgent",
            task_template="Create documentation",
            outputs=["documentation_results"]
        ))

        return execution
```

## Workflow Monitoring and Optimization

### Performance Monitoring

```python
class WorkflowMonitor:
    def __init__(self):
        self.workflow_metrics = {}
        self.step_metrics = {}

    def record_workflow_execution(self, workflow: Workflow):
        """Record workflow execution metrics"""
        execution_time = workflow.end_time - workflow.start_time if workflow.end_time else 0

        self.workflow_metrics[workflow.workflow_id] = {
            "name": workflow.name,
            "type": workflow.workflow_type.value,
            "status": workflow.status,
            "execution_time": execution_time,
            "steps_completed": len([s for s in workflow.steps if s.status == "completed"]),
            "total_steps": len(workflow.steps),
            "timestamp": time.time()
        }

    def record_step_execution(self, step: WorkflowStep, workflow_id: str):
        """Record step execution metrics"""
        if step.execution_time:
            step_key = f"{workflow_id}_{step.step_id}"
            self.step_metrics[step_key] = {
                "workflow_id": workflow_id,
                "step_id": step.step_id,
                "agent": step.agent_name,
                "execution_time": step.execution_time,
                "status": step.status,
                "timestamp": time.time()
            }

    def get_workflow_performance_report(self) -> Dict[str, Any]:
        """Generate workflow performance report"""
        total_workflows = len(self.workflow_metrics)
        completed_workflows = len([w for w in self.workflow_metrics.values() if w["status"] == "completed"])
        success_rate = completed_workflows / total_workflows if total_workflows > 0 else 0

        avg_execution_time = sum(w["execution_time"] for w in self.workflow_metrics.values()) / total_workflows

        return {
            "total_workflows": total_workflows,
            "completed_workflows": completed_workflows,
            "success_rate": success_rate,
            "average_execution_time": avg_execution_time,
            "workflow_types": self._get_workflow_type_stats()
        }

    def _get_workflow_type_stats(self) -> Dict[str, int]:
        """Get statistics by workflow type"""
        type_stats = {}
        for workflow in self.workflow_metrics.values():
            wtype = workflow["type"]
            type_stats[wtype] = type_stats.get(wtype, 0) + 1
        return type_stats

    def get_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify workflow bottlenecks"""
        bottlenecks = []

        for step_key, metrics in self.step_metrics.items():
            if metrics["execution_time"] > 30:  # Threshold for bottleneck
                bottlenecks.append({
                    "step": metrics["step_id"],
                    "workflow": metrics["workflow_id"],
                    "execution_time": metrics["execution_time"],
                    "agent": metrics["agent"]
                })

        return sorted(bottlenecks, key=lambda x: x["execution_time"], reverse=True)

class WorkflowOptimizer:
    def __init__(self, monitor: WorkflowMonitor):
        self.monitor = monitor

    def suggest_optimizations(self) -> List[str]:
        """Suggest workflow optimizations based on metrics"""
        suggestions = []

        # Check for bottlenecks
        bottlenecks = self.monitor.get_bottlenecks()
        if bottlenecks:
            suggestions.append(f"Address {len(bottlenecks)} workflow bottlenecks")

        # Check workflow type distribution
        performance_report = self.monitor.get_workflow_performance_report()
        workflow_types = performance_report["workflow_types"]

        # Suggest parallelization for sequential workflows
        sequential_count = workflow_types.get("sequential", 0)
        if sequential_count > len(workflow_types) * 0.7:
            suggestions.append("Consider converting sequential workflows to parallel where possible")

        # Check success rate
        success_rate = performance_report["success_rate"]
        if success_rate < 0.8:
            suggestions.append("Improve workflow success rate through better error handling")

        return suggestions
```

## Advanced Workflow Patterns

### Event-Driven Workflows

```python
class EventDrivenWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.event_handlers = {}
        self.active_workflows = {}

    def register_event_handler(self, event_type: str, handler):
        """Register handler for specific event types"""
        self.event_handlers[event_type] = handler

    async def handle_event(self, event: Dict[str, Any]):
        """Handle incoming events and trigger workflows"""
        event_type = event.get("type")
        handler = self.event_handlers.get(event_type)

        if handler:
            await handler(event)
        else:
            print(f"No handler found for event type: {event_type}")

    async def trigger_workflow_on_event(self, event: Dict[str, Any], workflow_template):
        """Trigger a workflow based on an event"""
        workflow = workflow_template(event)
        workflow_id = f"event_{event.get('id', time.time())}"

        # Customize workflow based on event data
        self._customize_workflow_for_event(workflow, event)

        self.active_workflows[workflow_id] = workflow

        # Execute workflow asynchronously
        asyncio.create_task(self._execute_workflow_async(workflow))

    def _customize_workflow_for_event(self, workflow: Workflow, event: Dict[str, Any]):
        """Customize workflow based on event data"""
        for step in workflow.steps:
            # Replace placeholders in task templates with event data
            for key, value in event.items():
                placeholder = f"{{{key}}}"
                step.task_template = step.task_template.replace(placeholder, str(value))

    async def _execute_workflow_async(self, workflow: Workflow):
        """Execute workflow asynchronously"""
        executor = WorkflowExecutor(self.agents)
        result = await executor.execute_workflow(workflow)
        print(f"Event-driven workflow completed: {result}")
```

### Self-Organizing Workflows

```python
class SelfOrganizingWorkflow:
    def __init__(self, agents):
        self.agents = agents
        self.workflow_history = []
        self.performance_patterns = {}

    async def create_adaptive_workflow(self, task: str) -> Workflow:
        """Create a workflow that adapts based on past performance"""
        # Analyze past performance
        similar_tasks = self._find_similar_tasks(task)
        best_pattern = self._identify_best_pattern(similar_tasks)

        # Create workflow based on best pattern
        workflow = Workflow("adaptive", "Self-Organizing Workflow", WorkflowType.SEQUENTIAL)

        for step_config in best_pattern["steps"]:
            step = WorkflowStep(
                step_id=step_config["id"],
                agent_name=step_config["agent"],
                task_template=step_config["task"]
            )
            workflow.add_step(step)

        return workflow

    def _find_similar_tasks(self, task: str) -> List[Dict[str, Any]]:
        """Find similar tasks from history"""
        similar = []
        task_keywords = set(task.lower().split())

        for past_task in self.workflow_history:
            past_keywords = set(past_task["task"].lower().split())
            similarity = len(task_keywords.intersection(past_keywords)) / len(task_keywords.union(past_keywords))

            if similarity > 0.3:  # Similarity threshold
                similar.append(past_task)

        return similar

    def _identify_best_pattern(self, similar_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify the best performing pattern"""
        if not similar_tasks:
            return self._get_default_pattern()

        # Group by pattern and calculate average performance
        pattern_performance = {}

        for task in similar_tasks:
            pattern_key = str(task.get("pattern", "default"))
            if pattern_key not in pattern_performance:
                pattern_performance[pattern_key] = []

            pattern_performance[pattern_key].append(task.get("performance", 0))

        # Find best performing pattern
        best_pattern = max(pattern_performance.items(),
                          key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0)

        return self._get_pattern_by_key(best_pattern[0])

    def _get_default_pattern(self) -> Dict[str, Any]:
        """Get default workflow pattern"""
        return {
            "steps": [
                {"id": "analyze", "agent": "AnalysisAgent", "task": "Analyze the task"},
                {"id": "execute", "agent": "ExecutionAgent", "task": "Execute the task"},
                {"id": "review", "agent": "ReviewAgent", "task": "Review the results"}
            ]
        }

    def record_workflow_performance(self, workflow: Workflow, performance: float):
        """Record workflow performance for learning"""
        workflow_record = {
            "task": workflow.name,
            "pattern": workflow.workflow_type.value,
            "performance": performance,
            "steps": [{"id": s.step_id, "agent": s.agent_name, "task": s.task_template} for s in workflow.steps],
            "timestamp": time.time()
        }

        self.workflow_history.append(workflow_record)
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Workflow Fundamentals** - Architecture and execution patterns
2. **Sequential Workflows** - Research pipelines and development workflows
3. **Parallel Workflows** - Multi-perspective analysis and parallel research
4. **Conditional Workflows** - Adaptive problem-solving workflows
5. **Hierarchical Workflows** - Project management and complex orchestration
6. **Workflow Monitoring** - Performance tracking and optimization
7. **Advanced Patterns** - Event-driven and self-organizing workflows

## Next Steps

Now that you understand multi-agent workflows, let's explore production deployment. In [Chapter 8: Production Deployment](08-production-deployment.md), we'll learn how to deploy multi-agent systems at scale with proper monitoring and management.

---

**Practice what you've learned:**
1. Create a sequential workflow for a complex task in your domain
2. Implement a parallel workflow that processes multiple subtasks simultaneously
3. Build a conditional workflow that adapts based on intermediate results
4. Set up workflow monitoring and performance tracking

*What kind of multi-agent workflow would you build first?* 🔄

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `workflow`, `self`, `step` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Multi-Agent Workflows` as an operating subsystem inside **Microsoft AutoGen Tutorial: Building Multi-Agent AI Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `step_id`, `agent_name`, `WorkflowStep` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Multi-Agent Workflows` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `workflow`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `step`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `workflow` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Custom Agent Development](06-custom-agents.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
