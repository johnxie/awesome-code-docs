---
layout: default
title: "Chapter 1: Getting Started with LangChain"
parent: "LangChain Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with LangChain

Welcome to your first steps with LangChain! If you've ever wanted to build applications that can understand and generate human-like text, you're in the right place. In this chapter, we'll set up your development environment and create your first LangChain application.

## What Problem Does LangChain Solve?

Imagine you want to build a chatbot that can:
- Remember your previous conversations
- Search through your documents to answer questions
- Use tools like calculators or web browsers
- Work with different AI models seamlessly

Before LangChain, you'd have to write custom code for each of these features. LangChain provides pre-built components that you can "chain" together like building blocks.

## Installing LangChain

Let's start by setting up your development environment. LangChain works with Python, so you'll need Python 3.8 or higher.

```bash
# Create a virtual environment
python -m venv langchain-env
source langchain-env/bin/activate  # On Windows: langchain-env\Scripts\activate

# Install LangChain
pip install langchain

# Install OpenAI integration (you'll need an API key)
pip install langchain-openai

# Optional: Install additional integrations
pip install langchain-community langchain-core
```

## Your First LangChain Application

Let's create a simple application that uses LangChain to interact with a language model. This will help you understand the basic concepts.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the language model
chat = ChatOpenAI(
    temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = very creative)
    model="gpt-3.5-turbo"  # You can also use gpt-4 for better results
)

# Create a simple conversation
messages = [
    SystemMessage(content="You are a helpful assistant that explains concepts clearly."),
    HumanMessage(content="What is LangChain and why should I use it?")
]

# Get the response
response = chat.invoke(messages)
print(response.content)
```

## Understanding the Core Components

Let's break down what just happened:

### 1. Language Model (`ChatOpenAI`)
This is the "brain" of your application. LangChain supports many different models:
- OpenAI's GPT models
- Anthropic's Claude
- Google's Gemini
- Local models via Ollama
- And many more!

### 2. Messages
LangChain uses a structured format for conversations:
- **SystemMessage**: Sets the AI's behavior and role
- **HumanMessage**: Represents user input
- **AIMessage**: Contains the AI's response

### 3. The `.invoke()` Method
This is LangChain's standard way to run components. You'll see this pattern throughout the framework.

## How It Works Under the Hood

When you call `chat.invoke(messages)`, LangChain:

1. **Formats the messages** into the format expected by the OpenAI API
2. **Makes the API call** to OpenAI's servers
3. **Parses the response** back into LangChain's message format
4. **Returns the result** for you to use

This abstraction layer is what makes LangChain powerful - you can swap out different models without changing your code!

## Testing Your Setup

Let's create a simple test script to make sure everything works:

```python
# test_langchain.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Make sure to set your OpenAI API key
# You can get one from https://platform.openai.com/api-keys
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def test_basic_chat():
    """Test basic chat functionality"""
    chat = ChatOpenAI(temperature=0.7)

    messages = [
        HumanMessage(content="Hello! Can you tell me one fun fact about programming?")
    ]

    response = chat.invoke(messages)
    print("🤖 AI Response:")
    print(response.content)
    print("\n✅ LangChain is working correctly!")

if __name__ == "__main__":
    test_basic_chat()
```

## Common Setup Issues

### API Key Not Set
```
Error: OpenAI API key not found
```
**Solution**: Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Network Issues
```
Error: Connection timeout
```
**Solution**: Check your internet connection and OpenAI service status.

### Version Conflicts
```
Error: ImportError
```
**Solution**: Make sure you're using compatible versions:
```bash
pip install --upgrade langchain langchain-openai langchain-core
```

## What We've Accomplished

Congratulations! 🎉 You've just:

1. **Set up your LangChain environment** with Python and necessary packages
2. **Created your first LangChain application** that can chat with an AI
3. **Learned about core components** like language models and messages
4. **Understood the basic architecture** of how LangChain works

## Next Steps

Now that you have the basics working, you're ready to explore more advanced features. In the next chapter, we'll learn about **Prompt Templates** - a powerful way to create reusable prompts for consistent results.

---

**Ready for more? Continue to [Chapter 2: Prompt Templates & Chains](02-prompt-templates.md)**

*What would you like to build with your new LangChain setup? Try modifying the example to ask different questions or change the system message!* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `langchain`, `messages`, `chat` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with LangChain` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `response`, `install` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with LangChain` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `langchain`.
2. **Input normalization**: shape incoming data so `messages` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `chat`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `langchain` and `messages` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Prompt Templates & Chains](02-prompt-templates.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
