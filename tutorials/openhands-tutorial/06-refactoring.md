---
layout: default
title: "OpenHands Tutorial - Chapter 6: Refactoring"
nav_order: 6
has_children: false
parent: OpenHands Tutorial
---

# Chapter 6: Refactoring - Code Structure Improvement and Modernization

Welcome to **Chapter 6: Refactoring - Code Structure Improvement and Modernization**. In this part of **OpenHands Tutorial: Autonomous Software Engineering Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master OpenHands' refactoring capabilities for improving code structure, performance, and maintainability through systematic code transformations.

## Overview

OpenHands provides sophisticated refactoring capabilities, from simple code improvements to complex architectural transformations. This chapter covers automated code refactoring, modernization, and optimization techniques.

## Code Structure Refactoring

### Function and Method Refactoring

```python
from openhands import OpenHands

# Refactoring agent
refactor_agent = OpenHands()

# Complex function refactoring
function_refactor = refactor_agent.run("""
Refactor this complex function into smaller, focused functions:

```python
def process_user_orders(user_id, orders_data, payment_info, shipping_address):
    # Validate user exists
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User {user_id} not found")
    
    # Process each order
    processed_orders = []
    total_amount = 0
    
    for order_data in orders_data:
        # Validate order data
        if not validate_order_data(order_data):
            continue
        
        # Calculate order total
        order_total = calculate_order_total(order_data['items'])
        total_amount += order_total
        
        # Create order record
        order = create_order_record(
            user_id=user_id,
            items=order_data['items'],
            total=order_total,
            shipping_address=shipping_address
        )
        
        processed_orders.append(order)
    
    # Process payment
    if total_amount > 0:
        payment_result = process_payment(
            payment_info=payment_info,
            amount=total_amount,
            orders=processed_orders
        )
        
        if not payment_result['success']:
            # Rollback orders
            rollback_orders(processed_orders)
            raise PaymentError("Payment processing failed")
    
    return {
        'processed_orders': processed_orders,
        'total_amount': total_amount,
        'payment_status': payment_result
    }
```

Refactor into:
1. Input validation functions
2. Order processing pipeline
3. Payment handling abstraction
4. Error handling and rollback mechanisms
5. Result aggregation and reporting

Include proper error handling, logging, and type hints.
""")

# Class refactoring
class_refactor = refactor_agent.run("""
Refactor this large class into smaller, focused classes:

```python
class UserManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache = {}
        self.logger = logging.getLogger(__name__)
    
    def create_user(self, user_data):
        # Validate input
        self._validate_user_data(user_data)
        
        # Check if user exists
        if self._user_exists(user_data['email']):
            raise ValueError("User already exists")
        
        # Hash password
        user_data['password_hash'] = self._hash_password(user_data['password'])
        
        # Save to database
        user_id = self.db.insert('users', user_data)
        
        # Send welcome email
        self._send_welcome_email(user_data['email'])
        
        # Cache user
        self.cache[user_id] = user_data
        
        return user_id
    
    def authenticate_user(self, email, password):
        # Get user from cache or DB
        user = self.cache.get(email) or self.db.query('users', {'email': email})
        
        if not user:
            return None
        
        # Verify password
        if self._verify_password(password, user['password_hash']):
            return user
        
        return None
    
    def update_user_profile(self, user_id, updates):
        # Validate updates
        self._validate_updates(updates)
        
        # Update in database
        self.db.update('users', user_id, updates)
        
        # Update cache
        if user_id in self.cache:
            self.cache[user_id].update(updates)
        
        # Log update
        self.logger.info(f"Updated user {user_id}")
    
    def delete_user(self, user_id):
        # Remove from cache
        self.cache.pop(user_id, None)
        
        # Remove from database
        self.db.delete('users', user_id)
        
        # Log deletion
        self.logger.info(f"Deleted user {user_id}")
    
    # Private helper methods
    def _validate_user_data(self, data):
        # Validation logic...
        pass
    
    def _user_exists(self, email):
        # Check existence...
        pass
    
    def _hash_password(self, password):
        # Hashing logic...
        pass
    
    def _verify_password(self, password, hash):
        # Verification logic...
        pass
    
    def _validate_updates(self, updates):
        # Validation logic...
        pass
    
    def _send_welcome_email(self, email):
        # Email logic...
        pass
```

Split into focused classes:
1. UserValidator - Input validation
2. UserRepository - Data access
3. AuthenticationService - Auth logic
4. EmailService - Notifications
5. CacheManager - Caching logic
6. UserManager - Orchestration
""")
```

## Architectural Refactoring

### Monolithic to Microservices

```python
# Architecture refactoring agent
architecture_agent = OpenHands()

# Monolithic to microservices refactoring
microservices_refactor = architecture_agent.run("""
Refactor this monolithic e-commerce application into microservices:

Current Monolithic Structure:
```python
class EcommerceApp:
    def __init__(self):
        self.users = UserManager()
        self.products = ProductManager()
        self.orders = OrderManager()
        self.payments = PaymentManager()
        self.inventory = InventoryManager()
        self.notifications = NotificationManager()
    
    def place_order(self, user_id, items):
        # Validate user
        user = self.users.get(user_id)
        
        # Check inventory
        for item in items:
            if not self.inventory.check_stock(item['id'], item['quantity']):
                raise OutOfStockError(f"Item {item['id']} out of stock")
        
        # Create order
        order = self.orders.create(user_id, items)
        
        # Process payment
        payment = self.payments.process(order.total)
        
        if payment.success:
            # Update inventory
            self.inventory.update_stock(items)
            
            # Send confirmation
            self.notifications.send_order_confirmation(user.email, order)
            
            return order
        else:
            # Cancel order
            self.orders.cancel(order.id)
            raise PaymentError("Payment failed")
```

Refactor into microservices:
1. **User Service** - User management and authentication
2. **Product Service** - Product catalog and information
3. **Order Service** - Order creation and management
4. **Payment Service** - Payment processing
5. **Inventory Service** - Stock management
6. **Notification Service** - Email and messaging

Include:
- Service boundaries and APIs
- Inter-service communication (REST/gRPC)
- Event-driven architecture
- Saga pattern for distributed transactions
- API Gateway design
- Service discovery and registration
""")

# Database refactoring
database_refactor = architecture_agent.run("""
Refactor database design from monolithic to microservices:

Current Monolithic Schema:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    created_at TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    category_id INT,
    stock_quantity INT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    total DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT,
    price DECIMAL(10,2)
);
```

Refactor for microservices:
1. **User Service Database** - User data only
2. **Product Service Database** - Product catalog
3. **Order Service Database** - Orders and items
4. **Payment Service Database** - Payment records
5. **Inventory Service Database** - Stock levels

Include:
- Database per service pattern
- Event sourcing for data consistency
- CQRS pattern implementation
- Data migration strategies
- API composition for complex queries
""")
```

## Performance Optimization Refactoring

### Algorithm and Data Structure Optimization

```python
# Performance optimization agent
perf_optimizer = OpenHands()

# Algorithm optimization
algorithm_refactor = perf_optimizer.run("""
Optimize these inefficient algorithms:

**Inefficient Search Algorithm:**
```python
def find_user_by_email(users_list, email):
    # O(n) linear search - inefficient for large lists
    for user in users_list:
        if user['email'] == email:
            return user
    return None
```

**Memory-Inefficient Data Processing:**
```python
def process_large_file(file_path):
    # Loads entire file into memory
    with open(file_path, 'r') as f:
        content = f.read()  # Memory intensive
    
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        # Creates new list for each processed line
        processed_lines.append(process_line(line))  # Memory inefficient
    
    return processed_lines
```

**Recursive Function with Deep Stack:**
```python
def fibonacci_recursive(n):
    if n <= 1:
        return n
    # Deep recursion can cause stack overflow
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)
```

Optimize to:
1. Use appropriate data structures (hash tables, trees, etc.)
2. Implement efficient algorithms (binary search, dynamic programming)
3. Use streaming processing for large data
4. Implement iterative solutions to avoid stack overflow
5. Add caching and memoization
6. Use concurrent/parallel processing where appropriate
""")

# Memory and resource optimization
memory_refactor = perf_optimizer.run("""
Refactor for memory and resource efficiency:

**Memory Leak in Cache:**
```python
class SimpleCache:
    def __init__(self):
        self.cache = {}
    
    def set(self, key, value):
        self.cache[key] = value  # No size limits or expiration
    
    def get(self, key):
        return self.cache.get(key)
```

**Inefficient String Concatenation:**
```python
def build_html_table(rows):
    html = "<table>"
    for row in rows:
        html += "<tr>"  # Creates new string each iteration
        for cell in row:
            html += f"<td>{cell}</td>"  # Memory inefficient
        html += "</tr>"
    html += "</table>"
    return html
```

**Resource-Intensive File Processing:**
```python
def count_words_in_files(file_paths):
    word_counts = {}
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            content = f.read()  # Loads entire file
            words = content.split()
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
    return word_counts
```

Refactor with:
1. LRU cache with size limits and TTL
2. StringBuilder pattern or join operations
3. Streaming file processing with generators
4. Memory-mapped files for large data
5. Connection pooling for database access
6. Lazy loading and pagination
""")
```

## Code Modernization

### Language Feature Adoption

```python
# Code modernization agent
modernizer = OpenHands()

# Python modernization
python_modernize = modernizer.run("""
Modernize this legacy Python code to use contemporary features:

**Legacy Code to Modernize:**
```python
# Python 2 style
def process_data(data_list):
    result = []
    for item in data_list:
        if item is not None:
            # Old-style formatting
            formatted = "Item: %s, Value: %d" % (item['name'], item['value'])
            result.append(formatted)
    return result

# Old-style class
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def filter_data(self, condition):
        # List comprehension could be more efficient
        filtered = []
        for item in self.data:
            if condition(item):
                filtered.append(item)
        return filtered

# Exception handling without context managers
def read_config(file_path):
    file_handle = open(file_path, 'r')
    try:
        config = {}
        for line in file_handle:
            key, value = line.strip().split('=')
            config[key] = value
        return config
    finally:
        file_handle.close()
```

Modernize to use:
1. **f-strings** instead of % formatting and .format()
2. **Type hints** for better code documentation
3. **Dataclasses** for simple data structures
4. **Context managers** with `with` statements
5. **Generator expressions** for memory efficiency
6. **Modern exception handling** with `raise from`
7. **Pathlib** for file path operations
8. **Enum** for constants
9. **functools.lru_cache** for memoization
10. **asyncio** for concurrent operations
""")

# JavaScript/Node.js modernization
js_modernize = modernizer.run("""
Modernize legacy JavaScript code to ES6+ features:

**Legacy Code:**
```javascript
// ES5 style
var UserManager = function() {
    this.users = [];
};

UserManager.prototype.addUser = function(user) {
    // Callback-based async
    fs.readFile('users.json', 'utf8', function(err, data) {
        if (err) throw err;
        
        var users = JSON.parse(data);
        users.push(user);
        
        fs.writeFile('users.json', JSON.stringify(users), function(err) {
            if (err) throw err;
            console.log('User added');
        });
    });
};

// Old-style promise handling
function fetchUser(userId) {
    return new Promise(function(resolve, reject) {
        http.get('/api/users/' + userId, function(res) {
            var data = '';
            res.on('data', function(chunk) {
                data += chunk;
            });
            res.on('end', function() {
                resolve(JSON.parse(data));
            });
        }).on('error', reject);
    });
}
```

Modernize to:
1. **ES6 classes** instead of prototype functions
2. **Arrow functions** for concise syntax
3. **Async/await** instead of callbacks and promises
4. **Template literals** for string interpolation
5. **Destructuring** for object/array manipulation
6. **Modules** with import/export
7. **Optional chaining** and nullish coalescing
8. **Map/Set** for collections
9. **Object spread/rest** operators
10. **Promises with async/await** patterns
""")
```

## Security Refactoring

### Security Vulnerability Fixes

```python
# Security refactoring agent
security_refactor = OpenHands()

# SQL injection and security fixes
security_fixes = security_refactor.run("""
Fix security vulnerabilities in this code:

**SQL Injection Vulnerable:**
```python
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABLE: Direct string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()
```

**Command Injection:**
```python
import subprocess

def run_command(user_input):
    # VULNERABLE: Direct command execution
    subprocess.call(f"ls -la {user_input}", shell=True)
```

**Insecure Password Storage:**
```python
def create_user(username, password):
    # VULNERABLE: Plain text password storage
    with open('users.txt', 'a') as f:
        f.write(f"{username}:{password}\n")
```

**XSS Vulnerability:**
```javascript
app.get('/user/:id', function(req, res) {
    // VULNERABLE: Direct HTML injection
    var userId = req.params.id;
    res.send('<h1>User: ' + userId + '</h1>');
});
```

**Insecure Random Generation:**
```python
import random

def generate_token():
    # VULNERABLE: Predictable random
    return str(random.randint(100000, 999999))
```

Fix with:
1. **Parameterized queries** for SQL
2. **Input validation and sanitization**
3. **Password hashing** with bcrypt/scrypt
4. **HTML escaping** and Content Security Policy
5. **Cryptographically secure random** generation
6. **Input validation** and whitelisting
7. **Secure headers** and CORS configuration
8. **Rate limiting** and abuse prevention
""")

# Authentication and authorization refactoring
auth_refactor = security_refactor.run("""
Refactor authentication and authorization:

**Weak Authentication:**
```python
def authenticate(username, password):
    users = load_users_from_file()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None
```

**Missing Authorization:**
```python
@app.route('/admin/users')
def admin_users():
    # No authorization check
    return get_all_users()
```

**Insecure Session Management:**
```python
# Client-side session storage
localStorage.setItem('session_token', token);

// Server-side session without expiration
sessions = {}
def create_session(user_id):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {'user_id': user_id}
    return session_id
```

Refactor to:
1. **Secure password hashing** with salt
2. **JWT tokens** with proper expiration
3. **Role-based access control** (RBAC)
4. **Session management** with secure cookies
5. **Multi-factor authentication**
6. **OAuth 2.0** integration
7. **API key authentication**
8. **Audit logging** for security events
""")
```

## Testing Integration in Refactoring

### Refactoring with Test Coverage

```python
# Refactoring with testing agent
test_refactor = OpenHands()

# Refactoring with test coverage
refactor_with_tests = test_refactor.run("""
Refactor this code while maintaining and improving test coverage:

**Original Code:**
```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0
    
    def add_item(self, item, price, quantity=1):
        self.items.append({
            'item': item,
            'price': price,
            'quantity': quantity
        })
        self.total += price * quantity
    
    def remove_item(self, item_name):
        for i, item in enumerate(self.items):
            if item['item'] == item_name:
                self.total -= item['price'] * item['quantity']
                del self.items[i]
                return True
        return False
    
    def get_total(self):
        return self.total
```

**Existing Tests:**
```python
def test_shopping_cart():
    cart = ShoppingCart()
    
    # Test adding items
    cart.add_item("Apple", 1.50, 2)
    assert cart.get_total() == 3.00
    
    # Test removing items
    cart.remove_item("Apple")
    assert cart.get_total() == 0.00
```

Refactor to improve:
1. **Type safety** with dataclasses and type hints
2. **Error handling** for invalid inputs
3. **Discount system** for flexible pricing
4. **Inventory integration** for stock checking
5. **Persistence layer** for saving carts
6. **Thread safety** for concurrent access

Ensure all existing tests pass and add comprehensive new tests for new features.
""")

# Legacy code modernization with tests
legacy_modernize = test_refactor.run("""
Modernize legacy code while preserving functionality through comprehensive testing:

**Legacy Code:**
```python
# Python 2 style code
def process_orders(orders):
    results = []
    for order in orders:
        if validate_order(order):
            total = calculate_total(order['items'])
            if total > 0:
                results.append({
                    'order_id': order['id'],
                    'total': total,
                    'status': 'processed'
                })
            else:
                results.append({
                    'order_id': order['id'],
                    'error': 'Invalid total'
                })
        else:
            results.append({
                'order_id': order['id'],
                'error': 'Invalid order'
            })
    return results
```

Modernize to:
1. **Type hints** and modern Python syntax
2. **Exception handling** instead of error dictionaries
3. **Generator functions** for memory efficiency
4. **Dataclasses** for data structures
5. **Async/await** for I/O operations
6. **Logging** for debugging and monitoring

Create comprehensive test suite that validates both old and new behavior, then perform the refactoring safely.
""")
```

## Automated Refactoring Tools

### Code Analysis and Suggestions

```python
# Automated refactoring tools
auto_refactor = OpenHands()

# Code analysis and automated refactoring
code_analysis = auto_refactor.run("""
Create automated code analysis and refactoring tools:

1. **Code Smell Detection**
   - Long methods (>50 lines)
   - Large classes (>300 lines)
   - High cyclomatic complexity
   - Duplicate code blocks
   - Unused variables and imports
   - Missing documentation

2. **Automated Refactoring Suggestions**
   - Extract method refactoring
   - Inline method refactoring
   - Move method/field refactoring
   - Rename refactoring
   - Change signature refactoring
   - Encapsulate field refactoring

3. **Safety Analysis**
   - Impact analysis for refactoring
   - Test coverage verification
   - Dependency analysis
   - Breaking change detection

4. **Batch Refactoring**
   - Apply refactoring across multiple files
   - Preview changes before applying
   - Rollback capability
   - Progress tracking and reporting

Include integration with popular IDEs and command-line tools.
""")

# IDE integration for refactoring
ide_integration = auto_refactor.run("""
Create IDE integration for refactoring tools:

1. **Visual Studio Code Extension**
   - Refactoring commands in command palette
   - Quick fixes for detected issues
   - Refactoring preview with diff view
   - Multi-file refactoring support

2. **PyCharm Plugin**
   - Intention actions for refactoring
   - Refactoring templates and presets
   - Code inspection integration
   - Test generation for refactored code

3. **Language Server Protocol**
   - LSP server for refactoring capabilities
   - Support for multiple editors
   - Standardized refactoring interface
   - Extensible refactoring providers

4. **Command-Line Tools**
   - CLI interface for batch refactoring
   - Configuration file support
   - CI/CD pipeline integration
   - Automated refactoring workflows

Include documentation, examples, and best practices for each integration.
""")
```

## Summary

In this chapter, we've covered OpenHands' comprehensive refactoring capabilities:

- **Code Structure Refactoring**: Function/method splitting, class decomposition
- **Architectural Refactoring**: Monolithic to microservices, database design
- **Performance Optimization**: Algorithm improvement, memory/resource efficiency
- **Code Modernization**: Language feature adoption, legacy code updates
- **Security Refactoring**: Vulnerability fixes, authentication improvements
- **Testing Integration**: Refactoring with test coverage maintenance
- **Automated Tools**: Code analysis, IDE integration, batch refactoring

OpenHands can systematically improve codebases while maintaining functionality and adding comprehensive testing.

## Key Takeaways

1. **Systematic Approach**: Follow structured refactoring methodologies
2. **Safety First**: Maintain test coverage and functionality during changes
3. **Modern Standards**: Adopt contemporary language features and patterns
4. **Performance Focus**: Optimize algorithms, memory usage, and resource consumption
5. **Security Priority**: Address vulnerabilities and implement security best practices
6. **Tool Integration**: Leverage automated tools and IDE integrations

Next, we'll explore **integration** - OpenHands' ability to connect applications with external APIs, databases, and services.

---

**Ready for the next chapter?** [Chapter 7: Integration](07-integration.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `refactoring`, `Refactor`, `Service` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Refactoring - Code Structure Improvement and Modernization` as an operating subsystem inside **OpenHands Tutorial: Autonomous Software Engineering Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `code`, `Code`, `OpenHands` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Refactoring - Code Structure Improvement and Modernization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `refactoring`.
2. **Input normalization**: shape incoming data so `Refactor` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Service`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [OpenHands Repository](https://github.com/OpenHands/OpenHands)
  Why it matters: authoritative reference on `OpenHands Repository` (github.com).
- [OpenHands Docs](https://docs.openhands.dev/)
  Why it matters: authoritative reference on `OpenHands Docs` (docs.openhands.dev).
- [OpenHands Releases](https://github.com/OpenHands/OpenHands/releases)
  Why it matters: authoritative reference on `OpenHands Releases` (github.com).

Suggested trace strategy:
- search upstream code for `refactoring` and `Refactor` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Testing - Comprehensive Test Suite Generation and Quality Assurance](05-testing.md)
- [Next Chapter: Chapter 7: Integration - Connecting Applications with External Services](07-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
