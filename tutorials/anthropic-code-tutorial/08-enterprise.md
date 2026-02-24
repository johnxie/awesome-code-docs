---
layout: default
title: "Chapter 8: Enterprise Integration"
parent: "Anthropic API Tutorial"
nav_order: 8
---

# Chapter 8: Enterprise Integration

Welcome to **Chapter 8: Enterprise Integration**. In this part of **Anthropic API Tutorial: Build Production Apps with Claude**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement enterprise-grade features including AWS Bedrock, Google Vertex AI, compliance, audit logging, and advanced security patterns.

## Overview

Enterprise deployments often require additional considerations around data residency, compliance, audit trails, and integration with existing infrastructure. This chapter covers enterprise-specific patterns for deploying Claude in production.

## AWS Bedrock Integration

### Setup and Authentication

```python
import anthropic

# Create Bedrock client
client = anthropic.AnthropicBedrock(
    # Uses AWS credentials from environment or IAM role
    aws_region="us-east-1"
)

# Or with explicit credentials
client = anthropic.AnthropicBedrock(
    aws_access_key="AKIA...",
    aws_secret_key="...",
    aws_region="us-east-1"
)

# Or with assumed role
client = anthropic.AnthropicBedrock(
    aws_region="us-east-1",
    aws_session_token="..."  # From STS AssumeRole
)
```

### Making Requests via Bedrock

```python
import anthropic

client = anthropic.AnthropicBedrock(aws_region="us-east-1")

# Bedrock uses different model IDs
message = client.messages.create(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello from Bedrock!"}
    ]
)

print(message.content[0].text)

# Available Bedrock model IDs:
# - anthropic.claude-3-5-sonnet-20241022-v2:0
# - anthropic.claude-3-5-haiku-20241022-v1:0
# - anthropic.claude-3-opus-20240229-v1:0
# - anthropic.claude-3-sonnet-20240229-v1:0
# - anthropic.claude-3-haiku-20240307-v1:0
```

### Bedrock with Streaming

```python
import anthropic

client = anthropic.AnthropicBedrock(aws_region="us-east-1")

with client.messages.stream(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem about cloud computing."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Cross-Region Setup

```python
class MultiRegionBedrockClient:
    """Bedrock client with multi-region failover."""

    def __init__(self, regions: list[str]):
        self.clients = {
            region: anthropic.AnthropicBedrock(aws_region=region)
            for region in regions
        }
        self.primary_region = regions[0]

    def create_message(self, **kwargs):
        """Try primary region, failover to others."""
        regions = [self.primary_region] + [
            r for r in self.clients.keys() if r != self.primary_region
        ]

        last_error = None
        for region in regions:
            try:
                return self.clients[region].messages.create(**kwargs)
            except Exception as e:
                last_error = e
                continue

        raise last_error

# Usage
client = MultiRegionBedrockClient(["us-east-1", "us-west-2", "eu-west-1"])
```

## Google Vertex AI Integration

### Setup

```python
import anthropic

# Create Vertex AI client
client = anthropic.AnthropicVertex(
    project_id="your-gcp-project",
    region="us-east5"  # or europe-west1
)

# Uses Application Default Credentials (ADC)
# Set up with: gcloud auth application-default login
```

### Making Requests via Vertex

```python
import anthropic

client = anthropic.AnthropicVertex(
    project_id="my-project",
    region="us-east5"
)

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello from Vertex AI!"}
    ]
)

print(message.content[0].text)

# Vertex AI model IDs:
# - claude-sonnet-4@20250514
# - claude-3-5-sonnet-v2@20241022
# - claude-3-5-haiku@20241022
# - claude-3-opus@20240229
```

## Compliance and Audit Logging

### Comprehensive Audit Logger

```python
import json
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Any
import logging

@dataclass
class AuditEntry:
    """Audit log entry for compliance."""
    event_id: str
    timestamp: str
    event_type: str
    user_id: str
    session_id: str
    model: str
    input_hash: str  # Hash of input for privacy
    output_hash: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    status: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None

class AuditLogger:
    """Enterprise audit logging for compliance."""

    def __init__(self, log_destination: str = "file"):
        self.destination = log_destination
        self.logger = logging.getLogger("anthropic.audit")

        # Configure based on destination
        if log_destination == "file":
            handler = logging.FileHandler("audit.log")
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_request(
        self,
        user_id: str,
        session_id: str,
        model: str,
        messages: list,
        response: Any,
        latency_ms: float,
        request_metadata: dict = None
    ):
        """Log an API request for audit purposes."""
        import uuid

        # Hash sensitive content instead of logging it
        input_content = json.dumps(messages)
        input_hash = hashlib.sha256(input_content.encode()).hexdigest()[:16]

        output_content = ""
        if hasattr(response, 'content') and response.content:
            output_content = str(response.content[0].text if response.content else "")
        output_hash = hashlib.sha256(output_content.encode()).hexdigest()[:16]

        entry = AuditEntry(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type="api_request",
            user_id=user_id,
            session_id=session_id,
            model=model,
            input_hash=input_hash,
            output_hash=output_hash,
            input_tokens=response.usage.input_tokens if hasattr(response, 'usage') else 0,
            output_tokens=response.usage.output_tokens if hasattr(response, 'usage') else 0,
            latency_ms=latency_ms,
            status="success",
            metadata=request_metadata
        )

        self._write_entry(entry)

    def log_error(
        self,
        user_id: str,
        session_id: str,
        model: str,
        error: Exception,
        request_metadata: dict = None
    ):
        """Log an error for audit purposes."""
        import uuid

        entry = AuditEntry(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type="api_error",
            user_id=user_id,
            session_id=session_id,
            model=model,
            input_hash="",
            output_hash="",
            input_tokens=0,
            output_tokens=0,
            latency_ms=0,
            status="error",
            error=str(error),
            metadata=request_metadata
        )

        self._write_entry(entry)

    def _write_entry(self, entry: AuditEntry):
        """Write audit entry to configured destination."""
        self.logger.info(json.dumps(asdict(entry)))
```

### GDPR-Compliant Data Handling

```python
class GDPRCompliantClient:
    """Client with GDPR compliance features."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.audit_logger = AuditLogger()
        self.data_retention_days = 30

    def create_message(
        self,
        user_id: str,
        session_id: str,
        consent_given: bool,
        **kwargs
    ):
        """Create message with GDPR compliance checks."""

        # Verify consent
        if not consent_given:
            raise ValueError("User consent required for AI processing")

        # Add data processing notice to system prompt
        system = kwargs.get("system", "")
        if system:
            system = f"{system}\n\nNote: This conversation may be processed for the stated purpose."
        kwargs["system"] = system

        start_time = time.time()
        try:
            response = self.client.messages.create(**kwargs)

            # Log for audit (without storing actual content)
            self.audit_logger.log_request(
                user_id=user_id,
                session_id=session_id,
                model=kwargs.get("model", "unknown"),
                messages=kwargs.get("messages", []),
                response=response,
                latency_ms=(time.time() - start_time) * 1000,
                request_metadata={"consent": consent_given}
            )

            return response

        except Exception as e:
            self.audit_logger.log_error(
                user_id=user_id,
                session_id=session_id,
                model=kwargs.get("model", "unknown"),
                error=e
            )
            raise

    def handle_deletion_request(self, user_id: str):
        """Handle GDPR right to deletion request."""
        # In practice, this would:
        # 1. Delete user's conversation history
        # 2. Remove user data from logs (or anonymize)
        # 3. Notify relevant systems
        # 4. Generate deletion confirmation

        return {
            "status": "deletion_requested",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "User data deletion request has been processed"
        }

    def export_user_data(self, user_id: str) -> dict:
        """Handle GDPR data portability request."""
        # Export all user data in machine-readable format
        return {
            "user_id": user_id,
            "export_date": datetime.utcnow().isoformat(),
            "data": {
                # Would include actual user data
                "conversations": [],
                "preferences": {},
                "usage_statistics": {}
            }
        }
```

## Single Sign-On Integration

### OAuth/OIDC Integration

```python
from functools import wraps
import jwt
from typing import Callable

class SSOAuthenticator:
    """SSO authentication for Claude API access."""

    def __init__(self, issuer: str, audience: str, jwks_uri: str):
        self.issuer = issuer
        self.audience = audience
        self.jwks_uri = jwks_uri
        self._jwks_client = jwt.PyJWKClient(jwks_uri)

    def validate_token(self, token: str) -> dict:
        """Validate JWT token from SSO provider."""
        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer
            )

            return {
                "valid": True,
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "roles": payload.get("roles", []),
                "groups": payload.get("groups", [])
            }

        except jwt.InvalidTokenError as e:
            return {
                "valid": False,
                "error": str(e)
            }

    def require_auth(self, required_roles: list = None):
        """Decorator to require authentication."""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Get token from request context
                token = kwargs.get("auth_token") or args[0] if args else None

                if not token:
                    raise PermissionError("Authentication required")

                validation = self.validate_token(token)
                if not validation["valid"]:
                    raise PermissionError(f"Invalid token: {validation['error']}")

                if required_roles:
                    user_roles = set(validation.get("roles", []))
                    if not user_roles.intersection(required_roles):
                        raise PermissionError("Insufficient permissions")

                # Add user info to kwargs
                kwargs["user_info"] = validation
                return func(*args, **kwargs)

            return wrapper
        return decorator


# Usage with FastAPI
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()
sso = SSOAuthenticator(
    issuer="https://login.example.com",
    audience="claude-api",
    jwks_uri="https://login.example.com/.well-known/jwks.json"
)

async def get_current_user(authorization: str = Header(...)):
    """Dependency to extract and validate user from token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization[7:]
    validation = sso.validate_token(token)

    if not validation["valid"]:
        raise HTTPException(status_code=401, detail=validation["error"])

    return validation

@app.post("/api/chat")
async def chat(request: dict, user: dict = Depends(get_current_user)):
    """Chat endpoint with SSO authentication."""
    # user contains validated user info
    # Proceed with Claude API call
    pass
```

## Role-Based Access Control

### RBAC Implementation

```python
from enum import Enum
from dataclasses import dataclass
from typing import Set, Dict

class Permission(Enum):
    """API permissions."""
    READ = "read"
    WRITE = "write"
    USE_OPUS = "use_opus"
    USE_SONNET = "use_sonnet"
    USE_HAIKU = "use_haiku"
    USE_TOOLS = "use_tools"
    USE_VISION = "use_vision"
    HIGH_TOKENS = "high_tokens"  # > 4096 max_tokens
    ADMIN = "admin"

@dataclass
class Role:
    """Role definition."""
    name: str
    permissions: Set[Permission]

class RBACManager:
    """Role-based access control for Claude API."""

    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}
        self._setup_default_roles()

    def _setup_default_roles(self):
        """Set up default roles."""
        self.roles["viewer"] = Role(
            name="viewer",
            permissions={Permission.READ}
        )

        self.roles["basic_user"] = Role(
            name="basic_user",
            permissions={
                Permission.READ,
                Permission.WRITE,
                Permission.USE_HAIKU,
                Permission.USE_SONNET
            }
        )

        self.roles["power_user"] = Role(
            name="power_user",
            permissions={
                Permission.READ,
                Permission.WRITE,
                Permission.USE_HAIKU,
                Permission.USE_SONNET,
                Permission.USE_OPUS,
                Permission.USE_TOOLS,
                Permission.USE_VISION,
                Permission.HIGH_TOKENS
            }
        )

        self.roles["admin"] = Role(
            name="admin",
            permissions={p for p in Permission}
        )

    def assign_role(self, user_id: str, role_name: str):
        """Assign a role to a user."""
        if role_name not in self.roles:
            raise ValueError(f"Unknown role: {role_name}")

        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role_name)

    def get_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user."""
        permissions = set()
        for role_name in self.user_roles.get(user_id, set()):
            if role_name in self.roles:
                permissions.update(self.roles[role_name].permissions)
        return permissions

    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        return permission in self.get_permissions(user_id)


class RBACEnforcedClient:
    """Claude client with RBAC enforcement."""

    MODEL_PERMISSIONS = {
        "claude-opus-4-20250514": Permission.USE_OPUS,
        "claude-sonnet-4-20250514": Permission.USE_SONNET,
        "claude-3-5-haiku-20241022": Permission.USE_HAIKU
    }

    def __init__(self, rbac: RBACManager):
        self.client = anthropic.Anthropic()
        self.rbac = rbac

    def create_message(self, user_id: str, **kwargs):
        """Create message with RBAC enforcement."""

        # Check model permission
        model = kwargs.get("model", "claude-sonnet-4-20250514")
        model_permission = self.MODEL_PERMISSIONS.get(model)
        if model_permission and not self.rbac.check_permission(user_id, model_permission):
            raise PermissionError(f"User {user_id} does not have permission to use {model}")

        # Check tools permission
        if kwargs.get("tools") and not self.rbac.check_permission(user_id, Permission.USE_TOOLS):
            raise PermissionError(f"User {user_id} does not have permission to use tools")

        # Check high tokens permission
        max_tokens = kwargs.get("max_tokens", 1024)
        if max_tokens > 4096 and not self.rbac.check_permission(user_id, Permission.HIGH_TOKENS):
            kwargs["max_tokens"] = 4096  # Enforce limit

        # Check vision permission (if images in messages)
        if self._has_images(kwargs.get("messages", [])):
            if not self.rbac.check_permission(user_id, Permission.USE_VISION):
                raise PermissionError(f"User {user_id} does not have permission to use vision")

        return self.client.messages.create(**kwargs)

    def _has_images(self, messages: list) -> bool:
        """Check if messages contain images."""
        for msg in messages:
            content = msg.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "image":
                        return True
        return False
```

## Multi-Tenant Architecture

### Tenant Isolation

```python
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class TenantConfig:
    """Configuration for a tenant."""
    tenant_id: str
    name: str
    api_key: Optional[str]  # Optional per-tenant API key
    model_allowlist: list
    max_tokens_per_request: int
    max_requests_per_minute: int
    max_tokens_per_day: int

class MultiTenantClient:
    """Multi-tenant Claude client with isolation."""

    def __init__(self, default_api_key: str = None):
        self.default_client = anthropic.Anthropic(api_key=default_api_key)
        self.tenant_configs: Dict[str, TenantConfig] = {}
        self.tenant_clients: Dict[str, anthropic.Anthropic] = {}
        self.usage_tracker: Dict[str, dict] = {}

    def register_tenant(self, config: TenantConfig):
        """Register a new tenant."""
        self.tenant_configs[config.tenant_id] = config

        # Create tenant-specific client if they have their own API key
        if config.api_key:
            self.tenant_clients[config.tenant_id] = anthropic.Anthropic(
                api_key=config.api_key
            )

        # Initialize usage tracking
        self.usage_tracker[config.tenant_id] = {
            "requests_this_minute": 0,
            "tokens_today": 0,
            "last_reset_minute": datetime.utcnow().minute,
            "last_reset_day": datetime.utcnow().date()
        }

    def create_message(self, tenant_id: str, **kwargs):
        """Create message for a specific tenant."""

        config = self.tenant_configs.get(tenant_id)
        if not config:
            raise ValueError(f"Unknown tenant: {tenant_id}")

        # Enforce tenant restrictions
        self._enforce_restrictions(tenant_id, config, kwargs)

        # Get appropriate client
        client = self.tenant_clients.get(tenant_id, self.default_client)

        # Make request
        response = client.messages.create(**kwargs)

        # Track usage
        self._track_usage(tenant_id, response)

        return response

    def _enforce_restrictions(self, tenant_id: str, config: TenantConfig, kwargs: dict):
        """Enforce tenant-specific restrictions."""

        # Check model allowlist
        model = kwargs.get("model", "claude-sonnet-4-20250514")
        if model not in config.model_allowlist:
            raise PermissionError(f"Model {model} not allowed for tenant {tenant_id}")

        # Enforce max tokens
        if kwargs.get("max_tokens", 0) > config.max_tokens_per_request:
            kwargs["max_tokens"] = config.max_tokens_per_request

        # Check rate limits
        usage = self.usage_tracker[tenant_id]
        now = datetime.utcnow()

        # Reset minute counter if needed
        if now.minute != usage["last_reset_minute"]:
            usage["requests_this_minute"] = 0
            usage["last_reset_minute"] = now.minute

        # Reset daily counter if needed
        if now.date() != usage["last_reset_day"]:
            usage["tokens_today"] = 0
            usage["last_reset_day"] = now.date()

        # Check limits
        if usage["requests_this_minute"] >= config.max_requests_per_minute:
            raise RateLimitError(f"Rate limit exceeded for tenant {tenant_id}")

        if usage["tokens_today"] >= config.max_tokens_per_day:
            raise RateLimitError(f"Daily token limit exceeded for tenant {tenant_id}")

    def _track_usage(self, tenant_id: str, response):
        """Track usage for a tenant."""
        usage = self.usage_tracker[tenant_id]
        usage["requests_this_minute"] += 1
        usage["tokens_today"] += (
            response.usage.input_tokens + response.usage.output_tokens
        )

    def get_tenant_usage(self, tenant_id: str) -> dict:
        """Get usage statistics for a tenant."""
        return self.usage_tracker.get(tenant_id, {})
```

## Disaster Recovery

### Failover Strategy

```python
import time
from enum import Enum
from typing import List, Optional

class Provider(Enum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"

class DisasterRecoveryClient:
    """Client with automatic failover across providers."""

    def __init__(
        self,
        providers: List[Provider] = None,
        bedrock_region: str = "us-east-1",
        vertex_project: str = None,
        vertex_region: str = "us-east5"
    ):
        self.providers = providers or [
            Provider.ANTHROPIC,
            Provider.BEDROCK,
            Provider.VERTEX
        ]

        self.clients = {}

        # Initialize available clients
        try:
            self.clients[Provider.ANTHROPIC] = anthropic.Anthropic()
        except:
            pass

        try:
            self.clients[Provider.BEDROCK] = anthropic.AnthropicBedrock(
                aws_region=bedrock_region
            )
        except:
            pass

        if vertex_project:
            try:
                self.clients[Provider.VERTEX] = anthropic.AnthropicVertex(
                    project_id=vertex_project,
                    region=vertex_region
                )
            except:
                pass

        self.model_mapping = {
            Provider.ANTHROPIC: {
                "sonnet": "claude-sonnet-4-20250514",
                "haiku": "claude-3-5-haiku-20241022"
            },
            Provider.BEDROCK: {
                "sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "haiku": "anthropic.claude-3-5-haiku-20241022-v1:0"
            },
            Provider.VERTEX: {
                "sonnet": "claude-3-5-sonnet-v2@20241022",
                "haiku": "claude-3-5-haiku@20241022"
            }
        }

    def create_message(self, model_tier: str = "sonnet", **kwargs):
        """Create message with automatic failover."""

        last_error = None

        for provider in self.providers:
            if provider not in self.clients:
                continue

            try:
                # Map model to provider-specific ID
                model_id = self.model_mapping[provider].get(model_tier)
                if not model_id:
                    continue

                kwargs_copy = kwargs.copy()
                kwargs_copy["model"] = model_id

                return self.clients[provider].messages.create(**kwargs_copy)

            except Exception as e:
                last_error = e
                logging.warning(f"Provider {provider.value} failed: {e}")
                continue

        raise last_error or Exception("No providers available")

    def health_check(self) -> dict:
        """Check health of all providers."""
        results = {}

        for provider in self.providers:
            if provider not in self.clients:
                results[provider.value] = {"status": "not_configured"}
                continue

            try:
                model_tier = "haiku"  # Use cheapest model for health check
                model_id = self.model_mapping[provider].get(model_tier)

                start = time.time()
                self.clients[provider].messages.create(
                    model=model_id,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                latency = (time.time() - start) * 1000

                results[provider.value] = {
                    "status": "healthy",
                    "latency_ms": latency
                }

            except Exception as e:
                results[provider.value] = {
                    "status": "unhealthy",
                    "error": str(e)
                }

        return results
```

## Summary

In this chapter, you've learned:

- **Cloud Providers**: Integrating with AWS Bedrock and Google Vertex AI
- **Compliance**: Audit logging and GDPR-compliant data handling
- **Authentication**: SSO/OIDC integration patterns
- **Authorization**: Role-based access control implementation
- **Multi-Tenancy**: Tenant isolation and resource management
- **Disaster Recovery**: Multi-provider failover strategies

## Key Takeaways

1. **Choose the Right Provider**: Direct API, Bedrock, or Vertex based on requirements
2. **Log Everything**: Comprehensive audit logs for compliance
3. **Enforce Access Control**: Implement RBAC for security
4. **Plan for Failure**: Multi-provider failover ensures availability
5. **Isolate Tenants**: Proper isolation for multi-tenant deployments

## Tutorial Complete!

Congratulations! You've completed the Anthropic API Tutorial. You now have the knowledge to:

- Build applications with the Messages API
- Extend Claude with tool use
- Process images with vision
- Stream responses for better UX
- Apply advanced prompt engineering
- Deploy with production best practices
- Integrate with enterprise systems

## Next Steps

- Explore the [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) for more examples
- Join the [Anthropic Discord](https://discord.gg/anthropic) community
- Review the [API Reference](https://docs.anthropic.com/en/api) for detailed documentation

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `user_id`, `anthropic` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Enterprise Integration` as an operating subsystem inside **Anthropic API Tutorial: Build Production Apps with Claude**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `model`, `kwargs`, `client` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Enterprise Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `user_id` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `anthropic`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
  Why it matters: authoritative reference on `Anthropic Python SDK` (github.com).
- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)
  Why it matters: authoritative reference on `Anthropic TypeScript SDK` (github.com).
- [Anthropic Docs](https://docs.anthropic.com/)
  Why it matters: authoritative reference on `Anthropic Docs` (docs.anthropic.com).

Suggested trace strategy:
- search upstream code for `self` and `user_id` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Production Best Practices](07-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
