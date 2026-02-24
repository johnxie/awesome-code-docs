---
layout: default
title: "Chapter 4: Generators & LLMs"
parent: "Haystack Tutorial"
nav_order: 4
---

# Chapter 4: Generators & LLMs

Welcome to **Chapter 4: Generators & LLMs**. In this part of **Haystack: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Integrate language models for intelligent answer generation in Haystack.

## 🎯 Overview

This chapter covers integrating Large Language Models (LLMs) with Haystack's retrieval system to create Retrieval-Augmented Generation (RAG) pipelines. You'll learn to connect various LLM providers and build sophisticated generative QA systems.

## 🤖 LLM Integration Basics

### Supported LLM Providers

Haystack supports a wide range of LLM providers through its generator components:

#### OpenAI
```python
from haystack.components.generators import OpenAIGenerator

# Initialize OpenAI generator
generator = OpenAIGenerator(
    model="gpt-4o",
    api_key="your-openai-api-key"  # Or set OPENAI_API_KEY env var
)

# Generate text
response = generator.run(prompt="What is machine learning?")
print(response["replies"][0])

# With generation parameters
response = generator.run(
    prompt="Explain neural networks",
    generation_kwargs={
        "temperature": 0.7,
        "max_tokens": 200,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }
)
```

#### Anthropic Claude
```python
from haystack.components.generators import AnthropicGenerator

# Initialize Anthropic generator
generator = AnthropicGenerator(
    model="claude-3-5-sonnet-20241022",
    api_key="your-anthropic-api-key"  # Or set ANTHROPIC_API_KEY env var
)

# Generate with Claude
response = generator.run(
    prompt="Write a short story about AI",
    generation_kwargs={
        "temperature": 0.8,
        "max_tokens": 500,
        "top_p": 1.0
    }
)
print(response["replies"][0])
```

#### Local Models (Ollama)
```python
from haystack.components.generators import OllamaGenerator

# Initialize Ollama generator (requires Ollama running locally)
generator = OllamaGenerator(
    model="llama3.1:8b",
    url="http://localhost:11434"
)

# Generate with local model
response = generator.run(
    prompt="What are the benefits of open-source AI?",
    generation_kwargs={
        "temperature": 0.3,
        "top_p": 0.9,
        "num_predict": 200
    }
)
```

#### Hugging Face Models
```python
from haystack.components.generators import HuggingFaceLocalGenerator
import torch

# Initialize local Hugging Face model
generator = HuggingFaceLocalGenerator(
    model="microsoft/DialoGPT-medium",
    torch_dtype=torch.float16,  # Use mixed precision
    device="cuda:0" if torch.cuda.is_available() else "cpu"
)

# Generate locally
response = generator.run(
    prompt="Hello, how are you?",
    generation_kwargs={
        "max_new_tokens": 50,
        "temperature": 0.7,
        "do_sample": True,
        "pad_token_id": generator.tokenizer.eos_token_id
    }
)
```

## 🔄 RAG Pipeline Construction

### Basic RAG Pipeline

```python
from haystack import Pipeline
from haystack.components.retrievers import EmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

# Create RAG pipeline
pipeline = Pipeline()

# Add components
pipeline.add_component("retriever", EmbeddingRetriever(document_store=document_store))
pipeline.add_component("prompt_builder", PromptBuilder(
    template="""
    Context information is below.
    ---------------------
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    ---------------------
    Given the context information, answer the query.
    Query: {{ query }}
    Answer:
    """
))
pipeline.add_component("generator", OpenAIGenerator(model="gpt-4o"))

# Connect components
pipeline.connect("retriever", "prompt_builder.documents")
pipeline.connect("prompt_builder", "generator")

# Run the pipeline
result = pipeline.run({
    "retriever": {"query": "What is machine learning?"},
    "prompt_builder": {"query": "What is machine learning?"}
})

print(result["generator"]["replies"][0])
```

### Advanced RAG with Re-ranking

```python
from haystack.components.rankers import SentenceTransformersDiversityRanker

class AdvancedRAGPipeline:
    def __init__(self, document_store):
        self.pipeline = Pipeline()

        # Retriever
        retriever = EmbeddingRetriever(document_store=document_store)
        self.pipeline.add_component("retriever", retriever)

        # Re-ranker for diversity and relevance
        ranker = SentenceTransformersDiversityRanker(
            model="sentence-transformers/all-MiniLM-L6-v2",
            top_k=10,
            similarity_threshold=0.5
        )
        self.pipeline.add_component("ranker", ranker)

        # Prompt builder with better template
        prompt_builder = PromptBuilder(
            template=self._get_advanced_prompt_template()
        )
        self.pipeline.add_component("prompt_builder", prompt_builder)

        # Generator with better parameters
        generator = OpenAIGenerator(
            model="gpt-4o",
            generation_kwargs={
                "temperature": 0.1,  # Lower temperature for factual answers
                "max_tokens": 300,
                "top_p": 0.9
            }
        )
        self.pipeline.add_component("generator", generator)

        # Connect components
        self.pipeline.connect("retriever", "ranker")
        self.pipeline.connect("ranker", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "generator")

    def _get_advanced_prompt_template(self):
        """Get advanced prompt template with instructions"""
        return """
        You are a helpful and accurate AI assistant. Use the provided context to answer the user's question.

        Guidelines:
        - Answer based only on the provided context
        - If the context doesn't contain enough information, say so
        - Be concise but comprehensive
        - Use direct quotes from the context when relevant
        - Structure your answer clearly

        Context:
        {% for document in documents %}
        Document {{ loop.index }}: {{ document.content }}
        {% endfor %}

        Question: {{ query }}

        Answer:"""

    def run_query(self, query, top_k=5):
        """Run a query through the RAG pipeline"""
        result = self.pipeline.run({
            "retriever": {"query": query, "top_k": top_k},
            "prompt_builder": {"query": query}
        })

        return {
            "answer": result["generator"]["replies"][0],
            "retrieved_docs": result["ranker"]["documents"],
            "query": query
        }

# Usage
rag_pipeline = AdvancedRAGPipeline(document_store)
result = rag_pipeline.run_query("How do neural networks learn?")

print("Question:", result["query"])
print("Answer:", result["answer"])
print(f"Retrieved {len(result['retrieved_docs'])} documents")
```

## 🎨 Prompt Engineering

### Dynamic Prompt Building

```python
from haystack.components.builders import PromptBuilder

class DynamicPromptBuilder:
    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self):
        """Load different prompt templates for different scenarios"""
        return {
            "factual": """
            Answer the following question using only the provided context.
            Be accurate and cite specific information from the context.

            Context: {% for document in documents %}{{ document.content }} {% endfor %}
            Question: {{ query }}
            Answer:""",

            "conversational": """
            You are a helpful assistant having a conversation.
            Use the provided context to inform your response, but respond naturally.

            Context: {% for document in documents %}{{ document.content }} {% endfor %}
            User: {{ query }}
            Assistant:""",

            "educational": """
            Explain the following topic using the provided context as reference.
            Use simple language and provide examples where helpful.

            Context: {% for document in documents %}{{ document.content }} {% endfor %}
            Topic: {{ query }}
            Explanation:""",

            "technical": """
            Provide a technical explanation using the provided documentation.
            Include code examples or technical details where available.

            Context: {% for document in documents %}{{ document.content }} {% endfor %}
            Technical Query: {{ query }}
            Technical Answer:"""
        }

    def build_prompt(self, query, documents, prompt_type="factual", additional_context=None):
        """Build a dynamic prompt based on query analysis"""
        # Analyze query to determine best prompt type
        detected_type = self._analyze_query_type(query)

        # Override with explicit type if provided
        prompt_type = prompt_type or detected_type

        template = self.templates.get(prompt_type, self.templates["factual"])

        # Add additional context if provided
        if additional_context:
            template = additional_context + "\n\n" + template

        # Build prompt using Haystack's PromptBuilder
        prompt_builder = PromptBuilder(template=template)

        return prompt_builder

    def _analyze_query_type(self, query):
        """Analyze query to determine appropriate prompt type"""
        query_lower = query.lower()

        # Simple rule-based analysis
        if any(word in query_lower for word in ["explain", "how does", "what is", "teach me"]):
            return "educational"
        elif any(word in query_lower for word in ["code", "implement", "function", "api"]):
            return "technical"
        elif any(word in query_lower for word in ["hello", "hi", "thanks", "bye"]):
            return "conversational"
        else:
            return "factual"

# Usage
dynamic_builder = DynamicPromptBuilder()

# Different query types get different prompts
queries = [
    "What is machine learning?",  # factual
    "Can you explain neural networks?",  # educational
    "How do I implement a REST API?",  # technical
    "Hello, how are you?",  # conversational
]

for query in queries:
    prompt_builder = dynamic_builder.build_prompt(query, [], prompt_type=None)
    print(f"Query: {query}")
    print(f"Detected type: {dynamic_builder._analyze_query_type(query)}")
    print("---")
```

### Context Optimization

```python
class ContextOptimizer:
    def __init__(self, max_context_length=4000):
        self.max_context_length = max_context_length

    def optimize_context(self, documents, query, strategy="summarize"):
        """Optimize context for better LLM performance"""
        if strategy == "summarize":
            return self._summarize_context(documents, query)
        elif strategy == "extract":
            return self._extract_relevant_sections(documents, query)
        elif strategy == "truncate":
            return self._truncate_context(documents)
        else:
            return documents

    def _summarize_context(self, documents, query):
        """Summarize context to fit within limits"""
        # Simple length-based summarization
        total_length = sum(len(doc.content) for doc in documents)
        if total_length <= self.max_context_length:
            return documents

        # Keep most relevant documents
        scored_docs = []
        for doc in documents:
            score = self._calculate_relevance_score(doc, query)
            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        # Keep documents until we hit the length limit
        optimized_docs = []
        current_length = 0

        for score, doc in scored_docs:
            if current_length + len(doc.content) <= self.max_context_length:
                optimized_docs.append(doc)
                current_length += len(doc.content)
            else:
                break

        return optimized_docs

    def _extract_relevant_sections(self, documents, query):
        """Extract only relevant sections from documents"""
        relevant_sections = []

        for doc in documents:
            sections = self._split_into_sections(doc.content)
            for section in sections:
                if self._is_relevant_section(section, query):
                    relevant_sections.append(section[:500])  # Limit section length

                    if len(" ".join(relevant_sections)) > self.max_context_length:
                        break

            if len(" ".join(relevant_sections)) > self.max_context_length:
                break

        # Create new document with relevant sections
        combined_content = "\n\n".join(relevant_sections)
        return [Document(content=combined_content, id="optimized_context")]

    def _truncate_context(self, documents):
        """Simple truncation approach"""
        combined_content = ""
        for doc in documents:
            if len(combined_content) + len(doc.content) <= self.max_context_length:
                combined_content += doc.content + "\n\n"
            else:
                remaining_space = self.max_context_length - len(combined_content)
                combined_content += doc.content[:remaining_space]
                break

        return [Document(content=combined_content, id="truncated_context")]

    def _calculate_relevance_score(self, document, query):
        """Calculate relevance score for document to query"""
        query_terms = set(query.lower().split())
        doc_terms = set(document.content.lower().split())

        # Simple term overlap score
        overlap = len(query_terms & doc_terms)
        return overlap / len(query_terms) if query_terms else 0

    def _split_into_sections(self, content):
        """Split document into sections (paragraphs)"""
        return [section.strip() for section in content.split('\n\n') if section.strip()]

    def _is_relevant_section(self, section, query):
        """Check if section is relevant to query"""
        query_terms = set(query.lower().split())
        section_terms = set(section.lower().split())

        overlap = len(query_terms & section_terms)
        return overlap > 0

# Usage
context_optimizer = ContextOptimizer(max_context_length=2000)

# Optimize context using different strategies
documents = [
    Document(content="Machine learning is a method of data analysis..."),
    Document(content="Neural networks are computing systems..."),
    Document(content="Deep learning uses neural networks with multiple layers...")
]

query = "What are neural networks?"

# Try different optimization strategies
strategies = ["summarize", "extract", "truncate"]
for strategy in strategies:
    optimized = context_optimizer.optimize_context(documents, query, strategy=strategy)
    total_length = sum(len(doc.content) for doc in optimized)
    print(f"{strategy.capitalize()}: {len(optimized)} docs, {total_length} chars")
```

## 🔄 Multi-Model Ensembles

### Ensemble Generation

```python
from haystack.components.generators import OpenAIGenerator, AnthropicGenerator
from haystack.components.joiners import DocumentJoiner

class EnsembleGenerator:
    def __init__(self):
        # Initialize multiple generators
        self.generators = {
            "gpt4": OpenAIGenerator(model="gpt-4o"),
            "claude": AnthropicGenerator(model="claude-3-5-sonnet-20241022"),
            "gpt3": OpenAIGenerator(model="gpt-3.5-turbo")
        }

        self.weights = {
            "gpt4": 0.5,
            "claude": 0.3,
            "gpt3": 0.2
        }

    def generate_ensemble(self, prompt, num_responses=3):
        """Generate responses from multiple models"""
        responses = {}

        for model_name, generator in self.generators.items():
            try:
                response = generator.run(
                    prompt=prompt,
                    generation_kwargs={
                        "temperature": 0.7,
                        "max_tokens": 300,
                        "n": num_responses
                    }
                )
                responses[model_name] = response["replies"]
            except Exception as e:
                print(f"Error with {model_name}: {e}")
                responses[model_name] = []

        return responses

    def combine_responses(self, responses, method="weighted_voting"):
        """Combine responses from multiple models"""
        if method == "weighted_voting":
            return self._weighted_voting(responses)
        elif method == "consensus":
            return self._find_consensus(responses)
        elif method == "best_of":
            return self._select_best(responses)
        else:
            return responses

    def _weighted_voting(self, responses):
        """Combine responses using weighted voting"""
        all_responses = []
        weights = []

        for model_name, model_responses in responses.items():
            weight = self.weights.get(model_name, 1.0)
            for response in model_responses:
                all_responses.append(response)
                weights.append(weight)

        # Simple weighted combination (could be more sophisticated)
        if all_responses:
            # Return the highest weighted response
            return max(zip(all_responses, weights), key=lambda x: x[1])[0]
        return ""

    def _find_consensus(self, responses):
        """Find consensus answer across models"""
        all_responses = []
        for model_responses in responses.values():
            all_responses.extend(model_responses)

        # Simple consensus: most common response structure
        # In practice, you'd use more sophisticated consensus finding
        if all_responses:
            return all_responses[0]  # Placeholder
        return ""

    def _select_best(self, responses):
        """Select the best response based on criteria"""
        # Evaluate each response and select the best
        scored_responses = []

        for model_name, model_responses in responses.items():
            for response in model_responses:
                score = self._evaluate_response_quality(response)
                scored_responses.append((response, score))

        if scored_responses:
            return max(scored_responses, key=lambda x: x[1])[0]
        return ""

    def _evaluate_response_quality(self, response):
        """Evaluate response quality (simple heuristics)"""
        score = 0

        # Length appropriateness
        if 50 < len(response) < 500:
            score += 1

        # Contains structured information
        if any(indicator in response.lower() for indicator in ["because", "however", "therefore"]):
            score += 1

        # Not too repetitive
        words = response.lower().split()
        if len(words) > 10 and len(set(words)) / len(words) > 0.5:
            score += 1

        return score

# Usage
ensemble = EnsembleGenerator()

prompt = "Explain the benefits of using multiple AI models in an ensemble."

# Generate with multiple models
responses = ensemble.generate_ensemble(prompt, num_responses=1)

# Combine responses
combined_response = ensemble.combine_responses(responses, method="weighted_voting")

print("Ensemble Response:")
print(combined_response)
```

## 📊 Generation Quality Evaluation

### Automated Quality Metrics

```python
from haystack.evaluation import Evaluator
import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

class GenerationEvaluator:
    def __init__(self):
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    def evaluate_generation(self, generated_responses, reference_responses=None):
        """Evaluate generation quality"""
        if reference_responses:
            return self._evaluate_against_references(generated_responses, reference_responses)
        else:
            return self._evaluate_self_consistency(generated_responses)

    def _evaluate_against_references(self, generated, references):
        """Evaluate against reference responses"""
        results = []

        for gen, ref in zip(generated, references):
            # BLEU score
            bleu = sentence_bleu([ref.split()], gen.split())

            # ROUGE scores
            rouge_scores = self.rouge_scorer.score(ref, gen)

            # Factual consistency (placeholder - would need fact-checking)
            consistency_score = self._check_factual_consistency(gen, ref)

            results.append({
                "bleu": bleu,
                "rouge1": rouge_scores["rouge1"].fmeasure,
                "rouge2": rouge_scores["rouge2"].fmeasure,
                "rougeL": rouge_scores["rougeL"].fmeasure,
                "consistency": consistency_score,
                "overall_score": (bleu + rouge_scores["rouge1"].fmeasure + consistency_score) / 3
            })

        # Aggregate results
        avg_results = {}
        for key in results[0].keys():
            avg_results[key] = sum(r[key] for r in results) / len(results)

        return avg_results

    def _evaluate_self_consistency(self, responses):
        """Evaluate self-consistency for multiple generations of same prompt"""
        if len(responses) < 2:
            return {"consistency": 1.0, "diversity": 0.0}

        # Calculate pairwise similarities
        similarities = []
        for i in range(len(responses)):
            for j in range(i+1, len(responses)):
                rouge_score = self.rouge_scorer.score(responses[i], responses[j])
                similarities.append(rouge_score["rougeL"].fmeasure)

        avg_similarity = sum(similarities) / len(similarities)

        return {
            "consistency": avg_similarity,  # Lower similarity = more diverse
            "diversity": 1 - avg_similarity  # Higher diversity score
        }

    def _check_factual_consistency(self, generated, reference):
        """Check factual consistency (simplified)"""
        # Simple check for contradictory statements
        contradictions = ["not", "isn't", "doesn't", "wasn't"]

        gen_lower = generated.lower()
        ref_lower = reference.lower()

        # Very basic consistency check
        gen_words = set(gen_lower.split())
        ref_words = set(ref_lower.split())

        overlap = len(gen_words & ref_words)
        total = len(gen_words | ref_words)

        return overlap / total if total > 0 else 0

    def benchmark_models(self, models, test_prompts, num_samples=3):
        """Benchmark multiple models on test prompts"""
        results = {}

        for model_name, generator in models.items():
            model_results = []

            for prompt in test_prompts:
                responses = []
                for _ in range(num_samples):
                    try:
                        result = generator.run(prompt=prompt)
                        responses.append(result["replies"][0])
                    except:
                        responses.append("")

                # Evaluate self-consistency
                consistency_results = self._evaluate_self_consistency(responses)
                model_results.append(consistency_results)

            # Average results across prompts
            avg_results = {}
            for key in model_results[0].keys():
                avg_results[key] = sum(r[key] for r in model_results) / len(model_results)

            results[model_name] = avg_results

        return results

# Usage
evaluator = GenerationEvaluator()

# Test responses
generated = ["Machine learning is a subset of AI that learns from data."]
references = ["Machine learning is a method of data analysis that automates analytical model building."]

results = evaluator.evaluate_generation(generated, references)
print("Evaluation Results:")
for metric, score in results.items():
    print(f"  {metric}: {score:.3f}")
```

## 🎯 Best Practices

### Prompt Engineering
1. **Be specific** about the desired output format and style
2. **Provide examples** in the prompt when possible
3. **Use system messages** to set context and behavior
4. **Specify constraints** (length, tone, format)
5. **Test and iterate** on prompts regularly

### Model Selection
1. **Match model capabilities** to your use case complexity
2. **Consider cost-performance trade-offs** between models
3. **Use specialized models** for domain-specific tasks
4. **Implement fallbacks** for reliability
5. **Monitor model performance** over time

### Generation Optimization
1. **Tune generation parameters** for your specific use case
2. **Implement caching** for repeated queries
3. **Use streaming** for better user experience
4. **Batch requests** when possible
5. **Monitor token usage** and costs

## 📈 Next Steps

With LLM integration complete, you're ready to:

- **[Chapter 5: Pipelines & Workflows](05-pipelines-workflows.md)** - Build complex search workflows
- **[Chapter 6: Evaluation & Optimization](06-evaluation-optimization.md)** - Measure and improve search quality
- **[Chapter 7: Custom Components](07-custom-components.md)** - Extend Haystack with custom functionality

---

**Ready to build complex search workflows? Continue to [Chapter 5: Pipelines & Workflows](05-pipelines-workflows.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `query`, `responses` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Generators & LLMs` as an operating subsystem inside **Haystack: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `documents`, `generator`, `response` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Generators & LLMs` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `query` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `responses`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Haystack](https://github.com/deepset-ai/haystack)
  Why it matters: authoritative reference on `Haystack` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `query` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Retrievers & Search](03-retrievers-search.md)
- [Next Chapter: Chapter 5: Pipelines & Workflows](05-pipelines-workflows.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
