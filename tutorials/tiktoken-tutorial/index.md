---
layout: default
title: "tiktoken Tutorial"
nav_order: 94
has_children: true
---

# tiktoken Tutorial: OpenAI Token Encoding & Optimization

> Master tiktoken, OpenAI's fast BPE tokenizer, to accurately count tokens, optimize prompts, and reduce API costs.

[![Stars](https://img.shields.io/github/stars/openai/tiktoken?style=social)](https://github.com/openai/tiktoken)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-Rust-blue)](https://github.com/openai/tiktoken)

## 🎯 What is tiktoken?

**tiktoken** is a fast Byte Pair Encoding (BPE) tokenizer library created by OpenAI for use with their models. It's 3-6x faster than comparable tokenizers and provides accurate token counting for GPT models, enabling precise cost estimation and context management.

### Key Features

| Feature | Description |
|:--------|:------------|
| **Fast Performance** | 3-6x faster than alternatives, written in Rust |
| **Accurate Counting** | Exact token counts for GPT-3.5, GPT-4, embeddings |
| **Multiple Encodings** | cl100k_base (GPT-4), p50k_base (GPT-3.5), r50k_base (legacy) |
| **Educational** | Includes `tiktoken._educational` for learning BPE |
| **Reversible** | Lossless encoding/decoding of any text |
| **Efficient** | ~4 bytes per token on average, excellent compression |

## Architecture Overview

```mermaid
graph LR
    subgraph Input["Input Text"]
        TEXT[Raw String]
    end

    subgraph Tokenizer["tiktoken Tokenizer"]
        LOAD[Load Encoding]
        BPE[BPE Algorithm]
        VOCAB[Vocabulary Lookup]
        CACHE[Token Cache]
    end

    subgraph Output["Outputs"]
        TOKENS[Token IDs]
        COUNT[Token Count]
        DECODED[Decoded Text]
    end

    TEXT --> LOAD
    LOAD --> BPE
    BPE --> VOCAB
    VOCAB --> CACHE
    CACHE --> TOKENS
    TOKENS --> COUNT
    TOKENS --> DECODED

    classDef input fill:#e1f5fe,stroke:#01579b
    classDef process fill:#f3e5f5,stroke:#4a148c
    classDef output fill:#e8f5e8,stroke:#1b5e20

    class TEXT input
    class LOAD,BPE,VOCAB,CACHE process
    class TOKENS,COUNT,DECODED output
```

## Tutorial Structure

> Status: This index is currently the published roadmap for the tutorial. Chapter pages are in progress.

| Chapter | Topic | What You'll Learn |
|:--------|:------|:------------------|
| **1. Getting Started (Planned)** | Basics | Installation, first encoding, BPE fundamentals |
| **2. Tokenization Mechanics (Planned)** | Deep Dive | How BPE works, encoding algorithms, vocabulary |
| **3. Practical Applications (Planned)** | Use Cases | Token counting, cost estimation, prompt optimization |
| **4. Educational Module (Planned)** | Learning | Training custom tokenizers, visualization tools |
| **5. Optimization Strategies (Planned)** | Performance | Caching, batch processing, performance tuning |

## Tech Stack

| Component | Technology |
|:----------|:-----------|
| **Core Library** | Rust (for performance) |
| **Python Bindings** | PyO3 |
| **Algorithm** | Byte Pair Encoding (BPE) |
| **Supported Encodings** | cl100k_base, p50k_base, r50k_base, p50k_edit, gpt2 |
| **Installation** | pip (pre-compiled wheels) |

## What You'll Learn

By the end of this tutorial, you'll be able to:

- **Count Tokens Accurately** for any GPT model before making API calls
- **Understand BPE** and how tokenization affects model behavior
- **Optimize Prompts** to stay within context limits and reduce costs
- **Estimate API Costs** precisely using token counts
- **Handle Edge Cases** like special tokens, Unicode, and rare characters
- **Build Custom Tokenizers** using the educational module
- **Integrate with Applications** for real-time token management

## Prerequisites

- **Python** programming experience
- **Basic understanding** of strings and encoding
- **OpenAI API** usage helpful but not required
- **pip** for package installation

## Related Tutorials

**Prerequisites:**
- None - this is a foundational utility tutorial

**Complementary:**
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/) - Using tiktoken with OpenAI API
- [LangChain Tutorial](../langchain-tutorial/) - Token counting in LLM frameworks
- [LlamaIndex Tutorial](../llamaindex-tutorial/) - Token management in RAG systems

**Next Steps:**
- Prompt optimization techniques
- Context window management
- Cost-effective API usage patterns

## Why Token Counting Matters

### Cost Estimation
```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode("Your prompt here")
cost = len(tokens) * 0.00003  # GPT-4 Turbo pricing
print(f"Estimated cost: ${cost:.6f}")
```

### Context Management
```python
max_tokens = 8192  # GPT-4 context limit
prompt_tokens = len(enc.encode(prompt))
max_response = max_tokens - prompt_tokens
```

### Chunking for RAG
```python
def chunk_text(text, max_tokens=500):
    tokens = enc.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [enc.decode(chunk) for chunk in chunks]
```

## Supported Encodings

| Encoding | Models | Vocabulary Size | Use Case |
|:---------|:-------|:----------------|:---------|
| **cl100k_base** | GPT-4, GPT-3.5 Turbo, text-embedding-3 | 100,256 | Current production models |
| **p50k_base** | GPT-3 (Davinci, Curie) | 50,281 | Legacy GPT-3 models |
| **r50k_base** | GPT-2, early GPT-3 | 50,257 | Legacy/research |
| **p50k_edit** | text-davinci-edit-001 | 50,281 | Edit models |
| **gpt2** | GPT-2 | 50,257 | Research/compatibility |

---

Ready to begin? Review the roadmap above while chapter pages are being finalized.

---

*Built with insights from the [tiktoken repository](https://github.com/openai/tiktoken) and OpenAI tokenization documentation.*
