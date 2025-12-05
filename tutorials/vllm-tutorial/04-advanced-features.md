---
layout: default
title: "vLLM Tutorial - Chapter 4: Advanced Features"
nav_order: 4
has_children: false
parent: vLLM Tutorial
---

# Chapter 4: Advanced Features - Streaming, Tool Calling, and Multi-Modal

> Explore vLLM's advanced capabilities including real-time streaming, function calling, and multi-modal models.

## Overview

This chapter covers vLLM's advanced features that enable sophisticated applications - real-time streaming for interactive experiences, tool calling for agent-like behavior, and multi-modal capabilities for vision-language tasks.

## Streaming Generation

### Basic Text Streaming

```python
import asyncio
from vllm import LLM, SamplingParams

# Initialize vLLM
llm = LLM(model="microsoft/DialoGPT-medium")

async def stream_text_generation():
    """Demonstrate basic streaming text generation"""

    prompt = "Tell me a story about a magical forest"
    sampling_params = SamplingParams(max_tokens=200, temperature=0.8)

    # Generate with streaming
    stream = llm.generate(prompt, sampling_params, stream=True)

    print("Streaming response:")
    print("=" * 50)

    async for output in stream:
        # Get the latest generated text
        if output.outputs:
            text = output.outputs[0].text
            # Print new text as it arrives
            print(text, end="", flush=True)
            await asyncio.sleep(0.01)  # Small delay for demonstration

    print("\n\nStreaming complete!")

# Run streaming example
await stream_text_generation()
```

### Advanced Streaming with Callbacks

```python
class StreamingCallback:
    def __init__(self):
        self.full_text = ""
        self.token_count = 0
        self.start_time = None

    async def on_token(self, token_text, token_id, logprob):
        """Called for each generated token"""
        if self.start_time is None:
            import time
            self.start_time = time.time()

        self.full_text += token_text
        self.token_count += 1

        # Print token with metadata
        probability = math.exp(logprob) if logprob is not None else 0
        print(f"Token: '{token_text}' (id: {token_id}, prob: {probability:.3f})")

    async def on_complete(self):
        """Called when generation is complete"""
        import time
        end_time = time.time()
        duration = end_time - self.start_time

        print("
Generation Complete!")
        print(f"Total tokens: {self.token_count}")
        print(".2f")
        print(".2f")

        return self.full_text

async def advanced_streaming():
    """Advanced streaming with detailed callbacks"""

    prompt = "Explain quantum computing in simple terms"
    sampling_params = SamplingParams(
        max_tokens=100,
        temperature=0.7,
        logprobs=1  # Get log probabilities
    )

    callback = StreamingCallback()

    # Custom streaming implementation
    result = llm.generate([prompt], sampling_params)[0]

    # Simulate streaming by processing tokens one by one
    for i, (token_id, logprob_data) in enumerate(zip(
        result.outputs[0].token_ids,
        result.outputs[0].logprobs or [None] * len(result.outputs[0].token_ids)
    )):
        # Decode token (simplified - actual implementation would use tokenizer)
        token_text = f"[Token{i}]"  # Placeholder

        # Get log probability
        logprob = logprob_data.most_likely_logprob if logprob_data else None

        # Call callback
        await callback.on_token(token_text, token_id, logprob)

    final_text = await callback.on_complete()
    return final_text

# Run advanced streaming
final_result = await advanced_streaming()
print(f"\nFinal result: {final_result}")
```

### Real-Time Chat Streaming

```python
class ChatStreamer:
    def __init__(self, llm):
        self.llm = llm
        self.conversation_history = []

    async def stream_chat_response(self, user_message):
        """Stream a chat response in real-time"""

        # Add user message to history
        self.conversation_history.append(f"User: {user_message}")

        # Create prompt from conversation history
        context = "\n".join(self.conversation_history[-4:])  # Last 4 messages
        prompt = f"{context}\nAssistant:"

        print("Assistant: ", end="", flush=True)

        sampling_params = SamplingParams(
            max_tokens=150,
            temperature=0.8,
            stop=["\nUser:", "\nAssistant:"]  # Stop at conversation boundaries
        )

        # Generate with streaming
        stream = self.llm.generate(prompt, sampling_params, stream=True)

        full_response = ""

        async for output in stream:
            if output.outputs:
                # Get new text since last output
                new_text = output.outputs[0].text[len(full_response):]
                full_response = output.outputs[0].text

                # Print new text
                print(new_text, end="", flush=True)

        print()  # New line

        # Add assistant response to history
        self.conversation_history.append(f"Assistant: {full_response}")

        return full_response

# Interactive chat streaming
async def interactive_chat():
    """Interactive chat with streaming responses"""

    streamer = ChatStreamer(llm)

    print("🤖 Streaming Chat Bot")
    print("Type 'quit' to exit")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            break

        await streamer.stream_chat_response(user_input)

    print("Goodbye! 👋")

# Uncomment to run interactive chat
# await interactive_chat()
```

## Tool Calling and Function Calling

### Basic Tool Integration

```python
# Define tools/functions that the model can call
def get_weather(location: str) -> str:
    """Get weather information for a location"""
    # Mock weather API
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Rainy, 15°C",
        "Tokyo": "Cloudy, 25°C"
    }

    return weather_data.get(location, f"Weather data not available for {location}")

def calculate(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        # Safe evaluation (in practice, use a proper math parser)
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"

def search_web(query: str) -> str:
    """Search the web for information"""
    # Mock search results
    mock_results = {
        "python tutorial": "Python is a programming language...",
        "machine learning": "Machine learning is a subset of AI...",
        "quantum computing": "Quantum computing uses quantum mechanics..."
    }

    return mock_results.get(query.lower(), f"No results found for '{query}'")

# Tool registry
available_tools = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_web": search_web
}

def execute_tool(tool_name: str, **kwargs) -> str:
    """Execute a tool with given parameters"""
    if tool_name in available_tools:
        try:
            return available_tools[tool_name](**kwargs)
        except Exception as e:
            return f"Tool execution error: {e}"
    else:
        return f"Unknown tool: {tool_name}"
```

### Tool-Calling with vLLM

```python
# vLLM with tool calling capabilities
class ToolCallingLLM:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools

    async def generate_with_tools(self, prompt, max_steps=5):
        """Generate response with tool calling capability"""

        current_prompt = prompt
        conversation = []

        for step in range(max_steps):
            # Generate next action
            tool_prompt = f"""
{prompt}

You have access to these tools:
{chr(10).join(f"- {name}: {func.__doc__ or 'No description'}" for name, func in self.tools.items())}

To use a tool, respond with: TOOL_CALL: tool_name(arguments)
For example: TOOL_CALL: get_weather(location="New York")

If you have enough information to answer, provide the final answer.
"""

            sampling_params = SamplingParams(
                max_tokens=100,
                temperature=0.1,  # Lower temperature for tool use
                stop=["\n"]  # Stop at line breaks for parsing
            )

            result = self.llm.generate([tool_prompt], sampling_params)[0]
            response = result.outputs[0].text.strip()

            print(f"Step {step + 1}: {response}")

            # Check if it's a tool call
            if response.startswith("TOOL_CALL:"):
                # Parse tool call
                tool_call = response[11:].strip()  # Remove "TOOL_CALL: "

                # Extract tool name and arguments (simplified parsing)
                if "(" in tool_call and tool_call.endswith(")"):
                    tool_name = tool_call.split("(")[0]
                    args_str = tool_call.split("(")[1].rstrip(")")

                    # Execute tool
                    tool_result = execute_tool(tool_name, **eval(f"dict({args_str})"))

                    # Add to conversation
                    current_prompt += f"\nTool result: {tool_result}"
                    conversation.append(f"Tool call: {tool_call}")
                    conversation.append(f"Tool result: {tool_result}")
                else:
                    return f"Invalid tool call format: {tool_call}"

            else:
                # Final answer
                return response

        return "Maximum steps reached without conclusion"

# Test tool calling
tool_llm = ToolCallingLLM(llm, available_tools)

test_queries = [
    "What's the weather like in London?",
    "What is 15 * 23?",
    "Tell me about machine learning"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    print("Reasoning:")
    result = await tool_llm.generate_with_tools(query)
    print(f"Final answer: {result}")
```

### Advanced Tool Integration

```python
# More sophisticated tool calling with structured responses
class AdvancedToolAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.conversation_history = []

    async def process_query(self, user_query):
        """Process user query with sophisticated tool usage"""

        system_prompt = """
You are an AI assistant with access to various tools. When answering questions:

1. First, determine if you need tools to answer the question
2. If tools are needed, call them in the right order
3. Use tool results to formulate your final answer
4. Be concise but informative

Available tools:
- get_weather(location): Get weather for a location
- calculate(expression): Calculate mathematical expressions
- search_web(query): Search for information online

Format tool calls as: TOOL: tool_name(ARGUMENTS)
"""

        full_prompt = f"{system_prompt}\n\nUser: {user_query}\nAssistant:"

        max_iterations = 3

        for iteration in range(max_iterations):
            sampling_params = SamplingParams(
                max_tokens=150,
                temperature=0.3,
                stop=["\nUser:", "\nAssistant:"]
            )

            result = self.llm.generate([full_prompt], sampling_params)[0]
            response = result.outputs[0].text.strip()

            # Check for tool calls
            tool_calls = self._extract_tool_calls(response)

            if tool_calls:
                # Execute tools and continue conversation
                tool_results = []
                for tool_call in tool_calls:
                    tool_name = tool_call['name']
                    args = tool_call['args']

                    result = execute_tool(tool_name, **args)
                    tool_results.append(f"{tool_name} result: {result}")

                # Add tool results to prompt
                full_prompt += f"\n{response}\n" + "\n".join(tool_results) + "\nAssistant:"
                continue

            else:
                # No more tool calls, return final answer
                return response

        return "Could not complete query within iteration limit"

    def _extract_tool_calls(self, response):
        """Extract tool calls from response"""
        import re

        tool_calls = []

        # Find patterns like TOOL: tool_name(arguments)
        tool_pattern = r'TOOL:\s*(\w+)\(([^)]*)\)'
        matches = re.findall(tool_pattern, response)

        for tool_name, args_str in matches:
            try:
                # Parse arguments (simplified)
                args = {}
                if args_str.strip():
                    # Simple argument parsing (location="New York")
                    arg_matches = re.findall(r'(\w+)="([^"]*)"', args_str)
                    args = {k: v for k, v in arg_matches}

                tool_calls.append({
                    'name': tool_name,
                    'args': args
                })

            except Exception as e:
                print(f"Error parsing tool call: {e}")
                continue

        return tool_calls

# Test advanced tool agent
advanced_agent = AdvancedToolAgent(llm, available_tools)

complex_queries = [
    "What's the weather in Tokyo and what is 144 divided by 12?",
    "Search for information about Python programming and calculate 2^10"
]

for query in complex_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    result = await advanced_agent.process_query(query)
    print(f"Answer: {result}")
```

## Multi-Modal Models

### Vision-Language Models

```python
# vLLM with multi-modal capabilities (when supported)
try:
    # Load a vision-language model (if available)
    vlm = LLM(model="llava-hf/llava-1.5-7b-hf")  # Example model

    # Multi-modal input processing
    def process_image_and_text(image_path, text_prompt):
        """Process image and text together"""

        # In practice, this would encode the image and combine with text
        # vLLM doesn't natively support images yet, but this shows the concept

        combined_prompt = f"[Image: {image_path}]\n{text_prompt}"

        sampling_params = SamplingParams(
            max_tokens=200,
            temperature=0.7
        )

        # This would work with actual multi-modal models
        # result = vlm.generate([combined_prompt], sampling_params)

        return "Multi-modal processing would happen here"

    # Example usage
    result = process_image_and_text("image.jpg", "Describe this image")

except Exception as e:
    print(f"Multi-modal models not available: {e}")
    print("Using text-only model for demonstration")

# Text-based image description simulation
def describe_image_concept(image_concept):
    """Simulate image description using text-only model"""

    prompt = f"Describe what you imagine this image would show: {image_concept}"

    sampling_params = SamplingParams(
        max_tokens=100,
        temperature=0.8
    )

    result = llm.generate([prompt], sampling_params)[0]
    return result.outputs[0].text.strip()

# Test image description
image_concepts = [
    "a sunset over mountains",
    "a busy city street at night",
    "a cat wearing sunglasses"
]

for concept in image_concepts:
    description = describe_image_concept(concept)
    print(f"\nConcept: {concept}")
    print(f"Description: {description}")
```

### Audio and Other Modalities

```python
# Audio processing simulation (when supported)
class AudioProcessingLLM:
    def __init__(self, llm):
        self.llm = llm

    def transcribe_audio(self, audio_description):
        """Simulate audio transcription"""

        prompt = f"""
Transcribe this audio recording. The recording contains:
{audio_description}

Provide the transcription with timestamps if relevant.
"""

        sampling_params = SamplingParams(
            max_tokens=200,
            temperature=0.1  # Low temperature for transcription
        )

        result = self.llm.generate([prompt], sampling_params)[0]
        return result.outputs[0].text.strip()

    def analyze_audio_content(self, audio_content):
        """Analyze audio content"""

        prompt = f"""
Analyze this audio content:
{audio_content}

Provide:
1. Summary of the content
2. Key topics discussed
3. Sentiment analysis
4. Action items or important points
"""

        result = self.llm.generate([prompt], SamplingParams(max_tokens=150))[0]
        return result.outputs[0].text.strip()

# Test audio processing
audio_processor = AudioProcessingLLM(llm)

audio_samples = [
    "A 30-second recording of someone saying 'Hello, this is a test message for speech recognition'",
    "A 2-minute podcast discussing the latest developments in artificial intelligence"
]

for audio_desc in audio_samples:
    transcription = audio_processor.transcribe_audio(audio_desc)
    analysis = audio_processor.analyze_audio_content(audio_desc)

    print(f"\nAudio: {audio_desc[:50]}...")
    print(f"Transcription: {transcription}")
    print(f"Analysis: {analysis[:100]}...")
```

## Custom Model Extensions

### Extending vLLM Capabilities

```python
# Custom model wrapper for specialized tasks
class SpecializedLLM:
    def __init__(self, base_llm, specializations=None):
        self.base_llm = base_llm
        self.specializations = specializations or {}

    def generate_code(self, description):
        """Specialized code generation"""

        code_prompt = f"""
Generate Python code for the following requirement:
{description}

Requirements:
- Include proper error handling
- Add type hints
- Include docstrings
- Follow PEP 8 style
- Add unit tests

Code:
```python
"""

        sampling_params = SamplingParams(
            max_tokens=300,
            temperature=0.3,  # Lower temperature for code
            stop=["```"]  # Stop at code block end
        )

        result = self.base_llm.generate([code_prompt], sampling_params)[0]
        return result.outputs[0].text.strip()

    def analyze_sentiment(self, text):
        """Specialized sentiment analysis"""

        sentiment_prompt = f"""
Analyze the sentiment of this text:
"{text}"

Provide:
1. Overall sentiment (positive/negative/neutral)
2. Confidence score (0-1)
3. Key positive/negative phrases
4. Suggested improvements

Analysis:
"""

        result = self.base_llm.generate([sentiment_prompt], SamplingParams(max_tokens=100))[0]
        return result.outputs[0].text.strip()

    def summarize_document(self, document, max_length=100):
        """Document summarization"""

        summary_prompt = f"""
Summarize the following document in {max_length} words or less:

{document}

Summary:
"""

        result = self.base_llm.generate([summary_prompt], SamplingParams(max_tokens=max_length))[0]
        return result.outputs[0].text.strip()

# Test specialized LLM
specialized_llm = SpecializedLLM(llm)

# Test different specializations
test_cases = [
    ("code", "Create a function to validate email addresses"),
    ("sentiment", "I love this product, it works great and customer service is excellent!"),
    ("summary", "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed. It uses algorithms and statistical models to analyze data and make predictions.")
]

for task_type, content in test_cases:
    if task_type == "code":
        result = specialized_llm.generate_code(content)
    elif task_type == "sentiment":
        result = specialized_llm.analyze_sentiment(content)
    elif task_type == "summary":
        result = specialized_llm.summarize_document(content)

    print(f"\n{task_type.upper()} TASK:")
    print(f"Input: {content[:50]}...")
    print(f"Result: {result[:100]}...")
```

## Performance Monitoring for Advanced Features

### Advanced Metrics Collection

```python
# Advanced monitoring for streaming and tool usage
class AdvancedMonitor:
    def __init__(self):
        self.metrics = {
            "streaming_sessions": 0,
            "tool_calls": 0,
            "tool_success_rate": 0.0,
            "average_streaming_latency": 0.0,
            "total_tokens_streamed": 0
        }

    def record_streaming_session(self, duration, token_count):
        """Record streaming session metrics"""
        self.metrics["streaming_sessions"] += 1
        self.metrics["total_tokens_streamed"] += token_count

        # Update rolling average
        current_avg = self.metrics["average_streaming_latency"]
        session_count = self.metrics["streaming_sessions"]

        self.metrics["average_streaming_latency"] = (
            (current_avg * (session_count - 1)) + duration
        ) / session_count

    def record_tool_call(self, success):
        """Record tool call metrics"""
        self.metrics["tool_calls"] += 1

        # Update success rate
        current_successes = self.metrics["tool_success_rate"] * (self.metrics["tool_calls"] - 1)
        current_successes += 1 if success else 0

        self.metrics["tool_success_rate"] = current_successes / self.metrics["tool_calls"]

    def get_report(self):
        """Generate metrics report"""
        return {
            **self.metrics,
            "streaming_throughput": (
                self.metrics["total_tokens_streamed"] /
                self.metrics["average_streaming_latency"]
                if self.metrics["average_streaming_latency"] > 0 else 0
            )
        }

# Global monitor
monitor = AdvancedMonitor()

# Enhanced streaming with monitoring
async def monitored_streaming(prompt):
    """Streaming with performance monitoring"""

    import time
    start_time = time.time()

    sampling_params = SamplingParams(max_tokens=100, temperature=0.7)

    # Simulate streaming with monitoring
    result = llm.generate([prompt], sampling_params)[0]
    response = result.outputs[0]

    # Simulate token-by-token streaming
    token_count = 0
    for token_id in response.token_ids:
        token_count += 1
        # In real streaming, each token would be yielded here
        pass

    duration = time.time() - start_time

    # Record metrics
    monitor.record_streaming_session(duration, token_count)

    return response.text

# Test monitored streaming
streaming_results = []
test_prompts = ["Tell me about AI", "Explain quantum physics", "Write a poem about coding"]

for prompt in test_prompts:
    result = await monitored_streaming(prompt)
    streaming_results.append(result)

# Get monitoring report
report = monitor.get_report()
print("\nAdvanced Monitoring Report:")
print(f"Streaming sessions: {report['streaming_sessions']}")
print(f"Total tokens streamed: {report['total_tokens_streamed']}")
print(".3f")
print(".2f")
```

## Summary

In this chapter, we've explored vLLM's advanced features:

- **Streaming Generation** - Real-time text generation with callbacks and monitoring
- **Tool Calling** - Function calling capabilities for agent-like behavior
- **Multi-Modal Processing** - Vision-language and audio processing concepts
- **Custom Model Extensions** - Specialized wrappers for different tasks
- **Advanced Monitoring** - Comprehensive metrics for complex features

These advanced features enable sophisticated applications like real-time chatbots, AI agents with tool use, and multi-modal AI systems.

## Key Takeaways

1. **Streaming**: Real-time generation for interactive applications
2. **Tool Integration**: Function calling for extending model capabilities
3. **Multi-Modal**: Processing text, images, and audio together
4. **Specialization**: Custom wrappers for domain-specific tasks
5. **Monitoring**: Comprehensive metrics for advanced features

Next, we'll explore **performance optimization** - batching, quantization, and GPU optimization techniques.

---

**Ready for the next chapter?** [Chapter 5: Performance Optimization](05-performance-optimization.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*