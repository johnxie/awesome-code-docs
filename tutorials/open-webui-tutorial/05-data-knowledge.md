---
layout: default
title: "Open WebUI Tutorial - Chapter 5: Data & Knowledge Management"
nav_order: 5
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 5: Data, Knowledge Bases & RAG Implementation

> Build intelligent knowledge systems with document ingestion, vector search, and Retrieval-Augmented Generation.

## Document Ingestion Pipeline

### File Upload & Processing

```python
from typing import List, Dict, Any
import os
from pathlib import Path
import tempfile
from dataclasses import dataclass
from enum import Enum

class DocumentType(Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    HTML = "html"
    CSV = "csv"
    JSON = "json"
    IMAGE = "image"

@dataclass
class Document:
    id: str
    name: str
    type: DocumentType
    content: str
    metadata: Dict[str, Any]
    chunks: List[str] = None
    embeddings: List[List[float]] = None

class DocumentProcessor:
    def __init__(self):
        self.processors = {
            DocumentType.PDF: self._process_pdf,
            DocumentType.DOCX: self._process_docx,
            DocumentType.TXT: self._process_text,
            DocumentType.MD: self._process_markdown,
            DocumentType.HTML: self._process_html,
            DocumentType.CSV: self._process_csv,
            DocumentType.JSON: self._process_json,
        }

    async def process_file(self, file_path: str, file_type: DocumentType) -> Document:
        """Process a file and extract its content."""

        # Read file content
        content = await self._read_file(file_path)

        # Extract metadata
        metadata = await self._extract_metadata(file_path, file_type)

        # Create document object
        doc_id = f"doc_{hash(file_path)}_{int(time.time())}"
        document = Document(
            id=doc_id,
            name=Path(file_path).name,
            type=file_type,
            content=content,
            metadata=metadata
        )

        # Process with specific handler
        processor = self.processors.get(file_type, self._process_text)
        processed_doc = await processor(document)

        return processed_doc

    async def _read_file(self, file_path: str) -> str:
        """Read file content with proper encoding detection."""
        try:
            # Try UTF-8 first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback to latin-1 for binary files that might be text
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    async def _extract_metadata(self, file_path: str, file_type: DocumentType) -> Dict[str, Any]:
        """Extract metadata from file."""
        stat = os.stat(file_path)

        metadata = {
            "file_path": file_path,
            "file_size": stat.st_size,
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
            "file_type": file_type.value
        }

        # Add type-specific metadata
        if file_type == DocumentType.PDF:
            metadata.update(await self._extract_pdf_metadata(file_path))
        elif file_type in [DocumentType.DOCX, DocumentType.DOC]:
            metadata.update(await self._extract_docx_metadata(file_path))

        return metadata

    async def _process_pdf(self, document: Document) -> Document:
        """Process PDF files."""
        try:
            import PyPDF2

            with open(document.metadata["file_path"], 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""

                # Extract text from all pages
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

                # Update metadata with page count
                document.metadata["page_count"] = len(pdf_reader.pages)
                document.content = text

        except ImportError:
            # Fallback if PyPDF2 not available
            document.content = "PDF processing requires PyPDF2 library"

        return document

    async def _process_docx(self, document: Document) -> Document:
        """Process Word documents."""
        try:
            from docx import Document as DocxDocument

            doc = DocxDocument(document.metadata["file_path"])
            text = ""

            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            document.content = text
            document.metadata["word_count"] = len(text.split())

        except ImportError:
            document.content = "DOCX processing requires python-docx library"

        return document

    async def _process_text(self, document: Document) -> Document:
        """Process plain text files."""
        # Content already read, just clean it up
        document.content = document.content.strip()
        document.metadata["line_count"] = len(document.content.split('\n'))
        document.metadata["word_count"] = len(document.content.split())

        return document

    async def _process_markdown(self, document: Document) -> Document:
        """Process Markdown files."""
        import re

        # Extract headers for table of contents
        headers = re.findall(r'^(#{1,6})\s+(.+)$', document.content, re.MULTILINE)
        document.metadata["headers"] = [{"level": len(h[0]), "text": h[1]} for h in headers]

        # Count code blocks
        code_blocks = len(re.findall(r'```', document.content))
        document.metadata["code_blocks"] = code_blocks

        return document

    async def _process_html(self, document: Document) -> Document:
        """Process HTML files."""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(document.content, 'html.parser')

            # Extract title
            title = soup.title.string if soup.title else "Untitled"
            document.metadata["title"] = title

            # Extract text content
            text = soup.get_text(separator='\n', strip=True)
            document.content = text

            # Extract links
            links = [a['href'] for a in soup.find_all('a', href=True)]
            document.metadata["links"] = links[:10]  # Limit to first 10

        except ImportError:
            # Remove HTML tags as fallback
            import re
            document.content = re.sub(r'<[^>]+>', '', document.content)

        return document

    async def _process_csv(self, document: Document) -> Document:
        """Process CSV files."""
        try:
            import csv
            import io

            # Read CSV content
            csv_reader = csv.DictReader(io.StringIO(document.content))
            rows = list(csv_reader)

            document.metadata["row_count"] = len(rows)
            document.metadata["columns"] = list(rows[0].keys()) if rows else []

            # Convert to structured text
            text_parts = [f"Columns: {', '.join(document.metadata['columns'])}"]
            text_parts.extend([f"Row {i+1}: {dict(row)}" for i, row in enumerate(rows[:5])])
            if len(rows) > 5:
                text_parts.append(f"... and {len(rows) - 5} more rows")

            document.content = "\n".join(text_parts)

        except Exception as e:
            document.content = f"CSV processing failed: {e}"

        return document

    async def _process_json(self, document: Document) -> Document:
        """Process JSON files."""
        try:
            import json

            data = json.loads(document.content)
            document.metadata["json_type"] = type(data).__name__

            if isinstance(data, dict):
                document.metadata["keys"] = list(data.keys())
            elif isinstance(data, list):
                document.metadata["item_count"] = len(data)
                if data and isinstance(data[0], dict):
                    document.metadata["item_keys"] = list(data[0].keys())

            # Pretty print for content
            document.content = json.dumps(data, indent=2)

        except json.JSONDecodeError:
            document.content = "Invalid JSON content"

        return document
```

### Text Chunking Strategies

```python
from typing import List, Dict, Any
import re
from dataclasses import dataclass

@dataclass
class TextChunk:
    text: str
    metadata: Dict[str, Any]
    start_pos: int
    end_pos: int

class TextChunker:
    def __init__(self):
        self.strategies = {
            "fixed_size": self._chunk_fixed_size,
            "sentence": self._chunk_by_sentence,
            "paragraph": self._chunk_by_paragraph,
            "semantic": self._chunk_semantic,
            "markdown": self._chunk_markdown
        }

    def chunk_text(self, text: str, strategy: str = "fixed_size",
                   chunk_size: int = 1000, overlap: int = 200) -> List[TextChunk]:
        """Chunk text using specified strategy."""

        if strategy not in self.strategies:
            raise ValueError(f"Unknown chunking strategy: {strategy}")

        chunker = self.strategies[strategy]
        return chunker(text, chunk_size, overlap)

    def _chunk_fixed_size(self, text: str, chunk_size: int, overlap: int) -> List[TextChunk]:
        """Fixed-size chunking with overlap."""
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Find word boundary if possible
            if end < len(text):
                # Look for last space within last 100 characters
                last_space = text.rfind(' ', end - 100, end)
                if last_space > start:
                    end = last_space

            chunk_text = text[start:end].strip()
            if chunk_text:  # Only add non-empty chunks
                chunks.append(TextChunk(
                    text=chunk_text,
                    metadata={"chunk_type": "fixed_size", "chunk_size": len(chunk_text)},
                    start_pos=start,
                    end_pos=end
                ))

            # Move start position with overlap
            start = end - overlap if overlap > 0 else end

        return chunks

    def _chunk_by_sentence(self, text: str, max_sentences: int = 5, overlap: int = 1) -> List[TextChunk]:
        """Chunk by sentences."""
        # Split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        chunks = []
        i = 0

        while i < len(sentences):
            chunk_sentences = sentences[i:i + max_sentences]
            chunk_text = ' '.join(chunk_sentences)

            if chunk_text.strip():
                chunks.append(TextChunk(
                    text=chunk_text,
                    metadata={
                        "chunk_type": "sentence",
                        "sentence_count": len(chunk_sentences)
                    },
                    start_pos=text.find(chunk_sentences[0]),
                    end_pos=text.find(chunk_sentences[-1]) + len(chunk_sentences[-1])
                ))

            # Move with overlap
            i += max_sentences - overlap

        return chunks

    def _chunk_by_paragraph(self, text: str, max_paragraphs: int = 3, overlap: int = 1) -> List[TextChunk]:
        """Chunk by paragraphs."""
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', text.strip())

        chunks = []
        i = 0

        while i < len(paragraphs):
            chunk_paragraphs = paragraphs[i:i + max_paragraphs]
            chunk_text = '\n\n'.join(chunk_paragraphs)

            if chunk_text.strip():
                chunks.append(TextChunk(
                    text=chunk_text,
                    metadata={
                        "chunk_type": "paragraph",
                        "paragraph_count": len(chunk_paragraphs)
                    },
                    start_pos=text.find(chunk_paragraphs[0]),
                    end_pos=text.find(chunk_paragraphs[-1]) + len(chunk_paragraphs[-1])
                ))

            # Move with overlap
            i += max_paragraphs - overlap

        return chunks

    def _chunk_markdown(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[TextChunk]:
        """Markdown-aware chunking."""
        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line)

            # Check if line starts a new section
            if re.match(r'^#{1,6}\s', line):  # Header
                # Save current chunk if it exists
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append(TextChunk(
                        text=chunk_text,
                        metadata={"chunk_type": "markdown_section"},
                        start_pos=0,  # Would need to calculate properly
                        end_pos=len(chunk_text)
                    ))

                # Start new chunk with header
                current_chunk = [line]
                current_size = line_size

            elif current_size + line_size > chunk_size:
                # Save current chunk
                if current_chunk:
                    chunk_text = '\n'.join(current_chunk)
                    chunks.append(TextChunk(
                        text=chunk_text,
                        metadata={"chunk_type": "markdown_block"},
                        start_pos=0,
                        end_pos=len(chunk_text)
                    ))

                # Start new chunk with overlap
                overlap_lines = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
                current_chunk = overlap_lines + [line]
                current_size = sum(len(l) for l in current_chunk)

            else:
                current_chunk.append(line)
                current_size += line_size

        # Add final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append(TextChunk(
                text=chunk_text,
                metadata={"chunk_type": "markdown_block"},
                start_pos=0,
                end_pos=len(chunk_text)
            ))

        return chunks

    def _chunk_semantic(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[TextChunk]:
        """Semantic chunking using embeddings similarity."""
        # This is a simplified version - in practice you'd use embeddings
        # to find semantic boundaries

        # For now, fall back to sentence chunking
        return self._chunk_by_sentence(text, max_sentences=10, overlap=2)
```

## Vector Database Integration

### Embedding Generation

```python
from typing import List, Dict, Any
import numpy as np
from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        pass

    @abstractmethod
    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        pass

class OpenAIEmbeddings(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/embeddings"

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        import aiohttp

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": texts,
                    "model": self.model
                }
            )

            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"OpenAI API error: {response.status} - {error_text}")

            result = await response.json()
            return [item["embedding"] for item in result["data"]]

    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]

class LocalEmbeddings(EmbeddingProvider):
    def __init__(self, model_path: str = None):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_path or 'all-MiniLM-L6-v2')
        except ImportError:
            raise ImportError("sentence-transformers required for local embeddings")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using local model."""
        import asyncio

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            self.model.encode,
            texts
        )

        # Convert to list of lists
        return [embedding.tolist() for embedding in embeddings]

    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate single embedding."""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]

class EmbeddingManager:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider
        self.cache = {}  # Simple in-memory cache

    async def get_embeddings(self, texts: List[str], use_cache: bool = True) -> List[List[float]]:
        """Get embeddings with optional caching."""
        if not use_cache:
            return await self.provider.generate_embeddings(texts)

        # Check cache
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            cache_key = hash(text)
            if cache_key in self.cache:
                continue
            uncached_texts.append(text)
            uncached_indices.append(i)

        # Generate embeddings for uncached texts
        if uncached_texts:
            embeddings = await self.provider.generate_embeddings(uncached_texts)

            # Cache results
            for text, embedding in zip(uncached_texts, embeddings):
                self.cache[hash(text)] = embedding

        # Build final result
        result = [None] * len(texts)
        for i, text in enumerate(texts):
            result[i] = self.cache[hash(text)]

        return result

    def clear_cache(self):
        """Clear embedding cache."""
        self.cache.clear()
```

### Vector Database Setup

```python
from typing import List, Dict, Any, Optional
import json
import asyncio
from abc import ABC, abstractmethod

class VectorDatabase(ABC):
    @abstractmethod
    async def store_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]], ids: List[str]):
        """Store vectors with metadata."""
        pass

    @abstractmethod
    async def search_vectors(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        pass

    @abstractmethod
    async def delete_vectors(self, ids: List[str]):
        """Delete vectors by IDs."""
        pass

class QdrantVectorDB(VectorDatabase):
    def __init__(self, url: str = "http://localhost:6333", collection_name: str = "documents"):
        from qdrant_client import QdrantClient, models

        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

        # Create collection if it doesn't exist
        try:
            self.client.get_collection(collection_name)
        except:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Adjust based on your embedding model
                    distance=models.Distance.COSINE
                )
            )

    async def store_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]], ids: List[str]):
        """Store vectors in Qdrant."""
        from qdrant_client import models

        points = [
            models.PointStruct(
                id=doc_id,
                vector=vector,
                payload=meta
            )
            for doc_id, vector, meta in zip(ids, vectors, metadata)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    async def search_vectors(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search vectors in Qdrant."""
        from qdrant_client import models

        search_filters = None
        if filters:
            # Convert filters to Qdrant format
            conditions = []
            for key, value in filters.items():
                if isinstance(value, str):
                    conditions.append(models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    ))
                elif isinstance(value, (int, float)):
                    conditions.append(models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    ))

            if conditions:
                search_filters = models.Filter(
                    must=conditions
                )

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=search_filters
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "metadata": hit.payload
            }
            for hit in results
        ]

    async def delete_vectors(self, ids: List[str]):
        """Delete vectors from Qdrant."""
        from qdrant_client import models

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=ids
            )
        )

class ChromaVectorDB(VectorDatabase):
    def __init__(self, persist_directory: str = "./chroma_db"):
        import chromadb

        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="documents")

    async def store_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]], ids: List[str]):
        """Store vectors in Chroma."""
        # Convert metadata to strings for Chroma
        string_metadata = []
        for meta in metadata:
            string_meta = {}
            for key, value in meta.items():
                if isinstance(value, (dict, list)):
                    string_meta[key] = json.dumps(value)
                else:
                    string_meta[key] = str(value)
            string_metadata.append(string_meta)

        self.collection.add(
            embeddings=vectors,
            metadatas=string_metadata,
            ids=ids
        )

    async def search_vectors(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search vectors in Chroma."""
        where_clause = None
        if filters:
            where_clause = {}
            for key, value in filters.items():
                where_clause[key] = str(value)

        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=limit,
            where=where_clause
        )

        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append({
                "id": results['ids'][0][i],
                "score": 1.0 - results['distances'][0][i] if results['distances'][0][i] else 0.5,
                "metadata": results['metadatas'][0][i]
            })

        return search_results

    async def delete_vectors(self, ids: List[str]):
        """Delete vectors from Chroma."""
        self.collection.delete(ids=ids)

class PineconeVectorDB(VectorDatabase):
    def __init__(self, api_key: str, environment: str, index_name: str = "documents"):
        import pinecone

        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
        self.index_name = index_name

    async def store_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]], ids: List[str]):
        """Store vectors in Pinecone."""
        # Prepare data for Pinecone
        vector_data = []
        for vector, meta, doc_id in zip(vectors, metadata, ids):
            # Flatten metadata for Pinecone
            flat_meta = {}
            for key, value in meta.items():
                if isinstance(value, (dict, list)):
                    flat_meta[key] = json.dumps(value)
                else:
                    flat_meta[key] = value

            vector_data.append({
                "id": doc_id,
                "values": vector,
                "metadata": flat_meta
            })

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(vector_data), batch_size):
            batch = vector_data[i:i + batch_size]
            self.index.upsert(vectors=batch)

    async def search_vectors(self, query_vector: List[float], limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search vectors in Pinecone."""
        filter_clause = None
        if filters:
            filter_clause = {}
            for key, value in filters.items():
                filter_clause[key] = {"$eq": value}

        results = self.index.query(
            vector=query_vector,
            top_k=limit,
            filter=filter_clause,
            include_metadata=True
        )

        return [
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata
            }
            for match in results.matches
        ]

    async def delete_vectors(self, ids: List[str]):
        """Delete vectors from Pinecone."""
        self.index.delete(ids=ids)
```

## RAG Implementation

### Retrieval-Augmented Generation Pipeline

```python
from typing import List, Dict, Any, Tuple
import asyncio

class RAGPipeline:
    def __init__(self, vector_db: VectorDatabase, embedding_manager: EmbeddingManager):
        self.vector_db = vector_db
        self.embedding_manager = embedding_manager
        self.llm_client = None  # Will be set based on configuration

    def set_llm_client(self, client):
        """Set the LLM client for generation."""
        self.llm_client = client

    async def add_documents(self, documents: List[Document]):
        """Add documents to the knowledge base."""
        all_chunks = []
        all_metadata = []
        all_ids = []

        # Process each document
        for doc in documents:
            if not doc.chunks:
                # Chunk the document if not already chunked
                chunker = TextChunker()
                doc.chunks = chunker.chunk_text(doc.content)

            # Generate embeddings for chunks
            if doc.chunks:
                chunk_texts = [chunk.text for chunk in doc.chunks]
                embeddings = await self.embedding_manager.get_embeddings(chunk_texts)

                # Prepare data for storage
                for i, (chunk, embedding) in enumerate(zip(doc.chunks, embeddings)):
                    chunk_metadata = {
                        **doc.metadata,
                        "chunk_index": i,
                        "chunk_start": chunk.start_pos,
                        "chunk_end": chunk.end_pos,
                        "chunk_type": chunk.metadata.get("chunk_type", "unknown"),
                        "document_id": doc.id,
                        "document_name": doc.name
                    }

                    all_chunks.append(embedding)
                    all_metadata.append(chunk_metadata)
                    all_ids.append(f"{doc.id}_chunk_{i}")

        # Store in vector database
        if all_chunks:
            await self.vector_db.store_vectors(all_chunks, all_metadata, all_ids)

    async def retrieve_context(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant context for a query."""
        # Generate embedding for query
        query_embedding = await self.embedding_manager.get_embeddings([query])
        query_embedding = query_embedding[0]

        # Search vector database
        results = await self.vector_db.search_vectors(
            query_vector=query_embedding,
            limit=top_k,
            filters=filters
        )

        return results

    async def generate_answer(self, query: str, context_docs: List[Dict[str, Any]] = None,
                            system_prompt: str = None) -> Dict[str, Any]:
        """Generate an answer using retrieved context."""

        if context_docs is None:
            context_docs = await self.retrieve_context(query)

        # Prepare context
        context_text = self._format_context(context_docs)

        # Create prompt
        if system_prompt is None:
            system_prompt = """You are a helpful assistant that answers questions based on the provided context.
If you cannot find the answer in the context, say so clearly.
Always cite your sources when possible."""

        full_prompt = f"{system_prompt}\n\nContext:\n{context_text}\n\nQuestion: {query}\n\nAnswer:"

        # Generate response
        response = await self.llm_client.generate_response(full_prompt)

        return {
            "answer": response,
            "sources": context_docs,
            "query": query
        }

    def _format_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents into context text."""
        context_parts = []

        for i, doc in enumerate(context_docs, 1):
            metadata = doc.get("metadata", {})

            # Create source reference
            source = f"Source {i}"
            if "document_name" in metadata:
                source += f" ({metadata['document_name']})"

            # Add content
            content = doc.get("metadata", {}).get("text", "")
            if not content and "content" in doc:
                content = doc["content"]

            context_parts.append(f"{source}:\n{content}\n")

        return "\n".join(context_parts)

    async def query(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Complete RAG query pipeline."""
        # Retrieve context
        context_docs = await self.retrieve_context(query, top_k, filters)

        # Generate answer
        result = await self.generate_answer(query, context_docs)

        return result

class ConversationalRAG:
    """RAG with conversation memory."""

    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline
        self.conversation_history = []
        self.max_history = 10

    async def chat(self, user_message: str, top_k: int = 5) -> Dict[str, Any]:
        """Chat with RAG context and conversation history."""

        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Create contextual query
        contextual_query = self._create_contextual_query(user_message)

        # Get RAG response
        rag_result = await self.rag_pipeline.query(contextual_query, top_k)

        # Add assistant response to history
        self.conversation_history.append({"role": "assistant", "content": rag_result["answer"]})

        # Trim history if needed
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

        return rag_result

    def _create_contextual_query(self, current_query: str) -> str:
        """Create a query that includes conversation context."""
        if len(self.conversation_history) <= 1:
            return current_query

        # Get recent conversation
        recent_history = self.conversation_history[-4:]  # Last 2 exchanges

        context_parts = []
        for msg in recent_history[:-1]:  # Exclude current message
            role = "Human" if msg["role"] == "user" else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")

        conversation_context = "\n".join(context_parts)

        return f"Conversation context:\n{conversation_context}\n\nCurrent question: {current_query}"

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
```

### Knowledge Base Management

```python
class KnowledgeBaseManager:
    def __init__(self, rag_pipeline: RAGPipeline):
        self.rag_pipeline = rag_pipeline
        self.knowledge_bases = {}  # name -> config
        self.document_collections = {}  # kb_name -> documents

    async def create_knowledge_base(self, name: str, config: Dict[str, Any]):
        """Create a new knowledge base."""
        kb_config = {
            "name": name,
            "description": config.get("description", ""),
            "embedding_model": config.get("embedding_model", "text-embedding-3-small"),
            "vector_db": config.get("vector_db", "qdrant"),
            "chunk_strategy": config.get("chunk_strategy", "fixed_size"),
            "chunk_size": config.get("chunk_size", 1000),
            "chunk_overlap": config.get("chunk_overlap", 200),
            "created_at": datetime.utcnow().isoformat()
        }

        self.knowledge_bases[name] = kb_config
        self.document_collections[name] = []

        return kb_config

    async def add_documents_to_kb(self, kb_name: str, documents: List[Document]):
        """Add documents to a knowledge base."""
        if kb_name not in self.knowledge_bases:
            raise ValueError(f"Knowledge base {kb_name} does not exist")

        # Process documents with KB-specific chunking
        kb_config = self.knowledge_bases[kb_name]
        chunker = TextChunker()

        for doc in documents:
            # Apply KB-specific chunking strategy
            doc.chunks = chunker.chunk_text(
                doc.content,
                strategy=kb_config["chunk_strategy"],
                chunk_size=kb_config["chunk_size"],
                overlap=kb_config["chunk_overlap"]
            )

        # Add to RAG pipeline
        await self.rag_pipeline.add_documents(documents)

        # Track in collection
        self.document_collections[kb_name].extend(documents)

    async def query_knowledge_base(self, kb_name: str, query: str, **kwargs) -> Dict[str, Any]:
        """Query a specific knowledge base."""
        if kb_name not in self.knowledge_bases:
            raise ValueError(f"Knowledge base {kb_name} does not exist")

        # Add KB filter
        filters = kwargs.get("filters", {})
        filters["knowledge_base"] = kb_name

        return await self.rag_pipeline.query(query, filters=filters, **kwargs)

    async def list_knowledge_bases(self) -> List[Dict[str, Any]]:
        """List all knowledge bases."""
        return list(self.knowledge_bases.values())

    async def get_kb_stats(self, kb_name: str) -> Dict[str, Any]:
        """Get statistics for a knowledge base."""
        if kb_name not in self.knowledge_bases:
            kb_config = self.knowledge_bases[kb_name]
            documents = self.document_collections[kb_name]

            total_docs = len(documents)
            total_chunks = sum(len(doc.chunks) for doc in documents if doc.chunks)
            total_size = sum(doc.metadata.get("file_size", 0) for doc in documents)

            return {
                "name": kb_name,
                "description": kb_config.get("description", ""),
                "total_documents": total_docs,
                "total_chunks": total_chunks,
                "total_size_bytes": total_size,
                "created_at": kb_config.get("created_at", "")
            }

    async def delete_knowledge_base(self, kb_name: str):
        """Delete a knowledge base and its documents."""
        if kb_name not in self.knowledge_bases:
            raise ValueError(f"Knowledge base {kb_name} does not exist")

        # Remove from collections
        del self.knowledge_bases[kb_name]
        del self.document_collections[kb_name]

        # Note: In a real implementation, you'd also clean up vector database
        # This would require tracking document IDs per KB
```

This comprehensive knowledge management system provides powerful RAG capabilities with flexible document processing, multiple vector database support, and conversational memory. The system can handle various document types and provides efficient retrieval for generating contextually relevant answers. 🚀