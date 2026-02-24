---
layout: default
title: "Chapter 5: Multi-Agent Systems"
parent: "LangGraph Tutorial"
nav_order: 5
---

# Chapter 5: Multi-Agent Systems

Welcome to the world of collaborative AI! Multi-agent systems take LangGraph to the next level by coordinating multiple AI agents that can communicate, delegate tasks, and work together toward complex goals. This chapter explores agent architectures, communication patterns, and orchestration strategies.

## Understanding Multi-Agent Coordination

Multi-agent systems involve multiple AI agents working together:
- **Task decomposition** - Breaking complex tasks into manageable subtasks
- **Agent specialization** - Different agents for different types of work
- **Communication protocols** - Structured ways agents exchange information
- **Conflict resolution** - Handling disagreements between agents
- **Resource allocation** - Managing shared resources and workloads

### Basic Multi-Agent Architecture

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
from langchain_openai import ChatOpenAI
from enum import Enum

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"

class AgentMessage(TypedDict):
    from_agent: str
    to_agent: str
    message_type: str
    content: str
    timestamp: str

class MultiAgentState(TypedDict):
    task: str
    agents: Dict[str, Dict[str, Any]]
    messages: List[AgentMessage]
    current_agent: str
    completed_tasks: List[str]
    final_result: str

def create_multi_agent_system() -> StateGraph:
    """Create a multi-agent system with coordinator and specialists"""

    graph = StateGraph(MultiAgentState)

    # Coordinator Agent
    def coordinator_agent(state: MultiAgentState) -> MultiAgentState:
        """Coordinates the multi-agent workflow"""
        task = state.get("task", "")
        messages = state.get("messages", [])

        # Analyze task and create subtasks
        subtasks = decompose_task(task)

        # Assign subtasks to agents
        agent_assignments = assign_subtasks_to_agents(subtasks)

        # Send messages to assigned agents
        new_messages = []
        for assignment in agent_assignments:
            message: AgentMessage = {
                "from_agent": "coordinator",
                "to_agent": assignment["agent"],
                "message_type": "task_assignment",
                "content": assignment["task"],
                "timestamp": get_current_timestamp()
            }
            new_messages.append(message)

        return {
            **state,
            "messages": messages + new_messages,
            "current_agent": "researcher",  # Start with researcher
            "subtasks": subtasks
        }

    # Researcher Agent
    def researcher_agent(state: MultiAgentState) -> MultiAgentState:
        """Handles research and information gathering"""
        messages = state.get("messages", [])
        agent_messages = [m for m in messages if m["to_agent"] == "researcher"]

        if not agent_messages:
            return state  # No tasks for researcher

        latest_task = agent_messages[-1]["content"]

        # Perform research
        research_results = perform_research(latest_task)

        # Send results to analyst
        result_message: AgentMessage = {
            "from_agent": "researcher",
            "to_agent": "analyst",
            "message_type": "research_results",
            "content": research_results,
            "timestamp": get_current_timestamp()
        }

        return {
            **state,
            "messages": messages + [result_message],
            "current_agent": "analyst",
            "research_results": research_results
        }

    # Analyst Agent
    def analyst_agent(state: MultiAgentState) -> MultiAgentState:
        """Analyzes research results and provides insights"""
        messages = state.get("messages", [])
        agent_messages = [m for m in messages if m["to_agent"] == "analyst"]

        if not agent_messages:
            return state

        research_data = agent_messages[-1]["content"]

        # Perform analysis
        analysis = analyze_research_data(research_data)

        # Send analysis to writer
        analysis_message: AgentMessage = {
            "from_agent": "analyst",
            "to_agent": "writer",
            "message_type": "analysis_results",
            "content": analysis,
            "timestamp": get_current_timestamp()
        }

        return {
            **state,
            "messages": messages + [analysis_message],
            "current_agent": "writer",
            "analysis_results": analysis
        }

    # Writer Agent
    def writer_agent(state: MultiAgentState) -> MultiAgentState:
        """Creates final output based on analysis"""
        messages = state.get("messages", [])
        agent_messages = [m for m in messages if m["to_agent"] == "writer"]

        if not agent_messages:
            return state

        analysis_data = agent_messages[-1]["content"]

        # Generate final output
        final_result = generate_final_output(analysis_data)

        return {
            **state,
            "final_result": final_result,
            "current_agent": "complete"
        }

    # Add nodes
    graph.add_node("coordinator", coordinator_agent)
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("writer", writer_agent)

    # Define routing logic
    def route_to_next_agent(state: MultiAgentState) -> str:
        current_agent = state.get("current_agent", "coordinator")

        agent_flow = {
            "coordinator": "researcher",
            "researcher": "analyst",
            "analyst": "writer",
            "writer": END
        }

        return agent_flow.get(current_agent, END)

    # Set up flow
    graph.set_entry_point("coordinator")
    graph.add_conditional_edges(
        "coordinator",
        route_to_next_agent,
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer"
        }
    )
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", END)

    return graph
```

## Agent Communication Patterns

### Message Passing Architecture

```python
class AgentCommunicationSystem:
    """Handles communication between agents"""

    def __init__(self):
        self.message_queue = []
        self.agent_states = {}

    def send_message(self, message: AgentMessage):
        """Send message to agent"""
        self.message_queue.append(message)

    def receive_messages(self, agent_id: str) -> List[AgentMessage]:
        """Get messages for specific agent"""
        agent_messages = [m for m in self.message_queue if m["to_agent"] == agent_id]
        # Remove from queue after delivery
        self.message_queue = [m for m in self.message_queue if m["to_agent"] != agent_id]
        return agent_messages

    def broadcast_message(self, from_agent: str, content: str, message_type: str = "broadcast"):
        """Send message to all agents"""
        # Implementation for broadcasting
        pass

class CommunicativeAgent:
    """Base class for agents that can communicate"""

    def __init__(self, agent_id: str, communication_system: AgentCommunicationSystem):
        self.agent_id = agent_id
        self.comm_system = communication_system
        self.knowledge_base = {}

    def send_message(self, to_agent: str, content: str, message_type: str = "task"):
        """Send message to another agent"""
        message: AgentMessage = {
            "from_agent": self.agent_id,
            "to_agent": to_agent,
            "message_type": message_type,
            "content": content,
            "timestamp": get_current_timestamp()
        }
        self.comm_system.send_message(message)

    def receive_messages(self) -> List[AgentMessage]:
        """Receive pending messages"""
        return self.comm_system.receive_messages(self.agent_id)

    def process_messages(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages and update state"""
        messages = self.receive_messages()

        for message in messages:
            state = self.handle_message(message, state)

        return state

    def handle_message(self, message: AgentMessage, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle individual message - override in subclasses"""
        return state
```

### Hierarchical Agent Organization

```python
def create_hierarchical_agent_system() -> StateGraph:
    """Create a hierarchical multi-agent system"""

    class HierarchicalState(TypedDict):
        task: str
        hierarchy_level: str
        supervisor: str
        subordinates: List[str]
        task_assignments: Dict[str, str]
        progress_reports: Dict[str, str]
        final_result: str

    graph = StateGraph(HierarchicalState)

    # Supervisor Agent
    def supervisor_agent(state: HierarchicalState) -> HierarchicalState:
        """Top-level supervisor that delegates to team leads"""
        task = state.get("task", "")

        # Break down task into major components
        major_components = decompose_major_task(task)

        # Assign to team leads
        assignments = {}
        for i, component in enumerate(major_components):
            team_lead = f"team_lead_{i+1}"
            assignments[team_lead] = component

        # Send assignments
        assignment_messages = []
        for team_lead, component_task in assignments.items():
            message: AgentMessage = {
                "from_agent": "supervisor",
                "to_agent": team_lead,
                "message_type": "major_task_assignment",
                "content": component_task,
                "timestamp": get_current_timestamp()
            }
            assignment_messages.append(message)

        return {
            **state,
            "hierarchy_level": "supervisor",
            "subordinates": list(assignments.keys()),
            "task_assignments": assignments,
            "messages": state.get("messages", []) + assignment_messages
        }

    # Team Lead Agent
    def team_lead_agent(state: HierarchicalState) -> HierarchicalState:
        """Team lead that coordinates individual contributors"""
        # Get assignment for this team lead
        current_agent = state.get("current_agent", "")
        assignment = state.get("task_assignments", {}).get(current_agent, "")

        if not assignment:
            return state

        # Break down into individual tasks
        individual_tasks = decompose_individual_tasks(assignment)

        # Assign to team members
        member_assignments = {}
        for i, task in enumerate(individual_tasks):
            member = f"member_{i+1}"
            member_assignments[member] = task

        return {
            **state,
            "individual_assignments": member_assignments,
            "team_progress": "tasks_assigned"
        }

    # Individual Contributor Agent
    def contributor_agent(state: HierarchicalState) -> HierarchicalState:
        """Individual contributor that executes specific tasks"""
        # Get individual assignment
        assignments = state.get("individual_assignments", {})
        current_member = state.get("current_member", "")

        task = assignments.get(current_member, "")

        if not task:
            return state

        # Execute task
        result = execute_individual_task(task)

        # Report progress
        progress_report = {
            "member": current_member,
            "task": task,
            "result": result,
            "status": "completed"
        }

        return {
            **state,
            "member_results": state.get("member_results", []) + [progress_report]
        }

    # Add nodes
    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("team_lead", team_lead_agent)
    graph.add_node("contributor", contributor_agent)

    # Set up hierarchical flow
    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "team_lead")
    graph.add_edge("team_lead", "contributor")
    graph.add_edge("contributor", END)

    return graph
```

## Conflict Resolution and Consensus

```python
class ConflictResolutionSystem:
    """Handles conflicts between agents"""

    def __init__(self):
        self.conflicts = []

    def detect_conflict(self, agent_proposals: Dict[str, Any]) -> bool:
        """Detect if agents have conflicting proposals"""
        proposals = list(agent_proposals.values())

        # Check for conflicting recommendations
        if len(set(proposals)) > 1:
            return True

        return False

    def resolve_conflict(self, agent_proposals: Dict[str, Any], conflict_type: str) -> Any:
        """Resolve conflict using appropriate strategy"""
        if conflict_type == "majority_vote":
            return self.majority_vote_resolution(agent_proposals)
        elif conflict_type == "weighted_vote":
            return self.weighted_vote_resolution(agent_proposals)
        elif conflict_type == "expert_consultation":
            return self.expert_consultation_resolution(agent_proposals)
        else:
            return self.fallback_resolution(agent_proposals)

    def majority_vote_resolution(self, proposals: Dict[str, Any]) -> Any:
        """Simple majority vote"""
        from collections import Counter
        votes = Counter(proposals.values())
        return votes.most_common(1)[0][0]

    def weighted_vote_resolution(self, proposals: Dict[str, Any]) -> Any:
        """Weighted vote based on agent expertise"""
        agent_weights = {
            "expert_agent": 0.5,
            "experienced_agent": 0.3,
            "novice_agent": 0.2
        }

        weighted_scores = {}
        for agent, proposal in proposals.items():
            weight = agent_weights.get(agent, 0.1)
            if proposal not in weighted_scores:
                weighted_scores[proposal] = 0
            weighted_scores[proposal] += weight

        return max(weighted_scores.items(), key=lambda x: x[1])[0]
```

## Agent Specialization and Skills

```python
class AgentSkillsManager:
    """Manages agent skills and task routing"""

    def __init__(self):
        self.agent_skills = {}
        self.task_requirements = {}

    def register_agent_skills(self, agent_id: str, skills: List[str]):
        """Register skills for an agent"""
        self.agent_skills[agent_id] = skills

    def find_best_agent_for_task(self, task: str, required_skills: List[str]) -> str:
        """Find the best agent for a given task"""
        task_skills = self.extract_task_skills(task, required_skills)

        best_agent = None
        best_score = 0

        for agent_id, skills in self.agent_skills.items():
            score = self.calculate_skill_match(skills, task_skills)
            if score > best_score:
                best_score = score
                best_agent = agent_id

        return best_agent or "default_agent"

    def calculate_skill_match(self, agent_skills: List[str], task_skills: List[str]) -> float:
        """Calculate how well agent skills match task requirements"""
        if not task_skills:
            return 1.0  # No specific skills required

        matches = sum(1 for skill in task_skills if skill in agent_skills)
        return matches / len(task_skills)

    def extract_task_skills(self, task: str, required_skills: List[str]) -> List[str]:
        """Extract required skills from task description"""
        # Simple keyword matching - could be enhanced with NLP
        task_lower = task.lower()
        extracted_skills = []

        skill_keywords = {
            "research": ["research", "analysis", "investigation"],
            "writing": ["writing", "content", "documentation"],
            "coding": ["programming", "development", "implementation"],
            "design": ["design", "ui", "ux", "visual"]
        }

        for skill, keywords in skill_keywords.items():
            if any(keyword in task_lower for keyword in keywords):
                extracted_skills.append(skill)

        return extracted_skills + required_skills
```

## Real-World Multi-Agent Example

```python
def create_customer_support_multi_agent() -> StateGraph:
    """Create a customer support multi-agent system"""

    class SupportState(TypedDict):
        customer_query: str
        query_category: str
        assigned_agents: List[str]
        agent_responses: Dict[str, str]
        final_response: str
        resolution_status: str

    graph = StateGraph(SupportState)

    # Triage Agent
    def triage_agent(state: SupportState) -> SupportState:
        """Categorize and route customer queries"""
        query = state.get("customer_query", "")

        # Classify query
        category = classify_query(query)

        # Determine required agent types
        agent_types = get_required_agents(category)

        return {
            **state,
            "query_category": category,
            "required_agents": agent_types
        }

    # Specialized Agents
    def technical_agent(state: SupportState) -> SupportState:
        """Handle technical support queries"""
        query = state.get("customer_query", "")
        category = state.get("query_category", "")

        if category != "technical":
            return state

        # Generate technical response
        response = generate_technical_response(query)

        return {
            **state,
            "agent_responses": {
                **state.get("agent_responses", {}),
                "technical_agent": response
            }
        }

    def billing_agent(state: SupportState) -> SupportState:
        """Handle billing-related queries"""
        query = state.get("customer_query", "")
        category = state.get("query_category", "")

        if category != "billing":
            return state

        response = generate_billing_response(query)

        return {
            **state,
            "agent_responses": {
                **state.get("agent_responses", {}),
                "billing_agent": response
            }
        }

    # Response Coordinator
    def response_coordinator(state: SupportState) -> SupportState:
        """Coordinate and finalize response"""
        responses = state.get("agent_responses", {})

        if not responses:
            final_response = "I'm sorry, I couldn't process your request. Please try again."
            status = "unresolved"
        else:
            # Combine responses from multiple agents
            final_response = combine_agent_responses(responses)
            status = "resolved"

        return {
            **state,
            "final_response": final_response,
            "resolution_status": status
        }

    # Add nodes
    graph.add_node("triage", triage_agent)
    graph.add_node("technical", technical_agent)
    graph.add_node("billing", billing_agent)
    graph.add_node("coordinator", response_coordinator)

    # Define routing based on category
    def route_by_category(state: SupportState) -> List[str]:
        category = state.get("query_category", "")
        required_agents = state.get("required_agents", [])

        routes = []
        if "technical" in required_agents:
            routes.append("technical")
        if "billing" in required_agents:
            routes.append("billing")

        return routes

    # Set up flow
    graph.set_entry_point("triage")

    # Conditional routing to appropriate agents
    graph.add_conditional_edges(
        "triage",
        route_by_category,
        {
            "technical": "technical",
            "billing": "billing"
        }
    )

    # All agents report to coordinator
    graph.add_edge("technical", "coordinator")
    graph.add_edge("billing", "coordinator")
    graph.add_edge("coordinator", END)

    return graph

# Helper functions
def classify_query(query: str) -> str:
    """Classify customer query"""
    if any(word in query.lower() for word in ["error", "bug", "not working", "technical"]):
        return "technical"
    elif any(word in query.lower() for word in ["bill", "payment", "charge", "refund"]):
        return "billing"
    else:
        return "general"

def get_required_agents(category: str) -> List[str]:
    """Get required agent types for category"""
    agent_mapping = {
        "technical": ["technical"],
        "billing": ["billing"],
        "general": ["technical", "billing"]
    }
    return agent_mapping.get(category, ["technical"])

def combine_agent_responses(responses: Dict[str, str]) -> str:
    """Combine responses from multiple agents"""
    if len(responses) == 1:
        return list(responses.values())[0]
    else:
        combined = "Based on our analysis:\n\n"
        for agent, response in responses.items():
            combined += f"{agent.replace('_', ' ').title()}: {response}\n\n"
        return combined
```

## What We've Accomplished

Outstanding! 🎉 You've mastered multi-agent systems in LangGraph:

1. **Basic multi-agent coordination** - Multiple agents working together
2. **Agent communication systems** - Structured message passing
3. **Hierarchical organizations** - Supervisor and subordinate agents
4. **Conflict resolution** - Handling disagreements between agents
5. **Agent specialization** - Skills-based task assignment
6. **Real-world applications** - Customer support multi-agent system

## Next Steps

Ready to integrate external tools and APIs? In [Chapter 6: Tool Integration](06-tool-integration.md), we'll explore connecting your LangGraph applications to external services!

---

**Practice what you've learned:**
1. Build a multi-agent system for content creation
2. Implement a hierarchical team structure for complex tasks
3. Create conflict resolution for differing agent opinions
4. Add agent specialization based on skills and expertise
5. Build a real-time multi-agent collaboration system

*What's the most complex multi-agent system you'll create?* 🤝

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `state`, `self`, `graph` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Multi-Agent Systems` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `task`, `messages`, `agent` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Multi-Agent Systems` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `graph`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Conditional Logic](04-conditional-logic.md)
- [Next Chapter: Chapter 6: Tool Integration](06-tool-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
