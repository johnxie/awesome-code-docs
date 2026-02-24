---
layout: default
title: "Chapter 7: Custom Components"
parent: "Haystack Tutorial"
nav_order: 7
---

# Chapter 7: Custom Components

Welcome to **Chapter 7: Custom Components**. In this part of **Haystack: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Build custom components to extend Haystack's functionality for specialized use cases.

## 🎯 Overview

This chapter covers creating custom components in Haystack to extend its functionality for specific requirements. You'll learn to build custom retrievers, generators, processors, and other components that integrate seamlessly with Haystack pipelines.

## 🏗️ Component Architecture

### Understanding Haystack Components

```python
# Base component structure
from haystack import component

@component
class CustomComponent:
    """
    Custom Haystack component with proper serialization and execution
    """

    def __init__(self, parameter1: str = "default", parameter2: int = 42):
        """Initialize component with parameters"""
        self.parameter1 = parameter1
        self.parameter2 = parameter2

    @component.output_types(output1=str, output2=dict)
    def run(self, input1: str, input2: list = None) -> dict:
        """
        Main execution method with type hints and output declarations

        Args:
            input1: Primary input parameter
            input2: Optional secondary input

        Returns:
            Dictionary with declared outputs
        """
        # Component logic here
        result1 = f"Processed: {input1}"
        result2 = {
            "parameter1": self.parameter1,
            "parameter2": self.parameter2,
            "input_length": len(input1),
            "timestamp": time.time()
        }

        return {
            "output1": result1,
            "output2": result2
        }

    def to_dict(self) -> dict:
        """Serialize component for pipeline saving"""
        return {
            "type": "custom_component",
            "init_parameters": {
                "parameter1": self.parameter1,
                "parameter2": self.parameter2
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CustomComponent":
        """Deserialize component from saved pipeline"""
        init_params = data.get("init_parameters", {})
        return cls(**init_params)

# Usage
custom_comp = CustomComponent(parameter1="custom_value", parameter2=100)
result = custom_comp.run(input1="test input")
print(result)
```

## 🔍 Custom Retrievers

### Domain-Specific Retriever

```python
from haystack.components.retrievers import EmbeddingRetriever
from haystack import component
import numpy as np

@component
class DomainSpecificRetriever:
    """
    Retriever optimized for specific domains with custom scoring
    """

    def __init__(
        self,
        document_store,
        domain_keywords: dict = None,
        recency_weight: float = 0.3,
        relevance_weight: float = 0.7
    ):
        self.document_store = document_store
        self.embedding_retriever = EmbeddingRetriever(document_store=document_store)
        self.domain_keywords = domain_keywords or {}
        self.recency_weight = recency_weight
        self.relevance_weight = relevance_weight

    @component.output_types(documents=list)
    def run(self, query: str, top_k: int = 5, domain_filter: str = None) -> dict:
        """Retrieve documents with domain-specific scoring"""

        # Get initial retrieval results
        initial_results = self.embedding_retriever.run(query=query, top_k=top_k * 2)

        # Apply domain-specific scoring
        scored_documents = []
        for doc in initial_results["documents"]:
            domain_score = self._calculate_domain_score(doc, query, domain_filter)
            recency_score = self._calculate_recency_score(doc)
            relevance_score = doc.score if doc.score else 0.5

            # Combine scores
            final_score = (
                self.relevance_weight * relevance_score +
                self.recency_weight * recency_score +
                0.2 * domain_score  # Domain weight
            )

            doc.score = final_score
            scored_documents.append(doc)

        # Sort by final score and return top_k
        scored_documents.sort(key=lambda x: x.score, reverse=True)

        return {"documents": scored_documents[:top_k]}

    def _calculate_domain_score(self, document, query, domain_filter):
        """Calculate domain-specific relevance score"""
        score = 0.0
        content_lower = document.content.lower()

        # Domain filter boost
        if domain_filter and domain_filter in self.domain_keywords:
            domain_terms = self.domain_keywords[domain_filter]
            term_matches = sum(1 for term in domain_terms if term.lower() in content_lower)
            score += min(term_matches * 0.2, 1.0)  # Cap at 1.0

        # Query-domain alignment
        query_terms = query.lower().split()
        for term in query_terms:
            if term in self.domain_keywords.get(domain_filter, []):
                score += 0.1

        return min(score, 1.0)

    def _calculate_recency_score(self, document):
        """Calculate recency score based on document age"""
        # Extract date from document metadata or content
        # This is a simplified implementation
        current_time = time.time()

        # Assume documents have a 'created_at' field in metadata
        created_at = document.meta.get('created_at', current_time - 365*24*3600)  # Default to 1 year ago

        if isinstance(created_at, str):
            # Parse date string - simplified
            created_at = current_time - 30*24*3600  # Assume 30 days ago

        age_days = (current_time - created_at) / (24 * 3600)

        # Recency score: newer documents get higher scores
        if age_days < 7:
            return 1.0  # Very recent
        elif age_days < 30:
            return 0.8  # Recent
        elif age_days < 90:
            return 0.6  # Somewhat recent
        else:
            return 0.3  # Old

    def to_dict(self):
        return {
            "type": "domain_specific_retriever",
            "init_parameters": {
                "domain_keywords": self.domain_keywords,
                "recency_weight": self.recency_weight,
                "relevance_weight": self.relevance_weight
            }
        }

    @classmethod
    def from_dict(cls, data):
        init_params = data.get("init_parameters", {})
        return cls(**init_params)

# Usage
domain_keywords = {
    "technical": ["algorithm", "implementation", "code", "programming", "software"],
    "business": ["strategy", "revenue", "market", "customers", "growth"],
    "medical": ["patient", "treatment", "diagnosis", "clinical", "health"]
}

retriever = DomainSpecificRetriever(
    document_store=document_store,
    domain_keywords=domain_keywords,
    recency_weight=0.2,
    relevance_weight=0.8
)

# Search with domain filtering
results = retriever.run(query="machine learning algorithms", domain_filter="technical")
for doc in results["documents"]:
    print(f"Score: {doc.score:.3f} - {doc.content[:100]}...")
```

### Hybrid Retriever with Learning

```python
@component
class AdaptiveHybridRetriever:
    """
    Hybrid retriever that learns from user feedback to optimize retrieval strategy
    """

    def __init__(self, document_store, learning_rate=0.1):
        self.document_store = document_store
        self.bm25_retriever = BM25Retriever(document_store=document_store)
        self.embedding_retriever = EmbeddingRetriever(document_store=document_store)

        # Learning parameters
        self.weights = {"bm25": 0.5, "embedding": 0.5}  # Start with equal weights
        self.learning_rate = learning_rate
        self.feedback_history = []

    @component.output_types(documents=list, strategy_weights=dict)
    def run(self, query: str, top_k: int = 5, user_feedback=None) -> dict:
        """Run adaptive hybrid retrieval"""

        # Update weights based on feedback
        if user_feedback:
            self._update_weights(user_feedback)

        # Get results from both retrievers
        bm25_results = self.bm25_retriever.run(query=query, top_k=top_k * 2)
        embedding_results = self.embedding_retriever.run(query=query, top_k=top_k * 2)

        # Combine results with learned weights
        combined_results = self._combine_results(
            bm25_results["documents"],
            embedding_results["documents"],
            top_k
        )

        return {
            "documents": combined_results,
            "strategy_weights": self.weights.copy()
        }

    def _combine_results(self, bm25_docs, embedding_docs, top_k):
        """Combine results from both retrievers using learned weights"""
        # Create score mapping
        doc_scores = {}

        # Process BM25 results
        for doc in bm25_docs:
            doc_id = doc.id
            bm25_score = doc.score if doc.score else 0.5
            doc_scores[doc_id] = {
                "document": doc,
                "bm25_score": bm25_score,
                "embedding_score": 0.0,
                "final_score": 0.0
            }

        # Process embedding results
        for doc in embedding_docs:
            doc_id = doc.id
            embedding_score = doc.score if doc.score else 0.5

            if doc_id in doc_scores:
                doc_scores[doc_id]["embedding_score"] = embedding_score
            else:
                doc_scores[doc_id] = {
                    "document": doc,
                    "bm25_score": 0.0,
                    "embedding_score": embedding_score,
                    "final_score": 0.0
                }

        # Calculate final scores
        for doc_id, scores in doc_scores.items():
            final_score = (
                self.weights["bm25"] * scores["bm25_score"] +
                self.weights["embedding"] * scores["embedding_score"]
            )
            scores["final_score"] = final_score

        # Sort by final score and return top_k
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda x: x["final_score"],
            reverse=True
        )

        return [item["document"] for item in sorted_docs[:top_k]]

    def _update_weights(self, feedback):
        """Update retrieval weights based on user feedback"""
        # Store feedback for learning
        self.feedback_history.append(feedback)

        # Keep only recent feedback
        if len(self.feedback_history) > 100:
            self.feedback_history = self.feedback_history[-100:]

        # Simple learning: adjust weights based on which strategy performed better
        if feedback.get("preferred_strategy"):
            preferred = feedback["preferred_strategy"]

            if preferred == "bm25":
                self.weights["bm25"] += self.learning_rate
                self.weights["embedding"] -= self.learning_rate
            elif preferred == "embedding":
                self.weights["embedding"] += self.learning_rate
                self.weights["bm25"] -= self.learning_rate

        # Normalize weights
        total = sum(self.weights.values())
        self.weights = {k: v/total for k, v in self.weights.items()}

# Usage
adaptive_retriever = AdaptiveHybridRetriever(document_store)

# First query
results1 = adaptive_retriever.run(query="What is machine learning?")
print("Initial weights:", results1["strategy_weights"])

# Provide feedback (simulating user preference)
feedback = {"preferred_strategy": "embedding"}  # User liked embedding results better

# Second query with learning
results2 = adaptive_retriever.run(query="How do neural networks work?", user_feedback=feedback)
print("Updated weights:", results2["strategy_weights"])
```

## 🤖 Custom Generators

### Specialized Content Generator

```python
from haystack.components.generators import OpenAIGenerator
from haystack import component

@component
class SpecializedContentGenerator:
    """
    Generator specialized for different content types and styles
    """

    def __init__(self, model="gpt-4o", api_key=None):
        self.generator = OpenAIGenerator(model=model, api_key=api_key)
        self.content_templates = self._load_content_templates()

    def _load_content_templates(self):
        """Load specialized content generation templates"""
        return {
            "tutorial": """
            Write a step-by-step tutorial for: {topic}

            Structure the tutorial as follows:
            1. Introduction and prerequisites
            2. Step-by-step instructions
            3. Common issues and solutions
            4. Best practices and tips

            Use clear, concise language suitable for {audience_level} audience.
            Include code examples where relevant.
            """,

            "documentation": """
            Write comprehensive documentation for: {topic}

            Include:
            - Overview and purpose
            - Installation/setup instructions
            - Usage examples with code
            - Configuration options
            - API reference
            - Troubleshooting guide

            Write in a professional, technical style.
            """,

            "explanation": """
            Explain the concept of {topic} in simple terms.

            Structure your explanation:
            1. Simple definition
            2. Analogy or real-world example
            3. Key components or steps
            4. Common applications
            5. Why it matters

            Use analogies and avoid technical jargon unless necessary.
            """
        }

    @component.output_types(generated_content=str, metadata=dict)
    def run(self, topic: str, content_type: str = "explanation",
            audience_level: str = "intermediate", additional_context: str = None) -> dict:
        """Generate specialized content"""

        # Select template
        template = self.content_templates.get(content_type, self.content_templates["explanation"])

        # Fill template
        prompt = template.format(
            topic=topic,
            audience_level=audience_level
        )

        # Add additional context if provided
        if additional_context:
            prompt += f"\n\nAdditional context: {additional_context}"

        # Generate content
        generation_kwargs = {
            "temperature": self._get_temperature_for_type(content_type),
            "max_tokens": self._get_max_tokens_for_type(content_type),
            "top_p": 0.9
        }

        result = self.generator.run(prompt=prompt, generation_kwargs=generation_kwargs)

        content = result["replies"][0]

        # Generate metadata
        metadata = {
            "content_type": content_type,
            "topic": topic,
            "audience_level": audience_level,
            "word_count": len(content.split()),
            "generation_time": time.time(),
            "model_used": self.generator.model
        }

        return {
            "generated_content": content,
            "metadata": metadata
        }

    def _get_temperature_for_type(self, content_type):
        """Get appropriate temperature for content type"""
        temperatures = {
            "tutorial": 0.3,      # More deterministic for instructions
            "documentation": 0.2, # Very deterministic for docs
            "explanation": 0.7    # More creative for explanations
        }
        return temperatures.get(content_type, 0.5)

    def _get_max_tokens_for_type(self, content_type):
        """Get appropriate max tokens for content type"""
        max_tokens = {
            "tutorial": 1500,
            "documentation": 2000,
            "explanation": 800
        }
        return max_tokens.get(content_type, 1000)

# Usage
content_generator = SpecializedContentGenerator()

# Generate different types of content
tutorial = content_generator.run(
    topic="building REST APIs with Python",
    content_type="tutorial",
    audience_level="beginner"
)

explanation = content_generator.run(
    topic="machine learning",
    content_type="explanation",
    audience_level="beginner"
)

print("Tutorial generated:", len(tutorial["generated_content"]), "characters")
print("Explanation generated:", len(explanation["generated_content"]), "characters")
```

### Multi-Modal Generator

```python
@component
class MultiModalContentGenerator:
    """
    Generator that creates content combining text, images, and structured data
    """

    def __init__(self, text_model="gpt-4o", image_model="dall-e-3"):
        self.text_generator = OpenAIGenerator(model=text_model)
        self.image_generator = OpenAIGenerator(model=image_model)  # Assuming image generation capability

    @component.output_types(
        content_package=dict,
        generated_items=list,
        metadata=dict
    )
    def run(self, topic: str, content_types: list = None,
            style_guide: dict = None) -> dict:
        """Generate multi-modal content package"""

        if content_types is None:
            content_types = ["text", "image"]

        if style_guide is None:
            style_guide = {}

        generated_items = []
        content_package = {
            "topic": topic,
            "timestamp": time.time(),
            "items": []
        }

        # Generate text content
        if "text" in content_types:
            text_item = self._generate_text_content(topic, style_guide)
            generated_items.append(text_item)
            content_package["items"].append(text_item)

        # Generate image content
        if "image" in content_types:
            image_item = self._generate_image_content(topic, style_guide)
            generated_items.append(image_item)
            content_package["items"].append(image_item)

        # Generate structured data
        if "structured" in content_types:
            structured_item = self._generate_structured_content(topic)
            generated_items.append(structured_item)
            content_package["items"].append(structured_item)

        metadata = {
            "total_items": len(generated_items),
            "content_types": content_types,
            "generation_time": time.time(),
            "models_used": ["gpt-4o", "dall-e-3"]
        }

        return {
            "content_package": content_package,
            "generated_items": generated_items,
            "metadata": metadata
        }

    def _generate_text_content(self, topic, style_guide):
        """Generate text content with styling"""
        style_prompt = ""
        if style_guide.get("tone"):
            style_prompt += f"Write in a {style_guide['tone']} tone. "
        if style_guide.get("length"):
            style_prompt += f"Keep the content {style_guide['length']}. "
        if style_guide.get("audience"):
            style_prompt += f"Target audience: {style_guide['audience']}. "

        prompt = f"""
        Create engaging content about: {topic}

        {style_prompt}

        Include:
        - Compelling introduction
        - Key information and insights
        - Practical examples
        - Call to action or conclusion

        Make it informative and well-structured.
        """

        result = self.text_generator.run(prompt=prompt, generation_kwargs={"temperature": 0.7})

        return {
            "type": "text",
            "content": result["replies"][0],
            "style": style_guide,
            "word_count": len(result["replies"][0].split())
        }

    def _generate_image_content(self, topic, style_guide):
        """Generate image descriptions and metadata"""
        style_description = ""
        if style_guide.get("art_style"):
            style_description += f" in {style_guide['art_style']} style"
        if style_guide.get("color_scheme"):
            style_description += f" with {style_guide['color_scheme']} color scheme"

        image_prompt = f"Create a detailed prompt for an image representing: {topic}{style_description}"

        result = self.text_generator.run(
            prompt=image_prompt,
            generation_kwargs={"temperature": 0.8, "max_tokens": 200}
        )

        # In a real implementation, you would use this prompt with an image generation API
        generated_prompt = result["replies"][0]

        return {
            "type": "image",
            "prompt": generated_prompt,
            "style": style_guide,
            "estimated_generation_time": "30-60 seconds"
        }

    def _generate_structured_content(self, topic):
        """Generate structured data (JSON, etc.)"""
        prompt = f"""
        Create structured information about: {topic}

        Provide the information in JSON format with the following structure:
        {{
            "name": "topic name",
            "category": "topic category",
            "key_facts": ["fact1", "fact2", "fact3"],
            "related_topics": ["topic1", "topic2"],
            "difficulty_level": "beginner|intermediate|advanced",
            "estimated_study_time": "X hours"
        }}
        """

        result = self.text_generator.run(
            prompt=prompt,
            generation_kwargs={"temperature": 0.2}  # Low temperature for structured output
        )

        # Parse JSON response
        try:
            import json
            structured_data = json.loads(result["replies"][0])
        except:
            structured_data = {"error": "Failed to parse structured data"}

        return {
            "type": "structured",
            "content": structured_data,
            "format": "json"
        }

# Usage
multimodal_generator = MultiModalContentGenerator()

# Generate comprehensive content package
result = multimodal_generator.run(
    topic="renewable energy technologies",
    content_types=["text", "image", "structured"],
    style_guide={
        "tone": "educational",
        "length": "comprehensive",
        "audience": "general public",
        "art_style": "realistic",
        "color_scheme": "earth tones"
    }
)

print(f"Generated {result['metadata']['total_items']} content items")
for item in result["generated_items"]:
    print(f"- {item['type']}: {len(str(item['content']))} characters")
```

## 🔧 Custom Processors

### Advanced Text Processor

```python
from haystack import component
import spacy
import re
from typing import List, Dict, Any

@component
class AdvancedTextProcessor:
    """
    Advanced text processing component with NLP capabilities
    """

    def __init__(self, language="en", enable_ner=True, enable_sentiment=True):
        self.language = language
        self.enable_ner = enable_ner
        self.enable_sentiment = enable_sentiment

        # Load spaCy model
        try:
            self.nlp = spacy.load(f"{language}_core_web_sm")
        except:
            # Fallback to basic processing
            self.nlp = None
            print("spaCy model not available, using basic processing")

    @component.output_types(
        processed_text=str,
        entities=list,
        sentiment=dict,
        metadata=dict
    )
    def run(self, text: str, processing_steps: List[str] = None) -> Dict[str, Any]:
        """Process text with advanced NLP capabilities"""

        if processing_steps is None:
            processing_steps = ["clean", "normalize", "extract_entities"]

        processed_text = text
        entities = []
        sentiment = {}
        metadata = {}

        # Apply processing steps
        for step in processing_steps:
            if step == "clean":
                processed_text = self._clean_text(processed_text)
            elif step == "normalize":
                processed_text = self._normalize_text(processed_text)
            elif step == "extract_entities" and self.enable_ner:
                entities = self._extract_entities(processed_text)
            elif step == "sentiment" and self.enable_sentiment:
                sentiment = self._analyze_sentiment(processed_text)

        # Generate metadata
        metadata = {
            "original_length": len(text),
            "processed_length": len(processed_text),
            "language": self.language,
            "processing_steps": processing_steps,
            "entity_count": len(entities),
            "processing_time": time.time()
        }

        return {
            "processed_text": processed_text,
            "entities": entities,
            "sentiment": sentiment,
            "metadata": metadata
        }

    def _clean_text(self, text: str) -> str:
        """Clean text by removing noise"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)

        # Fix common OCR errors (simplified)
        text = re.sub(r'\b1\b', 'l', text)  # 1 -> l
        text = re.sub(r'\b0\b', 'o', text)  # 0 -> o

        return text

    def _normalize_text(self, text: str) -> str:
        """Normalize text for consistent processing"""
        # Convert to lowercase
        text = text.lower()

        # Expand contractions (simplified)
        contractions = {
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            "i'm": "i am"
        }

        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)

        return text

    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities"""
        if not self.nlp:
            return []

        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": getattr(ent, '_.confidence', 0.8)  # spaCy confidence if available
            })

        return entities

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment"""
        # Simplified sentiment analysis
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "horrible", "hate", "dislike", "poor"]

        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            sentiment_score = 0.5  # Neutral
            sentiment_label = "neutral"
        else:
            sentiment_score = positive_count / total_sentiment_words
            if sentiment_score > 0.6:
                sentiment_label = "positive"
            elif sentiment_score < 0.4:
                sentiment_label = "negative"
            else:
                sentiment_label = "neutral"

        return {
            "score": sentiment_score,
            "label": sentiment_label,
            "positive_words": positive_count,
            "negative_words": negative_count
        }

# Usage
text_processor = AdvancedTextProcessor(language="en")

text = "Apple Inc. is doing great work with their new iPhone! I'm really impressed by their innovation."

result = text_processor.run(
    text=text,
    processing_steps=["clean", "normalize", "extract_entities", "sentiment"]
)

print("Processed text:", result["processed_text"])
print("Entities found:", len(result["entities"]))
print("Sentiment:", result["sentiment"]["label"])
print("Processing metadata:", result["metadata"])
```

### Quality Assurance Component

```python
@component
class QualityAssuranceChecker:
    """
    Component for checking content quality and compliance
    """

    def __init__(self, quality_rules=None, compliance_rules=None):
        self.quality_rules = quality_rules or self._default_quality_rules()
        self.compliance_rules = compliance_rules or self._default_compliance_rules()

    @component.output_types(
        quality_score=float,
        compliance_status=str,
        issues_found=list,
        recommendations=list
    )
    def run(self, content: str, content_type: str = "general",
            check_compliance: bool = True) -> Dict[str, Any]:
        """Check content quality and compliance"""

        quality_score = self._check_quality(content, content_type)
        compliance_status = "compliant"
        issues_found = []
        recommendations = []

        # Quality checks
        quality_issues, quality_recs = self._assess_quality(content, content_type)
        issues_found.extend(quality_issues)
        recommendations.extend(quality_recs)

        # Compliance checks
        if check_compliance:
            compliance_issues, compliance_recs = self._check_compliance(content)
            issues_found.extend(compliance_issues)
            recommendations.extend(compliance_recs)

            if compliance_issues:
                compliance_status = "non_compliant"

        # Adjust quality score based on issues
        quality_penalty = len(issues_found) * 0.1
        quality_score = max(0, quality_score - quality_penalty)

        return {
            "quality_score": quality_score,
            "compliance_status": compliance_status,
            "issues_found": issues_found,
            "recommendations": recommendations
        }

    def _default_quality_rules(self):
        """Default quality assessment rules"""
        return {
            "min_length": 100,
            "max_length": 10000,
            "min_sentences": 3,
            "spelling_errors_threshold": 5,
            "readability_score_min": 60
        }

    def _default_compliance_rules(self):
        """Default compliance rules"""
        return {
            "banned_words": ["inappropriate", "offensive"],
            "required_disclaimers": [],
            "content_restrictions": []
        }

    def _check_quality(self, content, content_type):
        """Calculate overall quality score"""
        score = 1.0  # Start with perfect score

        # Length check
        if len(content) < self.quality_rules["min_length"]:
            score -= 0.3
        elif len(content) > self.quality_rules["max_length"]:
            score -= 0.2

        # Sentence count
        sentences = len([s for s in content.split('.') if s.strip()])
        if sentences < self.quality_rules["min_sentences"]:
            score -= 0.2

        # Basic readability (simplified)
        words = content.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        readability = 100 - (avg_word_length * 10)  # Simplified formula

        if readability < self.quality_rules["readability_score_min"]:
            score -= 0.1

        return max(0, score)

    def _assess_quality(self, content, content_type):
        """Detailed quality assessment"""
        issues = []
        recommendations = []

        # Length issues
        if len(content) < 100:
            issues.append("Content too short")
            recommendations.append("Expand content with more details and examples")

        # Structure issues
        if content.count('\n\n') < 2:
            issues.append("Poor content structure")
            recommendations.append("Add proper paragraph breaks and sections")

        # Readability issues
        long_sentences = [s for s in content.split('.') if len(s.split()) > 30]
        if long_sentences:
            issues.append("Some sentences are too long")
            recommendations.append("Break down long sentences for better readability")

        return issues, recommendations

    def _check_compliance(self, content):
        """Check content compliance"""
        issues = []
        recommendations = []

        # Check for banned words
        for banned_word in self.compliance_rules["banned_words"]:
            if banned_word.lower() in content.lower():
                issues.append(f"Contains banned word: {banned_word}")
                recommendations.append(f"Remove or replace the word '{banned_word}'")

        # Check for required disclaimers
        for disclaimer in self.compliance_rules["required_disclaimers"]:
            if disclaimer.lower() not in content.lower():
                issues.append(f"Missing required disclaimer: {disclaimer}")
                recommendations.append(f"Add the required disclaimer: {disclaimer}")

        return issues, recommendations

# Usage
qa_checker = QualityAssuranceChecker()

content = """
This is a short article about machine learning. It covers basic concepts.
The content is good but could be longer with more details.
"""

result = qa_checker.run(content, content_type="article")

print(f"Quality Score: {result['quality_score']:.2f}")
print(f"Compliance Status: {result['compliance_status']}")
print(f"Issues Found: {len(result['issues_found'])}")
if result['issues_found']:
    print("Issues:", result['issues_found'])
if result['recommendations']:
    print("Recommendations:", result['recommendations'])
```

## 🔗 Integration Components

### External API Connector

```python
@component
class ExternalAPIConnector:
    """
    Component for integrating with external APIs and services
    """

    def __init__(self, api_config: dict):
        self.api_config = api_config
        self.session = requests.Session()
        self._setup_authentication()

    def _setup_authentication(self):
        """Setup authentication for API calls"""
        auth_type = self.api_config.get("auth_type", "none")

        if auth_type == "bearer":
            token = self.api_config.get("token")
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        elif auth_type == "api_key":
            key = self.api_config.get("api_key")
            header_name = self.api_config.get("header_name", "X-API-Key")
            self.session.headers.update({header_name: key})

    @component.output_types(api_response=dict, status_code=int, metadata=dict)
    def run(self, endpoint: str, method: str = "GET",
            data: dict = None, params: dict = None) -> Dict[str, Any]:
        """Make API call to external service"""

        base_url = self.api_config.get("base_url", "")
        url = f"{base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, params=params)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}

            metadata = {
                "url": url,
                "method": method,
                "response_time": response.elapsed.total_seconds(),
                "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
                "timestamp": time.time()
            }

            return {
                "api_response": response_data,
                "status_code": response.status_code,
                "metadata": metadata
            }

        except Exception as e:
            return {
                "api_response": {"error": str(e)},
                "status_code": 0,
                "metadata": {
                    "error": str(e),
                    "timestamp": time.time()
                }
            }

    def to_dict(self):
        """Serialize component (excluding sensitive data)"""
        return {
            "type": "external_api_connector",
            "init_parameters": {
                "api_config": {
                    k: v for k, v in self.api_config.items()
                    if k not in ["token", "api_key"]  # Don't serialize secrets
                }
            }
        }

# Usage
api_config = {
    "base_url": "https://api.github.com",
    "auth_type": "bearer",
    "token": "your-github-token"
}

api_connector = ExternalAPIConnector(api_config)

# Make API call
result = api_connector.run(
    endpoint="/repos/huggingface/transformers",
    method="GET"
)

print(f"Status Code: {result['status_code']}")
print(f"Response Keys: {list(result['api_response'].keys())}")
print(f"Response Time: {result['metadata']['response_time']:.3f}s")
```

## 🎯 Best Practices

### Component Design

1. **Single Responsibility**: Each component should have one clear purpose
2. **Type Safety**: Use proper type hints for inputs and outputs
3. **Error Handling**: Implement robust error handling and graceful degradation
4. **Configuration**: Make components configurable through parameters
5. **Documentation**: Provide clear docstrings and usage examples

### Testing Components

1. **Unit Tests**: Test individual component functionality
2. **Integration Tests**: Test components working together in pipelines
3. **Edge Cases**: Test with unusual inputs and error conditions
4. **Performance Tests**: Benchmark component performance
5. **Serialization Tests**: Test component save/load functionality

### Production Considerations

1. **Resource Management**: Properly manage memory and connections
2. **Rate Limiting**: Implement appropriate rate limiting for API calls
3. **Caching**: Add caching where appropriate to improve performance
4. **Monitoring**: Include metrics and logging for observability
5. **Security**: Handle sensitive data securely and validate inputs

## 📈 Next Steps

With custom components mastered, you're ready for:

- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Deploy Haystack with custom components at scale

---

**Ready for production deployment? Continue to [Chapter 8: Production Deployment](08-production-deployment.md)!** 🚀

*Congratulations! You've now completed the comprehensive Haystack tutorial with 8 full chapters covering everything from basic search to advanced custom components. You have the knowledge and skills to build sophisticated search systems and extend Haystack for specialized use cases.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `content`, `text` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Custom Components` as an operating subsystem inside **Haystack: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `result`, `score`, `component` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Custom Components` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `content` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `text`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Haystack](https://github.com/deepset-ai/haystack)
  Why it matters: authoritative reference on `Haystack` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `content` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Evaluation & Optimization](06-evaluation-optimization.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
