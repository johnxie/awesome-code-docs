---
layout: default
title: "Chapter 4: Framework Integration"
parent: "BentoML Tutorial"
nav_order: 4
---

# Chapter 4: Framework Integration

Welcome to **Chapter 4: Framework Integration**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explores how to integrate BentoML with popular ML frameworks including TensorFlow, PyTorch, Scikit-learn, and others. We'll cover framework-specific optimizations, model loading, and best practices for each framework.

## TensorFlow Integration

### Basic TensorFlow Model

```python
import bentoml.tensorflow
import tensorflow as tf
from bentoml.io import NumpyNdarray, JSON

# Create and train TensorFlow model
def create_tf_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

@bentoml.service
class TensorFlowService:
    def __init__(self):
        self.model = bentoml.tensorflow.load_model("tf_model:latest")

    @bentoml.api
    def predict_tf(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """TensorFlow prediction"""
        return self.model.predict(input_data)

    @bentoml.api
    def classify_tf(self, input_data: NumpyNdarray) -> JSON:
        """TensorFlow classification with probabilities"""
        predictions = self.model.predict(input_data)

        return {
            "class": int(tf.argmax(predictions, axis=1).numpy()[0]),
            "confidence": float(tf.reduce_max(predictions).numpy()),
            "probabilities": predictions.tolist()[0]
        }
```

### TensorFlow Serving Optimization

```python
@bentoml.service
class OptimizedTensorFlowService:
    def __init__(self):
        # Load model with optimization
        self.model = bentoml.tensorflow.load_model(
            "tf_model:latest",
            custom_objects=None,
            compile=True  # Enable graph optimization
        )

        # Enable XLA compilation for better performance
        tf.config.optimizer.set_jit(True)

    @bentoml.api
    def predict_optimized(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """Optimized TensorFlow prediction"""
        # Use tf.function for graph optimization
        @tf.function
        def optimized_predict(x):
            return self.model(x, training=False)

        return optimized_predict(input_data)
```

## PyTorch Integration

### Basic PyTorch Model

```python
import bentoml.pytorch
import torch
import torch.nn as nn
from bentoml.io import NumpyNdarray, JSON

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(20, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 10)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

@bentoml.service
class PyTorchService:
    def __init__(self):
        self.model = bentoml.pytorch.load_model("pytorch_model:latest")
        self.model.eval()  # Set to evaluation mode

    @bentoml.api
    def predict_pytorch(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """PyTorch prediction"""
        with torch.no_grad():
            input_tensor = torch.from_numpy(input_data).float()
            outputs = self.model(input_tensor)
            return outputs.numpy()
```

### PyTorch GPU Optimization

```python
@bentoml.service
class OptimizedPyTorchService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = bentoml.pytorch.load_model("pytorch_model:latest")
        self.model.to(self.device)
        self.model.eval()

        # Enable optimizations
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True

    @bentoml.api
    def predict_gpu(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """GPU-accelerated PyTorch prediction"""
        with torch.no_grad():
            input_tensor = torch.from_numpy(input_data).float().to(self.device)
            outputs = self.model(input_tensor)
            return outputs.cpu().numpy()
```

## Scikit-learn Integration

### Basic Scikit-learn Model

```python
import bentoml.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from bentoml.io import NumpyNdarray, JSON

@bentoml.service
class SklearnService:
    def __init__(self):
        self.model = bentoml.sklearn.load_model("sklearn_model:latest")
        self.scaler = bentoml.sklearn.load_model("scaler:latest")

    @bentoml.api
    def predict_sklearn(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """Scikit-learn prediction"""
        # Scale input data
        scaled_data = self.scaler.transform(input_data)
        return self.model.predict(scaled_data)

    @bentoml.api
    def predict_proba_sklearn(self, input_data: NumpyNdarray) -> JSON:
        """Scikit-learn prediction with probabilities"""
        scaled_data = self.scaler.transform(input_data)
        predictions = self.model.predict(scaled_data)
        probabilities = self.model.predict_proba(scaled_data)

        return {
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist(),
            "classes": self.model.classes_.tolist()
        }
```

## XGBoost Integration

```python
import bentoml.xgboost
import xgboost as xgb
from bentoml.io import NumpyNdarray, JSON

@bentoml.service
class XGBoostService:
    def __init__(self):
        self.model = bentoml.xgboost.load_model("xgboost_model:latest")

    @bentoml.api
    def predict_xgb(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """XGBoost prediction"""
        dmatrix = xgb.DMatrix(input_data)
        return self.model.predict(dmatrix)

    @bentoml.api
    def predict_xgb_binary(self, input_data: NumpyNdarray) -> JSON:
        """XGBoost binary classification"""
        dmatrix = xgb.DMatrix(input_data)
        predictions = self.model.predict(dmatrix)

        return {
            "predictions": (predictions > 0.5).astype(int).tolist(),
            "probabilities": predictions.tolist(),
            "threshold": 0.5
        }
```

## Multiple Framework Integration

### Ensemble Service

```python
@bentoml.service
class EnsembleService:
    def __init__(self):
        # Load models from different frameworks
        self.tf_model = bentoml.tensorflow.load_model("tf_model:latest")
        self.pytorch_model = bentoml.pytorch.load_model("pytorch_model:latest")
        self.sklearn_model = bentoml.sklearn.load_model("sklearn_model:latest")

    @bentoml.api
    def ensemble_predict(self, input_data: NumpyNdarray) -> JSON:
        """Ensemble prediction using multiple frameworks"""
        # TensorFlow prediction
        tf_pred = self.tf_model.predict(input_data)
        tf_class = np.argmax(tf_pred, axis=1)[0]

        # PyTorch prediction
        with torch.no_grad():
            torch_input = torch.from_numpy(input_data).float()
            torch_output = self.pytorch_model(torch_input)
            torch_class = torch.argmax(torch_output, dim=1).item()

        # Scikit-learn prediction
        sklearn_pred = self.sklearn_model.predict(input_data)[0]

        # Ensemble voting
        predictions = [tf_class, torch_class, sklearn_pred]
        final_prediction = max(set(predictions), key=predictions.count)

        return {
            "tensorflow_prediction": int(tf_class),
            "pytorch_prediction": int(torch_class),
            "sklearn_prediction": int(sklearn_pred),
            "ensemble_prediction": int(final_prediction),
            "agreement": len(set(predictions)) == 1
        }
```

## Custom Framework Integration

### Custom Model Loader

```python
import bentoml
from bentoml import Model
from typing import Any, Dict

class CustomModel:
    def __init__(self, model_path: str):
        # Load custom model
        self.model = self.load_custom_model(model_path)

    def load_custom_model(self, model_path: str):
        # Custom loading logic
        return load_model_from_path(model_path)

    def predict(self, input_data):
        # Custom prediction logic
        return self.model.predict(input_data)

# Custom BentoML integration
@bentoml.service
class CustomFrameworkService:
    def __init__(self):
        # Load custom model through BentoML
        self.model = CustomModel("path/to/custom/model")

    @bentoml.api
    def predict_custom(self, input_data: JSON) -> JSON:
        """Custom framework prediction"""
        result = self.model.predict(input_data["data"])
        return {"prediction": result}
```

## Framework-Specific Optimizations

### TensorFlow Optimizations

```python
@bentoml.service
class TensorFlowOptimizedService:
    def __init__(self):
        self.model = bentoml.tensorflow.load_model("tf_model:latest")

        # Enable optimizations
        tf.config.optimizer.set_jit(True)  # XLA compilation
        tf.config.threading.set_intra_op_parallelism_threads(4)
        tf.config.threading.set_inter_op_parallelism_threads(2)

    @bentoml.api
    def predict_optimized_tf(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """Optimized TensorFlow prediction"""
        @tf.function
        def optimized_predict(x):
            return self.model(x, training=False)

        return optimized_predict(input_data)
```

### PyTorch Optimizations

```python
@bentoml.service
class PyTorchOptimizedService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = bentoml.pytorch.load_model("pytorch_model:latest")

        self.model.to(self.device)
        self.model.eval()

        # Enable optimizations
        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True

    @bentoml.api
    def predict_optimized_torch(self, input_data: NumpyNdarray) -> NumpyNdarray:
        """Optimized PyTorch prediction"""
        with torch.no_grad():
            input_tensor = torch.from_numpy(input_data).float().to(self.device)

            # Use autocast for mixed precision
            with torch.cuda.amp.autocast():
                outputs = self.model(input_tensor)

            return outputs.cpu().numpy()
```

## Cross-Framework Pipelines

### Multi-Stage Pipeline

```python
@bentoml.service
class MultiStagePipelineService:
    def __init__(self):
        # Load different models for different stages
        self.preprocessor = bentoml.sklearn.load_model("preprocessor:latest")
        self.feature_extractor = bentoml.tensorflow.load_model("feature_extractor:latest")
        self.classifier = bentoml.pytorch.load_model("classifier:latest")

    @bentoml.api
    def predict_pipeline(self, input_data: JSON) -> JSON:
        """Multi-stage prediction pipeline"""
        raw_data = np.array(input_data["data"])

        # Stage 1: Preprocessing (Scikit-learn)
        preprocessed = self.preprocessor.transform(raw_data)

        # Stage 2: Feature extraction (TensorFlow)
        features = self.feature_extractor.predict(preprocessed)

        # Stage 3: Classification (PyTorch)
        with torch.no_grad():
            torch_features = torch.from_numpy(features).float()
            outputs = self.classifier(torch_features)
            predictions = torch.argmax(outputs, dim=1)

        return {
            "preprocessed_shape": preprocessed.shape,
            "features_shape": features.shape,
            "prediction": predictions.item(),
            "pipeline_stages": ["preprocessing", "feature_extraction", "classification"]
        }
```

## Model Version Management

### Version Comparison

```python
@bentoml.service
class VersionedService:
    def __init__(self):
        # Load multiple versions
        self.model_v1 = bentoml.sklearn.load_model("my_model:1.0.0")
        self.model_v2 = bentoml.sklearn.load_model("my_model:2.0.0")
        self.model_latest = bentoml.sklearn.load_model("my_model:latest")

    @bentoml.api
    def compare_versions(self, input_data: NumpyNdarray) -> JSON:
        """Compare predictions across model versions"""
        pred_v1 = self.model_v1.predict(input_data)
        pred_v2 = self.model_v2.predict(input_data)
        pred_latest = self.model_latest.predict(input_data)

        return {
            "version_1_0_0": pred_v1.tolist(),
            "version_2_0_0": pred_v2.tolist(),
            "latest": pred_latest.tolist(),
            "agreement": np.array_equal(pred_v1, pred_v2) and np.array_equal(pred_v2, pred_latest)
        }
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **TensorFlow Integration** - Basic and optimized TensorFlow models
2. **PyTorch Integration** - CPU and GPU-accelerated PyTorch models
3. **Scikit-learn Integration** - Traditional ML framework support
4. **XGBoost Integration** - Gradient boosting model support
5. **Multi-Framework Ensembles** - Combining models from different frameworks
6. **Custom Framework Support** - Integrating proprietary models
7. **Framework Optimizations** - Performance tuning for each framework
8. **Cross-Framework Pipelines** - Multi-stage processing pipelines
9. **Version Management** - Managing and comparing model versions

## Next Steps

Now that you understand framework integration, let's explore testing and validation strategies for your ML services. In [Chapter 5: Testing & Validation](05-testing-validation.md), we'll dive into comprehensive testing approaches, validation techniques, and quality assurance for ML services.

---

**Practice what you've learned:**
1. Integrate models from different ML frameworks
2. Create optimized services for specific frameworks
3. Build multi-stage processing pipelines
4. Implement version comparison and management

*Which ML framework do you use most frequently, and what optimizations would you like to implement?* 🧠

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `bentoml`, `model` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Framework Integration` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `input_data`, `torch`, `NumpyNdarray` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Framework Integration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `bentoml` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `model`.
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
- [Previous Chapter: Chapter 3: API Development](03-api-development.md)
- [Next Chapter: Chapter 5: Testing & Validation](05-testing-validation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
