---
layout: default
title: "DSPy Tutorial - Chapter 6: Advanced Patterns"
nav_order: 6
has_children: false
parent: DSPy Tutorial
---

# Chapter 6: Advanced Patterns - Multi-Hop Reasoning and Tool Integration

> Master sophisticated DSPy patterns including multi-hop reasoning, tool integration, and complex agent workflows.

## Overview

Advanced DSPy patterns enable complex reasoning chains, external tool integration, and sophisticated agent behaviors. These patterns go beyond simple question-answering to handle multi-step reasoning, tool use, and collaborative workflows.

## Multi-Hop Reasoning

### Chain-of-Thought with Multiple Steps

```python
import dspy

class MultiHopReasoning(dspy.Module):
    def __init__(self):
        super().__init__()

        # Multiple reasoning steps
        self.step1 = dspy.Predict(Step1Signature)
        self.step2 = dspy.Predict(Step2Signature)
        self.step3 = dspy.Predict(Step3Signature)
        self.synthesize = dspy.Predict(SynthesisSignature)

    def forward(self, problem):
        # Step 1: Analyze the problem
        analysis = self.step1(problem=problem)

        # Step 2: Break down into components
        breakdown = self.step2(
            problem=problem,
            analysis=analysis.analysis
        )

        # Step 3: Solve components
        solutions = self.step3(
            problem=problem,
            components=breakdown.components
        )

        # Synthesize final answer
        final_answer = self.synthesize(
            problem=problem,
            analysis=analysis.analysis,
            breakdown=breakdown.components,
            solutions=solutions.component_solutions
        )

        return dspy.Prediction(
            analysis=analysis.analysis,
            components=breakdown.components,
            solutions=solutions.component_solutions,
            final_answer=final_answer.final_answer,
            reasoning=final_answer.reasoning
        )

# Define signatures for each step
class Step1Signature(dspy.Signature):
    """Analyze the problem structure."""
    problem = dspy.InputField()
    analysis = dspy.OutputField(desc="analysis of problem type and requirements")

class Step2Signature(dspy.Signature):
    """Break problem into solvable components."""
    problem = dspy.InputField()
    analysis = dspy.InputField()
    components = dspy.OutputField(desc="list of problem components to solve")

class Step3Signature(dspy.Signature):
    """Solve individual components."""
    problem = dspy.InputField()
    components = dspy.InputField()
    component_solutions = dspy.OutputField(desc="solutions for each component")

class SynthesisSignature(dspy.Signature):
    """Synthesize final answer from all steps."""
    problem = dspy.InputField()
    analysis = dspy.InputField()
    breakdown = dspy.InputField()
    solutions = dspy.InputField()
    final_answer = dspy.OutputField()
    reasoning = dspy.OutputField(desc="reasoning for the final answer")

# Usage
multi_hop = MultiHopReasoning()
result = multi_hop(problem="Design a system to reduce urban traffic congestion")

print("Analysis:", result.analysis)
print("Final Answer:", result.final_answer)
```

### Recursive Problem Decomposition

```python
class RecursiveSolver(dspy.Module):
    def __init__(self, max_depth=3):
        super().__init__()
        self.max_depth = max_depth

        self.decompose = dspy.Predict(DecompositionSignature)
        self.solve_base = dspy.Predict(BaseSolutionSignature)
        self.combine = dspy.Predict(CombinationSignature)

    def forward(self, problem, depth=0):
        # Base case: solve directly
        if depth >= self.max_depth:
            solution = self.solve_base(problem=problem)
            return dspy.Prediction(
                solution=solution.solution,
                type="base_case",
                depth=depth
            )

        # Recursive case: decompose and solve subproblems
        decomposition = self.decompose(problem=problem, depth=depth)

        if decomposition.should_decompose.lower() == "no":
            # Solve directly
            solution = self.solve_base(problem=problem)
            return dspy.Prediction(
                solution=solution.solution,
                type="base_case",
                depth=depth
            )

        # Recursively solve subproblems
        sub_solutions = []
        for subproblem in decomposition.subproblems:
            sub_result = self.forward(subproblem, depth + 1)
            sub_solutions.append(sub_result.solution)

        # Combine solutions
        combination = self.combine(
            original_problem=problem,
            subproblems=decomposition.subproblems,
            sub_solutions=sub_solutions
        )

        return dspy.Prediction(
            solution=combination.combined_solution,
            subproblems=decomposition.subproblems,
            sub_solutions=sub_solutions,
            type="recursive",
            depth=depth
        )

# Supporting signatures
class DecompositionSignature(dspy.Signature):
    """Decide whether to decompose problem and create subproblems."""
    problem = dspy.InputField()
    depth = dspy.InputField(desc="current recursion depth")
    should_decompose = dspy.OutputField(desc="yes or no")
    subproblems = dspy.OutputField(desc="list of subproblems if decomposing")

class BaseSolutionSignature(dspy.Signature):
    """Solve a problem that doesn't need decomposition."""
    problem = dspy.InputField()
    solution = dspy.OutputField()

class CombinationSignature(dspy.Signature):
    """Combine solutions from subproblems."""
    original_problem = dspy.InputField()
    subproblems = dspy.InputField()
    sub_solutions = dspy.InputField()
    combined_solution = dspy.OutputField()

# Usage
recursive_solver = RecursiveSolver(max_depth=3)
result = recursive_solver(problem="Build a recommendation system for an e-commerce site")

print(f"Solution type: {result.type}")
print(f"Recursion depth: {result.depth}")
print("Final solution:", result.solution)
```

## Tool Integration

### Function Calling with Tools

```python
class ToolUsingAgent(dspy.Module):
    def __init__(self, tools=None):
        super().__init__()

        self.tools = tools or {}
        self.reason = dspy.Predict(ReasoningSignature)
        self.act = dspy.Predict(ActionSignature)

    def forward(self, task):
        actions_taken = []
        observations = []

        # Maximum steps to prevent infinite loops
        max_steps = 5

        for step in range(max_steps):
            # Reason about what to do
            reasoning = self.reason(
                task=task,
                previous_actions=actions_taken,
                previous_observations=observations
            )

            # Decide on action
            action = self.act(
                task=task,
                reasoning=reasoning.reasoning,
                available_tools=list(self.tools.keys())
            )

            # Execute action if it's a tool call
            if action.action_type == "tool_call" and action.tool_name in self.tools:
                try:
                    tool_result = self.tools[action.tool_name](**action.tool_args)
                    observation = f"Tool {action.tool_name} returned: {tool_result}"
                except Exception as e:
                    observation = f"Tool {action.tool_name} failed: {str(e)}"

                actions_taken.append(f"Called {action.tool_name} with {action.tool_args}")
                observations.append(observation)

            elif action.action_type == "final_answer":
                # Task is complete
                return dspy.Prediction(
                    final_answer=action.final_answer,
                    actions_taken=actions_taken,
                    observations=observations,
                    steps_taken=step + 1
                )
            else:
                # Invalid action
                actions_taken.append(f"Invalid action: {action.action_type}")
                observations.append("Action was invalid")

        # Max steps reached
        return dspy.Prediction(
            final_answer="Could not complete task within step limit",
            actions_taken=actions_taken,
            observations=observations,
            steps_taken=max_steps
        )

# Tool signatures
class ReasoningSignature(dspy.Signature):
    """Reason about next action to take."""
    task = dspy.InputField()
    previous_actions = dspy.InputField()
    previous_observations = dspy.InputField()
    reasoning = dspy.OutputField(desc="reasoning about what to do next")

class ActionSignature(dspy.Signature):
    """Decide on specific action to take."""
    task = dspy.InputField()
    reasoning = dspy.InputField()
    available_tools = dspy.InputField()
    action_type = dspy.OutputField(desc="tool_call or final_answer")
    tool_name = dspy.OutputField(desc="name of tool to call", required=False)
    tool_args = dspy.OutputField(desc="arguments for tool call", required=False)
    final_answer = dspy.OutputField(desc="final answer if complete", required=False)

# Define tools
def search_web(query):
    """Mock web search tool"""
    return f"Search results for '{query}': [mock results]"

def calculate(expression):
    """Mock calculator tool"""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

def get_weather(city):
    """Mock weather tool"""
    return f"Weather in {city}: 72°F, Sunny"

# Create tool-using agent
tools = {
    "search_web": search_web,
    "calculate": calculate,
    "get_weather": get_weather
}

tool_agent = ToolUsingAgent(tools=tools)

# Use the agent
result = tool_agent(task="What's the weather in Paris and what's 15% of 200?")
print("Final answer:", result.final_answer)
print("Actions taken:", result.actions_taken)
```

### DSPy ReAct Pattern

```python
class ReActAgent(dspy.Module):
    def __init__(self, tools=None):
        super().__init__()

        self.tools = tools or {}
        self.react = dspy.Predict(ReActSignature)

    def forward(self, question):
        trajectory = ""
        max_steps = 5

        for step in range(max_steps):
            # Generate next action using ReAct
            result = self.react(
                question=question,
                trajectory=trajectory,
                available_tools=list(self.tools.keys())
            )

            action = result.action
            trajectory += f"Thought: {result.thought}\nAction: {action}\n"

            # Check if final answer
            if action.startswith("Final Answer:"):
                final_answer = action.replace("Final Answer:", "").strip()
                return dspy.Prediction(
                    final_answer=final_answer,
                    trajectory=trajectory,
                    steps=step + 1
                )

            # Execute tool
            tool_result = self._execute_tool(action)
            trajectory += f"Observation: {tool_result}\n"

        # Max steps reached
        return dspy.Prediction(
            final_answer="Could not find answer within step limit",
            trajectory=trajectory,
            steps=max_steps
        )

    def _execute_tool(self, action):
        """Parse and execute tool call"""
        try:
            # Parse action (simplified parsing)
            if "search_web[" in action:
                query = action.split("search_web[")[1].split("]")[0]
                return self.tools["search_web"](query)
            elif "calculate[" in action:
                expr = action.split("calculate[")[1].split("]")[0]
                return self.tools["calculate"](expr)
            elif "get_weather[" in action:
                city = action.split("get_weather[")[1].split("]")[0]
                return self.tools["get_weather"](city)
            else:
                return f"Unknown tool action: {action}"
        except Exception as e:
            return f"Tool execution failed: {str(e)}"

class ReActSignature(dspy.Signature):
    """Reason and act in one step."""
    question = dspy.InputField()
    trajectory = dspy.InputField(desc="previous thoughts, actions, and observations")
    available_tools = dspy.InputField()
    thought = dspy.OutputField(desc="reasoning about what to do")
    action = dspy.OutputField(desc="action to take or final answer")

# Create ReAct agent
react_agent = ReActAgent(tools=tools)
result = react_agent(question="What's 25% of 80 and is it sunny in London?")

print("Final answer:", result.final_answer)
print("Steps taken:", result.steps)
```

## Collaborative Multi-Agent Patterns

### Agent Teams with Specializations

```python
class AgentTeam(dspy.Module):
    def __init__(self):
        super().__init__()

        # Specialized agents
        self.researcher = dspy.Predict(ResearcherSignature)
        self.analyst = dspy.Predict(AnalystSignature)
        self.writer = dspy.Predict(WriterSignature)
        self.reviewer = dspy.Predict(ReviewerSignature)

        # Coordination
        self.coordinator = dspy.Predict(CoordinationSignature)

    def forward(self, task):
        # Initial coordination
        coordination = self.coordinator(task=task)

        # Parallel execution of specialized tasks
        research_result = self.researcher(
            task=task,
            focus_area=coordination.research_focus
        )

        analysis_result = self.analyst(
            task=task,
            research_data=research_result.findings
        )

        # Sequential writing based on analysis
        writing_result = self.writer(
            task=task,
            research=research_result.findings,
            analysis=analysis_result.insights
        )

        # Review and refinement
        review_result = self.reviewer(
            task=task,
            draft=writing_result.draft,
            research=research_result.findings,
            analysis=analysis_result.insights
        )

        return dspy.Prediction(
            research=findings_result.findings,
            analysis=analysis_result.insights,
            draft=writing_result.draft,
            final_output=review_result.final_version,
            feedback=review_result.feedback
        )

# Team member signatures
class ResearcherSignature(dspy.Signature):
    """Research specialist."""
    task = dspy.InputField()
    focus_area = dspy.InputField()
    findings = dspy.OutputField(desc="research findings and data")

class AnalystSignature(dspy.Signature):
    """Analysis specialist."""
    task = dspy.InputField()
    research_data = dspy.InputField()
    insights = dspy.OutputField(desc="key insights and analysis")

class WriterSignature(dspy.Signature):
    """Writing specialist."""
    task = dspy.InputField()
    research = dspy.InputField()
    analysis = dspy.InputField()
    draft = dspy.OutputField(desc="written content draft")

class ReviewerSignature(dspy.Signature):
    """Review specialist."""
    task = dspy.InputField()
    draft = dspy.InputField()
    research = dspy.InputField()
    analysis = dspy.InputField()
    final_version = dspy.OutputField(desc="reviewed and improved version")
    feedback = dspy.OutputField(desc="review feedback and suggestions")

class CoordinationSignature(dspy.Signature):
    """Team coordination."""
    task = dspy.InputField()
    research_focus = dspy.OutputField(desc="what to research")
    analysis_focus = dspy.OutputField(desc="what to analyze")
    writing_approach = dspy.OutputField(desc="how to structure the output")

# Usage
team = AgentTeam()
result = team(task="Write a report on the impact of AI on healthcare")

print("Final report:", result.final_output)
print("Research findings:", result.research)
```

### Debate and Consensus Patterns

```python
class DebateSystem(dspy.Module):
    def __init__(self, num_rounds=3):
        super().__init__()
        self.num_rounds = num_rounds

        # Debate participants
        self.proponent = dspy.Predict(DebateSignature)
        self.opponent = dspy.Predict(DebateSignature)
        self.moderator = dspy.Predict(ModeratorSignature)

    def forward(self, topic):
        debate_history = []

        # Initial positions
        proponent_initial = self.proponent(
            topic=topic,
            role="proponent",
            debate_history=[],
            round_number=0
        )

        opponent_initial = self.opponent(
            topic=topic,
            role="opponent",
            debate_history=[],
            round_number=0
        )

        debate_history.extend([
            f"Proponent: {proponent_initial.argument}",
            f"Opponent: {opponent_initial.argument}"
        ])

        # Debate rounds
        for round_num in range(1, self.num_rounds + 1):
            # Proponent responds
            proponent_response = self.proponent(
                topic=topic,
                role="proponent",
                debate_history=debate_history,
                round_number=round_num
            )

            # Opponent responds
            opponent_response = self.opponent(
                topic=topic,
                role="opponent",
                debate_history=debate_history + [f"Proponent: {proponent_response.argument}"],
                round_number=round_num
            )

            debate_history.extend([
                f"Proponent (Round {round_num}): {proponent_response.argument}",
                f"Opponent (Round {round_num}): {opponent_response.argument}"
            ])

        # Moderator summarizes and finds consensus
        moderation = self.moderator(
            topic=topic,
            debate_history=debate_history
        )

        return dspy.Prediction(
            debate_history=debate_history,
            proponent_final=moderation.proponent_position,
            opponent_final=moderation.opponent_position,
            consensus=moderation.consensus,
            key_agreements=moderation.key_agreements,
            remaining_differences=moderation.remaining_differences
        )

# Debate signatures
class DebateSignature(dspy.Signature):
    """Debate participant."""
    topic = dspy.InputField()
    role = dspy.InputField(desc="proponent or opponent")
    debate_history = dspy.InputField(desc="previous debate exchanges")
    round_number = dspy.InputField()
    argument = dspy.OutputField(desc="argument or response for this round")

class ModeratorSignature(dspy.Signature):
    """Debate moderator and consensus finder."""
    topic = dspy.InputField()
    debate_history = dspy.InputField()
    proponent_position = dspy.OutputField(desc="final proponent position")
    opponent_position = dspy.OutputField(desc="final opponent position")
    consensus = dspy.OutputField(desc="agreed-upon points")
    key_agreements = dspy.OutputField(desc="main areas of agreement")
    remaining_differences = dspy.OutputField(desc="points of disagreement")

# Usage
debate_system = DebateSystem(num_rounds=2)
result = debate_system(topic="Should AI be regulated more strictly?")

print("Consensus:", result.consensus)
print("Key agreements:", result.key_agreements)
```

## Self-Improving Systems

### Meta-Learning Patterns

```python
class SelfImprovingAgent(dspy.Module):
    def __init__(self):
        super().__init__()

        # Core capabilities
        self.solve = dspy.Predict(ProblemSolvingSignature)

        # Meta-learning components
        self.evaluate = dspy.Predict(EvaluationSignature)
        self.improve = dspy.Predict(ImprovementSignature)

        # Experience storage
        self.experiences = []

    def forward(self, problem):
        # Initial solution attempt
        initial_solution = self.solve(problem=problem)

        # Evaluate the solution
        evaluation = self.evaluate(
            problem=problem,
            solution=initial_solution.solution
        )

        # Store experience
        experience = {
            "problem": problem,
            "solution": initial_solution.solution,
            "quality_score": evaluation.quality_score,
            "improvement_suggestions": evaluation.suggestions
        }
        self.experiences.append(experience)

        # Check if improvement is needed
        if evaluation.quality_score < 0.7:
            # Generate improvement
            improvement = self.improve(
                problem=problem,
                current_solution=initial_solution.solution,
                evaluation=evaluation.feedback,
                past_experiences=self.experiences[-5:]  # Last 5 experiences
            )

            # Apply improvement
            improved_solution = self.solve(
                problem=problem,
                improvement_guidance=improvement.improvement_guidance
            )

            return dspy.Prediction(
                final_solution=improved_solution.solution,
                initial_solution=initial_solution.solution,
                improvement_applied=True,
                quality_score=evaluation.quality_score,
                improvement_reason=improvement.reasoning
            )

        return dspy.Prediction(
            final_solution=initial_solution.solution,
            improvement_applied=False,
            quality_score=evaluation.quality_score
        )

# Meta-learning signatures
class ProblemSolvingSignature(dspy.Signature):
    """Solve problems, optionally using improvement guidance."""
    problem = dspy.InputField()
    improvement_guidance = dspy.InputField(required=False)
    solution = dspy.OutputField()

class EvaluationSignature(dspy.Signature):
    """Evaluate solution quality."""
    problem = dspy.InputField()
    solution = dspy.InputField()
    quality_score = dspy.OutputField(desc="score from 0.0 to 1.0")
    feedback = dspy.OutputField(desc="detailed feedback")
    suggestions = dspy.OutputField(desc="improvement suggestions")

class ImprovementSignature(dspy.Signature):
    """Generate improvement guidance."""
    problem = dspy.InputField()
    current_solution = dspy.InputField()
    evaluation = dspy.InputField()
    past_experiences = dspy.InputField()
    improvement_guidance = dspy.OutputField(desc="how to improve the solution")
    reasoning = dspy.OutputField(desc="reasoning for the improvement approach")

# Usage
self_improver = SelfImprovingAgent()
result = self_improver(problem="Design a more efficient sorting algorithm")

print(f"Improvement applied: {result.improvement_applied}")
print(f"Quality score: {result.quality_score}")
print("Final solution:", result.final_solution)
```

### Adaptive Behavior Patterns

```python
class AdaptiveAgent(dspy.Module):
    def __init__(self):
        super().__init__()

        # Multiple behavior modes
        self.creative_mode = dspy.Predict(CreativeSignature)
        self.analytical_mode = dspy.Predict(AnalyticalSignature)
        self.practical_mode = dspy.Predict(PracticalSignature)

        # Mode selection
        self.select_mode = dspy.Predict(ModeSelectionSignature)

        # Performance tracking
        self.performance_history = {}

    def forward(self, task):
        # Select appropriate mode based on task and history
        mode_selection = self.select_mode(
            task=task,
            performance_history=self.performance_history
        )

        selected_mode = mode_selection.selected_mode

        # Execute with selected mode
        if selected_mode == "creative":
            result = self.creative_mode(task=task)
        elif selected_mode == "analytical":
            result = self.analytical_mode(task=task)
        elif selected_mode == "practical":
            result = self.practical_mode(task=task)
        else:
            # Default fallback
            result = self.practical_mode(task=task)

        # Track performance for future adaptation
        task_type = mode_selection.task_type
        if task_type not in self.performance_history:
            self.performance_history[task_type] = []

        self.performance_history[task_type].append({
            "mode": selected_mode,
            "task": task,
            "result_quality": 0.8  # Would be evaluated
        })

        return dspy.Prediction(
            solution=result.solution,
            mode_used=selected_mode,
            reasoning=mode_selection.reasoning
        )

# Adaptive signatures
class ModeSelectionSignature(dspy.Signature):
    """Select the best approach for a task."""
    task = dspy.InputField()
    performance_history = dspy.InputField()
    selected_mode = dspy.OutputField(desc="creative, analytical, or practical")
    task_type = dspy.OutputField(desc="categorization of task type")
    reasoning = dspy.OutputField(desc="reasoning for mode selection")

class CreativeSignature(dspy.Signature):
    """Creative problem solving."""
    task = dspy.InputField()
    solution = dspy.OutputField(desc="innovative, creative solution")

class AnalyticalSignature(dspy.Signature):
    """Analytical problem solving."""
    task = dspy.InputField()
    solution = dspy.OutputField(desc="logical, step-by-step analysis")

class PracticalSignature(dspy.Signature):
    """Practical problem solving."""
    task = dspy.InputField()
    solution = dspy.OutputField(desc="practical, implementable solution")

# Usage
adaptive_agent = AdaptiveAgent()
result = adaptive_agent(task="Come up with a new marketing strategy for a tech startup")

print(f"Mode used: {result.mode_used}")
print("Solution:", result.solution)
```

## Summary

In this chapter, we've explored:

- **Multi-Hop Reasoning**: Chain-of-thought with multiple steps, recursive decomposition
- **Tool Integration**: Function calling, ReAct patterns, tool-using agents
- **Collaborative Patterns**: Agent teams, debate systems, consensus finding
- **Self-Improving Systems**: Meta-learning, adaptive behavior, experience-based improvement

These advanced patterns enable DSPy programs to handle complex, multi-step reasoning tasks that go far beyond simple question-answering.

## Key Takeaways

1. **Multi-Hop Reasoning**: Break complex problems into manageable steps
2. **Tool Integration**: Extend capabilities with external tools and APIs
3. **Collaborative Agents**: Multiple agents working together for better results
4. **Self-Improvement**: Systems that learn and adapt from experience
5. **Adaptive Behavior**: Dynamic selection of strategies based on context

Next, we'll explore **evaluation and metrics** - systematic evaluation and custom metrics for DSPy programs.

---

**Ready for the next chapter?** [Chapter 7: Evaluation & Metrics](07-evaluation.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*