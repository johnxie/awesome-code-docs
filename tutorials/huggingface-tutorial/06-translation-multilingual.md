---
layout: default
title: "Chapter 6: Translation & Multilingual Models"
parent: "HuggingFace Transformers Tutorial"
nav_order: 6
---

# Chapter 6: Translation & Multilingual Models

> Master cross-language AI applications with translation and multilingual models.

## 🎯 Overview

This chapter covers machine translation and multilingual language models using HuggingFace Transformers. You'll learn to build translation systems, work with multilingual models, and create applications that operate across multiple languages.

## 🌐 Machine Translation

### Using Pre-trained Translation Models

```python
from transformers import pipeline

# Initialize translation pipeline
translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-en-fr",
    tokenizer="Helsinki-NLP/opus-mt-en-fr"
)

# Translate text
english_text = "Hello, how are you today?"
french_translation = translator(english_text)

print(f"English: {english_text}")
print(f"French: {french_translation[0]['translation_text']}")

# Output:
# English: Hello, how are you today?
# French: Bonjour, comment allez-vous aujourd'hui ?
```

### Advanced Translation Pipeline

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class AdvancedTranslator:
    def __init__(self):
        # Load multiple translation models
        self.models = {}
        self.tokenizers = {}
        self._load_translation_models()

    def _load_translation_models(self):
        """Load various translation models"""
        translation_pairs = [
            ("en", "fr", "Helsinki-NLP/opus-mt-en-fr"),
            ("en", "de", "Helsinki-NLP/opus-mt-en-de"),
            ("fr", "en", "Helsinki-NLP/opus-mt-fr-en"),
            ("de", "en", "Helsinki-NLP/opus-mt-de-en"),
        ]

        for src, tgt, model_name in translation_pairs:
            try:
                self.tokenizers[f"{src}-{tgt}"] = AutoTokenizer.from_pretrained(model_name)
                self.models[f"{src}-{tgt}"] = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                print(f"Loaded {src}→{tgt} translation model")
            except Exception as e:
                print(f"Failed to load {src}→{tgt} model: {e}")

    def translate(self, text, source_lang="en", target_lang="fr", **kwargs):
        """Translate text between languages"""
        model_key = f"{source_lang}-{target_lang}"

        if model_key not in self.models:
            raise ValueError(f"Translation model for {source_lang}→{target_lang} not available")

        tokenizer = self.tokenizers[model_key]
        model = self.models[model_key]

        # Tokenize input
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        # Generate translation
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=kwargs.get("max_length", 200),
                num_beams=kwargs.get("num_beams", 4),
                early_stopping=True,
                length_penalty=kwargs.get("length_penalty", 2.0),
                no_repeat_ngram_size=kwargs.get("no_repeat_ngram_size", 3)
            )

        # Decode translation
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "original_text": text,
            "translation": translation,
            "source_language": source_lang,
            "target_language": target_lang,
            "model_used": model_key
        }

    def batch_translate(self, texts, source_lang="en", target_lang="fr"):
        """Translate multiple texts efficiently"""
        translations = []

        for text in texts:
            try:
                result = self.translate(text, source_lang, target_lang)
                translations.append(result)
            except Exception as e:
                translations.append({
                    "original_text": text,
                    "error": str(e)
                })

        return translations

# Usage
translator = AdvancedTranslator()

# Single translation
result = translator.translate("Machine learning is transforming industries.", "en", "fr")
print(f"Translation: {result['translation']}")

# Batch translation
texts = [
    "Artificial intelligence is the future.",
    "Natural language processing enables human-computer interaction.",
    "Computer vision allows machines to see and understand images."
]

batch_results = translator.batch_translate(texts, "en", "de")
for result in batch_results:
    print(f"EN: {result['original_text']}")
    print(f"DE: {result['translation']}")
    print("---")
```

## 🌍 Multilingual Language Models

### Using Multilingual BERT

```python
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
import numpy as np

class MultilingualEmbeddings:
    def __init__(self):
        # Load multilingual BERT
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
        self.model = AutoModel.from_pretrained("bert-base-multilingual-cased")

        # Supported languages (subset)
        self.supported_languages = {
            "en": "English",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean"
        }

    def get_embeddings(self, texts, languages=None):
        """Generate embeddings for texts in multiple languages"""
        if isinstance(texts, str):
            texts = [texts]

        if languages and len(languages) != len(texts):
            raise ValueError("Number of languages must match number of texts")

        embeddings = []

        for i, text in enumerate(texts):
            # Tokenize with appropriate language
            lang = languages[i] if languages else "en"

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )

            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling over token embeddings
                embedding = outputs.last_hidden_state.mean(dim=1).squeeze()

            embeddings.append({
                "text": text,
                "language": lang,
                "embedding": embedding.numpy(),
                "embedding_shape": embedding.shape
            })

        return embeddings

    def find_similar_texts(self, query_text, candidate_texts, query_lang="en", candidate_langs=None):
        """Find texts similar to query across languages"""
        # Get embeddings
        query_embedding = self.get_embeddings([query_text], [query_lang])[0]["embedding"]

        candidate_embeddings = self.get_embeddings(
            candidate_texts,
            candidate_langs or ["en"] * len(candidate_texts)
        )

        # Calculate similarities
        similarities = []
        for i, candidate in enumerate(candidate_embeddings):
            similarity = self._cosine_similarity(
                query_embedding,
                candidate["embedding"]
            )
            similarities.append({
                "text": candidate["text"],
                "language": candidate["language"],
                "similarity": similarity,
                "index": i
            })

        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)

        return similarities

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

# Usage
multilingual_emb = MultilingualEmbeddings()

# Cross-language similarity
query = "artificial intelligence"
candidates = [
    "intelligence artificielle",  # French
    "Inteligencia artificial",    # Spanish
    "Künstliche Intelligenz",     # German
    "artificial intelligence",    # English
    "cars and trucks"            # Unrelated
]

languages = ["fr", "es", "de", "en", "en"]

similar_texts = multilingual_emb.find_similar_texts(
    query, candidates, "en", languages
)

print("Most similar texts to 'artificial intelligence':")
for result in similar_texts[:3]:
    print(".3f")
```

### Language Detection and Routing

```python
from transformers import pipeline
import langid

class MultilingualProcessor:
    def __init__(self):
        self.language_detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
        self.translators = {}
        self._initialize_translators()

    def _initialize_translators(self):
        """Initialize translation models for common language pairs"""
        # This would load various translation models
        pass

    def process_multilingual_text(self, text, target_language="en"):
        """Process text in any language and translate to target language"""
        # Detect language
        lang_result = self.language_detector(text[:512])  # Limit input size
        detected_lang = lang_result[0]["label"]

        print(f"Detected language: {detected_lang}")

        # If already in target language, return as-is
        if detected_lang == target_language:
            return {
                "original_text": text,
                "processed_text": text,
                "language": detected_lang,
                "translated": False
            }

        # Translate to target language
        translation = self._translate_text(text, detected_lang, target_language)

        return {
            "original_text": text,
            "processed_text": translation,
            "original_language": detected_lang,
            "target_language": target_language,
            "translated": True
        }

    def _translate_text(self, text, source_lang, target_lang):
        """Translate text using appropriate model"""
        # Simplified translation - in practice, use proper translation models
        # This is a placeholder implementation

        # For demo purposes, we'll use a simple approach
        # In production, you'd use models like Helsinki-NLP/opus-mt-*

        translation_map = {
            "fr-en": {
                "Bonjour": "Hello",
                "Comment allez-vous": "How are you",
                "intelligence artificielle": "artificial intelligence"
            },
            "es-en": {
                "Hola": "Hello",
                "inteligencia artificial": "artificial intelligence"
            }
        }

        key = f"{source_lang}-{target_lang}"
        translations = translation_map.get(key, {})

        translated_text = text
        for source_word, target_word in translations.items():
            translated_text = translated_text.replace(source_word, target_word)

        return translated_text

    def create_multilingual_qa_system(self):
        """Create a QA system that works across languages"""
        return MultilingualQASystem(self)

class MultilingualQASystem:
    def __init__(self, processor):
        self.processor = processor
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    def answer_question(self, question, context, question_lang=None, context_lang=None):
        """Answer questions with multilingual support"""
        # Process question
        if question_lang:
            processed_question = self.processor.process_multilingual_text(question, "en")
            question_text = processed_question["processed_text"]
        else:
            question_text = question

        # Process context
        if context_lang:
            processed_context = self.processor.process_multilingual_text(context, "en")
            context_text = processed_context["processed_text"]
        else:
            context_text = context

        # Answer question
        answer = self.qa_pipeline(question=question_text, context=context_text)

        return {
            "question": question,
            "context": context,
            "answer": answer["answer"],
            "confidence": answer["score"],
            "question_language": question_lang,
            "context_language": context_lang
        }

# Usage
processor = MultilingualProcessor()

# Process multilingual text
result = processor.process_multilingual_text(
    "L'intelligence artificielle transforme notre monde",
    target_language="en"
)

print(f"Original: {result['original_text']}")
print(f"Translated: {result['processed_text']}")
print(f"Language: {result['original_language']}")

# Multilingual QA
qa_system = processor.create_multilingual_qa_system()

question = "¿Qué es la inteligencia artificial?"
context = "La inteligencia artificial es una rama de la informática que busca crear máquinas capaces de realizar tareas que requieren inteligencia humana."

answer = qa_system.answer_question(question, context, "es", "es")
print(f"Question: {answer['question']}")
print(f"Answer: {answer['answer']}")
```

## 🎭 Cross-Language Transfer Learning

### Zero-Shot Cross-Lingual Transfer

```python
from transformers import pipeline

class CrossLingualClassifier:
    def __init__(self):
        # Use multilingual model for zero-shot classification
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=0 if torch.cuda.is_available() else -1
        )

        # Define universal labels that work across languages
        self.universal_labels = [
            "positive", "negative", "neutral",  # Sentiment
            "technology", "business", "sports", "politics", "entertainment",  # Topics
            "question", "statement", "command", "request"  # Speech acts
        ]

    def classify_multilingual_text(self, texts, task="sentiment"):
        """Classify texts in any language"""
        if isinstance(texts, str):
            texts = [texts]

        # Select appropriate labels based on task
        task_labels = self._get_task_labels(task)

        results = []
        for text in texts:
            # Classify using zero-shot approach
            result = self.classifier(text, task_labels, multi_label=False)

            # Get top prediction
            top_label = result["labels"][0]
            confidence = result["scores"][0]

            results.append({
                "text": text,
                "classification": top_label,
                "confidence": confidence,
                "task": task,
                "all_scores": dict(zip(result["labels"], result["scores"]))
            })

        return results

    def _get_task_labels(self, task):
        """Get appropriate labels for different classification tasks"""
        label_sets = {
            "sentiment": ["positive", "negative", "neutral"],
            "topic": ["technology", "business", "sports", "politics", "entertainment", "health", "science", "arts"],
            "intent": ["question", "statement", "command", "request", "complaint", "praise"],
            "emotion": ["happy", "sad", "angry", "surprised", "fearful", "disgusted"],
            "urgency": ["urgent", "important", "normal", "low priority"]
        }

        return label_sets.get(task, self.universal_labels)

    def translate_and_classify(self, texts, languages, task="sentiment"):
        """Translate texts to English first, then classify"""
        translator = AdvancedTranslator()

        # Translate all texts to English
        english_texts = []
        for text, lang in zip(texts, languages):
            if lang != "en":
                translation = translator.translate(text, lang, "en")
                english_texts.append(translation["translation"])
            else:
                english_texts.append(text)

        # Classify in English
        return self.classify_multilingual_text(english_texts, task)

# Usage
cross_lingual = CrossLingualClassifier()

# Zero-shot classification in different languages
texts = [
    "This product is amazing!",  # English
    "Ce produit est incroyable !",  # French
    "¡Este producto es increíble!",  # Spanish
    "Dieses Produkt ist großartig!",  # German
]

languages = ["en", "fr", "es", "de"]

results = cross_lingual.classify_multilingual_text(texts, task="sentiment")

for result in results:
    print(f"Text: {result['text']}")
    print(f"Sentiment: {result['classification']} (confidence: {result['confidence']:.3f})")
    print("---")
```

## 📊 Building Multilingual Applications

### Multilingual Chatbot

```python
class MultilingualChatbot:
    def __init__(self):
        self.language_processor = MultilingualProcessor()
        self.qa_system = self.language_processor.create_multilingual_qa_system()
        self.conversation_memory = {}

    def chat(self, message, user_id, language=None):
        """Handle multilingual conversation"""
        # Detect language if not provided
        if not language:
            lang_detection = self.language_processor.language_detector(message[:200])
            language = lang_detection[0]["label"]

        # Initialize user memory if needed
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = {
                "messages": [],
                "language": language,
                "context": []
            }

        # Add message to memory
        self.conversation_memory[user_id]["messages"].append({
            "text": message,
            "language": language,
            "timestamp": datetime.now()
        })

        # Get conversation context
        context = self._get_conversation_context(user_id)

        # Process message based on type
        response = self._process_message(message, context, language)

        # Add response to memory
        self.conversation_memory[user_id]["messages"].append({
            "text": response["text"],
            "language": response["language"],
            "timestamp": datetime.now(),
            "is_bot": True
        })

        return response

    def _process_message(self, message, context, language):
        """Process user message and generate response"""
        # Simple intent classification
        intent = self._classify_intent(message, language)

        if intent == "question":
            # Use QA system
            qa_response = self.qa_system.answer_question(
                message, context, language, "en"  # Assume context is in English
            )
            response_text = qa_response["answer"]

        elif intent == "greeting":
            response_text = self._get_greeting(language)

        elif intent == "farewell":
            response_text = self._get_farewell(language)

        else:
            # General conversation
            response_text = self._generate_general_response(message, language)

        # Translate response if needed
        if language != "en":
            translator = AdvancedTranslator()
            translation = translator.translate(response_text, "en", language)
            response_text = translation["translation"]

        return {
            "text": response_text,
            "language": language,
            "intent": intent,
            "confidence": 0.8  # Placeholder
        }

    def _classify_intent(self, message, language):
        """Simple intent classification"""
        message_lower = message.lower()

        # Simple rule-based classification
        if any(word in message_lower for word in ["?", "what", "how", "why", "when", "where", "who"]):
            return "question"
        elif any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "greeting"
        elif any(word in message_lower for word in ["bye", "goodbye", "see you", "farewell"]):
            return "farewell"
        else:
            return "general"

    def _get_greeting(self, language):
        """Get language-appropriate greeting"""
        greetings = {
            "en": "Hello! How can I help you today?",
            "fr": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
            "es": "¡Hola! ¿Cómo puedo ayudarte hoy?",
            "de": "Hallo! Wie kann ich Ihnen heute helfen?",
            "it": "Ciao! Come posso aiutarti oggi?",
        }
        return greetings.get(language, greetings["en"])

    def _get_farewell(self, language):
        """Get language-appropriate farewell"""
        farewells = {
            "en": "Goodbye! Have a great day!",
            "fr": "Au revoir ! Passez une excellente journée !",
            "es": "¡Adiós! ¡Que tengas un gran día!",
            "de": "Auf Wiedersehen! Einen schönen Tag noch!",
            "it": "Arrivederci! Buona giornata!",
        }
        return farewells.get(language, farewells["en"])

    def _generate_general_response(self, message, language):
        """Generate general conversational response"""
        # This would use a more sophisticated model in practice
        return f"I understand you're saying: {message}. How can I assist you further?"

    def _get_conversation_context(self, user_id, max_messages=5):
        """Get recent conversation context"""
        messages = self.conversation_memory[user_id]["messages"]
        recent_messages = messages[-max_messages:]

        # Combine into context string
        context_parts = []
        for msg in recent_messages:
            prefix = "User:" if not msg.get("is_bot", False) else "Assistant:"
            context_parts.append(f"{prefix} {msg['text']}")

        return "\n".join(context_parts)

# Usage
chatbot = MultilingualChatbot()

# Simulate conversation
responses = []

# English
response1 = chatbot.chat("Hello!", "user1", "en")
responses.append(response1)

# French
response2 = chatbot.chat("Comment allez-vous?", "user1", "fr")
responses.append(response2)

# Spanish
response3 = chatbot.chat("¿Qué puedes hacer?", "user1", "es")
responses.append(response3)

for i, response in enumerate(responses, 1):
    print(f"Response {i}: {response['text']} (Language: {response['language']})")
```

## 🎯 Best Practices for Multilingual AI

### Language Detection and Handling

1. **Use reliable language detection** models
2. **Handle code-switching** (multiple languages in one text)
3. **Preserve original language** when possible
4. **Provide translation options** to users

### Cross-Language Transfer

1. **Leverage multilingual models** like mBERT, XLM-R
2. **Fine-tune on target languages** when possible
3. **Use translation as fallback** for low-resource languages
4. **Consider cultural context** in responses

### Performance Optimization

1. **Cache translations** for frequently used phrases
2. **Use appropriate model sizes** for different languages
3. **Implement language-specific optimizations**
4. **Monitor performance** across different languages

## 📈 Next Steps

With multilingual capabilities mastered, you're ready to:

- **[Chapter 7: Fine-tuning Models](07-fine-tuning.md)** - Customize models for specific tasks
- **[Chapter 8: Production Deployment](08-production-deployment.md)** - Scale Transformers applications

---

**Ready to fine-tune your own AI models? Continue to [Chapter 7: Fine-tuning Models](07-fine-tuning.md)!** 🚀