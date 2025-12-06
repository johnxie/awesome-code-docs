---
layout: default
title: "Outlines Tutorial - Chapter 3: JSON Schema"
nav_order: 3
has_children: false
parent: Outlines Tutorial
---

# Chapter 3: JSON Schema & Structured Data Generation

> Generate perfectly structured JSON data with guaranteed schema compliance using Outlines JSON Schema support.

## Basic JSON Schema Generation

### Simple Object Generation

```python
from outlines import models, generate
import json

# Load model
model = models.transformers("microsoft/DialoGPT-small")

# Define a simple JSON schema
person_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 120},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age"]
}

# Create JSON generator
json_generator = generate.json(model, person_schema)

# Generate structured data
person_data = json_generator("Generate information about a person named Alice")
print("Generated person data:")
print(json.dumps(person_data, indent=2))

# Validate the generated data
import jsonschema

try:
    jsonschema.validate(person_data, person_schema)
    print("✓ Generated data is valid according to schema")
except jsonschema.ValidationError as e:
    print(f"✗ Validation error: {e}")
```

### Array Generation

```python
# Generate array of objects
products_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "price": {"type": "number", "minimum": 0},
            "category": {"type": "string", "enum": ["electronics", "books", "clothing"]},
            "in_stock": {"type": "boolean"}
        },
        "required": ["name", "price", "category"]
    },
    "minItems": 1,
    "maxItems": 5
}

products_generator = generate.json(model, products_schema)

products = products_generator("Generate a list of products for an online store")
print("Generated products:")
print(json.dumps(products, indent=2))
```

## Advanced Schema Features

### Nested Objects and References

```python
# Complex schema with nested objects
company_schema = {
    "type": "object",
    "properties": {
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "founded": {"type": "integer", "minimum": 1800, "maximum": 2024},
                "headquarters": {"type": "string"}
            },
            "required": ["name", "founded"]
        },
        "employees": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"},
                    "salary": {"type": "number", "minimum": 0}
                },
                "required": ["name", "role"]
            }
        },
        "departments": {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True
        }
    },
    "required": ["company", "employees"]
}

company_generator = generate.json(model, company_schema)

company = company_generator("Generate information about a tech company")
print("Generated company data:")
print(json.dumps(company, indent=2))
```

### Enums and Constants

```python
# Schema with enums and constants
task_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "pattern": "^TASK-\\d{4}$"},
        "title": {"type": "string", "minLength": 5, "maxLength": 100},
        "status": {
            "type": "string",
            "enum": ["todo", "in_progress", "review", "done"]
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high", "urgent"]
        },
        "assignee": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 5
        }
    },
    "required": ["id", "title", "status", "priority"]
}

task_generator = generate.json(model, task_schema)

task = task_generator("Generate a task for software development")
print("Generated task:")
print(json.dumps(task, indent=2))
```

## Schema Validation and Error Handling

### Automatic Schema Validation

```python
import jsonschema
from jsonschema import ValidationError

def generate_validated_json(model, schema: dict, prompt: str, max_attempts: int = 3):
    """Generate JSON with validation and retry logic."""

    json_generator = generate.json(model, schema)

    for attempt in range(max_attempts):
        try:
            # Generate JSON
            result = json_generator(prompt)

            # Validate against schema
            jsonschema.validate(result, schema)

            print(f"✓ Valid JSON generated on attempt {attempt + 1}")
            return result

        except ValidationError as e:
            print(f"✗ Attempt {attempt + 1} failed validation: {e.message}")
            print(f"   Path: {' -> '.join(str(p) for p in e.absolute_path)}")
            continue

        except Exception as e:
            print(f"✗ Attempt {attempt + 1} failed with error: {e}")
            continue

    raise ValueError(f"Failed to generate valid JSON after {max_attempts} attempts")

# Usage with validation
api_response_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["success", "error"]},
        "message": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "username": {"type": "string"},
                "email": {"type": "string", "format": "email"}
            },
            "required": ["user_id", "username"]
        }
    },
    "required": ["status", "message"]
}

response = generate_validated_json(
    model,
    api_response_schema,
    "Generate an API response for user creation"
)

print("Validated API response:")
print(json.dumps(response, indent=2))
```

### Custom Validation Rules

```python
class EnhancedJSONGenerator:
    def __init__(self, model, schema: dict, custom_validators: dict = None):
        self.model = model
        self.schema = schema
        self.custom_validators = custom_validators or {}
        self.generator = generate.json(model, schema)

    def generate(self, prompt: str, **kwargs):
        """Generate with custom validation."""

        # Generate JSON
        result = self.generator(prompt, **kwargs)

        # Apply custom validators
        self._apply_custom_validation(result)

        return result

    def _apply_custom_validation(self, data):
        """Apply custom validation rules."""

        for field_path, validator in self.custom_validators.items():
            value = self._get_nested_value(data, field_path)
            if value is not None:
                validator(value, data)

    def _get_nested_value(self, data, path: str):
        """Get nested value from dot-separated path."""
        keys = path.split('.')
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

# Custom validators
def validate_email_domain(email: str, data: dict):
    """Validate email domain."""
    if '@' in email:
        domain = email.split('@')[1]
        allowed_domains = ['company.com', 'gmail.com', 'outlook.com']
        if domain not in allowed_domains:
            raise ValidationError(f"Email domain {domain} not allowed")

def validate_age_range(age: int, data: dict):
    """Validate age is reasonable."""
    if not (13 <= age <= 120):
        raise ValidationError(f"Age {age} is not in valid range")

# Enhanced generator with custom validation
enhanced_generator = EnhancedJSONGenerator(
    model,
    person_schema,
    {
        "email": validate_email_domain,
        "age": validate_age_range
    }
)

person = enhanced_generator.generate("Generate a person profile")
print("Enhanced validated person:")
print(json.dumps(person, indent=2))
```

## Schema Composition and Reuse

### Schema Inheritance

```python
# Base schemas for reuse
base_entity_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name"]
}

# Extended schemas
user_schema = {
    "allOf": [
        base_entity_schema,
        {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "role": {"type": "string", "enum": ["admin", "user", "guest"]},
                "is_active": {"type": "boolean"}
            },
            "required": ["email", "role"]
        }
    ]
}

product_schema = {
    "allOf": [
        base_entity_schema,
        {
            "type": "object",
            "properties": {
                "price": {"type": "number", "minimum": 0},
                "category": {"type": "string"},
                "stock_quantity": {"type": "integer", "minimum": 0}
            },
            "required": ["price", "category"]
        }
    ]
}

# Generate using extended schemas
user_generator = generate.json(model, user_schema)
product_generator = generate.json(model, product_schema)

user = user_generator("Generate a user profile")
product = product_generator("Generate a product listing")

print("Generated user:")
print(json.dumps(user, indent=2))
print("\nGenerated product:")
print(json.dumps(product, indent=2))
```

### Schema References ($ref)

```python
# Schema with references
referenced_schema = {
    "definitions": {
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "country": {"type": "string"},
                "postal_code": {"type": "string"}
            },
            "required": ["street", "city", "country"]
        },
        "contact": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "phone": {"type": "string"}
            }
        }
    },
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "headquarters": {"$ref": "#/definitions/address"},
        "contact": {"$ref": "#/definitions/contact"},
        "employees": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "address": {"$ref": "#/definitions/address"},
                    "contact": {"$ref": "#/definitions/contact"}
                },
                "required": ["name"]
            }
        }
    },
    "required": ["company_name", "headquarters"]
}

company_generator = generate.json(model, referenced_schema)

company = company_generator("Generate a company profile with employees")
print("Generated company with references:")
print(json.dumps(company, indent=2))
```

## Performance Optimization

### Schema Compilation and Caching

```python
from functools import lru_cache
import hashlib
import json

class SchemaCache:
    def __init__(self, model):
        self.model = model
        self._cache = {}

    @lru_cache(maxsize=100)
    def get_generator(self, schema_hash: str, schema: str):
        """Get cached generator for schema."""
        schema_dict = json.loads(schema)
        return generate.json(self.model, schema_dict)

    def generate_json(self, schema: dict, prompt: str):
        """Generate JSON with caching."""

        # Create hash for schema
        schema_str = json.dumps(schema, sort_keys=True)
        schema_hash = hashlib.md5(schema_str.encode()).hexdigest()

        # Get or create generator
        generator = self.get_generator(schema_hash, schema_str)

        return generator(prompt)

# Usage
schema_cache = SchemaCache(model)

# Reuse generators for same schemas
user1 = schema_cache.generate_json(user_schema, "Generate user Alice")
user2 = schema_cache.generate_json(user_schema, "Generate user Bob")

print("Cached generation results:")
print(json.dumps([user1, user2], indent=2))
```

### Batch JSON Generation

```python
import asyncio

async def batch_json_generation(model, schema: dict, prompts: list, max_concurrent: int = 3):
    """Generate multiple JSON objects concurrently."""

    json_generator = generate.json(model, schema)

    # Create semaphore for concurrency control
    semaphore = asyncio.Semaphore(max_concurrent)

    async def generate_single(prompt: str):
        async with semaphore:
            return await json_generator(prompt)

    # Generate all at once
    tasks = [generate_single(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)

    return results

# Usage
prompts = [
    "Generate a user profile for a developer",
    "Generate a user profile for a designer",
    "Generate a user profile for a manager",
    "Generate a user profile for an analyst"
]

results = await batch_json_generation(model, user_schema, prompts)

print("Batch generated users:")
for i, user in enumerate(results, 1):
    print(f"{i}. {user['name']} - {user['role']}")
```

## Integration with APIs

### REST API Response Generation

```python
# Generate API responses
api_response_schema = {
    "type": "object",
    "properties": {
        "statusCode": {"type": "integer", "enum": [200, 201, 400, 401, 403, 404, 500]},
        "success": {"type": "boolean"},
        "message": {"type": "string"},
        "data": {
            "oneOf": [
                {"type": "object"},  # For single objects
                {"type": "array"}    # For lists
            ]
        },
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        },
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["statusCode", "success", "message", "timestamp"]
}

api_generator = generate.json(model, api_response_schema)

# Generate different types of API responses
success_response = api_generator("Generate a successful API response for user creation")
error_response = api_generator("Generate an error API response for invalid input")

print("API Responses:")
print("Success:", json.dumps(success_response, indent=2))
print("Error:", json.dumps(error_response, indent=2))
```

### GraphQL Schema Generation

```python
# Generate GraphQL-like structured data
graphql_response_schema = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "posts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "title": {"type": "string"},
                                    "content": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "errors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "path": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }
}

graphql_generator = generate.json(model, graphql_response_schema)

response = graphql_generator("Generate a GraphQL response for user query")
print("Generated GraphQL response:")
print(json.dumps(response, indent=2))
```

## Error Handling and Debugging

### Schema Debugging

```python
def debug_json_generation(model, schema: dict, prompt: str, max_attempts: int = 5):
    """Debug JSON generation process."""

    print(f"Debugging JSON generation for prompt: '{prompt}'")
    print(f"Schema complexity: {len(json.dumps(schema))} characters")

    json_generator = generate.json(model, schema)

    for attempt in range(max_attempts):
        try:
            result = json_generator(prompt)

            # Validate schema
            jsonschema.validate(result, schema)
            print(f"✓ Attempt {attempt + 1}: Valid JSON generated")

            return result

        except ValidationError as e:
            print(f"✗ Attempt {attempt + 1}: Schema validation failed")
            print(f"   Error: {e.message}")
            print(f"   Path: {' -> '.join(str(p) for p in e.absolute_path)}")
            print(f"   Generated: {json.dumps(result, indent=2) if 'result' in locals() else 'N/A'}")

        except Exception as e:
            print(f"✗ Attempt {attempt + 1}: Generation failed with {type(e).__name__}: {e}")

    print("❌ All attempts failed")
    return None

# Debug problematic schema
debug_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name", "age"]
}

debug_result = debug_json_generation(model, debug_schema, "Generate a person")
if debug_result:
    print("Final result:", json.dumps(debug_result, indent=2))
```

This chapter demonstrates how Outlines can generate complex, schema-compliant JSON data with guaranteed structure and validation. The next chapter covers Pydantic models and type safety. 🚀