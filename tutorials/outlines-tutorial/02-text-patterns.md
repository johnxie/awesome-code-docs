---
layout: default
title: "Outlines Tutorial - Chapter 2: Text Patterns"
nav_order: 2
has_children: false
parent: Outlines Tutorial
---

# Chapter 2: Text Patterns & Regular Expressions

> Master regex-based constrained generation - from simple patterns to complex string validation with guaranteed compliance.

## Basic Regex Constraints

### Simple Pattern Matching

```python
from outlines import models, generate
import re

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Generate email addresses
email_generator = generate.regex(
    model,
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

email = email_generator("Generate a professional email address for")
print(f"Generated email: {email}")

# Verify with regex
if re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email):
    print("✓ Valid email format")
else:
    print("✗ Invalid email format")
```

### Phone Number Generation

```python
# Generate US phone numbers
phone_generator = generate.regex(
    model,
    r"\(\d{3}\) \d{3}-\d{4}"  # (123) 456-7890 format
)

phone = phone_generator("Generate a business phone number")
print(f"Business phone: {phone}")

# Generate international phone numbers
intl_phone_generator = generate.regex(
    model,
    r"\+\d{1,3} \d{1,4} \d{1,4} \d{1,4}"  # +1 234 567 8901 format
)

intl_phone = intl_phone_generator("Generate an international phone number")
print(f"International phone: {intl_phone}")
```

## Advanced Regex Patterns

### Structured Data Extraction

```python
# Generate structured log entries
log_generator = generate.regex(
    model,
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \[(INFO|WARN|ERROR)\] [\w\s]+"
)

log_entry = log_generator("Generate a system log entry about")
print(f"Log entry: {log_entry}")

# Generate configuration file entries
config_generator = generate.regex(
    model,
    r"[A-Z_][A-Z0-9_]*\s*=\s*(true|false|\d+|"[^"]*"|'[^']*')"
)

config = config_generator("Generate a configuration setting for")
print(f"Config: {config}")
```

### Code Generation Patterns

```python
# Generate Python variable names
var_generator = generate.regex(
    model,
    r"[a-z_][a-zA-Z0-9_]*"  # Valid Python identifier
)

variable = var_generator("Generate a Python variable name for")
print(f"Variable: {variable}")

# Generate function definitions
func_generator = generate.regex(
    model,
    r"def [a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z0-9_,=\s]*\):"
)

function = func_generator("Generate a Python function definition for")
print(f"Function: {function}")

# Generate import statements
import_generator = generate.regex(
    model,
    r"(from [a-zA-Z_][a-zA-Z0-9_.]* import [a-zA-Z_][a-zA-Z0-9_*, ]*|import [a-zA-Z_][a-zA-Z0-9_.]+)"
)

import_stmt = import_generator("Generate a Python import statement for")
print(f"Import: {import_stmt}")
```

## Complex Pattern Combinations

### Multi-Part Patterns

```python
# Generate structured addresses
address_generator = generate.regex(
    model,
    r"\d+\s+[A-Z][a-zA-Z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr),\s*[A-Z][a-zA-Z\s]+,\s*[A-Z]{2}\s*\d{5}"
)

address = address_generator("Generate a complete mailing address")
print(f"Address: {address}")

# Generate credit card numbers (format only, not valid numbers)
cc_generator = generate.regex(
    model,
    r"\d{4} \d{4} \d{4} \d{4}"  # XXXX XXXX XXXX XXXX format
)

cc_number = cc_generator("Generate a credit card number for")
print(f"CC Number: {cc_number}")
```

### Conditional Patterns

```python
# Generate conditional responses
response_generator = generate.regex(
    model,
    r"(Yes|No), (?:because|since|as) .+\."
)

response = response_generator("Should I proceed?")
print(f"Response: {response}")

# Generate decision explanations
decision_generator = generate.regex(
    model,
    r"I (recommend|suggest|advise) (?:you )?(?:to )?\w+ (?:because|since|as|due to) .+\."
)

decision = decision_generator("What should I do about")
print(f"Decision: {decision}")
```

## Regex Performance Optimization

### Efficient Pattern Design

```python
import time
from outlines import generate, models

model = models.transformers("microsoft/DialoGPT-small")

def benchmark_regex_pattern(pattern: str, test_prompt: str, iterations: int = 10):
    """Benchmark regex pattern performance."""

    generator = generate.regex(model, pattern)

    start_time = time.time()
    results = []

    for _ in range(iterations):
        result = generator(test_prompt)
        results.append(result)

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations

    return {
        "pattern": pattern,
        "avg_time": avg_time,
        "results": results[:3],  # First 3 examples
        "iterations": iterations
    }

# Compare pattern efficiency
patterns = [
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}", # Email with length limit
    r"\d{4}-\d{2}-\d{2}",                                 # Date
    r"\d{1,2}/\d{1,2}/\d{4}",                            # US date
]

for pattern in patterns:
    result = benchmark_regex_pattern(pattern, "Generate a", 5)
    print(f"Pattern: {pattern}")
    print(f"Avg time: {result['avg_time']:.3f}s")
    print(f"Sample: {result['results'][0]}")
    print("-" * 50)
```

### Pattern Precompilation

```python
import re
from outlines.generate import RegexGenerator

class OptimizedRegexGenerator:
    def __init__(self, model, pattern: str):
        self.model = model
        self.pattern = pattern
        self.compiled_regex = re.compile(pattern)
        self.generator = RegexGenerator(model, pattern)

    def validate_output(self, text: str) -> bool:
        """Validate if generated text matches pattern."""
        return bool(self.compiled_regex.match(text))

    def generate_with_validation(self, prompt: str, max_attempts: int = 3) -> str:
        """Generate with validation and retry."""

        for attempt in range(max_attempts):
            result = self.generator(prompt)

            if self.validate_output(result):
                return result
            else:
                print(f"Attempt {attempt + 1}: Generated text doesn't match pattern")
                print(f"Expected: {self.pattern}")
                print(f"Got: '{result}'")

        raise ValueError(f"Failed to generate valid output after {max_attempts} attempts")

# Usage
email_gen = OptimizedRegexGenerator(
    model,
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

email = email_gen.generate_with_validation("Generate a professional email")
print(f"Validated email: {email}")
```

## Pattern Libraries

### Domain-Specific Patterns

```python
class PatternLibrary:
    """Collection of useful regex patterns for different domains."""

    # Communication
    EMAIL = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_US = r"\(\d{3}\) \d{3}-\d{4}"
    URL = r"https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?"

    # Identification
    SSN = r"\d{3}-\d{2}-\d{4}"
    CREDIT_CARD = r"\d{4} \d{4} \d{4} \d{4}"
    PASSPORT = r"[A-Z]{1,2}\d{6,9}"

    # Data formats
    DATE_ISO = r"\d{4}-\d{2}-\d{2}"
    TIME_24H = r"\d{2}:\d{2}:\d{2}"
    IP_ADDRESS = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    # Programming
    PYTHON_VAR = r"[a-zA-Z_][a-zA-Z0-9_]*"
    EMAIL_VAR = r"[\w\.-]+@[\w\.-]+\.\w+"
    FUNCTION_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Business
    PRODUCT_CODE = r"[A-Z]{2,3}\d{4,6}"
    INVOICE_NUMBER = r"INV-\d{6}"
    EMPLOYEE_ID = r"EMP\d{6}"

    @classmethod
    def get_generator(cls, model, pattern_name: str):
        """Get a generator for a named pattern."""
        pattern = getattr(cls, pattern_name.upper(), None)
        if not pattern:
            raise ValueError(f"Unknown pattern: {pattern_name}")

        return generate.regex(model, pattern)

# Usage
patterns = PatternLibrary()

# Generate business data
invoice_gen = patterns.get_generator(model, "invoice_number")
product_gen = patterns.get_generator(model, "product_code")

invoice = invoice_gen("Generate an invoice number")
product = product_gen("Generate a product code")

print(f"Invoice: {invoice}")
print(f"Product: {product}")
```

### Custom Pattern Builder

```python
class RegexPatternBuilder:
    """Builder for complex regex patterns."""

    def __init__(self):
        self.parts = []

    def add_literal(self, text: str):
        """Add literal text."""
        self.parts.append(re.escape(text))
        return self

    def add_digits(self, count: int, exact: bool = True):
        """Add digit sequence."""
        if exact:
            self.parts.append(f"\\d{{{count}}}")
        else:
            self.parts.append(f"\\d{{{count}}}")
        return self

    def add_word_chars(self, min_len: int = 1, max_len: int = None):
        """Add word characters."""
        if max_len:
            self.parts.append(f"[a-zA-Z0-9_]{{{min_len},{max_len}}}")
        else:
            self.parts.append(f"[a-zA-Z0-9_]{{{min_len}}}")
        return self

    def add_choice(self, options: list):
        """Add choice between options."""
        escaped = [re.escape(opt) for opt in options]
        self.parts.append(f"(?:{'|'.join(escaped)})")
        return self

    def add_optional(self, pattern: str):
        """Add optional pattern."""
        self.parts.append(f"(?:{pattern})?")
        return self

    def build(self) -> str:
        """Build the complete regex pattern."""
        return "".join(self.parts)

# Usage
builder = RegexPatternBuilder()

# Build a complex pattern
pattern = (builder
    .add_literal("User: ")
    .add_word_chars(3, 20)
    .add_literal(" (")
    .add_choice(["admin", "user", "guest"])
    .add_literal(") - ")
    .add_choice(["login", "logout", "action"])
    .add_literal(" at ")
    .add_digits(2)
    .add_literal(":")
    .add_digits(2)
    .build())

print(f"Generated pattern: {pattern}")

# Use the pattern
complex_gen = generate.regex(model, pattern)
result = complex_gen("Generate a user log entry")
print(f"Generated: {result}")
```

## Error Handling & Validation

### Pattern Validation

```python
def validate_regex_pattern(pattern: str) -> dict:
    """Validate regex pattern and provide feedback."""

    result = {
        "valid": False,
        "error": None,
        "warnings": [],
        "complexity": "unknown"
    }

    try:
        # Try to compile the pattern
        compiled = re.compile(pattern)
        result["valid"] = True

        # Check for potential issues
        if len(pattern) > 1000:
            result["warnings"].append("Pattern is very long, may impact performance")

        # Count groups and complexity
        group_count = len(re.findall(r'\([^?]', pattern))
        if group_count > 10:
            result["warnings"].append(f"High number of groups ({group_count}), may be complex")

        # Estimate complexity
        if group_count < 3 and len(pattern) < 50:
            result["complexity"] = "simple"
        elif group_count < 5 and len(pattern) < 100:
            result["complexity"] = "medium"
        else:
            result["complexity"] = "complex"

    except re.error as e:
        result["error"] = str(e)

    return result

# Test patterns
test_patterns = [
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    r"(?:a|b|c){100}",  # Too complex
    r"[",               # Invalid syntax
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
]

for pattern in test_patterns:
    validation = validate_regex_pattern(pattern)
    status = "✓" if validation["valid"] else "✗"
    print(f"{status} {pattern}")
    if validation["error"]:
        print(f"   Error: {validation['error']}")
    if validation["warnings"]:
        print(f"   Warnings: {validation['warnings']}")
    print(f"   Complexity: {validation['complexity']}")
    print()
```

## Integration with Token-Level Control

### Advanced Masking Strategies

```python
from outlines.processors import RegexProcessor
import torch

class AdvancedRegexGenerator:
    def __init__(self, model, pattern: str):
        self.model = model
        self.pattern = pattern
        self.processor = RegexProcessor(pattern, model.tokenizer)

    def generate_with_masking(self, prompt: str, max_tokens: int = 50) -> str:
        """Generate text with regex masking."""

        input_ids = self.model.tokenizer.encode(prompt, return_tensors="pt")

        generated = input_ids
        mask = None

        for _ in range(max_tokens):
            # Get next token mask from regex processor
            mask = self.processor.get_mask(self.model.tokenizer, generated)

            # Forward pass
            with torch.no_grad():
                outputs = self.model.model(generated)
                next_token_logits = outputs.logits[:, -1, :]

            # Apply mask
            if mask is not None:
                next_token_logits[~mask] = float('-inf')

            # Sample next token
            next_token = torch.multinomial(
                torch.softmax(next_token_logits, dim=-1),
                num_samples=1
            )

            # Append to sequence
            generated = torch.cat([generated, next_token], dim=-1)

            # Check if we've completed the pattern
            if self.processor.is_finished(generated):
                break

        # Decode result
        result = self.model.tokenizer.decode(generated[0], skip_special_tokens=True)

        # Extract just the generated part
        if result.startswith(prompt):
            result = result[len(prompt):].strip()

        return result

# Usage
advanced_gen = AdvancedRegexGenerator(model, r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
email = advanced_gen.generate_with_masking("Contact: ")
print(f"Advanced generated email: {email}")
```

## Performance Comparison

### Regex vs Other Methods

```python
import time

def compare_generation_methods():
    """Compare regex generation with other constrained methods."""

    test_prompt = "Generate an email address for"
    iterations = 10

    # Regex method
    regex_gen = generate.regex(model, r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    start_time = time.time()
    regex_results = [regex_gen(test_prompt) for _ in range(iterations)]
    regex_time = time.time() - start_time

    # Choice method (limited options)
    choice_gen = generate.choice(model, ["user@example.com", "admin@test.com", "info@company.com"])

    start_time = time.time()
    choice_results = [choice_gen(test_prompt) for _ in range(iterations)]
    choice_time = time.time() - start_time

    # Unconstrained method
    text_gen = generate.text(model, max_tokens=20)

    start_time = time.time()
    text_results = [text_gen(test_prompt) for _ in range(iterations)]
    text_time = time.time() - start_time

    print("Performance Comparison:")
    print(f"Regex:     {regex_time:.2f}s ({regex_time/iterations:.3f}s per generation)")
    print(f"Choice:    {choice_time:.2f}s ({choice_time/iterations:.3f}s per generation)")
    print(f"Unconstrained: {text_time:.2f}s ({text_time/iterations:.3f}s per generation)")

    print("
Sample Results:")
    print(f"Regex:     {regex_results[0]}")
    print(f"Choice:    {choice_results[0]}")
    print(f"Unconstrained: {text_results[0][:50]}...")

compare_generation_methods()
```

This comprehensive guide to text patterns and regular expressions shows how Outlines can enforce complex string constraints while maintaining high performance. The next chapter explores JSON Schema validation for structured data generation. 🚀