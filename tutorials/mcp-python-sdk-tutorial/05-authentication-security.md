---
layout: default
title: "MCP Python SDK Tutorial - Chapter 5: Authentication & Security"
nav_order: 5
parent: MCP Python SDK Tutorial
---

# Chapter 5: Authentication & Security

Welcome to **Chapter 5: Authentication & Security**. In this part of **MCP Python SDK Tutorial: Building AI Tool Servers**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement secure authentication, authorization, and security best practices for production MCP servers.

## Authentication Patterns

### API Key Authentication

```python
import hashlib
import secrets

class APIKeyAuth:
    def __init__(self):
        self.valid_keys = set()

    def generate_key(self) -> str:
        key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        self.valid_keys.add(key_hash)
        return key

    def validate_key(self, key: str) -> bool:
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        return key_hash in self.valid_keys

auth = APIKeyAuth()

@app.call_tool()
async def call_tool(name: str, arguments: dict, context: dict):
    # Validate API key from context
    api_key = context.get("headers", {}).get("X-API-Key")
    if not auth.validate_key(api_key):
        return [TextContent(type="text", text="❌ Unauthorized")]

    # Process authenticated request
    ...
```

### OAuth 2.0 Integration

```python
from authlib.integrations.httpx_client import AsyncOAuth2Client

class OAuth2Server:
    def __init__(self, client_id, client_secret, token_url):
        self.client = AsyncOAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            token_endpoint=token_url
        )

    async def get_token(self):
        token = await self.client.fetch_token()
        return token['access_token']

    async def validate_token(self, token: str) -> bool:
        # Validate with OAuth provider
        try:
            response = await self.client.get(
                "https://api.provider.com/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            return response.status_code == 200
        except:
            return False
```

## Input Validation

```python
from pydantic import BaseModel, Field, validator
import re

class FilePathArgs(BaseModel):
    path: str = Field(..., description="File path")

    @validator('path')
    def validate_path(cls, v):
        # Prevent path traversal
        if ".." in v or v.startswith("/"):
            raise ValueError("Invalid path: path traversal detected")

        # Only allow specific directories
        if not v.startswith("data/"):
            raise ValueError("Path must be within data/ directory")

        return v

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        args = FilePathArgs(**arguments)
        # Safe to use args.path
    except ValueError as e:
        return [TextContent(type="text", text=f"Security Error: {e}")]
```

## Sanitization

```python
import html
import re

def sanitize_input(text: str) -> str:
    # Remove HTML
    text = html.escape(text)

    # Remove SQL injection patterns
    dangerous_patterns = [
        r"(\bDROP\b|\bDELETE\b|\bINSERT\b|\bUPDATE\b)",
        r"(--|;|\/\*|\*\/)"
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise ValueError("Potentially dangerous input detected")

    return text
```

## Resource Access Control

```python
class ResourceACL:
    def __init__(self):
        self.permissions = {
            "user_123": {"read": ["file:///public/*"], "write": []},
            "admin_456": {"read": ["file:///*"], "write": ["file:///*"]}
        }

    def can_access(self, user_id: str, resource_uri: str, action: str) -> bool:
        user_perms = self.permissions.get(user_id, {})
        allowed_patterns = user_perms.get(action, [])

        for pattern in allowed_patterns:
            if self.matches_pattern(resource_uri, pattern):
                return True
        return False

    def matches_pattern(self, uri: str, pattern: str) -> bool:
        # Simple glob matching
        import fnmatch
        return fnmatch.fnmatch(uri, pattern)

acl = ResourceACL()

@app.read_resource()
async def read_resource(uri: str, user_id: str):
    if not acl.can_access(user_id, uri, "read"):
        raise PermissionError(f"Access denied to {uri}")

    # Proceed with read
    ...
```

## Encryption

```python
from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())

    def decrypt(self, encrypted: bytes) -> str:
        return self.cipher.decrypt(encrypted).decode()

storage = SecureStorage()

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "store_secret":
        encrypted = storage.encrypt(arguments["secret"])
        return [TextContent(type="text", text=f"Stored: {encrypted.hex()[:20]}...")]
```

## Security Checklist

- ✅ Validate all inputs with Pydantic
- ✅ Sanitize user-provided strings
- ✅ Implement authentication (API keys/OAuth)
- ✅ Use HTTPS for production
- ✅ Prevent path traversal attacks
- ✅ Encrypt sensitive data at rest
- ✅ Log security events
- ✅ Rate limit requests
- ✅ Implement timeouts
- ✅ Use principle of least privilege

## Next Steps

Chapter 6 covers production deployment with Docker, monitoring, and scaling.

**Continue to:** [Chapter 6: Production Deployment](06-production-deployment.md)

---

*Previous: [← Chapter 4: Advanced Patterns](04-advanced-patterns.md)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `text`, `path` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Authentication & Security` as an operating subsystem inside **MCP Python SDK Tutorial: Building AI Tool Servers**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `call_tool`, `pattern`, `arguments` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Authentication & Security` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `path`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [MCP Python SDK repository](https://github.com/modelcontextprotocol/python-sdk)
  Why it matters: authoritative reference on `MCP Python SDK repository` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Advanced Patterns](04-advanced-patterns.md)
- [Next Chapter: Chapter 6: Production Deployment](06-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
