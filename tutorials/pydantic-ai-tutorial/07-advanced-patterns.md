---
layout: default
title: "Pydantic AI Tutorial - Chapter 7: Advanced Patterns"
nav_order: 7
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 7: Advanced Patterns & Multi-Step Workflows

Welcome to **Chapter 7: Advanced Patterns & Multi-Step Workflows**. In this part of **Pydantic AI Tutorial: Type-Safe AI Agent Development**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master complex agent workflows, dynamic reasoning patterns, and sophisticated interaction paradigms for advanced AI applications.

## Dynamic Agent Composition

### Agent Factory Pattern

```python
from typing import Dict, Any, Type, Optional
from pydantic_ai import Agent
from pydantic import BaseModel

class AgentFactory:
    """Factory for creating specialized agents dynamically."""

    def __init__(self):
        self.agent_templates: Dict[str, Dict[str, Any]] = {}
        self.created_agents: Dict[str, Agent] = {}

    def register_template(self, name: str, template: Dict[str, Any]):
        """Register an agent template."""
        self.agent_templates[name] = template

    def create_agent(self, template_name: str, customizations: Dict[str, Any] = None) -> Agent:
        """Create agent from template with customizations."""

        if template_name not in self.agent_templates:
            raise ValueError(f"Template {template_name} not found")

        template = self.agent_templates[template_name].copy()
        customizations = customizations or {}

        # Apply customizations
        for key, value in customizations.items():
            if key in template:
                if isinstance(template[key], dict) and isinstance(value, dict):
                    template[key].update(value)
                else:
                    template[key] = value
            else:
                template[key] = value

        # Create agent
        agent = Agent(**template)

        # Store reference
        agent_id = f"{template_name}_{id(agent)}"
        self.created_agents[agent_id] = agent

        return agent

    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about created agents."""
        template_usage = {}

        for agent_id, agent in self.created_agents.items():
            template_name = agent_id.split('_')[0]
            template_usage[template_name] = template_usage.get(template_name, 0) + 1

        return {
            "total_agents": len(self.created_agents),
            "template_usage": template_usage,
            "active_agents": len([a for a in self.created_agents.values() if hasattr(a, '_active')])
        }

# Create agent factory
factory = AgentFactory()

# Register agent templates
factory.register_template("code_assistant", {
    "model": "openai:gpt-4",
    "system_prompt": "You are an expert software developer. Provide clear, correct code solutions with explanations.",
    "result_type": None
})

factory.register_template("data_analyst", {
    "model": "openai:gpt-4",
    "system_prompt": "You are a data analysis expert. Provide insights from data with clear explanations.",
    "result_type": None
})

factory.register_template("creative_writer", {
    "model": "anthropic:claude-3-sonnet-20240229",
    "system_prompt": "You are a creative writer. Craft engaging, imaginative content.",
    "result_type": None
})

factory.register_template("math_tutor", {
    "model": "groq:mixtral-8x7b-32768",
    "system_prompt": "You are a patient math tutor. Explain concepts clearly with examples.",
    "result_type": None
})

# Create agents with customizations
code_agent = factory.create_agent("code_assistant", {
    "system_prompt": "You are an expert Python developer specializing in web applications."
})

creative_agent = factory.create_agent("creative_writer", {
    "model": "openai:gpt-4",  # Override model
    "system_prompt": "You are a creative writer specializing in science fiction."
})

print("🎯 Created Agents:")
print(f"Code Agent: {code_agent.model}")
print(f"Creative Agent: {creative_agent.model}")

# Test agents
code_result = code_agent.run_sync("Write a Python function to validate email addresses")
creative_result = creative_agent.run_sync("Write a short sci-fi story about AI consciousness")

print("
📝 Agent Results:")
print(f"Code: {len(code_result.data)} chars")
print(f"Creative: {len(creative_result.data)} chars")

print("
📊 Factory Stats:")
stats = factory.get_agent_stats()
for key, value in stats.items():
    print(f"{key}: {value}")
```

### Dynamic Agent Routing

```python
from typing import List, Dict, Any, Callable
import re

class IntelligentRouter:
    """Router that dynamically selects agents based on query analysis."""

    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        self.routing_rules: List[Dict[str, Any]] = []
        self.performance_history: Dict[str, int] = {}

    def add_routing_rule(self, condition: Callable[[str], bool],
                        agent_template: str, priority: int = 1):
        """Add a routing rule."""

        self.routing_rules.append({
            "condition": condition,
            "agent_template": agent_template,
            "priority": priority
        })

        # Sort by priority (higher priority first)
        self.routing_rules.sort(key=lambda x: x["priority"], reverse=True)

    def analyze_query(self, query: str) -> str:
        """Analyze query to determine appropriate agent."""

        # Check routing rules
        for rule in self.routing_rules:
            if rule["condition"](query):
                agent_template = rule["agent_template"]
                self.performance_history[agent_template] = self.performance_history.get(agent_template, 0) + 1
                return agent_template

        # Default fallback
        return "general_assistant"

    def get_agent_for_query(self, query: str) -> Agent:
        """Get appropriate agent for query."""

        agent_template = self.analyze_query(query)

        # Create agent with query-specific customizations
        customizations = self._get_query_customizations(query)

        agent = self.agent_factory.create_agent(agent_template, customizations)

        return agent

    def _get_query_customizations(self, query: str) -> Dict[str, Any]:
        """Get query-specific customizations."""

        customizations = {}

        # Language-specific customizations for code queries
        if "python" in query.lower():
            customizations["system_prompt"] = "You are a Python expert. Focus on Pythonic solutions."
        elif "javascript" in query.lower():
            customizations["system_prompt"] = "You are a JavaScript expert. Use modern ES6+ features."

        # Complexity-based customizations
        if len(query) > 200:
            customizations["model"] = "openai:gpt-4"  # Use more capable model
        elif len(query) < 50:
            customizations["model"] = "groq:mixtral-8x7b-32768"  # Use faster model

        return customizations

    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            "total_queries": sum(self.performance_history.values()),
            "agent_usage": self.performance_history,
            "routing_rules": len(self.routing_rules)
        }

# Create intelligent router
router = IntelligentRouter(factory)

# Add routing rules
def is_code_query(query: str) -> bool:
    code_keywords = ["function", "class", "code", "program", "algorithm", "script"]
    return any(keyword in query.lower() for keyword in code_keywords)

def is_math_query(query: str) -> bool:
    math_keywords = ["calculate", "equation", "solve", "math", "algebra", "geometry"]
    return any(keyword in query.lower() for keyword in math_keywords)

def is_creative_query(query: str) -> bool:
    creative_keywords = ["write", "story", "poem", "create", "design", "imagine"]
    return any(keyword in query.lower() for keyword in creative_keywords)

def is_data_query(query: str) -> bool:
    data_keywords = ["analyze", "data", "statistics", "chart", "graph", "trend"]
    return any(keyword in query.lower() for keyword in data_keywords)

router.add_routing_rule(is_code_query, "code_assistant", priority=3)
router.add_routing_rule(is_math_query, "math_tutor", priority=3)
router.add_routing_rule(is_creative_query, "creative_writer", priority=2)
router.add_routing_rule(is_data_query, "data_analyst", priority=2)

# Test intelligent routing
test_queries = [
    "Write a Python function to sort a list",
    "Calculate the area of a circle with radius 5",
    "Write a short story about time travel",
    "Analyze this sales data: [100, 150, 200, 180, 220]",
    "Hello, how are you today?"
]

print("🎯 Intelligent Routing Test:")
for query in test_queries:
    agent = router.get_agent_for_query(query)
    print(f"Query: {query[:40]}...")
    print(f"  Routed to: {agent.model}")
    print(f"  Agent type: {type(agent).__name__}")
    print()

print("📊 Routing Statistics:")
stats = router.get_routing_stats()
for key, value in stats.items():
    print(f"{key}: {value}")
```

## Chain-of-Thought Reasoning

### Structured Reasoning Chains

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent

class ReasoningStep(BaseModel):
    step_number: int
    thought: str
    action: str
    observation: str
    confidence: float = Field(ge=0.0, le=1.0)

class ChainOfThoughtResult(BaseModel):
    problem: str
    reasoning_chain: List[ReasoningStep]
    final_answer: str
    confidence: float

class ChainOfThoughtAgent(Agent):
    """Agent implementing chain-of-thought reasoning."""

    def __init__(self, max_steps: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.max_steps = max_steps

    async def reason_step_by_step(self, problem: str) -> ChainOfThoughtResult:
        """Execute chain-of-thought reasoning."""

        reasoning_chain = []
        current_thought = f"I need to solve: {problem}"

        for step in range(self.max_steps):
            # Generate next reasoning step
            step_prompt = self._create_reasoning_prompt(
                problem, current_thought, reasoning_chain, step
            )

            # Get structured reasoning step
            step_result = await self.run(step_prompt)

            # Parse the response (simplified - in practice you'd use structured output)
            try:
                # Extract thought, action, observation from response
                thought, action, observation, confidence = self._parse_step_response(step_result.data)

                reasoning_step = ReasoningStep(
                    step_number=step + 1,
                    thought=thought,
                    action=action,
                    observation=observation,
                    confidence=confidence
                )

                reasoning_chain.append(reasoning_step)

                # Check if we should stop
                if confidence > 0.9 or "final answer" in observation.lower():
                    break

                # Update current thought
                current_thought = observation

            except Exception as e:
                print(f"Error in reasoning step {step + 1}: {e}")
                break

        # Generate final answer
        final_answer = await self._generate_final_answer(problem, reasoning_chain)

        return ChainOfThoughtResult(
            problem=problem,
            reasoning_chain=reasoning_chain,
            final_answer=final_answer,
            confidence=sum(step.confidence for step in reasoning_chain) / len(reasoning_chain)
        )

    def _create_reasoning_prompt(self, problem: str, current_thought: str,
                                reasoning_chain: List[ReasoningStep], step: int) -> str:
        """Create prompt for next reasoning step."""

        chain_summary = "\n".join([
            f"Step {s.step_number}: {s.thought[:50]}... -> {s.action[:30]}... -> {s.observation[:50]}..."
            for s in reasoning_chain[-2:]  # Last 2 steps for context
        ])

        prompt = f"""
You are solving this problem using step-by-step reasoning: {problem}

Current thought: {current_thought}

Previous reasoning steps:
{chain_summary}

For step {step + 1}, provide:
1. Your current thought process
2. What action you'll take
3. Your observation/result
4. Confidence level (0-1)

Format your response as:
Thought: [your thinking]
Action: [what you'll do]
Observation: [result of action]
Confidence: [0.0-1.0]
        """.strip()

        return prompt

    def _parse_step_response(self, response: str) -> tuple[str, str, str, float]:
        """Parse step response into components."""

        lines = response.strip().split('\n')
        thought = ""
        action = ""
        observation = ""
        confidence = 0.5

        for line in lines:
            line = line.strip()
            if line.startswith("Thought:"):
                thought = line[8:].strip()
            elif line.startswith("Action:"):
                action = line[7:].strip()
            elif line.startswith("Observation:"):
                observation = line[13:].strip()
            elif line.startswith("Confidence:"):
                try:
                    confidence = float(line[11:].strip())
                    confidence = max(0.0, min(1.0, confidence))  # Clamp to valid range
                except:
                    pass

        return thought, action, observation, confidence

    async def _generate_final_answer(self, problem: str, reasoning_chain: List[ReasoningStep]) -> str:
        """Generate final answer from reasoning chain."""

        chain_summary = "\n".join([
            f"Step {step.step_number}: {step.observation}"
            for step in reasoning_chain
        ])

        final_prompt = f"""
Based on this reasoning chain, provide a final answer to: {problem}

Reasoning process:
{chain_summary}

Final Answer:
        """.strip()

        final_result = await self.run(final_prompt)
        return final_result.data

# Create chain-of-thought agent
cot_agent = ChainOfThoughtAgent(
    model='openai:gpt-4',
    max_steps=4
)

# Test chain-of-thought reasoning
reasoning_problem = """
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball.
How much does the ball cost?
"""

async def test_chain_of_thought():
    """Test chain-of-thought reasoning."""

    print("🧠 Testing Chain-of-Thought Reasoning:")
    print(f"Problem: {reasoning_problem.strip()}")

    result = await cot_agent.reason_step_by_step(reasoning_problem)

    print(f"\nReasoning Steps: {len(result.reasoning_chain)}")
    print(f"Final Confidence: {result.confidence:.2f}")
    print(f"Final Answer: {result.final_answer}")

    print("\nDetailed Reasoning Chain:")
    for step in result.reasoning_chain:
        print(f"Step {step.step_number}:")
        print(f"  Thought: {step.thought}")
        print(f"  Action: {step.action}")
        print(f"  Observation: {step.observation}")
        print(f"  Confidence: {step.confidence:.2f}")
        print()

# Run chain-of-thought test
asyncio.run(test_chain_of_thought())
```

## Multi-Agent Collaboration

### Agent Orchestration Framework

```python
from typing import List, Dict, Any, Optional
from enum import Enum
import asyncio

class CollaborationMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"

class AgentOrchestrator:
    """Orchestrate multiple agents for complex tasks."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.collaboration_history: List[Dict[str, Any]] = []

    def register_agent(self, name: str, agent: Agent, capabilities: List[str] = None):
        """Register an agent with capabilities."""
        self.agents[name] = {
            "agent": agent,
            "capabilities": capabilities or [],
            "performance_score": 1.0
        }

    def find_agents_for_task(self, task_requirements: List[str]) -> List[str]:
        """Find agents suitable for task requirements."""
        suitable_agents = []

        for name, agent_info in self.agents.items():
            agent_caps = agent_info["capabilities"]
            if any(req in agent_caps for req in task_requirements):
                suitable_agents.append(name)

        # Sort by performance score
        suitable_agents.sort(
            key=lambda x: self.agents[x]["performance_score"],
            reverse=True
        )

        return suitable_agents[:3]  # Return top 3

    async def execute_collaborative_task(self, task: str, mode: CollaborationMode = CollaborationMode.SEQUENTIAL) -> Dict[str, Any]:
        """Execute task with multiple agents collaborating."""

        collaboration_session = {
            "task": task,
            "mode": mode.value,
            "start_time": asyncio.get_event_loop().time(),
            "agent_contributions": [],
            "final_result": None
        }

        print(f"🤝 Starting {mode.value} collaboration for: {task[:50]}...")

        if mode == CollaborationMode.SEQUENTIAL:
            result = await self._execute_sequential(task)
        elif mode == CollaborationMode.PARALLEL:
            result = await self._execute_parallel(task)
        elif mode == CollaborationMode.HIERARCHICAL:
            result = await self._execute_hierarchical(task)

        collaboration_session["final_result"] = result
        collaboration_session["end_time"] = asyncio.get_event_loop().time()
        collaboration_session["duration"] = collaboration_session["end_time"] - collaboration_session["start_time"]

        self.collaboration_history.append(collaboration_session)

        return collaboration_session

    async def _execute_sequential(self, task: str) -> str:
        """Execute task sequentially through agents."""

        # Break task into subtasks
        subtasks = await self._decompose_task(task)

        current_result = ""

        for subtask in subtasks:
            agent_name = self.find_agents_for_task([subtask["type"]])[0]
            agent = self.agents[agent_name]["agent"]

            # Enhance prompt with context
            enhanced_prompt = f"""
Main task: {task}
Current progress: {current_result}

Subtask: {subtask["description"]}

Build upon previous work to complete this subtask.
            """.strip()

            result = await agent.run(enhanced_prompt)
            current_result += f"\n\n{subtask['description']}:\n{result.data}"

            # Record contribution
            self._record_contribution(agent_name, subtask["description"], result.data)

        return current_result

    async def _execute_parallel(self, task: str) -> str:
        """Execute task components in parallel."""

        subtasks = await self._decompose_task(task)

        # Execute subtasks concurrently
        parallel_tasks = []

        for subtask in subtasks:
            agent_name = self.find_agents_for_task([subtask["type"]])[0]
            agent = self.agents[agent_name]["agent"]

            task_coro = self._execute_subtask(agent, agent_name, subtask, task)
            parallel_tasks.append(task_coro)

        results = await asyncio.gather(*parallel_tasks)

        # Combine results
        combined_result = "\n\n".join(results)

        # Final synthesis
        synthesis_agent = self.agents["synthesizer"]["agent"]
        final_result = await synthesis_agent.run(f"""
Synthesize these parallel contributions into a coherent final result:

Task: {task}

Contributions:
{combined_result}

Provide a unified, well-structured final answer.
        """)

        return final_result.data

    async def _execute_hierarchical(self, task: str) -> str:
        """Execute task with hierarchical agent coordination."""

        # Coordinator agent breaks down task
        coordinator = self.agents["coordinator"]["agent"]

        breakdown = await coordinator.run(f"""
Break down this complex task into coordinated subtasks: {task}

Identify:
1. Key phases or components
2. Which types of specialists are needed for each
3. Dependencies between subtasks
4. Coordination requirements

Provide a structured breakdown.
        """)

        # Parse breakdown and execute hierarchically
        # (Simplified - in practice, you'd parse the breakdown properly)
        return await self._execute_sequential_with_dependencies(task, breakdown.data)

    async def _decompose_task(self, task: str) -> List[Dict[str, Any]]:
        """Decompose task into subtasks."""

        decomposer = self.agents["decomposer"]["agent"]

        decomposition = await decomposer.run(f"""
Decompose this task into 3-5 logical subtasks: {task}

For each subtask, specify:
- Description
- Type (research, analysis, writing, coding, etc.)
- Dependencies (if any)

Format as a clear list.
        """)

        # Parse decomposition (simplified)
        subtasks = [
            {"description": "Research the topic thoroughly", "type": "research"},
            {"description": "Analyze findings and extract insights", "type": "analysis"},
            {"description": "Create final deliverable", "type": "writing"}
        ]

        return subtasks

    async def _execute_subtask(self, agent: Agent, agent_name: str, subtask: Dict[str, Any], main_task: str) -> str:
        """Execute a single subtask."""

        result = await agent.run(f"""
Main task: {main_task}

Your subtask: {subtask["description"]}
Type: {subtask["type"]}

Provide your contribution to this subtask.
        """)

        self._record_contribution(agent_name, subtask["description"], result.data)

        return f"**{agent_name}** ({subtask['type']}): {result.data}"

    def _record_contribution(self, agent_name: str, subtask: str, result: str):
        """Record agent contribution for performance tracking."""

        contribution = {
            "agent": agent_name,
            "subtask": subtask,
            "result_length": len(result),
            "timestamp": asyncio.get_event_loop().time()
        }

        # Update performance score
        if len(result) > 100:  # Simple quality metric
            self.agents[agent_name]["performance_score"] *= 1.01  # Small boost
        else:
            self.agents[agent_name]["performance_score"] *= 0.99  # Small penalty

# Create orchestrator and register agents
orchestrator = AgentOrchestrator()

# Register agents with capabilities
orchestrator.register_agent("researcher", Agent('openai:gpt-4'), ["research", "information_gathering"])
orchestrator.register_agent("analyst", Agent('anthropic:claude-3-sonnet-20240229'), ["analysis", "insights"])
orchestrator.register_agent("writer", Agent('google:gemini-1.5-pro'), ["writing", "content_creation"])
orchestrator.register_agent("decomposer", Agent('groq:mixtral-8x7b-32768'), ["task_decomposition"])
orchestrator.register_agent("synthesizer", Agent('openai:gpt-4'), ["synthesis", "coordination"])

async def test_agent_collaboration():
    """Test multi-agent collaboration modes."""

    complex_task = """
    Create a comprehensive business plan for a sustainable energy startup.
    Include market analysis, technical approach, financial projections,
    and go-to-market strategy.
    """

    print("🎯 Testing Multi-Agent Collaboration:")

    # Test sequential collaboration
    print("\n📋 Sequential Collaboration:")
    sequential_result = await orchestrator.execute_collaborative_task(
        complex_task, CollaborationMode.SEQUENTIAL
    )

    print(f"Duration: {sequential_result['duration']:.2f}s")
    print(f"Agents involved: {len(sequential_result['agent_contributions'])}")

    # Test parallel collaboration
    print("\n⚡ Parallel Collaboration:")
    parallel_result = await orchestrator.execute_collaborative_task(
        complex_task, CollaborationMode.PARALLEL
    )

    print(f"Duration: {parallel_result['duration']:.2f}s")
    print(f"Agents involved: {len(parallel_result['agent_contributions'])}")

    # Compare performance
    speedup = sequential_result['duration'] / parallel_result['duration']
    print(f"\n🚀 Parallel speedup: {speedup:.2f}x")

    # Show final results
    print(f"\n📄 Sequential result length: {len(sequential_result['final_result'])} chars")
    print(f"📄 Parallel result length: {len(parallel_result['final_result'])} chars")

# Run collaboration tests
asyncio.run(test_agent_collaboration())
```

## Self-Improving Systems

### Learning from Feedback

```python
from typing import Dict, List, Any, Optional
from collections import defaultdict
import json

class SelfImprovingAgent(Agent):
    """Agent that learns and improves from feedback."""

    def __init__(self, learning_file: str = "agent_learning.json", **kwargs):
        super().__init__(**kwargs)
        self.learning_file = learning_file
        self.feedback_history: List[Dict[str, Any]] = []
        self.patterns_learned: Dict[str, Dict[str, Any]] = {}
        self.performance_metrics: Dict[str, float] = defaultdict(float)

        self._load_learning_data()

    def _load_learning_data(self):
        """Load learned patterns and feedback."""
        try:
            with open(self.learning_file, 'r') as f:
                data = json.load(f)
                self.feedback_history = data.get("feedback_history", [])
                self.patterns_learned = data.get("patterns_learned", {})
                self.performance_metrics.update(data.get("performance_metrics", {}))
        except FileNotFoundError:
            # Initialize with empty learning data
            pass

    def _save_learning_data(self):
        """Save learned patterns and feedback."""
        data = {
            "feedback_history": self.feedback_history[-100:],  # Keep last 100
            "patterns_learned": self.patterns_learned,
            "performance_metrics": dict(self.performance_metrics)
        }

        with open(self.learning_file, 'w') as f:
            json.dump(data, f, indent=2)

    async def run_with_learning(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run with learning and improvement capabilities."""

        # Analyze query and retrieve relevant patterns
        relevant_patterns = self._find_relevant_patterns(prompt)

        # Enhance prompt with learned patterns
        enhanced_prompt = self._enhance_prompt_with_patterns(prompt, relevant_patterns)

        # Execute with enhanced context
        result = await self.run(enhanced_prompt)

        # Store for potential feedback
        execution_record = {
            "prompt": prompt,
            "enhanced_prompt": enhanced_prompt,
            "result": result.data,
            "patterns_used": list(relevant_patterns.keys()),
            "timestamp": asyncio.get_event_loop().time(),
            "feedback_pending": True
        }

        self.feedback_history.append(execution_record)

        return {
            "result": result.data,
            "patterns_applied": len(relevant_patterns),
            "execution_record": execution_record
        }

    def provide_feedback(self, execution_record: Dict[str, Any], rating: float, comments: str = ""):
        """Provide feedback on execution to enable learning."""

        execution_record["feedback"] = {
            "rating": rating,  # 1.0 to 5.0
            "comments": comments,
            "timestamp": asyncio.get_event_loop().time()
        }
        execution_record["feedback_pending"] = False

        # Learn from feedback
        self._learn_from_feedback(execution_record)

        # Update performance metrics
        self.performance_metrics["total_feedback"] += 1
        self.performance_metrics["average_rating"] = (
            (self.performance_metrics["average_rating"] * (self.performance_metrics["total_feedback"] - 1)) + rating
        ) / self.performance_metrics["total_feedback"]

        self._save_learning_data()

    def _find_relevant_patterns(self, prompt: str) -> Dict[str, Dict[str, Any]]:
        """Find patterns relevant to the current prompt."""

        relevant_patterns = {}

        prompt_lower = prompt.lower()

        for pattern_name, pattern_data in self.patterns_learned.items():
            # Check if pattern keywords match prompt
            keywords = pattern_data.get("keywords", [])
            if any(keyword in prompt_lower for keyword in keywords):
                relevant_patterns[pattern_name] = pattern_data

        return relevant_patterns

    def _enhance_prompt_with_patterns(self, prompt: str, patterns: Dict[str, Dict[str, Any]]) -> str:
        """Enhance prompt with learned patterns."""

        if not patterns:
            return prompt

        enhancements = []

        for pattern_name, pattern_data in patterns.items():
            if pattern_data.get("successful", False):
                enhancement = pattern_data.get("enhancement_template", "")
                if enhancement:
                    enhancements.append(enhancement)

        if enhancements:
            enhanced_prompt = f"""
{prompt}

Based on successful past approaches:
{chr(10).join(f"- {enh}" for enh in enhancements[:3])}

Apply these insights to provide an excellent response.
            """.strip()
            return enhanced_prompt

        return prompt

    def _learn_from_feedback(self, execution_record: Dict[str, Any]):
        """Learn from feedback to improve future responses."""

        feedback = execution_record.get("feedback", {})
        rating = feedback.get("rating", 3.0)

        if rating >= 4.0:  # Successful execution
            # Extract successful patterns
            prompt = execution_record["prompt"]
            result = execution_record["result"]

            # Create pattern from successful execution
            pattern_name = f"success_pattern_{len(self.patterns_learned)}"

            self.patterns_learned[pattern_name] = {
                "keywords": self._extract_keywords(prompt),
                "enhancement_template": f"Use approach similar to: {result[:100]}...",
                "successful": True,
                "rating": rating,
                "created_from": execution_record["timestamp"]
            }

        elif rating <= 2.0:  # Unsuccessful execution
            # Learn what to avoid
            prompt = execution_record["prompt"]

            avoid_pattern = f"avoid_pattern_{len(self.patterns_learned)}"
            self.patterns_learned[avoid_pattern] = {
                "keywords": self._extract_keywords(prompt),
                "avoid_approach": f"Avoid approach that led to: {feedback.get('comments', 'poor results')}",
                "successful": False,
                "rating": rating
            }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for pattern matching."""

        # Simple keyword extraction (could be enhanced with NLP)
        words = text.lower().split()
        keywords = []

        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 3]

        # Get most frequent meaningful words
        from collections import Counter
        word_counts = Counter(meaningful_words)
        keywords = [word for word, count in word_counts.most_common(5)]

        return keywords

    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning and performance statistics."""

        successful_patterns = len([p for p in self.patterns_learned.values() if p.get("successful", False)])
        unsuccessful_patterns = len([p for p in self.patterns_learned.values() if not p.get("successful", False)])

        return {
            "total_patterns_learned": len(self.patterns_learned),
            "successful_patterns": successful_patterns,
            "unsuccessful_patterns": unsuccessful_patterns,
            "total_feedback": self.performance_metrics["total_feedback"],
            "average_rating": self.performance_metrics["average_rating"],
            "learning_efficiency": successful_patterns / max(1, len(self.patterns_learned))
        }

# Create self-improving agent
learning_agent = SelfImprovingAgent(
    model='openai:gpt-4',
    learning_file="agent_learning.json"
)

async def test_self_improvement():
    """Test self-improving agent capabilities."""

    test_prompts = [
        "Explain machine learning in simple terms",
        "Write a Python function to calculate fibonacci numbers",
        "Analyze the benefits of renewable energy",
        "Create a recipe for chocolate chip cookies"
    ]

    print("🧠 Testing Self-Improving Agent:")

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🎯 Test {i}: {prompt[:40]}...")

        # Execute with learning
        result = await learning_agent.run_with_learning(prompt)

        print(f"Patterns applied: {result['patterns_applied']}")
        print(f"Response length: {len(result['result'])} chars")

        # Simulate feedback (in practice, this would come from users)
        rating = 4.0 if len(result['result']) > 100 else 3.0  # Simple quality metric
        learning_agent.provide_feedback(result['execution_record'], rating, "Good response")

        print(f"Feedback provided: {rating}/5.0")

    # Show learning statistics
    stats = learning_agent.get_learning_stats()
    print("
📊 Learning Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")

    print(f"\nLearned patterns: {stats['total_patterns_learned']}")
    print(f"Learning efficiency: {stats['learning_efficiency']:.1%}")

# Run self-improvement test
asyncio.run(test_self_improvement())
```

This advanced patterns chapter demonstrates sophisticated agent architectures including dynamic composition, chain-of-thought reasoning, multi-agent collaboration, and self-improving systems that learn from feedback and experience. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `print`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Advanced Patterns & Multi-Step Workflows` as an operating subsystem inside **Pydantic AI Tutorial: Type-Safe AI Agent Development**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `Dict`, `task` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Advanced Patterns & Multi-Step Workflows` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/pydantic/pydantic-ai)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Error Handling, Retry Mechanisms & Recovery](06-error-handling.md)
- [Next Chapter: Chapter 8: Production Deployment & Scaling Pydantic AI Systems](08-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
