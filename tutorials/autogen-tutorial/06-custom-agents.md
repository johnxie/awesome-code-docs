---
layout: default
title: "Chapter 6: Custom Agent Development"
parent: "Microsoft AutoGen Tutorial"
nav_order: 6
---

# Chapter 6: Custom Agent Development

Welcome to custom agent development! In this chapter, we'll explore how to create specialized AutoGen agents with custom capabilities, behaviors, and domain-specific knowledge. Custom agents allow you to build AI systems tailored to specific tasks and domains.

## Custom Agent Architecture

### Base Agent Framework

```python
from autogen import AssistantAgent
from typing import Dict, Any, List, Optional, Callable
import time
import json

class CustomAgent(AssistantAgent):
    def __init__(self, name: str, specialty: str, **kwargs):
        super().__init__(name=name, **kwargs)

        self.specialty = specialty
        self.capabilities = []
        self.knowledge_base = {}
        self.behavior_patterns = {}
        self.performance_metrics = {
            "tasks_completed": 0,
            "success_rate": 0.0,
            "average_response_time": 0.0,
            "specialty_tasks": 0
        }

        # Initialize specialty-specific features
        self._initialize_specialty_features()

    def _initialize_specialty_features(self):
        """Initialize features specific to the agent's specialty"""
        if self.specialty == "research":
            self._setup_research_capabilities()
        elif self.specialty == "coding":
            self._setup_coding_capabilities()
        elif self.specialty == "analysis":
            self._setup_analysis_capabilities()
        elif self.specialty == "creative":
            self._setup_creative_capabilities()

    def add_capability(self, name: str, function: Callable, description: str):
        """Add a custom capability to the agent"""
        self.capabilities.append({
            "name": name,
            "function": function,
            "description": description
        })

        # Update function map for tool usage
        if not hasattr(self, 'function_map') or self.function_map is None:
            self.function_map = {}
        self.function_map[name] = function

    def add_knowledge(self, topic: str, information: Any):
        """Add domain-specific knowledge"""
        self.knowledge_base[topic] = {
            "content": information,
            "added_at": time.time(),
            "access_count": 0,
            "last_accessed": None
        }

    def retrieve_knowledge(self, topic: str) -> Optional[Any]:
        """Retrieve knowledge on a specific topic"""
        if topic in self.knowledge_base:
            knowledge = self.knowledge_base[topic]
            knowledge["access_count"] += 1
            knowledge["last_accessed"] = time.time()
            return knowledge["content"]
        return None

    def add_behavior_pattern(self, trigger: str, response_template: str):
        """Add a behavior pattern for specific situations"""
        self.behavior_patterns[trigger] = response_template

    def generate_reply(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Override to add custom logic"""
        user_message = messages[-1]["content"]

        # Check for behavior patterns
        for trigger, template in self.behavior_patterns.items():
            if trigger.lower() in user_message.lower():
                return self._apply_template(template, {"message": user_message})

        # Add specialty context
        specialty_context = self._get_specialty_context(user_message)
        if specialty_context:
            messages[-1]["content"] += f"\n\nSpecialty Context: {specialty_context}"

        # Generate response using parent method
        response = super().generate_reply(messages, **kwargs)

        # Update performance metrics
        self._update_performance_metrics()

        return response

    def _get_specialty_context(self, message: str) -> Optional[str]:
        """Get specialty-specific context for a message"""
        # This would be implemented by subclasses
        return None

    def _apply_template(self, template: str, variables: Dict[str, Any]) -> str:
        """Apply variables to a template string"""
        result = template
        for key, value in variables.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result

    def _update_performance_metrics(self):
        """Update performance metrics after each interaction"""
        self.performance_metrics["tasks_completed"] += 1

    def get_performance_report(self) -> Dict[str, Any]:
        """Get a performance report for the agent"""
        return {
            "name": self.name,
            "specialty": self.specialty,
            "capabilities_count": len(self.capabilities),
            "knowledge_topics": len(self.knowledge_base),
            **self.performance_metrics
        }
```

### Specialty-Specific Agent Classes

```python
class ResearchAgent(CustomAgent):
    def __init__(self, **kwargs):
        super().__init__(name="ResearchAgent", specialty="research", **kwargs)

    def _setup_research_capabilities(self):
        """Set up research-specific capabilities"""
        self.add_capability(
            "web_search",
            self._web_search,
            "Search the web for information"
        )
        self.add_capability(
            "analyze_sources",
            self._analyze_sources,
            "Analyze credibility and relevance of sources"
        )
        self.add_capability(
            "synthesize_findings",
            self._synthesize_findings,
            "Synthesize research findings into coherent insights"
        )

        # Add research-specific knowledge
        self.add_knowledge("research_methodology", {
            "qualitative_methods": ["interviews", "case studies", "ethnography"],
            "quantitative_methods": ["surveys", "experiments", "statistical analysis"],
            "mixed_methods": ["combining qualitative and quantitative approaches"]
        })

        # Add behavior patterns
        self.add_behavior_pattern(
            "find information",
            "I'll help you research that topic. Let me search for reliable sources and analyze the information."
        )

    def _get_specialty_context(self, message: str) -> Optional[str]:
        """Provide research-specific context"""
        if any(word in message.lower() for word in ["research", "find", "discover"]):
            return "As a research specialist, I can help you find reliable information, analyze sources, and synthesize findings."
        return None

    async def _web_search(self, query: str) -> Dict[str, Any]:
        """Perform web search (placeholder implementation)"""
        return {
            "query": query,
            "results": [
                {"title": f"Result for {query}", "url": f"https://example.com/{query}"}
            ]
        }

    async def _analyze_sources(self, sources: List[str]) -> Dict[str, Any]:
        """Analyze source credibility"""
        analysis = []
        for source in sources:
            # Simple credibility analysis
            credibility_score = 0.8 if ".edu" in source or ".gov" in source else 0.6
            analysis.append({
                "source": source,
                "credibility": credibility_score,
                "assessment": "High credibility" if credibility_score > 0.7 else "Moderate credibility"
            })

        return {"analysis": analysis}

    async def _synthesize_findings(self, findings: List[str]) -> str:
        """Synthesize research findings"""
        synthesis_prompt = f"""Please synthesize these research findings into a coherent summary:

Findings:
{chr(10).join(f"- {finding}" for finding in findings)}

Provide a well-structured summary with key insights and conclusions."""

        # This would use the LLM to generate synthesis
        return f"Synthesis of {len(findings)} findings completed."

class CodingAgent(CustomAgent):
    def __init__(self, **kwargs):
        super().__init__(name="CodingAgent", specialty="coding", **kwargs)

    def _setup_coding_capabilities(self):
        """Set up coding-specific capabilities"""
        self.add_capability(
            "write_code",
            self._write_code,
            "Write code for specific tasks"
        )
        self.add_capability(
            "debug_code",
            self._debug_code,
            "Debug and fix code issues"
        )
        self.add_capability(
            "review_code",
            self._review_code,
            "Review code for best practices and improvements"
        )

        # Add coding knowledge
        self.add_knowledge("programming_languages", {
            "python": {"paradigm": "multi-paradigm", "use_cases": ["web", "data science", "automation"]},
            "javascript": {"paradigm": "multi-paradigm", "use_cases": ["web", "server", "mobile"]},
            "java": {"paradigm": "object-oriented", "use_cases": ["enterprise", "android", "web"]}
        })

        self.add_behavior_pattern(
            "write code",
            "I'll help you write clean, efficient code. What programming language and functionality do you need?"
        )

    def _get_specialty_context(self, message: str) -> Optional[str]:
        """Provide coding-specific context"""
        if any(word in message.lower() for word in ["code", "program", "function", "class"]):
            return "As a coding specialist, I can help you write, debug, and review code in multiple programming languages."
        return None

    async def _write_code(self, language: str, task: str) -> str:
        """Write code for a specific task"""
        code_prompt = f"""Write {language} code to {task}.

Please include:
1. Clear comments explaining the code
2. Error handling where appropriate
3. Best practices for the language
4. Example usage

Language: {language}
Task: {task}"""

        # This would use the LLM to generate code
        return f"Generated {language} code for: {task}"

    async def _debug_code(self, code: str, error: str) -> str:
        """Debug code issues"""
        debug_prompt = f"""Debug this code:

Code:
{code}

Error:
{error}

Please identify the issue and provide a corrected version."""

        # This would use the LLM to debug
        return f"Debugged code with error: {error}"

    async def _review_code(self, code: str) -> Dict[str, Any]:
        """Review code for improvements"""
        review_prompt = f"""Review this code for best practices, performance, and potential improvements:

{code}

Please provide feedback on:
1. Code quality and style
2. Performance considerations
3. Security concerns
4. Best practices compliance"""

        # This would use the LLM to review
        return {
            "overall_score": 8.5,
            "strengths": ["Good structure", "Clear naming"],
            "improvements": ["Add error handling", "Consider performance optimization"],
            "suggestions": ["Use type hints", "Add docstrings"]
        }
```

## Agent Personality and Behavior

### Personality Framework

```python
from enum import Enum
from typing import Dict, Any

class PersonalityTrait(Enum):
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    ENTHUSIASTIC = "enthusiastic"
    CAUTIOUS = "cautious"

class AgentPersonality:
    def __init__(self):
        self.traits: Dict[PersonalityTrait, float] = {}
        self.communication_style = "balanced"
        self.response_templates: Dict[str, str] = {}

    def set_trait(self, trait: PersonalityTrait, intensity: float):
        """Set the intensity of a personality trait (0.0 to 1.0)"""
        self.traits[trait] = max(0.0, min(1.0, intensity))

    def add_response_template(self, situation: str, template: str):
        """Add a response template for specific situations"""
        self.response_templates[situation] = template

    def generate_response_modifier(self, base_response: str) -> str:
        """Modify a response based on personality traits"""
        modified_response = base_response

        # Apply personality modifications
        if self.traits.get(PersonalityTrait.FRIENDLY, 0) > 0.7:
            modified_response = self._make_friendlier(modified_response)

        if self.traits.get(PersonalityTrait.PROFESSIONAL, 0) > 0.7:
            modified_response = self._make_more_professional(modified_response)

        if self.traits.get(PersonalityTrait.ENTHUSIASTIC, 0) > 0.7:
            modified_response = self._add_enthusiasm(modified_response)

        return modified_response

    def _make_friendlier(self, response: str) -> str:
        """Make response friendlier"""
        friendly_phrases = ["I'd be happy to help!", "Let's work on this together!", "I'm excited to assist you!"]
        return f"{friendly_phrases[0]} {response}"

    def _make_more_professional(self, response: str) -> str:
        """Make response more professional"""
        return response.replace("Hey", "Hello").replace("Sure", "Certainly")

    def _add_enthusiasm(self, response: str) -> str:
        """Add enthusiasm to response"""
        enthusiastic_endings = ["I'm excited to help!", "This will be great!", "Let's make this awesome!"]
        return f"{response} {enthusiastic_endings[0]}"

class PersonalityDrivenAgent(CustomAgent):
    def __init__(self, personality: AgentPersonality, **kwargs):
        super().__init__(**kwargs)
        self.personality = personality

    def generate_reply(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Generate reply with personality modifications"""
        # Get base response from parent
        base_response = super().generate_reply(messages, **kwargs)

        # Apply personality modifications
        personalized_response = self.personality.generate_response_modifier(base_response)

        return personalized_response
```

### Behavior Learning System

```python
class BehaviorLearner:
    def __init__(self):
        self.behavior_history: List[Dict[str, Any]] = []
        self.success_patterns: Dict[str, float] = {}
        self.failure_patterns: Dict[str, float] = {}

    def record_interaction(self, input_text: str, response: str, outcome: str):
        """Record an interaction for learning"""
        interaction = {
            "input": input_text,
            "response": response,
            "outcome": outcome,  # "success", "failure", or "neutral"
            "timestamp": time.time()
        }

        self.behavior_history.append(interaction)

        # Update patterns
        self._update_patterns(input_text, outcome)

    def _update_patterns(self, input_text: str, outcome: str):
        """Update success/failure patterns"""
        # Extract keywords from input
        keywords = self._extract_keywords(input_text)

        for keyword in keywords:
            if outcome == "success":
                self.success_patterns[keyword] = self.success_patterns.get(keyword, 0) + 1
            elif outcome == "failure":
                self.failure_patterns[keyword] = self.failure_patterns.get(keyword, 0) + 1

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        words = text.lower().split()
        return [word for word in words if len(word) > 3]

    def get_best_response_pattern(self, input_text: str) -> Optional[str]:
        """Get the best response pattern for similar inputs"""
        keywords = self._extract_keywords(input_text)

        best_pattern = None
        best_score = 0

        for keyword in keywords:
            success_score = self.success_patterns.get(keyword, 0)
            failure_score = self.failure_patterns.get(keyword, 0)

            if success_score > failure_score:
                score = success_score / (success_score + failure_score)
                if score > best_score:
                    best_score = score
                    best_pattern = keyword

        return best_pattern

    def suggest_improvement(self, input_text: str) -> str:
        """Suggest improvements based on past performance"""
        best_pattern = self.get_best_response_pattern(input_text)

        if best_pattern:
            return f"Consider using approaches similar to successful interactions with '{best_pattern}'"
        else:
            return "No specific improvement suggestions available yet"

class AdaptiveAgent(CustomAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.behavior_learner = BehaviorLearner()

    def generate_reply(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Generate adaptive reply based on learning"""
        user_message = messages[-1]["content"]

        # Get suggestion from behavior learner
        suggestion = self.behavior_learner.get_best_response_pattern(user_message)

        # Add suggestion to context if available
        if suggestion:
            messages[-1]["content"] += f"\n\nLearning suggestion: {suggestion}"

        # Generate response
        response = super().generate_reply(messages, **kwargs)

        return response

    def record_outcome(self, input_text: str, response: str, outcome: str):
        """Record interaction outcome for learning"""
        self.behavior_learner.record_interaction(input_text, response, outcome)
```

## Advanced Agent Features

### Multi-Modal Agent

```python
class MultiModalAgent(CustomAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supported_modalities = ["text", "image", "audio", "video"]
        self.modal_processors = {}

    def add_modality_processor(self, modality: str, processor: Callable):
        """Add a processor for a specific modality"""
        self.modal_processors[modality] = processor

    async def process_multimodal_input(self, inputs: Dict[str, Any]) -> str:
        """Process inputs from multiple modalities"""
        processed_inputs = []

        for modality, data in inputs.items():
            if modality in self.modal_processors:
                processor = self.modal_processors[modality]
                processed_data = await processor(data)
                processed_inputs.append(f"{modality}: {processed_data}")
            else:
                processed_inputs.append(f"{modality}: {data}")

        # Combine processed inputs
        combined_input = "\n".join(processed_inputs)

        return combined_input

    async def generate_multimodal_response(self, text_response: str) -> Dict[str, Any]:
        """Generate response across multiple modalities"""
        response = {
            "text": text_response,
            "image": None,
            "audio": None
        }

        # Generate image if needed
        if "visualize" in text_response.lower():
            response["image"] = await self._generate_image(text_response)

        # Generate audio if needed
        if "speak" in text_response.lower():
            response["audio"] = await self._generate_audio(text_response)

        return response

    async def _generate_image(self, prompt: str) -> str:
        """Generate image from text prompt (placeholder)"""
        return f"Generated image for: {prompt}"

    async def _generate_audio(self, text: str) -> str:
        """Generate audio from text (placeholder)"""
        return f"Generated audio for: {text}"
```

### Collaborative Agent

```python
class CollaborativeAgent(CustomAgent):
    def __init__(self, team_members: List[CustomAgent], **kwargs):
        super().__init__(**kwargs)
        self.team_members = team_members
        self.collaboration_history = []
        self.trust_scores = {agent.name: 1.0 for agent in team_members}

    async def collaborate_on_task(self, task: str) -> Dict[str, Any]:
        """Collaborate with team members on a task"""
        # Decompose task
        subtasks = await self._decompose_task_for_team(task)

        # Assign subtasks to team members
        assignments = await self._assign_subtasks(subtasks)

        # Execute subtasks
        results = await self._execute_team_tasks(assignments)

        # Synthesize results
        final_result = await self._synthesize_team_results(results)

        # Update collaboration history
        self.collaboration_history.append({
            "task": task,
            "assignments": assignments,
            "results": results,
            "final_result": final_result,
            "timestamp": time.time()
        })

        return final_result

    async def _decompose_task_for_team(self, task: str) -> List[Dict[str, Any]]:
        """Decompose task for team collaboration"""
        # Use agent's specialty to decompose
        decomposition_prompt = f"""Decompose this task for a team of specialists:

Task: {task}

Team members: {[agent.name for agent in self.team_members]}

Provide subtasks that match team member specialties."""

        # This would use LLM to decompose
        return [
            {"description": "Research phase", "specialty": "research"},
            {"description": "Implementation phase", "specialty": "coding"},
            {"description": "Analysis phase", "specialty": "analysis"}
        ]

    async def _assign_subtasks(self, subtasks: List[Dict[str, Any]]) -> Dict[str, str]:
        """Assign subtasks to appropriate team members"""
        assignments = {}

        for subtask in subtasks:
            best_agent = self._find_best_agent_for_subtask(subtask)
            assignments[subtask["description"]] = best_agent.name

        return assignments

    def _find_best_agent_for_subtask(self, subtask: Dict[str, Any]) -> CustomAgent:
        """Find best agent for a subtask"""
        required_specialty = subtask.get("specialty", "")

        for agent in self.team_members:
            if agent.specialty == required_specialty:
                return agent

        # Fallback to highest trust score
        return max(self.team_members, key=lambda a: self.trust_scores.get(a.name, 0))

    async def _execute_team_tasks(self, assignments: Dict[str, str]) -> Dict[str, Any]:
        """Execute tasks assigned to team members"""
        results = {}

        for task_desc, agent_name in assignments.items():
            agent = next((a for a in self.team_members if a.name == agent_name), None)
            if agent:
                result = await agent.generate_reply(
                    messages=[{"role": "user", "content": task_desc}]
                )
                results[task_desc] = {
                    "agent": agent_name,
                    "result": result
                }

        return results

    async def _synthesize_team_results(self, results: Dict[str, Any]) -> str:
        """Synthesize results from team collaboration"""
        synthesis_prompt = f"""Synthesize these team results into a comprehensive final answer:

Results:
{json.dumps(results, indent=2)}

Provide a well-integrated final result."""

        # This would use LLM to synthesize
        return f"Synthesized results from {len(results)} team contributions"
```

## Agent Deployment and Management

### Agent Manager

```python
class AgentManager:
    def __init__(self):
        self.agents: Dict[str, CustomAgent] = {}
        self.active_agents: set = set()
        self.agent_metrics: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent: CustomAgent):
        """Register an agent with the manager"""
        self.agents[agent.name] = agent
        self.agent_metrics[agent.name] = {
            "registration_time": time.time(),
            "total_interactions": 0,
            "success_rate": 0.0,
            "average_response_time": 0.0
        }

    def activate_agent(self, agent_name: str):
        """Activate an agent"""
        if agent_name in self.agents:
            self.active_agents.add(agent_name)

    def deactivate_agent(self, agent_name: str):
        """Deactivate an agent"""
        self.active_agents.discard(agent_name)

    def get_agent(self, agent_name: str) -> Optional[CustomAgent]:
        """Get an agent by name"""
        return self.agents.get(agent_name)

    def get_active_agents(self) -> List[CustomAgent]:
        """Get all active agents"""
        return [self.agents[name] for name in self.active_agents if name in self.agents]

    def route_task_to_agent(self, task: str, agent_name: str = None) -> Optional[CustomAgent]:
        """Route a task to a specific agent or find the best agent"""
        if agent_name:
            return self.get_agent(agent_name)

        # Find best agent for task
        best_agent = None
        best_score = 0

        for agent in self.get_active_agents():
            score = self._calculate_task_fit(agent, task)
            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent

    def _calculate_task_fit(self, agent: CustomAgent, task: str) -> float:
        """Calculate how well an agent fits a task"""
        score = 0.0

        # Check specialty match
        task_lower = task.lower()
        if agent.specialty.lower() in task_lower:
            score += 0.5

        # Check capabilities
        for capability in agent.capabilities:
            if capability["name"].lower() in task_lower:
                score += 0.3

        # Check performance metrics
        metrics = self.agent_metrics.get(agent.name, {})
        success_rate = metrics.get("success_rate", 0.5)
        score += success_rate * 0.2

        return min(score, 1.0)

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "total_agents": len(self.agents),
            "active_agents": len(self.active_agents),
            "agent_status": {
                name: {
                    "active": name in self.active_agents,
                    "metrics": self.agent_metrics.get(name, {})
                }
                for name in self.agents.keys()
            }
        }
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Custom Agent Architecture** - Base framework for specialized agents
2. **Specialty-Specific Agents** - Research, coding, and analysis agents
3. **Agent Personality & Behavior** - Personality traits and adaptive behavior
4. **Advanced Agent Features** - Multi-modal and collaborative agents
5. **Agent Deployment & Management** - Agent manager and routing system

## Next Steps

Now that you understand custom agent development, let's explore multi-agent workflows. In [Chapter 7: Multi-Agent Workflows](07-multi-agent-workflows.md), we'll learn how to orchestrate complex interactions between multiple agents.

---

**Practice what you've learned:**
1. Create a custom agent with specialized capabilities for your domain
2. Implement personality traits and behavior patterns
3. Build a multi-modal agent that handles different input types
4. Set up an agent manager to coordinate multiple agents

*What kind of specialized agent would you build first?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `agent`, `Dict` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Custom Agent Development` as an operating subsystem inside **Microsoft AutoGen Tutorial: Building Multi-Agent AI Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `response`, `name`, `specialty` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Custom Agent Development` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `agent` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Dict`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `agent` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Task Decomposition](05-task-decomposition.md)
- [Next Chapter: Chapter 7: Multi-Agent Workflows](07-multi-agent-workflows.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
