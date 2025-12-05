---
layout: default
title: "Letta Tutorial - Chapter 6: Multi-Agent Systems"
nav_order: 6
has_children: false
parent: Letta Tutorial
---

# Chapter 6: Multi-Agent Systems

> Coordinate multiple agents, implement agent communication, and build collaborative workflows.

## Overview

Letta supports multi-agent systems where agents can communicate, delegate tasks, and collaborate. This chapter covers agent coordination, message passing, and implementing complex multi-agent workflows.

## Agent Communication

Agents can send messages to each other through the Letta system:

```python
from letta import create_client

client = create_client()

# Create multiple agents
researcher = client.create_agent(
    name="researcher",
    persona="You are a research specialist who finds and analyzes information."
)

writer = client.create_agent(
    name="writer",
    persona="You are a content writer who creates engaging articles."
)

editor = client.create_agent(
    name="editor",
    persona="You are an editor who reviews and improves content."
)
```

## Direct Agent Messaging

Agents can communicate directly:

```python
# Agent A sends message to Agent B
response = client.send_message(
    agent_name="researcher",
    message="Please research the latest developments in quantum computing",
    conversation_id=None  # New conversation
)

# Agent B's response
research_results = response.content

# Agent A sends results to Agent C
writer_response = client.send_message(
    agent_name="writer",
    message=f"Write an article about: {research_results}",
    conversation_id=None
)
```

## Agent Coordination Framework

Build a coordination system:

```python
class AgentCoordinator:
    def __init__(self, agents):
        self.agents = {agent.name: agent for agent in agents}
        self.conversations = {}

    def get_conversation(self, agent1, agent2):
        """Get or create conversation between two agents."""
        key = tuple(sorted([agent1, agent2]))
        if key not in self.conversations:
            # Create a shared conversation
            conv = client.create_conversation(
                agent_name=agent1,
                metadata={"participants": [agent1, agent2], "type": "agent_communication"}
            )
            self.conversations[key] = conv
        return self.conversations[key]

    def send_agent_message(self, from_agent, to_agent, message):
        """Send message from one agent to another."""
        conversation = self.get_conversation(from_agent, to_agent)

        response = client.send_message(
            agent_name=to_agent,
            message=f"[From {from_agent}]: {message}",
            conversation_id=conversation.id
        )

        return response

# Usage
coordinator = AgentCoordinator([researcher, writer, editor])

# Researcher sends findings to writer
coordinator.send_agent_message("researcher", "writer", "Here are the quantum computing findings...")

# Writer sends draft to editor
coordinator.send_agent_message("writer", "editor", "Please review this draft...")
```

## Workflow Orchestration

Implement structured workflows:

```python
class WorkflowOrchestrator:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def research_write_edit_workflow(self, topic):
        """Complete research -> write -> edit workflow."""
        print(f"Starting workflow for topic: {topic}")

        # Step 1: Research
        research_request = f"Research and summarize key points about {topic}"
        research_response = client.send_message(
            agent_name="researcher",
            message=research_request
        )

        print("✓ Research completed")

        # Step 2: Writing
        write_request = f"Write an engaging article based on this research: {research_response.content}"
        write_response = client.send_message(
            agent_name="writer",
            message=write_request
        )

        print("✓ Writing completed")

        # Step 3: Editing
        edit_request = f"Review and improve this article: {write_response.content}"
        edit_response = client.send_message(
            agent_name="editor",
            message=edit_request
        )

        print("✓ Editing completed")

        return {
            "research": research_response.content,
            "draft": write_response.content,
            "final": edit_response.content
        }

# Usage
orchestrator = WorkflowOrchestrator(coordinator)
result = orchestrator.research_write_edit_workflow("artificial intelligence")
```

## Agent Roles and Responsibilities

Define clear roles for collaborative tasks:

```python
AGENT_ROLES = {
    "project_manager": {
        "persona": "You are a project manager who coordinates tasks and ensures deadlines are met.",
        "responsibilities": ["task_assignment", "progress_tracking", "deadline_management"]
    },
    "developer": {
        "persona": "You are a software developer who writes clean, efficient code.",
        "responsibilities": ["coding", "code_review", "testing"]
    },
    "designer": {
        "persona": "You are a UX/UI designer who creates intuitive user experiences.",
        "responsibilities": ["design", "prototyping", "user_research"]
    },
    "qa_engineer": {
        "persona": "You are a QA engineer who ensures quality and catches bugs.",
        "responsibilities": ["testing", "bug_reporting", "quality_assurance"]
    }
}

def create_team(roles):
    """Create a team of agents with defined roles."""
    team = {}
    for role, config in roles.items():
        agent = client.create_agent(
            name=f"{role}_agent",
            persona=config["persona"],
            metadata={"role": role, "responsibilities": config["responsibilities"]}
        )
        team[role] = agent
    return team

# Create development team
team = create_team(AGENT_ROLES)
```

## Task Delegation System

Implement intelligent task delegation:

```python
class TaskDelegator:
    def __init__(self, team):
        self.team = team

    def delegate_task(self, task_description):
        """Delegate task to appropriate team member."""
        # Determine best agent for task
        best_agent = self._select_agent(task_description)

        # Send task to agent
        response = client.send_message(
            agent_name=best_agent,
            message=f"Task assigned: {task_description}"
        )

        return best_agent, response

    def _select_agent(self, task):
        """Select best agent for task based on description."""
        if "design" in task.lower() or "ui" in task.lower():
            return "designer_agent"
        elif "code" in task.lower() or "implement" in task.lower():
            return "developer_agent"
        elif "test" in task.lower() or "bug" in task.lower():
            return "qa_engineer_agent"
        else:
            return "project_manager_agent"

# Usage
delegator = TaskDelegator(team)

# Delegate tasks
agent, response = delegator.delegate_task("Design the login page UI")
print(f"Task delegated to {agent}")

agent, response = delegator.delegate_task("Implement user authentication")
print(f"Task delegated to {agent}")
```

## Collaborative Problem Solving

Agents working together on complex problems:

```python
class CollaborativeSolver:
    def __init__(self, coordinator, team):
        self.coordinator = coordinator
        self.team = team

    def solve_problem(self, problem_statement):
        """Solve complex problem with multiple agents."""
        print(f"Solving: {problem_statement}")

        # Step 1: Analysis by project manager
        analysis = client.send_message(
            agent_name="project_manager_agent",
            message=f"Analyze this problem and break it down: {problem_statement}"
        )

        # Step 2: Technical design by developer
        design = client.send_message(
            agent_name="developer_agent",
            message=f"Design technical solution for: {analysis.content}"
        )

        # Step 3: UI/UX by designer
        ui_design = client.send_message(
            agent_name="designer_agent",
            message=f"Design UI/UX for: {design.content}"
        )

        # Step 4: Testing strategy by QA
        testing = client.send_message(
            agent_name="qa_engineer_agent",
            message=f"Create testing strategy for: {design.content}"
        )

        # Step 5: Integration by project manager
        integration = client.send_message(
            agent_name="project_manager_agent",
            message=f"Create implementation plan combining: {design.content}, {ui_design.content}, {testing.content}"
        )

        return {
            "analysis": analysis.content,
            "design": design.content,
            "ui_design": ui_design.content,
            "testing": testing.content,
            "plan": integration.content
        }

# Usage
solver = CollaborativeSolver(coordinator, team)
solution = solver.solve_problem("Build a task management web application")
```

## Agent Memory Sharing

Agents can share relevant memories:

```python
def share_memory(from_agent, to_agent, memory_query):
    """Share relevant memories between agents."""
    # Search sender's memory
    memories = client.search_archival_memory(from_agent, memory_query, limit=5)

    # Share with recipient
    shared_info = "\n".join([f"- {mem.content}" for mem in memories])

    message = f"Shared memories about '{memory_query}':\n{shared_info}"

    response = coordinator.send_agent_message(from_agent, to_agent, message)
    return response

# Share project knowledge
share_memory("researcher", "writer", "quantum computing")
```

## Conflict Resolution

Handle disagreements between agents:

```python
class ConflictResolver:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def resolve_conflict(self, agent1, agent2, issue):
        """Resolve conflicts between agents."""
        # Create neutral mediator agent
        mediator = client.create_agent(
            name="mediator",
            persona="You are a neutral mediator who helps resolve conflicts and find compromise.",
            system="Listen to both sides, identify common ground, propose fair solutions."
        )

        # Get perspectives
        perspective1 = coordinator.send_agent_message(agent1, "mediator", f"What's your view on: {issue}")
        perspective2 = coordinator.send_agent_message(agent2, "mediator", f"What's your view on: {issue}")

        # Mediation
        mediation = client.send_message(
            agent_name="mediator",
            message=f"Agent A says: {perspective1.content}\n\nAgent B says: {perspective2.content}\n\nPlease provide a compromise solution."
        )

        return mediation.content

# Usage
resolver = ConflictResolver(coordinator)
resolution = resolver.resolve_conflict("developer_agent", "designer_agent", "button placement")
```

## Performance Monitoring

Track multi-agent performance:

```python
class MultiAgentMonitor:
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.metrics = {}

    def track_interaction(self, from_agent, to_agent, message, response):
        """Track agent interactions."""
        key = f"{from_agent}->{to_agent}"
        if key not in self.metrics:
            self.metrics[key] = {"count": 0, "total_time": 0}

        self.metrics[key]["count"] += 1
        # Track timing, success rates, etc.

    def get_metrics(self):
        """Get interaction metrics."""
        return self.metrics

    def identify_bottlenecks(self):
        """Find slow or overloaded agents."""
        bottlenecks = []
        for interaction, data in self.metrics.items():
            if data["avg_response_time"] > 30:  # seconds
                bottlenecks.append(interaction)
        return bottlenecks

# Usage
monitor = MultiAgentMonitor(coordinator)
# Track all interactions...
```

## Scaling Multi-Agent Systems

Strategies for larger agent networks:

```python
class AgentNetwork:
    def __init__(self):
        self.agents = {}
        self.groups = {}  # Group agents by specialty

    def add_agent(self, agent, groups=None):
        """Add agent to network."""
        self.agents[agent.name] = agent
        if groups:
            for group in groups:
                if group not in self.groups:
                    self.groups[group] = []
                self.groups[group].append(agent.name)

    def find_agents_by_skill(self, skill):
        """Find agents with specific skills."""
        matches = []
        for agent_name, agent in self.agents.items():
            if skill.lower() in agent.persona.lower():
                matches.append(agent_name)
        return matches

    def broadcast_to_group(self, group, message):
        """Send message to all agents in a group."""
        if group not in self.groups:
            return []

        responses = []
        for agent_name in self.groups[group]:
            response = client.send_message(
                agent_name=agent_name,
                message=f"[Group {group}]: {message}"
            )
            responses.append((agent_name, response))

        return responses

# Usage
network = AgentNetwork()
network.add_agent(researcher, ["research", "analysis"])
network.add_agent(writer, ["content", "writing"])
network.add_agent(editor, ["content", "review"])

# Find specialists
designers = network.find_agents_by_skill("design")

# Group communication
network.broadcast_to_group("content", "New style guide released")
```

## Best Practices

1. **Clear Roles**: Define distinct responsibilities for each agent
2. **Communication Protocols**: Establish how agents should communicate
3. **Conflict Resolution**: Have mechanisms for handling disagreements
4. **Monitoring**: Track performance and identify bottlenecks
5. **Scalability**: Design for growing numbers of agents
6. **Memory Sharing**: Enable relevant knowledge transfer between agents
7. **Fallbacks**: Handle agent failures gracefully

Next: Deploy agents as REST API services. 