---
layout: default
title: "Chapter 4: Document Loading & Processing"
parent: "LangChain Tutorial"
nav_order: 4
---

# Chapter 4: Document Loading & Processing

Welcome to the world of **Retrieval-Augmented Generation (RAG)**! So far, we've been working with language models that have knowledge up to their training cutoff. But what if you want your AI to answer questions about your specific documents, recent news, or proprietary data? That's where document processing comes in!

## What Problem Does Document Processing Solve?

Imagine you have:
- A collection of company documents
- Recent research papers
- Product documentation
- Personal notes and knowledge base

You want your AI to answer questions using this specific information, not just general knowledge. Document processing makes this possible by:

1. **Loading** documents from various sources
2. **Processing** them into manageable chunks
3. **Storing** them in a searchable format
4. **Retrieving** relevant information when needed

## Loading Documents

LangChain supports loading documents from many sources:

### 1. File System Documents

```python
from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader

# Load a text file
loader = TextLoader("data/my_document.txt")
documents = loader.load()

# Load a PDF
pdf_loader = PyPDFLoader("data/manual.pdf")
pdf_docs = pdf_loader.load()

# Load Word documents
docx_loader = Docx2txtLoader("data/guide.docx")
docx_docs = docx_loader.load()

print(f"Loaded {len(documents)} documents")
print(f"First document content preview: {documents[0].page_content[:200]}...")
```

### 2. Web Content

```python
from langchain.document_loaders import WebBaseLoader

# Load from a URL
web_loader = WebBaseLoader("https://example.com/documentation")
web_docs = web_loader.load()

# Load multiple URLs
urls = [
    "https://docs.langchain.com/getting-started",
    "https://python.langchain.com/docs/get_started/introduction"
]
web_loader = WebBaseLoader(urls)
docs = web_loader.load()
```

### 3. Directory Loading

```python
from langchain.document_loaders import DirectoryLoader

# Load all files from a directory
loader = DirectoryLoader(
    "data/",  # Directory path
    glob="**/*.txt",  # File pattern
    loader_cls=TextLoader  # Loader class to use
)
documents = loader.load()

print(f"Loaded {len(documents)} documents from directory")
```

## How Document Loading Works Under the Hood

When you load documents, LangChain:

1. **Reads the file** using appropriate parsers
2. **Extracts text content** from various formats (PDF, Word, HTML, etc.)
3. **Creates Document objects** with content and metadata
4. **Adds metadata** like source file, page numbers, etc.

```python
# Example of what a loaded document looks like
from langchain.schema import Document

doc = Document(
    page_content="This is the text content of the document...",
    metadata={
        "source": "data/manual.pdf",
        "page": 1,
        "title": "User Manual"
    }
)
```

## Text Splitting

Large documents need to be broken into smaller chunks for effective processing:

```python
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

# Basic character splitter
text_splitter = CharacterTextSplitter(
    separator="\n\n",  # Split on double newlines
    chunk_size=1000,  # Maximum characters per chunk
    chunk_overlap=200  # Overlap between chunks
)

# Split documents
split_docs = text_splitter.split_documents(documents)

print(f"Original documents: {len(documents)}")
print(f"Split chunks: {len(split_docs)}")
print(f"Average chunk size: {sum(len(doc.page_content) for doc in split_docs) / len(split_docs)}")
```

### Advanced Splitting Strategies

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Recursive splitter - tries different separators
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]  # Try these in order
)

# Markdown-aware splitter
from langchain.text_splitter import MarkdownTextSplitter

markdown_splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

## How Text Splitting Works Under the Hood

Text splitting is crucial for RAG because:

1. **Token Limits**: Language models have maximum context lengths
2. **Relevance**: Smaller chunks improve retrieval precision
3. **Overlap**: Ensures context isn't lost between chunks
4. **Performance**: Smaller chunks are faster to process

The recursive splitter works by:
1. Trying the first separator (paragraphs)
2. If chunks are too big, trying the next separator (sentences)
3. Continuing until all chunks meet the size requirements

## Document Processing Pipeline

Let's create a complete document processing pipeline:

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def process_documents(directory_path):
    """Complete document processing pipeline"""

    # 1. Load documents
    print("📁 Loading documents...")
    loader = DirectoryLoader(directory_path, glob="**/*.txt")
    raw_documents = loader.load()

    # 2. Clean and preprocess
    print("🧹 Cleaning documents...")
    cleaned_docs = []
    for doc in raw_documents:
        # Remove extra whitespace
        cleaned_content = " ".join(doc.page_content.split())
        cleaned_doc = Document(
            page_content=cleaned_content,
            metadata=doc.metadata
        )
        cleaned_docs.append(cleaned_doc)

    # 3. Split into chunks
    print("✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_documents = text_splitter.split_documents(cleaned_docs)

    # 4. Add processing metadata
    processed_docs = []
    for i, doc in enumerate(split_documents):
        doc.metadata.update({
            "chunk_id": i,
            "chunk_size": len(doc.page_content),
            "processed_at": new Date().toISOString()
        })
        processed_docs.append(doc)

    print(f"✅ Processed {len(processed_docs)} document chunks")
    return processed_docs

# Use the pipeline
documents = process_documents("data/")
```

## Advanced Document Processing

### 1. Custom Document Loaders

```python
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document

class CustomDatabaseLoader(BaseLoader):
    """Load documents from a custom database"""

    def __init__(self, connection_string, query):
        self.connection_string = connection_string
        self.query = query

    def load(self):
        # Connect to database and fetch documents
        # This is a simplified example
        documents = []

        # In real implementation, you'd connect to your database
        # and fetch records, then convert them to Document objects

        return documents
```

### 2. Document Transformers

```python
from langchain.document_transformers import BeautifulSoupTransformer

# Extract clean text from HTML
html_transformer = BeautifulSoupTransformer()
clean_docs = html_transformer.transform_documents(html_docs)
```

### 3. Metadata Enhancement

```python
def enhance_metadata(documents):
    """Add useful metadata to documents"""

    enhanced_docs = []
    for doc in documents:
        # Add word count
        word_count = len(doc.page_content.split())

        # Add reading time estimate
        reading_time = word_count / 200  # Average reading speed

        # Add content type detection
        content_type = detect_content_type(doc.page_content)

        enhanced_metadata = {
            **doc.metadata,
            "word_count": word_count,
            "reading_time_minutes": round(reading_time, 1),
            "content_type": content_type
        }

        enhanced_doc = Document(
            page_content=doc.page_content,
            metadata=enhanced_metadata
        )
        enhanced_docs.append(enhanced_doc)

    return enhanced_docs
```

## Document Quality Assessment

```python
def assess_document_quality(documents):
    """Assess the quality of loaded documents"""

    quality_metrics = []

    for doc in documents:
        content = doc.page_content
        metrics = {
            "chunk_size": len(content),
            "word_count": len(content.split()),
            "has_meaningful_content": len(content.strip()) > 50,
            "diversity_score": calculate_text_diversity(content),
            "language": detect_language(content)
        }
        quality_metrics.append(metrics)

    return quality_metrics

def calculate_text_diversity(text):
    """Calculate lexical diversity of text"""
    words = text.lower().split()
    unique_words = set(words)
    return len(unique_words) / len(words) if words else 0
```

## Best Practices for Document Processing

### 1. File Organization

```
data/
├── raw/           # Original files
├── processed/     # Cleaned documents
├── chunks/        # Split chunks
└── metadata/      # Processing metadata
```

### 2. Error Handling

```python
def load_documents_safely(directory_path):
    """Load documents with comprehensive error handling"""

    successful_loads = []
    failed_loads = []

    try:
        loader = DirectoryLoader(directory_path, glob="**/*.txt")
        documents = loader.load()
        successful_loads.extend(documents)

    except Exception as e:
        print(f"Error loading documents: {e}")
        failed_loads.append({"path": directory_path, "error": str(e)})

    return successful_loads, failed_loads
```

### 3. Performance Optimization

```python
from concurrent.futures import ThreadPoolExecutor

def process_documents_parallel(documents, num_workers=4):
    """Process documents in parallel"""

    def process_single_doc(doc):
        # Your document processing logic here
        return processed_doc

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        processed_docs = list(executor.map(process_single_doc, documents))

    return processed_docs
```

## Common Document Processing Patterns

### 1. Knowledge Base Processing

```python
def process_knowledge_base(kb_path):
    """Process a knowledge base with multiple document types"""

    # Load different types of documents
    text_loader = DirectoryLoader(kb_path, glob="**/*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader(kb_path, glob="**/*.pdf", loader_cls=PyPDFLoader)

    all_docs = []
    all_docs.extend(text_loader.load())
    all_docs.extend(pdf_loader.load())

    # Split and process
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)

    return chunks
```

### 2. Web Scraping Pipeline

```python
def scrape_and_process_website(url, max_pages=10):
    """Scrape website and process content"""

    from langchain.document_loaders import WebBaseLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    # Load website content
    loader = WebBaseLoader(url)
    documents = loader.load()

    # Split into manageable chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # Add website metadata
    for chunk in chunks:
        chunk.metadata.update({
            "source_type": "web",
            "url": url,
            "scraped_at": new Date().toISOString()
        })

    return chunks
```

## What We've Learned

Fantastic progress! 🎉 You've now mastered:

1. **Document Loading** - Loading from files, web, and directories
2. **Text Splitting** - Breaking large documents into manageable chunks
3. **Document Processing Pipelines** - Complete workflows for document handling
4. **Metadata Enhancement** - Adding useful information to documents
5. **Quality Assessment** - Evaluating document processing effectiveness
6. **Best Practices** - Error handling and performance optimization

## Next Steps

Now that you can load and process documents, let's learn how to store them for efficient retrieval. In [Chapter 5: Vector Stores & Retrieval](05-vector-stores.md), we'll explore how to make your documents searchable using embeddings and vector databases.

---

**Try this exercise:**
Create a document processing pipeline that:
1. Loads documents from a directory
2. Splits them into chunks
3. Adds metadata about word count and reading time
4. Filters out low-quality chunks
5. Saves the processed chunks for later use

*What types of documents do you want to make searchable with AI?* 📚

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `documents`, `langchain`, `load` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Document Loading & Processing` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `metadata`, `chunks`, `Load` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Document Loading & Processing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `documents`.
2. **Input normalization**: shape incoming data so `langchain` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `load`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `documents` and `langchain` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Memory Systems](03-memory-systems.md)
- [Next Chapter: Chapter 5: Vector Stores & Retrieval](05-vector-stores.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
