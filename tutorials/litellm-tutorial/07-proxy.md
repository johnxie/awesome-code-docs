---
layout: default
title: "LiteLLM Tutorial - Chapter 7: LiteLLM Proxy"
nav_order: 7
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 7: LiteLLM Proxy

Welcome to **Chapter 7: LiteLLM Proxy**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deploy a centralized OpenAI-compatible proxy server that routes requests to multiple LLM providers with unified authentication, rate limiting, and cost tracking.

## Overview

The LiteLLM Proxy provides a single endpoint that accepts OpenAI API calls and routes them to any configured LLM provider. This enables easy integration with existing applications while providing enterprise features like authentication, rate limiting, and cost tracking.

## Quick Start Proxy

Launch a basic proxy server:

```bash
# Install proxy dependencies
pip install litellm[proxy]

# Set environment variables
export OPENAI_API_KEY="sk-your-key"
export ANTHROPIC_API_KEY="sk-ant-your-key"

# Start proxy server
litellm --config config.yaml --port 8000
```

## Configuration File

Create a comprehensive proxy configuration:

```yaml
# config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-3
    litellm_params:
      model: claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt-3.5-turbo
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

general_settings:
  database_url: "sqlite:///litellm.db"  # For cost tracking
  master_key: "sk-1234"  # Master API key for admin access

# Optional: Rate limiting
rate_limit_config:
  redis_host: localhost
  redis_port: 6379
```

## Using the Proxy

The proxy accepts standard OpenAI API calls:

```python
import openai

# Point to your LiteLLM proxy
client = openai.OpenAI(
    api_key="your-proxy-key",  # Key from proxy config
    base_url="http://localhost:8000"  # Your proxy URL
)

# Use any configured model
response = client.chat.completions.create(
    model="gpt-4",  # Routes to OpenAI GPT-4
    messages=[{"role": "user", "content": "Hello!"}]
)

response = client.chat.completions.create(
    model="claude-3",  # Routes to Anthropic Claude
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Authentication

Configure authentication for different users:

```yaml
# config.yaml with user authentication
general_settings:
  database_url: "sqlite:///litellm.db"

# User API keys
user_config:
  - user_id: "user1"
    user_email: "user1@example.com"
    user_role: "app_user"
    max_budget: 100.0
    models: ["gpt-3.5-turbo", "claude-3-haiku-20240307"]

  - user_id: "user2"
    user_email: "user2@example.com"
    user_role: "app_user"
    max_budget: 50.0
    models: ["gpt-3.5-turbo"]

# Virtual keys (recommended for production)
general_settings:
  database_url: "postgresql://user:pass@host:5432/litellm"

# Create virtual keys for users
litellm --config config.yaml --generate_key --user_id user1
# Returns: sk-user1-key-12345

# Use virtual key
client = openai.OpenAI(
    api_key="sk-user1-key-12345",
    base_url="http://localhost:8000"
)
```

## Rate Limiting

Configure rate limits per user or globally:

```yaml
# config.yaml
rate_limit_config:
  redis_host: localhost
  redis_port: 6379

user_config:
  - user_id: "premium_user"
    user_email: "premium@example.com"
    user_role: "app_user"
    models: ["gpt-4", "claude-3"]
    rpm_limit: 100  # Requests per minute
    tpm_limit: 100000  # Tokens per minute
    max_budget: 500.0

  - user_id: "basic_user"
    user_email: "basic@example.com"
    user_role: "app_user"
    models: ["gpt-3.5-turbo"]
    rpm_limit: 20
    tpm_limit: 10000
    max_budget: 10.0

# Global rate limits
general_settings:
  global_max_rpm: 1000
  global_max_tpm: 1000000
```

## Cost Tracking

Enable detailed cost tracking and budgets:

```yaml
# config.yaml
general_settings:
  database_url: "sqlite:///costs.db"

user_config:
  - user_id: "team_a"
    user_email: "team_a@example.com"
    user_role: "app_user"
    max_budget: 200.0  # Monthly budget
    models: ["gpt-4", "gpt-3.5-turbo", "claude-3"]
    budget_duration: "30d"  # Reset every 30 days

# Enable cost tracking endpoints
litellm_settings:
  cost_tracking: true
```

Access cost data via API:

```python
import requests

# Get user spending
response = requests.get(
    "http://localhost:8000/user/spend",
    headers={"Authorization": "Bearer sk-user1-key"}
)

spend_data = response.json()
print(f"User spent: ${spend_data['total_spend']}")
```

## Model Fallbacks

Configure automatic fallbacks in the proxy:

```yaml
# config.yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      mode: fallback  # Enable fallback mode

  - model_name: gpt-4-fallback
    litellm_params:
      model: claude-3-opus-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
    model_info:
      mode: fallback

# Fallback routing
fallback_mapping:
  gpt-4: ["gpt-4-fallback"]  # If gpt-4 fails, try claude-3

general_settings:
  database_url: "sqlite:///litellm.db"
```

## Load Balancing

Distribute requests across multiple instances:

```yaml
# config.yaml with load balancing
model_list:
  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY_1
    model_info:
      mode: loadbalance

  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY_2
    model_info:
      mode: loadbalance

  - model_name: gpt-4
    litellm_params:
      model: gpt-4
      api_key: os.environ/OPENAI_API_KEY_3
    model_info:
      mode: loadbalance
```

## Caching

Enable response caching to reduce costs:

```yaml
# config.yaml
cache_settings:
  type: redis
  host: localhost
  port: 6379
  password: ""  # Optional

# Cache configuration
litellm_settings:
  cache: true
  cache_ttl: 3600  # Cache for 1 hour

# Semantic caching (cache similar requests)
cache_settings:
  type: redis
  host: localhost
  port: 6379
  similarity_threshold: 0.8  # Cache if similarity > 80%
```

## Logging and Monitoring

Configure comprehensive logging:

```yaml
# config.yaml
general_settings:
  database_url: "sqlite:///litellm.db"
  log_level: "INFO"

# Export logs to external systems
logging:
  - type: "datadog"
    datadog_api_key: "your-datadog-key"
    datadog_site: "datadoghq.com"

  - type: "sentry"
    dsn: "your-sentry-dsn"

  - type: "langsmith"
    project_name: "litellm-proxy"
    api_key: "your-langsmith-key"
```

## Deploying to Production

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["litellm", "--config", "config.yaml", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  litellm-proxy:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./litellm.db:/app/litellm.db
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:  # Optional, for production
    image: postgres:15
    environment:
      - POSTGRES_DB=litellm
      - POSTGRES_USER=litellm
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: litellm-proxy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: litellm-proxy
  template:
    metadata:
      labels:
        app: litellm-proxy
    spec:
      containers:
      - name: litellm
        image: your-registry/litellm:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: litellm-config
        - secretRef:
            name: litellm-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: litellm-service
spec:
  selector:
    app: litellm-proxy
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: litellm-config
data:
  config.yaml: |
    model_list:
      - model_name: gpt-4
        litellm_params:
          model: gpt-4
          api_key: os.environ/OPENAI_API_KEY
    general_settings:
      database_url: "postgresql://user:pass@postgres:5432/litellm"
```

## API Endpoints

The proxy provides additional endpoints beyond OpenAI compatibility:

```python
# Health check
response = requests.get("http://localhost:8000/health")

# List available models
response = requests.get("http://localhost:8000/v1/models")

# Get user spending
response = requests.get(
    "http://localhost:8000/user/spend",
    headers={"Authorization": "Bearer sk-user-key"}
)

# Admin endpoints (require master key)
response = requests.get(
    "http://localhost:8000/global/spend",
    headers={"Authorization": "Bearer sk-master-key"}
)

# Reset budget
response = requests.post(
    "http://localhost:8000/user/reset_budget",
    headers={"Authorization": "Bearer sk-master-key"},
    json={"user_id": "user123"}
)
```

## Integration Examples

### OpenAI SDK Integration

```python
import openai

# Drop-in replacement for OpenAI
client = openai.OpenAI(
    api_key="sk-your-proxy-key",
    base_url="http://localhost:8000"  # Your proxy URL
)

# All OpenAI code works unchanged
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### LangChain Integration

```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Use proxy as drop-in replacement
llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key="sk-your-proxy-key",
    openai_api_base="http://localhost:8000",
)

chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms."
    )
)

result = chain.run(topic="quantum computing")
```

### LlamaIndex Integration

```python
from llama_index.llms import OpenAI

# Configure to use proxy
llm = OpenAI(
    model="gpt-4",
    api_key="sk-your-proxy-key",
    api_base="http://localhost:8000",
)

from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("What is the meaning of life?")
```

## Security Best Practices

1. **Use HTTPS**: Always deploy behind SSL/TLS termination
2. **API Key Management**: Use virtual keys, rotate regularly
3. **Network Security**: Restrict access with firewalls and VPCs
4. **Rate Limiting**: Implement appropriate limits to prevent abuse
5. **Monitoring**: Log all requests and monitor for anomalies
6. **Data Encryption**: Encrypt sensitive data at rest and in transit
7. **Access Control**: Implement role-based access control

## Scaling Considerations

1. **Horizontal Scaling**: Run multiple proxy instances behind a load balancer
2. **Database Scaling**: Use managed PostgreSQL for production
3. **Redis Clustering**: Use Redis cluster for high availability
4. **CDN Integration**: Use CDN for global distribution
5. **Auto-scaling**: Configure Kubernetes HPA based on CPU/memory

## Troubleshooting

Common issues and solutions:

- **Connection Refused**: Check if proxy is running and port is correct
- **Authentication Failed**: Verify API keys are properly configured
- **Rate Limited**: Check rate limit configuration and usage
- **Model Not Found**: Ensure model is in `model_list` configuration
- **Database Errors**: Check database connection and permissions

## Monitoring and Alerting

Set up monitoring for production deployments:

```yaml
# Prometheus metrics
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    scrape_configs:
    - job_name: 'litellm-proxy'
      static_configs:
      - targets: ['litellm-service:8000']
      metrics_path: '/metrics'
```

The LiteLLM Proxy transforms how you deploy and manage LLM APIs, providing enterprise-grade features while maintaining OpenAI compatibility. It's the perfect solution for organizations wanting to standardize their AI infrastructure across multiple providers.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `litellm`, `config`, `proxy` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: LiteLLM Proxy` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `yaml`, `model`, `localhost` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: LiteLLM Proxy` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `litellm`.
2. **Input normalization**: shape incoming data so `config` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `proxy`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
  Why it matters: authoritative reference on `LiteLLM Repository` (github.com).
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
  Why it matters: authoritative reference on `LiteLLM Releases` (github.com).
- [LiteLLM Docs](https://docs.litellm.ai/)
  Why it matters: authoritative reference on `LiteLLM Docs` (docs.litellm.ai).

Suggested trace strategy:
- search upstream code for `litellm` and `config` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Cost Tracking](06-cost-tracking.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
