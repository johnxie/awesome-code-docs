---
layout: default
title: "Open WebUI Tutorial - Chapter 7: API Integrations & External Services"
nav_order: 7
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 7: API Integrations, Webhooks & External Service Connections

> Connect Open WebUI with external APIs, automate workflows, and extend functionality through integrations.

## REST API Integration

### Generic API Client

```python
from typing import Dict, Any, Optional, List
import aiohttp
import json
import time
from dataclasses import dataclass
from enum import Enum

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

@dataclass
class APIEndpoint:
    name: str
    url: str
    method: HTTPMethod
    headers: Dict[str, str] = None
    auth_type: str = "none"  # none, basic, bearer, api_key
    auth_config: Dict[str, Any] = None
    timeout: int = 30
    retries: int = 3

class APIClient:
    def __init__(self):
        self.endpoints: Dict[str, APIEndpoint] = {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def register_endpoint(self, endpoint: APIEndpoint):
        """Register an API endpoint."""
        self.endpoints[endpoint.name] = endpoint

    async def call_endpoint(self, endpoint_name: str, data: Dict[str, Any] = None,
                           params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Call a registered endpoint."""
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} not registered")

        endpoint = self.endpoints[endpoint_name]

        # Prepare request
        url = endpoint.url
        headers = endpoint.headers.copy() if endpoint.headers else {}
        auth_headers = self._prepare_auth_headers(endpoint)

        headers.update(auth_headers)

        # Add query parameters
        if params:
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url += "?" + query_string

        # Prepare request data
        request_data = None
        if data and endpoint.method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]:
            headers['Content-Type'] = 'application/json'
            request_data = json.dumps(data)

        # Make request with retries
        for attempt in range(endpoint.retries + 1):
            try:
                async with self.session.request(
                    method=endpoint.method.value,
                    url=url,
                    headers=headers,
                    data=request_data,
                    timeout=aiohttp.ClientTimeout(total=endpoint.timeout)
                ) as response:

                    response_data = await response.json()
                    response.headers = dict(response.headers)

                    return {
                        'status': response.status,
                        'headers': dict(response.headers),
                        'data': response_data
                    }

            except Exception as e:
                if attempt == endpoint.retries:
                    raise e
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

    def _prepare_auth_headers(self, endpoint: APIEndpoint) -> Dict[str, str]:
        """Prepare authentication headers."""
        headers = {}

        if endpoint.auth_type == "basic":
            import base64
            username = endpoint.auth_config.get('username', '')
            password = endpoint.auth_config.get('password', '')
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            headers['Authorization'] = f"Basic {credentials}"

        elif endpoint.auth_type == "bearer":
            token = endpoint.auth_config.get('token', '')
            headers['Authorization'] = f"Bearer {token}"

        elif endpoint.auth_type == "api_key":
            key_name = endpoint.auth_config.get('header_name', 'X-API-Key')
            key_value = endpoint.auth_config.get('key_value', '')
            headers[key_name] = key_value

        return headers

    def get_registered_endpoints(self) -> List[str]:
        """Get list of registered endpoint names."""
        return list(self.endpoints.keys())
```

### Popular API Integrations

```python
# Pre-configured API integrations
class APIIntegrations:
    def __init__(self, api_client: APIClient):
        self.client = api_client
        self._setup_integrations()

    def _setup_integrations(self):
        """Set up popular API integrations."""

        # GitHub API
        self.client.register_endpoint(APIEndpoint(
            name="github_user_repos",
            url="https://api.github.com/user/repos",
            method=HTTPMethod.GET,
            auth_type="bearer",
            auth_config={"token": os.getenv("GITHUB_TOKEN")},
            headers={"Accept": "application/vnd.github.v3+json"}
        ))

        # Slack API
        self.client.register_endpoint(APIEndpoint(
            name="slack_post_message",
            url="https://slack.com/api/chat.postMessage",
            method=HTTPMethod.POST,
            auth_type="bearer",
            auth_config={"token": os.getenv("SLACK_BOT_TOKEN")},
            headers={"Content-Type": "application/json"}
        ))

        # Notion API
        self.client.register_endpoint(APIEndpoint(
            name="notion_create_page",
            url="https://api.notion.com/v1/pages",
            method=HTTPMethod.POST,
            auth_type="bearer",
            auth_config={"token": os.getenv("NOTION_TOKEN")},
            headers={
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28"
            }
        ))

        # Jira API
        self.client.register_endpoint(APIEndpoint(
            name="jira_create_issue",
            url="https://your-domain.atlassian.net/rest/api/3/issue",
            method=HTTPMethod.POST,
            auth_type="basic",
            auth_config={
                "username": os.getenv("JIRA_EMAIL"),
                "password": os.getenv("JIRA_API_TOKEN")
            },
            headers={"Content-Type": "application/json"}
        ))

        # Google Calendar
        self.client.register_endpoint(APIEndpoint(
            name="google_create_event",
            url="https://www.googleapis.com/calendar/v3/calendars/primary/events",
            method=HTTPMethod.POST,
            auth_type="bearer",
            auth_config={"token": os.getenv("GOOGLE_ACCESS_TOKEN")},
            headers={"Content-Type": "application/json"}
        ))

        # Weather API (OpenWeatherMap)
        self.client.register_endpoint(APIEndpoint(
            name="weather_current",
            url="https://api.openweathermap.org/data/2.5/weather",
            method=HTTPMethod.GET,
            auth_type="api_key",
            auth_config={
                "header_name": "appid",
                "key_value": os.getenv("OPENWEATHER_API_KEY")
            }
        ))

    async def github_get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        """Get GitHub repositories for a user."""
        # Note: This would need a different endpoint or parameter handling
        return await self.client.call_endpoint("github_user_repos")

    async def slack_send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """Send a message to Slack."""
        data = {
            "channel": channel,
            "text": text
        }
        return await self.client.call_endpoint("slack_post_message", data=data)

    async def notion_create_page(self, parent_id: str, title: str, content: str) -> Dict[str, Any]:
        """Create a new page in Notion."""
        data = {
            "parent": {"database_id": parent_id},
            "properties": {
                "Name": {
                    "title": [{"text": {"content": title}}]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": content}}]
                    }
                }
            ]
        }
        return await self.client.call_endpoint("notion_create_page", data=data)

    async def jira_create_issue(self, project_key: str, summary: str, description: str) -> Dict[str, Any]:
        """Create a Jira issue."""
        data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Task"}
            }
        }
        return await self.client.call_endpoint("jira_create_issue", data=data)

    async def google_create_event(self, summary: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """Create a Google Calendar event."""
        data = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"}
        }
        return await self.client.call_endpoint("google_create_event", data=data)

    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city."""
        params = {"q": city, "units": "metric"}
        return await self.client.call_endpoint("weather_current", params=params)
```

## Webhook System

### Webhook Manager

```python
from typing import Dict, Any, Callable, List
import hmac
import hashlib
import json
import asyncio

class WebhookManager:
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key
        self.webhooks: Dict[str, Dict[str, Any]] = {}
        self.handlers: Dict[str, Callable] = {}

    def register_webhook(self, name: str, url: str, events: List[str],
                        headers: Dict[str, str] = None, secret: str = None):
        """Register a webhook endpoint."""
        self.webhooks[name] = {
            'url': url,
            'events': events,
            'headers': headers or {},
            'secret': secret or self.secret_key,
            'active': True
        }

    def unregister_webhook(self, name: str):
        """Unregister a webhook."""
        self.webhooks.pop(name, None)

    def register_handler(self, event_type: str, handler: Callable):
        """Register an event handler."""
        self.handlers[event_type] = handler

    async def trigger_event(self, event_type: str, data: Dict[str, Any]):
        """Trigger an event and send webhooks."""
        # Run local handlers first
        if event_type in self.handlers:
            try:
                await self.handlers[event_type](data)
            except Exception as e:
                print(f"Handler error for {event_type}: {e}")

        # Send webhooks
        tasks = []
        for name, webhook in self.webhooks.items():
            if event_type in webhook['events'] and webhook['active']:
                tasks.append(self._send_webhook(name, webhook, event_type, data))

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_webhook(self, name: str, webhook: Dict[str, Any],
                           event_type: str, data: Dict[str, Any]):
        """Send webhook to endpoint."""
        payload = {
            'event_type': event_type,
            'timestamp': int(time.time()),
            'data': data
        }

        headers = webhook['headers'].copy()
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = 'OpenWebUI-Webhook/1.0'

        # Add signature if secret is configured
        if webhook['secret']:
            signature = self._generate_signature(json.dumps(payload), webhook['secret'])
            headers['X-Webhook-Signature'] = signature

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    webhook['url'],
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:

                    if response.status >= 400:
                        print(f"Webhook {name} failed: {response.status}")
                    else:
                        print(f"Webhook {name} sent successfully")

        except Exception as e:
            print(f"Webhook {name} error: {e}")

    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook."""
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    def verify_webhook_signature(self, payload: str, signature: str, secret: str) -> bool:
        """Verify incoming webhook signature."""
        expected_signature = self._generate_signature(payload, secret)
        return hmac.compare_digest(expected_signature, signature)

    def list_webhooks(self) -> Dict[str, Dict[str, Any]]:
        """List all registered webhooks."""
        return self.webhooks.copy()

    def enable_webhook(self, name: str):
        """Enable a webhook."""
        if name in self.webhooks:
            self.webhooks[name]['active'] = True

    def disable_webhook(self, name: str):
        """Disable a webhook."""
        if name in self.webhooks:
            self.webhooks[name]['active'] = False
```

### Webhook Integrations

```python
# Pre-configured webhook integrations
class WebhookIntegrations:
    def __init__(self, webhook_manager: WebhookManager):
        self.webhook_manager = webhook_manager
        self._setup_integrations()

    def _setup_integrations(self):
        """Set up common webhook integrations."""

        # Slack webhook handler
        self.webhook_manager.register_handler('chat_created', self._handle_slack_notification)
        self.webhook_manager.register_handler('user_joined', self._handle_slack_notification)

        # Discord webhook handler
        self.webhook_manager.register_handler('chat_created', self._handle_discord_notification)

        # Email notification handler
        self.webhook_manager.register_handler('error_occurred', self._handle_email_notification)

    async def setup_slack_integration(self, webhook_url: str):
        """Set up Slack integration."""
        self.webhook_manager.register_webhook(
            'slack_notifications',
            webhook_url,
            ['chat_created', 'user_joined', 'error_occurred'],
            {'Content-Type': 'application/json'}
        )

    async def setup_discord_integration(self, webhook_url: str):
        """Set up Discord integration."""
        self.webhook_manager.register_webhook(
            'discord_notifications',
            webhook_url,
            ['chat_created', 'user_joined'],
            {'Content-Type': 'application/json'}
        )

    async def setup_email_integration(self, smtp_config: Dict[str, Any]):
        """Set up email integration."""
        self.email_config = smtp_config
        # Email handler is already registered

    async def _handle_slack_notification(self, data: Dict[str, Any]):
        """Handle Slack webhook notifications."""
        if 'slack_notifications' not in self.webhook_manager.webhooks:
            return

        webhook = self.webhook_manager.webhooks['slack_notifications']

        # Format message for Slack
        if data.get('event_type') == 'chat_created':
            message = {
                "text": f"New chat created by {data.get('user', 'Unknown')}",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"🎉 New chat created by *{data.get('user', 'Unknown')}*"
                        }
                    }
                ]
            }
        elif data.get('event_type') == 'user_joined':
            message = {
                "text": f"New user joined: {data.get('user', 'Unknown')}",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"👋 *{data.get('user', 'Unknown')}* joined Open WebUI"
                        }
                    }
                ]
            }
        else:
            message = {"text": f"Event: {data.get('event_type')}"}

        # Send to Slack webhook
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook['url'], json=message) as response:
                if response.status != 200:
                    print(f"Slack webhook failed: {response.status}")

    async def _handle_discord_notification(self, data: Dict[str, Any]):
        """Handle Discord webhook notifications."""
        if 'discord_notifications' not in self.webhook_manager.webhooks:
            return

        webhook = self.webhook_manager.webhooks['discord_notifications']

        # Format message for Discord
        if data.get('event_type') == 'chat_created':
            message = {
                "content": f"🎉 New chat created by {data.get('user', 'Unknown')}",
                "embeds": [
                    {
                        "title": "New Chat Created",
                        "description": f"A new conversation has been started by {data.get('user', 'Unknown')}",
                        "color": 3447003,  # Blue
                        "timestamp": data.get('timestamp')
                    }
                ]
            }
        elif data.get('event_type') == 'user_joined':
            message = {
                "content": f"👋 {data.get('user', 'Unknown')} joined Open WebUI",
                "embeds": [
                    {
                        "title": "New User",
                        "description": f"{data.get('user', 'Unknown')} has joined the platform",
                        "color": 5763719,  # Green
                        "timestamp": data.get('timestamp')
                    }
                ]
            }

        # Send to Discord webhook
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook['url'], json=message) as response:
                if response.status != 204:  # Discord returns 204 for success
                    print(f"Discord webhook failed: {response.status}")

    async def _handle_email_notification(self, data: Dict[str, Any]):
        """Handle email notifications."""
        if not hasattr(self, 'email_config'):
            return

        # This would integrate with an email service
        # Implementation depends on email provider (SendGrid, AWS SES, etc.)
        print(f"Email notification: {data.get('event_type')} - {data}")
```

## Function Calling System

### Advanced Function Manager

```python
from typing import Dict, Any, List, Callable, Awaitable
import inspect
import json

class FunctionDefinition:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any],
                 handler: Callable[..., Awaitable[Any]]):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

class FunctionCallingManager:
    def __init__(self):
        self.functions: Dict[str, FunctionDefinition] = {}
        self.call_history: List[Dict[str, Any]] = []

    def register_function(self, name: str, description: str, parameters: Dict[str, Any],
                         handler: Callable[..., Awaitable[Any]]):
        """Register a function for calling."""
        func_def = FunctionDefinition(name, description, parameters, handler)
        self.functions[name] = func_def

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get function definitions for LLM."""
        return [
            {
                'name': func.name,
                'description': func.description,
                'parameters': func.parameters
            }
            for func in self.functions.values()
        ]

    async def call_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered function."""
        if function_name not in self.functions:
            raise ValueError(f"Function {function_name} not registered")

        func_def = self.functions[function_name]

        # Log the call
        call_record = {
            'timestamp': time.time(),
            'function_name': function_name,
            'arguments': arguments
        }

        try:
            # Call the function
            result = await func_def.handler(**arguments)

            call_record['result'] = result
            call_record['success'] = True

            return result

        except Exception as e:
            call_record['error'] = str(e)
            call_record['success'] = False
            raise e

        finally:
            self.call_history.append(call_record)

    def get_call_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get function call history."""
        return self.call_history[-limit:]

    def auto_register_from_module(self, module):
        """Auto-register functions from a module with decorators."""
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, '_function_definition'):
                func_def = obj._function_definition
                self.register_function(
                    func_def['name'],
                    func_def['description'],
                    func_def['parameters'],
                    obj
                )

# Decorator for auto-registration
def openwebui_function(name: str, description: str, parameters: Dict[str, Any]):
    def decorator(func):
        func._function_definition = {
            'name': name,
            'description': description,
            'parameters': parameters
        }
        return func
    return decorator
```

### Pre-built Function Library

```python
# Utility functions for Open WebUI
class FunctionLibrary:
    def __init__(self, function_manager: FunctionCallingManager):
        self.function_manager = function_manager
        self._register_library_functions()

    def _register_library_functions(self):
        """Register common utility functions."""

        # Web search function
        self.function_manager.register_function(
            'web_search',
            'Search the web for information',
            {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'Search query'},
                    'num_results': {'type': 'integer', 'description': 'Number of results to return', 'default': 5}
                },
                'required': ['query']
            },
            self.web_search
        )

        # Calculator function
        self.function_manager.register_function(
            'calculate',
            'Perform mathematical calculations',
            {
                'type': 'object',
                'properties': {
                    'expression': {'type': 'string', 'description': 'Mathematical expression to evaluate'}
                },
                'required': ['expression']
            },
            self.calculate
        )

        # Code execution function
        self.function_manager.register_function(
            'execute_code',
            'Execute code in a safe environment',
            {
                'type': 'object',
                'properties': {
                    'language': {'type': 'string', 'description': 'Programming language'},
                    'code': {'type': 'string', 'description': 'Code to execute'}
                },
                'required': ['language', 'code']
            },
            self.execute_code
        )

        # File operations
        self.function_manager.register_function(
            'read_file',
            'Read content from a file',
            {
                'type': 'object',
                'properties': {
                    'file_path': {'type': 'string', 'description': 'Path to the file'}
                },
                'required': ['file_path']
            },
            self.read_file
        )

        # Database query function
        self.function_manager.register_function(
            'query_database',
            'Execute a database query',
            {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string', 'description': 'SQL query to execute'},
                    'database_url': {'type': 'string', 'description': 'Database connection URL'}
                },
                'required': ['query']
            },
            self.query_database
        )

    async def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Perform web search."""
        # This would integrate with a search API like SerpApi, Google Custom Search, etc.
        # Placeholder implementation
        return {
            'query': query,
            'results': [
                {'title': f'Result {i+1}', 'url': f'https://example.com/{i+1}', 'snippet': f'Search result {i+1} for {query}'}
                for i in range(num_results)
            ]
        }

    async def calculate(self, expression: str) -> Dict[str, Any]:
        """Safe mathematical calculation."""
        try:
            # Use a safe evaluation library or implement your own
            result = eval(expression, {"__builtins__": {}}, {})
            return {'result': result, 'expression': expression}
        except Exception as e:
            return {'error': str(e), 'expression': expression}

    async def execute_code(self, language: str, code: str) -> Dict[str, Any]:
        """Execute code in specified language."""
        # This should use a secure code execution service
        # Placeholder - DO NOT use eval in production!
        if language.lower() == 'python':
            try:
                # This is VERY unsafe - use a proper sandbox in production
                result = eval(code, {"__builtins__": {}}, {})
                return {'output': str(result), 'language': language}
            except Exception as e:
                return {'error': str(e), 'language': language}
        else:
            return {'error': f'Language {language} not supported', 'language': language}

    async def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read file content (with security checks)."""
        # Implement proper security checks and sandboxing
        try:
            # Check if file path is allowed
            if not self._is_path_allowed(file_path):
                return {'error': 'Access denied', 'file_path': file_path}

            with open(file_path, 'r') as f:
                content = f.read()

            return {
                'content': content,
                'file_path': file_path,
                'size': len(content)
            }
        except Exception as e:
            return {'error': str(e), 'file_path': file_path}

    async def query_database(self, query: str, database_url: str = None) -> Dict[str, Any]:
        """Execute database query."""
        # This should use connection pooling and proper security
        try:
            # Placeholder - implement proper database connection
            return {'error': 'Database integration not implemented', 'query': query}
        except Exception as e:
            return {'error': str(e), 'query': query}

    def _is_path_allowed(self, file_path: str) -> bool:
        """Check if file path is allowed to be read."""
        # Implement proper path validation and sandboxing
        import os.path
        abs_path = os.path.abspath(file_path)

        # Only allow files in specific directories
        allowed_dirs = ['/tmp', '/var/data']  # Configure as needed

        return any(abs_path.startswith(allowed_dir) for allowed_dir in allowed_dirs)
```

## Workflow Automation

### Zapier Integration

```python
class ZapierIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.zapier.com/v1"

    async def trigger_zap(self, zap_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a Zapier zap."""
        url = f"{self.base_url}/zaps/{zap_id}/execute"

        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            async with session.post(url, json=data, headers=headers) as response:
                return await response.json()

    async def list_zaps(self) -> List[Dict[str, Any]]:
        """List available zaps."""
        url = f"{self.base_url}/zaps"

        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {self.api_key}'}

            async with session.get(url, headers=headers) as response:
                return await response.json()
```

### IFTTT Integration

```python
class IFTTTIntegration:
    def __init__(self, key: str):
        self.key = key
        self.base_url = "https://maker.ifttt.com/trigger"

    async def trigger_event(self, event_name: str, data: Dict[str, Any] = None) -> bool:
        """Trigger an IFTTT event."""
        url = f"{self.base_url}/{event_name}/with/key/{self.key}"

        payload = {}
        if data:
            # IFTTT supports up to 3 values
            for i, (key, value) in enumerate(data.items()):
                if i < 3:
                    payload[f"value{i+1}"] = str(value)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return response.status == 200
```

This comprehensive integration system allows Open WebUI to connect with external services, automate workflows, and extend its functionality through APIs, webhooks, and function calling. The modular design makes it easy to add new integrations as needed. 🚀