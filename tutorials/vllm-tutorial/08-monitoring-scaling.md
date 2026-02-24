---
layout: default
title: "vLLM Tutorial - Chapter 8: Monitoring & Scaling"
nav_order: 8
has_children: false
parent: vLLM Tutorial
---

# Chapter 8: Monitoring & Scaling - Production Operations at Scale

Welcome to **Chapter 8: Monitoring & Scaling - Production Operations at Scale**. In this part of **vLLM Tutorial: High-Performance LLM Inference**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master comprehensive monitoring, performance optimization, and auto-scaling for vLLM deployments in production environments.

## Overview

Production vLLM deployments require sophisticated monitoring, performance optimization, and scaling strategies. This chapter covers real-time monitoring, auto-scaling, performance profiling, and operational best practices for large-scale deployments.

## Comprehensive Monitoring System

### Real-Time Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import psutil
import GPUtil
import threading
import time
from typing import Dict, Any
import asyncio

class VLLMProductionMonitor:
    def __init__(self, service_name: str = "vllm"):
        self.service_name = service_name

        # Request metrics
        self.request_total = Counter(
            f'{service_name}_requests_total',
            'Total number of requests',
            ['method', 'endpoint', 'status', 'model']
        )

        self.request_duration = Histogram(
            f'{service_name}_request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint', 'model'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0]
        )

        self.request_size = Summary(
            f'{service_name}_request_size_bytes',
            'Request size in bytes',
            ['method', 'endpoint']
        )

        # Generation metrics
        self.tokens_generated = Counter(
            f'{service_name}_tokens_generated_total',
            'Total number of tokens generated',
            ['model']
        )

        self.generation_time = Histogram(
            f'{service_name}_generation_time_seconds',
            'Time spent generating tokens',
            ['model'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        self.tokens_per_second = Gauge(
            f'{service_name}_tokens_per_second',
            'Current token generation rate',
            ['model']
        )

        # Model metrics
        self.model_loaded = Gauge(
            f'{service_name}_model_loaded',
            'Whether the model is loaded (1) or not (0)',
            ['model']
        )

        self.model_memory_usage = Gauge(
            f'{service_name}_model_memory_bytes',
            'Memory used by model',
            ['model', 'type']  # type: gpu, cpu, etc.
        )

        # Queue metrics
        self.queue_size = Gauge(
            f'{service_name}_queue_size',
            'Current queue size'
        )

        self.queue_wait_time = Histogram(
            f'{service_name}_queue_wait_time_seconds',
            'Time requests spend in queue',
            buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
        )

        # Error metrics
        self.error_total = Counter(
            f'{service_name}_errors_total',
            'Total number of errors',
            ['error_type', 'endpoint']
        )

        # Resource metrics
        self.cpu_usage = Gauge(
            f'{service_name}_cpu_usage_percent',
            'CPU usage percentage'
        )

        self.memory_usage = Gauge(
            f'{service_name}_memory_usage_bytes',
            'Memory usage in bytes'
        )

        self.gpu_memory_used = Gauge(
            f'{service_name}_gpu_memory_used_bytes',
            'GPU memory used in bytes',
            ['gpu_id']
        )

        self.gpu_utilization = Gauge(
            f'{service_name}_gpu_utilization_percent',
            'GPU utilization percentage',
            ['gpu_id']
        )

        # Business metrics
        self.user_sessions = Gauge(
            f'{service_name}_active_user_sessions',
            'Number of active user sessions'
        )

        self.api_calls_per_user = Histogram(
            f'{service_name}_api_calls_per_user',
            'API calls per user session',
            buckets=[1, 5, 10, 25, 50, 100, 500]
        )

    def start_monitoring(self, port: int = 8001):
        """Start Prometheus metrics server"""
        start_http_server(port)
        print(f"✅ {self.service_name} metrics server started on port {port}")

        # Start background monitoring
        threading.Thread(target=self._monitor_resources, daemon=True).start()

    def _monitor_resources(self):
        """Monitor system resources in background"""
        while True:
            try:
                # CPU and memory
                self.cpu_usage.set(psutil.cpu_percent(interval=1))
                memory = psutil.virtual_memory()
                self.memory_usage.set(memory.used)

                # GPU metrics
                try:
                    gpus = GPUtil.getGPUs()
                    for i, gpu in enumerate(gpus):
                        self.gpu_memory_used.labels(gpu_id=str(i)).set(gpu.memoryUsed * 1024**2)  # MB to bytes
                        self.gpu_utilization.labels(gpu_id=str(i)).set(gpu.load * 100)
                except:
                    pass  # GPU monitoring failed

            except Exception as e:
                print(f"Resource monitoring error: {e}")

            time.sleep(5)  # Update every 5 seconds

    def record_request(self, method: str, endpoint: str, duration: float,
                      status: str, model: str, request_size: int = 0):
        """Record request metrics"""
        self.request_total.labels(
            method=method, endpoint=endpoint, status=status, model=model
        ).inc()

        self.request_duration.labels(
            method=method, endpoint=endpoint, model=model
        ).observe(duration)

        if request_size > 0:
            self.request_size.labels(method=method, endpoint=endpoint).observe(request_size)

    def record_generation(self, model: str, tokens_count: int, generation_time: float):
        """Record generation metrics"""
        self.tokens_generated.labels(model=model).inc(tokens_count)
        self.generation_time.labels(model=model).observe(generation_time)

        # Update tokens per second
        if generation_time > 0:
            tps = tokens_count / generation_time
            self.tokens_per_second.labels(model=model).set(tps)

    def record_queue_metrics(self, queue_size: int, wait_time: float = 0):
        """Record queue metrics"""
        self.queue_size.set(queue_size)
        if wait_time > 0:
            self.queue_wait_time.observe(wait_time)

    def record_error(self, error_type: str, endpoint: str):
        """Record error metrics"""
        self.error_total.labels(error_type=error_type, endpoint=endpoint).inc()

    def update_model_status(self, model: str, loaded: bool):
        """Update model loaded status"""
        self.model_loaded.labels(model=model).set(1 if loaded else 0)

    def update_model_memory(self, model: str, memory_bytes: int, memory_type: str = "gpu"):
        """Update model memory usage"""
        self.model_memory_usage.labels(
            model=model, type=memory_type
        ).set(memory_bytes)

    def record_business_metrics(self, active_sessions: int, user_api_calls: int):
        """Record business metrics"""
        self.user_sessions.set(active_sessions)
        self.api_calls_per_user.observe(user_api_calls)

# Global monitor instance
monitor = VLLMProductionMonitor("vllm")
```

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uuid

class DistributedTracer:
    def __init__(self, service_name: str = "vllm"):
        self.service_name = service_name
        self.tracer = None
        self.setup_tracing()

    def setup_tracing(self):
        """Setup OpenTelemetry tracing"""
        trace.set_tracer_provider(TracerProvider())
        tracer = trace.get_tracer(__name__)

        # Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="jaeger-agent",
            agent_port=6831,
        )

        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        self.tracer = tracer

    def create_request_span(self, request_id: str, method: str, endpoint: str):
        """Create span for API request"""
        return self.tracer.start_as_span(
            f"{method} {endpoint}",
            attributes={
                "request.id": request_id,
                "http.method": method,
                "http.url": endpoint,
                "service.name": self.service_name
            }
        )

    def create_generation_span(self, request_id: str, model: str, prompt_length: int):
        """Create span for text generation"""
        return self.tracer.start_as_span(
            "text_generation",
            attributes={
                "request.id": request_id,
                "model.name": model,
                "prompt.length": prompt_length,
                "operation": "generation"
            }
        )

    def add_generation_attributes(self, span, tokens_generated: int,
                                generation_time: float, finish_reason: str):
        """Add generation-specific attributes to span"""
        span.set_attributes({
            "generation.tokens": tokens_generated,
            "generation.time": generation_time,
            "generation.finish_reason": finish_reason,
            "generation.tokens_per_second": tokens_generated / generation_time if generation_time > 0 else 0
        })

# Global tracer instance
tracer = DistributedTracer("vllm")
```

### Alerting and Anomaly Detection

```python
class AlertManager:
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        self.alerts = []
        self.thresholds = {
            'high_latency': 10.0,  # seconds
            'high_error_rate': 0.05,  # 5%
            'low_throughput': 10.0,  # tokens/second
            'high_memory_usage': 0.9,  # 90%
            'high_cpu_usage': 0.8,  # 80%
        }

    def check_thresholds(self, metrics: Dict[str, Any]):
        """Check metrics against thresholds and generate alerts"""

        alerts = []

        # Latency alert
        avg_latency = metrics.get('avg_request_latency', 0)
        if avg_latency > self.thresholds['high_latency']:
            alerts.append({
                'type': 'high_latency',
                'message': f'Average request latency is {avg_latency:.2f}s (threshold: {self.thresholds["high_latency"]}s)',
                'severity': 'warning',
                'value': avg_latency
            })

        # Error rate alert
        error_rate = metrics.get('error_rate', 0)
        if error_rate > self.thresholds['high_error_rate']:
            alerts.append({
                'type': 'high_error_rate',
                'message': f'Error rate is {error_rate:.2%} (threshold: {self.thresholds["high_error_rate"]:.2%})',
                'severity': 'error',
                'value': error_rate
            })

        # Throughput alert
        throughput = metrics.get('tokens_per_second', 0)
        if throughput < self.thresholds['low_throughput']:
            alerts.append({
                'type': 'low_throughput',
                'message': f'Token throughput is {throughput:.1f} tokens/s (threshold: {self.thresholds["low_throughput"]})',
                'severity': 'warning',
                'value': throughput
            })

        # Memory usage alert
        memory_usage = metrics.get('memory_usage_percent', 0)
        if memory_usage > self.thresholds['high_memory_usage']:
            alerts.append({
                'type': 'high_memory_usage',
                'message': f'Memory usage is {memory_usage:.1%} (threshold: {self.thresholds["high_memory_usage"]:.1%})',
                'severity': 'error',
                'value': memory_usage
            })

        # CPU usage alert
        cpu_usage = metrics.get('cpu_usage_percent', 0)
        if cpu_usage > self.thresholds['high_cpu_usage']:
            alerts.append({
                'type': 'high_cpu_usage',
                'message': f'CPU usage is {cpu_usage:.1%} (threshold: {self.thresholds["high_cpu_usage"]:.1%})',
                'severity': 'warning',
                'value': cpu_usage
            })

        # Send alerts
        for alert in alerts:
            self.send_alert(alert)

        return alerts

    def send_alert(self, alert: Dict[str, Any]):
        """Send alert notification"""
        self.alerts.append({
            **alert,
            'timestamp': time.time(),
            'service': 'vllm'
        })

        # Send to webhook if configured
        if self.webhook_url:
            import requests
            try:
                requests.post(self.webhook_url, json=alert, timeout=5)
            except Exception as e:
                print(f"Failed to send alert: {e}")

        # Log alert
        severity_emoji = {'error': '🚨', 'warning': '⚠️', 'info': 'ℹ️'}
        emoji = severity_emoji.get(alert['severity'], '❓')
        print(f"{emoji} ALERT: {alert['message']}")

    def get_recent_alerts(self, hours: int = 24) -> list:
        """Get recent alerts"""
        cutoff_time = time.time() - (hours * 3600)
        return [alert for alert in self.alerts if alert['timestamp'] > cutoff_time]

    def get_alert_summary(self) -> Dict[str, int]:
        """Get alert summary by type and severity"""
        summary = {}
        for alert in self.alerts[-100:]:  # Last 100 alerts
            alert_type = alert['type']
            severity = alert['severity']

            key = f"{alert_type}_{severity}"
            summary[key] = summary.get(key, 0) + 1

        return summary

# Global alert manager
alert_manager = AlertManager()
```

## Auto-Scaling Strategies

### Horizontal Pod Autoscaling

```python
# Kubernetes HPA configuration for vLLM
hpa_config = """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  # Scale based on CPU utilization
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Scale based on memory utilization
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  # Scale based on custom metrics
  - type: Pods
    pods:
      metric:
        name: vllm_queue_size
      target:
        type: AverageValue
        averageValue: "5"
  - type: Pods
    pods:
      metric:
        name: vllm_request_duration_seconds
        selector:
          matchLabels:
            quantile: "0.95"
      target:
        type: AverageValue
        averageValue: "2"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 1
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
"""

def create_hpa_manifest(queue_size_threshold: int = 5,
                       latency_threshold: float = 2.0,
                       min_replicas: int = 1,
                       max_replicas: int = 10) -> str:
    """Generate HPA manifest with custom parameters"""

    manifest = f"""
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-deployment
  minReplicas: {min_replicas}
  maxReplicas: {max_replicas}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: vllm_queue_size
      target:
        type: AverageValue
        averageValue: "{queue_size_threshold}"
  - type: Pods
    pods:
      metric:
        name: vllm_request_duration_seconds
        selector:
          matchLabels:
            quantile: "0.95"
      target:
        type: AverageValue
        averageValue: "{latency_threshold}"
"""

    return manifest

# Generate HPA manifest
hpa_manifest = create_hpa_manifest(
    queue_size_threshold=3,
    latency_threshold=1.5,
    min_replicas=2,
    max_replicas=8
)

print("Generated HPA Manifest:")
print("=" * 40)
print(hpa_manifest)
```

### Custom Metrics Autoscaling

```python
class AutoscalingManager:
    def __init__(self, k8s_client=None):
        self.k8s_client = k8s_client
        self.current_replicas = 1
        self.scaling_history = []

    async def evaluate_scaling_decision(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate whether to scale up or down"""

        decision = {
            'action': 'none',  # 'scale_up', 'scale_down', 'none'
            'reason': '',
            'confidence': 0.0,
            'target_replicas': self.current_replicas
        }

        # Scaling criteria
        queue_size = metrics.get('queue_size', 0)
        avg_latency = metrics.get('avg_latency', 0)
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)

        # Scale up conditions
        scale_up_conditions = [
            queue_size > 10,  # High queue
            avg_latency > 5.0,  # High latency
            cpu_usage > 0.8,  # High CPU
            memory_usage > 0.85  # High memory
        ]

        # Scale down conditions
        scale_down_conditions = [
            queue_size < 2,  # Low queue
            avg_latency < 0.5,  # Low latency
            cpu_usage < 0.3,  # Low CPU
            memory_usage < 0.4  # Low memory
        ]

        scale_up_score = sum(scale_up_conditions)
        scale_down_score = sum(scale_down_conditions)

        if scale_up_score >= 2:  # At least 2 conditions met
            decision['action'] = 'scale_up'
            decision['target_replicas'] = min(self.current_replicas * 2, 20)  # Double, max 20
            decision['confidence'] = scale_up_score / len(scale_up_conditions)
            decision['reason'] = f"High load detected: queue={queue_size}, latency={avg_latency:.2f}s, cpu={cpu_usage:.1%}"

        elif scale_down_score >= 3:  # At least 3 conditions met
            decision['action'] = 'scale_down'
            decision['target_replicas'] = max(self.current_replicas // 2, 1)  # Halve, min 1
            decision['confidence'] = scale_down_score / len(scale_down_conditions)
            decision['reason'] = f"Low load detected: queue={queue_size}, latency={avg_latency:.2f}s, cpu={cpu_usage:.1%}"

        # Record decision
        self.scaling_history.append({
            'timestamp': time.time(),
            'current_replicas': self.current_replicas,
            'decision': decision,
            'metrics': metrics
        })

        return decision

    async def execute_scaling(self, decision: Dict[str, Any]):
        """Execute scaling decision"""

        if decision['action'] == 'none':
            return

        target_replicas = decision['target_replicas']

        print(f"Executing {decision['action']} to {target_replicas} replicas")
        print(f"Reason: {decision['reason']}")

        # Execute scaling (would integrate with k8s API)
        if self.k8s_client:
            # Actual Kubernetes scaling
            # self.k8s_client.scale_deployment("vllm-deployment", target_replicas)
            pass
        else:
            # Mock scaling
            print(f"Mock scaling: {self.current_replicas} -> {target_replicas}")

        self.current_replicas = target_replicas

    async def run_autoscaling_loop(self, metrics_provider, interval: int = 60):
        """Run continuous autoscaling loop"""

        print("Starting autoscaling loop...")

        while True:
            try:
                # Get current metrics
                metrics = await metrics_provider.get_current_metrics()

                # Evaluate scaling decision
                decision = await self.evaluate_scaling_decision(metrics)

                # Execute scaling if needed
                if decision['action'] != 'none':
                    await self.execute_scaling(decision)

                # Log decision
                print(f"Scaling decision: {decision['action']} "
                      f"(confidence: {decision['confidence']:.2f})")

            except Exception as e:
                print(f"Autoscaling error: {e}")

            await asyncio.sleep(interval)

# Mock metrics provider
class MockMetricsProvider:
    async def get_current_metrics(self):
        """Provide mock metrics"""
        import random
        return {
            'queue_size': random.randint(0, 15),
            'avg_latency': random.uniform(0.1, 8.0),
            'cpu_usage': random.uniform(0.1, 0.95),
            'memory_usage': random.uniform(0.2, 0.95)
        }

# Test autoscaling
autoscaler = AutoscalingManager()
metrics_provider = MockMetricsProvider()

# Run autoscaling evaluation
async def test_autoscaling():
    for i in range(5):
        metrics = await metrics_provider.get_current_metrics()
        decision = await autoscaler.evaluate_scaling_decision(metrics)

        print(f"Evaluation {i+1}: {decision['action']} -> {decision['target_replicas']} replicas")
        print(f"  Reason: {decision['reason'][:60]}...")

        if decision['action'] != 'none':
            await autoscaler.execute_scaling(decision)

await test_autoscaling()
```

## Performance Profiling

### Detailed Performance Analysis

```python
import cProfile
import pstats
import io
from functools import wraps
import torch

class PerformanceProfiler:
    def __init__(self):
        self.profiles = {}
        self.performance_stats = {}

    def profile_function(self, func_name: str):
        """Decorator to profile function performance"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                pr = cProfile.Profile()
                pr.enable()

                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                pr.disable()

                # Get profile stats
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                ps.print_stats(10)  # Top 10 functions

                profile_data = {
                    'profile': s.getvalue(),
                    'execution_time': end_time - start_time,
                    'timestamp': time.time()
                }

                if func_name not in self.profiles:
                    self.profiles[func_name] = []

                self.profiles[func_name].append(profile_data)

                # Keep only last 10 profiles
                if len(self.profiles[func_name]) > 10:
                    self.profiles[func_name] = self.profiles[func_name][-10:]

                return result
            return wrapper
        return decorator

    def profile_gpu_operations(self, operation_name: str):
        """Profile GPU operations"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Reset GPU memory stats
                if torch.cuda.is_available():
                    torch.cuda.reset_peak_memory_stats()

                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                gpu_stats = {}
                if torch.cuda.is_available():
                    gpu_stats = {
                        'memory_allocated': torch.cuda.memory_allocated(),
                        'memory_reserved': torch.cuda.memory_reserved(),
                        'max_memory_allocated': torch.cuda.max_memory_allocated(),
                        'max_memory_reserved': torch.cuda.max_memory_reserved()
                    }

                profile_entry = {
                    'operation': operation_name,
                    'execution_time': end_time - start_time,
                    'gpu_stats': gpu_stats,
                    'timestamp': time.time()
                }

                if operation_name not in self.performance_stats:
                    self.performance_stats[operation_name] = []

                self.performance_stats[operation_name].append(profile_entry)

                return result
            return wrapper
        return decorator

    def get_performance_report(self, func_name: str = None) -> str:
        """Generate performance report"""

        report = "Performance Profiling Report\n"
        report += "=" * 40 + "\n\n"

        if func_name:
            profiles = self.profiles.get(func_name, [])
            if not profiles:
                return f"No profiles found for {func_name}"

            report += f"Function: {func_name}\n"
            report += f"Profile count: {len(profiles)}\n\n"

            # Average execution time
            avg_time = sum(p['execution_time'] for p in profiles) / len(profiles)
            report += f"Average execution time: {avg_time:.4f} seconds\n\n"

            # Latest profile
            if profiles:
                latest = profiles[-1]
                report += "Latest Profile:\n"
                report += latest['profile']

        else:
            # Summary of all profiled functions
            report += "Profiled Functions Summary:\n"
            for name, profiles in self.profiles.items():
                if profiles:
                    avg_time = sum(p['execution_time'] for p in profiles) / len(profiles)
                    report += f"  {name}: {len(profiles)} profiles, avg {avg_time:.4f}s\n"

        return report

# Global profiler instance
profiler = PerformanceProfiler()

# Example usage
@profiler.profile_function("text_generation")
def profiled_generation():
    """Example profiled function"""
    # Simulate some work
    time.sleep(0.1)
    return "Profiled result"

@profiler.profile_gpu_operations("gpu_inference")
def profiled_gpu_operation():
    """Example GPU operation"""
    if torch.cuda.is_available():
        # Simulate GPU work
        x = torch.randn(1000, 1000).cuda()
        y = torch.matmul(x, x)
        return y.sum().item()
    return 0

# Run profiled operations
result1 = profiled_generation()
result2 = profiled_gpu_operation()

# Generate report
report = profiler.get_performance_report()
print(report)
```

### Memory Leak Detection

```python
class MemoryLeakDetector:
    def __init__(self):
        self.memory_snapshots = []
        self.leak_threshold = 50 * 1024 * 1024  # 50MB

    def take_memory_snapshot(self):
        """Take current memory snapshot"""

        snapshot = {
            'timestamp': time.time(),
            'cpu_memory': psutil.Process().memory_info().rss,
            'gpu_memory': {}
        }

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                snapshot['gpu_memory'][f'gpu_{i}'] = torch.cuda.memory_allocated(i)

        self.memory_snapshots.append(snapshot)

        # Keep only last 10 snapshots
        if len(self.memory_snapshots) > 10:
            self.memory_snapshots = self.memory_snapshots[-10:]

    def detect_memory_leaks(self) -> list:
        """Detect potential memory leaks"""

        if len(self.memory_snapshots) < 3:
            return []

        leaks = []

        # Check for consistent memory growth
        recent_snapshots = self.memory_snapshots[-5:]

        # CPU memory trend
        cpu_memory = [s['cpu_memory'] for s in recent_snapshots]
        if len(cpu_memory) >= 3:
            cpu_growth = cpu_memory[-1] - cpu_memory[0]
            if cpu_growth > self.leak_threshold:
                leaks.append({
                    'type': 'cpu_memory_leak',
                    'growth': cpu_growth,
                    'severity': 'high' if cpu_growth > self.leak_threshold * 2 else 'medium'
                })

        # GPU memory trend
        for gpu_id in recent_snapshots[0]['gpu_memory'].keys():
            gpu_memory = [s['gpu_memory'].get(gpu_id, 0) for s in recent_snapshots]
            if len(gpu_memory) >= 3:
                gpu_growth = gpu_memory[-1] - gpu_memory[0]
                if gpu_growth > self.leak_threshold:
                    leaks.append({
                        'type': f'gpu_{gpu_id}_memory_leak',
                        'growth': gpu_growth,
                        'severity': 'high' if gpu_growth > self.leak_threshold * 2 else 'medium'
                    })

        return leaks

    def get_memory_report(self) -> str:
        """Generate memory usage report"""

        if not self.memory_snapshots:
            return "No memory snapshots available"

        latest = self.memory_snapshots[-1]

        report = "Memory Usage Report\n"
        report += "=" * 30 + "\n"
        report += f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(latest['timestamp']))}\n"
        report += f"CPU Memory: {latest['cpu_memory'] / 1024**2:.1f} MB\n"

        for gpu_id, memory in latest['gpu_memory'].items():
            report += f"{gpu_id.upper()} Memory: {memory / 1024**2:.1f} MB\n"

        # Check for leaks
        leaks = self.detect_memory_leaks()
        if leaks:
            report += "\n⚠️  Potential Memory Leaks Detected:\n"
            for leak in leaks:
                growth_mb = leak['growth'] / 1024**2
                report += f"  - {leak['type']}: +{growth_mb:.1f} MB ({leak['severity']})\n"

        return report

# Memory leak detector
memory_detector = MemoryLeakDetector()

# Simulate memory monitoring
for i in range(5):
    memory_detector.take_memory_snapshot()
    time.sleep(1)  # Simulate time between snapshots

# Generate memory report
memory_report = memory_detector.get_memory_report()
print(memory_report)
```

## Operational Best Practices

### Health Checks and Readiness Probes

```python
class HealthChecker:
    def __init__(self, llm, check_interval: int = 30):
        self.llm = llm
        self.check_interval = check_interval
        self.last_check = 0
        self.health_status = {
            'overall': 'unknown',
            'model_loaded': False,
            'memory_ok': False,
            'generation_working': False,
            'last_check_time': 0
        }

    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""

        current_time = time.time()

        # Rate limit checks
        if current_time - self.last_check < self.check_interval:
            return self.health_status

        self.last_check = current_time

        health_status = {
            'overall': 'healthy',
            'model_loaded': True,  # Assume loaded if we get here
            'memory_ok': True,
            'generation_working': True,
            'last_check_time': current_time
        }

        try:
            # Memory check
            if torch.cuda.is_available():
                memory_used = torch.cuda.memory_allocated()
                memory_total = torch.cuda.get_device_properties(0).total_memory
                memory_usage = memory_used / memory_total

                if memory_usage > 0.95:  # 95% memory usage
                    health_status['memory_ok'] = False
                    health_status['overall'] = 'unhealthy'

            # Generation check
            test_result = self.llm.generate(
                ["Quick health check"],
                SamplingParams(max_tokens=5, timeout=10)
            )

            if not test_result or not test_result[0].outputs[0].text.strip():
                health_status['generation_working'] = False
                health_status['overall'] = 'unhealthy'

        except Exception as e:
            health_status['overall'] = 'unhealthy'
            health_status['error'] = str(e)

        self.health_status = health_status
        return health_status

    def is_ready(self) -> bool:
        """Check if service is ready to accept requests"""
        return self.health_status.get('overall') == 'healthy'

    def get_health_report(self) -> str:
        """Generate detailed health report"""

        status = self.health_status

        report = "Health Check Report\n"
        report += "=" * 25 + "\n"
        report += f"Overall Status: {status['overall'].upper()}\n"
        report += f"Model Loaded: {status['model_loaded']}\n"
        report += f"Memory OK: {status['memory_ok']}\n"
        report += f"Generation Working: {status['generation_working']}\n"

        if status.get('last_check_time'):
            report += f"Last Check: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status['last_check_time']))}\n"

        if status.get('error'):
            report += f"Error: {status['error']}\n"

        return report

# Health checker
health_checker = HealthChecker(llm)

# Run health check
async def run_health_check():
    health_status = await health_checker.comprehensive_health_check()
    health_report = health_checker.get_health_report()

    print(health_report)
    print(f"Service Ready: {health_checker.is_ready()}")

await run_health_check()
```

## Summary

In this final chapter, we've covered advanced monitoring and scaling:

- **Comprehensive Monitoring**: Real-time metrics, distributed tracing, and alerting
- **Auto-Scaling**: Horizontal pod autoscaling and intelligent scaling decisions
- **Performance Profiling**: Detailed analysis and memory leak detection
- **Health Checks**: Comprehensive health monitoring and readiness probes

These practices enable production vLLM deployments that can handle enterprise workloads with high reliability and performance.

## Key Takeaways

1. **Monitoring**: Comprehensive metrics collection and alerting for operational visibility
2. **Scaling**: Intelligent auto-scaling based on multiple metrics and thresholds
3. **Profiling**: Detailed performance analysis and memory leak detection
4. **Health Checks**: Proactive monitoring and automated recovery
5. **Operational Excellence**: Production-ready practices for enterprise deployments

This concludes our comprehensive vLLM tutorial series. You've learned everything from basic inference to advanced production deployment and scaling strategies.

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `metrics`, `time` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Monitoring & Scaling - Production Operations at Scale` as an operating subsystem inside **vLLM Tutorial: High-Performance LLM Inference**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `report`, `decision`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Monitoring & Scaling - Production Operations at Scale` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `metrics` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `time`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/vllm-project/vllm)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `metrics` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Production Deployment - Serving vLLM at Scale](07-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
