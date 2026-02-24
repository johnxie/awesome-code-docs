---
layout: default
title: "Chapter 6: Deployment Strategies"
parent: "BentoML Tutorial"
nav_order: 6
---

# Chapter 6: Deployment Strategies

Welcome to **Chapter 6: Deployment Strategies**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers various deployment strategies for BentoML services, from simple Docker deployments to complex Kubernetes orchestrations and cloud platform integrations.

## Docker Deployment

### Basic Docker Deployment

```bash
# Build BentoML service into Docker image
bentoml build MyMLService:latest

# Or build from bento.yaml
bentoml build

# List built bentos
bentoml list

# Run the bento
bentoml serve my-ml-service:latest --port 3000
```

### Custom Dockerfile

```dockerfile
# Dockerfile for BentoML service
FROM bentoml/bento-server:latest

# Copy custom requirements
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Copy model files
COPY models/ /opt/models/

# Set environment variables
ENV MODEL_PATH=/opt/models
ENV WORKERS=4

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Run the service
CMD ["bentoml", "serve", "MyMLService:latest", "--port", "3000"]
```

### Docker Compose Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  ml-service:
    build: .
    ports:
      - "3000:3000"
    environment:
      - BENTOML_PORT=3000
      - WORKERS=4
    volumes:
      - ./models:/opt/models:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - ml-service
    restart: unless-stopped
```

## Kubernetes Deployment

### Basic Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bentoml-service
  template:
    metadata:
      labels:
        app: bentoml-service
    spec:
      containers:
      - name: bentoml
        image: my-bento:latest
        ports:
        - containerPort: 3000
        env:
        - name: BENTOML_PORT
          value: "3000"
        - name: WORKERS
          value: "4"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Kubernetes Service

```yaml
# k8s-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bentoml-service
spec:
  selector:
    app: bentoml-service
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

### Horizontal Pod Autoscaler

```yaml
# k8s-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bentoml-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bentoml-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Cloud Platform Deployments

### AWS Deployment

```python
# deploy_aws.py
import boto3
import bentoml

def deploy_to_aws():
    # Build and push Docker image
    bentoml.build("MyMLService:latest")
    image_uri = push_to_ecr("my-bento:latest")

    # Create ECS service
    ecs = boto3.client('ecs')

    ecs.create_service(
        cluster='ml-cluster',
        serviceName='bentoml-service',
        taskDefinition=create_task_definition(image_uri),
        desiredCount=3,
        loadBalancers=[{
            'targetGroupArn': 'arn:aws:elasticloadbalancing:...',
            'containerName': 'bentoml',
            'containerPort': 3000
        }]
    )

def push_to_ecr(image_name):
    # Push image to Amazon ECR
    ecr = boto3.client('ecr')
    # ... ECR push logic
    return image_uri
```

### Google Cloud Deployment

```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: bentoml-service
spec:
  template:
    spec:
      containers:
      - image: gcr.io/my-project/my-bento:latest
        ports:
        - containerPort: 3000
        env:
        - name: PORT
          value: "3000"
        resources:
          limits:
            cpu: 1000m
            memory: 2Gi
```

### Azure Deployment

```json
// azure-deploy.json
{
  "type": "Microsoft.ContainerInstance/containerGroups",
  "apiVersion": "2021-07-01",
  "name": "bentoml-container",
  "location": "eastus",
  "properties": {
    "containers": [{
      "name": "bentoml",
      "properties": {
        "image": "myregistry.azurecr.io/my-bento:latest",
        "ports": [{"port": 3000}],
        "resources": {
          "requests": {
            "cpu": 1,
            "memoryInGB": 2
          }
        }
      }
    }],
    "ipAddress": {
      "type": "Public",
      "ports": [{
        "protocol": "tcp",
        "port": 3000
      }]
    }
  }
}
```

## Advanced Deployment Patterns

### Blue-Green Deployment

```bash
# Blue-green deployment script
#!/bin/bash

# Deploy new version
kubectl apply -f k8s-deployment-green.yaml

# Wait for green deployment to be ready
kubectl wait --for=condition=available --timeout=300s deployment/bentoml-green

# Switch traffic to green
kubectl patch service bentoml-service -p '{"spec":{"selector":{"version":"green"}}}'

# Keep blue deployment for rollback
echo "Traffic switched to green deployment"

# Optional: Remove blue deployment after successful deployment
# kubectl delete deployment bentoml-blue
```

### Canary Deployment

```yaml
# k8s-canary.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: bentoml-canary
spec:
  http:
  - route:
    - destination:
        host: bentoml-service
        subset: v1
      weight: 90
    - destination:
        host: bentoml-service
        subset: v2
      weight: 10
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: bentoml-canary
spec:
  host: bentoml-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Multi-Region Deployment

```yaml
# k8s-multi-region.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-us-east
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: bentoml
        image: my-bento:latest
        env:
        - name: REGION
          value: "us-east"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bentoml-us-west
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: bentoml
        image: my-bento:latest
        env:
        - name: REGION
          value: "us-west"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: bentoml-global
spec:
  http:
  - route:
    - destination:
        host: bentoml-us-east
      weight: 60
    - destination:
        host: bentoml-us-west
      weight: 40
```

## Monitoring and Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import bentoml

# Define metrics
prediction_counter = Counter('bentoml_predictions_total', 'Total predictions')
prediction_duration = Histogram('bentoml_prediction_duration_seconds', 'Prediction duration')
active_requests = Gauge('bentoml_active_requests', 'Active requests')

@bentoml.service
class MonitoredService:
    @bentoml.api
    def predict(self, input_data):
        active_requests.inc()

        with prediction_duration.time():
            prediction_counter.inc()
            result = self.model.predict(input_data)

        active_requests.dec()
        return result
```

### Logging Configuration

```python
import logging
import sys

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bentoml.log')
    ]
)

# Add request logging middleware
@bentoml.service
class LoggedService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @bentoml.api
    def predict(self, input_data):
        self.logger.info(f"Prediction request: {len(input_data)} samples")

        try:
            result = self.model.predict(input_data)
            self.logger.info("Prediction completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Prediction failed: {str(e)}")
            raise
```

## Security Best Practices

### API Authentication

```python
import jwt
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = bentoml.context.request.headers.get('Authorization')

        if not auth_header:
            return {"error": "Authorization required"}, 401

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret-key', algorithms=['HS256'])
            bentoml.context.user = payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        return func(*args, **kwargs)
    return wrapper

@bentoml.service
class SecureService:
    @bentoml.api
    @require_auth
    def predict(self, input_data):
        user = bentoml.context.user
        return self.model.predict(input_data)
```

### Rate Limiting

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.user_requests = defaultdict(list)

    def is_allowed(self, user_id):
        now = time.time()
        user_reqs = self.user_requests[user_id]

        # Clean old requests
        user_reqs[:] = [req for req in user_reqs if now - req < 60]

        if len(user_reqs) >= self.requests_per_minute:
            return False

        user_reqs.append(now)
        return True

@bentoml.service
class RateLimitedService:
    def __init__(self):
        self.rate_limiter = RateLimiter()

    @bentoml.api
    def predict(self, input_data):
        user_id = bentoml.context.user.get('id', 'anonymous')

        if not self.rate_limiter.is_allowed(user_id):
            return {"error": "Rate limit exceeded"}, 429

        return self.model.predict(input_data)
```

## Performance Optimization

### Caching Strategies

```python
from functools import lru_cache
import hashlib

@bentoml.service
class CachedService:
    @lru_cache(maxsize=1000)
    def cached_predict(self, data_hash, input_data):
        return self.model.predict(input_data)

    @bentoml.api
    def predict_with_cache(self, input_data):
        # Create hash for caching
        data_str = str(input_data)
        data_hash = hashlib.md5(data_str.encode()).hexdigest()

        return self.cached_predict(data_hash, input_data)
```

### Async Processing

```python
import asyncio

@bentoml.service
class AsyncService:
    @bentoml.api
    async def predict_async(self, input_data):
        # Simulate async processing
        await asyncio.sleep(0.1)
        return self.model.predict(input_data)

    @bentoml.api
    async def batch_predict_async(self, input_data):
        # Process in parallel
        tasks = []
        batch_size = 10

        for i in range(0, len(input_data), batch_size):
            batch = input_data[i:i + batch_size]
            task = asyncio.create_task(self.process_batch(batch))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return [item for sublist in results for item in sublist]

    async def process_batch(self, batch):
        await asyncio.sleep(0.05)  # Simulate processing
        return self.model.predict(batch)
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **Docker Deployment** - Containerizing and running BentoML services
2. **Kubernetes Orchestration** - Scaling services with K8s deployments
3. **Cloud Platform Integration** - AWS, GCP, and Azure deployments
4. **Advanced Deployment Patterns** - Blue-green, canary, and multi-region deployments
5. **Monitoring & Observability** - Prometheus metrics and logging
6. **Security Best Practices** - Authentication, rate limiting, and access control
7. **Performance Optimization** - Caching and async processing strategies

## Next Steps

Now that you understand deployment strategies, let's explore monitoring and observability for your BentoML services. In [Chapter 7: Monitoring & Observability](07-monitoring-observability.md), we'll dive into comprehensive monitoring, logging, and performance tracking.

---

**Practice what you've learned:**
1. Deploy a BentoML service to Docker and Kubernetes
2. Set up monitoring and alerting for your deployments
3. Implement authentication and rate limiting
4. Configure auto-scaling for high-traffic scenarios

*What's your preferred deployment strategy for ML services?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `bentoml`, `self`, `service` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Deployment Strategies` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `input_data`, `spec` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Deployment Strategies` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `bentoml`.
2. **Input normalization**: shape incoming data so `self` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `service`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/bentoml/BentoML)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `bentoml` and `self` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Testing & Validation](05-testing-validation.md)
- [Next Chapter: Chapter 7: Monitoring & Observability](07-monitoring-observability.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
