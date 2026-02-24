---
layout: default
title: "Pydantic AI Tutorial - Chapter 3: Structured Outputs"
nav_order: 3
has_children: false
parent: Pydantic AI Tutorial
---

# Chapter 3: Structured Outputs & Pydantic Models

Welcome to **Chapter 3: Structured Outputs & Pydantic Models**. In this part of **Pydantic AI Tutorial: Type-Safe AI Agent Development**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master guaranteed structured data generation with complex Pydantic models, validation, and type safety.

## Basic Structured Output

### Simple Model Validation

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field
from typing import List, Optional

# Define structured output model
class Person(BaseModel):
    """A person with validated fields."""
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    occupation: str = Field(..., min_length=2)
    active: bool = True

# Create agent with structured output
agent = Agent('openai:gpt-4', result_type=Person)

# Generate structured data
result = agent.run_sync("Create a profile for a 28-year-old software engineer named Alex Johnson")

print("Generated Person:")
print(f"Name: {result.data.name}")
print(f"Age: {result.data.age}")
print(f"Email: {result.data.email}")
print(f"Occupation: {result.data.occupation}")
print(f"Active: {result.data.active}")

# Validation is automatic
assert isinstance(result.data, Person)
assert result.data.age == 28
assert "software engineer" in result.data.occupation.lower()
print("✓ All validations passed!")
```

### Complex Nested Structures

```python
class Address(BaseModel):
    street: str
    city: str
    state: str = Field(..., min_length=2, max_length=2)  # State code
    zip_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")

class Company(BaseModel):
    name: str
    industry: str
    founded_year: int = Field(..., ge=1800, le=2024)
    headquarters: Address
    employee_count: int = Field(..., ge=1)
    revenue: Optional[float] = Field(None, ge=0)
    public: bool = False

class Employee(BaseModel):
    id: str = Field(..., pattern=r"^EMP-\d{6}$")
    name: str
    position: str
    department: str
    salary: float = Field(..., ge=0)
    hire_date: str  # Could use date type
    manager_id: Optional[str] = None
    skills: List[str] = Field(default_factory=list, max_items=10)

class CompanyProfile(BaseModel):
    company: Company
    employees: List[Employee] = Field(..., min_items=1, max_items=20)
    ceo: Employee

# Generate complex nested structure
profile_agent = Agent('openai:gpt-4', result_type=CompanyProfile)

result = profile_agent.run_sync("""
Create a company profile for a tech startup called TechNova.
Include the company details, 3 employees, and designate one as CEO.
""")

print("Generated Company Profile:")
print(f"Company: {result.data.company.name}")
print(f"Industry: {result.data.company.industry}")
print(f"Founded: {result.data.founded_year}")
print(f"Headquarters: {result.data.company.headquarters.city}, {result.data.company.headquarters.state}")
print(f"Employees: {len(result.data.employees)}")
print(f"CEO: {result.data.ceo.name} - {result.data.ceo.position}")

# Verify nested validation
assert result.data.company.founded_year >= 1800
assert len(result.data.employees) >= 1
assert result.data.ceo.id.startswith("EMP-")
print("✓ Complex nested validation passed!")
```

## Advanced Pydantic Features

### Custom Validators and Field Constraints

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Any
from datetime import date
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class Task(BaseModel):
    id: str = Field(..., pattern=r"^TASK-\d{6}$")
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = None
    priority: Priority
    status: TaskStatus
    assignee: str = Field(..., min_length=2)
    estimated_hours: float = Field(..., ge=0.5, le=100)
    tags: List[str] = Field(default_factory=list, max_items=5)
    created_date: date
    due_date: Optional[date] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    @field_validator('due_date')
    @classmethod
    def due_date_after_created(cls, v, values):
        if v and 'created_date' in values.data and v < values.data['created_date']:
            raise ValueError('Due date cannot be before created date')
        return v

    @model_validator(mode='after')
    def validate_task_logic(self):
        # Business logic validation
        if self.priority == Priority.URGENT and self.status == TaskStatus.TODO:
            # Urgent tasks should be assigned immediately
            pass

        if self.estimated_hours > 40 and self.priority != Priority.HIGH:
            # Large tasks should be high priority
            pass

        return self

# Generate validated tasks
task_agent = Agent('openai:gpt-4', result_type=Task)

task = task_agent.run_sync("""
Create a high-priority task for implementing user authentication.
Assign it to Sarah Chen, estimate 16 hours, and set due date to next week.
""")

print("Generated Task:")
print(f"ID: {task.data.id}")
print(f"Title: {task.data.title}")
print(f"Priority: {task.data.priority.value}")
print(f"Status: {task.data.status.value}")
print(f"Assignee: {task.data.assignee}")
print(f"Estimated Hours: {task.data.estimated_hours}")
print(f"Created: {task.data.created_date}")
print(f"Due: {task.data.due_date}")

# Test validation
try:
    # This should fail due to empty title
    invalid_task = Task(
        id="TASK-000001",
        title="   ",  # Invalid: whitespace only
        priority=Priority.MEDIUM,
        status=TaskStatus.TODO,
        assignee="John",
        estimated_hours=8,
        created_date=date.today()
    )
except ValueError as e:
    print(f"✓ Validation caught invalid title: {e}")

print("✓ All task validations passed!")
```

### Union Types and Discriminated Unions

```python
from typing import Union, Literal

class TextMessage(BaseModel):
    type: Literal["text"]
    content: str = Field(..., min_length=1, max_length=1000)
    sender: str
    timestamp: str

class ImageMessage(BaseModel):
    type: Literal["image"]
    image_url: str
    caption: Optional[str] = None
    sender: str
    timestamp: str

class FileMessage(BaseModel):
    type: Literal["file"]
    file_name: str
    file_url: str
    file_size: int = Field(..., ge=0)
    sender: str
    timestamp: str

# Union type for different message types
Message = Union[TextMessage, ImageMessage, FileMessage]

class ChatSession(BaseModel):
    session_id: str
    participants: List[str] = Field(..., min_items=2)
    messages: List[Message] = Field(default_factory=list, max_items=100)

# Generate discriminated union
message_agent = Agent('openai:gpt-4', result_type=Message)
chat_agent = Agent('openai:gpt-4', result_type=ChatSession)

# Generate different message types
messages = []

# Text message
text_msg = message_agent.run_sync("Create a text message from Alice saying 'Hello everyone!'")
messages.append(text_msg.data)

# Image message
image_msg = message_agent.run_sync("Create an image message from Bob sharing a photo of a sunset")
messages.append(image_msg.data)

# File message
file_msg = message_agent.run_sync("Create a file message from Carol sharing a PDF document")
messages.append(file_msg.data)

print("Generated Messages:")
for i, msg in enumerate(messages, 1):
    print(f"{i}. {msg.type.upper()}: {msg.sender} - ", end="")
    if hasattr(msg, 'content'):
        print(f"'{msg.content}'")
    elif hasattr(msg, 'image_url'):
        print(f"Image: {msg.image_url}")
    elif hasattr(msg, 'file_name'):
        print(f"File: {msg.file_name} ({msg.file_size} bytes)")

# Generate chat session
chat = chat_agent.run_sync("""
Create a chat session with Alice, Bob, and Carol.
Include 2-3 messages of different types.
""")

print(f"\nChat Session: {chat.data.session_id}")
print(f"Participants: {', '.join(chat.data.participants)}")
print(f"Total messages: {len(chat.data.messages)}")

# Verify union type discrimination
for msg in chat.data.messages:
    if msg.type == "text":
        assert hasattr(msg, 'content')
    elif msg.type == "image":
        assert hasattr(msg, 'image_url')
    elif msg.type == "file":
        assert hasattr(msg, 'file_name')

print("✓ Union type discrimination validated!")
```

## List and Array Generation

### Structured List Outputs

```python
from pydantic import BaseModel, Field
from typing import List

class TodoItem(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    completed: bool = False
    priority: int = Field(..., ge=1, le=5)  # 1=low, 5=high
    tags: List[str] = Field(default_factory=list, max_items=3)

class TodoList(BaseModel):
    name: str
    description: Optional[str] = None
    items: List[TodoItem] = Field(..., min_items=1, max_items=20)
    created_by: str

# Generate structured list
todo_agent = Agent('openai:gpt-4', result_type=TodoList)

todo_list = todo_agent.run_sync("""
Create a todo list for planning a software development project.
Include 5-7 tasks with different priorities and categories.
""")

print("Generated Todo List:")
print(f"Name: {todo_list.data.name}")
print(f"Created by: {todo_list.data.created_by}")
print(f"Items: {len(todo_list.data.items)}")

for i, item in enumerate(todo_list.data.items, 1):
    status = "✓" if item.completed else "○"
    print(f"{i}. {status} {item.title} (Priority: {item.priority})")
    if item.tags:
        print(f"   Tags: {', '.join(item.tags)}")

# Validate list constraints
assert len(todo_list.data.items) >= 1
assert all(1 <= item.priority <= 5 for item in todo_list.data.items)
assert all(len(item.title) >= 3 for item in todo_list.data.items)
print("✓ List validation passed!")
```

### Complex Array Structures

```python
class Product(BaseModel):
    id: str = Field(..., pattern=r"^PROD-\d{4}$")
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., ge=0)
    category: str
    in_stock: bool = True
    rating: float = Field(..., ge=0, le=5)

class OrderItem(BaseModel):
    product: Product
    quantity: int = Field(..., ge=1, le=100)
    unit_price: float = Field(..., ge=0)

class Order(BaseModel):
    order_id: str = Field(..., pattern=r"^ORD-\d{6}$")
    customer_email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    items: List[OrderItem] = Field(..., min_items=1, max_items=50)
    order_date: str
    total_amount: float = Field(..., ge=0)

    @model_validator(mode='after')
    def validate_total_amount(self):
        calculated_total = sum(item.quantity * item.unit_price for item in self.items)
        if abs(calculated_total - self.total_amount) > 0.01:  # Allow small floating point differences
            raise ValueError(f"Total amount mismatch: calculated {calculated_total}, provided {self.total_amount}")
        return self

# Generate complex order structure
order_agent = Agent('openai:gpt-4', result_type=Order)

order = order_agent.run_sync("""
Create an order for a customer with email john.doe@example.com.
Include 3 different products with quantities and prices.
Calculate the correct total amount.
""")

print("Generated Order:")
print(f"Order ID: {order.data.order_id}")
print(f"Customer: {order.data.customer_email}")
print(f"Date: {order.data.order_date}")
print(f"Total: ${order.data.total_amount:.2f}")

print("\nItems:")
for item in order.data.items:
    print(f"  - {item.product.name} (x{item.quantity}) @ ${item.unit_price:.2f} each")
    print(f"    Category: {item.product.category}, Rating: {item.product.rating}/5")

# Verify business logic validation
calculated_total = sum(item.quantity * item.unit_price for item in order.data.items)
assert abs(calculated_total - order.data.total_amount) < 0.01
print(f"✓ Total validation passed: ${calculated_total:.2f}")
```

## JSON Schema Integration

### Converting Pydantic to JSON Schema

```python
from pydantic_ai import Agent
import json

def pydantic_to_json_schema(model_class):
    """Convert Pydantic model to JSON Schema for agent guidance."""
    return model_class.model_json_schema()

# Define model
class BlogPost(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=100)
    author: str
    tags: List[str] = Field(..., min_items=1, max_items=5)
    published: bool = False
    word_count: int = Field(..., ge=0)

# Get JSON schema
schema = pydantic_to_json_schema(BlogPost)
print("Generated JSON Schema:")
print(json.dumps(schema, indent=2))

# Use schema in prompt
schema_agent = Agent('openai:gpt-4')

prompt_with_schema = f"""
Generate a blog post according to this JSON schema:

{json.dumps(schema, indent=2)}

Create a blog post about artificial intelligence trends in 2024.
"""

# Note: In practice, you'd use result_type=BlogPost instead
result = schema_agent.run_sync(prompt_with_schema)
print(f"\nGenerated content length: {len(result.data)} characters")
```

### Schema Validation and Error Handling

```python
from pydantic import ValidationError

def generate_with_schema_validation(agent: Agent, schema_model, prompt: str, max_attempts: int = 3):
    """Generate with schema validation and retry on validation errors."""

    for attempt in range(max_attempts):
        try:
            # Create agent with result type
            typed_agent = Agent(agent.model.model_name, result_type=schema_model)

            result = typed_agent.run_sync(prompt)

            print(f"✓ Successfully generated valid {schema_model.__name__} on attempt {attempt + 1}")
            return result.data

        except ValidationError as e:
            print(f"✗ Validation error on attempt {attempt + 1}:")
            for error in e.errors()[:3]:  # Show first 3 errors
                field = '.'.join(str(loc) for loc in error['loc'])
                print(f"  {field}: {error['msg']}")

            if attempt < max_attempts - 1:
                # Modify prompt to address validation errors
                error_summary = "; ".join([f"{'.'.join(str(loc) for loc in error['loc'])}: {error['msg']}" for error in e.errors()[:2]])
                prompt = f"{prompt}\n\nPlease fix these validation errors: {error_summary}"

        except Exception as e:
            print(f"✗ Generation error on attempt {attempt + 1}: {e}")
            break

    raise RuntimeError(f"Failed to generate valid {schema_model.__name__} after {max_attempts} attempts")

# Test with validation and retry
class ResearchPaper(BaseModel):
    title: str = Field(..., min_length=10, max_length=200)
    abstract: str = Field(..., min_length=50, max_length=500)
    authors: List[str] = Field(..., min_items=1, max_items=10)
    keywords: List[str] = Field(..., min_items=3, max_items=8)
    publication_year: int = Field(..., ge=2020, le=2025)

agent = Agent('openai:gpt-4')

paper = generate_with_schema_validation(
    agent,
    ResearchPaper,
    "Write a research paper about machine learning ethics"
)

print("Generated Research Paper:")
print(f"Title: {paper.title}")
print(f"Authors: {', '.join(paper.authors)}")
print(f"Year: {paper.publication_year}")
print(f"Keywords: {', '.join(paper.keywords)}")
print(f"Abstract length: {len(paper.abstract)} characters")
```

## Advanced Validation Patterns

### Conditional Validation

```python
from pydantic import BaseModel, Field, field_validator

class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=13, le=120)
    account_type: str = Field(..., enum=["free", "premium", "enterprise"])
    subscription_end: Optional[date] = None

    @field_validator('subscription_end')
    @classmethod
    def validate_subscription(cls, v, values):
        account_type = values.data.get('account_type')
        if account_type in ['premium', 'enterprise'] and v is None:
            raise ValueError(f"{account_type} accounts must have subscription_end date")
        if account_type == 'free' and v is not None:
            raise ValueError("Free accounts cannot have subscription_end date")
        return v

    @field_validator('age')
    @classmethod
    def validate_age_for_account(cls, v, values):
        account_type = values.data.get('account_type')
        if account_type == 'enterprise' and v < 18:
            raise ValueError("Enterprise accounts require users to be 18+")
        return v

# Generate with conditional validation
profile_agent = Agent('openai:gpt-4', result_type=UserProfile)

profiles = []

# Free account
free_profile = profile_agent.run_sync("Create a profile for a 16-year-old student with free account")
profiles.append(("Free Account", free_profile.data))

# Premium account
premium_profile = profile_agent.run_sync("Create a profile for a 25-year-old professional with premium account and 1-year subscription")
profiles.append(("Premium Account", premium_profile.data))

# Enterprise account
enterprise_profile = profile_agent.run_sync("Create a profile for a 30-year-old executive with enterprise account and 2-year subscription")
profiles.append(("Enterprise Account", enterprise_profile.data))

print("Generated User Profiles:")
for account_type, profile in profiles:
    print(f"\n{account_type}:")
    print(f"  Username: {profile.username}")
    print(f"  Age: {profile.age}")
    print(f"  Account Type: {profile.account_type}")
    print(f"  Subscription End: {profile.subscription_end}")

# Test validation failures
try:
    invalid_profile = UserProfile(
        username="test",
        email="test@example.com",
        age=15,
        account_type="enterprise"  # Should fail - too young for enterprise
    )
except ValidationError as e:
    print(f"\n✓ Validation caught invalid enterprise account: {e.errors()[0]['msg']}")
```

### Cross-Field Validation

```python
class Project(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    priority: str = Field(..., enum=["low", "medium", "high", "critical"])
    budget: float = Field(..., ge=0)
    team_size: int = Field(..., ge=1, le=50)
    start_date: date
    end_date: Optional[date] = None
    status: str = Field(..., enum=["planning", "active", "on_hold", "completed"])
    risk_level: str = Field(..., enum=["low", "medium", "high"])

    @model_validator(mode='after')
    def validate_project_logic(self):
        # Date validation
        if self.end_date and self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")

        # Budget validation based on team size
        min_budget = self.team_size * 50000  # $50k per team member
        if self.budget < min_budget:
            raise ValueError(f"Budget too low for team size. Minimum: ${min_budget:,.0f}")

        # Risk assessment based on priority and budget
        if self.priority == "critical" and self.risk_level == "low":
            raise ValueError("Critical priority projects cannot have low risk level")

        # Status validation
        if self.status == "completed" and not self.end_date:
            raise ValueError("Completed projects must have end date")

        return self

# Generate project with complex validation
project_agent = Agent('openai:gpt-4', result_type=Project)

project = project_agent.run_sync("""
Create a high-priority software development project.
Team of 8 developers, budget $800,000, starting next month.
Expected duration 12 months.
""")

print("Generated Project:")
print(f"Name: {project.data.name}")
print(f"Priority: {project.data.priority}")
print(f"Budget: ${project.data.budget:,.0f}")
print(f"Team Size: {project.data.team_size}")
print(f"Start Date: {project.data.start_date}")
print(f"End Date: {project.data.end_date}")
print(f"Status: {project.data.status}")
print(f"Risk Level: {project.data.risk_level}")

# Validate cross-field constraints
days_duration = (project.data.end_date - project.data.start_date).days if project.data.end_date else 0
print(f"Duration: {days_duration} days")

# All validations passed automatically
print("✓ All cross-field validations passed!")
```

## Serialization and API Integration

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic_ai import Agent
from typing import List

app = FastAPI(title="Structured AI API", version="1.0.0")

# Create agents for different endpoints
person_agent = Agent('openai:gpt-4', result_type=Person)
task_agent = Agent('openai:gpt-4', result_type=Task)
company_agent = Agent('openai:gpt-4', result_type=CompanyProfile)

@app.post("/generate/person", response_model=Person)
async def generate_person(description: str):
    """Generate a person profile from description."""
    try:
        result = await person_agent.run(description)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate/task", response_model=Task)
async def generate_task(description: str):
    """Generate a task from description."""
    try:
        result = await task_agent.run(description)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/generate/company", response_model=CompanyProfile)
async def generate_company(description: str):
    """Generate a company profile from description."""
    try:
        result = await company_agent.run(description)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/schemas")
async def get_schemas():
    """Get JSON schemas for all models."""
    return {
        "person": Person.model_json_schema(),
        "task": Task.model_json_schema(),
        "company": CompanyProfile.model_json_schema()
    }

# Test the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Testing Structured Outputs

```python
import requests

# Test person generation
response = requests.post("http://localhost:8000/generate/person",
                        json="Create a profile for a 35-year-old data scientist")

if response.status_code == 200:
    person = response.json()
    print("Generated Person via API:")
    print(f"Name: {person['name']}")
    print(f"Age: {person['age']}")
    print(f"Occupation: {person['occupation']}")

# Test schema endpoint
schema_response = requests.get("http://localhost:8000/schemas")
if schema_response.status_code == 200:
    schemas = schema_response.json()
    print(f"\nAvailable schemas: {list(schemas.keys())}")
    print(f"Person schema has {len(schemas['person']['properties'])} properties")
```

This comprehensive structured outputs chapter demonstrates how to generate guaranteed valid data structures using Pydantic models, complex validation rules, and seamless API integration. The type safety ensures that generated data always conforms to your specifications. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `print`, `Field`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Structured Outputs & Pydantic Models` as an operating subsystem inside **Pydantic AI Tutorial: Type-Safe AI Agent Development**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `BaseModel`, `self`, `item` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Structured Outputs & Pydantic Models` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `print`.
2. **Input normalization**: shape incoming data so `Field` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/pydantic/pydantic-ai)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `print` and `Field` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Advanced Model Configuration & Provider Setup](02-model-configuration.md)
- [Next Chapter: Chapter 4: Dependencies, Tools & External Integrations](04-dependencies-tools.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
