---
layout: default
title: "Letta Tutorial - Chapter 7: REST API"
nav_order: 7
has_children: false
parent: Letta Tutorial
---

# Chapter 7: REST API

> Deploy Letta agents as REST API services for integration with applications.

## Overview

Letta provides a REST API for programmatic access to agents. This chapter covers API endpoints, authentication, deployment options, and building applications that integrate with Letta agents.

## Starting the API Server

Run Letta as a REST service:

```bash
# Start API server on default port 8283
letta server

# Or specify custom port
letta server --port 8000

# Enable CORS for web applications
letta server --cors
```

The API will be available at `http://localhost:8283`.

## API Endpoints

### Agent Management

```python
import requests

BASE_URL = "http://localhost:8283"

# List all agents
response = requests.get(f"{BASE_URL}/agents")
agents = response.json()

# Get specific agent
response = requests.get(f"{BASE_URL}/agents/sam")
agent = response.json()

# Create new agent
agent_data = {
    "name": "api-agent",
    "persona": "You are a helpful API assistant.",
    "model": "gpt-4o-mini"
}
response = requests.post(f"{BASE_URL}/agents", json=agent_data)
new_agent = response.json()
```

### Conversations

```python
# List conversations for an agent
response = requests.get(f"{BASE_URL}/agents/sam/conversations")
conversations = response.json()

# Get conversation messages
response = requests.get(f"{BASE_URL}/agents/sam/conversations/{conversation_id}/messages")
messages = response.json()

# Create new conversation
response = requests.post(f"{BASE_URL}/agents/sam/conversations")
conversation = response.json()
```

### Sending Messages

```python
# Send message to agent
message_data = {
    "message": "Hello, how are you?",
    "conversation_id": conversation_id  # optional
}

response = requests.post(
    f"{BASE_URL}/agents/sam/messages",
    json=message_data
)

agent_response = response.json()
print(agent_response["content"])
```

## Python Client Library

Use the official Python client for easier integration:

```python
from letta import create_client

# Connect to remote Letta server
client = create_client(base_url="http://localhost:8283")

# All operations work the same as local
agents = client.list_agents()
response = client.send_message("sam", "Hello from Python client!")
```

## Authentication

Secure your API endpoints:

```bash
# Enable authentication
letta server --auth

# Set API key
export LETTA_API_KEY="your-secret-key"
```

Include API key in requests:

```python
headers = {"Authorization": "Bearer your-secret-key"}

response = requests.get(
    f"{BASE_URL}/agents",
    headers=headers
)
```

## Web Application Integration

Build web apps that interact with Letta agents:

```javascript
// frontend.js - React/Vue/etc.
async function sendToAgent(message) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    return data.response;
}

// backend.js - Express/FastAPI/etc.
app.post('/api/chat', async (req, res) => {
    try {
        const response = await fetch('http://localhost:8283/agents/sam/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer your-letta-api-key'
            },
            body: JSON.stringify({
                message: req.body.message
            })
        });

        const data = await response.json();
        res.json({ response: data.content });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
```

## Streaming Responses

Handle streaming for real-time responses:

```python
import json

def stream_agent_response(agent_name, message):
    """Stream agent response in real-time."""
    response = requests.post(
        f"{BASE_URL}/agents/{agent_name}/messages",
        json={"message": message, "stream": True},
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))
            if 'content' in data:
                yield data['content']

# Usage
for chunk in stream_agent_response("sam", "Tell me a story"):
    print(chunk, end="", flush=True)
```

## Batch Processing

Process multiple messages efficiently:

```python
def batch_process(agent_name, messages):
    """Process multiple messages in batch."""
    batch_data = {
        "messages": messages,
        "batch_size": len(messages)
    }

    response = requests.post(
        f"{BASE_URL}/agents/{agent_name}/batch",
        json=batch_data
    )

    return response.json()

# Usage
messages = [
    "Hello",
    "How are you?",
    "What's your name?"
]

results = batch_process("sam", messages)
for i, result in enumerate(results):
    print(f"Message {i+1}: {result['content']}")
```

## Error Handling

Implement robust error handling:

```python
def safe_send_message(agent_name, message, retries=3):
    """Send message with error handling and retries."""
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{BASE_URL}/agents/{agent_name}/messages",
                json={"message": message},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                raise Exception(f"Failed to send message after {retries} attempts: {str(e)}")
            time.sleep(1)

    raise Exception("Max retries exceeded")

# Usage
try:
    response = safe_send_message("sam", "Hello")
    print(response["content"])
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limiting

Handle API rate limits:

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def rate_limited_send(agent_name, message):
    """Send message with rate limiting."""
    return requests.post(
        f"{BASE_URL}/agents/{agent_name}/messages",
        json={"message": message}
    )

# Usage
response = rate_limited_send("sam", "Hello")
```

## Caching Layer

Add caching for frequently asked questions:

```python
import redis
from hashlib import md5

redis_client = redis.Redis(host='localhost', port=6379)

def send_with_cache(agent_name, message, ttl=3600):
    """Send message with caching."""
    # Create cache key
    key = md5(f"{agent_name}:{message}".encode()).hexdigest()

    # Check cache
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    # Send to agent
    response = requests.post(
        f"{BASE_URL}/agents/{agent_name}/messages",
        json={"message": message}
    )

    result = response.json()

    # Cache result
    redis_client.setex(key, ttl, json.dumps(result))

    return result
```

## Monitoring and Logging

Add monitoring to API calls:

```python
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitored_send_message(agent_name, message):
    """Send message with monitoring."""
    start_time = time.time()

    try:
        response = requests.post(
            f"{BASE_URL}/agents/{agent_name}/messages",
            json={"message": message}
        )

        duration = time.time() - start_time

        logger.info(f"Agent {agent_name} response time: {duration:.2f}s")

        if response.status_code != 200:
            logger.error(f"Agent {agent_name} error: {response.status_code}")

        return response.json()

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Agent {agent_name} failed after {duration:.2f}s: {str(e)}")
        raise
```

## Load Balancing

Deploy multiple Letta instances:

```yaml
# docker-compose.yml with load balancer
version: '3.8'
services:
  letta1:
    image: letta/letta:latest
    environment:
      - LETTA_API_KEY=${API_KEY}

  letta2:
    image: letta/letta:latest
    environment:
      - LETTA_API_KEY=${API_KEY}

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - letta1
      - letta2

# nginx.conf
events {}
http {
    upstream letta_backend {
        server letta1:8283;
        server letta2:8283;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://letta_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## API Documentation

Generate API documentation:

```bash
# Generate OpenAPI spec
letta server --docs

# Access docs at http://localhost:8283/docs
```

The API docs will show all endpoints, parameters, and response schemas.

## Security Best Practices

1. **HTTPS Only**: Always use HTTPS in production
2. **API Keys**: Use strong, rotated API keys
3. **Input Validation**: Validate all inputs server-side
4. **Rate Limiting**: Implement appropriate rate limits
5. **Monitoring**: Log all API access and errors
6. **CORS**: Configure CORS properly for web apps
7. **Timeouts**: Set reasonable timeouts for all requests

## Example Application

Complete chat application:

```python
# app.py - Flask example
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
LETTA_URL = "http://localhost:8283"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    agent = data.get('agent', 'sam')

    try:
        response = requests.post(
            f"{LETTA_URL}/agents/{agent}/messages",
            json={"message": message},
            timeout=30
        )

        if response.status_code == 200:
            return jsonify({"response": response.json()["content"]})
        else:
            return jsonify({"error": "Agent error"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

Next: Production deployment and scaling strategies. 