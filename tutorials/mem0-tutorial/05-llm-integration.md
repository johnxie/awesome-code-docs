---
layout: default
title: "Chapter 5: Integrating with LLMs"
parent: "Mem0 Tutorial"
nav_order: 5
---

# Chapter 5: Integrating with LLMs

Welcome to **Chapter 5: Integrating with LLMs**. In this part of **Mem0 Tutorial: Building Production-Ready AI Agents with Scalable Long-Term Memory**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Seamlessly connect Mem0 with various Large Language Models for enhanced AI agent capabilities.

## 🎯 Overview

This chapter covers integrating Mem0 with different LLM providers, implementing memory-augmented conversations, and building sophisticated AI agents that leverage persistent memory for more intelligent and personalized interactions.

## 🤖 LLM Provider Integration

### OpenAI Integration

```python
from mem0 import Memory
from openai import OpenAI
import json

class OpenAIMemoryIntegration:
    """Integrate Mem0 with OpenAI models"""

    def __init__(self, openai_api_key: str):
        self.memory = Memory()
        self.client = OpenAI(api_key=openai_api_key)

    def memory_augmented_completion(self, user_message: str, user_id: str = None,
                                  model: str = "gpt-4", temperature: float = 0.7) -> str:
        """Generate completion with memory context"""

        # Retrieve relevant memories
        relevant_memories = self.memory.search(user_message, user_id=user_id, limit=5)

        # Build context from memories
        memory_context = self._build_memory_context(relevant_memories)

        # Create enhanced prompt
        system_prompt = f"""You are a helpful AI assistant with access to the user's memory and preferences.

MEMORY CONTEXT:
{memory_context}

Use this context to provide personalized, relevant responses. Reference past interactions when appropriate, but don't explicitly mention "memory" unless asked."""

        # Generate response
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=1000
        )

        ai_response = response.choices[0].message.content

        # Store the interaction in memory
        self._store_interaction(user_message, ai_response, user_id)

        return ai_response

    def _build_memory_context(self, memories: list) -> str:
        """Build context string from memories"""

        if not memories:
            return "No previous interactions found."

        context_parts = []
        for i, mem in enumerate(memories[:3]):  # Limit to top 3
            context_parts.append(f"{i+1}. {mem['content']}")

        return "\n".join(context_parts)

    def _store_interaction(self, user_message: str, ai_response: str, user_id: str = None):
        """Store interaction in memory"""

        # Store user message
        self.memory.add(
            f"User asked: {user_message}",
            user_id=user_id,
            metadata={
                "interaction_type": "user_message",
                "timestamp": time.time(),
                "message_length": len(user_message)
            }
        )

        # Store AI response
        self.memory.add(
            f"AI responded: {ai_response}",
            user_id=user_id,
            metadata={
                "interaction_type": "ai_response",
                "timestamp": time.time(),
                "response_length": len(ai_response)
            }
        )

    def memory_enhanced_chat(self, conversation_history: list, user_id: str = None) -> str:
        """Continue conversation with memory enhancement"""

        # Extract current user message
        current_message = conversation_history[-1]["content"] if conversation_history else ""

        # Get memory context
        memory_context = self._get_conversation_memory_context(conversation_history, user_id)

        # Build enhanced conversation
        system_prompt = f"""You are continuing a conversation. Use the following memory context to maintain continuity and personalization:

MEMORY CONTEXT:
{memory_context}

Continue the conversation naturally, referencing previous topics when relevant."""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)

        # Generate response
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.8,
            max_tokens=800
        )

        ai_response = response.choices[0].message.content

        # Store new interaction
        self._store_interaction(current_message, ai_response, user_id)

        return ai_response

    def _get_conversation_memory_context(self, conversation_history: list, user_id: str = None) -> str:
        """Get memory context relevant to the conversation"""

        if not conversation_history:
            return "No conversation history available."

        # Extract topics from recent conversation
        recent_messages = conversation_history[-4:]  # Last 4 messages
        conversation_text = " ".join([msg["content"] for msg in recent_messages])

        # Search for related memories
        related_memories = self.memory.search(conversation_text, user_id=user_id, limit=3)

        if not related_memories:
            return "No relevant memories found for this conversation."

        context_parts = ["Related information from memory:"]
        for mem in related_memories:
            context_parts.append(f"- {mem['content']}")

        return "\n".join(context_parts)

# Usage
openai_integration = OpenAIMemoryIntegration(openai_api_key="your-api-key")

# Memory-augmented completion
response = openai_integration.memory_augmented_completion(
    "What's my favorite programming language?",
    user_id="user123"
)
print(f"Memory-enhanced response: {response}")

# Memory-enhanced chat
conversation = [
    {"role": "user", "content": "I love Python programming"},
    {"role": "assistant", "content": "That's great! Python is indeed a powerful language."},
    {"role": "user", "content": "What other languages should I learn?"}
]

chat_response = openai_integration.memory_enhanced_chat(conversation, user_id="user123")
print(f"Chat response: {chat_response}")
```

### Anthropic Claude Integration

```python
import anthropic
from mem0 import Memory

class ClaudeMemoryIntegration:
    """Integrate Mem0 with Anthropic Claude"""

    def __init__(self, anthropic_api_key: str):
        self.memory = Memory()
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)

    def claude_memory_conversation(self, user_message: str, user_id: str = None,
                                 model: str = "claude-3-sonnet-20240229") -> str:
        """Have conversation with Claude using memory context"""

        # Retrieve relevant memories
        memories = self.memory.search(user_message, user_id=user_id, limit=4)

        # Build memory context
        memory_context = self._format_memory_for_claude(memories)

        # Create system prompt
        system_prompt = f"""You are Claude, an AI assistant created by Anthropic. You have access to the user's memory and interaction history.

MEMORY CONTEXT:
{memory_context}

Use this context to provide personalized, helpful responses. Reference the user's preferences and past interactions when relevant, but keep responses natural and not overly mechanical."""

        # Generate response
        response = self.client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = response.content[0].text

        # Store interaction
        self._store_claude_interaction(user_message, ai_response, user_id)

        return ai_response

    def _format_memory_for_claude(self, memories: list) -> str:
        """Format memories for Claude's context window"""

        if not memories:
            return "No memory context available."

        formatted_memories = []
        for i, mem in enumerate(memories):
            # Claude works well with structured context
            formatted_memories.append(f"Memory {i+1}: {mem['content']}")

        context = "\n".join(formatted_memories)

        # Add usage guidance for Claude
        context += "\n\nUse this information to personalize your response while maintaining natural conversation flow."

        return context

    def _store_claude_interaction(self, user_message: str, ai_response: str, user_id: str = None):
        """Store Claude interaction in memory"""

        # Store user message
        self.memory.add(
            f"User query: {user_message}",
            user_id=user_id,
            metadata={
                "ai_provider": "claude",
                "interaction_type": "user_query",
                "model": "claude-3-sonnet-20240229"
            }
        )

        # Store AI response
        self.memory.add(
            f"Claude response: {ai_response}",
            user_id=user_id,
            metadata={
                "ai_provider": "claude",
                "interaction_type": "ai_response",
                "model": "claude-3-sonnet-20240229"
            }
        )

    def compare_memory_usage(self, query: str, user_id: str = None) -> dict:
        """Compare responses with and without memory"""

        # Response without memory
        basic_response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.7,
            messages=[{"role": "user", "content": query}]
        ).content[0].text

        # Response with memory
        memory_response = self.claude_memory_conversation(query, user_id)

        return {
            "query": query,
            "basic_response": basic_response,
            "memory_response": memory_response,
            "basic_length": len(basic_response),
            "memory_length": len(memory_response),
            "has_memory_context": len(self.memory.search(query, user_id=user_id, limit=1)) > 0
        }

# Usage
claude_integration = ClaudeMemoryIntegration(anthropic_api_key="your-api-key")

# Memory-enhanced Claude conversation
response = claude_integration.claude_memory_conversation(
    "What's my preferred coding style?",
    user_id="developer456"
)
print(f"Claude with memory: {response}")

# Compare with/without memory
comparison = claude_integration.compare_memory_usage(
    "How do I usually approach debugging?",
    user_id="developer456"
)
print(f"Comparison - Basic: {comparison['basic_length']} chars, Memory: {comparison['memory_length']} chars")
```

### Multiple LLM Provider Support

```python
from typing import Dict, List, Any, Optional
import asyncio

class MultiLLMMemoryIntegration:
    """Integrate Mem0 with multiple LLM providers"""

    def __init__(self, providers_config: Dict[str, Dict[str, Any]]):
        self.memory = Memory()
        self.providers = {}

        # Initialize providers
        for provider_name, config in providers_config.items():
            if provider_name == "openai":
                from openai import OpenAI
                self.providers[provider_name] = OpenAI(api_key=config["api_key"])
            elif provider_name == "anthropic":
                import anthropic
                self.providers[provider_name] = anthropic.Anthropic(api_key=config["api_key"])
            elif provider_name == "ollama":
                # For local models
                self.providers[provider_name] = {"base_url": config["base_url"]}

        self.provider_performance = {}

    def route_to_best_provider(self, query: str, user_id: str = None,
                             context_requirements: Dict[str, Any] = None) -> str:
        """Route query to the best available provider based on context"""

        # Analyze query and context
        query_analysis = self._analyze_query_requirements(query, context_requirements)

        # Get relevant memories
        memories = self.memory.search(query, user_id=user_id, limit=3)

        # Route based on requirements
        if query_analysis["requires_creativity"] and "anthropic" in self.providers:
            return "anthropic"  # Claude for creative tasks
        elif query_analysis["requires_reasoning"] and "openai" in self.providers:
            return "openai"  # GPT-4 for complex reasoning
        elif query_analysis["requires_speed"] and "ollama" in self.providers:
            return "ollama"  # Local models for speed
        else:
            # Default to first available
            return next(iter(self.providers.keys()))

    def _analyze_query_requirements(self, query: str, context_requirements: Dict[str, Any] = None) -> Dict[str, bool]:
        """Analyze what capabilities the query requires"""

        requirements = {
            "requires_creativity": False,
            "requires_reasoning": False,
            "requires_speed": False,
            "requires_memory": False
        }

        query_lower = query.lower()

        # Creativity indicators
        if any(word in query_lower for word in ["create", "design", "imagine", "write", "generate"]):
            requirements["requires_creativity"] = True

        # Reasoning indicators
        if any(word in query_lower for word in ["explain", "analyze", "compare", "why", "how"]):
            requirements["requires_reasoning"] = True

        # Speed requirements (from context)
        if context_requirements and context_requirements.get("priority") == "high":
            requirements["requires_speed"] = True

        # Memory requirements
        if any(word in query_lower for word in ["remember", "recall", "previously", "before"]):
            requirements["requires_memory"] = True

        return requirements

    async def multi_provider_query(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """Query multiple providers and compare results"""

        # Get memory context
        memories = self.memory.search(query, user_id=user_id, limit=3)
        memory_context = "\n".join([mem["content"] for mem in memories])

        results = {}

        # Query each provider
        for provider_name, provider in self.providers.items():
            try:
                if provider_name == "openai":
                    response = await self._query_openai(query, memory_context, provider)
                elif provider_name == "anthropic":
                    response = await self._query_anthropic(query, memory_context, provider)
                elif provider_name == "ollama":
                    response = await self._query_ollama(query, memory_context, provider)

                results[provider_name] = {
                    "response": response,
                    "success": True,
                    "response_time": time.time()
                }

                # Store performance metrics
                self._update_provider_performance(provider_name, True, time.time())

            except Exception as e:
                results[provider_name] = {
                    "error": str(e),
                    "success": False
                }
                self._update_provider_performance(provider_name, False, time.time())

        # Determine best response
        best_provider = self._select_best_response(results)

        return {
            "query": query,
            "best_response": results[best_provider]["response"] if best_provider else None,
            "best_provider": best_provider,
            "all_responses": results,
            "memory_used": len(memories) > 0
        }

    async def _query_openai(self, query: str, memory_context: str, client) -> str:
        """Query OpenAI with memory context"""
        prompt = f"Context: {memory_context}\n\nQuestion: {query}" if memory_context else query

        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
        )

        return response.choices[0].message.content

    async def _query_anthropic(self, query: str, memory_context: str, client) -> str:
        """Query Anthropic with memory context"""
        prompt = f"Context: {memory_context}\n\nQuestion: {query}" if memory_context else query

        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
        )

        return response.content[0].text

    async def _query_ollama(self, query: str, memory_context: str, config: dict) -> str:
        """Query Ollama local model"""
        import requests

        prompt = f"Context: {memory_context}\n\nQuestion: {query}" if memory_context else query

        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: requests.post(
                f"{config['base_url']}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": prompt,
                    "stream": False
                }
            )
        )

        return response.json()["response"]

    def _update_provider_performance(self, provider: str, success: bool, timestamp: float):
        """Update provider performance metrics"""

        if provider not in self.provider_performance:
            self.provider_performance[provider] = {
                "total_queries": 0,
                "successful_queries": 0,
                "average_response_time": 0,
                "last_used": None
            }

        perf = self.provider_performance[provider]
        perf["total_queries"] += 1
        perf["last_used"] = timestamp

        if success:
            perf["successful_queries"] += 1

        # Update success rate
        perf["success_rate"] = perf["successful_queries"] / perf["total_queries"]

    def _select_best_response(self, results: Dict[str, Any]) -> Optional[str]:
        """Select the best response based on criteria"""

        # Simple selection: prefer successful responses, then by provider preference
        successful_providers = [
            provider for provider, result in results.items()
            if result.get("success", False)
        ]

        if not successful_providers:
            return None

        # Provider preference order
        preference_order = ["openai", "anthropic", "ollama"]

        for preferred in preference_order:
            if preferred in successful_providers:
                return preferred

        # Fallback to first successful
        return successful_providers[0]

    def get_provider_analytics(self) -> Dict[str, Any]:
        """Get analytics about provider performance"""

        analytics = {
            "total_providers": len(self.providers),
            "provider_performance": self.provider_performance,
            "most_reliable": None,
            "fastest_average": None
        }

        if self.provider_performance:
            # Find most reliable
            analytics["most_reliable"] = max(
                self.provider_performance.items(),
                key=lambda x: x[1]["success_rate"]
            )[0]

        return analytics

# Usage
providers_config = {
    "openai": {"api_key": "your-openai-key"},
    "anthropic": {"api_key": "your-anthropic-key"},
    "ollama": {"base_url": "http://localhost:11434"}
}

multi_llm = MultiLLMMemoryIntegration(providers_config)

# Route to best provider
query = "Create a creative story about AI"
best_provider = multi_llm.route_to_best_provider(query)
print(f"Routed to: {best_provider}")

# Multi-provider comparison
async def run_comparison():
    results = await multi_llm.multi_provider_query(
        "What's the most important thing I should remember about machine learning?",
        user_id="researcher789"
    )

    print(f"Best provider: {results['best_provider']}")
    print(f"Memory used: {results['memory_used']}")

# Run comparison
asyncio.run(run_comparison())

# Get analytics
analytics = multi_llm.get_provider_analytics()
print(f"Provider analytics: {analytics}")
```

## 🔄 Memory-Augmented Conversations

### Conversation Memory Management

```python
class ConversationMemoryManager:
    """Manage memory across conversation sessions"""

    def __init__(self):
        self.memory = Memory()
        self.active_conversations = {}

    def start_conversation(self, user_id: str, conversation_id: str = None) -> str:
        """Start a new conversation session"""

        if not conversation_id:
            conversation_id = f"conv_{user_id}_{int(time.time())}"

        self.active_conversations[conversation_id] = {
            "user_id": user_id,
            "start_time": time.time(),
            "message_count": 0,
            "topics_discussed": set(),
            "memory_references": []
        }

        # Store conversation start in memory
        self.memory.add(
            f"Started new conversation session: {conversation_id}",
            user_id=user_id,
            metadata={
                "conversation_id": conversation_id,
                "event_type": "conversation_start",
                "session_type": "interactive"
            }
        )

        return conversation_id

    def add_message_to_conversation(self, conversation_id: str, role: str,
                                  content: str, metadata: Dict[str, Any] = None):
        """Add a message to the conversation and update memory"""

        if conversation_id not in self.active_conversations:
            raise ValueError(f"Conversation {conversation_id} not found")

        conv_data = self.active_conversations[conversation_id]
        conv_data["message_count"] += 1

        # Extract topics from message
        topics = self._extract_topics(content)
        conv_data["topics_discussed"].update(topics)

        # Store message in memory
        memory_content = f"Conversation {conversation_id} - {role}: {content}"

        memory_metadata = {
            "conversation_id": conversation_id,
            "message_role": role,
            "message_number": conv_data["message_count"],
            "topics": list(topics),
            "session_active": True
        }

        if metadata:
            memory_metadata.update(metadata)

        memory_id = self.memory.add(memory_content, user_id=conv_data["user_id"], metadata=memory_metadata)

        # Track memory reference
        conv_data["memory_references"].append(memory_id)

        return memory_id

    def get_conversation_context(self, conversation_id: str, max_messages: int = 5) -> str:
        """Get conversation context from memory"""

        if conversation_id not in self.active_conversations:
            return "No active conversation context available."

        conv_data = self.active_conversations[conversation_id]

        # Retrieve recent messages from this conversation
        conversation_memories = self.memory.search(
            f"conversation {conversation_id}",
            user_id=conv_data["user_id"],
            limit=max_messages
        )

        # Sort by message number
        conversation_memories.sort(
            key=lambda x: x.get("metadata", {}).get("message_number", 0)
        )

        # Build context
        context_parts = [f"Conversation Context (last {len(conversation_memories)} messages):"]

        for mem in conversation_memories:
            role = mem.get("metadata", {}).get("message_role", "unknown")
            content = mem["content"].replace(f"Conversation {conversation_id} - {role}: ", "")
            context_parts.append(f"{role.title()}: {content}")

        return "\n".join(context_parts)

    def _extract_topics(self, message: str) -> set:
        """Extract topics from message content"""

        # Simple topic extraction
        topics = set()

        # Common topics in AI/tech conversations
        topic_keywords = {
            "machine_learning": ["machine learning", "ml", "model", "training"],
            "programming": ["python", "code", "programming", "function", "class"],
            "ai": ["artificial intelligence", "ai", "neural network", "deep learning"],
            "data": ["data", "database", "dataset", "analytics"],
            "cloud": ["aws", "azure", "gcp", "cloud", "kubernetes"],
            "web": ["api", "rest", "frontend", "backend", "react", "vue"]
        }

        message_lower = message.lower()

        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.add(topic)

        return topics

    def end_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """End conversation and summarize"""

        if conversation_id not in self.active_conversations:
            return {"error": "Conversation not found"}

        conv_data = self.active_conversations[conversation_id]

        # Calculate conversation statistics
        duration = time.time() - conv_data["start_time"]
        summary = {
            "conversation_id": conversation_id,
            "user_id": conv_data["user_id"],
            "duration_seconds": duration,
            "message_count": conv_data["message_count"],
            "topics_discussed": list(conv_data["topics_discussed"]),
            "memories_created": len(conv_data["memory_references"]),
            "end_time": time.time()
        }

        # Store conversation summary in memory
        summary_content = f"""Conversation Summary:
- Duration: {duration:.1f} seconds
- Messages: {summary['message_count']}
- Topics: {', '.join(summary['topics_discussed'])}
- Memory entries created: {summary['memories_created']}"""

        self.memory.add(
            summary_content,
            user_id=conv_data["user_id"],
            metadata={
                "conversation_id": conversation_id,
                "event_type": "conversation_end",
                "summary": summary
            }
        )

        # Clean up active conversation
        del self.active_conversations[conversation_id]

        return summary

    def get_user_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's conversation history"""

        # Search for conversation summaries
        conversation_summaries = self.memory.search(
            "conversation summary",
            user_id=user_id,
            limit=limit
        )

        history = []
        for summary in conversation_summaries:
            metadata = summary.get("metadata", {})
            if metadata.get("event_type") == "conversation_end":
                history.append({
                    "conversation_id": metadata.get("conversation_id"),
                    "summary": metadata.get("summary", {}),
                    "timestamp": metadata.get("created_at", summary.get("created_at"))
                })

        # Sort by timestamp
        history.sort(key=lambda x: x["timestamp"] or 0, reverse=True)

        return history

# Usage
conv_manager = ConversationMemoryManager()

# Start conversation
conversation_id = conv_manager.start_conversation("user123")

# Add messages
conv_manager.add_message_to_conversation(
    conversation_id, "user", "Hi, I need help with machine learning"
)

conv_manager.add_message_to_conversation(
    conversation_id, "assistant", "I'd be happy to help with machine learning! What specific aspect are you interested in?"
)

conv_manager.add_message_to_conversation(
    conversation_id, "user", "I'm interested in neural networks and Python programming"
)

# Get conversation context
context = conv_manager.get_conversation_context(conversation_id)
print(f"Conversation Context:\n{context}")

# End conversation
summary = conv_manager.end_conversation(conversation_id)
print(f"Conversation Summary: {summary}")

# Get user history
history = conv_manager.get_user_conversation_history("user123", limit=5)
print(f"User has {len(history)} past conversations")
```

## 🤖 Advanced Agent Patterns

### Memory-Enabled AI Agent

```python
class MemoryEnabledAIAgent:
    """AI agent with integrated memory capabilities"""

    def __init__(self, llm_provider="openai", memory_config=None):
        self.memory = Memory()
        self.llm_provider = llm_provider
        self.conversation_manager = ConversationMemoryManager()

        # Initialize LLM client
        if llm_provider == "openai":
            from openai import OpenAI
            self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif llm_provider == "anthropic":
            import anthropic
            self.llm = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        self.active_conversations = {}

    def start_interaction(self, user_id: str) -> str:
        """Start a new interaction session"""

        conversation_id = self.conversation_manager.start_conversation(user_id)

        # Get user's memory context
        user_memories = self.memory.search("", user_id=user_id, limit=5)
        memory_context = self._format_memory_context(user_memories)

        welcome_message = f"""Hello! I'm your AI assistant with memory of our previous interactions.

Here's what I remember about you:
{memory_context}

How can I help you today?"""

        # Store welcome message
        self.conversation_manager.add_message_to_conversation(
            conversation_id, "assistant", welcome_message
        )

        self.active_conversations[user_id] = conversation_id

        return welcome_message

    def _format_memory_context(self, memories: list) -> str:
        """Format memory context for display"""

        if not memories:
            return "We haven't interacted before, so I'm getting to know you!"

        context_parts = []
        for i, mem in enumerate(memories[:3]):
            # Clean up memory content for display
            content = mem["content"]
            # Remove technical prefixes if present
            if content.startswith("User") or content.startswith("AI"):
                content = content.split(": ", 1)[-1] if ": " in content else content

            context_parts.append(f"• {content[:100]}{'...' if len(content) > 100 else ''}")

        return "\n".join(context_parts)

    def process_message(self, user_id: str, message: str) -> str:
        """Process user message with memory context"""

        # Get or create conversation
        if user_id not in self.active_conversations:
            self.start_interaction(user_id)

        conversation_id = self.active_conversations[user_id]

        # Add user message to conversation
        self.conversation_manager.add_message_to_conversation(
            conversation_id, "user", message
        )

        # Get conversation context
        conversation_context = self.conversation_manager.get_conversation_context(conversation_id)

        # Search for relevant memories
        relevant_memories = self.memory.search(message, user_id=user_id, limit=3)
        memory_context = self._build_memory_prompt(relevant_memories)

        # Generate response
        response = self._generate_response(message, conversation_context, memory_context)

        # Add response to conversation
        self.conversation_manager.add_message_to_conversation(
            conversation_id, "assistant", response
        )

        # Store interaction in memory
        self._store_interaction_memory(user_id, message, response)

        return response

    def _build_memory_prompt(self, memories: list) -> str:
        """Build memory context for LLM prompt"""

        if not memories:
            return "No specific memories found for this topic."

        memory_parts = ["Based on our previous interactions:"]

        for mem in memories:
            # Extract relevant content
            content = mem["content"]
            # Focus on user preferences and facts
            if any(keyword in content.lower() for keyword in ["prefer", "like", "usually", "typically", "favorite"]):
                memory_parts.append(f"- {content}")

        if len(memory_parts) == 1:
            return "I don't have specific memories directly related to this topic."

        return "\n".join(memory_parts)

    def _generate_response(self, message: str, conversation_context: str, memory_context: str) -> str:
        """Generate response using LLM with memory context"""

        system_prompt = f"""You are a helpful AI assistant with memory of user interactions.

{memory_context}

{conversation_context}

Respond naturally and reference relevant memories when appropriate. Be conversational and helpful."""

        if self.llm_provider == "openai":
            response = self.llm.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.8,
                max_tokens=800
            )
            return response.choices[0].message.content

        elif self.llm_provider == "anthropic":
            response = self.llm.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=800,
                temperature=0.8,
                system=system_prompt,
                messages=[{"role": "user", "content": message}]
            )
            return response.content[0].text

    def _store_interaction_memory(self, user_id: str, user_message: str, ai_response: str):
        """Store interaction details in memory"""

        # Store user query pattern
        self.memory.add(
            f"User asked about: {user_message[:100]}{'...' if len(user_message) > 100 else ''}",
            user_id=user_id,
            metadata={
                "interaction_type": "query",
                "topic": self._extract_main_topic(user_message),
                "query_length": len(user_message)
            }
        )

        # Store AI response pattern
        self.memory.add(
            f"AI provided information about: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}",
            user_id=user_id,
            metadata={
                "interaction_type": "response",
                "response_length": len(ai_response),
                "helpful_rating": "unknown"  # Could be updated with user feedback
            }
        )

    def _extract_main_topic(self, message: str) -> str:
        """Extract main topic from message"""

        # Simple topic extraction
        topics = []
        message_lower = message.lower()

        topic_mappings = {
            "programming": ["code", "python", "javascript", "programming", "function"],
            "machine_learning": ["machine learning", "ml", "model", "training", "neural"],
            "data": ["data", "database", "analytics", "dataset"],
            "web": ["web", "api", "frontend", "backend", "http"],
            "cloud": ["aws", "azure", "cloud", "kubernetes", "docker"]
        }

        for topic, keywords in topic_mappings.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)

        return topics[0] if topics else "general"

    def end_interaction(self, user_id: str) -> Dict[str, Any]:
        """End user interaction"""

        if user_id in self.active_conversations:
            conversation_id = self.active_conversations[user_id]
            summary = self.conversation_manager.end_conversation(conversation_id)
            del self.active_conversations[user_id]
            return summary

        return {"message": "No active conversation to end"}

    def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user based on memory"""

        # Get user's memories
        user_memories = self.memory.search("", user_id=user_id, limit=50)

        insights = {
            "total_interactions": len(user_memories),
            "frequent_topics": self._analyze_frequent_topics(user_memories),
            "preferences": self._extract_user_preferences(user_memories),
            "interaction_patterns": self._analyze_interaction_patterns(user_memories)
        }

        return insights

    def _analyze_frequent_topics(self, memories: list) -> List[str]:
        """Analyze most frequent topics"""

        topics = []
        for mem in memories:
            metadata = mem.get("metadata", {})
            topic = metadata.get("topic")
            if topic and topic != "general":
                topics.append(topic)

        # Count frequencies
        from collections import Counter
        topic_counts = Counter(topics)

        return [topic for topic, count in topic_counts.most_common(5)]

    def _extract_user_preferences(self, memories: list) -> List[str]:
        """Extract user preferences from memories"""

        preferences = []

        for mem in memories:
            content = mem["content"].lower()
            if "prefer" in content or "like" in content or "favorite" in content:
                # Extract preference statements
                if len(content) < 200:  # Only short preference statements
                    preferences.append(mem["content"])

        return preferences[:5]  # Top 5 preferences

    def _analyze_interaction_patterns(self, memories: list) -> Dict[str, Any]:
        """Analyze user interaction patterns"""

        patterns = {
            "avg_query_length": 0,
            "most_active_times": [],
            "common_question_types": []
        }

        query_lengths = []
        timestamps = []

        for mem in memories:
            metadata = mem.get("metadata", {})
            interaction_type = metadata.get("interaction_type")

            if interaction_type == "query":
                query_lengths.append(metadata.get("query_length", 0))

            if "created_at" in mem:
                timestamps.append(mem["created_at"])

        if query_lengths:
            patterns["avg_query_length"] = sum(query_lengths) / len(query_lengths)

        # Analyze time patterns (simplified)
        if timestamps:
            patterns["total_interactions"] = len(timestamps)
            patterns["first_interaction"] = min(timestamps)
            patterns["last_interaction"] = max(timestamps)

        return patterns

# Usage
agent = MemoryEnabledAIAgent(llm_provider="openai")

# Start interaction
welcome = agent.start_interaction("researcher456")
print(f"Welcome message: {welcome}")

# Process messages
response1 = agent.process_message("researcher456", "What's the best way to learn machine learning?")
print(f"Response 1: {response1}")

response2 = agent.process_message("researcher456", "Do you remember what programming languages I mentioned before?")
print(f"Response 2: {response2}")

# Get user insights
insights = agent.get_user_insights("researcher456")
print(f"User insights: {insights}")

# End interaction
summary = agent.end_interaction("researcher456")
print(f"Interaction summary: {summary}")
```

## 🎯 Best Practices

### LLM Integration Guidelines

1. **Provider Selection**: Choose LLM providers based on task requirements (creativity, reasoning, speed)
2. **Context Management**: Limit context size to stay within token limits while preserving important information
3. **Fallback Strategies**: Implement fallback to simpler models when advanced models fail
4. **Cost Optimization**: Monitor token usage and implement caching to reduce costs
5. **Rate Limiting**: Respect API rate limits and implement queuing for high-volume scenarios

### Memory-Augmented Conversations

1. **Context Window Management**: Keep conversation context within LLM token limits
2. **Memory Relevance**: Only include highly relevant memories in context
3. **Temporal Awareness**: Consider recency when retrieving memories
4. **Privacy Protection**: Implement proper data sanitization and user consent
5. **Session Management**: Properly handle conversation sessions and cleanup

### Production Deployment Considerations

1. **Scalability**: Design for horizontal scaling across multiple LLM providers
2. **Reliability**: Implement retry logic and circuit breakers for API failures
3. **Monitoring**: Track LLM performance, memory usage, and user satisfaction
4. **Security**: Encrypt sensitive data and implement proper authentication
5. **Cost Management**: Monitor and optimize API usage costs

## 📈 Next Steps

With LLM integration mastered, you're ready to:

- **[Chapter 6: Building Memory-Enabled Applications](06-memory-applications.md)** - Real-world use cases and implementation patterns
- **[Chapter 7: Performance Optimization](07-performance-optimization.md)** - Scaling memory systems for production workloads
- **[Chapter 8: Deployment & Monitoring](08-production-deployment.md)** - Deploying memory-enabled AI systems at scale

---

**Ready to build memory-enabled applications? Continue to [Chapter 6: Building Memory-Enabled Applications](06-memory-applications.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `user_id`, `memory` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Integrating with LLMs` as an operating subsystem inside **Mem0 Tutorial: Building Production-Ready AI Agents with Scalable Long-Term Memory**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `response`, `conversation_id` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Integrating with LLMs` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `memory`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/mem0ai/mem0)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `user_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Advanced Memory Features](04-advanced-features.md)
- [Next Chapter: Chapter 6: Building Memory-Enabled Applications](06-memory-applications.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
