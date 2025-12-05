---
layout: default
title: "AG2 Tutorial - Chapter 3: Conversation Patterns"
nav_order: 3
has_children: false
parent: AG2 Tutorial
---

# Chapter 3: Conversation Patterns

> Master the different ways AG2 agents can interact: two-agent chats, sequential workflows, and group collaborations.

## Overview

AG2 supports multiple conversation patterns that enable different types of agent interactions. Understanding these patterns is crucial for designing effective multi-agent systems.

## Two-Agent Conversations

### Basic Back-and-Forth Chat

The simplest pattern: direct conversation between two agents.

```python
from ag2 import AssistantAgent, UserProxyAgent

# Create agents
assistant = AssistantAgent(
    name="assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={"model": "gpt-4", "api_key": "your-key"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Write a Python function to calculate fibonacci numbers."
)
```

### Custom Message Handling

```python
class CustomAssistant(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message_count = 0

    def receive(self, message, sender, request_reply=None):
        self.message_count += 1
        print(f"Message {self.message_count} from {sender.name}: {message[:50]}...")

        # Custom logic based on message content
        if "error" in message.lower():
            print("Error detected - escalating...")
        elif "success" in message.lower():
            print("Success detected - continuing...")

        return super().receive(message, sender, request_reply)

custom_assistant = CustomAssistant(
    name="custom_assistant",
    llm_config=llm_config
)
```

## Sequential Conversations

### Agent-to-Agent Handoffs

Chain multiple agents in sequence, where each agent hands off to the next.

```python
from ag2 import AssistantAgent, UserProxyAgent

# Create specialized agents
researcher = AssistantAgent(
    name="researcher",
    system_message="Research and gather information on the given topic.",
    llm_config=llm_config
)

writer = AssistantAgent(
    name="writer",
    system_message="Create well-structured content based on research provided.",
    llm_config=llm_config
)

editor = AssistantAgent(
    name="editor",
    system_message="Review and improve content for clarity, accuracy, and style.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config=False
)

# Sequential conversation: researcher -> writer -> editor
def sequential_workflow(topic):
    # Phase 1: Research
    research_result = user_proxy.initiate_chat(
        researcher,
        message=f"Research the topic: {topic}. Provide key facts and insights.",
        max_turns=3
    )

    # Phase 2: Writing
    writing_result = user_proxy.initiate_chat(
        writer,
        message=f"Based on this research: {research_result}. Write a comprehensive article.",
        max_turns=5
    )

    # Phase 3: Editing
    final_result = user_proxy.initiate_chat(
        editor,
        message=f"Edit this article: {writing_result}. Improve clarity and flow.",
        max_turns=3
    )

    return final_result

# Execute workflow
result = sequential_workflow("Artificial Intelligence in Healthcare")
```

### Conditional Sequential Flow

```python
def conditional_sequential_workflow(query):
    # Initial assessment
    assessor = AssistantAgent(
        name="assessor",
        system_message="Assess the complexity and type of this query.",
        llm_config=llm_config
    )

    assessment = user_proxy.initiate_chat(
        assessor,
        message=f"Assess this query: {query}",
        max_turns=1
    )

    # Route based on assessment
    if "complex" in assessment.lower():
        # Use expert agents
        expert = AssistantAgent(
            name="expert",
            system_message="Handle complex technical queries.",
            llm_config=llm_config
        )
        result = user_proxy.initiate_chat(expert, message=query)

    elif "creative" in assessment.lower():
        # Use creative agents
        creative = AssistantAgent(
            name="creative",
            system_message="Handle creative and design queries.",
            llm_config=llm_config
        )
        result = user_proxy.initiate_chat(creative, message=query)

    else:
        # Use general assistant
        result = user_proxy.initiate_chat(assistant, message=query)

    return result
```

## Group Chat Conversations

### Basic Group Chat

Multiple agents collaborating in a single conversation.

```python
from ag2 import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create specialized agents
product_manager = AssistantAgent(
    name="product_manager",
    system_message="Focus on user needs, business value, and product strategy.",
    llm_config=llm_config
)

designer = AssistantAgent(
    name="designer",
    system_message="Focus on user experience, interface design, and usability.",
    llm_config=llm_config
)

developer = AssistantAgent(
    name="developer",
    system_message="Focus on technical implementation, architecture, and code quality.",
    llm_config=llm_config
)

qa_specialist = AssistantAgent(
    name="qa_specialist",
    system_message="Focus on quality assurance, testing, and reliability.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config=False
)

# Create group chat
group_chat = GroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin"  # Each agent speaks in turn
)

# Create group chat manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

# Start group discussion
user_proxy.initiate_chat(
    manager,
    message="Design and plan a mobile app for fitness tracking."
)
```

### Auto Speaker Selection

Let agents decide who should speak next based on the conversation.

```python
# Group chat with auto speaker selection
auto_group_chat = GroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=15,
    speaker_selection_method="auto",  # LLM decides who speaks next
    allow_repeat_speaker=False       # Prevent same agent speaking twice in a row
)

auto_manager = GroupChatManager(
    groupchat=auto_group_chat,
    llm_config=llm_config
)

# The LLM will automatically select the most appropriate agent for each turn
user_proxy.initiate_chat(
    auto_manager,
    message="Fix the bug in our user authentication system."
)
```

### Custom Speaker Selection

Implement your own logic for selecting speakers.

```python
class CustomGroupChat(GroupChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speaker_history = []
        self.phase = "planning"

    def select_speaker(self, last_speaker, selector):
        """Custom speaker selection based on project phase"""
        if self.phase == "planning" and "product_manager" not in self.speaker_history:
            self.phase = "design"
            return self.agent_by_name("product_manager")

        elif self.phase == "design" and "designer" not in self.speaker_history:
            self.phase = "development"
            return self.agent_by_name("designer")

        elif self.phase == "development" and "developer" not in self.speaker_history:
            self.phase = "testing"
            return self.agent_by_name("developer")

        elif self.phase == "testing" and "qa_specialist" not in self.speaker_history:
            return self.agent_by_name("qa_specialist")

        # Round-robin for continued discussion
        available_agents = [agent for agent in self.agents
                          if agent != last_speaker and agent != selector]
        return available_agents[0] if available_agents else selector

custom_group_chat = CustomGroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=20
)

custom_manager = GroupChatManager(
    groupchat=custom_group_chat,
    llm_config=llm_config
)
```

## Nested Conversations

### Hierarchical Agent Structures

Agents that can spawn sub-conversations with specialized sub-agents.

```python
class HierarchicalAgent(AssistantAgent):
    def __init__(self, sub_agents=None, **kwargs):
        super().__init__(**kwargs)
        self.sub_agents = sub_agents or []
        self.active_sub_conversation = None

    def initiate_sub_conversation(self, task, sub_agent):
        """Start a focused sub-conversation for a specific task"""
        if sub_agent in self.sub_agents:
            self.active_sub_conversation = {
                "task": task,
                "agent": sub_agent,
                "messages": []
            }
            return True
        return False

    def handle_complex_task(self, task):
        """Break complex task into sub-tasks and delegate"""
        if "design" in task.lower():
            self.initiate_sub_conversation(task, "designer")
        elif "code" in task.lower():
            self.initiate_sub_conversation(task, "developer")
        elif "test" in task.lower():
            self.initiate_sub_conversation(task, "qa_specialist")

# Create hierarchical agent
team_lead = HierarchicalAgent(
    name="team_lead",
    sub_agents=["designer", "developer", "qa_specialist"],
    system_message="I coordinate complex projects by delegating to specialists.",
    llm_config=llm_config
)

# Sub-agents
specialists = {
    "designer": designer,
    "developer": developer,
    "qa_specialist": qa_specialist
}
```

### Conversation Context Management

```python
class ContextManager:
    def __init__(self):
        self.conversations = {}
        self.active_contexts = []

    def create_context(self, conversation_id, agents, initial_message):
        """Create a new conversation context"""
        context = {
            "id": conversation_id,
            "agents": agents,
            "messages": [initial_message],
            "metadata": {
                "created_at": time.time(),
                "status": "active",
                "parent_context": None
            }
        }
        self.conversations[conversation_id] = context
        self.active_contexts.append(conversation_id)
        return context

    def fork_context(self, parent_id, new_agents, branch_message):
        """Create a sub-conversation from existing context"""
        parent_context = self.conversations[parent_id]
        child_id = f"{parent_id}_branch_{len(parent_context.get('children', []))}"

        child_context = {
            "id": child_id,
            "agents": new_agents,
            "messages": [branch_message],
            "metadata": {
                "created_at": time.time(),
                "status": "active",
                "parent_context": parent_id
            }
        }

        self.conversations[child_id] = child_context
        if "children" not in parent_context:
            parent_context["children"] = []
        parent_context["children"].append(child_id)

        return child_context

    def merge_context(self, child_id, parent_id):
        """Merge child conversation back into parent"""
        child_context = self.conversations[child_id]
        parent_context = self.conversations[parent_id]

        # Add summary to parent
        summary = f"Sub-conversation completed: {child_context['messages'][-1]}"
        parent_context["messages"].append(summary)

        child_context["metadata"]["status"] = "merged"
        if child_id in self.active_contexts:
            self.active_contexts.remove(child_id)

context_manager = ContextManager()
```

## Advanced Patterns

### Debate and Consensus

```python
def debate_consensus(topic, agents, rounds=3):
    """Agents debate a topic and reach consensus"""
    debate_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=rounds * len(agents),
        speaker_selection_method="round_robin"
    )

    debate_manager = GroupChatManager(
        groupchat=debate_chat,
        llm_config=llm_config
    )

    # Start debate
    user_proxy.initiate_chat(
        debate_manager,
        message=f"Debate the following topic and reach consensus: {topic}"
    )

    # Consensus round
    consensus_agent = AssistantAgent(
        name="consensus_builder",
        system_message="Synthesize the debate and find common ground.",
        llm_config=llm_config
    )

    consensus = user_proxy.initiate_chat(
        consensus_agent,
        message="Based on the debate above, what is the consensus?"
    )

    return consensus

# Debate example
debate_agents = [product_manager, designer, developer]
consensus = debate_consensus(
    "Should we use React Native or Flutter for our mobile app?",
    debate_agents
)
```

### Collaborative Problem Solving

```python
def collaborative_solve(problem, agent_team):
    """Agents collaborate to solve a complex problem"""
    # Phase 1: Problem Analysis
    analyst = AssistantAgent(
        name="problem_analyst",
        system_message="Break down complex problems into manageable components.",
        llm_config=llm_config
    )

    analysis = user_proxy.initiate_chat(
        analyst,
        message=f"Analyze this problem: {problem}"
    )

    # Phase 2: Solution Brainstorming
    brainstorm_chat = GroupChat(
        agents=agent_team,
        messages=[{"content": f"Based on this analysis: {analysis}. Brainstorm solutions.", "role": "user"}],
        max_round=8,
        speaker_selection_method="auto"
    )

    brainstorm_manager = GroupChatManager(
        groupchat=brainstorm_chat,
        llm_config=llm_config
    )

    user_proxy.initiate_chat(brainstorm_manager, message="Start brainstorming!")

    # Phase 3: Solution Selection
    selector = AssistantAgent(
        name="solution_selector",
        system_message="Evaluate options and recommend the best solution.",
        llm_config=llm_config
    )

    recommendation = user_proxy.initiate_chat(
        selector,
        message="Based on the brainstorming above, recommend the best solution."
    )

    return recommendation

# Collaborative problem solving
team = [product_manager, designer, developer, qa_specialist]
solution = collaborative_solve(
    "Our app crashes when users upload large files",
    team
)
```

## Best Practices

### Conversation Design
- **Clear Objectives**: Each conversation should have a clear goal
- **Appropriate Scope**: Don't try to solve too many things in one conversation
- **Agent Roles**: Ensure each agent has a distinct, non-overlapping role
- **Termination Conditions**: Define when conversations should end

### Group Chat Management
- **Size Matters**: Keep groups to 3-7 agents for optimal collaboration
- **Speaker Selection**: Use auto-selection for dynamic conversations
- **Turn Limits**: Set reasonable max_round limits to prevent runaway discussions
- **Facilitation**: Consider having a moderator agent to keep discussions on track

### Error Handling
- **Timeout Management**: Set appropriate timeouts for long conversations
- **Fallback Strategies**: Have backup plans when conversations stall
- **Recovery Mechanisms**: Ability to restart or redirect stuck conversations

### Performance Optimization
- **Message Limits**: Limit conversation history to prevent token bloat
- **Caching**: Cache common responses and agent configurations
- **Async Processing**: Use async patterns for concurrent agent processing
- **Resource Monitoring**: Track token usage and computational resources

## Summary

In this chapter, we've covered:

- **Two-Agent Conversations**: Basic back-and-forth and custom message handling
- **Sequential Conversations**: Agent handoffs and conditional workflows
- **Group Chat**: Round-robin, auto-selection, and custom speaker selection
- **Nested Conversations**: Hierarchical structures and context management
- **Advanced Patterns**: Debate/consensus and collaborative problem solving
- **Best Practices**: Design principles, management strategies, and optimization

Next, we'll explore **code execution** - how to safely run code within AG2 conversations.

---

**Ready for the next chapter?** [Chapter 4: Code Execution](04-code-execution.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*