---
layout: default
title: "n8n AI Tutorial - Chapter 3: Document AI"
nav_order: 3
has_children: false
parent: n8n AI Tutorial
---

# Chapter 3: Document AI and Content Processing

Welcome to **Chapter 3: Document AI and Content Processing**. In this part of **n8n AI Tutorial: Workflow Automation with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Extract information from PDFs, images, web pages, and documents using AI-powered processing.

## Document Processing Nodes

n8n provides various nodes for processing different document types with AI assistance.

## PDF Processing

### PDF to Text Extraction

```json
{
  "parameters": {
    "operation": "pdfToText",
    "binaryData": true,
    "dataPropertyName": "data",
    "options": {
      "mimeType": "application/pdf"
    }
  },
  "name": "Extract PDF Text",
  "type": "n8n-nodes-base.extractFromFile",
  "typeVersion": 1
}
```

### AI-Powered PDF Analysis

```json
{
  "nodes": [
    {
      "parameters": {
        "operation": "pdfToText",
        "binaryData": true,
        "dataPropertyName": "data"
      },
      "name": "PDF Extractor",
      "type": "n8n-nodes-base.extractFromFile"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "You are an expert document analyzer. Extract key information and provide a structured summary."
          },
          {
            "role": "user",
            "content": "Analyze this document and extract:\n1. Main topic\n2. Key findings\n3. Important dates\n4. Contact information\n\nDocument text:\n{{ $json.text }}"
          }
        ],
        "responseFormat": "json"
      },
      "name": "AI Document Analyzer",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ],
  "connections": {
    "PDF Extractor": {
      "main": [
        [
          {
            "node": "AI Document Analyzer",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Web Scraping with AI

### Web Page Content Extraction

```json
{
  "parameters": {
    "url": "={{ $json.website_url }}",
    "responseFormat": "html",
    "options": {
      "followRedirects": true,
      "timeout": 10000
    }
  },
  "name": "Web Scraper",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 1
}
```

### AI-Powered Web Content Analysis

```json
{
  "nodes": [
    {
      "parameters": {
        "url": "={{ $json.url }}",
        "responseFormat": "html"
      },
      "name": "Fetch Webpage",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "dataPropertyName": "data",
        "extractionValues": {
          "values": [
            {
              "key": "title",
              "cssSelector": "title",
              "returnValue": "text"
            },
            {
              "key": "content",
              "cssSelector": "body",
              "returnValue": "html"
            }
          ]
        }
      },
      "name": "Extract Content",
      "type": "n8n-nodes-base.html"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "You are a web content analyzer. Extract and summarize the key information from web pages."
          },
          {
            "role": "user",
            "content": "Summarize this webpage content in 3 key points:\n\nTitle: {{ $json.title }}\nContent: {{ $json.content }}"
          }
        ]
      },
      "name": "AI Content Summarizer",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Image Processing with AI

### Image Analysis

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Describe this image in detail:"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "={{ $json.image_url }}"
            }
          }
        ]
      }
    ]
  },
  "name": "Image Analyzer",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### OCR with AI Enhancement

```json
{
  "nodes": [
    {
      "parameters": {
        "operation": "ocr",
        "binaryData": true,
        "dataPropertyName": "data",
        "options": {
          "language": "eng",
          "tesseractOptions": {
            "psm": 3
          }
        }
      },
      "name": "OCR Extractor",
      "type": "n8n-nodes-base.extractFromFile"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "Clean and correct OCR text. Fix any errors and improve formatting."
          },
          {
            "role": "user",
            "content": "Correct this OCR text:\n{{ $json.text }}"
          }
        ]
      },
      "name": "AI Text Corrector",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Document Classification

### Automatic Document Categorization

```json
{
  "parameters": {
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "system",
        "content": "You are a document classifier. Analyze the content and classify it into one of these categories: invoice, contract, report, email, legal, technical, marketing, financial, medical, other."
      },
      {
        "role": "user",
        "content": "Classify this document:\n\n{{ $json.document_text }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Document Classifier",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Multi-Label Classification

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Analyze the document and assign multiple relevant tags from: urgent, confidential, legal, financial, technical, customer-related, internal, external, review-required, approved, rejected."
      },
      {
        "role": "user",
        "content": "Tag this document with relevant labels:\n{{ $json.content }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Document Tagger",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Information Extraction

### Structured Data Extraction

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Extract structured information from documents. Return valid JSON with the requested fields."
      },
      {
        "role": "user",
        "content": "Extract the following from this invoice:\n- Invoice number\n- Date\n- Vendor name\n- Total amount\n- Line items\n\nDocument: {{ $json.document_text }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Invoice Extractor",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Entity Recognition

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Extract named entities from text. Return JSON with arrays for: persons, organizations, locations, dates, amounts."
      },
      {
        "role": "user",
        "content": "Extract entities from:\n{{ $json.text }}"
      }
    ],
    "responseFormat": "json"
  },
  "name": "Entity Extractor",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Document Summarization

### Automatic Summarization

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are an expert document summarizer. Create concise, accurate summaries that capture the main points and key information."
      },
      {
        "role": "user",
        "content": "Summarize this document in 3-5 bullet points:\n\n{{ $json.document_text }}"
      }
    ],
    "maxTokens": 300
  },
  "name": "Document Summarizer",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Executive Summary Generation

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Create executive summaries for business documents. Focus on key decisions, actions, and outcomes."
      },
      {
        "role": "user",
        "content": "Create an executive summary for:\n{{ $json.document_text }}\n\nInclude: purpose, key findings, recommendations, next steps."
      }
    ],
    "responseFormat": "json"
  },
  "name": "Executive Summary",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Document Q&A System

### Interactive Document Query

```json
{
  "nodes": [
    {
      "parameters": {
        "model": "text-embedding-ada-002",
        "input": "={{ $json.document_chunks }}"
      },
      "name": "Create Embeddings",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "operation": "upsert",
        "pineconeIndex": "documents",
        "items": "={{ $json.embeddings.map((emb, i) => ({ id: $json.chunk_ids[i], values: emb, metadata: { text: $json.chunks[i] } })) }}"
      },
      "name": "Store in Vector DB",
      "type": "@n8n/n8n-nodes-langchain.pinecone"
    },
    {
      "parameters": {
        "model": "text-embedding-ada-002",
        "input": "={{ $json.question }}"
      },
      "name": "Query Embedding",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "operation": "getMany",
        "pineconeIndex": "documents",
        "query": "={{ $json.query_embedding[0] }}",
        "numberOfResults": 3
      },
      "name": "Retrieve Context",
      "type": "@n8n/n8n-nodes-langchain.pinecone"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "Answer questions based on the provided context. If the answer isn't in the context, say so."
          },
          {
            "role": "user",
            "content": "Context:\n{{ $json.context_chunks.join('\\n---\\n') }}\n\nQuestion: {{ $json.question }}"
          }
        ]
      },
      "name": "Generate Answer",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    }
  ]
}
```

## Automated Document Processing

### Email Document Processing

```json
{
  "nodes": [
    {
      "parameters": {
        "resource": "message",
        "operation": "getAll",
        "options": {
          "filter": "has:attachment filename:pdf"
        }
      },
      "name": "Gmail Trigger",
      "type": "n8n-nodes-base.gmail"
    },
    {
      "parameters": {
        "operation": "pdfToText",
        "binaryData": true,
        "dataPropertyName": "data"
      },
      "name": "Extract PDF",
      "type": "n8n-nodes-base.extractFromFile"
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "messages": [
          {
            "role": "system",
            "content": "Analyze this document and determine: 1) Document type 2) Priority level (high/medium/low) 3) Key action items 4) Response needed (yes/no)"
          },
          {
            "role": "user",
            "content": "Analyze: {{ $json.text }}"
          }
        ],
        "responseFormat": "json"
      },
      "name": "AI Document Analysis",
      "type": "@n8n/n8n-nodes-langchain.openAi"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.priority }}",
              "operation": "equal",
              "value2": "high"
            }
          ]
        }
      },
      "name": "High Priority Check",
      "type": "n8n-nodes-base.if"
    }
  ]
}
```

## Content Generation

### Automated Report Generation

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "You are a professional report writer. Create well-structured, comprehensive reports."
      },
      {
        "role": "user",
        "content": "Generate a business report with these sections:\n1. Executive Summary\n2. Current Situation\n3. Analysis\n4. Recommendations\n\nData: {{ $json.business_data }}"
      }
    ],
    "maxTokens": 2000
  },
  "name": "Report Generator",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

### Content Enhancement

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "Improve content quality: fix grammar, enhance clarity, add structure, make more engaging."
      },
      {
        "role": "user",
        "content": "Enhance this content:\n{{ $json.original_text }}"
      }
    ]
  },
  "name": "Content Enhancer",
  "type": "@n8n/n8n-nodes-langchain.openAi"
}
```

## Integration Patterns

### API-Based Document Processing

```python
import requests
import json

def process_document_with_n8n(document_url, webhook_url):
    """Send document to n8n workflow for processing."""

    payload = {
        "document_url": document_url,
        "processing_type": "analysis"
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        result = response.json()
        return {
            "summary": result.get("summary"),
            "entities": result.get("entities"),
            "sentiment": result.get("sentiment")
        }
    else:
        raise Exception(f"n8n processing failed: {response.text}")

# Usage
result = process_document_with_n8n(
    "https://example.com/document.pdf",
    "http://localhost:5678/webhook/document-processor"
)
```

## Best Practices

1. **Pre-processing**: Clean and structure input documents before AI processing
2. **Chunking**: Split large documents into manageable chunks
3. **Caching**: Cache processed results to avoid reprocessing
4. **Validation**: Validate AI-extracted information
5. **Error Handling**: Handle document parsing failures gracefully
6. **Rate Limiting**: Respect API limits when processing batches
7. **Monitoring**: Track processing success rates and quality
8. **Security**: Sanitize document content before processing

Document AI transforms how organizations process and understand their content. The next chapter explores building autonomous AI agents with tool access.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `content`, `json`, `nodes` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Document AI and Content Processing` as an operating subsystem inside **n8n AI Tutorial: Workflow Automation with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `name`, `parameters`, `role` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Document AI and Content Processing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `content`.
2. **Input normalization**: shape incoming data so `json` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `nodes`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/n8n-io/n8n)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `content` and `json` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: AI Nodes and LLM Integration](02-ai-nodes.md)
- [Next Chapter: Chapter 4: Building AI Agents with Tools](04-ai-agents.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
