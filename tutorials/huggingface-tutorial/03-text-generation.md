---
layout: default
title: "Chapter 3: Text Generation"
parent: "HuggingFace Transformers Tutorial"
nav_order: 3
---

# Chapter 3: Text Generation

> Master the art of AI-powered text generation with Transformers models.

## 🎯 Overview

This chapter explores text generation capabilities in HuggingFace Transformers, covering everything from creative writing to code generation and conversational AI. You'll learn to use and fine-tune models like GPT, T5, and other generative architectures.

## 📝 Understanding Text Generation

### Generation Strategies

#### 1. **Greedy Decoding**
- Always selects the most probable next token
- Fast but can produce repetitive text
- Good for deterministic tasks

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

inputs = tokenizer("The future of AI is", return_tensors="pt")
outputs = model.generate(
    inputs.input_ids,
    max_length=50,
    do_sample=False,  # Greedy decoding
    num_beams=1
)

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
# "The future of AI is bright. The technology is advancing rapidly..."
```

#### 2. **Sampling Methods**
- Introduces randomness for more creative outputs
- Temperature controls randomness
- Top-k and top-p filtering improve quality

```python
# Temperature sampling
outputs = model.generate(
    inputs.input_ids,
    max_length=100,
    do_sample=True,
    temperature=0.7,  # Lower = more focused, Higher = more creative
    top_k=50,         # Consider top 50 tokens
    top_p=0.9         # Nucleus sampling
)

# Beam search for quality
outputs = model.generate(
    inputs.input_ids,
    max_length=100,
    num_beams=5,      # Beam search with 5 beams
    early_stopping=True,
    no_repeat_ngram_size=2  # Avoid repetition
)
```

#### 3. **Advanced Techniques**
- Contrastive search
- Diverse beam search
- Length penalty and repetition penalty

```python
# Contrastive search (improves quality and reduces repetition)
outputs = model.generate(
    inputs.input_ids,
    max_length=100,
    do_sample=True,
    top_k=4,
    penalty_alpha=0.6,  # Contrastive search parameter
    repetition_penalty=1.2
)

# Length-aware generation
outputs = model.generate(
    inputs.input_ids,
    min_length=50,
    max_length=100,
    length_penalty=2.0,  # Favor longer sequences
    num_beams=4
)
```

## 🤖 Popular Text Generation Models

### GPT Series (OpenAI-inspired)

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def generate_story(prompt, max_length=200):
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=3,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
    )

    story = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return story

# Generate a creative story
prompt = "In a world where dreams could be harvested like crops,"
story = generate_story(prompt)
print(story)
```

### T5 (Text-to-Text Transfer Transformer)

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer

# T5 for various text-to-text tasks
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

def t5_generate(task_prefix, input_text):
    input_with_prefix = f"{task_prefix}: {input_text}"
    inputs = tokenizer(input_with_prefix, return_tensors="pt")

    outputs = model.generate(
        inputs.input_ids,
        max_length=100,
        num_beams=4,
        early_stopping=True
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

# Different T5 tasks
print(t5_generate("translate English to French", "Hello, how are you?"))
print(t5_generate("summarize", "Long article text here..."))
print(t5_generate("question", "What is the capital of France?"))
```

### Code Generation Models

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# CodeLlama for code generation
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")

def generate_code(prompt, language="python"):
    full_prompt = f"Write a {language} function that {prompt}"

    inputs = tokenizer(full_prompt, return_tensors="pt")

    outputs = model.generate(
        inputs.input_ids,
        max_length=200,
        temperature=0.2,  # Lower temperature for code
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return code

# Generate code
code = generate_code("calculates the fibonacci sequence recursively")
print(code)
```

## 🎨 Creative Writing Applications

### Story Generation Pipeline

```python
from transformers import pipeline
import torch

class StoryGenerator:
    def __init__(self):
        self.generator = pipeline(
            "text-generation",
            model="gpt2-large",
            device=0 if torch.cuda.is_available() else -1
        )

    def generate_story(self, premise, genre="fantasy", length="medium"):
        # Define genre-specific prompts
        genre_prompts = {
            "fantasy": "In a magical kingdom, ",
            "scifi": "In the year 2147, ",
            "mystery": "The detective discovered that ",
            "romance": "Their eyes met across the crowded room, "
        }

        prompt = genre_prompts.get(genre, "") + premise

        # Adjust generation parameters based on desired length
        length_params = {
            "short": {"max_length": 100, "min_length": 50},
            "medium": {"max_length": 300, "min_length": 150},
            "long": {"max_length": 600, "min_length": 300}
        }

        params = length_params.get(length, length_params["medium"])
        params.update({
            "num_return_sequences": 1,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True,
            "no_repeat_ngram_size": 3,
            "repetition_penalty": 1.2
        })

        result = self.generator(prompt, **params)
        story = result[0]['generated_text']

        return self._post_process_story(story)

    def _post_process_story(self, story):
        """Clean up and format the generated story"""
        # Remove the original prompt if it appears
        # Add proper paragraph breaks
        # Ensure the story ends properly
        return story.strip()

# Usage
generator = StoryGenerator()
story = generator.generate_story(
    "a young wizard discovers an ancient artifact",
    genre="fantasy",
    length="medium"
)
print(story)
```

### Dialogue Generation

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

class DialogueGenerator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

    def generate_response(self, conversation_history, personality="friendly"):
        # Format conversation history
        chat_history = self._format_history(conversation_history)

        # Add personality cues
        personality_prefixes = {
            "friendly": "I'm happy to help! ",
            "professional": "Certainly, let me assist you. ",
            "humorous": "Well, that's an interesting question! ",
            "concise": "Here's what you need to know: "
        }

        if personality in personality_prefixes:
            chat_history = personality_prefixes[personality] + chat_history

        # Generate response
        inputs = self.tokenizer.encode(chat_history + self.tokenizer.eos_token, return_tensors="pt")

        outputs = self.model.generate(
            inputs,
            max_length=len(inputs[0]) + 50,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1
        )

        response = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        return response.strip()

    def _format_history(self, history):
        """Format conversation history for the model"""
        formatted = ""
        for message in history[-3:]:  # Keep last 3 exchanges
            formatted += message + self.tokenizer.eos_token
        return formatted

# Usage
dialogue_gen = DialogueGenerator()
history = [
    "Hello, how can I help you today?",
    "I'm looking for information about machine learning.",
    "That's a fascinating field! What specifically interests you?"
]

response = dialogue_gen.generate_response(history, personality="helpful")
print(response)
```

## 📝 Advanced Text Generation Techniques

### Controlled Generation with Guidance

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class ControlledGenerator:
    def __init__(self, model_name="gpt2-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Define control tokens/categories
        self.control_categories = {
            "positive": ["good", "great", "excellent", "amazing", "wonderful"],
            "negative": ["bad", "terrible", "awful", "horrible", "disappointing"],
            "technical": ["algorithm", "system", "process", "method", "technique"],
            "creative": ["imagine", "dream", "fantasy", "creative", "artistic"]
        }

    def generate_with_bias(self, prompt, bias_category, strength=2.0):
        """Generate text with bias towards certain categories"""
        inputs = self.tokenizer(prompt, return_tensors="pt")

        # Get bias tokens
        bias_tokens = self.control_categories.get(bias_category, [])
        bias_ids = [self.tokenizer.encode(token, add_special_tokens=False)[0]
                   for token in bias_tokens if token in self.tokenizer.get_vocab()]

        # Create bias mask
        vocab_size = self.tokenizer.vocab_size
        bias_mask = torch.ones(vocab_size)

        for token_id in bias_ids:
            bias_mask[token_id] = strength

        # Generate with bias
        outputs = self.model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=100,
            do_sample=True,
            temperature=0.8,
            repetition_penalty=1.2,
            logits_processor=[self._create_bias_processor(bias_mask)]
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _create_bias_processor(self, bias_mask):
        """Create a logits processor for biasing generation"""
        class BiasLogitsProcessor:
            def __init__(self, bias_mask):
                self.bias_mask = bias_mask

            def __call__(self, input_ids, scores):
                scores = scores * self.bias_mask
                return scores

        return BiasLogitsProcessor(bias_mask)

# Usage
generator = ControlledGenerator()
positive_review = generator.generate_with_bias(
    "The new smartphone has", "positive", strength=3.0
)
print(positive_review)
```

### Multi-Step Generation Pipeline

```python
class MultiStepGenerator:
    def __init__(self):
        # Initialize different models for different steps
        self.outline_generator = pipeline("text-generation", model="gpt2-medium")
        self.content_generator = pipeline("text-generation", model="gpt2-large")
        self.editor = pipeline("text2text-generation", model="t5-base")

    def generate_article(self, topic, word_count=800):
        """Generate a complete article through multiple steps"""

        # Step 1: Generate outline
        outline_prompt = f"Create a detailed outline for an article about {topic}:"
        outline_result = self.outline_generator(
            outline_prompt,
            max_length=200,
            num_return_sequences=1,
            temperature=0.7
        )
        outline = outline_result[0]['generated_text']

        # Step 2: Generate content for each section
        sections = self._parse_outline(outline)
        content_sections = []

        for section in sections:
            section_prompt = f"Write a detailed section about: {section}"
            section_content = self.content_generator(
                section_prompt,
                max_length=300,
                temperature=0.8,
                do_sample=True
            )[0]['generated_text']
            content_sections.append(section_content)

        # Step 3: Combine and edit
        full_content = "\n\n".join(content_sections)

        # Step 4: Post-edit for coherence
        edit_prompt = f"Edit this article for clarity and flow: {full_content[:1000]}..."
        edited_content = self.editor(edit_prompt, max_length=1000)[0]['generated_text']

        return {
            "outline": outline,
            "content": edited_content,
            "sections": len(sections),
            "word_count": len(edited_content.split())
        }

    def _parse_outline(self, outline):
        """Parse outline into sections"""
        # Simple parsing logic - can be improved
        lines = outline.split('\n')
        sections = [line.strip('- ').strip() for line in lines
                   if line.strip().startswith(('-', '1.', '2.', '3.'))]
        return sections[:5]  # Limit to 5 sections

# Usage
generator = MultiStepGenerator()
article = generator.generate_article("The Future of Artificial Intelligence")
print(f"Generated article with {article['word_count']} words")
print(f"Outline: {article['outline'][:200]}...")
```

## 🔧 Optimization Techniques

### Memory-Efficient Generation

```python
from transformers import BitsAndBytesConfig
import torch

# 8-bit quantization for memory efficiency
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0
)

model_8bit = AutoModelForCausalLM.from_pretrained(
    "gpt2-xl",
    quantization_config=quantization_config,
    device_map="auto"
)

# Use with smaller batch sizes
def generate_efficient(text, max_length=100):
    inputs = tokenizer(text, return_tensors="pt").to(model_8bit.device)

    with torch.no_grad():
        outputs = model_8bit.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=max_length,
            do_sample=True,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Batch Generation

```python
def batch_generate(prompts, batch_size=4):
    """Generate text for multiple prompts efficiently"""
    all_generated = []

    for i in range(0, len(prompts), batch_size):
        batch_prompts = prompts[i:i + batch_size]

        # Tokenize batch
        inputs = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        # Generate batch
        outputs = model.generate(
            **inputs,
            max_length=100,
            do_sample=True,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode batch
        batch_generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        all_generated.extend(batch_generated)

    return all_generated

# Usage
prompts = [
    "The benefits of renewable energy include",
    "Machine learning algorithms can",
    "The future of transportation involves",
    "Climate change affects"
]

results = batch_generate(prompts)
for prompt, result in zip(prompts, results):
    print(f"Prompt: {prompt}")
    print(f"Generated: {result}")
    print("---")
```

## 🎯 Best Practices

### Quality vs. Speed Trade-offs

| Approach | Quality | Speed | Use Case |
|----------|---------|-------|----------|
| **Greedy** | Medium | Fastest | Deterministic tasks |
| **Sampling (T=0.7)** | High | Fast | Creative writing |
| **Beam Search** | Highest | Slow | High-quality generation |
| **Contrastive Search** | High | Medium | Balanced quality/speed |

### Common Pitfalls and Solutions

1. **Repetitive Text**
   - **Solution**: Increase `repetition_penalty`, use `no_repeat_ngram_size`

2. **Off-topic Generation**
   - **Solution**: Use more specific prompts, add constraints

3. **Incoherent Output**
   - **Solution**: Lower temperature, use better prompts, post-process

4. **Memory Issues**
   - **Solution**: Use quantization, smaller models, batch processing

## 📈 Next Steps

With text generation mastered, you're ready to:

- **[Chapter 4: Question Answering](04-question-answering.md)** - Build Q&A systems with custom knowledge bases
- **[Chapter 5: Named Entity Recognition](05-named-entity-recognition.md)** - Extract structured information from text
- **[Chapter 6: Translation & Multilingual Models](06-translation-multilingual.md)** - Work with cross-language AI applications

---

**Ready to build intelligent Q&A systems? Continue to [Chapter 4: Question Answering](04-question-answering.md)!** 🚀