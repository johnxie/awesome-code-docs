---
layout: default
title: "Phidata Tutorial - Chapter 5: Multi-Agent Systems"
nav_order: 5
has_children: false
parent: Phidata Tutorial
---

# Chapter 5: Multi-Agent Systems - Coordinating Teams of AI Agents

Welcome to **Chapter 5: Multi-Agent Systems - Coordinating Teams of AI Agents**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build collaborative agent teams that can delegate tasks, share knowledge, and work together to solve complex problems.

## Basic Multi-Agent Coordination

### Agent Teams

```python
from phidata.agent import Agent
from phidata.team import Team

# Create specialized agents
researcher = Agent(
    name="ResearchAgent",
    instructions="You are a research specialist. Find accurate information and provide comprehensive analysis.",
    model="gpt-4",
    role="Researcher"
)

analyst = Agent(
    name="DataAnalyst",
    instructions="You are a data analyst. Analyze data, identify patterns, and provide insights.",
    model="gpt-4",
    role="Analyst"
)

writer = Agent(
    name="ContentWriter",
    instructions="You are a content writer. Create engaging, well-structured content based on research and analysis.",
    model="gpt-4",
    role="Writer"
)

# Create a team
market_research_team = Team(
    name="MarketResearchTeam",
    description="A team specialized in comprehensive market research and reporting",
    agents=[researcher, analyst, writer],
    instructions="Work together to provide comprehensive market research reports."
)

# Run team on a complex task
result = market_research_team.run("""
Conduct market research on the electric vehicle industry and create a comprehensive report covering:
1. Current market size and growth trends
2. Key players and competitive landscape
3. Consumer adoption patterns
4. Future outlook and predictions
5. Investment opportunities
""")

print("Team Result:")
print(result)
```

### Hierarchical Agent Organization

```python
from phidata.team import Team
from typing import List

class HierarchicalTeam(Team):
    """Team with hierarchical organization and role-based coordination."""

    def __init__(self, name: str, lead_agent: Agent, specialist_agents: List[Agent], **kwargs):
        super().__init__(name=name, agents=[lead_agent] + specialist_agents, **kwargs)
        self.lead_agent = lead_agent
        self.specialist_agents = specialist_agents

    def coordinate_task(self, task: str) -> str:
        """Coordinate complex task through hierarchical delegation."""

        # Lead agent breaks down the task
        breakdown = self.lead_agent.run(f"""
        Break down this complex task into subtasks that can be handled by specialists:
        {task}

        Identify which subtasks should go to which specialist type.
        Provide clear instructions for each subtask.
        """)

        print(f"Task breakdown by {self.lead_agent.name}:")
        print(breakdown)

        # Parse breakdown and delegate (simplified)
        subtask_results = []

        # Simulate delegation to specialists
        for i, specialist in enumerate(self.specialist_agents):
            specialist_task = f"""
            Based on this task breakdown: {breakdown}

            Focus on your area of expertise and provide detailed work on subtask {i+1}.
            """

            result = specialist.run(specialist_task)
            subtask_results.append(f"{specialist.name}: {result}")

        # Lead agent synthesizes results
        synthesis = self.lead_agent.run(f"""
        Synthesize these specialist contributions into a comprehensive final result:

        {chr(10).join(subtask_results)}

        Provide a well-structured, cohesive final answer that integrates all contributions.
        """)

        return synthesis

# Create hierarchical team
ceo_agent = Agent(
    name="CEOAgent",
    instructions="You are the CEO. Provide strategic direction, break down complex tasks, and ensure high-quality results.",
    model="gpt-4",
    role="CEO"
)

marketing_specialist = Agent(
    name="MarketingSpecialist",
    instructions="You are a marketing specialist. Focus on market analysis, customer insights, and marketing strategies.",
    model="gpt-4",
    role="Marketing"
)

technical_specialist = Agent(
    name="TechnicalSpecialist",
    instructions="You are a technical specialist. Focus on technical feasibility, implementation details, and technical requirements.",
    model="gpt-4",
    role="Technical"
)

financial_specialist = Agent(
    name="FinancialSpecialist",
    instructions="You are a financial specialist. Focus on financial analysis, costs, revenue projections, and ROI calculations.",
    model="gpt-4",
    role="Financial"
)

# Create hierarchical team
executive_team = HierarchicalTeam(
    name="ExecutiveTeam",
    lead_agent=ceo_agent,
    specialist_agents=[marketing_specialist, technical_specialist, financial_specialist],
    description="Executive team for strategic decision making and project planning"
)

# Execute complex strategic task
strategic_result = executive_team.coordinate_task("""
Evaluate launching a new AI-powered productivity tool. Consider:
- Market opportunity and competitive landscape
- Technical implementation requirements
- Financial projections and investment needs
- Go-to-market strategy and timeline
""")

print("Strategic Analysis Result:")
print(strategic_result)
```

## Communication Protocols

### Message Passing Between Agents

```python
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: str  # "request", "response", "broadcast", "delegate"
    content: str
    metadata: Dict[str, Any] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}

class MessageBus:
    """Centralized message passing system for agents."""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.message_history: List[AgentMessage] = []

    def register_agent(self, agent: Agent):
        """Register an agent with the message bus."""
        self.agents[agent.name] = agent

    async def send_message(self, message: AgentMessage):
        """Send message to recipient(s)."""
        await self.message_queue.put(message)
        self.message_history.append(message)

        print(f"📨 {message.sender} -> {message.receiver}: {message.message_type}")

    async def broadcast_message(self, sender: str, message_type: str, content: str):
        """Broadcast message to all agents."""
        for agent_name in self.agents.keys():
            if agent_name != sender:
                message = AgentMessage(
                    sender=sender,
                    receiver=agent_name,
                    message_type=message_type,
                    content=content
                )
                await self.send_message(message)

    async def process_messages(self):
        """Process messages from the queue."""
        while True:
            message = await self.message_queue.get()

            if message.receiver in self.agents:
                await self.deliver_message(message)
            elif message.receiver == "all":
                await self.broadcast_message(message.sender, message.message_type, message.content)

            self.message_queue.task_done()

    async def deliver_message(self, message: AgentMessage):
        """Deliver message to specific agent."""
        agent = self.agents[message.receiver]

        # Format message for agent
        formatted_message = f"""
        Message from {message.sender}:
        Type: {message.message_type}
        Content: {message.content}
        """

        if message.metadata:
            formatted_message += f"\nMetadata: {message.metadata}"

        # Agent processes the message
        response = agent.run(formatted_message)

        # Send response back if it's a request
        if message.message_type == "request":
            response_message = AgentMessage(
                sender=message.receiver,
                receiver=message.sender,
                message_type="response",
                content=response,
                metadata={"original_request": message.content}
            )
            await self.send_message(response_message)

# Enhanced agent with messaging capabilities
class CommunicativeAgent(Agent):
    """Agent that can communicate through message bus."""

    def __init__(self, message_bus: MessageBus, **kwargs):
        super().__init__(**kwargs)
        self.message_bus = message_bus
        message_bus.register_agent(self)

    async def send_request(self, receiver: str, content: str) -> str:
        """Send request to another agent and wait for response."""
        request_message = AgentMessage(
            sender=self.name,
            receiver=receiver,
            message_type="request",
            content=content
        )

        await self.message_bus.send_message(request_message)

        # In practice, you'd implement proper async waiting
        # For demo, we'll simulate with a delay
        await asyncio.sleep(0.1)

        # Check for responses (simplified)
        responses = [msg for msg in self.message_bus.message_history
                    if msg.sender == receiver and msg.message_type == "response"
                    and msg.metadata.get("original_request") == content]

        return responses[-1].content if responses else "No response received"

# Create message bus
message_bus = MessageBus()

# Create communicative agents
project_manager = CommunicativeAgent(
    message_bus=message_bus,
    name="ProjectManager",
    instructions="You are a project manager. Coordinate tasks and ensure timely delivery.",
    model="gpt-4"
)

developer = CommunicativeAgent(
    message_bus=message_bus,
    name="Developer",
    instructions="You are a developer. Write code and implement features.",
    model="gpt-4"
)

designer = CommunicativeAgent(
    message_bus=message_bus,
    name="Designer",
    instructions="You are a designer. Create user interfaces and user experiences.",
    model="gpt-4"
)

# Start message processing
asyncio.create_task(message_bus.process_messages())

# Simulate agent communication
async def demonstrate_communication():
    # Project manager delegates task
    await message_bus.send_message(AgentMessage(
        sender="ProjectManager",
        receiver="Developer",
        message_type="request",
        content="Implement user authentication for the web app. Use JWT tokens and bcrypt for password hashing."
    ))

    await asyncio.sleep(0.2)  # Allow processing

    # Check message history
    print("Message History:")
    for msg in message_bus.message_history[-3:]:  # Last 3 messages
        print(f"{msg.timestamp}: {msg.sender} -> {msg.receiver} ({msg.message_type})")
        print(f"  {msg.content[:100]}...")
        print()

asyncio.run(demonstrate_communication())
```

## Task Delegation and Workflow Management

### Dynamic Task Assignment

```python
from typing import Dict, List, Any, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task:
    """Represents a task that can be delegated to agents."""

    def __init__(self, id: str, description: str, priority: str = "medium",
                 required_skills: List[str] = None, dependencies: List[str] = None):
        self.id = id
        self.description = description
        self.priority = priority
        self.required_skills = required_skills or []
        self.dependencies = dependencies or []
        self.status = TaskStatus.PENDING
        self.assigned_agent: Optional[str] = None
        self.result: Optional[str] = None
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

class TaskManager:
    """Manages task delegation and workflow coordination."""

    def __init__(self, agents: Dict[str, Agent]):
        self.agents = agents
        self.tasks: Dict[str, Task] = {}
        self.agent_skills: Dict[str, List[str]] = self._analyze_agent_skills()

    def _analyze_agent_skills(self) -> Dict[str, List[str]]:
        """Analyze agent skills based on their instructions and tools."""
        skills = {}

        for agent_name, agent in self.agents.items():
            agent_skills = []

            # Analyze instructions for keywords
            instructions_lower = agent.instructions.lower()

            if any(word in instructions_lower for word in ["research", "search", "find", "analyze"]):
                agent_skills.append("research")

            if any(word in instructions_lower for word in ["code", "program", "develop", "implement"]):
                agent_skills.append("development")

            if any(word in instructions_lower for word in ["design", "ui", "ux", "interface"]):
                agent_skills.append("design")

            if any(word in instructions_lower for word in ["write", "content", "article", "document"]):
                agent_skills.append("writing")

            if any(word in instructions_lower for word in ["analyze", "data", "statistics", "insights"]):
                agent_skills.append("analysis")

            # Analyze tools
            if hasattr(agent, 'tools') and agent.tools:
                tool_names = [tool.name.lower() for tool in agent.tools]
                if any('search' in name for name in tool_names):
                    agent_skills.append("search")
                if any('code' in name or 'dev' in name for name in tool_names):
                    agent_skills.append("coding")

            skills[agent_name] = agent_skills

        return skills

    def create_task(self, description: str, priority: str = "medium",
                   required_skills: List[str] = None) -> str:
        """Create a new task."""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(description) % 1000}"

        task = Task(
            id=task_id,
            description=description,
            priority=priority,
            required_skills=required_skills
        )

        self.tasks[task_id] = task
        return task_id

    def assign_task(self, task_id: str) -> bool:
        """Assign task to best available agent."""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.PENDING:
            return False

        best_agent = self._find_best_agent(task)
        if best_agent:
            task.assigned_agent = best_agent
            task.status = TaskStatus.IN_PROGRESS
            return True

        return False

    def _find_best_agent(self, task: Task) -> Optional[str]:
        """Find best agent for task based on skills and availability."""
        candidates = []

        for agent_name, skills in self.agent_skills.items():
            # Check if agent has required skills
            skill_match = len(set(task.required_skills) & set(skills)) / len(task.required_skills) if task.required_skills else 1.0

            # Prioritize based on priority
            priority_score = {"high": 3, "medium": 2, "low": 1}.get(task.priority, 1)

            # Combined score
            total_score = skill_match * priority_score

            candidates.append((total_score, agent_name))

        # Return agent with highest score
        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][1]

        return None

    async def execute_task(self, task_id: str) -> bool:
        """Execute assigned task."""
        task = self.tasks.get(task_id)
        if not task or not task.assigned_agent:
            return False

        agent = self.agents.get(task.assigned_agent)
        if not agent:
            return False

        try:
            # Execute task
            result = agent.run(task.description)

            # Update task
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()

            return True

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = f"Error: {str(e)}"
            return False

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status."""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}

        return {
            "id": task.id,
            "description": task.description,
            "status": task.status.value,
            "assigned_agent": task.assigned_agent,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "result": task.result
        }

    def get_agent_workload(self) -> Dict[str, Any]:
        """Get workload statistics for all agents."""
        workload = {}

        for agent_name in self.agents.keys():
            agent_tasks = [t for t in self.tasks.values() if t.assigned_agent == agent_name]

            workload[agent_name] = {
                "total_tasks": len(agent_tasks),
                "completed_tasks": len([t for t in agent_tasks if t.status == TaskStatus.COMPLETED]),
                "in_progress_tasks": len([t for t in agent_tasks if t.status == TaskStatus.IN_PROGRESS]),
                "pending_tasks": len([t for t in agent_tasks if t.status == TaskStatus.PENDING])
            }

        return workload

# Create task management system
task_manager = TaskManager({
    "ResearchAgent": researcher,
    "DataAnalyst": analyst,
    "ContentWriter": writer
})

# Create and execute tasks
task_descriptions = [
    "Research the latest trends in AI for 2024",
    "Analyze sales data and identify key patterns",
    "Write a blog post about machine learning best practices"
]

required_skills = [
    ["research"],
    ["analysis"],
    ["writing"]
]

print("Task Management Demonstration:")
for desc, skills in zip(task_descriptions, required_skills):
    # Create task
    task_id = task_manager.create_task(desc, required_skills=skills)

    # Assign task
    assigned = task_manager.assign_task(task_id)

    if assigned:
        print(f"✓ Task '{desc[:30]}...' assigned to {task_manager.tasks[task_id].assigned_agent}")

        # Execute task
        success = asyncio.run(task_manager.execute_task(task_id))
        status = task_manager.get_task_status(task_id)

        print(f"  Status: {status['status']}")
        print(f"  Result preview: {status['result'][:100] if status['result'] else 'None'}...")
    else:
        print(f"✗ Could not assign task: {desc[:30]}...")

    print()

# Show workload statistics
workload = task_manager.get_agent_workload()
print("Agent Workload:")
for agent, stats in workload.items():
    print(f"{agent}: {stats['completed_tasks']}/{stats['total_tasks']} tasks completed")
```

## Conflict Resolution and Consensus Building

### Agent Debate and Consensus

```python
class ConsensusBuilder:
    """Facilitates debate and consensus building among agents."""

    def __init__(self, agents: Dict[str, Agent], moderator: Agent):
        self.agents = agents
        self.moderator = moderator
        self.discussions: Dict[str, List[Dict[str, Any]]] = {}

    async def debate_topic(self, topic_id: str, topic: str, rounds: int = 3) -> Dict[str, Any]:
        """Conduct structured debate on a topic."""

        self.discussions[topic_id] = []

        # Initial positions
        initial_positions = {}
        for agent_name, agent in self.agents.items():
            prompt = f"""
            Take a clear position on this topic and provide your reasoning:

            Topic: {topic}

            Provide:
            1. Your position (support, oppose, or neutral)
            2. Key arguments supporting your position
            3. Any conditions that would change your position
            """

            position = agent.run(prompt)
            initial_positions[agent_name] = position

            self.discussions[topic_id].append({
                "round": 0,
                "agent": agent_name,
                "content": position,
                "type": "initial_position"
            })

        # Debate rounds
        for round_num in range(1, rounds + 1):
            for agent_name, agent in self.agents.items():
                # Get other agents' positions
                other_positions = {
                    name: pos for name, pos in initial_positions.items()
                    if name != agent_name
                }

                debate_prompt = f"""
                Based on the other agents' positions, refine your position on:

                Topic: {topic}

                Other agents' positions:
                {chr(10).join([f"{name}: {pos[:200]}..." for name, pos in other_positions.items()])}

                Round {round_num}: Consider the counterarguments and either:
                1. Strengthen your original position with additional arguments
                2. Modify your position based on compelling counterarguments
                3. Find common ground or areas of agreement

                Provide your updated position and reasoning.
                """

                updated_position = agent.run(debate_prompt)

                self.discussions[topic_id].append({
                    "round": round_num,
                    "agent": agent_name,
                    "content": updated_position,
                    "type": "debate_round"
                })

        # Moderator synthesizes consensus
        consensus_prompt = f"""
        Review this debate and determine if consensus can be reached:

        Topic: {topic}

        Debate summary:
        {self._summarize_discussion(topic_id)}

        Provide:
        1. Areas of agreement among agents
        2. Remaining points of disagreement
        3. Recommended consensus position (if possible)
        4. Any compromises or conditions for agreement
        """

        consensus = self.moderator.run(consensus_prompt)

        return {
            "topic": topic,
            "consensus": consensus,
            "discussion_summary": self._summarize_discussion(topic_id),
            "total_rounds": rounds,
            "participants": list(self.agents.keys())
        }

    def _summarize_discussion(self, topic_id: str) -> str:
        """Summarize the discussion for consensus building."""
        discussion = self.discussions.get(topic_id, [])

        summary_parts = []

        # Initial positions
        initial = [d for d in discussion if d["type"] == "initial_position"]
        summary_parts.append("Initial Positions:")
        for item in initial:
            summary_parts.append(f"  {item['agent']}: {item['content'][:150]}...")

        # Final positions
        final_round = max([d["round"] for d in discussion])
        final_positions = [d for d in discussion if d["round"] == final_round]

        summary_parts.append(f"\nFinal Positions (Round {final_round}):")
        for item in final_positions:
            summary_parts.append(f"  {item['agent']}: {item['content'][:150]}...")

        return "\n".join(summary_parts)

# Create debate system
debaters = {
    "EconomicAnalyst": Agent(
        name="EconomicAnalyst",
        instructions="You are an economic analyst. Consider economic impacts, costs, and financial implications.",
        model="gpt-4"
    ),
    "EnvironmentalExpert": Agent(
        name="EnvironmentalExpert",
        instructions="You are an environmental expert. Focus on ecological impacts and sustainability.",
        model="gpt-4"
    ),
    "SocialScientist": Agent(
        name="SocialScientist",
        instructions="You are a social scientist. Consider social impacts, equity, and community effects.",
        model="gpt-4"
    )
}

moderator = Agent(
    name="DebateModerator",
    instructions="You are an impartial debate moderator. Facilitate constructive discussion and find consensus.",
    model="gpt-4"
)

consensus_builder = ConsensusBuilder(debaters, moderator)

# Conduct debate
debate_topic = "Should cities implement congestion pricing for vehicles?"

debate_result = asyncio.run(consensus_builder.debate_topic(
    "congestion_pricing", debate_topic, rounds=2
))

print("Debate Results:")
print(f"Topic: {debate_result['topic']}")
print(f"Participants: {', '.join(debate_result['participants'])}")
print(f"Consensus: {debate_result['consensus'][:500]}...")
```

## Scalability and Performance

### Agent Pool Management

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

class AgentPool:
    """Manage a pool of agents for scalable task processing."""

    def __init__(self, agent_configs: List[Dict[str, Any]], max_concurrent: int = 5):
        self.agent_configs = agent_configs
        self.max_concurrent = max_concurrent
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self.active_agents: Dict[str, Agent] = {}

    def get_agent(self, agent_type: str) -> Agent:
        """Get or create agent of specified type."""
        if agent_type not in self.active_agents:
            config = next((c for c in self.agent_configs if c["type"] == agent_type), None)
            if not config:
                raise ValueError(f"Unknown agent type: {agent_type}")

            # Create agent (in practice, you'd pool/reuse agents)
            agent = Agent(
                name=f"{agent_type}_{len(self.active_agents)}",
                instructions=config["instructions"],
                model=config["model"]
            )

            self.active_agents[agent_type] = agent

        return self.active_agents[agent_type]

    async def process_tasks_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple tasks concurrently."""

        async def process_single_task(task: Dict[str, Any]):
            agent_type = task.get("agent_type", "general")
            agent = self.get_agent(agent_type)

            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                agent.run,
                task["description"]
            )

            return {
                "task_id": task["id"],
                "result": result,
                "agent_type": agent_type
            }

        # Process all tasks concurrently
        results = await asyncio.gather(*[process_single_task(task) for task in tasks])

        return results

# Define agent pool configurations
agent_pool_configs = [
    {
        "type": "researcher",
        "instructions": "You are a research specialist. Find and analyze information.",
        "model": "gpt-4"
    },
    {
        "type": "writer",
        "instructions": "You are a content writer. Create engaging written content.",
        "model": "gpt-4"
    },
    {
        "type": "analyst",
        "instructions": "You are a data analyst. Analyze data and provide insights.",
        "model": "gpt-4"
    },
    {
        "type": "coder",
        "instructions": "You are a programmer. Write and explain code.",
        "model": "gpt-4"
    }
]

# Create agent pool
agent_pool = AgentPool(agent_pool_configs, max_concurrent=3)

# Process batch of tasks
batch_tasks = [
    {"id": "task_1", "description": "Research the latest AI developments", "agent_type": "researcher"},
    {"id": "task_2", "description": "Write a blog post about machine learning", "agent_type": "writer"},
    {"id": "task_3", "description": "Analyze sales data trends", "agent_type": "analyst"},
    {"id": "task_4", "description": "Create a Python script for data processing", "agent_type": "coder"},
    {"id": "task_5", "description": "Research quantum computing applications", "agent_type": "researcher"}
]

print("Processing batch tasks...")
batch_results = asyncio.run(agent_pool.process_tasks_batch(batch_tasks))

print("Batch processing results:")
for result in batch_results:
    print(f"Task {result['task_id']} ({result['agent_type']}): {result['result'][:100]}...")

print(f"\nProcessed {len(batch_results)} tasks successfully")
```

This comprehensive multi-agent systems chapter demonstrates how to build collaborative agent teams with sophisticated coordination, communication, and task management capabilities. The modular architecture allows for easy scaling and specialization of agent roles. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `task`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Multi-Agent Systems - Coordinating Teams of AI Agents` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `message`, `name`, `agents` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Multi-Agent Systems - Coordinating Teams of AI Agents` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Memory Systems - Building Context-Aware Agents](04-memory-systems.md)
- [Next Chapter: Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving](06-advanced-reasoning.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
