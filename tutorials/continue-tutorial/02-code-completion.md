---
layout: default
title: "Chapter 2: Code Completion & Generation"
parent: "Continue Tutorial"
nav_order: 2
---

# Chapter 2: Code Completion & Generation

Welcome to **Chapter 2: Code Completion & Generation**. In this part of **Continue Tutorial: Open-Source AI Coding Agents for IDE and CLI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Now that you have Continue installed and configured, let's explore its most powerful feature: **intelligent code completion and generation**. This is where Continue truly shines - providing context-aware suggestions that understand your codebase, coding patterns, and intent.

## What Makes Continue's Completion Special?

Unlike basic autocomplete tools, Continue's completion system:
- **Understands Context** - Analyzes your entire codebase for relevant patterns
- **Learns Your Style** - Adapts to your coding preferences and conventions
- **Provides Multi-Line Suggestions** - Generates complete functions, classes, and logic blocks
- **Handles Complex Logic** - Manages error handling, edge cases, and best practices
- **Supports Multiple Languages** - Works across Python, JavaScript, TypeScript, Go, and more

## Understanding Completion Triggers

### Automatic Triggers

```python
# Continue automatically suggests completions when you:
# 1. Start typing a function name
def calculate_
#    ↑ Cursor here triggers suggestions

# 2. Begin a class definition
class User
#    ↑ Suggests complete class structure

# 3. Start a conditional statement
if user and user.
#    ↑ Suggests property access with null checking

# 4. Begin an API call
fetch('/api/users')
#    ↑ Suggests complete async/await pattern
```

### Manual Triggers

```javascript
// Press Tab to accept suggestions
// Press Cmd/Ctrl + Shift + L to open chat interface
// Use "/" commands for specific actions:
// /comment - Add documentation
// /fix - Fix errors in selected code
// /test - Generate tests
// /refactor - Suggest refactoring options
```

## Advanced Code Completion Patterns

### Function Generation

```python
# Type: def process_user_data(user_data, db_connection):
# Continue suggests complete implementation:

def process_user_data(user_data, db_connection):
    """
    Process user data and store in database with validation.

    Args:
        user_data (dict): User information to process
        db_connection: Database connection object

    Returns:
        dict: Processing results with success status

    Raises:
        ValueError: If user_data is invalid
        DatabaseError: If database operation fails
    """
    try:
        # Validate input data
        if not user_data or not isinstance(user_data, dict):
            raise ValueError("Invalid user data provided")

        required_fields = ['name', 'email', 'age']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")

        # Process user data
        processed_data = {
            'name': user_data['name'].strip().title(),
            'email': user_data['email'].lower().strip(),
            'age': int(user_data['age']),
            'processed_at': datetime.now().isoformat(),
            'status': 'active'
        }

        # Store in database
        with db_connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (name, email, age, processed_at, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                processed_data['name'],
                processed_data['email'],
                processed_data['age'],
                processed_data['processed_at'],
                processed_data['status']
            ))

            user_id = cursor.fetchone()[0]
            db_connection.commit()

        return {
            'success': True,
            'user_id': user_id,
            'message': 'User data processed successfully'
        }

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'error_type': 'validation'
        }

    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db_connection.rollback()
        return {
            'success': False,
            'error': 'Failed to process user data',
            'error_type': 'database'
        }
```

### Class Generation

```typescript
// Type: class ApiService {
// Continue suggests complete service class:

class ApiService {
  private baseUrl: string;
  private timeout: number;
  private retryAttempts: number;

  constructor(baseUrl: string = '/api', timeout: number = 5000) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
    this.retryAttempts = 3;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new Error('Request timeout');
      }

      throw error;
    }
  }

  async getUsers(params?: { limit?: number; offset?: number }): Promise<User[]> {
    const queryParams = params ?
      `?${new URLSearchParams(params as any)}` : '';
    return this.makeRequest<User[]>(`/users${queryParams}`);
  }

  async getUserById(id: number): Promise<User> {
    return this.makeRequest<User>(`/users/${id}`);
  }

  async createUser(userData: Omit<User, 'id'>): Promise<User> {
    return this.makeRequest<User>('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(id: number, userData: Partial<User>): Promise<User> {
    return this.makeRequest<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(id: number): Promise<void> {
    await this.makeRequest(`/users/${id}`, {
      method: 'DELETE',
    });
  }

  async getUserPosts(userId: number): Promise<Post[]> {
    return this.makeRequest<Post[]>(`/users/${userId}/posts`);
  }

  async getUserComments(userId: number): Promise<Comment[]> {
    return this.makeRequest<Comment[]>(`/users/${userId}/comments`);
  }
}

// Type definitions
interface User {
  id: number;
  name: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

interface Post {
  id: number;
  title: string;
  content: string;
  userId: number;
  createdAt: string;
}

interface Comment {
  id: number;
  content: string;
  userId: number;
  postId: number;
  createdAt: string;
}
```

### React Component Generation

```jsx
// Type: function UserDashboard({ userId }) {
// Continue suggests complete React component:

import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService } from '../services/apiService';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { UserProfile } from '../components/UserProfile';
import { UserStats } from '../components/UserStats';
import { RecentActivity } from '../components/RecentActivity';

function UserDashboard({ userId: propUserId }) {
  const { id: paramUserId } = useParams();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Use prop userId or URL parameter
  const currentUserId = propUserId || paramUserId;

  const fetchUserData = useCallback(async () => {
    if (!currentUserId) return;

    try {
      setLoading(true);
      setError(null);

      // Fetch user data, stats, and activity in parallel
      const [userData, userStats, userActivity] = await Promise.all([
        apiService.getUserById(currentUserId),
        apiService.getUserStats(currentUserId),
        apiService.getUserActivity(currentUserId)
      ]);

      setUser(userData);
      setStats(userStats);
      setActivity(userActivity);
    } catch (err) {
      setError(err.message || 'Failed to load user data');
      console.error('Error fetching user data:', err);
    } finally {
      setLoading(false);
    }
  }, [currentUserId]);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  const handleRefresh = () => {
    fetchUserData();
  };

  const handleEditProfile = () => {
    navigate(`/users/${currentUserId}/edit`);
  };

  const handleViewPosts = () => {
    navigate(`/users/${currentUserId}/posts`);
  };

  if (loading) {
    return <LoadingSpinner message="Loading user dashboard..." />;
  }

  if (error) {
    return (
      <ErrorMessage
        message={error}
        onRetry={handleRefresh}
        retryLabel="Try Again"
      />
    );
  }

  if (!user) {
    return (
      <ErrorMessage
        message="User not found"
        onRetry={() => navigate('/users')}
        retryLabel="Back to Users"
      />
    );
  }

  return (
    <div className="user-dashboard">
      <div className="dashboard-header">
        <h1>User Dashboard</h1>
        <div className="dashboard-actions">
          <button
            onClick={handleRefresh}
            className="btn-secondary"
            disabled={loading}
          >
            Refresh
          </button>
          <button
            onClick={handleEditProfile}
            className="btn-primary"
          >
            Edit Profile
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-main">
          <UserProfile user={user} onEdit={handleEditProfile} />
        </div>

        <div className="dashboard-sidebar">
          <UserStats stats={stats} />
          <RecentActivity
            activities={activity}
            onViewAll={handleViewPosts}
          />
        </div>
      </div>
    </div>
  );
}

UserDashboard.propTypes = {
  userId: PropTypes.string
};

export default UserDashboard;
```

## Context-Aware Generation

### Understanding Code Context

Continue analyzes multiple types of context to provide better suggestions:

```javascript
// File Context - Current file content and structure
const fileContext = {
  language: 'javascript',
  framework: 'react',
  imports: ['react', 'useState', 'useEffect'],
  existingFunctions: ['handleSubmit', 'validateForm'],
  codingStyle: 'camelCase',
  indentation: 'spaces'
};

// Project Context - Project-wide patterns
const projectContext = {
  dependencies: ['react', 'axios', 'lodash'],
  fileStructure: 'feature-based',
  stateManagement: 'redux',
  testingFramework: 'jest',
  codeStyle: 'airbnb'
};

// Git Context - Recent changes and patterns
const gitContext = {
  recentCommits: ['feat: add user authentication'],
  modifiedFiles: ['src/auth.js', 'src/App.js'],
  codingPatterns: ['async/await', 'error boundaries']
};
```

### Leveraging Context for Better Suggestions

```python
# Continue uses context to suggest:
# 1. Consistent naming conventions
def fetch_user_data(user_id):  # Based on project naming patterns
    pass

# 2. Framework-specific patterns
@app.route('/users')  # Flask route pattern
def get_users():
    return jsonify(users)

# 3. Error handling patterns from existing code
try:
    result = process_data(data)
except ValueError as e:  # Based on existing error handling
    logger.error(f"Invalid data: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# 4. Import suggestions based on usage
from flask import jsonify, request  # Based on Flask usage patterns
import logging
logger = logging.getLogger(__name__)
```

## Multi-Line and Complex Logic Generation

### API Endpoint Generation

```python
# Type: @app.route('/api/users/<int:user_id>', methods=['GET'])
# Continue suggests complete Flask REST API endpoint:

@app.route('/api/users/<int:user_id>', methods=['GET'])
@require_auth
@validate_user_id
def get_user(user_id):
    """
    Get user information by ID.

    Args:
        user_id (int): User ID from URL parameter

    Returns:
        JSON: User data or error message

    Raises:
        404: If user not found
        500: If database error occurs
    """
    try:
        # Get user from database
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': f'No user found with ID {user_id}'
            }), 404

        # Get user's recent posts
        recent_posts = Post.query.filter_by(
            user_id=user_id,
            created_at >= datetime.now() - timedelta(days=30)
        ).limit(5).all()

        # Format response
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active,
            'profile': {
                'bio': user.profile.bio if user.profile else None,
                'avatar_url': user.profile.avatar_url if user.profile else None,
                'location': user.profile.location if user.profile else None
            },
            'stats': {
                'posts_count': user.posts.count(),
                'followers_count': user.followers.count(),
                'following_count': user.following.count()
            },
            'recent_posts': [{
                'id': post.id,
                'title': post.title,
                'created_at': post.created_at.isoformat(),
                'likes_count': post.likes.count()
            } for post in recent_posts]
        }

        # Log successful request
        logger.info(f"User {user_id} data retrieved successfully")

        return jsonify({
            'success': True,
            'data': user_data
        })

    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving user {user_id}: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'Database error',
            'message': 'Failed to retrieve user data'
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error retrieving user {user_id}: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
```

### Database Model Generation

```python
# Type: class Product(db.Model):
# Continue suggests complete SQLAlchemy model:

class Product(db.Model):
    """Product model for e-commerce application."""

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    category = db.relationship('Category', backref='products')
    brand = db.relationship('Brand', backref='products')
    images = db.relationship('ProductImage', backref='product', cascade='all, delete-orphan')
    reviews = db.relationship('ProductReview', backref='product', cascade='all, delete-orphan')
    variants = db.relationship('ProductVariant', backref='product', cascade='all, delete-orphan')

    def __init__(self, name, description=None, price=0.00, sku=None, category_id=None):
        self.name = name
        self.description = description
        self.price = price
        self.sku = sku or self.generate_sku()
        self.category_id = category_id

    def __repr__(self):
        return f'<Product {self.name}>'

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0

    @property
    def average_rating(self):
        """Calculate average rating from reviews."""
        if not self.reviews:
            return 0.0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def generate_sku(self):
        """Generate a unique SKU for the product."""
        import uuid
        return f"PRD-{uuid.uuid4().hex[:8].upper()}"

    def to_dict(self):
        """Convert product to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'sku': self.sku,
            'category_id': self.category_id,
            'brand_id': self.brand_id,
            'stock_quantity': self.stock_quantity,
            'is_active': self.is_active,
            'is_in_stock': self.is_in_stock,
            'average_rating': self.average_rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'category': self.category.name if self.category else None,
            'brand': self.brand.name if self.brand else None,
            'image_count': len(self.images),
            'review_count': len(self.reviews)
        }

    def update_stock(self, quantity_change):
        """Update product stock quantity."""
        self.stock_quantity += quantity_change
        if self.stock_quantity < 0:
            self.stock_quantity = 0

    def soft_delete(self):
        """Soft delete the product."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    @classmethod
    def get_active_products(cls):
        """Get all active products."""
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_products_by_category(cls, category_id):
        """Get products by category."""
        return cls.query.filter_by(category_id=category_id, is_active=True).all()

    @classmethod
    def search_products(cls, search_term):
        """Search products by name or description."""
        search_filter = f"%{search_term}%"
        return cls.query.filter(
            db.or_(
                cls.name.ilike(search_filter),
                cls.description.ilike(search_filter)
            ),
            cls.is_active == True
        ).all()
```

## Advanced Completion Techniques

### Pattern Recognition

Continue learns and recognizes patterns in your code:

```javascript
// Pattern: API route with error handling
app.get('/api/data/:id', async (req, res) => {
  try {
    const data = await Data.findById(req.params.id);
    if (!data) {
      return res.status(404).json({ error: 'Data not found' });
    }
    res.json(data);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Continue recognizes this pattern and suggests similar structures
// when you type: app.post('/api/users', async (req, res) => {
```

### Intelligent Imports

```python
# When you type: pd.DataFrame(
# Continue suggests: import pandas as pd

# When you type: plt.plot(
# Continue suggests: import matplotlib.pyplot as plt

# When you type: torch.nn.Module
# Continue suggests: import torch.nn as nn
```

### Code Style Consistency

```typescript
// Based on existing code style, Continue suggests:

// If your project uses interfaces:
interface UserData {
  id: number;
  name: string;
  email: string;
}

// If your project uses types:
type UserData = {
  id: number;
  name: string;
  email: string;
};
```

## Performance Optimization

### Caching Strategies

```json
{
  "continue": {
    "completion": {
      "cacheEnabled": true,
      "cacheSize": "1GB",
      "cacheStrategy": "adaptive",
      "contextWindowSize": 10000,
      "debounceDelay": 150
    }
  }
}
```

### Model Selection

```json
{
  "continue": {
    "completion": {
      "fastModel": "gpt-3.5-turbo",
      "qualityModel": "gpt-4",
      "autoSelectModel": true,
      "qualityThreshold": 0.8,
      "maxTokens": 2000
    }
  }
}
```

## Testing Generated Code

```python
# Continue can help generate tests for your functions

def calculate_total(items):
    """Calculate total price of items in cart."""
    return sum(item['price'] * item['quantity'] for item in items)

# Type: def test_calculate_total():
# Continue suggests complete test:

def test_calculate_total():
    """Test calculate_total function."""

    # Test empty cart
    assert calculate_total([]) == 0

    # Test single item
    items = [{'price': 10.00, 'quantity': 1}]
    assert calculate_total(items) == 10.00

    # Test multiple items
    items = [
        {'price': 10.00, 'quantity': 2},
        {'price': 5.00, 'quantity': 3}
    ]
    assert calculate_total(items) == 35.00

    # Test floating point precision
    items = [{'price': 1.99, 'quantity': 2}]
    assert abs(calculate_total(items) - 3.98) < 0.01

    # Test zero quantity
    items = [{'price': 10.00, 'quantity': 0}]
    assert calculate_total(items) == 0

    print("All tests passed!")

if __name__ == "__main__":
    test_calculate_total()
```

## Best Practices for Code Generation

### 1. Review and Validate

Always review generated code for:
- **Logic correctness** - Does it handle edge cases?
- **Security issues** - Are there SQL injection or XSS vulnerabilities?
- **Performance** - Is it optimized for your use case?
- **Code style** - Does it match your project conventions?

### 2. Use as Starting Point

Generated code is a great starting point, but customize it for your specific needs:
- Add project-specific business logic
- Include domain-specific validations
- Adapt to your existing architecture
- Add comprehensive error handling

### 3. Learn from Patterns

Pay attention to the patterns Continue suggests:
- Error handling approaches
- Code organization techniques
- Naming conventions
- Documentation styles

### 4. Combine with Manual Coding

Use Continue for:
- **Repetitive code** - CRUD operations, boilerplate
- **Complex logic** - Multi-step algorithms, error handling
- **Documentation** - Function/class documentation
- **Testing** - Unit test generation

Keep manual control for:
- **Business logic** - Domain-specific rules
- **Architecture decisions** - System design choices
- **Performance-critical code** - Optimized implementations
- **Security-sensitive code** - Encryption, authentication

## What's Next?

Fantastic! You've mastered Continue's intelligent code completion and generation capabilities. The suggestions you're seeing now are powered by sophisticated AI that understands your context, coding patterns, and project structure.

In [Chapter 3: Refactoring & Optimization](03-refactoring-optimization.md), we'll explore how Continue can help you improve existing code - identifying performance bottlenecks, suggesting architectural improvements, and modernizing legacy code.

Ready to level up your code quality? Let's continue to [Chapter 3: Refactoring & Optimization](03-refactoring-optimization.md)!

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `user`, `error` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Code Completion & Generation` as an operating subsystem inside **Continue Tutorial: Open-Source AI Coding Agents for IDE and CLI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `User`, `users` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Code Completion & Generation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `user` receives stable contracts.
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
- search upstream code for `self` and `user` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with Continue](01-getting-started.md)
- [Next Chapter: Chapter 3: Refactoring & Optimization](03-refactoring-optimization.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
