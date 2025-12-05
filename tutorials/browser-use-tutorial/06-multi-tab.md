---
layout: default
title: "Browser Use Tutorial - Chapter 6: Multi-Tab Workflows"
nav_order: 6
has_children: false
parent: Browser Use Tutorial
---

# Chapter 6: Multi-Tab Workflows - Managing Complex Multi-Tab Operations

> Coordinate multiple browser tabs, manage complex workflows, and handle concurrent browser operations.

## Overview

Multi-tab workflows enable complex browser automation scenarios involving multiple pages, concurrent operations, and sophisticated task coordination. This chapter covers managing multiple tabs, coordinating complex workflows, and handling concurrent browser operations.

## Basic Multi-Tab Operations

### Tab Creation and Management

```python
# basic_multi_tab.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def basic_multi_tab_operations():
    """Demonstrate basic multi-tab operations"""

    agent = Agent(
        task="""
        Perform operations across multiple browser tabs:

        1. Start with a single tab open to https://httpbin.org/
        2. Open a new tab and go to https://news.ycombinator.com/
        3. In the news tab, find and remember an interesting article title
        4. Switch back to the httpbin tab
        5. Use the POST endpoint to submit the article title as data
        6. Switch between tabs to verify both operations completed
        7. Close the news tab and keep the results tab open

        Demonstrate tab switching, data transfer between tabs, and cleanup.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30,
        use_vision=True
    )

    result = await agent.run()
    print(f"Multi-Tab Result: {result}")

if __name__ == "__main__":
    asyncio.run(basic_multi_tab_operations())
```

### Tab State Management

```python
# tab_state_management.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def tab_state_management():
    """Manage state across multiple tabs"""

    agent = Agent(
        task="""
        Manage application state across multiple tabs:

        1. Open a tab for data collection (e.g., search results)
        2. Open a second tab for data processing/form filling
        3. Copy relevant data from the first tab to the second tab
        4. Process or submit the data in the second tab
        5. Return to the first tab to collect more data
        6. Repeat the process for multiple data items
        7. Track progress across both tabs

        This simulates real-world workflows like research and form filling.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=40,
        use_vision=True
    )

    result = await agent.run()
    print(f"Tab State Management Result: {result}")

if __name__ == "__main__":
    asyncio.run(tab_state_management())
```

## Complex Workflow Coordination

### Research and Documentation Workflow

```python
# research_workflow.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def research_documentation_workflow():
    """Complex research and documentation workflow"""

    agent = Agent(
        task="""
        Execute a comprehensive research and documentation workflow:

        TAB 1 (Research): https://scholar.google.com/
        - Search for "large language model evaluation metrics"
        - Identify 3-5 key papers
        - Extract titles, authors, and abstracts

        TAB 2 (Analysis): https://chat.openai.com/ or similar
        - Analyze the abstracts for common themes
        - Identify evaluation methodologies mentioned
        - Note any gaps in current research

        TAB 3 (Documentation): Create a summary document
        - Compile findings into a structured report
        - Include references to all sources
        - Save or display the final research summary

        Coordinate data flow between tabs and maintain research integrity.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=60,
        use_vision=True
    )

    result = await agent.run()
    print(f"Research Workflow Result: {result}")

if __name__ == "__main__":
    asyncio.run(research_documentation_workflow())
```

### E-commerce Workflow

```python
# ecommerce_workflow.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def ecommerce_price_comparison():
    """Multi-tab e-commerce price comparison workflow"""

    agent = Agent(
        task="""
        Perform comprehensive product price comparison:

        TAB 1: Amazon
        - Search for "wireless headphones"
        - Find top 3 products with prices
        - Note product names, prices, and ratings

        TAB 2: Best Buy
        - Search for same headphones
        - Compare prices and availability
        - Check for any exclusive deals

        TAB 3: Walmart
        - Same product search
        - Price and availability check
        - Look for bulk or bundle deals

        TAB 4: Comparison Summary
        - Create a comparison table
        - Identify best deals
        - Consider shipping costs and ratings
        - Recommend the best purchase option

        This demonstrates real-world shopping research automation.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=70,
        use_vision=True
    )

    result = await agent.run()
    print(f"E-commerce Workflow Result: {result}")

if __name__ == "__main__":
    asyncio.run(ecommerce_price_comparison())
```

## Concurrent Operations

### Parallel Data Collection

```python
# parallel_data_collection.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def parallel_data_collection():
    """Collect data from multiple sources simultaneously"""

    agent = Agent(
        task="""
        Perform parallel data collection across multiple tabs:

        1. Open tabs for different data sources:
           - Weather data from weather.com
           - Stock prices from yahoo finance
           - News headlines from cnn.com
           - Social media trends from twitter.com

        2. Collect relevant data from each source simultaneously
        3. Synthesize information across all sources
        4. Create a comprehensive dashboard or summary
        5. Update information as needed

        Focus on coordinating parallel operations and data synthesis.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=50,
        use_vision=True
    )

    result = await agent.run()
    print(f"Parallel Collection Result: {result}")

if __name__ == "__main__":
    asyncio.run(parallel_data_collection())
```

### Background Monitoring

```python
# background_monitoring.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def background_monitoring_workflow():
    """Monitor multiple sources for changes"""

    agent = Agent(
        task="""
        Set up background monitoring across multiple tabs:

        TAB 1: Email monitoring
        - Check Gmail or similar for new messages
        - Monitor for specific senders or subjects

        TAB 2: Social media monitoring
        - Check Twitter/LinkedIn for mentions
        - Monitor for brand or product mentions

        TAB 3: News monitoring
        - Check news sites for relevant articles
        - Monitor for industry news or competitor updates

        TAB 4: Dashboard/Alert system
        - Compile alerts from all monitoring tabs
        - Create summary of important updates
        - Set up notification triggers

        Demonstrate continuous monitoring and alert generation.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=45,
        use_vision=True
    )

    result = await agent.run()
    print(f"Monitoring Workflow Result: {result}")

if __name__ == "__main__":
    asyncio.run(background_monitoring_workflow())
```

## Session Management

### Persistent Sessions

```python
# persistent_sessions.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def persistent_session_workflow():
    """Maintain sessions across multiple operations"""

    # Configure browser for session persistence
    browser_config = BrowserConfig(
        persist_cookies=True,
        user_data_dir="./browser_sessions",
        # Keep browser state between runs
    )

    agent = Agent(
        task="""
        Demonstrate session persistence across operations:

        1. Start a new session and log into a service (if ethical testing)
        2. Perform several operations while maintaining login state
        3. Open new tabs that inherit the authenticated session
        4. Perform cross-tab operations with maintained authentication
        5. Demonstrate that session persists across different operations

        Use ethical testing sites like httpbin.org that support sessions.
        Focus on session management and state persistence.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser_config,
        max_steps=35
    )

    result = await agent.run()
    print(f"Persistent Session Result: {result}")

if __name__ == "__main__":
    asyncio.run(persistent_session_workflow())
```

### Session Recovery

```python
# session_recovery.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def session_recovery_workflow():
    """Handle session interruptions and recovery"""

    agent = Agent(
        task="""
        Demonstrate session recovery and error handling:

        1. Start a multi-tab workflow
        2. Simulate or handle potential session interruptions
        3. Implement recovery mechanisms:
           - Re-authenticate if session expires
           - Restore tab states
           - Resume interrupted operations
           - Recover partial progress

        4. Complete the workflow despite potential interruptions
        5. Document recovery strategies used

        Focus on robustness and error recovery in multi-tab scenarios.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=40,
        retry_on_error=True,
        max_retries=3
    )

    result = await agent.run()
    print(f"Session Recovery Result: {result}")

if __name__ == "__main__":
    asyncio.run(session_recovery_workflow())
```

## Advanced Multi-Tab Patterns

### Data Pipeline Workflows

```python
# data_pipeline.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def data_pipeline_workflow():
    """Create data processing pipelines across tabs"""

    agent = Agent(
        task="""
        Build a data processing pipeline across multiple tabs:

        TAB 1: Data Collection
        - Scrape data from various sources
        - Collect raw data into structured format
        - Validate data quality

        TAB 2: Data Processing
        - Clean and normalize collected data
        - Perform calculations and transformations
        - Apply business rules and logic

        TAB 3: Data Visualization
        - Create charts and graphs from processed data
        - Generate reports and summaries
        - Format data for presentation

        TAB 4: Data Export
        - Export processed data to various formats
        - Send to external systems or APIs
        - Generate automated reports

        Demonstrate end-to-end data pipeline automation.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=80,
        use_vision=True
    )

    result = await agent.run()
    print(f"Data Pipeline Result: {result}")

if __name__ == "__main__":
    asyncio.run(data_pipeline_workflow())
```

### Collaborative Workflows

```python
# collaborative_workflow.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def collaborative_workflow():
    """Simulate collaborative work across multiple contexts"""

    agent = Agent(
        task="""
        Demonstrate collaborative workflow across tabs:

        TAB 1: Research & Planning
        - Research project requirements
        - Gather specifications and constraints
        - Create project plan and timeline

        TAB 2: Development Environment
        - Set up development tools and IDE
        - Configure project structure
        - Initialize version control

        TAB 3: Documentation
        - Create project documentation
        - Write API specifications
        - Generate user guides

        TAB 4: Testing & Validation
        - Set up testing frameworks
        - Create test cases and scenarios
        - Validate functionality and performance

        TAB 5: Deployment & Monitoring
        - Configure deployment pipeline
        - Set up monitoring and alerting
        - Create rollback procedures

        Coordinate all aspects of a software development project.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=100,
        use_vision=True
    )

    result = await agent.run()
    print(f"Collaborative Workflow Result: {result}")

if __name__ == "__main__":
    asyncio.run(collaborative_workflow())
```

## Resource Management

### Memory and Performance Optimization

```python
# resource_optimization.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def resource_optimized_workflow():
    """Optimize resource usage in multi-tab scenarios"""

    # Optimized browser configuration
    browser_config = BrowserConfig(
        headless=True,           # Reduce resource usage
        disable_images=True,     # Faster loading
        max_contexts=5,          # Limit concurrent tabs
        browser_context_timeout=300,  # Clean up old contexts
    )

    agent = Agent(
        task="""
        Perform resource-efficient multi-tab operations:

        1. Open multiple tabs efficiently
        2. Manage memory usage across tabs
        3. Clean up unused tabs and contexts
        4. Balance performance with resource constraints
        5. Monitor and optimize resource usage
        6. Complete operations within memory limits

        Demonstrate scalable multi-tab automation.
        """,
        llm=ChatOpenAI(model="gpt-4o-mini"),  # Use efficient model
        browser=browser_config,
        max_steps=50,
        use_vision=False  # Reduce processing overhead
    )

    import time
    start_time = time.time()

    result = await agent.run()

    end_time = time.time()
    duration = end_time - start_time

    print(f"Workflow completed in {duration:.2f} seconds")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(resource_optimized_workflow())
```

### Tab Lifecycle Management

```python
# tab_lifecycle.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def tab_lifecycle_management():
    """Manage tab creation, usage, and cleanup"""

    agent = Agent(
        task="""
        Demonstrate proper tab lifecycle management:

        1. Create tabs strategically based on workflow needs
        2. Use tabs efficiently without unnecessary proliferation
        3. Switch between tabs for different phases of work
        4. Close completed tabs to free resources
        5. Maintain important tabs for ongoing work
        6. Clean up all tabs at workflow completion

        Focus on efficient resource usage and workflow organization.
        """,
        llm=ChatOpenai(model="gpt-4o"),
        max_steps=40
    )

    result = await agent.run()
    print(f"Tab Lifecycle Result: {result}")

if __name__ == "__main__":
    asyncio.run(tab_lifecycle_management())
```

## Summary

In this chapter, we've covered:

- **Basic Multi-Tab Operations**: Tab creation, switching, and management
- **Workflow Coordination**: Complex multi-step processes across tabs
- **Concurrent Operations**: Parallel data collection and monitoring
- **Session Management**: Persistent sessions and recovery mechanisms
- **Advanced Patterns**: Data pipelines and collaborative workflows
- **Resource Optimization**: Memory management and performance tuning
- **Lifecycle Management**: Efficient tab creation and cleanup

## Key Takeaways

1. **Strategic Tab Usage**: Create tabs for specific workflow phases
2. **State Coordination**: Manage data flow between related tabs
3. **Resource Awareness**: Monitor and optimize memory/performance
4. **Session Persistence**: Maintain authentication and context across tabs
5. **Error Recovery**: Handle tab failures and session interruptions
6. **Scalability**: Design workflows that work with limited resources
7. **Cleanup Discipline**: Properly close and clean up tabs when done

## Next Steps

Now that you can manage complex multi-tab workflows, let's explore **custom actions** for domain-specific browser automation.

---

**Ready for Chapter 7?** [Custom Actions](07-custom-actions.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*