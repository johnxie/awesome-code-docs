---
layout: default
title: "Chapter 3: API Development"
parent: "BentoML Tutorial"
nav_order: 3
---

# Chapter 3: API Development

Welcome to **Chapter 3: API Development**. In this part of **BentoML Tutorial: Building Production-Ready ML Services**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on creating robust, scalable APIs for your BentoML services. We'll explore different input/output formats, request handling, authentication, and advanced API features.

## API Input/Output Formats

### JSON APIs

```python
from bentoml.io import JSON
from typing import Dict, List, Any

@bentoml.service
class JSONAPIService:
    @bentoml.api
    def predict_json(self, input_data: JSON) -> JSON:
        """Handle JSON input and output"""
        features = input_data["features"]
        metadata = input_data.get("metadata", {})

        # Process features
        prediction = self.model.predict([features])

        return {
            "prediction": prediction.tolist()[0],
            "confidence": float(np.max(prediction)),
            "model_version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata
        }

    @bentoml.api
    def batch_predict_json(self, input_data: JSON) -> JSON:
        """Batch prediction with JSON"""
        features_list = input_data["features"]
        predictions = []

        for features in features_list:
            prediction = self.model.predict([features])
            predictions.append({
                "features": features,
                "prediction": prediction.tolist()[0],
                "confidence": float(np.max(prediction))
            })

        return {
            "predictions": predictions,
            "total_processed": len(predictions),
            "batch_id": str(uuid.uuid4())
        }
```

### NumPy Array APIs

```python
from bentoml.io import NumpyNdarray

@bentoml.service
class NumpyAPIService:
    @bentoml.api
    def predict_numpy(self, input_array: NumpyNdarray) -> NumpyNdarray:
        """Direct NumPy array processing"""
        return self.model.predict(input_array)

    @bentoml.api
    def predict_proba_numpy(self, input_array: NumpyNdarray) -> NumpyNdarray:
        """Prediction probabilities"""
        return self.model.predict_proba(input_array)

    @bentoml.api
    def transform_numpy(self, input_array: NumpyNdarray) -> NumpyNdarray:
        """Data transformation"""
        return self.preprocessor.transform(input_array)
```

### File Upload APIs

```python
from bentoml.io import File
import pandas as pd
import json

@bentoml.service
class FileAPIService:
    @bentoml.api
    def predict_csv(self, csv_file: File) -> JSON:
        """Process CSV file"""
        # Read CSV
        df = pd.read_csv(csv_file)

        # Preprocess
        processed_data = self.preprocessor.transform(df.values)

        # Predict
        predictions = self.model.predict(processed_data)

        return {
            "predictions": predictions.tolist(),
            "rows_processed": len(df),
            "columns": list(df.columns)
        }

    @bentoml.api
    def predict_json_file(self, json_file: File) -> JSON:
        """Process JSON file"""
        data = json.load(json_file)
        features = data["features"]

        prediction = self.model.predict([features])

        return {
            "prediction": prediction.tolist()[0],
            "original_data": data
        }
```

### Image APIs

```python
from bentoml.io import Image
import PIL.Image as PILImage

@bentoml.service
class ImageAPIService:
    @bentoml.api
    def classify_image(self, image: Image) -> JSON:
        """Image classification"""
        # Preprocess image
        processed_image = self.preprocess_image(image)

        # Classify
        prediction = self.model.predict(processed_image)

        return {
            "prediction": self.class_names[prediction[0]],
            "confidence": float(np.max(prediction)),
            "class_id": int(prediction[0])
        }

    @bentoml.api
    def detect_objects(self, image: Image) -> JSON:
        """Object detection"""
        # Run detection
        detections = self.detection_model.predict(image)

        return {
            "detections": detections,
            "count": len(detections)
        }

    def preprocess_image(self, image: Image):
        """Image preprocessing"""
        # Convert to PIL Image
        pil_image = PILImage.fromarray(image)

        # Resize and normalize
        processed = self.image_processor(pil_image)

        return processed
```

## Advanced API Features

### Authentication

```python
from functools import wraps
from bentoml.io import JSON
import jwt
import os

def require_auth(api_func):
    """Decorator for API authentication"""
    @wraps(api_func)
    def wrapper(*args, **kwargs):
        # Get request context
        request = bentoml.context.request

        # Check authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Authorization header required", "status": 401}

        try:
            # Decode JWT token
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])

            # Add user info to context
            bentoml.context.user = payload

        except jwt.ExpiredSignatureError:
            return {"error": "Token expired", "status": 401}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token", "status": 401}

        return api_func(*args, **kwargs)

    return wrapper

@bentoml.service
class AuthenticatedService:
    @bentoml.api
    @require_auth
    def predict_secure(self, input_data: JSON) -> JSON:
        """Secure prediction endpoint"""
        user = bentoml.context.user

        # Log user action
        self.logger.info(f"Prediction by user {user['user_id']}")

        prediction = self.model.predict([input_data["features"]])

        return {
            "prediction": prediction.tolist()[0],
            "user_id": user["user_id"],
            "timestamp": datetime.now().isoformat()
        }
```

### Rate Limiting

```python
from collections import defaultdict
import time
from bentoml.io import JSON

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.user_requests = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        user_reqs = self.user_requests[user_id]

        # Remove old requests
        user_reqs[:] = [req for req in user_reqs if now - req < 60]

        if len(user_reqs) >= self.requests_per_minute:
            return False

        user_reqs.append(now)
        return True

@bentoml.service
class RateLimitedService:
    def __init__(self):
        self.rate_limiter = RateLimiter(requests_per_minute=30)

    @bentoml.api
    def predict_rate_limited(self, input_data: JSON) -> JSON:
        """Rate limited prediction"""
        user_id = input_data.get("user_id", "anonymous")

        if not self.rate_limiter.is_allowed(user_id):
            return {
                "error": "Rate limit exceeded",
                "retry_after": 60,
                "status": 429
            }

        prediction = self.model.predict([input_data["features"]])

        return {
            "prediction": prediction.tolist()[0],
            "user_id": user_id
        }
```

### Request Validation

```python
from pydantic import BaseModel, validator
from typing import List, Optional
from bentoml.io import JSON

class PredictionRequest(BaseModel):
    features: List[float]
    user_id: Optional[str] = None
    metadata: Optional[dict] = {}

    @validator('features')
    def validate_features(cls, v):
        if len(v) != 20:
            raise ValueError('Features must have exactly 20 values')
        if not all(-10 <= x <= 10 for x in v):
            raise ValueError('Feature values must be between -10 and 10')
        return v

class BatchPredictionRequest(BaseModel):
    requests: List[PredictionRequest]
    priority: Optional[str] = "normal"

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ["low", "normal", "high"]:
            raise ValueError('Priority must be low, normal, or high')
        return v

@bentoml.service
class ValidatedAPIService:
    @bentoml.api
    def predict_validated(self, request: JSON) -> JSON:
        """Validated prediction endpoint"""
        try:
            # Validate request
            pred_request = PredictionRequest(**request)

            # Make prediction
            prediction = self.model.predict([pred_request.features])

            return {
                "prediction": prediction.tolist()[0],
                "user_id": pred_request.user_id,
                "validated": True
            }

        except Exception as e:
            return {
                "error": str(e),
                "status": 400
            }

    @bentoml.api
    def batch_predict_validated(self, request: JSON) -> JSON:
        """Validated batch prediction"""
        try:
            batch_request = BatchPredictionRequest(**request)

            predictions = []
            for pred_request in batch_request.requests:
                prediction = self.model.predict([pred_request.features])
                predictions.append({
                    "prediction": prediction.tolist()[0],
                    "user_id": pred_request.user_id
                })

            return {
                "predictions": predictions,
                "batch_size": len(predictions),
                "priority": batch_request.priority
            }

        except Exception as e:
            return {
                "error": str(e),
                "status": 400
            }
```

## API Versioning

```python
@bentoml.service(name="ml-service", version="1.0.0")
class VersionedServiceV1:
    @bentoml.api
    def predict_v1(self, input_data: JSON) -> JSON:
        """Version 1 prediction"""
        return {"version": "1.0.0", "prediction": 0.8}

@bentoml.service(name="ml-service", version="2.0.0")
class VersionedServiceV2:
    @bentoml.api
    def predict_v2(self, input_data: JSON) -> JSON:
        """Version 2 prediction with confidence"""
        return {
            "version": "2.0.0",
            "prediction": 0.8,
            "confidence": 0.95
        }

    @bentoml.api
    def predict_v1_compatible(self, input_data: JSON) -> JSON:
        """Backward compatible endpoint"""
        result = self.predict_v2(input_data)
        # Return only version 1 fields
        return {"version": "1.0.0", "prediction": result["prediction"]}
```

## Streaming APIs

```python
from bentoml.io import JSON
import asyncio
import json

@bentoml.service
class StreamingService:
    @bentoml.api
    def predict_streaming(self, input_data: JSON) -> JSON:
        """Streaming prediction results"""
        def generate_predictions():
            batch_size = 10
            data = input_data["data"]

            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                predictions = self.model.predict(batch)

                yield {
                    "batch": i // batch_size,
                    "predictions": predictions.tolist(),
                    "progress": min(100, ((i + len(batch)) / len(data)) * 100)
                }

        results = list(generate_predictions())
        return {"results": results}

    @bentoml.api
    async def predict_async(self, input_data: JSON) -> JSON:
        """Asynchronous prediction"""
        # Simulate async processing
        await asyncio.sleep(0.1)

        prediction = self.model.predict([input_data["features"]])

        return {
            "prediction": prediction.tolist()[0],
            "processing_time": 0.1
        }
```

## Documentation

### Auto-generated API Docs

```python
@bentoml.service(
    name="documented-service",
    description="A well-documented ML service"
)
class DocumentedService:
    @bentoml.api(
        description="Predict using trained model",
        example={
            "input_data": {
                "features": [1.2, 3.4, 5.6, 7.8, 9.0],
                "user_id": "user123"
            }
        }
    )
    def predict_documented(self, input_data: JSON) -> JSON:
        """
        Make a prediction using the trained model.

        This endpoint accepts feature data and returns predictions
        with confidence scores and additional metadata.

        Args:
            input_data: JSON object containing features and optional metadata

        Returns:
            JSON object with prediction results
        """
        features = input_data["features"]
        prediction = self.model.predict([features])

        return {
            "prediction": prediction.tolist()[0],
            "confidence": float(np.max(prediction)),
            "model_info": {
                "name": "Random Forest Classifier",
                "version": "1.0.0",
                "accuracy": 0.95
            }
        }
```

### Custom OpenAPI Documentation

```python
from bentoml.openapi import OpenAPI

@bentoml.service
class CustomDocsService:
    def customize_openapi(self, openapi: OpenAPI) -> OpenAPI:
        """Customize OpenAPI documentation"""
        # Add security schemes
        openapi.components.securitySchemes = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        # Add global security
        openapi.security = [{"bearerAuth": []}]

        # Customize response schemas
        openapi.components.schemas["PredictionResponse"] = {
            "type": "object",
            "properties": {
                "prediction": {"type": "number"},
                "confidence": {"type": "number"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        }

        return openapi
```

## Error Handling and Status Codes

```python
@bentoml.service
class RobustAPIService:
    @bentoml.api
    def predict_with_status(self, input_data: JSON):
        """Prediction with custom status codes"""
        try:
            if not self.validate_input(input_data):
                # Return 400 Bad Request
                bentoml.context.response.status_code = 400
                return {"error": "Invalid input data"}

            prediction = self.model.predict([input_data["features"]])

            # Return 200 OK with result
            return {
                "prediction": prediction.tolist()[0],
                "status": "success"
            }

        except ModelLoadError:
            # Return 503 Service Unavailable
            bentoml.context.response.status_code = 503
            return {"error": "Model temporarily unavailable"}

        except Exception as e:
            # Return 500 Internal Server Error
            bentoml.context.response.status_code = 500
            return {"error": "Internal server error"}

    def validate_input(self, data):
        """Input validation"""
        required_fields = ["features"]
        if not all(field in data for field in required_fields):
            return False

        if not isinstance(data["features"], list):
            return False

        if len(data["features"]) != 20:
            return False

        return True
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned:

1. **Multiple API Formats** - JSON, NumPy, File, and Image APIs
2. **Authentication** - JWT-based authentication for secure APIs
3. **Rate Limiting** - Protecting APIs from abuse
4. **Request Validation** - Pydantic-based input validation
5. **API Versioning** - Managing multiple API versions
6. **Streaming APIs** - Real-time response streaming
7. **Documentation** - Auto-generated and custom API docs
8. **Error Handling** - Comprehensive error handling with status codes

## Next Steps

Now that you understand advanced API development, let's explore how to integrate BentoML with different ML frameworks. In [Chapter 4: Framework Integration](04-framework-integration.md), we'll dive into working with TensorFlow, PyTorch, Scikit-learn, and other popular ML frameworks.

---

**Practice what you've learned:**
1. Create APIs with different input/output formats
2. Implement authentication and rate limiting
3. Add comprehensive request validation
4. Create versioned APIs with backward compatibility

*What's the most complex API you've designed for an ML service?* 🔌

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `prediction`, `bentoml` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: API Development` as an operating subsystem inside **BentoML Tutorial: Building Production-Ready ML Services**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `JSON`, `features`, `input_data` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: API Development` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `prediction` receives stable contracts.
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
- search upstream code for `self` and `prediction` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Model Packaging & Services](02-model-packaging.md)
- [Next Chapter: Chapter 4: Framework Integration](04-framework-integration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
