---
layout: default
title: "Letta Tutorial - Chapter 5: Conversation Management"
nav_order: 5
has_children: false
parent: Letta Tutorial
---

# Chapter 5: Conversation Management

Welcome to **Chapter 5: Conversation Management**. In this part of **Letta Tutorial: Stateful LLM Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Handle long-running dialogues, manage conversation state, and implement conversation patterns.

## Overview

Letta excels at managing long-term conversations. This chapter covers conversation lifecycle, state management, branching conversations, and implementing conversation patterns.

## Conversation Basics

Each conversation has a unique ID and maintains its own context:

```python
from letta import create_client

client = create_client()

# Start a new conversation
conversation = client.create_conversation(agent_name="sam")

print(f"Conversation ID: {conversation.id}")

# Send messages
response1 = client.send_message(
    agent_name="sam",
    message="Hello, let's discuss machine learning!",
    conversation_id=conversation.id
)

response2 = client.send_message(
    agent_name="sam",
    message="What are some good algorithms for classification?",
    conversation_id=conversation.id
)
```

## Conversation State

Track conversation metadata:

```python
# Get conversation details
conv = client.get_conversation(conversation.id)

print(f"Created: {conv.created_at}")
print(f"Last updated: {conv.updated_at}")
print(f"Message count: {conv.message_count}")
print(f"Summary: {conv.summary}")
```

## Message History

Access and search conversation history:

```python
# Get recent messages
messages = client.get_messages(
    agent_name="sam",
    conversation_id=conversation.id,
    limit=10
)

for msg in messages:
    print(f"{msg.role}: {msg.content[:50]}...")

# Search within conversation
results = client.search_messages(
    agent_name="sam",
    conversation_id=conversation.id,
    query="machine learning",
    limit=5
)
```

## Conversation Summarization

Automatically generate conversation summaries:

```python
# Enable auto-summarization
conversation = client.create_conversation(
    agent_name="sam",
    auto_summarize=True,
    summary_interval=20  # Summarize every 20 messages
)

# Or manually summarize
summary = client.summarize_conversation(
    agent_name="sam",
    conversation_id=conversation.id
)

print(f"Conversation summary: {summary}")
```

## Branching Conversations

Create conversation branches for exploring alternatives:

```python
# Start main conversation
main_conv = client.create_conversation(agent_name="writer")

# Branch from a specific point
branch_conv = client.branch_conversation(
    agent_name="writer",
    from_conversation_id=main_conv.id,
    from_message_id="msg_123"  # Branch from this message
)

# Continue different paths
client.send_message(
    agent_name="writer",
    message="Let's make the character more heroic",
    conversation_id=main_conv.id
)

client.send_message(
    agent_name="writer",
    message="Let's make the character more mysterious",
    conversation_id=branch_conv.id
)
```

## Conversation Templates

Save conversation starters for common scenarios:

```python
CONVERSATION_TEMPLATES = {
    "code-review": {
        "initial_message": "I'd like you to review this code. Please focus on best practices, security, and performance.",
        "system_context": "You are conducting a thorough code review."
    },
    "interview-practice": {
        "initial_message": "Let's practice a job interview. I'll be the candidate, you be the interviewer.",
        "system_context": "You are an experienced interviewer asking insightful questions."
    },
    "learning-session": {
        "initial_message": "I'm here to learn about [TOPIC]. Please explain concepts clearly and ask questions to check my understanding.",
        "system_context": "You are a patient teacher who adapts to the student's pace."
    }
}

def start_structured_conversation(agent_name, template_name, **kwargs):
    """Start a conversation from a template."""
    template = CONVERSATION_TEMPLATES[template_name]

    # Create conversation
    conversation = client.create_conversation(agent_name=agent_name)

    # Send initial message
    initial_msg = template["initial_message"]
    if kwargs:
        initial_msg = initial_msg.format(**kwargs)

    response = client.send_message(
        agent_name=agent_name,
        message=initial_msg,
        conversation_id=conversation.id
    )

    return conversation, response
```

## Long-Term Conversation Patterns

### Project-Based Conversations

```python
class ProjectConversation:
    def __init__(self, agent_name, project_name):
        self.agent_name = agent_name
        self.project_name = project_name
        self.conversation = client.create_conversation(
            agent_name=agent_name,
            metadata={"project": project_name, "type": "project"}
        )

    def send_project_message(self, message, context=None):
        """Send message with project context."""
        full_message = f"Project: {self.project_name}\n"
        if context:
            full_message += f"Context: {context}\n"
        full_message += f"Message: {message}"

        return client.send_message(
            agent_name=self.agent_name,
            message=full_message,
            conversation_id=self.conversation.id
        )

    def get_project_history(self, limit=50):
        """Get project-specific message history."""
        return client.get_messages(
            agent_name=self.agent_name,
            conversation_id=self.conversation.id,
            limit=limit
        )

# Usage
project_chat = ProjectConversation("coder", "web-app")
project_chat.send_project_message("Let's plan the database schema")
project_chat.send_project_message("What about user authentication?", "Following up on security requirements")
```

### Session-Based Learning

```python
class LearningSession:
    def __init__(self, agent_name, student_name, topic):
        self.agent_name = agent_name
        self.student_name = student_name
        self.topic = topic
        self.session_num = 1

        self.conversation = client.create_conversation(
            agent_name=agent_name,
            metadata={
                "student": student_name,
                "topic": topic,
                "session_type": "learning"
            }
        )

    def start_session(self):
        """Begin a learning session."""
        welcome = f"""Starting learning session #{self.session_num} on {self.topic}

Student: {self.student_name}

Please assess my current knowledge level and create a personalized learning plan."""

        response = client.send_message(
            agent_name=self.agent_name,
            message=welcome,
            conversation_id=self.conversation.id
        )

        self.session_num += 1
        return response

    def continue_session(self, student_input):
        """Continue the learning session."""
        return client.send_message(
            agent_name=self.agent_name,
            message=student_input,
            conversation_id=self.conversation.id
        )

# Usage
math_session = LearningSession("teacher", "Alice", "Calculus")
math_session.start_session()
math_session.continue_session("I'm struggling with derivatives")
```

## Conversation Archiving and Retrieval

Archive old conversations for reference:

```python
def archive_conversation(agent_name, conversation_id, archive_reason="completed"):
    """Archive a conversation."""
    client.update_conversation(
        agent_name=agent_name,
        conversation_id=conversation_id,
        metadata={"status": "archived", "archive_reason": archive_reason}
    )

def find_similar_conversations(agent_name, query, limit=5):
    """Find conversations similar to a query."""
    # Search across all conversations
    results = client.search_conversations(
        agent_name=agent_name,
        query=query,
        limit=limit
    )

    return results

# Archive completed project
archive_conversation("coder", "conv_123", "project_completed")

# Find similar past conversations
similar = find_similar_conversations("support", "password reset issue")
```

## Conversation Analytics

Analyze conversation patterns:

```python
def analyze_conversation(conversation_id):
    """Analyze conversation metrics."""
    messages = client.get_messages(
        agent_name="sam",  # Need to know agent name
        conversation_id=conversation_id,
        limit=1000
    )

    stats = {
        "total_messages": len(messages),
        "avg_message_length": sum(len(m.content) for m in messages) / len(messages),
        "conversation_duration": (messages[-1].created_at - messages[0].created_at).total_seconds(),
        "user_messages": len([m for m in messages if m.role == "user"]),
        "agent_messages": len([m for m in messages if m.role == "assistant"]),
    }

    return stats

# Get conversation insights
stats = analyze_conversation("conv_123")
print(f"Conversation lasted {stats['conversation_duration']/3600:.1f} hours")
```

## Multi-User Conversations

Handle conversations with multiple participants:

```python
class MultiUserConversation:
    def __init__(self, agent_name, participants):
        self.agent_name = agent_name
        self.participants = participants
        self.conversation = client.create_conversation(
            agent_name=agent_name,
            metadata={
                "participants": participants,
                "type": "multi_user"
            }
        )

    def add_message(self, user_name, message):
        """Add a message from a specific user."""
        if user_name not in self.participants:
            raise ValueError(f"User {user_name} not in participants")

        formatted_message = f"[{user_name}]: {message}"

        response = client.send_message(
            agent_name=self.agent_name,
            message=formatted_message,
            conversation_id=self.conversation.id
        )

        return response

# Usage
group_chat = MultiUserConversation("facilitator", ["Alice", "Bob", "Charlie"])
group_chat.add_message("Alice", "I think we should focus on the UI first")
group_chat.add_message("Bob", "I agree, but let's not forget about the API")
```

## Conversation Context Management

Maintain conversation context across sessions:

```python
def resume_conversation(agent_name, conversation_id, context_summary=None):
    """Resume a previous conversation."""
    if context_summary:
        # Add context summary to help agent remember
        client.send_message(
            agent_name=agent_name,
            message=f"Context summary: {context_summary}",
            conversation_id=conversation_id
        )

    return client.get_conversation(conversation_id)

def get_conversation_context(conversation_id, max_messages=10):
    """Get recent context for resuming."""
    messages = client.get_messages(
        agent_name="sam",  # Need agent name
        conversation_id=conversation_id,
        limit=max_messages
    )

    # Generate context summary
    context = "\n".join([f"{m.role}: {m.content}" for m in messages[-5:]])
    return context

# Resume with context
context = get_conversation_context("conv_123")
resume_conversation("sam", "conv_123", context)
```

## Best Practices

1. **Clear Conversation Boundaries**: Know when to start new conversations vs continuing existing ones
2. **Regular Summarization**: Keep conversations focused and manageable
3. **Metadata Management**: Tag conversations with relevant metadata for searching
4. **Archival Strategy**: Archive completed conversations to reduce active conversation load
5. **Context Preservation**: Use summaries and context when resuming conversations
6. **Participant Management**: Track conversation participants and their roles
7. **Performance Monitoring**: Monitor conversation length, engagement, and outcomes

Next: Coordinate multiple agents working together.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `agent_name`, `self`, `conversation` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Conversation Management` as an operating subsystem inside **Letta Tutorial: Stateful LLM Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `client`, `conversation_id`, `message` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Conversation Management` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `agent_name`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `conversation`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/letta-ai/letta)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `agent_name` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Tool Integration](04-tools.md)
- [Next Chapter: Chapter 6: Multi-Agent Systems](06-multi-agent.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
