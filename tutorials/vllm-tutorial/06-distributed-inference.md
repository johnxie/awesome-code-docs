---
layout: default
title: "vLLM Tutorial - Chapter 6: Distributed Inference"
nav_order: 6
has_children: false
parent: vLLM Tutorial
---

# Chapter 6: Distributed Inference - Scaling Across GPUs and Nodes

> Master distributed inference techniques with vLLM including multi-GPU setups, tensor parallelism, and cluster deployments.

## Overview

Distributed inference enables scaling vLLM across multiple GPUs and compute nodes. This chapter covers tensor parallelism, pipeline parallelism, multi-node setups, and production deployment strategies for handling high-throughput workloads.

## Tensor Parallelism Basics

### Single-Node Multi-GPU Setup

```python
from vllm import LLM, SamplingParams
import torch

def setup_tensor_parallelism(model_name, num_gpus=2):
    """Set up tensor parallelism across multiple GPUs on single node"""

    print(f"Setting up tensor parallelism with {num_gpus} GPUs...")

    # Check GPU availability
    available_gpus = torch.cuda.device_count()
    if available_gpus < num_gpus:
        raise ValueError(f"Requested {num_gpus} GPUs but only {available_gpus} available")

    try:
        llm = LLM(
            model=model_name,
            tensor_parallel_size=num_gpus,  # Enable tensor parallelism
            gpu_memory_utilization=0.85,   # Use 85% of each GPU's memory
            max_model_len=2048,
            dtype="half"  # FP16 for memory efficiency
        )

        print(f"✅ Tensor parallelism configured across {num_gpus} GPUs")
        return llm

    except Exception as e:
        print(f"❌ Tensor parallelism setup failed: {e}")
        return None

# Test tensor parallelism
if torch.cuda.device_count() >= 2:
    tp_llm = setup_tensor_parallelism("microsoft/DialoGPT-large", num_gpus=2)

    if tp_llm:
        # Test generation
        prompts = ["Explain quantum computing", "What is machine learning?"]
        results = tp_llm.generate(prompts, SamplingParams(max_tokens=100))

        print("Tensor parallelism test results:")
        for i, result in enumerate(results):
            print(f"Prompt {i+1}: {len(result.outputs[0].text)} characters generated")
else:
    print("Multi-GPU setup not available - requires 2+ GPUs")
```

### Understanding Tensor Parallelism

```python
# Visualize tensor parallelism
def explain_tensor_parallelism():
    """Explain how tensor parallelism works"""

    print("Tensor Parallelism Explanation:")
    print("=" * 40)

    print("\nWithout Tensor Parallelism:")
    print("Single GPU handles entire model")
    print("Model: [Layer1][Layer2][Layer3][Layer4]")
    print("GPU 1: [L1][L2][L3][L4] ← Limited by GPU memory")

    print("\nWith Tensor Parallelism (2 GPUs):")
    print("Model split across GPUs")
    print("GPU 1: [L1][L2]     GPU 2: [L3][L4]")
    print("Communication overhead but 2x memory capacity")

    print("\nBenefits:")
    print("• Scale to larger models")
    print("• Better memory utilization")
    print("• Higher throughput")

    print("\nTrade-offs:")
    print("• Inter-GPU communication latency")
    print("• More complex setup")
    print("• Not all operations are parallelizable")

explain_tensor_parallelism()
```

### Performance Scaling with Tensor Parallelism

```python
def benchmark_tensor_parallelism(model_name="microsoft/DialoGPT-large"):
    """Benchmark performance scaling with tensor parallelism"""

    import time

    results = {}

    # Test different GPU counts
    gpu_counts = [1] + list(range(2, torch.cuda.device_count() + 1, 2))

    test_prompts = ["Write a detailed explanation of neural networks"] * 4
    sampling_params = SamplingParams(max_tokens=200, temperature=0.7)

    for num_gpus in gpu_counts:
        try:
            print(f"\nBenchmarking with {num_gpus} GPUs...")

            # Setup
            llm = LLM(
                model=model_name,
                tensor_parallel_size=num_gpus,
                gpu_memory_utilization=0.8
            )

            # Warm up
            llm.generate(["warmup"], SamplingParams(max_tokens=10))

            # Benchmark
            start_time = time.time()
            batch_results = llm.generate(test_prompts, sampling_params)
            end_time = time.time()

            batch_time = end_time - start_time
            total_tokens = sum(len(r.outputs[0].token_ids) for r in batch_results)
            throughput = total_tokens / batch_time

            results[num_gpus] = {
                'throughput': throughput,
                'batch_time': batch_time,
                'total_tokens': total_tokens,
                'success': True
            }

            print(".2f")
            print(".3f")

        except Exception as e:
            results[num_gpus] = {
                'success': False,
                'error': str(e)
            }
            print(f"❌ Failed: {e}")

    return results

# Run benchmark if multi-GPU available
if torch.cuda.device_count() >= 2:
    tp_results = benchmark_tensor_parallelism()

    print("\nTensor Parallelism Scaling Results:")
    print("=" * 50)

    for gpus, result in tp_results.items():
        if result['success']:
            print(f"{gpus} GPUs: {result['throughput']:.2f} tokens/s")
        else:
            print(f"{gpus} GPUs: Failed - {result['error']}")
else:
    print("Multi-GPU benchmark requires 2+ GPUs")
```

## Pipeline Parallelism

### Model Parallelism Strategies

```python
# Pipeline parallelism (advanced - requires custom setup)
def setup_pipeline_parallelism():
    """Set up pipeline parallelism across GPUs"""

    print("Pipeline Parallelism Setup:")
    print("Note: This is a conceptual demonstration")
    print("Actual implementation requires model surgery and custom distribution")

    # Conceptual pipeline setup
    pipeline_config = {
        'gpu_0': ['embedding', 'layer_0', 'layer_1'],
        'gpu_1': ['layer_2', 'layer_3', 'layer_4'],
        'gpu_2': ['layer_5', 'layer_6', 'layer_7'],
        'gpu_3': ['layer_8', 'layer_9', 'output']
    }

    print("\nPipeline Distribution:")
    for gpu, layers in pipeline_config.items():
        print(f"{gpu}: {layers}")

    print("\nBenefits:")
    print("• Micro-batch processing")
    print("• Reduced memory per GPU")
    print("• Better for deep models")

    print("\nChallenges:")
    print("• Pipeline bubble time")
    print("• Complex synchronization")
    print("• Harder to implement")

    return pipeline_config

pipeline_config = setup_pipeline_parallelism()
```

### 3D Parallelism (Data + Tensor + Pipeline)

```python
def explain_3d_parallelism():
    """Explain 3D parallelism strategy"""

    print("3D Parallelism: Data + Tensor + Pipeline")
    print("=" * 50)

    print("\nData Parallelism:")
    print("• Same model on multiple GPUs")
    print("• Different data batches per GPU")
    print("• Gradient synchronization")
    print("• Scales batch size")

    print("\nTensor Parallelism:")
    print("• Model split across GPUs")
    print("• Parallel matrix operations")
    print("• Scales model size")
    print("• Requires fast interconnect")

    print("\nPipeline Parallelism:")
    print("• Model layers distributed across GPUs")
    print("• Micro-batch pipelining")
    print("• Scales model depth")
    print("• Minimizes memory per GPU")

    print("\nCombined 3D Parallelism:")
    print("• Data: Multiple replicas")
    print("• Tensor: Split within replicas")
    print("• Pipeline: Layers across GPUs")
    print("• Maximum scalability")

    print("\nExample: 8 GPUs, 2 nodes")
    print("Node 1: [Data1-Tensor1-Pipeline1] [Data2-Tensor2-Pipeline2]")
    print("Node 2: [Data3-Tensor3-Pipeline3] [Data4-Tensor4-Pipeline4]")

explain_3d_parallelism()
```

## Multi-Node Distributed Inference

### Ray-Based Distributed Setup

```python
# Multi-node setup with Ray (if available)
try:
    import ray

    def setup_ray_cluster():
        """Set up Ray cluster for distributed inference"""

        # Initialize Ray
        ray.init()

        @ray.remote(num_gpus=1)
        class DistributedLLM:
            def __init__(self, model_name):
                from vllm import LLM
                self.llm = LLM(model_name)

            def generate(self, prompts, sampling_params):
                return self.llm.generate(prompts, sampling_params)

        # Create distributed LLM instances
        llm_actors = [
            DistributedLLM.remote("microsoft/DialoGPT-medium")
            for _ in range(min(4, torch.cuda.device_count()))
        ]

        print(f"✅ Created {len(llm_actors)} distributed LLM actors")
        return llm_actors

    # Test Ray distributed setup
    if torch.cuda.device_count() >= 2:
        ray_actors = setup_ray_cluster()

        # Distributed generation
        futures = []
        for i, actor in enumerate(ray_actors):
            future = actor.generate.remote(
                [f"Test prompt {i}"],
                SamplingParams(max_tokens=50)
            )
            futures.append(future)

        # Collect results
        results = ray.get(futures)

        print("Ray distributed results:")
        for i, result in enumerate(results):
            print(f"Actor {i}: {len(result[0].outputs[0].text)} chars generated")

    else:
        print("Ray distributed setup requires 2+ GPUs")

except ImportError:
    print("Ray not available - install with: pip install ray")
```

### Kubernetes Multi-Node Deployment

```python
# Kubernetes deployment for multi-node inference
def generate_k8s_manifests(num_nodes=2, gpus_per_node=2):
    """Generate Kubernetes manifests for distributed inference"""

    manifests = {}

    # Deployment manifest
    deployment = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-distributed
spec:
  replicas: {num_nodes}
  selector:
    matchLabels:
      app: vllm-distributed
  template:
    metadata:
      labels:
        app: vllm-distributed
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_NAME
          value: "microsoft/DialoGPT-large"
        - name: TENSOR_PARALLEL_SIZE
          value: "{gpus_per_node}"
        resources:
          limits:
            nvidia.com/gpu: {gpus_per_node}
          requests:
            memory: "32Gi"
            cpu: "8"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
"""

    # Service manifest
    service = """
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
spec:
  selector:
    app: vllm-distributed
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""

    # Ingress manifest
    ingress = """
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vllm-ingress
spec:
  rules:
  - host: vllm.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vllm-service
            port:
              number: 80
"""

    manifests['deployment'] = deployment
    manifests['service'] = service
    manifests['ingress'] = ingress

    return manifests

# Generate and display manifests
k8s_manifests = generate_k8s_manifests(num_nodes=2, gpus_per_node=2)

print("Kubernetes Deployment Manifests:")
print("=" * 40)

for name, manifest in k8s_manifests.items():
    print(f"\n{name.upper()}:")
    print(manifest)
```

## Load Balancing and Request Routing

### Intelligent Load Balancer

```python
class DistributedLoadBalancer:
    def __init__(self, llm_instances):
        self.instances = llm_instances
        self.request_count = 0
        self.instance_stats = {i: {'requests': 0, 'latency': 0} for i in range(len(llm_instances))}

    async def route_request(self, prompt, sampling_params):
        """Route request to best available instance"""

        # Simple round-robin for demonstration
        instance_id = self.request_count % len(self.instances)
        instance = self.instances[instance_id]
        self.request_count += 1

        # Track request
        self.instance_stats[instance_id]['requests'] += 1

        import time
        start_time = time.time()

        # Route to instance
        result = instance.generate([prompt], sampling_params)[0]

        end_time = time.time()
        latency = end_time - start_time

        # Update stats
        self.instance_stats[instance_id]['latency'] = (
            (self.instance_stats[instance_id]['latency'] +
             latency) / 2  # Rolling average
        )

        return result.outputs[0].text, instance_id

    def get_load_stats(self):
        """Get load balancing statistics"""

        total_requests = sum(stats['requests'] for stats in self.instance_stats.values())
        avg_latency = sum(stats['latency'] for stats in self.instance_stats.values()) / len(self.instance_stats)

        return {
            'total_requests': total_requests,
            'instance_stats': self.instance_stats,
            'average_latency': avg_latency,
            'load_distribution': [stats['requests'] for stats in self.instance_stats.values()]
        }

# Test load balancer
if torch.cuda.device_count() >= 2:
    # Create multiple instances
    instances = []
    for i in range(min(2, torch.cuda.device_count())):
        llm_instance = LLM(
            model="microsoft/DialoGPT-medium",
            tensor_parallel_size=1
        )
        instances.append(llm_instance)

    load_balancer = DistributedLoadBalancer(instances)

    # Test routing
    test_prompts = [f"Test request {i}" for i in range(6)]

    import asyncio
    async def test_routing():
        for prompt in test_prompts:
            result, instance_id = await load_balancer.route_request(
                prompt,
                SamplingParams(max_tokens=30)
            )
            print(f"Request routed to instance {instance_id}: {result[:50]}...")

        # Get stats
        stats = load_balancer.get_load_stats()
        print(f"\nLoad Stats: {stats}")

    await test_routing()
else:
    print("Load balancer test requires 2+ GPUs")
```

### Adaptive Request Routing

```python
class AdaptiveRouter:
    def __init__(self, llm_instances):
        self.instances = llm_instances
        self.performance_history = {i: [] for i in range(len(llm_instances))}

    async def route_adaptive(self, prompt, sampling_params):
        """Route based on instance performance and current load"""

        # Calculate instance scores based on recent performance
        instance_scores = {}

        for instance_id, history in self.performance_history.items():
            if history:
                avg_latency = sum(h['latency'] for h in history) / len(history)
                success_rate = sum(h['success'] for h in history) / len(history)
                # Higher score for lower latency and higher success
                score = success_rate / (avg_latency + 0.1)  # Avoid division by zero
            else:
                score = 1.0  # Default score for new instances

            instance_scores[instance_id] = score

        # Select best instance
        best_instance_id = max(instance_scores.keys(), key=lambda x: instance_scores[x])
        instance = self.instances[best_instance_id]

        import time
        start_time = time.time()

        try:
            result = instance.generate([prompt], sampling_params)[0]
            success = True
            response = result.outputs[0].text
        except Exception as e:
            success = False
            response = f"Error: {e}"

        end_time = time.time()
        latency = end_time - start_time

        # Update performance history
        self.performance_history[best_instance_id].append({
            'latency': latency,
            'success': success,
            'timestamp': time.time()
        })

        # Keep only recent history (last 100 requests)
        if len(self.performance_history[best_instance_id]) > 100:
            self.performance_history[best_instance_id] = self.performance_history[best_instance_id][-100:]

        return response, best_instance_id, success

# Test adaptive routing
if torch.cuda.device_count() >= 2:
    instances = [LLM("microsoft/DialoGPT-medium") for _ in range(min(2, torch.cuda.device_count()))]
    adaptive_router = AdaptiveRouter(instances)

    async def test_adaptive_routing():
        test_prompts = ["Hello", "How are you?", "What's the weather?", "Tell me a joke"]

        for prompt in test_prompts:
            response, instance_id, success = await adaptive_router.route_adaptive(
                prompt,
                SamplingParams(max_tokens=20)
            )
            status = "✅" if success else "❌"
            print(f"{status} Instance {instance_id}: {response[:40]}...")

    await test_adaptive_routing()
else:
    print("Adaptive routing test requires 2+ GPUs")
```

## Fault Tolerance and Recovery

### Instance Health Monitoring

```python
class HealthMonitor:
    def __init__(self, llm_instances, health_check_interval=30):
        self.instances = llm_instances
        self.health_status = {i: {'healthy': True, 'last_check': 0} for i in range(len(llm_instances))}
        self.health_check_interval = health_check_interval

    async def monitor_health(self):
        """Continuously monitor instance health"""

        while True:
            for instance_id, instance in enumerate(self.instances):
                current_time = time.time()
                last_check = self.health_status[instance_id]['last_check']

                if current_time - last_check > self.health_check_interval:
                    # Perform health check
                    is_healthy = await self._check_instance_health(instance)

                    self.health_status[instance_id]['healthy'] = is_healthy
                    self.health_status[instance_id]['last_check'] = current_time

                    if not is_healthy:
                        print(f"⚠️ Instance {instance_id} is unhealthy")
                    else:
                        print(f"✅ Instance {instance_id} is healthy")

            await asyncio.sleep(self.health_check_interval)

    async def _check_instance_health(self, instance):
        """Check if instance is responding"""

        try:
            # Simple health check - try a short generation
            result = instance.generate(
                ["test"],
                SamplingParams(max_tokens=5, timeout=10)
            )

            return len(result) > 0 and len(result[0].outputs[0].text) > 0

        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def get_healthy_instances(self):
        """Get list of healthy instance IDs"""

        return [i for i, status in self.health_status.items() if status['healthy']]

    def get_health_report(self):
        """Get comprehensive health report"""

        total_instances = len(self.instances)
        healthy_instances = sum(1 for status in self.health_status.values() if status['healthy'])

        return {
            'total_instances': total_instances,
            'healthy_instances': healthy_instances,
            'unhealthy_instances': total_instances - healthy_instances,
            'health_percentage': (healthy_instances / total_instances) * 100 if total_instances > 0 else 0,
            'instance_details': self.health_status
        }

# Test health monitoring
health_monitor = HealthMonitor([llm] * min(2, max(1, torch.cuda.device_count())))

# Start monitoring
monitor_task = asyncio.create_task(health_monitor.monitor_health())

# Let it run briefly
await asyncio.sleep(5)

# Get health report
report = health_monitor.get_health_report()
print("Health Report:")
print(f"Healthy instances: {report['healthy_instances']}/{report['total_instances']}")

# Stop monitoring
monitor_task.cancel()
```

### Automatic Failover

```python
class FailoverManager:
    def __init__(self, primary_instances, backup_instances=None):
        self.primary_instances = primary_instances
        self.backup_instances = backup_instances or []
        self.active_instances = primary_instances.copy()
        self.failed_instances = set()

    async def execute_with_failover(self, prompt, sampling_params, max_retries=2):
        """Execute with automatic failover"""

        for attempt in range(max_retries + 1):
            if not self.active_instances:
                raise Exception("No active instances available")

            # Select instance (round-robin)
            instance_id = attempt % len(self.active_instances)
            instance = self.active_instances[instance_id]

            try:
                result = instance.generate([prompt], sampling_params)[0]
                return result.outputs[0].text, instance_id, attempt

            except Exception as e:
                print(f"Instance {instance_id} failed (attempt {attempt + 1}): {e}")

                # Mark instance as failed
                self.failed_instances.add(instance_id)
                self.active_instances.remove(instance)

                # Try to activate backup
                if self.backup_instances and attempt < max_retries:
                    backup_id = len(self.primary_instances) + len(self.active_instances)
                    if backup_id < len(self.primary_instances) + len(self.backup_instances):
                        backup_instance = self.backup_instances[backup_id - len(self.primary_instances)]
                        self.active_instances.append(backup_instance)
                        print(f"Activated backup instance {backup_id}")

        raise Exception("All instances failed")

    def get_failover_stats(self):
        """Get failover statistics"""

        return {
            'total_instances': len(self.primary_instances) + len(self.backup_instances),
            'active_instances': len(self.active_instances),
            'failed_instances': len(self.failed_instances),
            'backup_instances': len(self.backup_instances)
        }

# Test failover
primary_llm = LLM("microsoft/DialoGPT-medium")
backup_llm = LLM("gpt2")  # Simulating backup with different model

failover_manager = FailoverManager(
    primary_instances=[primary_llm],
    backup_instances=[backup_llm]
)

# Test failover (simulate failure by using invalid instance)
try:
    result, instance_id, attempts = await failover_manager.execute_with_failover(
        "Test prompt",
        SamplingParams(max_tokens=20)
    )
    print(f"Success: Instance {instance_id}, Attempts: {attempts}")
    print(f"Result: {result[:50]}...")

except Exception as e:
    print(f"Final failure: {e}")

stats = failover_manager.get_failover_stats()
print(f"Failover stats: {stats}")
```

## Production Deployment Patterns

### High Availability Setup

```python
def create_ha_deployment_manifest():
    """Create high availability deployment manifest"""

    ha_manifest = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-ha-deployment
spec:
  replicas: 3  # Multiple replicas for HA
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: vllm-ha
  template:
    metadata:
      labels:
        app: vllm-ha
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: vllm-ha
              topologyKey: kubernetes.io/hostname
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_NAME
          value: "microsoft/DialoGPT-large"
        - name: TENSOR_PARALLEL_SIZE
          value: "2"
        resources:
          limits:
            nvidia.com/gpu: 2
          requests:
            memory: "16Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-ha-service
spec:
  selector:
    app: vllm-ha
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vllm-ha-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: vllm-ha.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vllm-ha-service
            port:
              number: 80
"""

    return ha_manifest

# Generate HA manifest
ha_manifest = create_ha_deployment_manifest()
print("High Availability Deployment Manifest:")
print("=" * 50)
print(ha_manifest)
```

## Monitoring and Observability

### Distributed Metrics Collection

```python
# Distributed monitoring setup
class DistributedMonitor:
    def __init__(self, instance_ids):
        self.instance_ids = instance_ids
        self.metrics = {i: {} for i in instance_ids}

    async def collect_distributed_metrics(self):
        """Collect metrics from all distributed instances"""

        # In a real setup, this would query each instance's metrics endpoint
        for instance_id in self.instance_ids:
            # Simulate metric collection
            self.metrics[instance_id] = {
                'requests_per_second': 10 + instance_id,
                'average_latency': 0.5 + (instance_id * 0.1),
                'memory_usage': 0.7 + (instance_id * 0.05),
                'gpu_utilization': 0.8 + (instance_id * 0.03),
                'queue_length': instance_id * 2,
                'error_rate': instance_id * 0.01
            }

        return self.metrics

    def generate_cluster_report(self):
        """Generate comprehensive cluster report"""

        if not self.metrics:
            return "No metrics available"

        total_instances = len(self.metrics)
        total_rps = sum(m.get('requests_per_second', 0) for m in self.metrics.values())
        avg_latency = sum(m.get('average_latency', 0) for m in self.metrics.values()) / total_instances
        avg_memory = sum(m.get('memory_usage', 0) for m in self.metrics.values()) / total_instances
        avg_gpu = sum(m.get('gpu_utilization', 0) for m in self.metrics.values()) / total_instances

        report = ".2f"".3f"".3f"".3f"f"""
Cluster Performance Report
==========================
Total Instances: {total_instances}
Total RPS: {total_rps:.1f}
Average Latency: {avg_latency:.3f}s
Average Memory Usage: {avg_memory:.1f}
Average GPU Utilization: {avg_gpu:.1f}

Instance Details:
"""

        for instance_id, metrics in self.metrics.items():
            report += f"""
Instance {instance_id}:
  RPS: {metrics.get('requests_per_second', 0):.1f}
  Latency: {metrics.get('average_latency', 0):.3f}s
  Memory: {metrics.get('memory_usage', 0):.1f}
  GPU: {metrics.get('gpu_utilization', 0):.1f}
  Queue: {metrics.get('queue_length', 0)}
  Errors: {metrics.get('error_rate', 0):.3f}
"""

        return report

# Test distributed monitoring
monitor = DistributedMonitor([0, 1, 2])  # Simulate 3 instances

# Collect metrics
await monitor.collect_distributed_metrics()

# Generate report
report = monitor.generate_cluster_report()
print(report)
```

## Summary

In this chapter, we've covered distributed inference techniques:

- **Tensor Parallelism**: Model distribution across multiple GPUs
- **Pipeline Parallelism**: Layer distribution and micro-batching
- **Multi-Node Setup**: Kubernetes and Ray-based distributed deployments
- **Load Balancing**: Intelligent request routing and failover
- **Fault Tolerance**: Health monitoring and automatic recovery
- **Production Deployment**: High availability and monitoring

Distributed inference enables scaling vLLM to handle enterprise workloads with high throughput and reliability.

## Key Takeaways

1. **Tensor Parallelism**: Distribute models across GPUs for larger models
2. **Load Balancing**: Route requests intelligently for optimal performance
3. **Fault Tolerance**: Monitor health and provide automatic failover
4. **Scalability**: Scale from single GPU to multi-node clusters
5. **Monitoring**: Comprehensive observability for distributed systems

Next, we'll explore **production deployment** - serving vLLM with FastAPI, Docker, and Kubernetes.

---

**Ready for the next chapter?** [Chapter 7: Production Deployment](07-production-deployment.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*