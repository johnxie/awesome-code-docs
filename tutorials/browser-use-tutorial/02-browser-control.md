---
layout: default
title: "Browser Use Tutorial - Chapter 2: Browser Control Basics"
nav_order: 2
has_children: false
parent: Browser Use Tutorial
---

# Chapter 2: Browser Control Basics

> Master fundamental browser operations: navigation, clicking, typing, scrolling, and page interaction.

## Overview

This chapter covers the core browser control operations that form the foundation of web automation with Browser Use. You'll learn how to navigate pages, interact with elements, handle forms, and manage browser state.

## Navigation Operations

### Basic Page Navigation

```python
# navigation_basics.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def navigation_basics():
    """Demonstrate basic navigation operations"""

    agent = Agent(
        task="""
        Navigate to the following websites and describe what you find:

        1. Go to https://example.com
        2. Describe the main heading and content
        3. Go to https://httpbin.org/
        4. Click on the "GET" link
        5. Describe the response you see

        Return a summary of both pages.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=20
    )

    result = await agent.run()
    print(f"Navigation Summary: {result}")

if __name__ == "__main__":
    asyncio.run(navigation_basics())
```

### URL Navigation Patterns

```python
# url_navigation.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def url_navigation_patterns():
    """Different ways to navigate to URLs"""

    tasks = [
        # Direct navigation
        "Navigate to https://google.com and describe the search interface",

        # Search and navigate
        "Search for 'Python programming' on Google and click the first result",

        # Multi-step navigation
        """
        1. Go to github.com
        2. Search for 'browser-use'
        3. Click on the browser-use repository
        4. Read the README description
        5. Return the main purpose of the project
        """
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n--- Task {i} ---")

        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            max_steps=15
        )

        result = await agent.run()
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(url_navigation_patterns())
```

### Handling Page Loads and Timeouts

```python
# page_load_handling.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def page_load_handling():
    """Handle different page loading scenarios"""

    # Configure browser for better page load handling
    browser_config = BrowserConfig(
        wait_for_load_timeout=30,  # Wait up to 30 seconds for page load
        navigation_timeout=15,     # Wait up to 15 seconds for navigation
    )

    agent = Agent(
        task="""
        Test different page loading scenarios:

        1. Go to a fast-loading page: https://httpbin.org/html
        2. Wait for it to fully load and extract the H1 title

        3. Go to a slower page: https://httpbin.org/delay/3
        4. Wait for the delayed response and confirm you got the result

        5. Try to access a non-existent page: https://httpbin.org/status/404
        6. Handle the error gracefully and report what happened

        Return a summary of all three scenarios.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser_config,
        max_steps=25
    )

    result = await agent.run()
    print(f"Page Load Test Results: {result}")

if __name__ == "__main__":
    asyncio.run(page_load_handling())
```

## Element Interaction

### Clicking Elements

```python
# clicking_elements.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def clicking_examples():
    """Demonstrate various clicking operations"""

    click_tasks = [
        # Basic button click
        """
        Go to https://httpbin.org/forms/post
        Fill in the form with sample data:
        - Customer name: John Doe
        - Telephone: 555-0123
        - Email: john@example.com
        - Pizza Size: Large
        Click the submit button and describe the response
        """,

        # Link clicking
        """
        Go to https://news.ycombinator.com/
        Click on the title of the top story
        Read the article or page that opens
        Summarize what the story is about
        """,

        # Multiple clicks
        """
        Go to https://httpbin.org/
        Click on each of the main endpoint links (GET, POST, PUT, DELETE)
        For each one, describe what the endpoint does
        Return a summary of all HTTP methods
        """
    ]

    for i, task in enumerate(click_tasks, 1):
        print(f"\n--- Click Task {i} ---")

        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            max_steps=20
        )

        result = await agent.run()
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(clicking_examples())
```

### Typing and Text Input

```python
# typing_input.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def typing_examples():
    """Demonstrate text input and typing operations"""

    typing_tasks = [
        # Simple text input
        """
        Go to https://httpbin.org/forms/post
        Fill in the customer name field with "Alice Johnson"
        Fill in the telephone field with "555-0199"
        Fill in the email field with "alice@example.com"
        Don't submit the form, just confirm the fields are filled
        """,

        # Search and input
        """
        Go to https://google.com
        Type "weather in San Francisco" in the search box
        Press Enter to search
        Extract the current temperature and weather conditions
        """,

        # Multi-field form
        """
        Go to https://httpbin.org/forms/post
        Fill out the entire delivery form:
        - Customer name: Bob Smith
        - Telephone: 555-0150
        - Email: bob.smith@email.com
        - Pizza Size: Medium
        - Toppings: Pepperoni, Mushrooms, Extra Cheese
        - Delivery Instructions: Ring doorbell twice
        - Payment Method: Credit Card

        Verify all fields are filled correctly before submitting
        """
    ]

    for i, task in enumerate(typing_tasks, 1):
        print(f"\n--- Typing Task {i} ---")

        agent = Agent(
            task=task,
            llm=ChatOpenAI(model="gpt-4o"),
            max_steps=25
        )

        result = await agent.run()
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(typing_examples())
```

### Advanced Element Selection

```python
# element_selection.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def advanced_element_selection():
    """Advanced techniques for finding and interacting with elements"""

    agent = Agent(
        task="""
        Go to https://httpbin.org/ and perform these element selection tasks:

        1. Find and click the link that says "GET"
        2. On the new page, find the JSON response
        3. Extract the "url" field from the JSON
        4. Go back to the main page

        5. Find and click the link for "POST"
        6. On the POST page, find the form
        7. Fill in some sample data in the text area
        8. Submit the form
        9. Extract the JSON response showing the posted data

        Return a comparison of GET vs POST responses.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=30,
        use_vision=True  # Enable vision for better element detection
    )

    result = await agent.run()
    print(f"Element Selection Results: {result}")

if __name__ == "__main__":
    asyncio.run(advanced_element_selection())
```

## Scrolling and Page Navigation

### Scrolling Operations

```python
# scrolling_operations.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def scrolling_demo():
    """Demonstrate scrolling and page navigation"""

    agent = Agent(
        task="""
        Go to https://news.ycombinator.com/ and perform these scrolling tasks:

        1. Read the titles of the first 5 stories on the front page
        2. Scroll down to see more stories
        3. Read 5 more story titles
        4. Scroll to the bottom of the page
        5. Find and read the "More" link or pagination
        6. Try to go to the next page of stories

        Return a list of all 10+ story titles you found, noting which page they were on.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=35
    )

    result = await agent.run()
    print(f"Scrolling Results: {result}")

if __name__ == "__main__":
    asyncio.run(scrolling_demo())
```

### Infinite Scroll Handling

```python
# infinite_scroll.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def infinite_scroll_handling():
    """Handle pages with infinite scroll"""

    agent = Agent(
        task="""
        Go to https://httpbin.org/stream/20 and handle the streaming response:

        1. Load the page with streaming data
        2. Wait for the content to load
        3. Scroll through all the streamed items
        4. Count how many items are displayed
        5. Extract the content of the last few items

        This demonstrates handling dynamic content loading.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=25
    )

    result = await agent.run()
    print(f"Infinite Scroll Results: {result}")

if __name__ == "__main__":
    asyncio.run(infinite_scroll_handling())
```

## Browser State Management

### Managing Cookies and Sessions

```python
# session_management.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def session_management():
    """Demonstrate cookie and session handling"""

    # Configure browser to persist cookies
    browser_config = BrowserConfig(
        persist_cookies=True,
        user_data_dir="./browser_data"  # Persist browser data
    )

    agent = Agent(
        task="""
        Test session and cookie persistence:

        1. Go to https://httpbin.org/cookies/set/session_id/12345
        2. Verify the cookie was set by checking the response
        3. Navigate to https://httpbin.org/cookies
        4. Confirm the session_id cookie is still present
        5. Try to access https://httpbin.org/cookies/delete?session_id
        6. Verify the cookie was deleted

        Return a summary of the cookie operations.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser_config,
        max_steps=20
    )

    result = await agent.run()
    print(f"Session Management Results: {result}")

if __name__ == "__main__":
    asyncio.run(session_management())
```

### Multiple Browser Contexts

```python
# multi_context.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def multi_context_demo():
    """Demonstrate multiple browser contexts"""

    # Create isolated browser contexts
    contexts = []

    # Context 1: Regular browsing
    agent1 = Agent(
        task="Go to https://httpbin.org/user-agent and extract the user agent string",
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=10
    )

    # Context 2: With custom user agent
    browser_config2 = BrowserConfig(
        user_agent="Custom Bot 1.0"
    )
    agent2 = Agent(
        task="Go to https://httpbin.org/user-agent and extract the user agent string",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser_config2,
        max_steps=10
    )

    # Run both agents
    result1 = await agent1.run()
    result2 = await agent2.run()

    print(f"Default User Agent: {result1}")
    print(f"Custom User Agent: {result2}")

if __name__ == "__main__":
    asyncio.run(multi_context_demo())
```

## Error Handling and Recovery

### Handling Navigation Errors

```python
# error_handling.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def error_handling_demo():
    """Demonstrate error handling and recovery"""

    agent = Agent(
        task="""
        Test error handling scenarios:

        1. Try to navigate to https://httpbin.org/status/500
        2. Handle the server error gracefully
        3. Try to navigate to a completely invalid URL: https://this-domain-does-not-exist-12345.com
        4. Handle the DNS/network error
        5. Finally, successfully navigate to https://httpbin.org/
        6. Confirm you can access the working site

        Return a summary of how you handled each error scenario.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        max_steps=25,
        retry_on_error=True,
        max_retries=2
    )

    result = await agent.run()
    print(f"Error Handling Results: {result}")

if __name__ == "__main__":
    asyncio.run(error_handling_demo())
```

### Timeout Management

```python
# timeout_management.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def timeout_management():
    """Handle various timeout scenarios"""

    # Configure timeouts
    browser_config = BrowserConfig(
        navigation_timeout=10,     # 10 seconds for navigation
        element_timeout=5,         # 5 seconds for element waiting
        script_timeout=30,         # 30 seconds for scripts
    )

    agent = Agent(
        task="""
        Test timeout handling:

        1. Go to https://httpbin.org/delay/2 (2 second delay - should work)
        2. Verify the response loads within timeout

        3. Try to access https://httpbin.org/delay/15 (15 second delay - may timeout)
        4. Handle the timeout gracefully if it occurs

        5. Go to a normal page to confirm browser still works

        Return results of timeout testing.
        """,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser_config,
        max_steps=20
    )

    result = await agent.run()
    print(f"Timeout Management Results: {result}")

if __name__ == "__main__":
    asyncio.run(timeout_management())
```

## Performance Considerations

### Optimizing Browser Operations

```python
# performance_optimization.py
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI
from browser_use.browser.browser import BrowserConfig

async def performance_optimization():
    """Demonstrate performance optimization techniques"""

    # Optimized browser configuration
    browser_config = BrowserConfig(
        headless=True,           # Run headless for speed
        disable_images=True,     # Don't load images
        disable_javascript=False, # Keep JS for dynamic content
        extra_chromium_args=[
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",  # Additional image blocking
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
        ]
    )

    # Fast LLM for quick tasks
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Faster model
        temperature=0.1,      # More deterministic
        max_tokens=500        # Limit output
    )

    agent = Agent(
        task="""
        Perform a quick data extraction task:

        1. Go to https://httpbin.org/json
        2. Extract the JSON data
        3. Parse and summarize the content
        4. Return the results quickly

        Focus on speed and efficiency.
        """,
        llm=llm,
        browser=browser_config,
        max_steps=10,          # Limit steps
        use_vision=False,      # Skip vision for speed
    )

    import time
    start_time = time.time()

    result = await agent.run()

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Task completed in {execution_time:.2f} seconds")
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(performance_optimization())
```

## Summary

In this chapter, we've covered:

- **Navigation**: Basic page navigation and URL handling
- **Element Interaction**: Clicking buttons and links
- **Text Input**: Typing and form filling operations
- **Scrolling**: Page scrolling and infinite scroll handling
- **Browser State**: Managing cookies, sessions, and contexts
- **Error Handling**: Dealing with timeouts and navigation errors
- **Performance**: Optimizing browser operations for speed

## Key Takeaways

1. **Natural Language Control**: Describe browser actions in plain English
2. **Robust Element Detection**: Combines vision and DOM for reliable interaction
3. **Error Recovery**: Built-in retry logic and graceful error handling
4. **State Management**: Persistent sessions and cookie handling
5. **Performance Tuning**: Configuration options for speed optimization
6. **Timeout Handling**: Configurable timeouts for different operations

## Next Steps

Now that you understand browser control basics, let's explore **element selection** techniques for more precise web automation.

---

**Ready for Chapter 3?** [Element Selection](03-element-selection.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*