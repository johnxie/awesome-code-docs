---
layout: default
title: "Outlines Tutorial - Chapter 4: Type Safety"
nav_order: 4
has_children: false
parent: Outlines Tutorial
---

# Chapter 4: Type Safety & Pydantic Integration

> Generate type-safe Python objects with runtime validation using Pydantic models and Outlines.

## Basic Pydantic Integration

### Simple Model Generation

```python
from outlines import models, generate
from pydantic import BaseModel, Field
from typing import List, Optional
import json

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Define Pydantic models
class Person(BaseModel):
    name: str = Field(..., description="Full name of the person")
    age: int = Field(..., ge=0, le=120, description="Age in years")
    email: Optional[str] = Field(None, description="Email address")
    occupation: str = Field(..., description="Job title or occupation")

# Generate with Pydantic model
person_generator = generate.pydantic(model, Person)

# Generate a person
person = person_generator("Generate information about a software engineer")
print("Generated person:")
print(f"Name: {person.name}")
print(f"Age: {person.age}")
print(f"Email: {person.email}")
print(f"Occupation: {person.occupation}")

# Access as typed object
print(f"Type of age: {type(person.age)}")  # <class 'int'>
print(f"Is valid: {person.model_validate(person.model_dump())}")  # Validation
```

### Complex Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str = Field(..., pattern=r"\d{5}(-\d{4})?")

class Company(BaseModel):
    name: str
    industry: str
    founded_year: int = Field(..., ge=1800, le=2024)
    headquarters: Address
    employee_count: int = Field(..., ge=1)
    is_public: bool = False

class Employee(BaseModel):
    id: str = Field(..., pattern=r"EMP-\d{6}")
    name: str
    role: str
    department: str
    salary: float = Field(..., ge=0)
    hire_date: str  # Could use date type with custom parsing

class CompanyProfile(BaseModel):
    company: Company
    employees: List[Employee] = Field(..., min_items=1, max_items=10)

# Generate complex nested structure
company_generator = generate.pydantic(model, CompanyProfile)

company_profile = company_generator("Generate a tech company profile with 3 employees")

print("Generated company profile:")
print(f"Company: {company_profile.company.name}")
print(f"Industry: {company_profile.company.industry}")
print(f"Headquarters: {company_profile.company.headquarters.city}, {company_profile.company.headquarters.state}")
print(f"Employees: {len(company_profile.employees)}")

for emp in company_profile.employees:
    print(f"  - {emp.name} ({emp.role}) in {emp.department}")
```

## Advanced Pydantic Features

### Custom Validators and Constraints

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import date, datetime
import re

class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=13, le=120)
    join_date: date
    is_active: bool = True
    tags: List[str] = Field(default_factory=list, max_items=5)

    @field_validator('username')
    @classmethod
    def username_not_reserved(cls, v):
        reserved = ['admin', 'root', 'system', 'guest']
        if v.lower() in reserved:
            raise ValueError(f'Username "{v}" is reserved')
        return v

    @field_validator('email')
    @classmethod
    def email_domain_allowed(cls, v):
        allowed_domains = ['gmail.com', 'outlook.com', 'company.com', 'edu']
        domain = v.split('@')[1]
        if domain not in allowed_domains:
            raise ValueError(f'Email domain "{domain}" not allowed')
        return v

    @model_validator(mode='after')
    def validate_profile(self):
        # Custom cross-field validation
        if self.age < 18 and not self.email.endswith('.edu'):
            raise ValueError('Users under 18 must have .edu email')

        # Business logic validation
        if 'admin' in self.tags and not self.is_active:
            raise ValueError('Inactive users cannot have admin tag')

        return self

# Generate with validation
profile_generator = generate.pydantic(model, UserProfile)

try:
    profile = profile_generator("Generate a profile for a 25-year-old developer")
    print("Generated valid profile:")
    print(f"Username: {profile.username}")
    print(f"Email: {profile.email}")
    print(f"Age: {profile.age}")
    print(f"Tags: {profile.tags}")

except Exception as e:
    print(f"Generation/validation failed: {e}")
```

### Enum and Literal Types

```python
from enum import Enum
from typing import Literal

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class Task(BaseModel):
    id: str = Field(..., pattern=r"^TASK-\d{6}$")
    title: str = Field(..., min_length=5, max_length=100)
    description: Optional[str] = None
    priority: Priority
    status: Status
    assignee: str
    estimated_hours: float = Field(..., ge=0, le=100)
    tags: List[str] = Field(default_factory=list)

    @model_validator(mode='after')
    def validate_task_logic(self):
        # Urgent tasks should be high priority
        if self.priority == Priority.URGENT and self.status == Status.TODO:
            # Auto-assign to urgent queue (could be handled differently)
            pass
        return self

# Generate tasks with enums
task_generator = generate.pydantic(model, Task)

task = task_generator("Generate a high-priority bug fix task")

print("Generated task:")
print(f"ID: {task.id}")
print(f"Title: {task.title}")
print(f"Priority: {task.priority.value}")
print(f"Status: {task.status.value}")
print(f"Assignee: {task.assignee}")

# Verify enum types
print(f"Priority type: {type(task.priority)}")  # <enum 'Priority'>
print(f"Status type: {type(task.status)}")      # <enum 'Status'>
```

## Union Types and Discriminated Unions

```python
from typing import Union, Literal

class TextMessage(BaseModel):
    type: Literal["text"]
    content: str
    sender: str

class ImageMessage(BaseModel):
    type: Literal["image"]
    image_url: str
    caption: Optional[str] = None
    sender: str

class SystemMessage(BaseModel):
    type: Literal["system"]
    event: str
    timestamp: str

# Union type for different message types
Message = Union[TextMessage, ImageMessage, SystemMessage]

class ChatSession(BaseModel):
    session_id: str
    participants: List[str]
    messages: List[Message] = Field(default_factory=list, max_items=50)

# Generate discriminated union
message_generator = generate.pydantic(model, Message)
chat_generator = generate.pydantic(model, ChatSession)

# Generate different message types
text_msg = message_generator("Generate a text message from Alice")
image_msg = message_generator("Generate an image message from Bob")
system_msg = message_generator("Generate a system message about user joining")

print("Generated messages:")
print(f"Text: {text_msg.content if hasattr(text_msg, 'content') else 'N/A'}")
print(f"Image: {image_msg.image_url if hasattr(image_msg, 'image_url') else 'N/A'}")
print(f"System: {system_msg.event if hasattr(system_msg, 'event') else 'N/A'}")

# Generate chat session
chat = chat_generator("Generate a chat session with 3 messages")
print(f"\nChat session with {len(chat.messages)} messages")
```

## Serialization and Deserialization

### JSON Conversion with Validation

```python
import json

class APISerializer:
    def __init__(self, model_class: type[BaseModel]):
        self.model_class = model_class

    def from_json_string(self, json_str: str) -> BaseModel:
        """Deserialize JSON string to validated model."""
        data = json.loads(json_str)
        return self.model_class(**data)

    def to_json_string(self, instance: BaseModel) -> str:
        """Serialize model to JSON string."""
        return instance.model_dump_json(indent=2)

    def validate_and_convert(self, data: dict) -> BaseModel:
        """Validate dict and convert to model."""
        return self.model_class(**data)

# API response models
class APIResponse(BaseModel):
    status: Literal["success", "error"]
    message: str
    data: Optional[dict] = None
    errors: Optional[List[str]] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    profile: Optional[dict] = None

# Create serializers
api_serializer = APISerializer(APIResponse)
user_serializer = APISerializer(UserResponse)

# Generate and serialize
response_gen = generate.pydantic(model, APIResponse)
user_gen = generate.pydantic(model, UserResponse)

# Generate API response
api_response = response_gen("Generate a successful API response")

# Convert to JSON
json_response = api_serializer.to_json_string(api_response)
print("API Response JSON:")
print(json_response)

# Parse back from JSON
parsed_response = api_serializer.from_json_string(json_response)
print(f"Parsed status: {parsed_response.status}")
```

### Custom JSON Encoders

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)

class AuditLogEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str
    user_id: str
    resource: str
    details: dict = Field(default_factory=dict)

    def to_json(self) -> str:
        """Custom JSON serialization."""
        return json.dumps(self, cls=CustomJSONEncoder, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'AuditLogEntry':
        """Custom JSON deserialization."""
        data = json.loads(json_str)
        # Handle datetime parsing
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

# Generate audit logs
audit_generator = generate.pydantic(model, AuditLogEntry)

audit_entry = audit_generator("Generate an audit log for user login")

# Serialize to JSON
json_log = audit_entry.to_json()
print("Audit log JSON:")
print(json_log)

# Deserialize from JSON
parsed_log = AuditLogEntry.from_json(json_log)
print(f"Parsed action: {parsed_log.action}")
print(f"Parsed timestamp: {parsed_log.timestamp}")
```

## Integration with FastAPI

### Type-Safe API Endpoints

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from outlines import models, generate

# FastAPI app
app = FastAPI(title="Outlines API", version="1.0.0")

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# API Models
class TaskRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=500)
    priority: Optional[str] = Field(None, pattern=r"^(low|medium|high|urgent)$")

class TaskResponse(BaseModel):
    id: str
    title: str = Field(..., min_length=5, max_length=100)
    description: str
    priority: str
    status: str = "todo"
    created_at: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

# Create generators
task_generator = generate.pydantic(model, TaskResponse)

@app.post("/generate-task", response_model=TaskResponse)
async def generate_task(request: TaskRequest):
    """Generate a structured task from description."""

    try:
        # Create prompt from request
        prompt = f"Generate a task based on: {request.description}"
        if request.priority:
            prompt += f" Priority should be {request.priority}."

        # Generate task
        task = task_generator(prompt)

        # Validate generated task meets requirements
        if request.priority and task.priority != request.priority:
            # Regenerate with specific priority
            priority_prompt = f"{prompt} Make sure priority is {request.priority}."
            task = task_generator(priority_prompt)

        return task

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/task-schema")
async def get_task_schema():
    """Return the JSON schema for TaskResponse."""
    return TaskResponse.model_json_schema()

# Batch generation endpoint
@app.post("/generate-tasks", response_model=List[TaskResponse])
async def generate_tasks(requests: List[TaskRequest]):
    """Generate multiple tasks."""

    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 tasks per request")

    tasks = []
    for req in requests:
        try:
            prompt = f"Generate a task: {req.description}"
            task = task_generator(prompt)
            tasks.append(task)
        except Exception as e:
            # Continue with other tasks, could log error
            continue

    return tasks

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### API Testing

```python
import requests
import json

# Test the API
base_url = "http://localhost:8000"

# Test task generation
task_request = {
    "description": "Implement user authentication system with JWT tokens and password hashing",
    "priority": "high"
}

response = requests.post(f"{base_url}/generate-task", json=task_request)
if response.status_code == 200:
    task = response.json()
    print("Generated task:")
    print(json.dumps(task, indent=2))

    # Validate with Pydantic
    from your_api_models import TaskResponse
    validated_task = TaskResponse(**task)
    print(f"✓ Task is valid: {validated_task.title}")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Test schema endpoint
schema_response = requests.get(f"{base_url}/task-schema")
if schema_response.status_code == 200:
    schema = schema_response.json()
    print("\nTask schema properties:")
    for prop, details in schema.get('properties', {}).items():
        print(f"  {prop}: {details.get('type', 'unknown')}")
```

## Performance and Caching

### Model Instance Caching

```python
from functools import lru_cache
import time

class CachedPydanticGenerator:
    def __init__(self, model, model_class: type[BaseModel], cache_ttl: int = 300):
        self.model = model
        self.model_class = model_class
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._generator = generate.pydantic(model, model_class)

    def generate(self, prompt: str, use_cache: bool = True) -> BaseModel:
        """Generate with caching."""

        if not use_cache:
            return self._generator(prompt)

        cache_key = hash(prompt)

        # Check cache
        if cache_key in self._cache:
            cached_result, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_result

        # Generate new result
        result = self._generator(prompt)

        # Cache result
        self._cache[cache_key] = (result, time.time())

        # Limit cache size
        if len(self._cache) > 1000:
            # Remove oldest entries (simple implementation)
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]

        return result

    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()

# Usage with caching
cached_generator = CachedPydanticGenerator(model, Person)

# First generation (will be computed)
person1 = cached_generator.generate("Generate a person named Alice")
print(f"Generated: {person1.name}")

# Second generation with same prompt (will be cached)
person2 = cached_generator.generate("Generate a person named Alice")
print(f"Cached result: {person2.name}")

print(f"Same object: {person1 is person2}")  # True if cached
```

### Async Generation

```python
import asyncio
from typing import List

class AsyncPydanticGenerator:
    def __init__(self, model, model_class: type[BaseModel]):
        self.model = model
        self.model_class = model_class
        self._generator = generate.pydantic(model, model_class)

    async def generate_single(self, prompt: str) -> BaseModel:
        """Generate a single instance."""
        # Note: In practice, you'd need async model support
        # This is a simplified example
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._generator, prompt)

    async def generate_batch(self, prompts: List[str], max_concurrent: int = 3) -> List[BaseModel]:
        """Generate multiple instances concurrently."""

        semaphore = asyncio.Semaphore(max_concurrent)

        async def generate_with_semaphore(prompt: str):
            async with semaphore:
                return await self.generate_single(prompt)

        tasks = [generate_with_semaphore(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)

        return results

# Usage
async_generator = AsyncPydanticGenerator(model, Task)

# Generate single task
task = await async_generator.generate_single("Generate a bug fix task")
print(f"Single task: {task.title}")

# Generate multiple tasks concurrently
prompts = [
    "Generate a feature development task",
    "Generate a documentation task",
    "Generate a testing task"
]

tasks = await async_generator.generate_batch(prompts)
print(f"Generated {len(tasks)} tasks:")
for t in tasks:
    print(f"  - {t.title}")
```

## Error Handling and Validation

### Comprehensive Error Handling

```python
from pydantic import ValidationError
import traceback

class RobustPydanticGenerator:
    def __init__(self, model, model_class: type[BaseModel], max_retries: int = 3):
        self.model = model
        self.model_class = model_class
        self.max_retries = max_retries
        self._generator = generate.pydantic(model, model_class)

    def generate_with_validation(self, prompt: str, **kwargs) -> BaseModel:
        """Generate with comprehensive error handling and validation."""

        last_error = None

        for attempt in range(self.max_retries):
            try:
                # Generate raw result
                raw_result = self._generator(prompt, **kwargs)

                # Additional validation
                self._validate_business_rules(raw_result)

                print(f"✓ Successfully generated valid {self.model_class.__name__} on attempt {attempt + 1}")
                return raw_result

            except ValidationError as e:
                last_error = e
                print(f"✗ Attempt {attempt + 1}: Pydantic validation failed")
                print(f"   Errors: {len(e.errors())} validation errors")

                # Print detailed errors
                for error in e.errors()[:3]:  # Show first 3 errors
                    field = '.'.join(str(loc) for loc in error['loc'])
                    print(f"   - {field}: {error['msg']}")

            except Exception as e:
                last_error = e
                print(f"✗ Attempt {attempt + 1}: Generation failed with {type(e).__name__}")
                print(f"   Error: {str(e)}")

                # Print stack trace for debugging
                if attempt == self.max_retries - 1:
                    traceback.print_exc()

        # If we get here, all attempts failed
        raise RuntimeError(f"Failed to generate valid {self.model_class.__name__} after {self.max_retries} attempts. Last error: {last_error}")

    def _validate_business_rules(self, instance: BaseModel):
        """Apply custom business rule validation."""

        # Example business rules for Task model
        if hasattr(instance, 'priority') and hasattr(instance, 'status'):
            if instance.priority == 'urgent' and instance.status == 'todo':
                # Could add special handling or warnings
                pass

        # Check for required relationships
        if hasattr(instance, 'assignee') and hasattr(instance, 'status'):
            if not instance.assignee and instance.status != 'todo':
                raise ValidationError("Tasks with status other than 'todo' must have an assignee")

# Usage with robust error handling
robust_generator = RobustPydanticGenerator(model, Task)

try:
    task = robust_generator.generate_with_validation(
        "Generate an urgent task without assignee (should fail business rules)"
    )
    print("Generated task:", task.title)

except RuntimeError as e:
    print("Generation failed:", str(e))
```

This comprehensive chapter demonstrates how Outlines integrates with Pydantic to provide type-safe, validated object generation with runtime guarantees. The next chapter covers context-free grammars and formal language generation. 🚀