---
layout: default
title: "Chapter 7: Monitoring & Observability"
parent: "BentoML Tutorial"
nav_order: 7
---

# Chapter 7: Monitoring & Observability

Welcome to **Chapter 7: Monitoring & Observability**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on comprehensive monitoring and observability for BentoML services. We'll explore metrics collection, logging strategies, performance monitoring, and alerting systems to ensure your ML services run reliably in production.

## Metrics Collection

### Basic Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import bentoml

# Define metrics
prediction_counter = Counter(
    'bentoml_predictions_total',
    'Total number of predictions',
    ['model_name', 'endpoint']
)

prediction_duration = Histogram(
    'bentoml_prediction_duration_seconds',
    'Prediction duration in seconds',
    ['model_name', 'endpoint']
)

active_requests = Gauge(
    'bentoml_active_requests',
    'Number of active requests',
    ['model_name']
)

model_accuracy = Gauge(
    'bentoml_model_accuracy',
    'Current model accuracy',
    ['model_name', 'version']
)

@bentoml.service
class MonitoredService:
    def __init__(self):
        self.model_name = "my_model"

    @bentoml.api
    def predict(self, input_data):
        active_requests.labels(model_name=self.model_name).inc()

        with prediction_duration.labels(
            model_name=self.model_name,
            endpoint="predict"
        ).time():
            prediction_counter.labels(
                model_name=self.model_name,
                endpoint="predict"
            ).inc()

            result = self.model.predict(input_data)

        active_requests.labels(model_name=self.model_name).dec()

        return {"prediction": result.tolist()}
```

### Custom Metrics

```python
from prometheus_client import Histogram, Counter
import numpy as np

class ModelMetrics:
    def __init__(self, model_name):
        self.model_name = model_name

        # Prediction quality metrics
        self.prediction_confidence = Histogram(
            'bentoml_prediction_confidence',
            'Prediction confidence distribution',
            ['model_name'],
            buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        )

        self.outlier_predictions = Counter(
            'bentoml_outlier_predictions_total',
            'Number of outlier predictions',
            ['model_name']
        )

    def record_prediction(self, prediction, confidence):
        """Record prediction metrics"""
        self.prediction_confidence.labels(
            model_name=self.model_name
        ).observe(confidence)

        # Detect outliers (low confidence predictions)
        if confidence < 0.3:
            self.outlier_predictions.labels(
                model_name=self.model_name
            ).inc()

@bentoml.service
class AdvancedMonitoredService:
    def __init__(self):
        self.metrics = ModelMetrics("advanced_model")

    @bentoml.api
    def predict_with_metrics(self, input_data):
        predictions = self.model.predict(input_data)
        confidence_scores = self.model.predict_proba(input_data).max(axis=1)

        # Record metrics for each prediction
        for conf in confidence_scores:
            self.metrics.record_prediction(None, conf)

        return {
            "predictions": predictions.tolist(),
            "confidence_scores": confidence_scores.tolist()
        }
```

## Logging Strategies

### Structured Logging

```python
import logging
import json
import sys
from datetime import datetime

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log_request(self, request_id, endpoint, input_shape, user_id=None):
        """Log incoming request"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "endpoint": endpoint,
            "input_shape": input_shape,
            "user_id": user_id,
            "event": "request_started"
        }

        self.logger.info(json.dumps(log_data))

    def log_response(self, request_id, response_time, status="success"):
        """Log response"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "response_time": response_time,
            "status": status,
            "event": "request_completed"
        }

        self.logger.info(json.dumps(log_data))

    def log_error(self, request_id, error_type, error_message):
        """Log error"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "error_type": error_type,
            "error_message": error_message,
            "event": "request_error"
        }

        self.logger.error(json.dumps(log_data))

@bentoml.service
class LoggedService:
    def __init__(self):
        self.logger = StructuredLogger("BentoMLService")

    @bentoml.api
    def predict_with_logging(self, input_data):
        import uuid
        import time

        request_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            self.logger.log_request(
                request_id,
                "predict",
                input_data.shape if hasattr(input_data, 'shape') else len(input_data)
            )

            result = self.model.predict(input_data)

            response_time = time.time() - start_time
            self.logger.log_response(request_id, response_time)

            return {"prediction": result.tolist()}

        except Exception as e:
            response_time = time.time() - start_time
            self.logger.log_error(request_id, type(e).__name__, str(e))
            raise
```

### Log Aggregation

```python
import logging
from logging.handlers import RotatingFileHandler
import os

class LogAggregator:
    def __init__(self, log_dir="./logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Configure main logger
        self.logger = logging.getLogger("BentoML")
        self.logger.setLevel(logging.INFO)

        # File handler with rotation
        log_file = os.path.join(log_dir, "bentoml.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_request_logger(self, request_id):
        """Get logger for specific request"""
        return self.logger.getChild(f"request.{request_id}")

@bentoml.service
class AggregatedLoggingService:
    def __init__(self):
        self.log_aggregator = LogAggregator()

    @bentoml.api
    def predict_with_aggregation(self, input_data):
        import uuid

        request_id = str(uuid.uuid4())
        request_logger = self.log_aggregator.get_request_logger(request_id)

        request_logger.info("Starting prediction")
        request_logger.info(f"Input shape: {input_data.shape}")

        result = self.model.predict(input_data)

        request_logger.info("Prediction completed")
        request_logger.info(f"Output shape: {result.shape}")

        return {"prediction": result.tolist()}
```

## Performance Monitoring

### Response Time Monitoring

```python
import time
from collections import deque
import statistics

class PerformanceMonitor:
    def __init__(self, window_size=100):
        self.response_times = deque(maxlen=window_size)
        self.request_count = 0
        self.error_count = 0

    def record_request(self, response_time, success=True):
        """Record request metrics"""
        self.response_times.append(response_time)
        self.request_count += 1

        if not success:
            self.error_count += 1

    def get_metrics(self):
        """Get current performance metrics"""
        if not self.response_times:
            return {
                "avg_response_time": 0,
                "p95_response_time": 0,
                "p99_response_time": 0,
                "error_rate": 0,
                "total_requests": 0
            }

        return {
            "avg_response_time": statistics.mean(self.response_times),
            "p95_response_time": statistics.quantiles(self.response_times, n=20)[18],  # 95th percentile
            "p99_response_time": statistics.quantiles(self.response_times, n=100)[98],  # 99th percentile
            "error_rate": self.error_count / self.request_count if self.request_count > 0 else 0,
            "total_requests": self.request_count
        }

@bentoml.service
class PerformanceMonitoredService:
    def __init__(self):
        self.monitor = PerformanceMonitor()

    @bentoml.api
    def predict_with_monitoring(self, input_data):
        start_time = time.time()

        try:
            result = self.model.predict(input_data)
            response_time = time.time() - start_time

            self.monitor.record_request(response_time, success=True)

            return {"prediction": result.tolist()}

        except Exception as e:
            response_time = time.time() - start_time
            self.monitor.record_request(response_time, success=False)
            raise

    @bentoml.api
    def get_performance_metrics(self):
        """Get current performance metrics"""
        return self.monitor.get_metrics()
```

## Alerting System

### Threshold-Based Alerting

```python
class AlertManager:
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            "response_time_p95": 2.0,  # 2 seconds
            "error_rate": 0.05,        # 5%
            "active_requests": 100     # 100 concurrent requests
        }

    def check_thresholds(self, metrics):
        """Check if any thresholds are exceeded"""
        alerts = []

        if metrics["p95_response_time"] > self.thresholds["response_time_p95"]:
            alerts.append({
                "type": "performance",
                "message": f"P95 response time ({metrics['p95_response_time']:.2f}s) exceeds threshold",
                "severity": "warning"
            })

        if metrics["error_rate"] > self.thresholds["error_rate"]:
            alerts.append({
                "type": "error",
                "message": f"Error rate ({metrics['error_rate']:.2%}) exceeds threshold",
                "severity": "critical"
            })

        self.alerts.extend(alerts)
        return alerts

    def get_active_alerts(self):
        """Get currently active alerts"""
        return self.alerts[-10:]  # Last 10 alerts

@bentoml.service
class AlertingService:
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.alert_manager = AlertManager()

    @bentoml.api
    def predict_with_alerts(self, input_data):
        start_time = time.time()

        try:
            result = self.model.predict(input_data)
            response_time = time.time() - start_time

            self.monitor.record_request(response_time, success=True)

            # Check for alerts
            metrics = self.monitor.get_metrics()
            alerts = self.alert_manager.check_thresholds(metrics)

            return {
                "prediction": result.tolist(),
                "alerts": alerts
            }

        except Exception as e:
            response_time = time.time() - start_time
            self.monitor.record_request(response_time, success=False)
            raise

    @bentoml.api
    def get_alerts(self):
        """Get active alerts"""
        return {"alerts": self.alert_manager.get_active_alerts()}
```

## Health Checks

### Comprehensive Health Checks

```python
@bentoml.service
class HealthCheckService:
    def __init__(self):
        self.start_time = time.time()
        self.last_prediction_time = None
        self.prediction_count = 0

    @bentoml.api
    def health(self):
        """Basic health check"""
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "uptime": time.time() - self.start_time
        }

    @bentoml.api
    def readiness(self):
        """Readiness check"""
        try:
            # Check if model is loaded
            if not hasattr(self, 'model'):
                return {"status": "not_ready", "reason": "Model not loaded"}

            # Quick model test
            test_input = np.array([[1, 2, 3, 4, 5]])
            self.model.predict(test_input)

            return {"status": "ready"}

        except Exception as e:
            return {"status": "not_ready", "reason": str(e)}

    @bentoml.api
    def liveness(self):
        """Liveness check"""
        # Check if service is responsive
        current_time = time.time()

        # If no predictions in last 5 minutes, might be stuck
        if (self.last_prediction_time and
            current_time - self.last_prediction_time > 300):
            return {"status": "unhealthy", "reason": "No recent activity"}

        return {"status": "healthy"}

    @bentoml.api
    def metrics(self):
        """Detailed metrics endpoint"""
        return {
            "uptime": time.time() - self.start_time,
            "total_predictions": self.prediction_count,
            "last_prediction": self.last_prediction_time,
            "memory_usage": self.get_memory_usage(),
            "cpu_usage": self.get_cpu_usage()
        }

    def get_memory_usage(self):
        """Get current memory usage"""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB

    def get_cpu_usage(self):
        """Get current CPU usage"""
        import psutil
        return psutil.cpu_percent(interval=1)
```

## Distributed Tracing

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter
import bentoml

# Configure tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=14268,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@bentoml.service
class TracedService:
    @bentoml.api
    def predict_with_tracing(self, input_data):
        with tracer.start_as_span("prediction_request") as span:
            span.set_attribute("input.shape", str(input_data.shape))
            span.set_attribute("model.name", "my_model")

            with tracer.start_as_span("model_inference") as child_span:
                child_span.set_attribute("batch_size", len(input_data))

                result = self.model.predict(input_data)

                child_span.set_attribute("output.shape", str(result.shape))

            span.set_attribute("output.shape", str(result.shape))
            span.set_status(trace.Status(trace.StatusCode.OK))

            return {"prediction": result.tolist()}
```

## Dashboard Integration

### Grafana Integration

```python
from prometheus_client import Gauge, Counter, Histogram
import time

class MetricsDashboard:
    def __init__(self):
        # Request metrics
        self.request_count = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status']
        )

        self.request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration',
            ['method', 'endpoint']
        )

        # Business metrics
        self.prediction_accuracy = Gauge(
            'model_prediction_accuracy',
            'Model prediction accuracy'
        )

        self.data_drift_score = Gauge(
            'model_data_drift_score',
            'Data drift detection score'
        )

    def record_request(self, method, endpoint, status, duration):
        """Record HTTP request metrics"""
        self.request_count.labels(method, endpoint, status).inc()
        self.request_duration.labels(method, endpoint).observe(duration)

    def update_business_metrics(self, accuracy, drift_score):
        """Update business-specific metrics"""
        self.prediction_accuracy.set(accuracy)
        self.data_drift_score.set(drift_score)

@bentoml.service
class DashboardService:
    def __init__(self):
        self.dashboard = MetricsDashboard()

    @bentoml.api
    def predict_with_dashboard(self, input_data):
        start_time = time.time()

        try:
            result = self.model.predict(input_data)

            # Record metrics
            duration = time.time() - start_time
            self.dashboard.record_request("POST", "/predict", "200", duration)

            return {"prediction": result.tolist()}

        except Exception as e:
            duration = time.time() - start_time
            self.dashboard.record_request("POST", "/predict", "500", duration)
            raise
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **Metrics Collection** - Prometheus integration and custom metrics
2. **Structured Logging** - JSON logging and log aggregation
3. **Performance Monitoring** - Response time tracking and analysis
4. **Alerting Systems** - Threshold-based alerts and notifications
5. **Health Checks** - Readiness, liveness, and comprehensive health endpoints
6. **Distributed Tracing** - OpenTelemetry integration for request tracing
7. **Dashboard Integration** - Grafana and monitoring dashboard setup

## Next Steps

Now that you understand monitoring and observability, let's explore production scaling strategies for your BentoML services. In [Chapter 8: Production Scaling](08-production-scaling.md), we'll dive into auto-scaling, load balancing, and high-availability architectures.

---

**Practice what you've learned:**
1. Set up comprehensive monitoring for your BentoML services
2. Implement structured logging with aggregation
3. Create alerting rules for performance thresholds
4. Build health check endpoints for your services
5. Integrate tracing for distributed request tracking

*What's the most important metric to monitor for your ML services?* 📊

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `time`, `bentoml` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Monitoring & Observability` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `metrics`, `input_data`, `model_name` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Monitoring & Observability` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `time` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `bentoml`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/bentoml/BentoML)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `time` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Deployment Strategies](06-deployment-strategies.md)
- [Next Chapter: Chapter 8: Production Scaling](08-production-scaling.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
