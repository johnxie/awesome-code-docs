---
layout: default
title: "Chapter 2: Model Packaging & Services"
parent: "BentoML Tutorial"
nav_order: 2
---

# Chapter 2: Model Packaging & Services

Welcome to **Chapter 2: Model Packaging & Services**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Now that you understand the basics of BentoML, let's dive deeper into model packaging and service creation. This chapter explores how to create production-ready ML services with advanced features, proper error handling, and optimized performance.

## Advanced Service Creation

### Service Architecture

```python
import bentoml
import numpy as np
from bentoml.io import JSON, NumpyNdarray
from typing import List, Dict, Any

@bentoml.service(
    name="advanced-ml-service",
    version="1.0.0",
    description="Advanced ML service with multiple models and features"
)
class AdvancedMLService:
    def __init__(self):
        # Initialize models
        self.classifier = bentoml.sklearn.load_model("classifier:latest")
        self.regressor = bentoml.sklearn.load_model("regressor:latest")
        self.preprocessor = bentoml.sklearn.load_model("preprocessor:latest")

        # Initialize runners for better performance
        self.classifier_runner = bentoml.sklearn.load_runner("classifier:latest")
        self.regressor_runner = bentoml.sklearn.load_runner("regressor:latest")
        self.preprocessor_runner = bentoml.sklearn.load_runner("preprocessor:latest")

    @bentoml.api
    def classify(self, input_data: NumpyNdarray) -> JSON:
        """Classify input data"""
        # Preprocess data
        processed_data = self.preprocessor_runner.run(input_data)

        # Make prediction
        predictions = self.classifier_runner.run(processed_data)

        return {
            "predictions": predictions.tolist(),
            "confidence": np.max(predictions, axis=1).tolist(),
            "classes": np.argmax(predictions, axis=1).tolist()
        }

    @bentoml.api
    def predict_regression(self, input_data: NumpyNdarray) -> JSON:
        """Regression prediction"""
        processed_data = self.preprocessor_runner.run(input_data)
        predictions = self.regressor_runner.run(processed_data)

        return {
            "predictions": predictions.tolist(),
            "mean_prediction": float(np.mean(predictions)),
            "std_prediction": float(np.std(predictions))
        }

    @bentoml.api
    def batch_predict(self, input_data: NumpyNdarray, batch_size: int = 32) -> JSON:
        """Batch prediction with custom batch size"""
        results = []

        for i in range(0, len(input_data), batch_size):
            batch = input_data[i:i + batch_size]
            processed_batch = self.preprocessor_runner.run(batch)
            predictions = self.classifier_runner.run(processed_batch)

            results.extend(predictions.tolist())

        return {"batch_predictions": results}
```

## Model Management

### Model Versioning

```python
import bentoml

# Save model with metadata
model = bentoml.sklearn.save_model(
    "my_model",
    trained_model,
    metadata={
        "accuracy": 0.95,
        "dataset": "customer_data_v2",
        "training_date": "2024-01-15",
        "framework": "scikit-learn",
        "version": "2.1.0"
    },
    labels={
        "owner": "ml-team",
        "project": "customer-churn",
        "environment": "production"
    }
)

print(f"Model saved: {model.tag}")
```

### Model Loading and Management

```python
# Load specific model version
model_v1 = bentoml.sklearn.load_model("my_model:1.0.0")
model_v2 = bentoml.sklearn.load_model("my_model:2.0.0")
latest_model = bentoml.sklearn.load_model("my_model:latest")

# List all model versions
models = bentoml.models.list()
for model in models:
    if model.name == "my_model":
        print(f"Version: {model.tag}, Created: {model.creation_time}")

# Get model metadata
model_info = bentoml.models.get("my_model:latest")
print(f"Model info: {model_info.metadata}")
```

### Model Optimization

```python
import bentoml
from bentoml.models import Model

# Optimize model for inference
optimized_model = bentoml.models.optimize(
    "my_model:latest",
    optimization_config={
        "quantization": "int8",  # Reduce model size
        "pruning": 0.1,          # Remove 10% of weights
        "compilation": "onnx"    # Convert to ONNX format
    }
)

# Save optimized model
bentoml.models.save(optimized_model, "my_model_optimized")
```

## Runner Configuration

### Basic Runners

```python
# Load model as runner
runner = bentoml.sklearn.load_runner("my_model:latest")

# Runner configuration
runner = bentoml.sklearn.load_runner(
    "my_model:latest",
    init_params={
        "n_jobs": 4,           # Parallel processing
        "batch_size": 32,      # Batch processing
        "max_batch_size": 128  # Maximum batch size
    }
)
```

### Advanced Runner Configuration

```python
# GPU runner configuration
gpu_runner = bentoml.pytorch.load_runner(
    "pytorch_model:latest",
    init_params={
        "device": "cuda",      # Use GPU
        "device_id": 0,        # GPU device ID
        "precision": "fp16"    # Half precision
    }
)

# Distributed runner
distributed_runner = bentoml.tensorflow.load_runner(
    "tf_model:latest",
    init_params={
        "strategy": "mirrored",  # Multi-GPU strategy
        "devices": ["/gpu:0", "/gpu:1"]
    }
)
```

### Custom Runner

```python
from bentoml import Runner, Runnable
from typing import Any, Dict

class CustomRunner(Runnable):
    def __init__(self, model_path: str):
        self.model = self.load_model(model_path)

    def load_model(self, model_path: str):
        # Custom model loading logic
        return load_custom_model(model_path)

    @bentoml.Runnable.method
    def predict(self, input_data: Any) -> Dict[str, Any]:
        # Custom prediction logic
        result = self.model.predict(input_data)
        return {"prediction": result, "confidence": 0.95}

# Create custom runner
custom_runner = CustomRunner("path/to/model")
runner = Runner(custom_runner)
```

## Service Configuration

### Resource Configuration

```python
@bentoml.service(
    name="resource-configured-service",
    resources={
        "cpu": "2",           # 2 CPU cores
        "memory": "4Gi",      # 4GB RAM
        "gpu": "1",           # 1 GPU
        "gpu_memory": "8Gi"   # 8GB GPU memory
    },
    workers=4,  # Number of workers
    timeout=300  # Request timeout in seconds
)
class ResourceConfiguredService:
    pass
```

### Environment Configuration

```python
@bentoml.service(
    name="env-configured-service",
    envs=[
        {"name": "MODEL_PATH", "value": "/opt/models"},
        {"name": "LOG_LEVEL", "value": "INFO"},
        {"name": "DATABASE_URL", "value": "postgresql://..."},
        {"name": "REDIS_URL", "value": "redis://..."}
    ],
    secrets=["api_key", "database_password"]  # Sensitive environment variables
)
class EnvConfiguredService:
    def __init__(self):
        self.model_path = os.environ.get("MODEL_PATH")
        self.db_url = os.environ.get("DATABASE_URL")
        self.redis_url = os.environ.get("REDIS_URL")
```

### Health Checks

```python
@bentoml.service
class HealthCheckService:
    def __init__(self):
        self.start_time = time.time()

    @bentoml.api
    def health(self) -> JSON:
        """Health check endpoint"""
        return {
            "status": "healthy",
            "uptime": time.time() - self.start_time,
            "timestamp": time.time()
        }

    @bentoml.api
    def readiness(self) -> JSON:
        """Readiness check endpoint"""
        # Check if models are loaded and ready
        try:
            self.check_model_health()
            return {"status": "ready"}
        except Exception as e:
            return {"status": "not_ready", "error": str(e)}

    def check_model_health(self):
        """Custom health check logic"""
        if not hasattr(self, 'model'):
            raise Exception("Model not loaded")
        # Additional health checks...
```

## Error Handling

### Exception Handling

```python
@bentoml.service
class ErrorHandlingService:
    @bentoml.api
    def predict_with_error_handling(self, input_data: JSON) -> JSON:
        """Prediction with comprehensive error handling"""
        try:
            # Validate input
            if not self.validate_input(input_data):
                return {"error": "Invalid input format", "status": 400}

            # Process data
            processed_data = self.preprocess(input_data)

            # Make prediction
            prediction = self.model.predict(processed_data)

            return {
                "prediction": prediction.tolist(),
                "status": 200
            }

        except ValueError as e:
            return {"error": f"Validation error: {str(e)}", "status": 400}
        except RuntimeError as e:
            return {"error": f"Runtime error: {str(e)}", "status": 500}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "status": 500}

    def validate_input(self, data):
        """Input validation logic"""
        required_fields = ["features", "metadata"]
        if not all(field in data for field in required_fields):
            return False
        return True

    def preprocess(self, data):
        """Data preprocessing logic"""
        # Preprocessing code here
        return processed_data
```

### Custom Exceptions

```python
class MLServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ModelNotFoundError(MLServiceError):
    def __init__(self, model_name: str):
        super().__init__(f"Model '{model_name}' not found", 404)

class InvalidInputError(MLServiceError):
    def __init__(self, details: str):
        super().__init__(f"Invalid input: {details}", 400)

@bentoml.service
class RobustService:
    @bentoml.api
    def predict(self, input_data: JSON) -> JSON:
        try:
            if "model_name" not in input_data:
                raise InvalidInputError("model_name is required")

            model = self.load_model(input_data["model_name"])
            if model is None:
                raise ModelNotFoundError(input_data["model_name"])

            prediction = model.predict(input_data["features"])
            return {"prediction": prediction.tolist()}

        except MLServiceError as e:
            return {"error": e.message, "status": e.status_code}
        except Exception as e:
            return {"error": f"Internal error: {str(e)}", "status": 500}
```

## Performance Optimization

### Batch Processing

```python
@bentoml.service
class BatchProcessingService:
    @bentoml.api
    def predict_batch(self, input_data: NumpyNdarray) -> JSON:
        """Optimized batch prediction"""
        batch_size = 32

        if len(input_data) <= batch_size:
            # Single batch
            predictions = self.runner.run(input_data)
            return {"predictions": predictions.tolist()}

        # Multiple batches
        predictions = []
        for i in range(0, len(input_data), batch_size):
            batch = input_data[i:i + batch_size]
            batch_predictions = self.runner.run(batch)
            predictions.extend(batch_predictions.tolist())

        return {"predictions": predictions}

    @bentoml.api
    def predict_streaming(self, input_data: NumpyNdarray) -> JSON:
        """Streaming prediction for large datasets"""
        def prediction_generator():
            batch_size = 16
            for i in range(0, len(input_data), batch_size):
                batch = input_data[i:i + batch_size]
                predictions = self.runner.run(batch)
                yield predictions.tolist()

        all_predictions = []
        for batch_predictions in prediction_generator():
            all_predictions.extend(batch_predictions)

        return {"predictions": all_predictions}
```

### Caching

```python
from functools import lru_cache
import hashlib

@bentoml.service
class CachedService:
    def __init__(self):
        self.cache = {}
        self.cache_size = 1000

    @lru_cache(maxsize=128)
    def cached_preprocessing(self, data_hash: str, data: str):
        """Cache preprocessing results"""
        # Expensive preprocessing logic
        return self.preprocess_data(data)

    def get_data_hash(self, data):
        """Generate hash for data caching"""
        data_str = str(data)
        return hashlib.md5(data_str.encode()).hexdigest()

    @bentoml.api
    def predict_with_cache(self, input_data: JSON) -> JSON:
        data_hash = self.get_data_hash(input_data)

        # Check cache
        if data_hash in self.cache:
            return self.cache[data_hash]

        # Process and cache
        processed_data = self.cached_preprocessing(data_hash, str(input_data))
        prediction = self.model.predict(processed_data)

        result = {"prediction": prediction.tolist()}

        # Cache result
        if len(self.cache) < self.cache_size:
            self.cache[data_hash] = result

        return result
```

## Testing and Validation

### Unit Testing

```python
import pytest
import numpy as np
from bentoml.testing import Server

def test_service_prediction():
    """Test service prediction endpoint"""
    with Server("AdvancedMLService") as server:
        # Test data
        test_data = np.random.rand(10, 20)

        # Make request
        response = server.post("/classify", json={"input_data": test_data.tolist()})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == len(test_data)

def test_batch_processing():
    """Test batch processing functionality"""
    with Server("AdvancedMLService") as server:
        # Large dataset
        test_data = np.random.rand(100, 20)

        response = server.post("/batch_predict", json={"input_data": test_data.tolist()})

        assert response.status_code == 200
        data = response.json()
        assert len(data["batch_predictions"]) == len(test_data)
```

### Integration Testing

```python
def test_model_loading():
    """Test model loading and runner initialization"""
    runner = bentoml.sklearn.load_runner("my_model:latest")

    # Test runner
    test_input = np.random.rand(5, 20)
    predictions = runner.run(test_input)

    assert predictions.shape[0] == test_input.shape[0]

def test_error_handling():
    """Test error handling in service"""
    with Server("ErrorHandlingService") as server:
        # Test invalid input
        response = server.post("/predict_with_error_handling", json={})

        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["status"] == 400
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **Advanced Service Creation** - Multi-model services with runners
2. **Model Management** - Versioning, optimization, and metadata
3. **Runner Configuration** - Performance optimization and GPU support
4. **Service Configuration** - Resources, environments, and health checks
5. **Error Handling** - Comprehensive exception handling and custom errors
6. **Performance Optimization** - Batch processing and caching strategies
7. **Testing and Validation** - Unit and integration testing for ML services

## Next Steps

Now that you understand advanced service creation and optimization, let's explore how to define and work with different API endpoints. In [Chapter 3: API Development](03-api-development.md), we'll dive into creating REST APIs, handling different data formats, and implementing advanced API features.

---

**Practice what you've learned:**
1. Create a multi-model service with different ML frameworks
2. Implement comprehensive error handling and logging
3. Set up batch processing for large datasets
4. Configure services for different deployment environments

*What advanced service feature would you like to implement next?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `bentoml`, `input_data` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Model Packaging & Services` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `predictions`, `model`, `prediction` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Model Packaging & Services` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `bentoml` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `input_data`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/bentoml/BentoML)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `bentoml` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with BentoML](01-getting-started.md)
- [Next Chapter: Chapter 3: API Development](03-api-development.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
