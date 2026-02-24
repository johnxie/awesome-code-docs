---
layout: default
title: "Chapter 2: Prompt Templates & Chains"
parent: "LangChain Tutorial"
nav_order: 2
---

# Chapter 2: Prompt Templates & Chains

Welcome to **Chapter 2: Prompt Templates & Chains**. In this part of **LangChain Tutorial: Building AI Applications with Large Language Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Now that you have LangChain set up and working, let's learn about one of its most powerful features: **Prompt Templates** and **Chains**. These tools will help you create consistent, reusable interactions with language models.

## What Problem Do Prompt Templates Solve?

Imagine you're building a customer support chatbot. You want it to always respond in a friendly, professional manner, but adapt to different situations. Without prompt templates, you'd have to rewrite the same basic instructions every time:

```python
# Without templates - repetitive and error-prone
response1 = chat.invoke([
    HumanMessage(content="You are a helpful customer support agent for TechCorp. Always be polite and offer solutions. Customer says: My laptop won't turn on.")
])

response2 = chat.invoke([
    HumanMessage(content="You are a helpful customer support agent for TechCorp. Always be polite and offer solutions. Customer says: I forgot my password.")
])
```

With prompt templates, you write the instructions once and reuse them everywhere!

## Creating Your First Prompt Template

Let's start with a simple example:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Create a prompt template
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that specializes in {topic}."),
    ("human", "{question}")
])

# Use the template
prompt = template.invoke({
    "topic": "Python programming",
    "question": "How do I read a CSV file?"
})

print(prompt)
# Output:
# ChatPromptValue(messages=[
#     SystemMessage(content='You are a helpful assistant that specializes in Python programming.'),
#     HumanMessage(content='How do I read a CSV file?')
# ])
```

## How It Works Under the Hood

Prompt templates work by:

1. **Defining placeholders** using curly braces `{variable_name}`
2. **Providing values** when you invoke the template
3. **Generating complete prompts** ready for the language model

The `invoke()` method replaces all placeholders with actual values and returns a properly formatted prompt.

## Different Types of Prompt Templates

### 1. Chat Prompt Templates
Best for conversational AI with multiple message types:

```python
from langchain_core.prompts import ChatPromptTemplate

# Multi-turn conversation template
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} expert."),
    ("human", "What is {topic}?"),
    ("ai", "Let me explain {topic} to you."),
    ("human", "Can you give me a practical example?")
])

prompt = chat_template.invoke({
    "role": "Python",
    "topic": "list comprehensions"
})
```

### 2. String Prompt Templates
Simple templates for single messages:

```python
from langchain_core.prompts import PromptTemplate

# Simple string template
string_template = PromptTemplate.from_template(
    "Translate the following text from {source_lang} to {target_lang}: {text}"
)

prompt = string_template.invoke({
    "source_lang": "English",
    "target_lang": "Spanish",
    "text": "Hello, how are you?"
})
```

## Creating Chains

Now let's combine prompt templates with language models to create **chains**:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Create components
prompt = ChatPromptTemplate.from_template(
    "Tell me a fun fact about {topic}"
)

model = ChatOpenAI()
output_parser = StrOutputParser()

# Create a chain using the | operator (LangChain Expression Language)
chain = prompt | model | output_parser

# Use the chain
result = chain.invoke({"topic": "octopuses"})
print(result)
# Output: "Octopuses have three hearts and blue blood!..."
```

## How Chains Work Under the Hood

The `|` operator creates a **pipeline** where:
1. **Prompt** receives input and creates formatted messages
2. **Model** receives messages and generates response
3. **Output Parser** receives response and extracts useful data

This is called the **LangChain Expression Language (LCEL)** - a declarative way to compose components.

## Advanced Chain Patterns

### 1. Multi-Step Reasoning Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Step 1: Analyze the problem
analysis_prompt = ChatPromptTemplate.from_template(
    "Analyze this problem: {problem}\n\nWhat are the key components?"
)

# Step 2: Generate solution
solution_prompt = ChatPromptTemplate.from_template(
    "Based on this analysis: {analysis}\n\nProvide a step-by-step solution."
)

model = ChatOpenAI()

# Create multi-step chain
analysis_chain = analysis_prompt | model
solution_chain = solution_prompt | model

# Use both chains together
problem = "How do I optimize a slow database query?"

analysis = analysis_chain.invoke({"problem": problem})
solution = solution_chain.invoke({
    "problem": problem,
    "analysis": analysis.content
})

print(f"Analysis: {analysis.content}")
print(f"Solution: {solution.content}")
```

### 2. Conditional Chains

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def route_query(query):
    """Route queries to different specialists based on content"""
    if "code" in query.lower() or "programming" in query.lower():
        return "coder"
    elif "design" in query.lower() or "ui" in query.lower():
        return "designer"
    else:
        return "general"

# Different templates for different types of queries
templates = {
    "coder": ChatPromptTemplate.from_template(
        "You are a senior software engineer. Help with: {query}"
    ),
    "designer": ChatPromptTemplate.from_template(
        "You are a UX/UI designer. Help with: {query}"
    ),
    "general": ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer: {query}"
    )
}

model = ChatOpenAI()

def process_query(query):
    route = route_query(query)
    template = templates[route]
    chain = template | model

    result = chain.invoke({"query": query})
    return result.content

# Test the routing
print(process_query("How do I center a div in CSS?"))  # Routes to coder
print(process_query("What color should my button be?"))  # Routes to designer
```

## Best Practices for Prompt Templates

### 1. Be Specific
```python
# Good: Clear instructions
template = ChatPromptTemplate.from_template(
    "Explain {concept} in simple terms, as if teaching a beginner. Use one example."
)

# Avoid: Vague instructions
template = ChatPromptTemplate.from_template(
    "Tell me about {concept}"
)
```

### 2. Use Examples
```python
template = ChatPromptTemplate.from_template("""
Classify this product review as positive, negative, or neutral.

Review: {review}

Examples:
- "Great product, highly recommend!" → positive
- "It's okay, nothing special" → neutral
- "Poor quality, don't buy" → negative

Classification:"""
)
```

### 3. Provide Context
```python
template = ChatPromptTemplate.from_template("""
You are a {role} writing for {audience}.
Topic: {topic}
Style: {style}

Write a {length} article about {topic}:"""
)
```

## Common Patterns and Templates

### Code Review Template
```python
code_review_template = ChatPromptTemplate.from_template("""
Review this {language} code for:
1. Bugs and errors
2. Performance issues
3. Code style and best practices
4. Security concerns

Code:
```python
{code}
```

Provide specific recommendations for improvement.
""")
```

### Content Creation Template
```python
content_template = ChatPromptTemplate.from_template("""
Create {content_type} about {topic} for {audience}.

Requirements:
- Length: {length}
- Tone: {tone}
- Key points to cover: {key_points}

Make it engaging and informative.
""")
```

## Debugging Chains

When your chains don't work as expected:

```python
# Add debugging to see intermediate results
chain = prompt | (lambda x: (print(f"Prompt: {x}"), x)[1]) | model | output_parser

# Or use the built-in debugging
import langchain_core
langchain_core.debug = True

result = chain.invoke({"topic": "AI"})
```

## What We've Learned

Great job! 🎉 You've now mastered:

1. **Prompt Templates** - Reusable prompt structures with variables
2. **Basic Chains** - Combining prompts, models, and parsers
3. **Advanced Patterns** - Multi-step reasoning and conditional routing
4. **Best Practices** - Writing effective prompts and debugging chains

## Next Steps

Ready to add memory to your applications? In [Chapter 3: Memory Systems](03-memory-systems.md), we'll learn how to make your AI applications remember conversations and maintain context across interactions.

---

**Practice what you've learned:**
1. Create a prompt template for your favorite use case
2. Build a chain that uses it
3. Experiment with different variables and see how they affect results

*What's the most interesting chain you can think of building?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `ChatPromptTemplate`, `from_template`, `query` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Prompt Templates & Chains` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `template`, `topic`, `invoke` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Prompt Templates & Chains` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `ChatPromptTemplate`.
2. **Input normalization**: shape incoming data so `from_template` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `query`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `ChatPromptTemplate` and `from_template` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LangChain](01-getting-started.md)
- [Next Chapter: Chapter 3: Memory Systems](03-memory-systems.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
