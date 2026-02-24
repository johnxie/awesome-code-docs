---
layout: default
title: "Chapter 4: Question Answering"
parent: "HuggingFace Transformers Tutorial"
nav_order: 4
---

# Chapter 4: Question Answering

Welcome to **Chapter 4: Question Answering**. In this part of **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build intelligent Q&A systems that can answer questions from documents and knowledge bases.

## 🎯 Overview

This chapter covers question answering (QA) systems using HuggingFace Transformers. You'll learn to build extractive and generative QA models, create custom knowledge bases, and deploy QA systems that can answer questions from your own documents.

## ❓ Types of Question Answering

### Extractive QA
- Finds and extracts answer spans directly from text
- Most accurate for fact-based questions
- Requires labeled training data

### Generative QA
- Generates answers using language models
- More flexible, can handle complex questions
- Can synthesize information from multiple sources

### Closed-Book QA
- Answers questions using model's internal knowledge
- No external context provided
- Good for general knowledge questions

### Open-Book QA
- Uses provided context or knowledge base
- More accurate and up-to-date
- Requires retrieval systems

## 📖 Extractive Question Answering

### Using Pre-trained QA Models

```python
from transformers import pipeline

# Initialize QA pipeline
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-uncased-distilled-squad",
    tokenizer="distilbert-base-uncased-distilled-squad"
)

# Example context and question
context = """
The HuggingFace Transformers library is an open-source library for natural language processing.
It provides thousands of pre-trained models for tasks like text classification, question answering,
text generation, and more. The library is built on top of PyTorch and TensorFlow, making it easy
to integrate into existing machine learning workflows.
"""

question = "What is HuggingFace Transformers?"

# Get answer
result = qa_pipeline(question=question, context=context)
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['score']:.4f}")
print(f"Position: {result['start']} to {result['end']}")
# Answer: an open-source library for natural language processing
# Confidence: 0.9876
# Position: 4 to 58
```

### Advanced Extractive QA

```python
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

class AdvancedQASystem:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.max_length = 512

    def answer_question(self, question, context, return_all_answers=False):
        """Answer a question given context"""
        # Tokenize input
        inputs = self.tokenizer(
            question,
            context,
            max_length=self.max_length,
            truncation=True,
            padding=True,
            return_tensors="pt"
        )

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get start and end logits
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits

        # Get answer span
        start_idx = torch.argmax(start_logits)
        end_idx = torch.argmax(end_logits) + 1

        # Convert to text
        answer_tokens = inputs.input_ids[0][start_idx:end_idx]
        answer = self.tokenizer.decode(answer_tokens, skip_special_tokens=True)

        # Calculate confidence
        start_prob = torch.softmax(start_logits, dim=1)[0][start_idx]
        end_prob = torch.softmax(end_logits, dim=1)[0][end_idx-1]
        confidence = (start_prob * end_prob).item()

        # Handle impossible answers (for SQuAD 2.0 models)
        if answer.strip() == "" or confidence < 0.1:
            return {
                "answer": "I cannot find a confident answer to this question.",
                "confidence": 0.0,
                "start": 0,
                "end": 0
            }

        return {
            "answer": answer,
            "confidence": confidence,
            "start": start_idx.item(),
            "end": end_idx.item()
        }

    def batch_answer(self, questions, contexts):
        """Answer multiple questions efficiently"""
        results = []
        for question, context in zip(questions, contexts):
            result = self.answer_question(question, context)
            results.append(result)
        return results

# Usage
qa_system = AdvancedQASystem()

questions = [
    "What is machine learning?",
    "How does neural networks work?",
    "What are transformers in AI?"
]

contexts = [
    "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
    "Neural networks are computing systems inspired by biological neural networks that can learn from data.",
    "Transformers are a type of neural network architecture that uses self-attention mechanisms for processing sequential data."
]

results = qa_system.batch_answer(questions, contexts)
for q, r in zip(questions, results):
    print(f"Q: {q}")
    print(f"A: {r['answer']} (confidence: {r['confidence']:.3f})")
    print("---")
```

## 🤖 Generative Question Answering

### Using Language Models for QA

```python
from transformers import pipeline
import torch

class GenerativeQASystem:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.qa_pipeline = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.context_window = 1024

    def answer_with_context(self, question, context):
        """Answer question using provided context"""
        # Prepare prompt with context
        prompt = f"""
Based on the following context, answer the question accurately and concisely.

Context:
{context[:self.context_window]}

Question: {question}

Answer:"""

        # Generate answer
        response = self.qa_pipeline(
            prompt,
            max_length=len(prompt.split()) + 100,
            num_return_sequences=1,
            temperature=0.3,  # Lower temperature for factual answers
            do_sample=True,
            pad_token_id=self.qa_pipeline.tokenizer.eos_token_id
        )

        # Extract answer
        generated_text = response[0]['generated_text']
        answer = generated_text.split("Answer:")[-1].strip()

        return answer

    def answer_without_context(self, question):
        """Answer using model's internal knowledge"""
        prompt = f"Question: {question}\nAnswer:"

        response = self.qa_pipeline(
            prompt,
            max_length=200,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )

        answer = response[0]['generated_text'].split("Answer:")[-1].strip()
        return answer

# Usage
gen_qa = GenerativeQASystem()

# With context
context = "The Python programming language was created by Guido van Rossum and first released in 1991."
question = "Who created Python?"
answer = gen_qa.answer_with_context(question, context)
print(f"With context: {answer}")

# Without context
question = "What is the capital of France?"
answer = gen_qa.answer_without_context(question)
print(f"Without context: {answer}")
```

## 📚 Building Custom Knowledge Bases

### Document-Based QA System

```python
from transformers import DPRQuestionEncoder, DPRContextEncoder, DPRQuestionEncoderTokenizer, DPRContextEncoderTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import faiss

class DocumentQASystem:
    def __init__(self):
        # Initialize DPR models for retrieval
        self.q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
        self.ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
        self.q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
        self.ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

        # Initialize FAISS index for efficient search
        self.dimension = 768  # DPR embedding dimension
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity

        # Storage for documents and metadata
        self.documents = []
        self.doc_embeddings = []
        self.metadata = []

    def add_documents(self, documents, metadata=None):
        """Add documents to the knowledge base"""
        if metadata is None:
            metadata = [{}] * len(documents)

        # Encode documents
        doc_embeddings = []
        for doc in documents:
            inputs = self.ctx_tokenizer(doc, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                embedding = self.ctx_encoder(**inputs).pooler_output.numpy()
            doc_embeddings.append(embedding[0])

        # Normalize embeddings for cosine similarity
        doc_embeddings = np.array(doc_embeddings)
        norms = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
        doc_embeddings = doc_embeddings / norms

        # Add to FAISS index
        self.index.add(doc_embeddings.astype('float32'))

        # Store documents and metadata
        self.documents.extend(documents)
        self.doc_embeddings.extend(doc_embeddings)
        self.metadata.extend(metadata)

    def retrieve_documents(self, question, top_k=5):
        """Retrieve relevant documents for a question"""
        # Encode question
        inputs = self.q_tokenizer(question, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            q_embedding = self.q_encoder(**inputs).pooler_output.numpy()

        # Normalize question embedding
        q_embedding = q_embedding / np.linalg.norm(q_embedding)

        # Search in FAISS index
        scores, indices = self.index.search(q_embedding.astype('float32'), top_k)

        # Retrieve documents
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):  # Valid index
                results.append({
                    "document": self.documents[idx],
                    "score": float(score),
                    "metadata": self.metadata[idx]
                })

        return results

    def answer_question(self, question, qa_system=None):
        """Answer question using retrieved documents"""
        # Retrieve relevant documents
        relevant_docs = self.retrieve_documents(question, top_k=3)

        if not relevant_docs:
            return "No relevant information found."

        # Combine top documents as context
        context = "\n\n".join([doc["document"] for doc in relevant_docs[:2]])

        # Use QA system to answer
        if qa_system:
            answer = qa_system.answer_with_context(question, context)
        else:
            # Simple extraction-based answer
            answer = self._extract_answer(question, context)

        return {
            "answer": answer,
            "sources": relevant_docs,
            "context": context
        }

    def _extract_answer(self, question, context):
        """Simple answer extraction (fallback)"""
        # This is a basic implementation - use a proper QA model for better results
        sentences = context.split('.')
        relevant_sentences = [s.strip() for s in sentences if any(word.lower() in s.lower() for word in question.split())]

        return '. '.join(relevant_sentences[:2]) if relevant_sentences else "Information found but unable to extract concise answer."

# Usage
qa_kb = DocumentQASystem()

# Add documents
documents = [
    "Python is a high-level programming language created by Guido van Rossum in 1991.",
    "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
    "Neural networks are computing systems inspired by biological neural networks.",
    "HuggingFace Transformers is a library for natural language processing built on PyTorch."
]

qa_kb.add_documents(documents)

# Answer questions
question = "Who created Python?"
result = qa_kb.answer_question(question)
print(f"Question: {question}")
print(f"Answer: {result['answer']}")
print(f"Sources found: {len(result['sources'])}")
```

## 🔍 Multi-Hop Question Answering

### Complex Reasoning QA

```python
from transformers import pipeline
import re

class MultiHopQASystem:
    def __init__(self):
        self.qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
        self.decomposer = QuestionDecomposer()

    def answer_complex_question(self, question, knowledge_base):
        """Answer complex questions that require multiple reasoning steps"""
        # Decompose complex question into simpler sub-questions
        sub_questions = self.decomposer.decompose(question)

        # Answer each sub-question
        intermediate_answers = {}
        for sub_q in sub_questions:
            answer = self._answer_sub_question(sub_q, knowledge_base)
            intermediate_answers[sub_q] = answer

        # Synthesize final answer from intermediate answers
        final_answer = self._synthesize_answer(question, intermediate_answers)

        return {
            "final_answer": final_answer,
            "intermediate_answers": intermediate_answers,
            "reasoning_chain": sub_questions
        }

    def _answer_sub_question(self, sub_question, knowledge_base):
        """Answer a single sub-question"""
        # Search for relevant information
        relevant_docs = knowledge_base.retrieve_documents(sub_question, top_k=2)

        if not relevant_docs:
            return "No information found"

        # Combine contexts
        context = "\n".join([doc["document"] for doc in relevant_docs])

        # Answer using QA model
        result = self.qa_model(question=sub_question, context=context)
        return result["answer"]

    def _synthesize_answer(self, original_question, intermediate_answers):
        """Synthesize final answer from intermediate answers"""
        # Combine intermediate answers coherently
        answers = list(intermediate_answers.values())

        # Simple synthesis - can be enhanced with more sophisticated methods
        if len(answers) == 1:
            return answers[0]
        elif len(answers) == 2:
            return f"{answers[0]}, and {answers[1]}"
        else:
            return ". ".join(answers)

class QuestionDecomposer:
    def __init__(self):
        self.patterns = {
            "comparison": r"(?:compare|difference between|vs\.?|versus)",
            "cause_effect": r"(?:because|why|cause|effect|reason)",
            "temporal": r"(?:before|after|when|timeline|history)",
            "quantitative": r"(?:how many|how much|percentage|amount)"
        }

    def decompose(self, question):
        """Decompose complex question into simpler sub-questions"""
        question_lower = question.lower()

        sub_questions = []

        # Check for comparison questions
        if re.search(self.patterns["comparison"], question_lower):
            parts = re.split(r"(?:vs\.?|versus|and)", question_lower, flags=re.IGNORECASE)
            if len(parts) >= 2:
                sub_questions.extend([f"What is {part.strip()}?" for part in parts[:2]])

        # Check for cause/effect questions
        elif re.search(self.patterns["cause_effect"], question_lower):
            sub_questions.append(f"What causes {question.replace('why', '').replace('because', '').strip()}?")
            sub_questions.append(f"What are the effects of {question.replace('why', '').replace('because', '').strip()}?")

        # Check for temporal questions
        elif re.search(self.patterns["temporal"], question_lower):
            sub_questions.append(f"When did {question.replace('when', '').strip()} happen?")
            sub_questions.append(f"What was the timeline of {question.replace('when', '').strip()}?")

        # Default: single question
        if not sub_questions:
            sub_questions = [question]

        return sub_questions

# Usage
multi_hop_qa = MultiHopQASystem()

complex_question = "Why was Python created and how has it evolved?"
result = multi_hop_qa.answer_complex_question(complex_question, qa_kb)

print(f"Complex Question: {complex_question}")
print(f"Final Answer: {result['final_answer']}")
print(f"Reasoning Steps: {result['reasoning_chain']}")
```

## 🎯 Specialized QA Applications

### Medical QA System

```python
class MedicalQASystem:
    def __init__(self):
        self.qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
        self.confidence_threshold = 0.7
        self.disclaimer = "This is not medical advice. Please consult a healthcare professional."

    def answer_medical_question(self, question, patient_context=""):
        """Answer medical questions with appropriate disclaimers"""
        # Check if question requires professional medical advice
        if self._requires_professional_advice(question):
            return {
                "answer": "This question requires consultation with a qualified healthcare professional.",
                "disclaimer": self.disclaimer,
                "professional_advice": True
            }

        # Search medical knowledge base
        relevant_info = self._search_medical_kb(question, patient_context)

        if not relevant_info:
            return {
                "answer": "I don't have sufficient information to answer this question accurately.",
                "disclaimer": self.disclaimer
            }

        # Generate answer
        context = relevant_info["context"]
        result = self.qa_model(question=question, context=context)

        if result["score"] < self.confidence_threshold:
            return {
                "answer": "I found some information but I'm not confident in the accuracy.",
                "disclaimer": self.disclaimer,
                "confidence": result["score"]
            }

        return {
            "answer": result["answer"],
            "disclaimer": self.disclaimer,
            "confidence": result["score"],
            "source": relevant_info["source"]
        }

    def _requires_professional_advice(self, question):
        """Check if question requires professional medical advice"""
        professional_indicators = [
            "diagnosis", "treatment", "medication", "symptoms",
            "pain", "illness", "disease", "emergency"
        ]

        question_lower = question.lower()
        return any(indicator in question_lower for indicator in professional_indicators)

    def _search_medical_kb(self, question, patient_context):
        """Search medical knowledge base"""
        # This would integrate with a medical knowledge base
        # For demo purposes, using placeholder
        return {
            "context": "Medical information would be retrieved from trusted sources.",
            "source": "Medical Knowledge Base"
        }

# Usage
medical_qa = MedicalQASystem()

questions = [
    "What are the symptoms of the flu?",
    "Should I take aspirin for a headache?"
]

for question in questions:
    result = medical_qa.answer_medical_question(question)
    print(f"Q: {question}")
    print(f"A: {result['answer']}")
    if 'disclaimer' in result:
        print(f"Disclaimer: {result['disclaimer']}")
    print("---")
```

## 📊 Evaluation and Metrics

### QA System Evaluation

```python
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

class QAEvaluator:
    def __init__(self):
        self.metrics = []

    def evaluate_predictions(self, predictions, ground_truths):
        """Evaluate QA predictions against ground truth"""
        exact_matches = []
        f1_scores = []

        for pred, gt in zip(predictions, ground_truths):
            # Exact match
            em = self._exact_match(pred["answer"], gt["answer"])
            exact_matches.append(em)

            # F1 score
            f1 = self._f1_score(pred["answer"], gt["answer"])
            f1_scores.append(f1)

            # Store individual results
            self.metrics.append({
                "question": pred["question"],
                "predicted": pred["answer"],
                "ground_truth": gt["answer"],
                "exact_match": em,
                "f1_score": f1,
                "confidence": pred.get("confidence", 0)
            })

        return {
            "exact_match": np.mean(exact_matches),
            "f1_score": np.mean(f1_scores),
            "total_questions": len(predictions)
        }

    def _exact_match(self, prediction, ground_truth):
        """Calculate exact match score"""
        return prediction.strip().lower() == ground_truth.strip().lower()

    def _f1_score(self, prediction, ground_truth):
        """Calculate F1 score for token overlap"""
        pred_tokens = set(prediction.lower().split())
        gt_tokens = set(ground_truth.lower().split())

        if len(pred_tokens) == 0 and len(gt_tokens) == 0:
            return 1.0

        intersection = pred_tokens & gt_tokens
        if len(intersection) == 0:
            return 0.0

        precision = len(intersection) / len(pred_tokens)
        recall = len(intersection) / len(gt_tokens)

        return 2 * (precision * recall) / (precision + recall)

    def analyze_errors(self):
        """Analyze common error patterns"""
        errors = [m for m in self.metrics if not m["exact_match"]]

        error_analysis = {
            "total_errors": len(errors),
            "low_confidence_errors": len([e for e in errors if e["confidence"] < 0.5]),
            "high_confidence_errors": len([e for e in errors if e["confidence"] > 0.8]),
            "error_patterns": self._identify_error_patterns(errors)
        }

        return error_analysis

    def _identify_error_patterns(self, errors):
        """Identify common error patterns"""
        patterns = {
            "partial_answer": 0,
            "wrong_entity": 0,
            "context_mismatch": 0,
            "spelling_errors": 0
        }

        # Simple pattern detection - can be enhanced
        for error in errors:
            pred, gt = error["predicted"], error["ground_truth"]
            if len(pred.split()) < len(gt.split()) * 0.5:
                patterns["partial_answer"] += 1
            # Add more pattern detection logic...

        return patterns

# Usage
evaluator = QAEvaluator()

# Example predictions and ground truths
predictions = [
    {"question": "Who created Python?", "answer": "Guido van Rossum", "confidence": 0.95},
    {"question": "What is ML?", "answer": "Machine Learning", "confidence": 0.87}
]

ground_truths = [
    {"answer": "Guido van Rossum"},
    {"answer": "Machine Learning"}
]

results = evaluator.evaluate_predictions(predictions, ground_truths)
print(f"Exact Match: {results['exact_match']:.3f}")
print(f"F1 Score: {results['f1_score']:.3f}")

error_analysis = evaluator.analyze_errors()
print(f"Errors: {error_analysis['total_errors']}")
```

## 🎯 Best Practices

### Data Quality
1. **Clean and preprocess documents** before indexing
2. **Use diverse, high-quality sources** for knowledge bases
3. **Regularly update and refresh** document collections
4. **Validate answer quality** through human review

### Model Selection
1. **Extractive QA** for factual, span-based questions
2. **Generative QA** for complex, reasoning-based questions
3. **Domain-specific models** for specialized knowledge areas
4. **Ensemble approaches** for improved accuracy

### Performance Optimization
1. **Index optimization** for faster retrieval
2. **Caching strategies** for frequent queries
3. **Batch processing** for multiple questions
4. **Model quantization** for deployment efficiency

## 📈 Next Steps

With QA systems mastered, you're ready to:

- **[Chapter 5: Named Entity Recognition](05-named-entity-recognition.md)** - Extract structured information from text
- **[Chapter 6: Translation & Multilingual Models](06-translation-multilingual.md)** - Work with cross-language AI applications
- **[Chapter 7: Fine-tuning Models](07-fine-tuning.md)** - Customize models for specific tasks

---

**Ready to extract structured information from text? Continue to [Chapter 5: Named Entity Recognition](05-named-entity-recognition.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `question`, `answer` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Question Answering` as an operating subsystem inside **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `context`, `result`, `print` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Question Answering` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `question` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `answer`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/huggingface/transformers)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `question` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Text Generation](03-text-generation.md)
- [Next Chapter: Chapter 5: Named Entity Recognition](05-named-entity-recognition.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
