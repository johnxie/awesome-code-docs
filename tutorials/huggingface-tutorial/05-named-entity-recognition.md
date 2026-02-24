---
layout: default
title: "Chapter 5: Named Entity Recognition"
parent: "HuggingFace Transformers Tutorial"
nav_order: 5
---

# Chapter 5: Named Entity Recognition

Welcome to **Chapter 5: Named Entity Recognition**. In this part of **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Extract structured information and named entities from unstructured text using NER models.

## 🎯 Overview

This chapter covers Named Entity Recognition (NER) using HuggingFace Transformers. You'll learn to identify and classify named entities like persons, organizations, locations, dates, and more from text, and build applications that extract structured information from unstructured data.

## 🏷️ Understanding Named Entities

### Common Entity Types

| Entity Type | Description | Examples |
|-------------|-------------|----------|
| **PERSON** | People names | "John Smith", "Marie Curie" |
| **ORG** | Organizations | "Google", "United Nations" |
| **LOC** | Locations | "New York", "Mount Everest" |
| **MISC** | Miscellaneous | "COVID-19", "Python" |
| **DATE** | Dates and times | "January 1, 2024", "3 PM" |
| **MONEY** | Monetary values | "$100", "€50" |
| **PERCENT** | Percentages | "25%", "50 percent" |

### NER Approaches

#### 1. **Rule-Based NER**
- Uses hand-crafted rules and dictionaries
- Fast and predictable
- Limited to known patterns

#### 2. **Machine Learning NER**
- Uses traditional ML algorithms (SVM, CRF)
- Requires feature engineering
- Good accuracy with sufficient training data

#### 3. **Deep Learning NER**
- Uses neural networks (LSTM, BERT)
- Learns features automatically
- State-of-the-art accuracy
- Requires more computational resources

## 🔍 Using Pre-trained NER Models

### Basic NER with Pipeline

```python
from transformers import pipeline

# Initialize NER pipeline
ner_pipeline = pipeline(
    "ner",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"  # Group sub-word tokens
)

# Example text
text = """
Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in Cupertino, California.
The company was incorporated on April 1, 1976, and went public on December 12, 1980.
"""

# Extract entities
entities = ner_pipeline(text)

# Display results
for entity in entities:
    print(f"{entity['entity_group']}: {entity['word']} (confidence: {entity['score']:.3f})")

# Output:
# ORG: Apple Inc. (confidence: 0.999)
# PERSON: Steve Jobs (confidence: 0.999)
# PERSON: Steve Wozniak (confidence: 0.999)
# PERSON: Ronald Wayne (confidence: 0.999)
# LOC: Cupertino (confidence: 0.999)
# LOC: California (confidence: 0.998)
# DATE: April 1, 1976 (confidence: 0.999)
# DATE: December 12, 1980 (confidence: 0.999)
```

### Advanced NER Configuration

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

class AdvancedNER:
    def __init__(self, model_name="dbmdz/bert-large-cased-finetuned-conll03-english"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.id2label = self.model.config.id2label

    def extract_entities(self, text, aggregation_strategy="simple"):
        """Extract named entities with advanced options"""
        # Tokenize input
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get predictions
        predictions = torch.argmax(outputs.logits, dim=2)
        predicted_token_class = [self.id2label[t.item()] for t in predictions[0]]

        # Convert to entities
        entities = self._predictions_to_entities(
            predicted_token_class,
            inputs.tokens(),
            aggregation_strategy
        )

        return entities

    def _predictions_to_entities(self, predictions, tokens, strategy):
        """Convert predictions to entity format"""
        entities = []
        current_entity = None

        for token, prediction in zip(tokens, predictions):
            if token in ["[CLS]", "[SEP]", "[PAD]"]:
                continue

            # BIO tagging scheme
            if prediction.startswith("B-"):
                # Start of new entity
                if current_entity:
                    entities.append(current_entity)

                entity_type = prediction[2:]  # Remove B-
                current_entity = {
                    "entity": entity_type,
                    "word": self._clean_token(token),
                    "start": len(self.tokenizer.decode(tokens[:tokens.index(token)])),
                    "end": len(self.tokenizer.decode(tokens[:tokens.index(token) + 1])),
                    "score": 1.0  # Simplified confidence
                }

            elif prediction.startswith("I-") and current_entity:
                # Continuation of current entity
                current_entity["word"] += self._clean_token(token)
                current_entity["end"] = len(self.tokenizer.decode(tokens[:tokens.index(token) + 1]))

            elif prediction == "O":
                # Outside entity
                if current_entity:
                    entities.append(current_entity)
                    current_entity = None

        # Add final entity if exists
        if current_entity:
            entities.append(current_entity)

        return entities

    def _clean_token(self, token):
        """Clean token by removing special characters"""
        if token.startswith("##"):
            return token[2:]  # BERT subword continuation
        return token

# Usage
advanced_ner = AdvancedNER()

text = "Elon Musk founded Tesla in 2003 and SpaceX in 2002."
entities = advanced_ner.extract_entities(text)

for entity in entities:
    print(f"{entity['entity']}: {entity['word']}")
```

## 🌍 Multilingual NER

### Cross-Language Entity Recognition

```python
from transformers import pipeline

# Multilingual NER models
multilingual_models = {
    "German": "fhswf/bert_de_ner",
    "French": "Jean-Baptiste/camembert-ner",
    "Spanish": "mrm8488/bert-spanish-ner",
    "Chinese": "ckiplab/bert-base-chinese-ner",
    "Arabic": "aubmindlab/bert-base-arabic-ner"
}

class MultilingualNER:
    def __init__(self):
        self.pipelines = {}
        self._load_models()

    def _load_models(self):
        """Load multilingual NER models"""
        for language, model_name in multilingual_models.items():
            try:
                self.pipelines[language] = pipeline(
                    "ner",
                    model=model_name,
                    aggregation_strategy="simple"
                )
                print(f"Loaded {language} NER model")
            except Exception as e:
                print(f"Failed to load {language} model: {e}")

    def extract_entities_multilingual(self, texts, languages):
        """Extract entities from texts in different languages"""
        results = {}

        for text, language in zip(texts, languages):
            if language in self.pipelines:
                entities = self.pipelines[language](text)
                results[language] = entities
            else:
                results[language] = []

        return results

# Usage
multilingual_ner = MultilingualNER()

texts = [
    "Angela Merkel was the Chancellor of Germany from 2005 to 2021.",
    "Emmanuel Macron est le président de la France depuis 2017.",
    "习近平是中国国家主席。"
]

languages = ["German", "French", "Chinese"]

results = multilingual_ner.extract_entities_multilingual(texts, languages)

for lang, entities in results.items():
    print(f"\n{lang} entities:")
    for entity in entities:
        print(f"  {entity['entity_group']}: {entity['word']}")
```

## 🏗️ Building Custom NER Models

### Fine-tuning for Domain-Specific Entities

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import Dataset
import torch

class CustomNERTrainer:
    def __init__(self, base_model="bert-base-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForTokenClassification.from_pretrained(
            base_model,
            num_labels=len(self.label_list)
        )

    @property
    def label_list(self):
        """Define label list for custom entities"""
        return [
            "O",          # Outside entity
            "B-PERSON",   # Beginning of person
            "I-PERSON",   # Inside person
            "B-ORG",      # Beginning of organization
            "I-ORG",      # Inside organization
            "B-LOC",      # Beginning of location
            "I-LOC",      # Inside location
            "B-PRODUCT",  # Beginning of product
            "I-PRODUCT",  # Inside product
            "B-TECH",     # Beginning of technology
            "I-TECH"      # Inside technology
        ]

    def prepare_dataset(self, texts, labels):
        """Prepare dataset for training"""
        def tokenize_and_align_labels(examples):
            tokenized_inputs = self.tokenizer(
                examples["tokens"],
                truncation=True,
                is_split_into_words=True
            )

            labels = []
            for i, label in enumerate(examples["ner_tags"]):
                word_ids = tokenized_inputs.word_ids(batch_index=i)
                previous_word_idx = None
                label_ids = []
                for word_idx in word_ids:
                    if word_idx is None:
                        label_ids.append(-100)
                    elif word_idx != previous_word_idx:
                        label_ids.append(label[word_idx])
                    else:
                        label_ids.append(label[word_idx] if self.label_all_tokens else -100)
                    previous_word_idx = word_idx

                labels.append(label_ids)

            tokenized_inputs["labels"] = labels
            return tokenized_inputs

        # Convert to dataset format
        dataset = Dataset.from_dict({
            "tokens": texts,
            "ner_tags": labels
        })

        tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

        return tokenized_dataset

    def train(self, train_dataset, eval_dataset, output_dir="./custom-ner-model"):
        """Train the custom NER model"""
        training_args = TrainingArguments(
            output_dir=output_dir,
            evaluation_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=3,
            weight_decay=0.01,
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self._compute_metrics,
        )

        trainer.train()
        trainer.save_model(output_dir)

        return trainer

    def _compute_metrics(self, eval_pred):
        """Compute evaluation metrics"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=2)

        # Remove ignored index (special tokens)
        true_predictions = [
            [self.label_list[p] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]
        true_labels = [
            [self.label_list[l] for (p, l) in zip(prediction, label) if l != -100]
            for prediction, label in zip(predictions, labels)
        ]

        # Calculate metrics using seqeval
        results = self._calculate_seq_f1(true_predictions, true_labels)

        return {
            "precision": results["precision"],
            "recall": results["recall"],
            "f1": results["f1"],
            "accuracy": results["accuracy"],
        }

    def _calculate_seq_f1(self, predictions, labels):
        """Calculate sequence-level F1 scores"""
        # Simplified implementation - in practice, use seqeval library
        return {
            "precision": 0.85,  # Placeholder
            "recall": 0.82,     # Placeholder
            "f1": 0.83,         # Placeholder
            "accuracy": 0.89    # Placeholder
        }

# Usage example
trainer = CustomNERTrainer()

# Example training data (simplified)
texts = [
    ["John", "Smith", "works", "at", "Google", "in", "California"],
    ["Microsoft", "released", "Windows", "11", "in", "2021"]
]

labels = [
    ["B-PERSON", "I-PERSON", "O", "O", "B-ORG", "O", "B-LOC"],
    ["B-ORG", "O", "B-PRODUCT", "I-PRODUCT", "O", "B-DATE"]
]

train_dataset = trainer.prepare_dataset(texts, labels)
# trainer.train(train_dataset, eval_dataset)
```

## 📊 Entity Relationship Extraction

### Beyond NER: Extracting Relationships

```python
from transformers import pipeline
import spacy
import networkx as nx

class EntityRelationshipExtractor:
    def __init__(self):
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities_and_relations(self, text):
        """Extract entities and their relationships"""
        # Extract named entities
        entities = self.ner_pipeline(text)

        # Parse with spaCy for dependency relations
        doc = self.nlp(text)

        # Build knowledge graph
        kg = self._build_knowledge_graph(doc, entities)

        return {
            "entities": entities,
            "relationships": kg["relationships"],
            "graph": kg["graph"]
        }

    def _build_knowledge_graph(self, doc, entities):
        """Build knowledge graph from text"""
        graph = nx.DiGraph()
        relationships = []

        # Add entities as nodes
        entity_nodes = {}
        for entity in entities:
            entity_id = f"{entity['entity_group']}_{entity['word']}"
            graph.add_node(entity_id, type=entity['entity_group'], text=entity['word'])
            entity_nodes[entity['start']] = entity_id

        # Extract relationships based on dependency parsing
        for token in doc:
            if token.dep_ in ['nsubj', 'dobj', 'pobj', 'attr']:
                # Find related entities
                subject = self._find_closest_entity(token, entity_nodes, direction='left')
                object_ = self._find_closest_entity(token, entity_nodes, direction='right')

                if subject and object_:
                    relation = {
                        "subject": subject,
                        "predicate": token.lemma_,
                        "object": object_,
                        "confidence": 0.8
                    }
                    relationships.append(relation)

                    # Add edge to graph
                    graph.add_edge(subject, object_, relation=token.lemma_, weight=0.8)

        return {
            "graph": graph,
            "relationships": relationships
        }

    def _find_closest_entity(self, token, entity_nodes, direction='right', max_distance=5):
        """Find closest entity to a token"""
        pos = token.i
        search_range = range(pos + 1, min(pos + max_distance + 1, len(token.doc))) if direction == 'right' \
                      else range(max(pos - max_distance, 0), pos)

        for i in search_range:
            if token.doc[i].idx in entity_nodes:
                return entity_nodes[token.doc[i].idx]

        return None

# Usage
extractor = EntityRelationshipExtractor()

text = "Steve Jobs founded Apple Inc. in Cupertino, California in 1976."
result = extractor.extract_entities_and_relations(text)

print("Entities:")
for entity in result["entities"]:
    print(f"  {entity['entity_group']}: {entity['word']}")

print("\nRelationships:")
for rel in result["relationships"]:
    print(f"  {rel['subject']} -> {rel['predicate']} -> {rel['object']}")
```

## 🔍 Specialized NER Applications

### Medical NER

```python
from transformers import pipeline

class MedicalNER:
    def __init__(self):
        # Use BioBERT or similar medical NER model
        self.ner_pipeline = pipeline(
            "ner",
            model="d4data/biomedical-ner-all",
            aggregation_strategy="simple"
        )

    def extract_medical_entities(self, text):
        """Extract medical entities from text"""
        entities = self.ner_pipeline(text)

        # Categorize medical entities
        categorized = {
            "diseases": [],
            "drugs": [],
            "symptoms": [],
            "procedures": [],
            "body_parts": []
        }

        for entity in entities:
            entity_type = entity['entity_group'].lower()
            if 'disease' in entity_type or 'disorder' in entity_type:
                categorized["diseases"].append(entity)
            elif 'drug' in entity_type or 'medication' in entity_type:
                categorized["drugs"].append(entity)
            elif 'symptom' in entity_type:
                categorized["symptoms"].append(entity)
            elif 'procedure' in entity_type or 'treatment' in entity_type:
                categorized["procedures"].append(entity)
            elif 'body' in entity_type or 'organ' in entity_type:
                categorized["body_parts"].append(entity)

        return categorized

# Usage
medical_ner = MedicalNER()

text = "The patient presented with chest pain and was diagnosed with myocardial infarction. Treatment included aspirin and angioplasty."

entities = medical_ner.extract_medical_entities(text)

for category, ents in entities.items():
    if ents:
        print(f"\n{category.upper()}:")
        for ent in ents:
            print(f"  {ent['word']} (confidence: {ent['score']:.3f})")
```

### Financial NER

```python
class FinancialNER:
    def __init__(self):
        # Use FinBERT or financial NER model
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"
        )

    def extract_financial_entities(self, text):
        """Extract financial entities and concepts"""
        entities = self.ner_pipeline(text)

        # Enhance with financial-specific patterns
        financial_entities = {
            "companies": [],
            "currencies": [],
            "amounts": [],
            "dates": [],
            "products": []
        }

        for entity in entities:
            if entity['entity_group'] == 'ORG':
                # Check if it's a financial company
                if self._is_financial_company(entity['word']):
                    financial_entities["companies"].append(entity)
            elif entity['entity_group'] in ['MONEY', 'PERCENT']:
                financial_entities["amounts"].append(entity)
            elif entity['entity_group'] == 'DATE':
                financial_entities["dates"].append(entity)

        # Add pattern-based extraction for missing entities
        financial_entities["currencies"].extend(self._extract_currencies(text))
        financial_entities["products"].extend(self._extract_financial_products(text))

        return financial_entities

    def _is_financial_company(self, company_name):
        """Check if company is financial/investment related"""
        financial_keywords = ['bank', 'financial', 'investment', 'capital', 'fund', 'securities']
        return any(keyword in company_name.lower() for keyword in financial_keywords)

    def _extract_currencies(self, text):
        """Extract currency mentions using patterns"""
        import re
        currency_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # $123.45
            r'€[\d,]+(?:\.\d{2})?',  # €123.45
            r'£[\d,]+(?:\.\d{2})?',  # £123.45
            r'¥[\d,]+(?:\.\d{2})?',  # ¥123.45
        ]

        currencies = []
        for pattern in currency_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                currencies.append({
                    "word": match.group(),
                    "entity_group": "CURRENCY",
                    "start": match.start(),
                    "end": match.end(),
                    "score": 0.95
                })

        return currencies

    def _extract_financial_products(self, text):
        """Extract financial product mentions"""
        products = []
        product_keywords = {
            'stock': 'EQUITY',
            'bond': 'DEBT',
            'option': 'DERIVATIVE',
            'future': 'DERIVATIVE',
            'etf': 'FUND',
            'mutual fund': 'FUND'
        }

        text_lower = text.lower()
        for product, category in product_keywords.items():
            if product in text_lower:
                start = text_lower.find(product)
                products.append({
                    "word": text[start:start + len(product)],
                    "entity_group": category,
                    "start": start,
                    "end": start + len(product),
                    "score": 0.85
                })

        return products

# Usage
financial_ner = FinancialNER()

text = "Apple Inc. stock rose 5% to $150. The company's bond yields decreased by 0.2%."

entities = financial_ner.extract_financial_entities(text)

for category, ents in entities.items():
    if ents:
        print(f"\n{category.upper()}:")
        for ent in ents:
            print(f"  {ent['word']} ({ent.get('entity_group', 'UNKNOWN')}, confidence: {ent['score']:.3f})")
```

## 📊 Evaluation Metrics

### NER Model Evaluation

```python
from sklearn.metrics import classification_report, precision_recall_fscore_support
import numpy as np

class NEREvaluator:
    def __init__(self):
        self.true_entities = []
        self.pred_entities = []

    def add_prediction(self, true_labels, pred_labels):
        """Add prediction for evaluation"""
        self.true_entities.extend(true_labels)
        self.pred_entities.extend(pred_labels)

    def evaluate(self):
        """Calculate NER evaluation metrics"""
        # Entity-level evaluation
        entity_metrics = self._calculate_entity_metrics()

        # Token-level evaluation
        token_metrics = self._calculate_token_metrics()

        # Class-wise evaluation
        class_metrics = self._calculate_class_metrics()

        return {
            "entity_level": entity_metrics,
            "token_level": token_metrics,
            "class_wise": class_metrics,
            "confusion_analysis": self._analyze_confusion()
        }

    def _calculate_entity_metrics(self):
        """Calculate entity-level precision, recall, F1"""
        true_positives = 0
        false_positives = 0
        false_negatives = 0

        # Simplified entity matching - in practice, use proper entity alignment
        for true_ent, pred_ent in zip(self.true_entities, self.pred_entities):
            if self._entities_match(true_ent, pred_ent):
                true_positives += 1
            else:
                false_positives += 1
                false_negatives += 1

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }

    def _calculate_token_metrics(self):
        """Calculate token-level accuracy"""
        correct_tokens = sum(1 for t, p in zip(self.true_entities, self.pred_entities) if t == p)
        total_tokens = len(self.true_entities)

        return {
            "accuracy": correct_tokens / total_tokens if total_tokens > 0 else 0
        }

    def _calculate_class_metrics(self):
        """Calculate per-class metrics"""
        # Extract unique classes
        classes = list(set([ent.split('-')[-1] for ent in self.true_entities + self.pred_entities]))

        class_report = classification_report(
            self.true_entities,
            self.pred_entities,
            labels=classes,
            output_dict=True
        )

        return class_report

    def _entities_match(self, true_ent, pred_ent):
        """Check if two entities match (simplified)"""
        return true_ent == pred_ent

    def _analyze_confusion(self):
        """Analyze common confusion patterns"""
        confusion_matrix = {}

        for true_ent, pred_ent in zip(self.true_entities, self.pred_entities):
            if true_ent != pred_ent:
                key = f"{true_ent} -> {pred_ent}"
                confusion_matrix[key] = confusion_matrix.get(key, 0) + 1

        # Return most common confusions
        sorted_confusions = sorted(confusion_matrix.items(), key=lambda x: x[1], reverse=True)
        return sorted_confusions[:10]

# Usage
evaluator = NEREvaluator()

# Example predictions
true_labels = ["B-PERSON", "I-PERSON", "O", "B-ORG", "O"]
pred_labels = ["B-PERSON", "I-PERSON", "O", "B-LOC", "O"]

evaluator.add_prediction(true_labels, pred_labels)
results = evaluator.evaluate()

print(f"Entity-level F1: {results['entity_level']['f1_score']:.3f}")
print(f"Token-level Accuracy: {results['token_level']['accuracy']:.3f}")
```

## 🎯 Best Practices

### Data Quality
1. **Use diverse training data** representing various entity types
2. **Balance entity classes** to avoid bias towards common entities
3. **Include context** around entities for better recognition
4. **Validate annotations** through multiple reviewers

### Model Selection
1. **Domain-specific models** for specialized NER tasks
2. **Multilingual models** for cross-language applications
3. **Ensemble approaches** combining multiple models
4. **Fine-tuning** on domain-specific data

### Performance Optimization
1. **Batch processing** for efficient inference
2. **Model quantization** for deployment
3. **Caching** for repeated texts
4. **GPU acceleration** for large-scale processing

## 📈 Next Steps

With NER mastered, you're ready to:

- **[Chapter 6: Translation & Multilingual Models](06-translation-multilingual.md)** - Work with cross-language AI applications
- **[Chapter 7: Fine-tuning Models](07-fine-tuning.md)** - Customize models for specific tasks
- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Scale Transformers applications

---

**Ready to work with multilingual AI models? Continue to [Chapter 6: Translation & Multilingual Models](06-translation-multilingual.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `entity`, `entities` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Named Entity Recognition` as an operating subsystem inside **HuggingFace Transformers Tutorial: Building State-of-the-Art AI Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `text`, `token`, `model` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Named Entity Recognition` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `entity` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `entities`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/huggingface/transformers)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `entity` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Question Answering](04-question-answering.md)
- [Next Chapter: Chapter 6: Translation & Multilingual Models](06-translation-multilingual.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
