---
layout: default
title: "Chapter 2: Text Classification & Analysis"
parent: "HuggingFace Transformers Tutorial"
nav_order: 2
---

# Chapter 2: Text Classification & Analysis

Welcome to **Chapter 2: Text Classification & Analysis**. In this part of **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Welcome back! Now that you understand the basics of HuggingFace Transformers, let's dive into one of the most powerful and widely-used applications: **text classification**. From sentiment analysis to topic categorization, text classification powers many real-world AI applications.

## Understanding Text Classification

### What is Text Classification?

Text classification is the process of categorizing text documents into predefined classes or categories. It's one of the fundamental tasks in natural language processing and has applications in:

- **Sentiment Analysis**: Positive, negative, or neutral opinions
- **Topic Classification**: News categorization, content tagging
- **Intent Detection**: Understanding user intent in chatbots
- **Language Detection**: Identifying the language of text
- **Spam Detection**: Filtering unwanted content

### Classification Pipeline

```python
from transformers import pipeline
import torch

# Create classification pipeline
classifier = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
    device=0 if torch.cuda.is_available() else -1
)

# Classify text
result = classifier("I love using HuggingFace Transformers!")
print(result)
# Output: [{'label': 'LABEL_2', 'score': 0.8956}]
```

## Sentiment Analysis

### Building a Sentiment Classifier

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Get label mapping
        self.label_mapping = {
            0: "negative",
            1: "neutral",
            2: "positive"
        }

    def analyze_sentiment(self, text):
        """Analyze sentiment of input text"""
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Get predicted class and confidence
        predicted_class = torch.argmax(predictions, dim=-1).item()
        confidence = predictions[0][predicted_class].item()

        return {
            "sentiment": self.label_mapping[predicted_class],
            "confidence": confidence,
            "probabilities": {
                "negative": predictions[0][0].item(),
                "neutral": predictions[0][1].item(),
                "positive": predictions[0][2].item()
            }
        }

# Usage
analyzer = SentimentAnalyzer()
result = analyzer.analyze_sentiment("I absolutely love this new feature!")
print(result)
```

### Advanced Sentiment Analysis

```python
class AdvancedSentimentAnalyzer:
    def __init__(self):
        # Use multiple models for better accuracy
        self.models = {
            "twitter": SentimentAnalyzer("cardiffnlp/twitter-roberta-base-sentiment-latest"),
            "general": SentimentAnalyzer("j-hartmann/sentiment-roberta-large-english-3-classes"),
            "financial": SentimentAnalyzer("ProsusAI/finbert")  # For financial text
        }

    def analyze_comprehensive(self, text, domain="general"):
        """Comprehensive sentiment analysis with multiple models"""
        results = {}

        # Get results from all models
        for model_name, analyzer in self.models.items():
            try:
                result = analyzer.analyze_sentiment(text)
                results[model_name] = result
            except Exception as e:
                results[model_name] = {"error": str(e)}

        # Ensemble prediction
        ensemble_result = self._ensemble_prediction(results, domain)

        return {
            "individual_results": results,
            "ensemble_prediction": ensemble_result,
            "confidence_score": self._calculate_confidence(results)
        }

    def _ensemble_prediction(self, results, domain):
        """Combine predictions from multiple models"""
        sentiments = []
        confidences = []

        for model_name, result in results.items():
            if "error" not in result:
                sentiments.append(result["sentiment"])
                confidences.append(result["confidence"])

        # Majority voting with confidence weighting
        sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}

        for sentiment, confidence in zip(sentiments, confidences):
            sentiment_scores[sentiment] += confidence

        final_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        final_confidence = sentiment_scores[final_sentiment] / sum(confidences)

        return {
            "sentiment": final_sentiment,
            "confidence": final_confidence
        }

    def _calculate_confidence(self, results):
        """Calculate overall confidence in ensemble prediction"""
        valid_results = [r for r in results.values() if "error" not in r]
        if not valid_results:
            return 0.0

        # Average confidence across all models
        return sum(r["confidence"] for r in valid_results) / len(valid_results)

# Usage
advanced_analyzer = AdvancedSentimentAnalyzer()
result = advanced_analyzer.analyze_comprehensive(
    "The company's Q4 results exceeded expectations, stock is up 15%!",
    domain="financial"
)
print(result)
```

## Topic Classification

### Building a Topic Classifier

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import torch

class TopicClassifier:
    def __init__(self, model_name="facebook/bart-large-mnli"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Define topics
        self.topics = [
            "technology", "business", "politics", "sports", "entertainment",
            "science", "health", "education", "environment", "finance"
        ]

    def classify_topic(self, text, candidate_topics=None):
        """Classify the main topic of the text"""
        if candidate_topics is None:
            candidate_topics = self.topics

        # Prepare input
        premise = text
        hypothesis_template = "This text is about {}."

        # Calculate entailment scores for each topic
        topic_scores = {}

        for topic in candidate_topics:
            hypothesis = hypothesis_template.format(topic)

            # Tokenize
            inputs = self.tokenizer(
                premise, hypothesis,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.nn.functional.softmax(logits, dim=-1)

            # Entailment score (index 2 for entailment)
            entailment_score = probs[0][2].item()
            topic_scores[topic] = entailment_score

        # Get best topic
        best_topic = max(topic_scores, key=topic_scores.get)
        confidence = topic_scores[best_topic]

        return {
            "topic": best_topic,
            "confidence": confidence,
            "all_scores": topic_scores
        }

# Usage
topic_classifier = TopicClassifier()
result = topic_classifier.classify_topic(
    "Apple announces new M3 chip with revolutionary AI capabilities for MacBook Pro"
)
print(result)
```

## Multi-Label Classification

### Building a Multi-Label Classifier

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class MultiLabelClassifier:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        # For multi-label, we use a model fine-tuned for the task
        # This is a simplified example - in practice you'd use a proper multi-label model
        self.model_name = model_name
        self.labels = ["urgent", "technical", "business", "personal", "question", "complaint"]

    def classify_multiple_labels(self, text):
        """Classify text with multiple possible labels"""
        # This is a simplified implementation
        # In practice, you'd use a model specifically trained for multi-label classification

        results = {}

        # Check each label individually (simplified approach)
        for label in self.labels:
            # Use simple keyword matching for demonstration
            score = self._calculate_label_score(text, label)
            results[label] = score

        # Filter significant labels
        significant_labels = {
            label: score for label, score in results.items()
            if score > 0.3  # Threshold
        }

        return {
            "labels": significant_labels,
            "primary_label": max(significant_labels, key=significant_labels.get) if significant_labels else None
        }

    def _calculate_label_score(self, text, label):
        """Calculate relevance score for a label (simplified)"""
        text_lower = text.lower()
        label_keywords = {
            "urgent": ["urgent", "asap", "emergency", "immediate", "critical"],
            "technical": ["bug", "error", "code", "server", "database", "api"],
            "business": ["meeting", "proposal", "contract", "revenue", "client"],
            "personal": ["vacation", "sick", "personal", "family", "leave"],
            "question": ["what", "how", "why", "when", "where", "?", "help"],
            "complaint": ["problem", "issue", "wrong", "bad", "terrible", "disappointed"]
        }

        keywords = label_keywords.get(label, [])
        matches = sum(1 for keyword in keywords if keyword in text_lower)

        return min(matches / len(keywords), 1.0) if keywords else 0.0

# Usage
multi_classifier = MultiLabelClassifier()
result = multi_classifier.classify_multiple_labels(
    "Urgent: Server is down and affecting all customers. Need immediate technical assistance!"
)
print(result)
```

## Performance Optimization

### Batch Processing

```python
class BatchTextClassifier:
    def __init__(self, classifier):
        self.classifier = classifier
        self.batch_size = 32

    def classify_batch(self, texts):
        """Classify multiple texts efficiently"""
        results = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]

            # Classify batch
            batch_results = []
            for text in batch:
                result = self.classifier.classify(text)
                batch_results.append(result)

            results.extend(batch_results)

        return results

    async def classify_batch_async(self, texts):
        """Async batch processing for better performance"""
        import asyncio

        # Create tasks for parallel processing
        tasks = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            task = asyncio.create_task(self._process_batch_async(batch))
            tasks.append(task)

        # Wait for all batches to complete
        batch_results = await asyncio.gather(*tasks)

        # Flatten results
        return [result for batch in batch_results for result in batch]

    async def _process_batch_async(self, batch):
        """Process a single batch asynchronously"""
        # Implementation would use async-compatible classification
        return [self.classifier.classify(text) for text in batch]

# Usage
batch_classifier = BatchTextClassifier(sentiment_analyzer)
texts = ["Great product!", "Terrible service", "Okay experience"]
results = batch_classifier.classify_batch(texts)
print(results)
```

## Integration with Modern Applications

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Text Classification API")

class ClassificationRequest(BaseModel):
    text: str
    task: str = "sentiment"  # sentiment, topic, etc.

class BatchClassificationRequest(BaseModel):
    texts: List[str]
    task: str = "sentiment"

@app.post("/classify")
async def classify_text(request: ClassificationRequest):
    """Classify a single text"""
    try:
        if request.task == "sentiment":
            result = sentiment_analyzer.analyze_sentiment(request.text)
        elif request.task == "topic":
            result = topic_classifier.classify_topic(request.text)
        else:
            raise HTTPException(status_code=400, detail="Unsupported task")

        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify/batch")
async def classify_batch(request: BatchClassificationRequest):
    """Classify multiple texts"""
    try:
        batch_classifier = BatchTextClassifier(sentiment_analyzer)
        results = batch_classifier.classify_batch(request.texts)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## What We've Accomplished

✅ **Mastered text classification** with HuggingFace Transformers
✅ **Built sentiment analysis** systems with multiple models
✅ **Created topic classification** for content categorization
✅ **Implemented multi-label classification** for complex scenarios
✅ **Optimized performance** with batch processing
✅ **Integrated with modern applications** via REST APIs

## Next Steps

Ready to generate text with AI? In [Chapter 3: Text Generation](03-text-generation.md), we'll explore how to build creative writing assistants, code generators, and conversational AI systems using HuggingFace models.

---

**Key Takeaway:** Text classification is the foundation of many AI applications. With HuggingFace Transformers, you can build sophisticated classification systems that rival commercial offerings, all while maintaining full control over your models and data.

*Classification powers everything from spam filters to recommendation systems—master it and unlock countless AI applications!*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `text`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Text Classification & Analysis` as an operating subsystem inside **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `results`, `sentiment`, `confidence` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Text Classification & Analysis` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/huggingface/transformers)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with HuggingFace Transformers](01-getting-started.md)
- [Next Chapter: Chapter 3: Text Generation](03-text-generation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
