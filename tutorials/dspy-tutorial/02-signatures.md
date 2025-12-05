---
layout: default
title: "DSPy Tutorial - Chapter 2: Signatures"
nav_order: 2
has_children: false
parent: DSPy Tutorial
---

# Chapter 2: Signatures - Defining LM Input/Output Behavior

> Master the art of defining signatures, the fundamental abstraction that specifies what goes into and comes out of your language model calls.

## Overview

Signatures are the core abstraction in DSPy. They define the input/output contract for your LM calls, specifying what information goes in and what comes out. Unlike traditional prompting where you manually craft text, signatures allow DSPy to automatically optimize how the LM processes your inputs to produce the desired outputs.

## Basic Signature Structure

### Minimal Signature

```python
import dspy

class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""

    question = dspy.InputField()
    answer = dspy.OutputField()
```

### Complete Signature with Descriptions

```python
class DescriptiveQA(dspy.Signature):
    """Answer questions using provided context. Be concise and accurate."""

    context = dspy.InputField(desc="background information relevant to the question")
    question = dspy.InputField(desc="the question to answer")
    answer = dspy.OutputField(desc="concise answer, typically 1-5 words")
```

## Field Types and Properties

### InputField Properties

```python
class AdvancedInputs(dspy.Signature):
    """Demonstrate various InputField configurations."""

    # Basic input
    query = dspy.InputField()

    # Input with description
    context = dspy.InputField(desc="relevant background information")

    # Required vs optional inputs
    required_field = dspy.InputField(desc="this field is required")
    optional_field = dspy.InputField(desc="this field is optional", required=False)

    # Prefixed inputs (adds prefix to the field name in prompts)
    user_query = dspy.InputField(desc="what the user asked", prefix="User: ")
    system_info = dspy.InputField(desc="system context", prefix="System: ")
```

### OutputField Properties

```python
class AdvancedOutputs(dspy.Signature):
    """Demonstrate various OutputField configurations."""

    # Basic output
    answer = dspy.OutputField()

    # Output with description and guidance
    summary = dspy.OutputField(desc="brief summary, 2-3 sentences")

    # Structured outputs
    category = dspy.OutputField(desc="classify as: positive, negative, neutral")
    confidence = dspy.OutputField(desc="confidence score from 0.0 to 1.0")

    # Multiple choice outputs
    choice = dspy.OutputField(desc="select one: A, B, C, or D")

    # Prefixed outputs
    reasoning = dspy.OutputField(desc="step-by-step reasoning", prefix="Reasoning: ")
    final_answer = dspy.OutputField(desc="the final answer", prefix="Answer: ")
```

## Signature Patterns

### Question Answering

```python
class QuestionAnswering(dspy.Signature):
    """Answer questions based on provided context."""

    context = dspy.InputField(desc="relevant passages from knowledge base")
    question = dspy.InputField(desc="question to answer")
    answer = dspy.OutputField(desc="answer supported by context")

# Usage
qa = dspy.Predict(QuestionAnswering)
result = qa(context="Paris is the capital of France.", question="What is the capital of France?")
print(result.answer)  # "Paris"
```

### Text Generation

```python
class TextGeneration(dspy.Signature):
    """Generate text based on a prompt."""

    prompt = dspy.InputField(desc="description of what to generate")
    style = dspy.InputField(desc="writing style: formal, casual, technical")
    length = dspy.InputField(desc="approximate word count")
    generated_text = dspy.OutputField(desc="the generated content")

# Usage
generator = dspy.Predict(TextGeneration)
result = generator(
    prompt="Write about climate change",
    style="formal",
    length="200"
)
```

### Classification Tasks

```python
class SentimentAnalysis(dspy.Signature):
    """Analyze sentiment of given text."""

    text = dspy.InputField(desc="text to analyze")
    sentiment = dspy.OutputField(desc="positive, negative, or neutral")
    confidence = dspy.OutputField(desc="confidence score 0.0-1.0")
    reasoning = dspy.OutputField(desc="brief explanation for classification")

# Usage
classifier = dspy.Predict(SentimentAnalysis)
result = classifier(text="I love this product!")
print(f"Sentiment: {result.sentiment}, Confidence: {result.confidence}")
```

### Code Generation

```python
class CodeGeneration(dspy.Signature):
    """Generate code based on specification."""

    language = dspy.InputField(desc="programming language")
    task = dspy.InputField(desc="what the code should do")
    requirements = dspy.InputField(desc="specific requirements or constraints")
    code = dspy.OutputField(desc="complete, runnable code")
    explanation = dspy.OutputField(desc="brief explanation of how the code works")

# Usage
coder = dspy.Predict(CodeGeneration)
result = coder(
    language="Python",
    task="sort a list of numbers",
    requirements="use bubble sort algorithm"
)
```

### Multi-Step Reasoning

```python
class MultiStepReasoning(dspy.Signature):
    """Solve problems with step-by-step reasoning."""

    problem = dspy.InputField(desc="the problem to solve")
    step1_reasoning = dspy.OutputField(desc="first step of reasoning")
    step1_answer = dspy.OutputField(desc="result of first step")
    step2_reasoning = dspy.OutputField(desc="second step of reasoning")
    step2_answer = dspy.OutputField(desc="result of second step")
    final_answer = dspy.OutputField(desc="final solution")

# Usage
reasoner = dspy.ChainOfThought(MultiStepReasoning)
result = reasoner(problem="Calculate 15% of 80")
```

## Advanced Signature Techniques

### Conditional Fields

```python
class ConditionalSignature(dspy.Signature):
    """Signature with conditional field requirements."""

    task_type = dspy.InputField(desc="type of task: math, text, code")

    # Conditional fields based on task_type
    math_problem = dspy.InputField(desc="math problem to solve", required=False)
    text_input = dspy.InputField(desc="text to process", required=False)
    code_spec = dspy.InputField(desc="code specification", required=False)

    output = dspy.OutputField(desc="result based on task type")

    def validate(self):
        """Custom validation logic"""
        if self.task_type == "math" and not self.math_problem:
            raise ValueError("math_problem required for math tasks")
        if self.task_type == "text" and not self.text_input:
            raise ValueError("text_input required for text tasks")
        if self.task_type == "code" and not self.code_spec:
            raise ValueError("code_spec required for code tasks")
```

### Structured Outputs

```python
class StructuredOutput(dspy.Signature):
    """Generate structured JSON-like outputs."""

    query = dspy.InputField(desc="user query")
    format_type = dspy.InputField(desc="desired output format: json, xml, csv")

    # Structured output fields
    title = dspy.OutputField(desc="main title or heading")
    summary = dspy.OutputField(desc="brief summary")
    tags = dspy.OutputField(desc="comma-separated list of tags")
    metadata = dspy.OutputField(desc="additional metadata as key-value pairs")

# Usage with structured parsing
structured = dspy.Predict(StructuredOutput)
result = structured(
    query="Summarize the latest AI developments",
    format_type="json"
)
```

### Multi-Modal Signatures

```python
class MultiModalSignature(dspy.Signature):
    """Handle multiple input modalities."""

    text_description = dspy.InputField(desc="text description of the task")
    image_url = dspy.InputField(desc="URL of image to analyze", required=False)
    audio_transcript = dspy.InputField(desc="transcription of audio", required=False)

    combined_analysis = dspy.OutputField(desc="analysis combining all modalities")
    key_insights = dspy.OutputField(desc="main insights from the analysis")

# Note: Actual multi-modal support depends on the underlying LM
```

## Signature Composition

### Combining Signatures

```python
class CombinedSignature(dspy.Signature):
    """Combine multiple signature patterns."""

    # Input section
    user_query = dspy.InputField(desc="original user question")
    context = dspy.InputField(desc="relevant background information")

    # Processing fields
    reasoning = dspy.OutputField(desc="step-by-step reasoning process")
    confidence = dspy.OutputField(desc="confidence in the answer")

    # Output section
    answer = dspy.OutputField(desc="final answer")
    sources = dspy.OutputField(desc="sources used for the answer")
```

### Hierarchical Signatures

```python
class HierarchicalQA(dspy.Signature):
    """Multi-level question answering."""

    question = dspy.InputField()

    # First level: categorize
    category = dspy.OutputField(desc="question category: factual, opinion, procedural")

    # Second level: answer based on category
    factual_answer = dspy.OutputField(desc="answer for factual questions", required=False)
    opinion_answer = dspy.OutputField(desc="answer for opinion questions", required=False)
    procedural_answer = dspy.OutputField(desc="answer for procedural questions", required=False)

    # Meta information
    confidence = dspy.OutputField(desc="confidence score")
    reasoning = dspy.OutputField(desc="reasoning for categorization")
```

## Signature Optimization

### Manual Optimization

```python
class OptimizedQA(dspy.Signature):
    """Manually optimized signature for better performance."""

    question = dspy.InputField(desc="clear, specific question requiring factual answer")

    # Provide more context to the model
    context = dspy.InputField(
        desc="relevant facts and information to help answer the question accurately",
        required=False
    )

    # More detailed output specification
    answer = dspy.OutputField(
        desc="concise, accurate answer based on facts. Use evidence from context when available."
    )

    # Additional quality indicators
    confidence = dspy.OutputField(
        desc="confidence level: high, medium, or low",
        required=False
    )

    evidence = dspy.OutputField(
        desc="key facts or evidence supporting the answer",
        required=False
    )
```

### DSPy-Optimized Signatures

DSPy can automatically optimize signatures:

```python
# DSPy will automatically improve this signature during optimization
class AutoOptimizedQA(dspy.Signature):
    """DSPy will optimize this signature automatically."""

    question = dspy.InputField()
    answer = dspy.OutputField()

# Later, during compilation:
# teleprompter = dspy.BootstrapFewShot(...)
# optimized_program = teleprompter.compile(program, trainset)
# The signature prompts will be automatically improved
```

## Signature Best Practices

### Clarity and Specificity

```python
# Bad: Vague descriptions
class VagueSignature(dspy.Signature):
    text = dspy.InputField()
    output = dspy.OutputField()

# Good: Clear, specific descriptions
class ClearSignature(dspy.Signature):
    """Extract key information from product reviews."""

    review_text = dspy.InputField(desc="customer review text to analyze")
    product_name = dspy.OutputField(desc="name of the product being reviewed")
    rating = dspy.OutputField(desc="numerical rating out of 5 stars")
    sentiment = dspy.OutputField(desc="overall sentiment: positive, negative, neutral")
    key_features = dspy.OutputField(desc="main features mentioned, comma-separated")
```

### Appropriate Granularity

```python
# Too granular (too many fields)
class OverGranular(dspy.Signature):
    input1 = dspy.InputField()
    input2 = dspy.InputField()
    input3 = dspy.InputField()
    output1 = dspy.OutputField()
    output2 = dspy.OutputField()
    output3 = dspy.OutputField()
    output4 = dspy.OutputField()
    output5 = dspy.OutputField()

# Just right granularity
class AppropriateGranular(dspy.Signature):
    """Process customer feedback comprehensively."""

    customer_feedback = dspy.InputField(desc="raw customer feedback text")

    analysis = dspy.OutputField(desc="""structured analysis containing:
    - Overall sentiment (positive/negative/neutral)
    - Key themes and topics
    - Specific suggestions or complaints
    - Priority level (high/medium/low)""")
```

### Error Handling

```python
class RobustSignature(dspy.Signature):
    """Signature with built-in error handling guidance."""

    task = dspy.InputField(desc="the task to perform")
    constraints = dspy.InputField(desc="any constraints or requirements", required=False)

    result = dspy.OutputField(desc="the completed task result")
    success = dspy.OutputField(desc="whether the task was completed successfully: yes/no")
    error_message = dspy.OutputField(desc="error message if task failed", required=False)
    retry_suggestion = dspy.OutputField(desc="suggestion for how to retry if failed", required=False)
```

## Testing Signatures

### Unit Testing

```python
def test_signature():
    """Test signature behavior with various inputs."""

    # Test basic functionality
    qa = dspy.Predict(BasicQA)

    # Test with simple question
    result = qa(question="What is 2+2?")
    assert hasattr(result, 'answer')
    assert isinstance(result.answer, str)

    # Test with complex question
    result = qa(question="Explain quantum computing in simple terms")
    assert len(result.answer) > 10  # Should give detailed answer

    print("All signature tests passed!")

# Run tests
test_signature()
```

### Signature Validation

```python
def validate_signature_output(signature_class, inputs, expected_outputs):
    """Validate that signature produces expected output structure."""

    program = dspy.Predict(signature_class)

    for input_data, expected in zip(inputs, expected_outputs):
        result = program(**input_data)

        # Check that all expected fields are present
        for field in expected:
            assert hasattr(result, field), f"Missing field: {field}"

        # Check field types
        for field, expected_type in expected.items():
            actual_value = getattr(result, field)
            assert isinstance(actual_value, expected_type), \
                f"Field {field}: expected {expected_type}, got {type(actual_value)}"

    print("Signature validation passed!")

# Example validation
validate_signature_output(
    SentimentAnalysis,
    [{"text": "I love this product!"}],
    [{"sentiment": str, "confidence": str, "reasoning": str}]
)
```

## Common Signature Patterns

### RAG Signatures

```python
class RAGSignature(dspy.Signature):
    """Standard signature for retrieval-augmented generation."""

    question = dspy.InputField(desc="user question")
    context = dspy.InputField(desc="retrieved relevant passages")

    answer = dspy.OutputField(desc="answer based on context")
    confidence = dspy.OutputField(desc="confidence in answer: high/medium/low")
    evidence = dspy.OutputField(desc="quotes from context supporting the answer")
```

### Chain-of-Thought Signatures

```python
class CoTSignature(dspy.Signature):
    """Signature for chain-of-thought reasoning."""

    question = dspy.InputField(desc="problem to solve")

    reasoning = dspy.OutputField(desc="step-by-step reasoning process")
    answer = dspy.OutputField(desc="final answer")
```

### Multi-Agent Signatures

```python
class MultiAgentSignature(dspy.Signature):
    """Signature for coordinating multiple agents."""

    task = dspy.InputField(desc="overall task to accomplish")
    agent_outputs = dspy.InputField(desc="outputs from individual agents")

    synthesis = dspy.OutputField(desc="synthesized result combining all inputs")
    coordination_notes = dspy.OutputField(desc="notes on how inputs were combined")
```

## Summary

In this chapter, we've explored:

- **Basic Signature Structure** - InputField and OutputField with descriptions
- **Field Properties** - Required/optional fields, prefixes, and constraints
- **Common Patterns** - QA, classification, generation, and reasoning signatures
- **Advanced Techniques** - Conditional fields, structured outputs, and composition
- **Optimization** - Manual and automatic signature improvement
- **Best Practices** - Clarity, granularity, and error handling
- **Testing** - Unit tests and validation for signatures

Signatures are the foundation of DSPy programming. They define the interface between your program and the language model, allowing DSPy to automatically optimize prompts and model configurations.

## Key Takeaways

1. **Clarity Matters**: Detailed field descriptions guide LM behavior
2. **Structure Enables Optimization**: Well-defined signatures allow DSPy to optimize automatically
3. **Granularity Balance**: Too few fields limit expressiveness, too many create complexity
4. **Validation is Key**: Test signatures thoroughly to ensure reliable behavior
5. **Patterns Exist**: Reuse common signature patterns for similar tasks

Next, we'll explore **modules** - the reusable components that implement signature behavior.

---

**Ready for the next chapter?** [Chapter 3: Modules](03-modules.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*