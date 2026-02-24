---
layout: default
title: "Chapter 5: Debugging & Testing"
parent: "Continue Tutorial"
nav_order: 5
---

# Chapter 5: Debugging & Testing

Welcome to the world of intelligent debugging and testing! While Continue excels at code generation, its true debugging power shines when helping you **identify bugs, write comprehensive tests, and ensure code reliability**. This chapter explores how Continue transforms debugging from a tedious process into an intelligent, guided experience.

## What Problem Does This Solve?

Debugging and testing are often:
- **Time-consuming** - Manually tracing through complex code
- **Error-prone** - Missing edge cases or incorrect assumptions
- **Tedious** - Writing repetitive test cases
- **Incomplete** - Not covering all scenarios

Continue makes debugging and testing:
- **Intelligent** - AI-powered bug detection and analysis
- **Comprehensive** - Automatic test case generation
- **Guided** - Step-by-step debugging assistance
- **Efficient** - Rapid identification of root causes

## Intelligent Bug Detection

### Static Analysis & Bug Detection

```javascript
// Continue analyzes your code and suggests potential issues

// Original code with subtle bug
function calculateDiscount(price, discountPercent) {
  if (discountPercent > 100) {
    return price; // Bug: Should return 0 or throw error
  }
  return price * (1 - discountPercent / 100);
}

// Continue suggests: "Potential bug: discount > 100% should be handled"
// Suggested fix:
function calculateDiscount(price, discountPercent) {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Discount percentage must be between 0 and 100');
  }
  return price * (1 - discountPercent / 100);
}
```

### Runtime Error Analysis

```python
# Continue helps debug runtime errors with intelligent analysis

def process_payment(amount, card_number):
    try:
        # Process payment logic
        result = payment_gateway.charge(card_number, amount)
        return result
    except Exception as e:
        # Continue suggests: "Add specific error handling for payment failures"
        logger.error(f"Payment failed: {e}")
        raise PaymentError("Payment processing failed")

# Enhanced version with Continue's suggestions:
def process_payment(amount, card_number):
    try:
        # Validate inputs
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        if not card_number or len(str(card_number)) < 13:
            raise ValueError("Invalid card number")

        # Process payment with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = payment_gateway.charge(card_number, amount)
                return result
            except PaymentGatewayError as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Payment attempt {attempt + 1} failed: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise ValidationError(str(e))
    except PaymentGatewayError as e:
        logger.error(f"Payment gateway error: {e}")
        raise PaymentError("Payment processing failed")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise PaymentError("An unexpected error occurred")
```

## Automated Test Generation

### Unit Test Generation

```python
# Continue generates comprehensive unit tests

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Continue generates comprehensive tests:
import pytest

class TestFibonacci:
    """Test cases for fibonacci function."""

    def test_base_cases(self):
        """Test the base cases of the fibonacci sequence."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_small_values(self):
        """Test small fibonacci values."""
        assert fibonacci(2) == 1
        assert fibonacci(3) == 2
        assert fibonacci(4) == 3
        assert fibonacci(5) == 5
        assert fibonacci(6) == 8

    def test_larger_values(self):
        """Test larger fibonacci values."""
        assert fibonacci(10) == 55
        assert fibonacci(15) == 610
        assert fibonacci(20) == 6765

    def test_negative_input(self):
        """Test behavior with negative input."""
        # This should cause infinite recursion - test for reasonable timeout
        with pytest.raises(RecursionError):
            fibonacci(-1)

    def test_performance(self):
        """Test that function performs reasonably for moderate inputs."""
        import time
        start = time.time()
        result = fibonacci(30)
        end = time.time()

        assert result == 832040
        assert end - start < 1.0  # Should complete in less than 1 second

    @pytest.mark.parametrize("n,expected", [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 3),
        (5, 5), (6, 8), (7, 13), (8, 21), (9, 34)
    ])
    def test_parametrized(self, n, expected):
        """Parametrized test for multiple fibonacci values."""
        assert fibonacci(n) == expected

    def test_return_type(self):
        """Test that function returns integers."""
        for i in range(10):
            assert isinstance(fibonacci(i), int)
```

### Integration Test Generation

```javascript
// Continue generates integration tests for complex workflows

class UserRegistrationFlow {
  constructor(userService, emailService, notificationService) {
    this.userService = userService;
    this.emailService = emailService;
    this.notificationService = notificationService;
  }

  async registerUser(userData) {
    const user = await this.userService.create(userData);
    await this.emailService.sendWelcomeEmail(user.email);
    await this.notificationService.notifyAdmin(user.id);
    return user;
  }
}

// Continue generates comprehensive integration tests:
const { mock, restore } = require('simple-mock');

describe('UserRegistrationFlow', () => {
  let flow;
  let userService;
  let emailService;
  let notificationService;

  beforeEach(() => {
    // Create mocks
    userService = {
      create: mock().resolveWith({ id: 1, email: 'test@example.com' })
    };
    emailService = {
      sendWelcomeEmail: mock().resolveWith(true)
    };
    notificationService = {
      notifyAdmin: mock().resolveWith(true)
    };

    flow = new UserRegistrationFlow(userService, emailService, notificationService);
  });

  afterEach(() => {
    restore();
  });

  describe('registerUser', () => {
    it('should successfully register a user and send notifications', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      const result = await flow.registerUser(userData);

      // Verify user was created
      assert(userService.create.called);
      assert(userService.create.lastCall.args[0] === userData);

      // Verify welcome email was sent
      assert(emailService.sendWelcomeEmail.called);
      assert(emailService.sendWelcomeEmail.lastCall.args[0] === userData.email);

      // Verify admin notification was sent
      assert(notificationService.notifyAdmin.called);

      // Verify correct user object returned
      assert(result.id === 1);
      assert(result.email === userData.email);
    });

    it('should handle user creation failure', async () => {
      userService.create = mock().rejectWith(new Error('Database error'));

      const userData = { name: 'Jane Doe', email: 'jane@example.com' };

      try {
        await flow.registerUser(userData);
        assert.fail('Should have thrown an error');
      } catch (error) {
        assert(error.message === 'Database error');
      }

      // Verify email and notification were not sent
      assert(!emailService.sendWelcomeEmail.called);
      assert(!notificationService.notifyAdmin.called);
    });

    it('should handle email service failure gracefully', async () => {
      emailService.sendWelcomeEmail = mock().rejectWith(new Error('SMTP error'));

      const userData = { name: 'Bob Smith', email: 'bob@example.com' };

      try {
        await flow.registerUser(userData);
        assert.fail('Should have thrown an error');
      } catch (error) {
        assert(error.message === 'SMTP error');
      }

      // Verify user was still created and admin was notified
      assert(userService.create.called);
      assert(notificationService.notifyAdmin.called);
    });

    it('should validate input data', async () => {
      const invalidData = { name: '', email: 'invalid-email' };

      try {
        await flow.registerUser(invalidData);
        assert.fail('Should have thrown validation error');
      } catch (error) {
        assert(error.message.includes('validation'));
      }

      // Verify no services were called
      assert(!userService.create.called);
      assert(!emailService.sendWelcomeEmail.called);
      assert(!notificationService.notifyAdmin.called);
    });
  });
});
```

## Interactive Debugging Assistance

### Step-by-Step Bug Analysis

```typescript
// Continue provides interactive debugging guidance

function complexCalculation(a: number, b: number, operation: string): number {
  // Continue detects potential issues:
  // "Warning: No input validation for 'operation' parameter"

  switch (operation) {
    case 'add':
      return a + b;
    case 'subtract':
      return a - b;
    case 'multiply':
      return a * b;
    case 'divide':
      if (b === 0) {
        throw new Error('Division by zero');
      }
      return a / b;
    default:
      // Continue suggests: "Handle invalid operation gracefully"
      throw new Error(`Unknown operation: ${operation}`);
  }
}

// Enhanced version with Continue's suggestions:
function complexCalculation(a: number, b: number, operation: string): number {
  // Input validation
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('Both a and b must be numbers');
  }

  if (!operation || typeof operation !== 'string') {
    throw new TypeError('Operation must be a non-empty string');
  }

  const validOperations = ['add', 'subtract', 'multiply', 'divide'];
  if (!validOperations.includes(operation)) {
    throw new Error(`Invalid operation: ${operation}. Valid operations: ${validOperations.join(', ')}`);
  }

  // Perform calculation with detailed logging for debugging
  let result: number;
  switch (operation) {
    case 'add':
      result = a + b;
      break;
    case 'subtract':
      result = a - b;
      break;
    case 'multiply':
      result = a * b;
      break;
    case 'divide':
      if (b === 0) {
        throw new Error('Division by zero is not allowed');
      }
      result = a / b;
      break;
  }

  // Log calculation for debugging purposes
  console.log(`Calculation: ${a} ${operation} ${b} = ${result}`);

  return result;
}
```

### Root Cause Analysis

```python
# Continue helps identify root causes of bugs

def process_data_file(file_path):
    """Process data from a file."""
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return process_data(data)
    except FileNotFoundError:
        # Continue suggests: "Provide more specific error information"
        raise FileNotFoundError(f"Data file not found: {file_path}")
    except PermissionError:
        # Continue suggests: "Handle permission errors explicitly"
        raise PermissionError(f"Permission denied reading file: {file_path}")
    except Exception as e:
        # Continue suggests: "Add context to unexpected errors"
        raise RuntimeError(f"Failed to process data file {file_path}: {str(e)}")

# Enhanced version with comprehensive error handling:
def process_data_file(file_path):
    """Process data from a file with comprehensive error handling."""

    # Input validation
    if not file_path or not isinstance(file_path, str):
        raise TypeError("File path must be a non-empty string")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file does not exist: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"File is not readable: {file_path}")

    try:
        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError(f"File too large: {file_size} bytes")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

            if not data.strip():
                raise ValueError("File is empty or contains only whitespace")

            return process_data(data)

    except UnicodeDecodeError:
        raise ValueError(f"File encoding error. Expected UTF-8: {file_path}")
    except MemoryError:
        raise RuntimeError(f"File too large to load into memory: {file_path}")
    except Exception as e:
        # Log detailed error information for debugging
        logger.error(f"Unexpected error processing file {file_path}: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'}")
        raise RuntimeError(f"Failed to process data file: {str(e)}")
```

## Performance Testing & Optimization

### Load Testing Generation

```typescript
// Continue generates performance tests

import { check } from 'k6';
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users over 2 minutes
    { duration: '5m', target: 100 }, // Stay at 100 users for 5 minutes
    { duration: '2m', target: 200 }, // Ramp up to 200 users over 2 minutes
    { duration: '5m', target: 200 }, // Stay at 200 users for 5 minutes
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(99)<1000'], // 99% of requests should be below 1000ms
    http_req_failed: ['rate<0.1'],     // Error rate should be below 10%
  },
};

export default function () {
  const response = http.get('https://api.example.com/users');

  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 1000ms': (r) => r.timings.duration < 1000,
    'has users array': (r) => {
      try {
        const data = JSON.parse(r.body);
        return Array.isArray(data.users);
      } catch (e) {
        return false;
      }
    },
  });
}
```

### Code Coverage Analysis

```python
# Continue helps improve test coverage

import pytest
import coverage
from my_module import Calculator

class TestCalculator:
    """Comprehensive test suite for Calculator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()

    def teardown_method(self):
        """Clean up after each test."""
        pass

    # Basic functionality tests
    def test_addition(self):
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0

    def test_subtraction(self):
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(3, 5) == -2
        assert self.calc.subtract(0, 0) == 0

    def test_multiplication(self):
        assert self.calc.multiply(2, 3) == 6
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(0, 5) == 0

    def test_division(self):
        assert self.calc.divide(6, 3) == 2
        assert self.calc.divide(5, 2) == 2.5
        assert self.calc.divide(-6, 3) == -2

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(5, 0)

    # Edge cases
    def test_large_numbers(self):
        result = self.calc.add(999999999, 999999999)
        assert result == 1999999998

    def test_floating_point_precision(self):
        result = self.calc.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10  # Account for floating point precision

    def test_string_inputs(self):
        with pytest.raises(TypeError):
            self.calc.add("2", 3)

    def test_none_inputs(self):
        with pytest.raises(TypeError):
            self.calc.add(None, 5)

    # Integration tests
    def test_complex_calculation(self):
        # Test a complex calculation involving multiple operations
        result = self.calc.add(
            self.calc.multiply(2, 3),
            self.calc.divide(10, 2)
        )
        assert result == 11  # (2*3) + (10/2) = 6 + 5 = 11

    # Performance tests
    def test_performance_under_load(self):
        import time
        start_time = time.time()

        for _ in range(1000):
            self.calc.add(1, 1)

        end_time = time.time()
        duration = end_time - start_time

        # Should complete 1000 operations in less than 1 second
        assert duration < 1.0

    # Error handling tests
    def test_invalid_operation(self):
        # Test behavior when invalid operation is requested
        with pytest.raises(ValueError):
            self.calc.perform_operation("invalid", 2, 3)

    def test_network_timeout_simulation(self):
        # Simulate network timeout scenarios
        original_timeout = self.calc.timeout
        self.calc.timeout = 0.001  # Very short timeout

        with pytest.raises(TimeoutError):
            self.calc.network_operation()

        self.calc.timeout = original_timeout
```

## Automated Testing Workflows

### Test-Driven Development Support

```typescript
// Continue helps with TDD workflows

// 1. Write failing test first
describe('PasswordValidator', () => {
  it('should validate strong passwords', () => {
    const validator = new PasswordValidator();

    expect(validator.isStrong('weak')).toBe(false);
    expect(validator.isStrong('StrongPass123!')).toBe(true);
  });
});

// 2. Continue generates implementation
class PasswordValidator {
  isStrong(password: string): boolean {
    // Continue generates implementation based on test expectations
    if (!password || password.length < 8) {
      return false;
    }

    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChars = /[!@#$%^&*]/.test(password);

    return hasUppercase && hasLowercase && hasNumbers && hasSpecialChars;
  }
}

// 3. Continue generates additional tests
describe('PasswordValidator', () => {
  let validator: PasswordValidator;

  beforeEach(() => {
    validator = new PasswordValidator();
  });

  it('should reject passwords shorter than 8 characters', () => {
    expect(validator.isStrong('Short1!')).toBe(false);
    expect(validator.isStrong('')).toBe(false);
  });

  it('should require uppercase letters', () => {
    expect(validator.isStrong('password123!')).toBe(false);
    expect(validator.isStrong('Password123!')).toBe(true);
  });

  it('should require lowercase letters', () => {
    expect(validator.isStrong('PASSWORD123!')).toBe(false);
    expect(validator.isStrong('Password123!')).toBe(true);
  });

  it('should require numbers', () => {
    expect(validator.isStrong('Password!')).toBe(false);
    expect(validator.isStrong('Password123!')).toBe(true);
  });

  it('should require special characters', () => {
    expect(validator.isStrong('Password123')).toBe(false);
    expect(validator.isStrong('Password123!')).toBe(true);
  });

  it('should handle edge cases', () => {
    expect(validator.isStrong(null)).toBe(false);
    expect(validator.isStrong(undefined)).toBe(false);
    expect(validator.isStrong(123)).toBe(false);
  });
});
```

## Debugging Best Practices

### 1. **Systematic Debugging Approach**
- Reproduce the issue consistently
- Isolate the problem area
- Use logging and breakpoints effectively
- Test fixes incrementally

### 2. **Comprehensive Test Coverage**
- Test happy path scenarios
- Test edge cases and error conditions
- Test performance under load
- Test integration between components

### 3. **Automated Testing Strategy**
- Unit tests for individual functions
- Integration tests for component interactions
- End-to-end tests for complete workflows
- Performance tests for scalability

### 4. **Continuous Testing**
- Run tests on every code change
- Monitor test results and coverage
- Fix failing tests immediately
- Review and update tests regularly

### 5. **Debugging Tools Integration**
- Use breakpoints and step-through debugging
- Leverage logging and monitoring
- Implement error tracking and alerting
- Use profiling tools for performance issues

## What's Next?

Fantastic! You've mastered Continue's debugging and testing capabilities. The ability to generate comprehensive tests and provide intelligent debugging guidance is incredibly powerful for ensuring code quality and reliability.

In [Chapter 6: Custom Models & Configuration](06-custom-models.md), we'll explore how to configure Continue with custom AI models and create personalized development environments.

Ready to customize Continue for your specific needs? Let's continue to [Chapter 6: Custom Models & Configuration](06-custom-models.md)!

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## How it Works Under the Hood

Under the hood, `Chapter 5: Debugging & Testing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `assert`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `error`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Continue Repository](https://github.com/continuedev/continue)
  Why it matters: authoritative reference on `Continue Repository` (github.com).
- [Continue Docs](https://docs.continue.dev)
  Why it matters: authoritative reference on `Continue Docs` (docs.continue.dev).
- [Continue Releases](https://github.com/continuedev/continue/releases)
  Why it matters: authoritative reference on `Continue Releases` (github.com).

Suggested trace strategy:
- search upstream code for `assert` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Documentation & Comments](04-documentation-comments.md)
- [Next Chapter: Chapter 6: Custom Models & Configuration](06-custom-models.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
