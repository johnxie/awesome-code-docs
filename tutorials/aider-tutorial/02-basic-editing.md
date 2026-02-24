---
layout: default
title: "Aider Tutorial - Chapter 2: Basic Editing Operations"
nav_order: 2
has_children: false
parent: Aider Tutorial
---

# Chapter 2: Basic Editing Operations

Welcome to **Chapter 2: Basic Editing Operations**. In this part of **Aider Tutorial: AI Pair Programming in Your Terminal**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master adding, modifying, and deleting code with AI assistance.

## Overview

This chapter focuses on the fundamental editing operations in Aider: adding new code, modifying existing code, and deleting unnecessary code. You'll learn how to craft effective prompts and use Aider's diff-based editing system.

## Understanding Aider's Editing Model

### Diff-Based Editing

Aider uses a sophisticated diff-based editing approach that shows you exactly what changes will be made before applying them:

```python
# Original code
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# Your request: "Add tax calculation to the total"

# Aider shows this diff:
def calculate_total(items, tax_rate=0.08):
    subtotal = 0
    for item in items:
        subtotal += item.price

    tax = subtotal * tax_rate
    total = subtotal + tax
    return total
```

### The SEARCH/REPLACE Pattern

Aider internally uses a SEARCH/REPLACE pattern to make precise edits:

```
<<<<<<< SEARCH
existing code here
=======
new code here
>>>>>>> REPLACE
```

## Adding New Code

### Adding Functions

```bash
# Start Aider in your project
cd my-python-project
aider

# Add a file to work with
> /add utils.py
```

**Request: Add a utility function to validate email addresses**

Aider will add:
```python
import re

def validate_email(email):
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

### Adding Classes

**Request: Add a User class with basic attributes and methods**

Aider creates:
```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.now()
        self.is_active = True

    def update_email(self, new_email):
        if validate_email(new_email):
            self.email = new_email
        else:
            raise ValueError("Invalid email format")

    def deactivate(self):
        self.is_active = False
```

### Adding Imports

**Request: Add the necessary imports for the User class**

Aider adds:
```python
from datetime import datetime
import re
```

## Modifying Existing Code

### Changing Function Signatures

```python
# Original function
def process_data(data):
    return data.upper()

# Request: "Modify process_data to accept an optional case parameter"

# Result:
def process_data(data, case='upper'):
    if case == 'upper':
        return data.upper()
    elif case == 'lower':
        return data.lower()
    elif case == 'title':
        return data.title()
    else:
        raise ValueError(f"Unsupported case: {case}")
```

### Adding Error Handling

```python
# Original code
def divide_numbers(a, b):
    return a / b

# Request: "Add error handling for division by zero"

# Result:
def divide_numbers(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except TypeError:
        raise ValueError("Both arguments must be numbers")
```

### Adding Type Hints

```python
# Original code
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# Request: "Add type hints to calculate_average"

# Result:
from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

## Deleting Code

### Removing Unused Functions

```python
# Original code with unused function
def calculate_area(radius):
    return 3.14159 * radius * radius

def calculate_circumference(radius):
    return 2 * 3.14159 * radius

def main():
    print(calculate_area(5))

# Request: "Remove the unused calculate_circumference function"

# Result:
def calculate_area(radius):
    return 3.14159 * radius * radius

def main():
    print(calculate_area(5))
```

### Simplifying Complex Expressions

```python
# Original complex code
def is_valid_user(user):
    if user is not None:
        if user.age >= 18:
            if user.email is not None:
                if '@' in user.email:
                    return True
    return False

# Request: "Simplify the is_valid_user function"

# Result:
def is_valid_user(user):
    return (user is not None and
            user.age >= 18 and
            user.email is not None and
            '@' in user.email)
```

## Working with Multiple Changes

### Sequential Modifications

```bash
# Start with a simple function
> /add calculator.py

# First change
> Add a function to add two numbers

# Second change (builds on first)
> Add a function to multiply two numbers

# Third change (modifies existing)
> Add input validation to both functions
```

### Reviewing Changes

```bash
# See what Aider plans to change
> /diff

# Accept all changes
> (just press Enter or type 'y')

# Or reject and refine
> That's not quite right. Make the validation raise ValueError instead of returning None
```

## Advanced Editing Patterns

### Refactoring Code

```python
# Original tightly coupled code
class DataProcessor:
    def process(self, data):
        # Validate
        if not data:
            return None

        # Transform
        result = []
        for item in data:
            result.append(item.upper())

        # Save to database
        self.save_to_db(result)

        return result

# Request: "Refactor to separate concerns into smaller methods"

# Result:
class DataProcessor:
    def process(self, data):
        validated_data = self._validate_data(data)
        if validated_data is None:
            return None

        transformed_data = self._transform_data(validated_data)
        self._save_to_database(transformed_data)

        return transformed_data

    def _validate_data(self, data):
        if not data:
            return None
        return data

    def _transform_data(self, data):
        return [item.upper() for item in data]

    def _save_to_database(self, data):
        # Database saving logic here
        pass
```

### Adding Documentation

```python
# Original undocumented function
def complex_calculation(a, b, c):
    if c == 0:
        return a + b
    else:
        return (a * b) / c

# Request: "Add comprehensive docstring and inline comments"

# Result:
def complex_calculation(a, b, c):
    """
    Perform a complex calculation with conditional logic.

    Args:
        a (float): First operand
        b (float): Second operand
        c (float): Divisor (when non-zero)

    Returns:
        float: Result of calculation

    Raises:
        ZeroDivisionError: If c is zero in division case

    Examples:
        >>> complex_calculation(2, 3, 0)
        5.0
        >>> complex_calculation(2, 3, 2)
        3.0
    """
    # Handle case where c is zero (addition)
    if c == 0:
        return a + b
    else:
        # Handle case where c is non-zero (multiplication then division)
        return (a * b) / c
```

### Code Style Improvements

```python
# Original poorly styled code
def fn(x,y,z):
    result=[]
    for i in range(len(x)):
        if x[i]>0:
            result.append(x[i]*y[i]+z)
    return result

# Request: "Improve code style and readability"

# Result:
def calculate_weighted_sum(positive_values, weights, offset):
    """
    Calculate weighted sum for positive values with an offset.

    Args:
        positive_values: List of numeric values
        weights: Corresponding weights for each value
        offset: Value to add to each result

    Returns:
        List of calculated values for positive inputs only
    """
    results = []

    for value, weight in zip(positive_values, weights):
        if value > 0:
            weighted_value = value * weight + offset
            results.append(weighted_value)

    return results
```

## Error Handling and Recovery

### Fixing Syntax Errors

```python
# Code with syntax error
def broken_function(
    print("This is broken")

# Request: "Fix the syntax error"

# Result:
def broken_function():
    print("This is fixed")
```

### Handling Logic Errors

```python
# Code with logic error
def find_max(numbers):
    max_val = 0  # Bug: should be None or numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

# Request: "Fix the bug in find_max function"

# Result:
def find_max(numbers):
    if not numbers:
        raise ValueError("Cannot find max of empty list")

    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

## Working with Different File Types

### Python Files

```python
# Adding to existing Python file
> /add models.py

# Request: "Add a Product model class with price validation"

# Result:
from decimal import Decimal
from typing import Optional

class Product:
    def __init__(self, name: str, price: Decimal):
        self.name = name
        self.price = self._validate_price(price)
        self.created_at = datetime.now()

    def _validate_price(self, price: Decimal) -> Decimal:
        if price <= 0:
            raise ValueError("Price must be positive")
        return price

    def apply_discount(self, percentage: Decimal) -> None:
        discount = self.price * (percentage / 100)
        self.price -= discount
```

### JavaScript/Node.js Files

```javascript
// Adding to existing JS file
> /add server.js

// Request: "Add Express route for user registration"

// Result:
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

const router = express.Router();

// User registration route
router.post('/register', async (req, res) => {
    try {
        const { username, email, password } = req.body;

        // Validate input
        if (!username || !email || !password) {
            return res.status(400).json({
                error: 'Username, email, and password are required'
            });
        }

        // Hash password
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        // TODO: Save user to database

        // Generate JWT token
        const token = jwt.sign(
            { userId: 'user-id', username },
            process.env.JWT_SECRET,
            { expiresIn: '24h' }
        );

        res.status(201).json({
            message: 'User registered successfully',
            token
        });

    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({
            error: 'Internal server error'
        });
    }
});

module.exports = router;
```

### Configuration Files

```yaml
# Adding to YAML config
> /add config.yaml

# Request: "Add database configuration section"

# Result:
database:
  host: localhost
  port: 5432
  name: myapp
  username: ${DB_USER}
  password: ${DB_PASSWORD}
  ssl_mode: require
  connection_pool:
    min_connections: 2
    max_connections: 10
    connection_timeout: 30s

redis:
  host: localhost
  port: 6379
  password: ${REDIS_PASSWORD}
  db: 0
  connection_timeout: 5s

logging:
  level: info
  format: json
  outputs:
    - stdout
    - file: /var/log/app.log
```

## Best Practices for Basic Editing

### Be Specific in Your Requests

```bash
# ❌ Vague
> Add error handling

# ✅ Specific
> Add try-catch blocks to the database connection methods that raise ConnectionError on failure
```

### Provide Context

```bash
# ❌ No context
> Add validation

# ✅ With context
> Add input validation to the user registration function that checks email format and password strength
```

### Review Before Accepting

```bash
# Always check the diff
> /diff

# Ask for clarification if needed
> Can you show me what the validate_email function will look like?

# Request modifications
> Use a more restrictive email regex pattern
```

### Build Incrementally

```bash
# Start simple
> Add a basic user model

# Then enhance
> Add password hashing to the user model

# Then extend
> Add relationship to orders in the user model
```

## Summary

In this chapter, we've covered:

- **Adding Code**: Functions, classes, imports, and documentation
- **Modifying Code**: Function signatures, error handling, type hints
- **Deleting Code**: Removing unused functions and simplifying expressions
- **Multiple Changes**: Sequential modifications and change review
- **Advanced Patterns**: Refactoring, documentation, and style improvements
- **Error Recovery**: Fixing syntax and logic errors
- **File Types**: Working with Python, JavaScript, and configuration files

## Key Takeaways

1. **Review Changes**: Always use `/diff` before accepting modifications
2. **Be Specific**: Clear, detailed prompts produce better results
3. **Build Incrementally**: Make small changes and iterate
4. **Context Matters**: Provide sufficient context for complex changes
5. **Error Handling**: Aider can fix both syntax and logic errors
6. **Multi-language**: Works with various programming languages and formats

## Next Steps

Now that you understand basic editing operations, let's explore **multi-file projects** and how to work across multiple files effectively.

---

**Ready for Chapter 3?** [Multi-File Projects](03-multi-file.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `email`, `numbers` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Basic Editing Operations` as an operating subsystem inside **Aider Tutorial: AI Pair Programming in Your Terminal**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `user`, `Request`, `Result` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Basic Editing Operations` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `email` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `numbers`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Aider Repository](https://github.com/Aider-AI/aider)
  Why it matters: authoritative reference on `Aider Repository` (github.com).
- [Aider Releases](https://github.com/Aider-AI/aider/releases)
  Why it matters: authoritative reference on `Aider Releases` (github.com).
- [Aider Docs](https://aider.chat/)
  Why it matters: authoritative reference on `Aider Docs` (aider.chat).

Suggested trace strategy:
- search upstream code for `self` and `email` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Aider](01-getting-started.md)
- [Next Chapter: Chapter 3: Multi-File Projects](03-multi-file.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
