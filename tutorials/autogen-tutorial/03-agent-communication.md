---
layout: default
title: "Chapter 3: Agent Communication"
parent: "Microsoft AutoGen Tutorial"
nav_order: 3
---

# Chapter 3: Agent Communication

Welcome to the fascinating world of agent communication! In this chapter, we'll explore how AutoGen agents communicate with each other, exchange information, and coordinate their actions. Effective communication is the foundation of successful multi-agent systems.

## Communication Fundamentals

### Message Structure

AutoGen uses a structured message format for agent communication:

```python
from typing import Dict, Any, List
from enum import Enum

class MessageType(Enum):
    TEXT = "text"
    FUNCTION_CALL = "function_call"
    FUNCTION_RESPONSE = "function_response"
    SYSTEM = "system"
    ERROR = "error"

class AgentMessage:
    def __init__(self, sender: str, receiver: str, content: Any, message_type: MessageType = MessageType.TEXT):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type
        self.timestamp = time.time()
        self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type.value,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        message = cls(
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            message_type=MessageType(data["message_type"])
        )
        message.timestamp = data["timestamp"]
        message.metadata = data["metadata"]
        return message
```

### Communication Protocols

```python
from autogen import AssistantAgent, UserProxyAgent
import asyncio

class CommunicationProtocol:
    def __init__(self):
        self.message_queue = asyncio.Queue()
        self.active_conversations = {}
        self.message_handlers = {}

    async def send_message(self, message: AgentMessage):
        """Send a message to the appropriate recipient"""
        await self.message_queue.put(message)

        # Log the message
        print(f"[{message.timestamp}] {message.sender} -> {message.receiver}: {message.content}")

    async def receive_message(self, agent_name: str) -> AgentMessage:
        """Receive a message for a specific agent"""
        while True:
            message = await self.message_queue.get()
            if message.receiver == agent_name or message.receiver == "all":
                return message
            else:
                # Put it back if it's not for this agent
                await self.message_queue.put(message)
                await asyncio.sleep(0.1)

    def register_handler(self, message_type: MessageType, handler):
        """Register a handler for specific message types"""
        self.message_handlers[message_type] = handler

    async def process_message(self, message: AgentMessage):
        """Process a message using registered handlers"""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            await handler(message)
        else:
            print(f"No handler found for message type: {message.message_type}")
```

## Basic Agent Communication

### One-on-One Conversations

```python
from autogen import AssistantAgent, UserProxyAgent
import os

# Set up agents
alice = AssistantAgent(
    name="Alice",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You are Alice, a friendly AI assistant."
)

bob = AssistantAgent(
    name="Bob",
    llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
    system_message="You are Bob, a knowledgeable AI assistant."
)

# Method 1: Direct conversation using initiate_chat
user_proxy = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER"
)

# Alice initiates conversation with Bob
result = user_proxy.initiate_chat(
    alice,
    message="Hi Bob, can you help me understand quantum computing?"
)

print("Conversation completed!")
print(f"Number of turns: {len(result.chat_history)}")

# Method 2: Manual message passing
def create_direct_conversation(agent1: AssistantAgent, agent2: AssistantAgent, initial_message: str):
    """Create a direct conversation between two agents"""
    messages = [{"role": "user", "content": initial_message}]

    # Agent 1 responds to initial message
    response1 = agent1.generate_reply(messages=messages)
    print(f"{agent1.name}: {response1}")
    messages.append({"role": "assistant", "content": response1})

    # Agent 2 responds to agent 1
    messages.append({"role": "user", "content": f"{agent1.name} said: {response1}"})
    response2 = agent2.generate_reply(messages=messages)
    print(f"{agent2.name}: {response2}")

    return [response1, response2]

# Create a conversation between Alice and Bob
conversation = create_direct_conversation(
    alice, bob,
    "Alice, what's your favorite programming language and why?"
)
```

### Multi-Agent Conversations

```python
from autogen import GroupChat, GroupChatManager

class MultiAgentConversation:
    def __init__(self, agents: List[AssistantAgent]):
        self.agents = agents
        self.conversation_history = []

    def create_group_chat(self, max_rounds: int = 5):
        """Create a group chat among agents"""
        groupchat = GroupChat(
            agents=self.agents,
            messages=[],
            max_round= max_rounds,
            speaker_selection_method="round_robin",
            allow_repeat_speaker=False
        )

        manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}
        )

        return manager

    def start_discussion(self, topic: str, max_rounds: int = 5):
        """Start a multi-agent discussion on a topic"""
        manager = self.create_group_chat(max_rounds)

        user_proxy = UserProxyAgent(
            name="DiscussionCoordinator",
            human_input_mode="NEVER",
            code_execution_config=False
        )

        result = user_proxy.initiate_chat(
            manager,
            message=f"Let's discuss: {topic}"
        )

        # Store conversation history
        self.conversation_history.append({
            "topic": topic,
            "participants": [agent.name for agent in self.agents],
            "messages": result.chat_history,
            "duration": len(result.chat_history)
        })

        return result

# Create a team of agents
research_team = [
    AssistantAgent(
        name="Researcher",
        llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
        system_message="You are a research specialist. You gather and analyze information."
    ),
    AssistantAgent(
        name="Analyst",
        llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
        system_message="You are a data analyst. You analyze information and draw insights."
    ),
    AssistantAgent(
        name="Writer",
        llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]},
        system_message="You are a content writer. You create clear, engaging content."
    )
]

# Start a multi-agent conversation
conversation_manager = MultiAgentConversation(research_team)
result = conversation_manager.start_discussion(
    "The impact of artificial intelligence on job markets",
    max_rounds=8
)

print(f"Discussion completed with {len(result.chat_history)} messages")
```

## Advanced Communication Patterns

### Structured Communication Protocols

```python
from enum import Enum
from typing import Dict, Any, List
import json

class CommunicationProtocol(Enum):
    REQUEST_RESPONSE = "request_response"
    PUBLISH_SUBSCRIBE = "publish_subscribe"
    BROADCAST = "broadcast"
    NEGOTIATION = "negotiation"

class StructuredCommunicator:
    def __init__(self):
        self.protocols = {}
        self.message_templates = {}

    def define_protocol(self, name: str, protocol_type: CommunicationProtocol, schema: Dict[str, Any]):
        """Define a communication protocol"""
        self.protocols[name] = {
            "type": protocol_type,
            "schema": schema,
            "validators": []
        }

    def create_message_template(self, protocol_name: str, template_name: str, template: Dict[str, Any]):
        """Create a message template for a protocol"""
        if protocol_name not in self.protocols:
            raise ValueError(f"Protocol {protocol_name} not defined")

        self.message_templates[f"{protocol_name}.{template_name}"] = template

    def send_structured_message(self, sender: str, receiver: str, protocol: str, template: str, data: Dict[str, Any]):
        """Send a structured message using a defined protocol and template"""
        if protocol not in self.protocols:
            raise ValueError(f"Protocol {protocol} not defined")

        template_key = f"{protocol}.{template}"
        if template_key not in self.message_templates:
            raise ValueError(f"Template {template} not found for protocol {protocol}")

        # Merge template with data
        message_template = self.message_templates[template_key]
        message_content = self._merge_template_data(message_template, data)

        # Validate message against protocol schema
        self._validate_message(protocol, message_content)

        # Create and send message
        message = AgentMessage(
            sender=sender,
            receiver=receiver,
            content=message_content,
            message_type=MessageType.TEXT
        )

        return message

    def _merge_template_data(self, template: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge template with actual data"""
        result = json.loads(json.dumps(template))  # Deep copy

        def merge_recursive(target, source):
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    merge_recursive(target[key], value)
                else:
                    target[key] = value

        merge_recursive(result, data)
        return result

    def _validate_message(self, protocol: str, message: Dict[str, Any]):
        """Validate message against protocol schema"""
        protocol_def = self.protocols[protocol]
        # Add validation logic here based on schema
        pass

# Usage example
communicator = StructuredCommunicator()

# Define a request-response protocol for task assignment
communicator.define_protocol("task_assignment", CommunicationProtocol.REQUEST_RESPONSE, {
    "type": "object",
    "properties": {
        "task_id": {"type": "string"},
        "description": {"type": "string"},
        "priority": {"type": "string"},
        "deadline": {"type": "string"}
    },
    "required": ["task_id", "description"]
})

# Create message templates
communicator.create_message_template("task_assignment", "assign_task", {
    "action": "assign_task",
    "task": {
        "id": "{task_id}",
        "description": "{description}",
        "priority": "{priority}",
        "deadline": "{deadline}"
    },
    "metadata": {
        "timestamp": "{timestamp}",
        "sender_role": "{sender_role}"
    }
})

# Send a structured message
message = communicator.send_structured_message(
    sender="Manager",
    receiver="Worker",
    protocol="task_assignment",
    template="assign_task",
    data={
        "task_id": "TASK-001",
        "description": "Analyze quarterly sales data",
        "priority": "high",
        "deadline": "2024-02-01",
        "timestamp": "2024-01-15T10:00:00Z",
        "sender_role": "project_manager"
    }
)
```

### Context-Aware Communication

```python
class ContextAwareCommunicator:
    def __init__(self):
        self.conversation_context = {}
        self.agent_states = {}
        self.relationship_graph = {}

    def update_context(self, agent_name: str, context: Dict[str, Any]):
        """Update conversation context for an agent"""
        if agent_name not in self.conversation_context:
            self.conversation_context[agent_name] = []

        self.conversation_context[agent_name].append({
            "timestamp": time.time(),
            "context": context
        })

        # Keep only recent context (last 10 entries)
        if len(self.conversation_context[agent_name]) > 10:
            self.conversation_context[agent_name].pop(0)

    def get_context(self, agent_name: str) -> Dict[str, Any]:
        """Get current context for an agent"""
        if agent_name not in self.conversation_context:
            return {}

        contexts = self.conversation_context[agent_name]
        if not contexts:
            return {}

        # Return most recent context
        return contexts[-1]["context"]

    def adapt_message_to_context(self, message: str, sender: str, receiver: str) -> str:
        """Adapt message based on conversation context"""
        receiver_context = self.get_context(receiver)

        # Adapt message based on receiver's state
        if receiver_context.get("busy", False):
            adapted_message = f"[URGENT] {message}"
        elif receiver_context.get("expertise_area"):
            expertise = receiver_context["expertise_area"]
            adapted_message = f"Regarding your expertise in {expertise}: {message}"
        else:
            adapted_message = message

        return adapted_message

    def build_relationship_context(self, agent1: str, agent2: str):
        """Build context based on agent relationships"""
        if agent1 not in self.relationship_graph:
            self.relationship_graph[agent1] = {}
        if agent2 not in self.relationship_graph:
            self.relationship_graph[agent2] = {}

        # Track interaction history
        if agent2 not in self.relationship_graph[agent1]:
            self.relationship_graph[agent1][agent2] = {
                "interactions": 0,
                "last_interaction": None,
                "relationship_strength": 0
            }

        self.relationship_graph[agent1][agent2]["interactions"] += 1
        self.relationship_graph[agent1][agent2]["last_interaction"] = time.time()

    def get_relationship_context(self, agent1: str, agent2: str) -> Dict[str, Any]:
        """Get relationship context between two agents"""
        if (agent1 in self.relationship_graph and
            agent2 in self.relationship_graph[agent1]):
            return self.relationship_graph[agent1][agent2]
        return {"interactions": 0, "relationship_strength": 0}

# Usage example
context_communicator = ContextAwareCommunicator()

# Update agent contexts
context_communicator.update_context("Alice", {
    "current_task": "data_analysis",
    "expertise_area": "machine_learning",
    "busy": False
})

context_communicator.update_context("Bob", {
    "current_task": "report_writing",
    "expertise_area": "technical_writing",
    "busy": True
})

# Build relationship context
context_communicator.build_relationship_context("Alice", "Bob")

# Adapt message based on context
original_message = "Can you help me with this analysis?"
adapted_message = context_communicator.adapt_message_to_context(
    original_message, "Alice", "Bob"
)

print(f"Adapted message: {adapted_message}")
# Output: "[URGENT] Can you help me with this analysis?" (because Bob is busy)
```

## Communication Strategies

### Turn-Taking Strategies

```python
from enum import Enum

class TurnTakingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    PRIORITY_BASED = "priority_based"
    RANDOM = "random"
    EXPERTISE_BASED = "expertise_based"

class ConversationManager:
    def __init__(self, agents: List[AssistantAgent], strategy: TurnTakingStrategy = TurnTakingStrategy.ROUND_ROBIN):
        self.agents = agents
        self.strategy = strategy
        self.current_turn = 0
        self.conversation_history = []

    def get_next_speaker(self) -> AssistantAgent:
        """Determine which agent should speak next"""
        if self.strategy == TurnTakingStrategy.ROUND_ROBIN:
            agent = self.agents[self.current_turn % len(self.agents)]
            self.current_turn += 1
            return agent

        elif self.strategy == TurnTakingStrategy.RANDOM:
            import random
            return random.choice(self.agents)

        elif self.strategy == TurnTakingStrategy.PRIORITY_BASED:
            # Sort agents by priority (implementation needed)
            return self._get_highest_priority_agent()

        elif self.strategy == TurnTakingStrategy.EXPERTISE_BASED:
            # Choose agent based on topic expertise
            return self._get_most_expert_agent()

    def _get_highest_priority_agent(self) -> AssistantAgent:
        """Get agent with highest priority"""
        # Implementation would check agent priorities
        return self.agents[0]

    def _get_most_expert_agent(self) -> AssistantAgent:
        """Get agent most qualified for current topic"""
        # Implementation would analyze conversation topic and agent expertise
        return self.agents[0]

    def facilitate_conversation(self, topic: str, max_turns: int = 10):
        """Facilitate a structured conversation"""
        messages = [{"role": "system", "content": f"Topic: {topic}"}]

        for turn in range(max_turns):
            speaker = self.get_next_speaker()
            print(f"\n--- Turn {turn + 1}: {speaker.name} ---")

            # Generate response
            response = speaker.generate_reply(messages=messages)
            print(f"{speaker.name}: {response}")

            # Add to conversation history
            messages.append({"role": "assistant", "content": f"{speaker.name}: {response}"})
            self.conversation_history.append({
                "turn": turn + 1,
                "speaker": speaker.name,
                "message": response
            })

        return self.conversation_history

# Usage
agents = [
    AssistantAgent(name="Expert1", llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}),
    AssistantAgent(name="Expert2", llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}),
    AssistantAgent(name="Expert3", llm_config={"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]})
]

manager = ConversationManager(agents, TurnTakingStrategy.ROUND_ROBIN)
history = manager.facilitate_conversation("AI ethics and responsible development", max_turns=6)
```

### Conflict Resolution

```python
class ConflictResolver:
    def __init__(self):
        self.conflict_patterns = {
            "contradictory_information": self._resolve_contradictory_info,
            "resource_contention": self._resolve_resource_contention,
            "opinion_disagreement": self._resolve_opinion_disagreement
        }

    def detect_conflict(self, messages: List[Dict[str, Any]]) -> str:
        """Detect type of conflict in messages"""
        # Analyze recent messages for conflict patterns
        recent_messages = messages[-5:]  # Last 5 messages

        for message in recent_messages:
            content = message.get("content", "").lower()

            if any(word in content for word in ["contradiction", "disagree", "opposite"]):
                return "contradictory_information"
            elif any(word in content for word in ["conflict", "contention", "competition"]):
                return "resource_contention"
            elif any(word in content for word in ["different opinion", "disagree", "alternative view"]):
                return "opinion_disagreement"

        return "no_conflict"

    def resolve_conflict(self, conflict_type: str, context: Dict[str, Any]) -> str:
        """Resolve detected conflict"""
        resolver = self.conflict_patterns.get(conflict_type)
        if resolver:
            return resolver(context)
        return "Unable to resolve conflict"

    def _resolve_contradictory_info(self, context: Dict[str, Any]) -> str:
        """Resolve contradictory information"""
        return """I notice there are conflicting viewpoints. Let me help clarify:

1. Each perspective has valid points
2. We should gather more evidence to determine accuracy
3. Consider the source credibility and recency of information
4. A combined approach might yield the best solution

Would anyone like to provide additional evidence or context?"""

    def _resolve_resource_contention(self, context: Dict[str, Any]) -> str:
        """Resolve resource contention"""
        return """There's a resource conflict. Here's how we can resolve it:

1. Prioritize based on urgency and importance
2. Consider resource sharing or sequential usage
3. Look for alternative resources
4. Establish clear ownership and usage guidelines

Let's discuss the priority and find a mutually beneficial solution."""

    def _resolve_opinion_disagreement(self, context: Dict[str, Any]) -> str:
        """Resolve opinion disagreement"""
        return """Different perspectives are valuable! Here's how to handle this:

1. Acknowledge the validity of different viewpoints
2. Focus on shared goals and objectives
3. Look for areas of agreement
4. Consider hybrid or compromise solutions
5. Document the decision-making process

What aspects of each approach are most important to our goals?"""

# Usage in conversation
conflict_resolver = ConflictResolver()

def enhanced_conversation_manager(messages: List[Dict[str, Any]], agents: List[AssistantAgent]):
    """Enhanced conversation with conflict resolution"""
    conflict_type = conflict_resolver.detect_conflict(messages)

    if conflict_type != "no_conflict":
        print(f"Conflict detected: {conflict_type}")

        # Add conflict resolution message
        resolution_message = conflict_resolver.resolve_conflict(conflict_type, {
            "messages": messages,
            "agents": [agent.name for agent in agents]
        })

        # Add resolution to conversation
        messages.append({
            "role": "system",
            "content": f"Conflict Resolution: {resolution_message}"
        })

    return messages
```

## Communication Monitoring and Analytics

```python
class CommunicationAnalytics:
    def __init__(self):
        self.message_stats = {}
        self.conversation_metrics = {}
        self.agent_interactions = {}

    def record_message(self, message: AgentMessage):
        """Record message for analytics"""
        sender = message.sender
        receiver = message.receiver

        # Update message statistics
        if sender not in self.message_stats:
            self.message_stats[sender] = {"sent": 0, "received": 0}

        if receiver not in self.message_stats:
            self.message_stats[receiver] = {"sent": 0, "received": 0}

        self.message_stats[sender]["sent"] += 1
        self.message_stats[receiver]["received"] += 1

        # Update interaction matrix
        if sender not in self.agent_interactions:
            self.agent_interactions[sender] = {}

        if receiver not in self.agent_interactions[sender]:
            self.agent_interactions[sender][receiver] = 0

        self.agent_interactions[sender][receiver] += 1

    def get_communication_summary(self) -> Dict[str, Any]:
        """Get summary of communication patterns"""
        return {
            "message_statistics": self.message_stats,
            "interaction_matrix": self.agent_interactions,
            "most_active_sender": self._get_most_active("sent"),
            "most_active_receiver": self._get_most_active("received"),
            "communication_efficiency": self._calculate_efficiency()
        }

    def _get_most_active(self, metric: str) -> str:
        """Get most active agent for a metric"""
        max_count = 0
        most_active = None

        for agent, stats in self.message_stats.items():
            if stats[metric] > max_count:
                max_count = stats[metric]
                most_active = agent

        return most_active

    def _calculate_efficiency(self) -> float:
        """Calculate communication efficiency"""
        total_messages = sum(stats["sent"] for stats in self.message_stats.values())
        total_interactions = sum(
            sum(interactions.values())
            for interactions in self.agent_interactions.values()
        )

        # Efficiency = meaningful interactions / total messages
        return total_interactions / total_messages if total_messages > 0 else 0

# Usage
analytics = CommunicationAnalytics()

# Record messages
analytics.record_message(AgentMessage("Alice", "Bob", "Hello Bob!"))
analytics.record_message(AgentMessage("Bob", "Alice", "Hi Alice!"))
analytics.record_message(AgentMessage("Alice", "Charlie", "Need help with analysis"))

# Get analytics
summary = analytics.get_communication_summary()
print("Communication Summary:")
print(f"- Most active sender: {summary['most_active_sender']}")
print(f"- Communication efficiency: {summary['communication_efficiency']:.2f}")
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Communication Fundamentals** - Message structure and protocols
2. **Basic Agent Communication** - One-on-one and multi-agent conversations
3. **Advanced Communication Patterns** - Structured protocols and context-aware messaging
4. **Communication Strategies** - Turn-taking and conflict resolution
5. **Communication Monitoring** - Analytics and performance tracking

## Next Steps

Now that you understand how agents communicate, let's explore how to integrate external tools and APIs. In [Chapter 4: Tool Integration](04-tool-integration.md), we'll learn how agents can use external tools to extend their capabilities and perform real-world actions.

---

**Practice what you've learned:**
1. Create a structured communication protocol for task assignment
2. Implement context-aware messaging between agents
3. Build a conflict resolution system for multi-agent conversations
4. Set up communication analytics to monitor agent interactions

*What kind of multi-agent conversation would you create first?* 🤖

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `message`, `messages` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Agent Communication` as an operating subsystem inside **Microsoft AutoGen Tutorial: Building Multi-Agent AI Systems**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `receiver`, `agents`, `sender` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Agent Communication` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `message` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `messages`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/microsoft/autogen)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `message` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Agent Architecture & Roles](02-agent-architecture.md)
- [Next Chapter: Chapter 4: Tool Integration](04-tool-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
