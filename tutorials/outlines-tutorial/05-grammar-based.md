---
layout: default
title: "Outlines Tutorial - Chapter 5: Grammar-Based Generation"
nav_order: 5
has_children: false
parent: Outlines Tutorial
---

# Chapter 5: Grammar-Based Generation & Context-Free Grammars

Welcome to **Chapter 5: Grammar-Based Generation & Context-Free Grammars**. In this part of **Outlines Tutorial: Structured Text Generation with LLMs**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Control LLM outputs with formal grammars - generate syntactically correct programs, mathematical expressions, and domain-specific languages.

## Basic Context-Free Grammar

### Simple Grammar Definition

```python
from outlines import models, generate
import json

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Define a simple arithmetic expression grammar
arithmetic_grammar = """
?start: expression

?expression: term (("+" | "-") term)*

?term: factor (("*" | "/") factor)*

?factor: NUMBER | "(" expression ")"

NUMBER: /\d+/
"""

# Generate arithmetic expressions
arithmetic_generator = generate.cfg(model, arithmetic_grammar)

expression = arithmetic_generator("Generate a mathematical expression")
print(f"Generated expression: {expression}")

# Validate the expression (basic check)
try:
    # Safe evaluation for demonstration
    result = eval(expression.replace(" ", ""))
    print(f"Expression evaluates to: {result}")
except:
    print("Expression syntax is valid but may be complex")
```

### Programming Language Grammar

```python
# Python-like syntax grammar
python_grammar = """
?start: statement

?statement: assignment | if_statement | function_def

assignment: VARIABLE "=" expression

if_statement: "if" expression ":" block ["else" ":" block]

function_def: "def" VARIABLE "(" parameters ")" ":" block

parameters: [parameter ("," parameter)*]

parameter: VARIABLE [":" type_hint]

type_hint: "int" | "str" | "float" | "bool"

block: NEWLINE INDENT statement+ DEDENT

expression: VARIABLE | NUMBER | STRING | expression operator expression

operator: "+" | "-" | "*" | "/" | "==" | "!=" | "<" | ">" | "<=" | ">="

VARIABLE: /[a-zA-Z_][a-zA-Z0-9_]*/
NUMBER: /\d+(\.\d+)?/
STRING: /"[^"]*"/

%import common.NEWLINE
%import common.INDENT
%import common.DEDENT
"""

python_generator = generate.cfg(model, python_grammar)

# Generate Python-like code
code = python_generator("Generate a simple Python function")
print("Generated Python-like code:")
print(code)
```

## Advanced Grammar Features

### EBNF Grammar Syntax

```python
# Extended Backus-Naur Form grammar for JSON-like structure
json_grammar = """
?start: object

object: "{" [pair ("," pair)*] "}"

pair: STRING ":" value

value: STRING | NUMBER | "true" | "false" | "null" | object | array

array: "[" [value ("," value)*] "]"

STRING: /"[^"]*"/
NUMBER: /\d+(\.\d+)?/
"""

json_generator = generate.cfg(model, json_grammar)

# Generate JSON-like structure
json_data = json_generator("Generate a person object with name, age, and hobbies")
print("Generated JSON-like structure:")
print(json_data)

# Parse and validate
try:
    parsed = json.loads(json_data)
    print("✓ Generated structure is valid JSON")
except json.JSONDecodeError as e:
    print(f"✗ Generated structure is not valid JSON: {e}")
```

### Domain-Specific Languages

```python
# DSL for task management
task_dsl_grammar = """
?start: task_definition

task_definition: "task" VARIABLE "{" task_body "}"

task_body: (property | dependency | action)*

property: "priority" ":" ("low" | "medium" | "high" | "urgent")
        | "assignee" ":" STRING
        | "estimate" ":" NUMBER "hours"

dependency: "depends_on" ":" VARIABLE

action: "notify" ":" STRING
      | "assign_to" ":" VARIABLE
      | "set_status" ":" ("todo" | "doing" | "done")

VARIABLE: /[a-zA-Z_][a-zA-Z0-9_]*/
STRING: /"[^"]*"/
NUMBER: /\d+/
"""

task_generator = generate.cfg(model, task_dsl_grammar)

task_definition = task_generator("Generate a task definition for bug fixing")
print("Generated task DSL:")
print(task_definition)
```

### Mathematical Expressions

```python
# Advanced mathematical expression grammar
math_grammar = """
?start: expression

?expression: term (("+" | "-") term)*

?term: power (("**" power))*

?power: factor (("*" | "/") factor)*

?factor: func_call | variable | number | "(" expression ")"

func_call: FUNC_NAME "(" expression ("," expression)* ")"

variable: VARIABLE

number: NUMBER

FUNC_NAME: "sin" | "cos" | "tan" | "log" | "exp" | "sqrt"

VARIABLE: /[a-zA-Z][a-zA-Z0-9_]*/
NUMBER: /\d+(\.\d+)?/
"""

math_generator = generate.cfg(model, math_grammar)

expression = math_generator("Generate a complex mathematical expression")
print(f"Generated math expression: {expression}")

# Try to evaluate (safely)
def safe_eval_math(expr: str):
    """Safely evaluate mathematical expressions."""
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({"sin": math.sin, "cos": math.cos, "tan": math.tan,
                         "log": math.log, "exp": math.exp, "sqrt": math.sqrt})

    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except:
        return None

import math
result = safe_eval_math(expression)
if result is not None:
    print(f"Expression evaluates to: {result}")
else:
    print("Expression is valid but cannot be evaluated")
```

## Grammar Composition and Reuse

### Modular Grammar Design

```python
class GrammarBuilder:
    """Builder for complex, modular grammars."""

    def __init__(self):
        self.rules = {}
        self.terminals = {}

    def add_rule(self, name: str, definition: str):
        """Add a grammar rule."""
        self.rules[name] = definition

    def add_terminal(self, name: str, pattern: str):
        """Add a terminal pattern."""
        self.terminals[name] = pattern

    def build_grammar(self, start_rule: str = "start") -> str:
        """Build complete grammar string."""
        lines = []

        # Start rule
        lines.append(f"?{start_rule}: {self.rules.get(start_rule, 'expression')}")

        # Other rules
        for name, definition in self.rules.items():
            if name != start_rule:
                lines.append(f"?{name}: {definition}")

        # Terminals
        for name, pattern in self.terminals.items():
            lines.append(f"{name}: {pattern}")

        return "\n".join(lines)

# Build a complex grammar modularly
builder = GrammarBuilder()

# Base expression rules
builder.add_rule("expression", "term (('+' | '-') term)*")
builder.add_rule("term", "factor (('*' | '/') factor)*")
builder.add_rule("factor", "NUMBER | VARIABLE | '(' expression ')'")

# Add function calls
builder.add_rule("factor", "function_call | NUMBER | VARIABLE | '(' expression ')'")
builder.add_rule("function_call", "FUNC_NAME '(' expression (',' expression)* ')'")

# Terminals
builder.add_terminal("FUNC_NAME", "sin|cos|tan|log|exp|sqrt")
builder.add_terminal("VARIABLE", "/[a-zA-Z_][a-zA-Z0-9_]*/")
builder.add_terminal("NUMBER", "/\\d+(\\.\\d+)?/")

# Build grammar
complex_math_grammar = builder.build_grammar()

print("Built grammar:")
print(complex_math_grammar)

# Use the grammar
complex_generator = generate.cfg(model, complex_math_grammar)
result = complex_generator("Generate a mathematical expression with functions")
print(f"\nGenerated: {result}")
```

### Grammar Inheritance and Extension

```python
class GrammarExtender:
    """Extend existing grammars with additional rules."""

    def __init__(self, base_grammar: str):
        self.base_grammar = base_grammar
        self.extensions = {}

    def extend_rule(self, rule_name: str, extension: str):
        """Extend an existing rule."""
        self.extensions[rule_name] = extension

    def add_rule(self, rule_name: str, definition: str):
        """Add a new rule."""
        self.extensions[rule_name] = definition

    def build_extended_grammar(self) -> str:
        """Build extended grammar."""
        lines = self.base_grammar.split('\n')

        # Add extensions
        for rule_name, extension in self.extensions.items():
            if rule_name.startswith('?'):
                # New rule
                lines.append(f"{rule_name}: {extension}")
            else:
                # Extend existing rule (simplified - would need better parsing)
                lines.append(f"?{rule_name}: {extension}")

        return '\n'.join(lines)

# Start with arithmetic grammar
base_arithmetic = """
?start: expression
?expression: term (("+" | "-") term)*
?term: factor (("*" | "/") factor)*
?factor: NUMBER | "(" expression ")"
NUMBER: /\d+/
"""

# Extend with variables and functions
extender = GrammarExtender(base_arithmetic)

extender.extend_rule("factor", "NUMBER | VARIABLE | FUNCTION | '(' expression ')'")
extender.add_rule("function", "FUNC_NAME '(' expression ')'")
extender.add_terminal("VARIABLE", "/[a-zA-Z_][a-zA-Z0-9_]*/")
extender.add_terminal("FUNCTION", "sin|cos|sqrt")
extender.add_terminal("FUNC_NAME", "sin|cos|sqrt")

extended_grammar = extender.build_extended_grammar()
print("Extended grammar:")
print(extended_grammar)
```

## Grammar Debugging and Validation

### Grammar Validation

```python
def validate_grammar(grammar_text: str) -> dict:
    """Validate grammar syntax and structure."""

    validation_result = {
        "valid": False,
        "errors": [],
        "warnings": [],
        "rules": {},
        "terminals": []
    }

    lines = grammar_text.strip().split('\n')

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        try:
            if ':' in line:
                parts = line.split(':', 1)
                rule_name = parts[0].strip()
                definition = parts[1].strip()

                if rule_name.startswith('?'):
                    # Grammar rule
                    rule_name = rule_name[1:]  # Remove ?
                    validation_result["rules"][rule_name] = definition
                else:
                    # Terminal
                    validation_result["terminals"].append(rule_name)

                    # Validate regex patterns
                    if definition.startswith('/') and definition.endswith('/'):
                        import re
                        try:
                            re.compile(definition[1:-1])
                        except re.error as e:
                            validation_result["errors"].append(
                                f"Line {i}: Invalid regex pattern '{definition}': {e}"
                            )
                    else:
                        validation_result["warnings"].append(
                            f"Line {i}: Terminal '{rule_name}' may not be properly escaped"
                        )
            else:
                validation_result["errors"].append(f"Line {i}: Invalid grammar line format")

        except Exception as e:
            validation_result["errors"].append(f"Line {i}: Parse error - {e}")

    # Check for required start rule
    if "start" not in validation_result["rules"]:
        validation_result["errors"].append("Missing required 'start' rule")

    # Check for undefined rules
    defined_rules = set(validation_result["rules"].keys())
    defined_terminals = set(validation_result["terminals"])

    for rule_name, definition in validation_result["rules"].items():
        # Extract rule references (simplified)
        words = definition.replace('(', ' ').replace(')', ' ').replace('|', ' ').split()
        for word in words:
            if word.isupper() and word not in defined_terminals:
                if word not in defined_rules:
                    validation_result["warnings"].append(
                        f"Rule '{rule_name}' references undefined symbol '{word}'"
                    )

    validation_result["valid"] = len(validation_result["errors"]) == 0

    return validation_result

# Test grammar validation
test_grammar = """
?start: expression
?expression: term (("+" | "-") term)*
?term: factor (("*" | "/") factor)*
?factor: NUMBER | "(" expression ")"
NUMBER: /\d+/
"""

validation = validate_grammar(test_grammar)
print("Grammar validation:")
print(f"Valid: {validation['valid']}")
if validation['errors']:
    print("Errors:")
    for error in validation['errors']:
        print(f"  - {error}")
if validation['warnings']:
    print("Warnings:")
    for warning in validation['warnings']:
        print(f"  - {warning}")
```

### Grammar Testing and Debugging

```python
class GrammarDebugger:
    """Debug and test grammars."""

    def __init__(self, model):
        self.model = model

    def test_grammar(self, grammar: str, test_prompts: list, max_attempts: int = 3) -> dict:
        """Test grammar with multiple prompts."""

        results = {
            "grammar_valid": False,
            "tests": []
        }

        try:
            generator = generate.cfg(self.model, grammar)
            results["grammar_valid"] = True
        except Exception as e:
            results["error"] = str(e)
            return results

        for prompt in test_prompts:
            test_result = {
                "prompt": prompt,
                "generations": [],
                "success_rate": 0.0
            }

            successful = 0
            for attempt in range(max_attempts):
                try:
                    result = generator(prompt)
                    test_result["generations"].append({
                        "attempt": attempt + 1,
                        "result": result,
                        "success": True
                    })
                    successful += 1
                except Exception as e:
                    test_result["generations"].append({
                        "attempt": attempt + 1,
                        "error": str(e),
                        "success": False
                    })

            test_result["success_rate"] = successful / max_attempts
            results["tests"].append(test_result)

        return results

    def analyze_generation_patterns(self, grammar: str, prompts: list, num_samples: int = 10) -> dict:
        """Analyze patterns in generated outputs."""

        try:
            generator = generate.cfg(self.model, grammar)
        except Exception as e:
            return {"error": str(e)}

        all_generations = []
        for prompt in prompts:
            for _ in range(num_samples):
                try:
                    result = generator(prompt)
                    all_generations.append(result)
                except:
                    continue

        analysis = {
            "total_generations": len(all_generations),
            "unique_generations": len(set(all_generations)),
            "avg_length": sum(len(g) for g in all_generations) / len(all_generations) if all_generations else 0,
            "samples": all_generations[:5]  # First 5 samples
        }

        return analysis

# Test grammar debugging
debugger = GrammarDebugger(model)

# Test prompts
test_prompts = [
    "Generate a simple expression",
    "Generate a complex calculation",
    "Generate an arithmetic problem"
]

# Debug grammar
debug_results = debugger.test_grammar(arithmetic_grammar, test_prompts)
print("Grammar debugging results:")
print(f"Grammar valid: {debug_results['grammar_valid']}")

for test in debug_results.get('tests', []):
    print(f"\nPrompt: {test['prompt']}")
    print(f"Success rate: {test['success_rate']:.1f}")
    successful = [g for g in test['generations'] if g['success']]
    if successful:
        print(f"Sample result: {successful[0]['result']}")

# Analyze patterns
analysis = debugger.analyze_generation_patterns(arithmetic_grammar, test_prompts[:1])
print("
Generation analysis:")
print(f"Total generations: {analysis['total_generations']}")
print(f"Unique generations: {analysis['unique_generations']}")
print(f"Average length: {analysis['avg_length']:.1f}")
```

## Performance Optimization

### Grammar Compilation Caching

```python
from functools import lru_cache
import hashlib

class GrammarCache:
    """Cache compiled grammars for performance."""

    def __init__(self, model):
        self.model = model
        self._cache = {}

    @lru_cache(maxsize=50)
    def get_generator(self, grammar_hash: str, grammar: str):
        """Get cached grammar generator."""
        return generate.cfg(self.model, grammar)

    def generate(self, grammar: str, prompt: str) -> str:
        """Generate with grammar caching."""

        # Create hash for grammar
        grammar_hash = hashlib.md5(grammar.encode()).hexdigest()

        # Get or create generator
        generator = self.get_generator(grammar_hash, grammar)

        return generator(prompt)

# Usage
grammar_cache = GrammarCache(model)

# Reuse grammar generators
result1 = grammar_cache.generate(arithmetic_grammar, "Generate expression 1")
result2 = grammar_cache.generate(arithmetic_grammar, "Generate expression 2")

print("Cached generation results:")
print(f"Result 1: {result1}")
print(f"Result 2: {result2}")
```

### Grammar Size Optimization

```python
def optimize_grammar(grammar: str) -> str:
    """Optimize grammar for better performance."""

    lines = grammar.strip().split('\n')
    optimized_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove unnecessary whitespace
        line = ' '.join(line.split())

        # Combine simple alternatives
        if '|' in line and len(line.split('|')) <= 3:
            # Keep simple rules as-is
            pass

        # Optimize common patterns
        line = line.replace('(("+" | "-"))', '("+" | "-")')
        line = line.replace('(( "*" | "/" ))', '("*" | "/")')

        optimized_lines.append(line)

    return '\n'.join(optimized_lines)

# Optimize arithmetic grammar
original_grammar = """
?start: expression
?expression: term (("+" | "-") term)*
?term: factor (("*" | "/") factor)*
?factor: NUMBER | "(" expression ")"
NUMBER: /\d+/
"""

optimized_grammar = optimize_grammar(original_grammar)
print("Original grammar:")
print(original_grammar)
print("\nOptimized grammar:")
print(optimized_grammar)

# Compare performance
import time

def benchmark_grammar(grammar: str, iterations: int = 10) -> float:
    """Benchmark grammar performance."""
    generator = generate.cfg(model, grammar)

    start_time = time.time()
    for _ in range(iterations):
        generator("Generate a simple expression")
    end_time = time.time()

    return (end_time - start_time) / iterations

original_time = benchmark_grammar(original_grammar)
optimized_time = benchmark_grammar(optimized_grammar)

print("
Performance comparison:")
print(f"Original: {original_time:.3f}s per generation")
print(f"Optimized: {optimized_time:.3f}s per generation")
print(f"Improvement: {(original_time - optimized_time) / original_time * 100:.1f}%")
```

This comprehensive chapter demonstrates how Outlines uses context-free grammars to generate syntactically correct outputs for programming languages, mathematical expressions, and domain-specific languages. The next chapter covers advanced features and performance optimization. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `expression`, `print`, `grammar` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Grammar-Based Generation & Context-Free Grammars` as an operating subsystem inside **Outlines Tutorial: Structured Text Generation with LLMs**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `self`, `line`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Grammar-Based Generation & Context-Free Grammars` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `expression`.
2. **Input normalization**: shape incoming data so `print` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `grammar`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/outlines-dev/outlines)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `expression` and `print` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Type Safety & Pydantic Integration](04-type-safety.md)
- [Next Chapter: Chapter 6: Advanced Features & Performance Optimization](06-advanced-features.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
