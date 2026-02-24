---
layout: default
title: "Chapter 2: Document Processing"
parent: "RAGFlow Tutorial"
nav_order: 2
---

# Chapter 2: Document Processing

Welcome to **Chapter 2: Document Processing**. In this part of **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explores RAGFlow's powerful document processing capabilities. You'll learn how to upload, parse, and optimize documents from various formats for maximum retrieval performance.

## 🎯 What You'll Learn

- Document upload methods and formats
- Advanced parsing techniques
- Chunking strategies for optimal retrieval
- Document preprocessing and cleaning
- Handling complex document structures

## 📁 Supported Document Formats

RAGFlow supports 100+ document formats out of the box:

### Text-Based Documents
```python
# Plain text files
text_formats = [
    '.txt', '.md', '.json', '.xml', '.csv',
    '.log', '.ini', '.cfg', '.yml', '.yaml'
]

# Office documents
office_formats = [
    '.docx', '.doc', '.xlsx', '.xls',
    '.pptx', '.ppt', '.pdf'
]

# Web content
web_formats = ['.html', '.htm']

# Code files
code_formats = [
    '.py', '.js', '.java', '.cpp', '.c', '.h',
    '.php', '.rb', '.go', '.rs', '.ts', '.tsx'
]
```

## 📤 Document Upload Methods

### Web Interface Upload

```python
# Using RAGFlow's web interface
import requests
from pathlib import Path

class DocumentUploader:
    def __init__(self, base_url="http://localhost:80", api_key=None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def upload_file(self, file_path, kb_id, parser_config=None):
        """Upload a single file"""
        file_path = Path(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, self._get_mime_type(file_path))}

            data = {
                'kb_id': kb_id,
                'parser_config': json.dumps(parser_config or {})
            }

            response = requests.post(
                f"{self.base_url}/api/v1/documents/upload",
                files=files,
                data=data,
                headers=self.headers
            )

        return response.json()

    def upload_directory(self, dir_path, kb_id, recursive=True):
        """Upload all files in a directory"""
        dir_path = Path(dir_path)
        results = []

        pattern = '**/*' if recursive else '*'

        for file_path in dir_path.glob(pattern):
            if file_path.is_file() and self._is_supported_format(file_path):
                result = self.upload_file(str(file_path), kb_id)
                results.append(result)

        return results

    def _get_mime_type(self, file_path):
        """Get MIME type for file"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'

    def _is_supported_format(self, file_path):
        """Check if file format is supported"""
        supported_extensions = {
            '.txt', '.md', '.pdf', '.docx', '.xlsx', '.pptx',
            '.html', '.json', '.xml', '.py', '.js', '.java'
        }
        return file_path.suffix.lower() in supported_extensions
```

### Batch Upload with Progress Tracking

```python
import asyncio
import aiohttp
from tqdm import tqdm
import json

class BatchUploader:
    def __init__(self, base_url="http://localhost:80", api_key=None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async def upload_batch(self, file_paths, kb_id):
        """Upload multiple files concurrently"""
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = []

            for file_path in file_paths:
                task = self._upload_single_file(session, file_path, kb_id)
                tasks.append(task)

            # Use tqdm for progress tracking
            results = []
            with tqdm(total=len(tasks), desc="Uploading files") as pbar:
                for coro in asyncio.as_completed(tasks):
                    result = await coro
                    results.append(result)
                    pbar.update(1)

            return results

    async def _upload_single_file(self, session, file_path, kb_id):
        """Upload a single file asynchronously"""
        with open(file_path, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('file', f, filename=Path(file_path).name)
            data.add_field('kb_id', str(kb_id))

            async with session.post(
                f"{self.base_url}/api/v1/documents/upload",
                data=data
            ) as response:
                return await response.json()
```

## 🔍 Advanced Parsing Techniques

### PDF Document Parsing

```python
class PDFParser:
    def __init__(self):
        try:
            import PyPDF2
            self.pdf_parser = PyPDF2
        except ImportError:
            print("PyPDF2 not installed. Install with: pip install PyPDF2")

    def parse_pdf(self, file_path, extract_metadata=True):
        """Parse PDF with advanced options"""
        with open(file_path, 'rb') as file:
            pdf_reader = self.pdf_parser.PdfReader(file)

            # Extract metadata
            metadata = {}
            if extract_metadata and pdf_reader.metadata:
                metadata = {
                    'title': pdf_reader.metadata.get('/Title', ''),
                    'author': pdf_reader.metadata.get('/Author', ''),
                    'subject': pdf_reader.metadata.get('/Subject', ''),
                    'creator': pdf_reader.metadata.get('/Creator', ''),
                    'producer': pdf_reader.metadata.get('/Producer', ''),
                    'creation_date': pdf_reader.metadata.get('/CreationDate', '')
                }

            # Extract text from all pages
            text_content = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"

            return {
                'content': text_content,
                'metadata': metadata,
                'page_count': len(pdf_reader.pages),
                'file_size': Path(file_path).stat().st_size
            }
```

### Office Document Parsing

```python
class OfficeParser:
    def __init__(self):
        try:
            import docx
            import openpyxl
            import pptx
            self.docx = docx
            self.xlsx = openpyxl
            self.pptx = pptx
        except ImportError:
            print("Install office libraries: pip install python-docx openpyxl python-pptx")

    def parse_docx(self, file_path):
        """Parse Word documents"""
        doc = self.docx.Document(file_path)

        content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)

        # Extract tables
        tables = []
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)
            tables.append(table_data)

        return {
            'content': '\n'.join(content),
            'tables': tables,
            'paragraph_count': len(content)
        }

    def parse_xlsx(self, file_path):
        """Parse Excel spreadsheets"""
        wb = self.xlsx.load_workbook(file_path, data_only=True)

        sheets_data = {}
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            sheet_data = []

            for row in sheet.iter_rows(values_only=True):
                # Filter out None values
                clean_row = [str(cell) if cell is not None else '' for cell in row]
                if any(clean_row):  # Only add non-empty rows
                    sheet_data.append(clean_row)

            sheets_data[sheet_name] = sheet_data

        return {
            'sheets': sheets_data,
            'sheet_count': len(wb.sheetnames)
        }
```

## ✂️ Chunking Strategies

### Intelligent Text Chunking

```python
import re
from typing import List, Dict, Any
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

class AdvancedChunker:
    def __init__(self):
        # Download NLTK data if needed
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

    def semantic_chunking(self, text: str, max_chunk_size: int = 512) -> List[str]:
        """Chunk text based on semantic similarity"""
        # Split into sentences
        sentences = nltk.sent_tokenize(text)

        chunks = []
        current_chunk = ""
        current_embeddings = []

        for sentence in sentences:
            # Calculate embedding for sentence
            sentence_embedding = self._get_sentence_embedding(sentence)

            # Check if adding sentence would exceed chunk size
            if len(current_chunk + sentence) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
                current_embeddings = [sentence_embedding]
            else:
                # Check semantic similarity
                if current_embeddings:
                    similarity = self._calculate_similarity(
                        sentence_embedding, current_embeddings[-1]
                    )

                    # If similarity is low, start new chunk
                    if similarity < 0.3:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                        current_embeddings = [sentence_embedding]
                    else:
                        current_chunk += " " + sentence
                        current_embeddings.append(sentence_embedding)
                else:
                    current_chunk = sentence
                    current_embeddings = [sentence_embedding]

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def hierarchical_chunking(self, text: str) -> Dict[str, List[str]]:
        """Create hierarchical chunks (document -> sections -> paragraphs)"""
        # Split by sections (assuming markdown-style headers)
        sections = re.split(r'(?=^#{1,6}\s)', text, flags=re.MULTILINE)

        hierarchical_chunks = {
            'document': [text],
            'sections': [],
            'paragraphs': []
        }

        for section in sections:
            if section.strip():
                hierarchical_chunks['sections'].append(section.strip())

                # Split into paragraphs
                paragraphs = re.split(r'\n\s*\n', section)
                hierarchical_chunks['paragraphs'].extend(
                    [p.strip() for p in paragraphs if p.strip()]
                )

        return hierarchical_chunks

    def _get_sentence_embedding(self, sentence: str) -> List[float]:
        """Get embedding for a sentence (simplified version)"""
        # In practice, use a proper embedding model
        words = sentence.lower().split()
        return [hash(word) % 1000 / 1000.0 for word in words[:10]]

    def _calculate_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        import numpy as np
        vec1 = np.array(emb1)
        vec2 = np.array(emb2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
```

### Optimal Chunk Size Selection

```python
class ChunkOptimizer:
    def __init__(self):
        self.chunk_sizes = [256, 512, 1024, 2048]

    def find_optimal_chunk_size(self, text: str, target_chunks: int = 10) -> int:
        """Find optimal chunk size for given text"""
        text_length = len(text)

        # Calculate optimal size based on target number of chunks
        optimal_size = text_length // target_chunks

        # Find closest standard size
        return min(self.chunk_sizes, key=lambda x: abs(x - optimal_size))

    def adaptive_chunking(self, text: str) -> List[str]:
        """Adaptively chunk text based on content"""
        # Analyze text structure
        sentences = nltk.sent_tokenize(text)
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)

        # Adjust chunk size based on sentence length
        if avg_sentence_length < 50:  # Short sentences
            chunk_size = 256
        elif avg_sentence_length < 100:  # Medium sentences
            chunk_size = 512
        else:  # Long sentences
            chunk_size = 1024

        # Apply chunking
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk + sentence) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
```

## 🧹 Document Preprocessing

### Text Cleaning and Normalization

```python
import re
import unicodedata
from typing import List, Set

class TextPreprocessor:
    def __init__(self):
        # Common stopwords (can be expanded)
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been'
        }

    def clean_text(self, text: str) -> str:
        """Comprehensive text cleaning"""
        # Convert to lowercase
        text = text.lower()

        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep sentence structure
        text = re.sub(r'[^\w\s.,!?-]', '', text)

        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?])', r'\1', text)

        return text.strip()

    def remove_noise(self, text: str) -> str:
        """Remove noisy elements from text"""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters"""
        # Convert to NFKC form (compatibility decomposition followed by canonical composition)
        text = unicodedata.normalize('NFKC', text)

        # Replace common unicode characters
        replacements = {
            ''': "'",
            ''': "'",
            '"': '"',
            '"': '"',
            '…': '...',
            '–': '-',
            '—': '-',
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract important keywords from text"""
        words = re.findall(r'\b\w+\b', text.lower())

        # Remove stopwords
        words = [word for word in words if word not in self.stopwords and len(word) > 2]

        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
```

### Document Structure Analysis

```python
class DocumentAnalyzer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze document structure and characteristics"""
        # Basic statistics
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)

        analysis = {
            'total_characters': len(text),
            'total_words': len(words),
            'total_sentences': len(sentences),
            'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
        }

        # Readability metrics
        analysis.update(self._calculate_readability(text))

        # Language detection
        analysis['language'] = self._detect_language(text)

        # Content type classification
        analysis['content_type'] = self._classify_content_type(text)

        return analysis

    def _calculate_readability(self, text: str) -> Dict[str, float]:
        """Calculate readability scores"""
        sentences = nltk.sent_tokenize(text)
        words = nltk.word_tokenize(text)

        if not sentences or not words:
            return {'flesch_score': 0, 'readability_level': 'unknown'}

        # Simplified Flesch Reading Ease Score
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)

        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length)

        # Determine readability level
        if flesch_score >= 90:
            level = '5th grade'
        elif flesch_score >= 80:
            level = '6th grade'
        elif flesch_score >= 70:
            level = '7th grade'
        elif flesch_score >= 60:
            level = '8th-9th grade'
        elif flesch_score >= 50:
            level = '10th-12th grade'
        elif flesch_score >= 30:
            level = 'college'
        else:
            level = 'college graduate'

        return {
            'flesch_score': flesch_score,
            'readability_level': level
        }

    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        # This is a simplified version - use langdetect library for production
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to']
        text_lower = text.lower()

        english_count = sum(1 for word in english_words if word in text_lower)

        return 'english' if english_count >= 3 else 'unknown'

    def _classify_content_type(self, text: str) -> str:
        """Classify document content type"""
        text_lower = text.lower()

        # Technical content indicators
        tech_indicators = ['api', 'function', 'class', 'method', 'algorithm', 'database']
        tech_score = sum(1 for indicator in tech_indicators if indicator in text_lower)

        # Business content indicators
        business_indicators = ['revenue', 'profit', 'market', 'strategy', 'customer', 'sales']
        business_score = sum(1 for indicator in business_indicators if indicator in text_lower)

        # Academic content indicators
        academic_indicators = ['research', 'study', 'analysis', 'theory', 'methodology']
        academic_score = sum(1 for indicator in academic_indicators if indicator in text_lower)

        # Determine content type
        max_score = max(tech_score, business_score, academic_score)

        if max_score == 0:
            return 'general'
        elif tech_score == max_score:
            return 'technical'
        elif business_score == max_score:
            return 'business'
        else:
            return 'academic'
```

## 📊 Processing Pipeline

### Complete Document Processing Workflow

```python
class DocumentProcessingPipeline:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.chunker = AdvancedChunker()
        self.analyzer = DocumentAnalyzer()

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Complete document processing pipeline"""
        # Step 1: Extract text content
        content = self._extract_content(file_path)

        # Step 2: Preprocess text
        cleaned_content = self.preprocessor.clean_text(content)
        cleaned_content = self.preprocessor.remove_noise(cleaned_content)
        cleaned_content = self.preprocessor.normalize_unicode(cleaned_content)

        # Step 3: Analyze document
        analysis = self.analyzer.analyze_structure(cleaned_content)

        # Step 4: Extract keywords
        keywords = self.preprocessor.extract_keywords(cleaned_content)

        # Step 5: Create chunks
        chunks = self.chunker.semantic_chunking(cleaned_content)

        # Step 6: Generate metadata
        metadata = {
            'file_path': file_path,
            'file_size': Path(file_path).stat().st_size,
            'processing_timestamp': datetime.now().isoformat(),
            'chunk_count': len(chunks),
            'keywords': keywords
        }

        return {
            'content': cleaned_content,
            'chunks': chunks,
            'analysis': analysis,
            'metadata': metadata
        }

    def _extract_content(self, file_path: str) -> str:
        """Extract text content from various file formats"""
        file_ext = Path(file_path).suffix.lower()

        if file_ext == '.pdf':
            parser = PDFParser()
            return parser.parse_pdf(file_path)['content']
        elif file_ext == '.docx':
            parser = OfficeParser()
            return parser.parse_docx(file_path)['content']
        elif file_ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
```

## 🎯 Best Practices

### Document Processing Guidelines

1. **File Format Selection**
   - Use text-based formats when possible (.txt, .md)
   - Ensure PDFs have extractable text (not scanned images)
   - Convert office documents to PDF before processing

2. **Chunk Size Optimization**
   - Smaller chunks (256-512) for precise retrieval
   - Larger chunks (1024-2048) for context preservation
   - Test different sizes for your specific use case

3. **Preprocessing Strategy**
   - Remove noise while preserving meaning
   - Normalize text encoding
   - Handle special characters appropriately

4. **Quality Assurance**
   - Validate extracted content
   - Check chunk quality and coherence
   - Monitor processing success rates

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've mastered:

- ✅ Multiple document upload methods
- ✅ Advanced parsing for various formats
- ✅ Intelligent chunking strategies
- ✅ Text preprocessing and cleaning
- ✅ Document structure analysis
- ✅ Complete processing pipeline

## 🚀 What's Next?

Ready to configure your knowledge bases? Let's explore [Chapter 3: Knowledge Base Setup](03-knowledge-base-setup.md) to learn about creating and managing knowledge bases effectively.

---

**Practice what you've learned:**
1. Upload documents of different formats to RAGFlow
2. Experiment with various chunking strategies
3. Analyze document structures and readability
4. Build a complete document processing pipeline
5. Optimize chunk sizes for your use case

*What's the most challenging document type you've processed?* 📄

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `text`, `file_path` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Document Processing` as an operating subsystem inside **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `current_chunk`, `sentence` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Document Processing` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `file_path`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/infiniflow/ragflow)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with RAGFlow](01-getting-started.md)
- [Next Chapter: Chapter 3: Knowledge Base Setup](03-knowledge-base-setup.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
