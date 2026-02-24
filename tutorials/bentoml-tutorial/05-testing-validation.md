---
layout: default
title: "Chapter 5: Testing & Validation"
parent: "BentoML Tutorial"
nav_order: 5
---

# Chapter 5: Testing & Validation

Welcome to **Chapter 5: Testing & Validation**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers comprehensive testing and validation strategies for BentoML services. We'll explore unit testing, integration testing, performance testing, and validation techniques to ensure your ML services are reliable and production-ready.

## Unit Testing

### Basic Service Testing

```python
import pytest
import numpy as np
from bentoml.testing import Server

def test_basic_prediction():
    """Test basic prediction functionality"""
    with Server("MyMLService") as server:
        # Test data
        test_input = np.random.rand(5, 20)

        # Make request
        response = server.post("/predict", json={"input_data": test_input.tolist()})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == len(test_input)

def test_input_validation():
    """Test input validation"""
    with Server("MyMLService") as server:
        # Invalid input
        response = server.post("/predict", json={"invalid": "data"})

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
```

### Model Testing

```python
def test_model_loading():
    """Test model loading and initialization"""
    import bentoml.sklearn

    # Load model
    model = bentoml.sklearn.load_model("my_model:latest")

    # Test model properties
    assert hasattr(model, 'predict')
    assert hasattr(model, 'predict_proba')

    # Test with sample data
    sample_input = np.random.rand(10, 20)
    predictions = model.predict(sample_input)

    assert predictions.shape[0] == sample_input.shape[0]

def test_model_consistency():
    """Test model prediction consistency"""
    import bentoml.sklearn

    model = bentoml.sklearn.load_model("my_model:latest")
    test_input = np.random.rand(5, 20)

    # Make multiple predictions
    pred1 = model.predict(test_input)
    pred2 = model.predict(test_input)

    # Results should be identical
    np.testing.assert_array_equal(pred1, pred2)
```

## Integration Testing

### End-to-End Testing

```python
def test_end_to_end_workflow():
    """Test complete workflow from request to response"""
    with Server("AdvancedMLService") as server:
        # Prepare test data
        test_data = np.random.rand(10, 20)
        expected_features = test_data.shape[1]

        # Test prediction endpoint
        response = server.post("/classify", json={"input_data": test_data.tolist()})

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "predictions" in data
        assert "confidence" in data
        assert "classes" in data
        assert len(data["predictions"]) == len(test_data)

def test_batch_processing():
    """Test batch processing capabilities"""
    with Server("AdvancedMLService") as server:
        # Large batch
        batch_data = np.random.rand(100, 20)

        response = server.post("/batch_predict",
                             json={"input_data": batch_data.tolist()})

        assert response.status_code == 200
        data = response.json()

        assert len(data["batch_predictions"]) == len(batch_data)
```

### API Integration Testing

```python
def test_api_integration():
    """Test API integration with external services"""
    with Server("ExternalAPIService") as server:
        # Mock external API responses
        with pytest.mock.patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = {"result": "success"}

            response = server.post("/call_external_api",
                                 json={"data": "test"})

            assert response.status_code == 200
            data = response.json()
            assert data["external_result"] == "success"

def test_database_integration():
    """Test database integration"""
    with Server("DatabaseService") as server:
        # Mock database connection
        with pytest.mock.patch('psycopg2.connect') as mock_connect:
            mock_connect.return_value.cursor.return_value.fetchall.return_value = [
                (1, "test_data")
            ]

            response = server.post("/query_database",
                                 json={"query": "SELECT * FROM test"})

            assert response.status_code == 200
            data = response.json()
            assert len(data["results"]) == 1
```

## Performance Testing

### Load Testing

```python
import concurrent.futures
import time

def test_concurrent_requests():
    """Test handling of concurrent requests"""
    with Server("MyMLService") as server:
        def make_request():
            test_data = np.random.rand(1, 20)
            response = server.post("/predict",
                                 json={"input_data": test_data.tolist()})
            return response.status_code

        # Test with multiple concurrent requests
        num_requests = 50
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert all(status == 200 for status in results)

def test_response_time():
    """Test response time performance"""
    with Server("MyMLService") as server:
        test_data = np.random.rand(1, 20)

        start_time = time.time()
        response = server.post("/predict",
                             json={"input_data": test_data.tolist()})
        end_time = time.time()

        response_time = end_time - start_time

        # Response should be under 1 second
        assert response_time < 1.0
        assert response.status_code == 200
```

### Memory Testing

```python
def test_memory_usage():
    """Test memory usage under load"""
    import psutil
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    with Server("MyMLService") as server:
        # Make multiple large requests
        for _ in range(10):
            large_data = np.random.rand(1000, 20)
            response = server.post("/predict",
                                 json={"input_data": large_data.tolist()})
            assert response.status_code == 200

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory

    # Memory increase should be reasonable
    assert memory_increase < 500  # Less than 500MB increase
```

## Validation Testing

### Input Validation

```python
def test_input_validation():
    """Test comprehensive input validation"""
    with Server("ValidatedAPIService") as server:
        # Valid input
        valid_data = {
            "features": [1.0] * 20,
            "user_id": "test_user"
        }
        response = server.post("/predict_validated", json=valid_data)
        assert response.status_code == 200

        # Invalid input - wrong number of features
        invalid_data = {
            "features": [1.0] * 10  # Should be 20
        }
        response = server.post("/predict_validated", json=invalid_data)
        assert response.status_code == 400

        # Invalid input - out of range values
        invalid_data = {
            "features": [100.0] * 20  # Should be -10 to 10
        }
        response = server.post("/predict_validated", json=invalid_data)
        assert response.status_code == 400
```

### Output Validation

```python
def test_output_validation():
    """Test output validation and formatting"""
    with Server("ValidatedAPIService") as server:
        test_data = {"features": [1.0] * 20}

        response = server.post("/predict_validated", json=test_data)
        data = response.json()

        # Validate response structure
        required_fields = ["prediction", "confidence", "validated"]
        for field in required_fields:
            assert field in data

        # Validate data types
        assert isinstance(data["prediction"], (int, float))
        assert isinstance(data["confidence"], (int, float))
        assert isinstance(data["validated"], bool)

        # Validate value ranges
        assert 0 <= data["confidence"] <= 1
```

## Error Handling Testing

```python
def test_error_handling():
    """Test error handling and recovery"""
    with Server("ErrorHandlingService") as server:
        # Test model loading error
        with pytest.mock.patch('bentoml.sklearn.load_model') as mock_load:
            mock_load.side_effect = Exception("Model not found")

            response = server.post("/predict_with_error_handling",
                                 json={"features": [1.0] * 20})

            assert response.status_code == 200  # Service handles error gracefully
            data = response.json()
            assert "error" in data
            assert data["status"] == 500

def test_timeout_handling():
    """Test timeout handling"""
    with Server("MyMLService", timeout=1) as server:
        # Slow operation
        with pytest.mock.patch.object(server.app.model, 'predict') as mock_predict:
            mock_predict.side_effect = lambda x: time.sleep(2) or np.array([0])

            response = server.post("/predict",
                                 json={"input_data": [[1.0] * 20]})

            # Should handle timeout gracefully
            assert response.status_code in [200, 408, 504]
```

## Model Validation

### Model Accuracy Testing

```python
def test_model_accuracy():
    """Test model accuracy against test dataset"""
    import bentoml.sklearn

    model = bentoml.sklearn.load_model("my_model:latest")

    # Load test data (in practice, this would be your test dataset)
    X_test = np.random.rand(100, 20)
    y_test = np.random.randint(0, 10, 100)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate accuracy
    accuracy = np.mean(predictions == y_test)

    # Assert minimum accuracy threshold
    assert accuracy >= 0.8  # 80% minimum accuracy

    print(f"Model accuracy: {accuracy:.3f}")
```

### Model Drift Detection

```python
def test_model_drift():
    """Test for model drift using reference data"""
    import bentoml.sklearn

    model = bentoml.sklearn.load_model("my_model:latest")

    # Reference data (from training time)
    X_ref = np.random.rand(1000, 20)

    # Current predictions on reference data
    ref_predictions = model.predict_proba(X_ref)

    # Store reference statistics
    ref_mean = np.mean(ref_predictions, axis=0)
    ref_std = np.std(ref_predictions, axis=0)

    # Simulate current data
    X_current = np.random.rand(100, 20)
    current_predictions = model.predict_proba(X_current)

    # Check for drift
    current_mean = np.mean(current_predictions, axis=0)
    current_std = np.std(current_predictions, axis=0)

    # Calculate drift metrics
    mean_drift = np.max(np.abs(current_mean - ref_mean))
    std_drift = np.max(np.abs(current_std - ref_std))

    # Assert drift is within acceptable limits
    assert mean_drift < 0.1  # Maximum 10% drift
    assert std_drift < 0.2   # Maximum 20% std deviation change

    print(f"Mean drift: {mean_drift:.3f}")
    print(f"Std drift: {std_drift:.3f}")
```

## Continuous Integration

### GitHub Actions Testing

```yaml
# .github/workflows/test-bentoml.yml
name: Test BentoML Service

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest bentoml[testing]

    - name: Run tests
      run: |
        pytest tests/ -v --cov=bentoml_service --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Docker Testing

```bash
# Test in Docker environment
docker build -t my-bento-test .

# Run tests in container
docker run --rm my-bento-test pytest tests/

# Test API endpoints
docker run -d -p 3000:3000 --name test-service my-bento-test
curl -X POST "http://localhost:3000/predict" \
     -H "Content-Type: application/json" \
     -d '{"input_data": [[1,2,3,4,5]]}'
docker stop test-service
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **Unit Testing** - Testing individual components and functions
2. **Integration Testing** - Testing complete workflows and API integrations
3. **Performance Testing** - Load testing, response time, and memory usage
4. **Validation Testing** - Input/output validation and data integrity
5. **Error Handling Testing** - Exception handling and recovery testing
6. **Model Validation** - Accuracy testing and drift detection
7. **CI/CD Integration** - Automated testing in CI pipelines
8. **Docker Testing** - Containerized testing environments

## Next Steps

Now that you understand testing and validation, let's explore deployment strategies for your BentoML services. In [Chapter 6: Deployment Strategies](06-deployment-strategies.md), we'll dive into Docker deployment, Kubernetes orchestration, and cloud platform integrations.

---

**Practice what you've learned:**
1. Create comprehensive test suites for your ML services
2. Implement performance testing for high-throughput scenarios
3. Set up CI/CD pipelines with automated testing
4. Add model validation and drift detection to your services

*What's the most critical aspect of testing ML services in your experience?* 🧪

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `response`, `assert`, `server` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Testing & Validation` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Test`, `json`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Testing & Validation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `response`.
2. **Input normalization**: shape incoming data so `assert` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `server`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/bentoml/BentoML)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `response` and `assert` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Framework Integration](04-framework-integration.md)
- [Next Chapter: Chapter 6: Deployment Strategies](06-deployment-strategies.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
