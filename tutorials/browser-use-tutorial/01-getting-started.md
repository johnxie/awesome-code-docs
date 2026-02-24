---
layout: default
title: "Browser Use Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Browser Use Tutorial
---

# Chapter 1: Getting Started with Browser Use

Welcome to **Chapter 1: Getting Started with Browser Use**. In this part of **Browser Use Tutorial: AI-Powered Web Automation Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


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

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Browser Use Tutorial: AI-Powered Web Automation Agents**
- tutorial slug: **browser-use-tutorial**
- chapter focus: **Chapter 1: Getting Started with Browser Use**
- system context: **Browser Use Tutorial**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. Define the runtime boundary for `Chapter 1: Getting Started with Browser Use`.
2. Separate control-plane decisions from data-plane execution.
3. Capture input contracts, transformation points, and output contracts.
4. Trace state transitions across request lifecycle stages.
5. Identify extension hooks and policy interception points.
6. Map ownership boundaries for team and automation workflows.
7. Specify rollback and recovery paths for unsafe changes.
8. Track observability signals for correctness, latency, and cost.

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Runtime mode | managed defaults | explicit policy config | speed vs control |
| State handling | local ephemeral | durable persisted state | simplicity vs auditability |
| Tool integration | direct API use | mediated adapter layer | velocity vs governance |
| Rollout method | manual change | staged + canary rollout | effort vs safety |
| Incident response | best effort logs | runbooks + SLO alerts | cost vs reliability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| stale context | inconsistent outputs | missing refresh window | enforce context TTL and refresh hooks |
| policy drift | unexpected execution | ad hoc overrides | centralize policy profiles |
| auth mismatch | 401/403 bursts | credential sprawl | rotation schedule + scope minimization |
| schema breakage | parser/validation errors | unmanaged upstream changes | contract tests per release |
| retry storms | queue congestion | no backoff controls | jittered backoff + circuit breakers |
| silent regressions | quality drop without alerts | weak baseline metrics | eval harness with thresholds |

### Implementation Runbook

1. Establish a reproducible baseline environment.
2. Capture chapter-specific success criteria before changes.
3. Implement minimal viable path with explicit interfaces.
4. Add observability before expanding feature scope.
5. Run deterministic tests for happy-path behavior.
6. Inject failure scenarios for negative-path validation.
7. Compare output quality against baseline snapshots.
8. Promote through staged environments with rollback gates.
9. Record operational lessons in release notes.

### Quality Gate Checklist

- [ ] chapter-level assumptions are explicit and testable
- [ ] API/tool boundaries are documented with input/output examples
- [ ] failure handling includes retry, timeout, and fallback policy
- [ ] security controls include auth scopes and secret rotation plans
- [ ] observability includes logs, metrics, traces, and alert thresholds
- [ ] deployment guidance includes canary and rollback paths
- [ ] docs include links to upstream sources and related tracks
- [ ] post-release verification confirms expected behavior under load

### Source Alignment

- [Browser Use Repository](https://github.com/browser-use/browser-use)
- [Browser Use Releases](https://github.com/browser-use/browser-use/releases)
- [Browser Use Docs](https://docs.browser-use.com/)
- [Browser Use Cloud](https://cloud.browser-use.com/)

### Cross-Tutorial Connection Map

- [OpenHands Tutorial](../openhands-tutorial/)
- [Cline Tutorial](../cline-tutorial/)
- [Roo Code Tutorial](../roo-code-tutorial/)
- [Claude Code Tutorial](../claude-code-tutorial/)
- [Chapter 1: Getting Started](01-getting-started.md)

### Advanced Practice Exercises

1. Build a minimal end-to-end implementation for `Chapter 1: Getting Started with Browser Use`.
2. Add instrumentation and measure baseline latency and error rate.
3. Introduce one controlled failure and confirm graceful recovery.
4. Add policy constraints and verify they are enforced consistently.
5. Run a staged rollout and document rollback decision criteria.

### Review Questions

1. Which execution boundary matters most for this chapter and why?
2. What signal detects regressions earliest in your environment?
3. What tradeoff did you make between delivery speed and governance?
4. How would you recover from the highest-impact failure mode?
5. What must be automated before scaling to team-wide adoption?

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `result`, `agent`, `print` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Browser Use` as an operating subsystem inside **Browser Use Tutorial: AI-Powered Web Automation Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Agent`, `browser`, `ChatOpenAI` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Browser Use` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `result`.
2. **Input normalization**: shape incoming data so `agent` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `print`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Browser Use Repository](https://github.com/browser-use/browser-use)
  Why it matters: authoritative reference on `Browser Use Repository` (github.com).
- [Browser Use Releases](https://github.com/browser-use/browser-use/releases)
  Why it matters: authoritative reference on `Browser Use Releases` (github.com).
- [Browser Use Docs](https://docs.browser-use.com/)
  Why it matters: authoritative reference on `Browser Use Docs` (docs.browser-use.com).
- [Browser Use Cloud](https://cloud.browser-use.com/)
  Why it matters: authoritative reference on `Browser Use Cloud` (cloud.browser-use.com).

Suggested trace strategy:
- search upstream code for `result` and `agent` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Browser Control Basics](02-browser-control.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
