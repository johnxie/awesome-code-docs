---
layout: default
title: "Browser Use Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Browser Use Tutorial
---

# Chapter 1: Getting Started with Browser Use

> Install Browser Use, configure your environment, and create your first AI-powered browser agent.

## Overview

This chapter introduces Browser Use and guides you through installation, setup, and running your first AI-powered browser automation. By the end, you'll have a working agent that can autonomously browse and interact with websites.

## Installation

### Prerequisites

```bash
# Required software
- Python 3.10 or later
- pip package manager
- Git (for cloning repositories)

# Verify Python version
python --version  # Should be 3.10+

# Upgrade pip if needed
pip install --upgrade pip
```

### Installing Browser Use

```bash
# Install browser-use
pip install browser-use

# For development (optional)
git clone https://github.com/browser-use/browser-use.git
cd browser-use
pip install -e .
```

### Installing Playwright Browsers

```bash
# Install Playwright browsers (required for web automation)
pip install playwright

# Install browser binaries
playwright install

# Install specific browsers
playwright install chromium  # Recommended for most use cases
playwright install firefox   # Alternative browser
playwright install webkit    # Safari-like browser

# Verify installation
playwright --version
python -c "import playwright; print('Playwright installed successfully')"
```

### Installing LLM Dependencies

```bash
# For OpenAI
pip install langchain-openai

# For Anthropic
pip install langchain-anthropic

# For Google
pip install langchain-google-genai

# Optional: For local models
pip install langchain-ollama
```

## Configuration

### API Key Setup

```bash
# OpenAI API Key
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Anthropic API Key
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-api-key-here"

# Google API Key
export GOOGLE_API_KEY="your-google-api-key"

# Test API connectivity
python -c "
import openai
client = openai.OpenAI()
print('OpenAI API connected:', client.models.list() is not None)
"
```

### Environment Configuration

```bash
# Create .env file for configuration
cat > .env << EOF
# LLM Configuration
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key

# Browser Configuration
BROWSER_TYPE=chromium
HEADLESS=false  # Set to true for headless mode
SLOW_MO=1000    # Slow down actions for debugging

# Agent Configuration
MAX_STEPS=50
VERBOSE=true
SAVE_CONVERSATION=true
EOF

# Load environment variables
export $(cat .env | xargs)
```

## Your First Browser Agent

### Basic Agent Creation

```python
# first_agent.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7
    )

    # Create the agent
    agent = Agent(
        task="Go to google.com and search for 'browser automation with AI'",
        llm=llm,
    )

    # Run the agent
    result = await agent.run()

    print("Agent completed task!")
    print(f"Final result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
# Run your first agent
python first_agent.py
```

### Understanding the Agent Lifecycle

```python
# agent_lifecycle.py - Detailed agent execution
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    # Configure LLM with detailed logging
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        verbose=True  # Enable detailed logging
    )

    # Create agent with detailed configuration
    agent = Agent(
        task="""
        1. Navigate to https://httpbin.org/
        2. Click on the "GET" link to test basic requests
        3. Verify that the page loads correctly
        4. Return a summary of what you found
        """,
        llm=llm,
        max_steps=20,  # Limit steps to prevent infinite loops
        use_vision=True,  # Use vision for better element detection
        save_conversation_path="./conversation.json"  # Save conversation
    )

    print("Starting agent...")
    result = await agent.run()
    print("
Agent finished!")

    # Analyze the result
    print(f"Task completed: {result.is_done()}")
    print(f"Steps taken: {len(result.history) if result.history else 'N/A'}")

    # Check for extracted content
    if hasattr(result, 'extracted_content') and result.extracted_content:
        print(f"Extracted content: {result.extracted_content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Browser Control Basics

### Navigation and Page Interaction

```python
# navigation_example.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def navigation_demo():
    agent = Agent(
        task="""
        Navigate through the following websites and summarize what you find:

        1. Go to wikipedia.org
        2. Search for "Artificial Intelligence"
        3. Click on the first result
        4. Read the introduction paragraph
        5. Extract the main definition of AI

        Return a clear summary of the AI definition you found.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30
    )

    result = await agent.run()
    print(f"AI Definition Summary: {result}")

if __name__ == "__main__":
    asyncio.run(navigation_demo())
```

### Element Interaction

```python
# interaction_example.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def interaction_demo():
    agent = Agent(
        task="""
        1. Go to https://www.google.com
        2. Find the search box
        3. Type "weather in Tokyo" into the search box
        4. Click the search button or press Enter
        5. Wait for results to load
        6. Extract the current temperature and weather conditions
        7. Return the weather information
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=25
    )

    result = await agent.run()
    print(f"Tokyo Weather: {result}")

if __name__ == "__main__":
    asyncio.run(interaction_demo())
```

## Advanced Agent Configuration

### Custom Agent Settings

```python
# advanced_agent.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import Browser, BrowserConfig

async def advanced_agent_demo():
    # Custom browser configuration
    browser_config = BrowserConfig(
        headless=False,  # Show browser window
        disable_security=True,  # For testing only
        extra_chromium_args=[
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
    )

    # Custom LLM configuration
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,  # More deterministic
        max_tokens=2000,
        model_kwargs={
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    )

    # Advanced agent configuration
    agent = Agent(
        task="""
        Perform a comprehensive analysis of a news website:

        1. Go to https://news.ycombinator.com/
        2. Identify the top 5 stories
        3. For each story, extract:
           - Title
           - Score (points)
           - Number of comments
           - URL
        4. Sort by score (highest first)
        5. Return structured data about the top stories
        """,
        llm=llm,
        browser=browser_config,
        max_steps=50,
        use_vision=True,  # Use vision for better element detection
        save_conversation_path="./news_analysis.json",
        generate_gif=True  # Create GIF of the session
    )

    result = await agent.run()

    print("News Analysis Complete!")
    print(f"Stories found: {len(result.extracted_content) if result.extracted_content else 0}")

    # Process and display results
    if result.extracted_content:
        for story in sorted(result.extracted_content,
                          key=lambda x: x.get('score', 0),
                          reverse=True)[:5]:
            print(f"Title: {story.get('title', 'N/A')}")
            print(f"Score: {story.get('score', 'N/A')}")
            print(f"Comments: {story.get('comments', 'N/A')}")
            print("---")

if __name__ == "__main__":
    asyncio.run(advanced_agent_demo())
```

## Debugging and Troubleshooting

### Enable Debug Logging

```python
# debug_agent.py
import asyncio
import logging
from browser_use import Agent
from langchain_openai import ChatOpenAI

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('browser_use').setLevel(logging.DEBUG)

async def debug_agent():
    agent = Agent(
        task="Go to example.com and describe what you see",
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=10
    )

    try:
        result = await agent.run()
        print(f"Success: {result}")
    except Exception as e:
        print(f"Error: {e}")
        # Check browser state
        if hasattr(agent, 'browser') and agent.browser:
            print("Browser is still running")

if __name__ == "__main__":
    asyncio.run(debug_agent())
```

### Common Issues and Solutions

```python
# troubleshooting.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def robust_agent():
    try:
        agent = Agent(
            task="""
            Go to a website that might be slow or have issues.
            Handle any potential problems gracefully.
            """,
            llm=ChatOpenAI(model="gpt-4o"),
            max_steps=20,
            # Add retry logic
            retry_on_error=True,
            max_retries=3
        )

        result = await agent.run()

        if result.is_done():
            print("Task completed successfully!")
        else:
            print("Task completed with some issues")

        return result

    except Exception as e:
        print(f"Agent failed: {e}")
        # Implement fallback logic
        return await fallback_agent()

async def fallback_agent():
    """Simplified fallback when main agent fails"""
    simple_agent = Agent(
        task="Provide a simple text response since browser automation failed",
        llm=ChatOpenAI(model="gpt-3.5-turbo"),  # Use simpler model
    )
    return await simple_agent.run()

if __name__ == "__main__":
    asyncio.run(robust_agent())
```

## Performance Optimization

### Optimizing Agent Performance

```python
# optimized_agent.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def optimized_agent():
    # Fast LLM for quick tasks
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Faster and cheaper
        temperature=0.1,      # More deterministic
        max_tokens=1000       # Limit output
    )

    agent = Agent(
        task="""
        Quick task: Go to httpbin.org and extract the user agent string.
        Be efficient and don't waste steps.
        """,
        llm=llm,
        max_steps=10,         # Limit steps
        use_vision=False,     # Skip vision for simple tasks
        wait_for_load=False   # Don't wait for full page loads
    )

    import time
    start_time = time.time()

    result = await agent.run()

    end_time = time.time()
    print(f"Task completed in {end_time - start_time:.2f} seconds")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(optimized_agent())
```

## Summary

In this chapter, we've covered:

- **Installation**: Setting up Browser Use and dependencies
- **Configuration**: API keys and environment setup
- **Basic Agent Creation**: Your first browser automation script
- **Navigation and Interaction**: Basic web browsing with AI
- **Advanced Configuration**: Custom browser and LLM settings
- **Debugging**: Troubleshooting common issues
- **Performance**: Optimizing agent execution

## Key Takeaways

1. **Easy Setup**: Browser Use installs quickly and works with popular LLMs
2. **Natural Language Tasks**: Describe what you want the agent to do in plain English
3. **Vision + DOM**: Combines visual understanding with HTML parsing for robust automation
4. **Async Execution**: All operations are asynchronous for better performance
5. **Configurable**: Extensive customization options for different use cases
6. **Error Handling**: Built-in retry logic and error recovery

## Next Steps

Now that you can run basic browser agents, let's explore **browser control basics** including navigation, clicking, and typing operations.

---

**Ready for Chapter 2?** [Browser Control Basics](02-browser-control.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*