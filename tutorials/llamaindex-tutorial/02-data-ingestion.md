---
layout: default
title: "Chapter 2: Data Ingestion & Loading"
parent: "LlamaIndex Tutorial"
nav_order: 2
---

# Chapter 2: Data Ingestion & Loading

Welcome to **Chapter 2: Data Ingestion & Loading**. In this part of **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Master the art of loading diverse data sources into LlamaIndex for comprehensive RAG systems.

## 🎯 Overview

This chapter covers LlamaIndex's powerful data ingestion capabilities, showing you how to load data from various sources including files, APIs, databases, and web content. You'll learn to handle different data formats and create robust data pipelines for your RAG applications.

## 📁 File-Based Data Loading

### Loading Local Files

```python
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.readers.file import (
    PDFReader, DocxReader, CSVReader, JSONReader
)
import os

# Method 1: Simple Directory Reader (automatic file type detection)
def load_directory_data(directory_path: str):
    """Load all supported files from a directory"""
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        recursive=True,  # Include subdirectories
        required_exts=[".pdf", ".docx", ".txt", ".md"],  # Filter file types
        exclude=["*.tmp", "*.log"]  # Exclude specific patterns
    )

    documents = reader.load_data()

    print(f"Loaded {len(documents)} documents from {directory_path}")
    for doc in documents[:3]:  # Show first 3
        print(f"- {doc.metadata.get('file_name', 'Unknown')}: {len(doc.text)} chars")

    return documents

# Method 2: Specific file readers for better control
def load_specific_files():
    """Load specific file types with custom readers"""
    documents = []

    # PDF files
    pdf_reader = PDFReader()
    pdf_docs = pdf_reader.load_data("path/to/document.pdf")
    documents.extend(pdf_docs)

    # Word documents
    docx_reader = DocxReader()
    docx_docs = docx_reader.load_data("path/to/document.docx")
    documents.extend(docx_docs)

    # CSV files
    csv_reader = CSVReader()
    csv_docs = csv_reader.load_data("path/to/data.csv")
    documents.extend(csv_docs)

    # JSON files
    json_reader = JSONReader()
    json_docs = json_reader.load_data("path/to/data.json")
    documents.extend(json_docs)

    return documents

# Method 3: Manual document creation
def create_documents_from_text():
    """Create Document objects from raw text or structured data"""
    documents = []

    # From text files
    with open("data/article.txt", "r", encoding="utf-8") as f:
        text = f.read()
        doc = Document(
            text=text,
            metadata={
                "source": "article.txt",
                "author": "Unknown",
                "date": "2024-01-01",
                "category": "general"
            },
            id_="article_001"
        )
        documents.append(doc)

    # From structured data
    import json
    with open("data/products.json", "r") as f:
        products = json.load(f)

    for product in products:
        text = f"Product: {product['name']}\nDescription: {product['description']}\nPrice: ${product['price']}"
        doc = Document(
            text=text,
            metadata={
                "source": "products.json",
                "product_id": product["id"],
                "category": product["category"],
                "price": product["price"]
            },
            id_=f"product_{product['id']}"
        )
        documents.append(doc)

    return documents

# Usage examples
if __name__ == "__main__":
    # Load from directory
    docs = load_directory_data("./data")

    # Load specific files
    specific_docs = load_specific_files()

    # Create from text
    manual_docs = create_documents_from_text()

    all_docs = docs + specific_docs + manual_docs
    print(f"Total documents loaded: {len(all_docs)}")
```

### Handling Large Files and Chunking

```python
from llama_index.core.node_parser import SimpleNodeParser, HierarchicalNodeParser
from llama_index.core.schema import Document
from llama_index.core import Settings

# Configure chunking settings
Settings.chunk_size = 1024
Settings.chunk_overlap = 200

def chunk_documents_basic(documents):
    """Basic document chunking"""
    parser = SimpleNodeParser.from_defaults(
        chunk_size=Settings.chunk_size,
        chunk_overlap=Settings.chunk_overlap,
        include_metadata=True,
        include_prev_next_rel=True  # Include previous/next relationships
    )

    nodes = parser.get_nodes_from_documents(documents)

    print(f"Created {len(nodes)} chunks from {len(documents)} documents")
    print(f"Average chunk size: {sum(len(node.text) for node in nodes) / len(nodes):.0f} chars")

    return nodes

def chunk_documents_hierarchical(documents):
    """Hierarchical chunking for complex documents"""
    parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=[2048, 512, 128],  # Multiple levels of chunking
        chunk_overlap=100,
        include_metadata=True,
        include_prev_next_rel=True
    )

    nodes = parser.get_nodes_from_documents(documents)

    # Organize by hierarchy level
    root_nodes = [n for n in nodes if n.parent_node is None]
    child_nodes = [n for n in nodes if n.parent_node is not None]

    print(f"Hierarchical chunking: {len(root_nodes)} root chunks, {len(child_nodes)} child chunks")

    return nodes

def chunk_documents_semantic(documents):
    """Semantic chunking based on content meaning"""
    from llama_index.core.node_parser import SemanticSplitterNodeParser
    from llama_index.embeddings.openai import OpenAIEmbedding

    embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    parser = SemanticSplitterNodeParser(
        buffer_size=1,  # Number of sentences to group
        breakpoint_percentile_threshold=95,  # Similarity threshold for splits
        embed_model=embed_model
    )

    nodes = parser.get_nodes_from_documents(documents)

    print(f"Semantic chunking created {len(nodes)} semantically coherent chunks")

    return nodes

# Advanced chunking strategies
def chunk_documents_advanced(documents):
    """Advanced chunking with multiple strategies"""
    from llama_index.core.node_parser import MarkdownNodeParser, CodeSplitter

    all_nodes = []

    for doc in documents:
        file_type = doc.metadata.get("file_type", "text")

        if file_type == "markdown":
            # Use markdown-aware chunking
            parser = MarkdownNodeParser()
            nodes = parser.get_nodes_from_documents([doc])
            all_nodes.extend(nodes)

        elif file_type in ["python", "javascript", "java"]:
            # Use code-aware chunking
            parser = CodeSplitter(
                language=file_type,
                chunk_lines=50,  # Chunk every 50 lines
                chunk_lines_overlap=10,
                max_chars=2000
            )
            nodes = parser.get_nodes_from_documents([doc])
            all_nodes.extend(nodes)

        else:
            # Default chunking
            parser = SimpleNodeParser.from_defaults(
                chunk_size=1024,
                chunk_overlap=200
            )
            nodes = parser.get_nodes_from_documents([doc])
            all_nodes.extend(nodes)

    print(f"Advanced chunking: {len(all_nodes)} total nodes from {len(documents)} documents")
    return all_nodes

# Usage
documents = [
    Document(text="Long document content here...", metadata={"file_type": "markdown"}),
    Document(text="Code content here...", metadata={"file_type": "python"}),
    Document(text="Regular text content...", metadata={"file_type": "text"})
]

# Different chunking strategies
basic_nodes = chunk_documents_basic(documents.copy())
hierarchical_nodes = chunk_documents_hierarchical(documents.copy())
# semantic_nodes = chunk_documents_semantic(documents.copy())  # Requires OpenAI API
advanced_nodes = chunk_documents_advanced(documents.copy())
```

## 🌐 Web and API Data Loading

### Loading from Web Sources

```python
from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader
from llama_index.readers.web import WholeSiteReader, RssReader
import asyncio

async def load_web_pages():
    """Load content from web pages"""
    urls = [
        "https://example.com/article1",
        "https://example.com/article2",
        "https://blog.example.com/post1"
    ]

    # Simple web page reader
    reader = SimpleWebPageReader()
    documents = await reader.aload_data(urls)

    print(f"Loaded {len(documents)} web pages")
    for doc in documents:
        print(f"- {doc.metadata.get('title', 'No title')}: {len(doc.text)} chars")

    return documents

def load_web_pages_soup():
    """Load web pages with BeautifulSoup for better parsing"""
    reader = BeautifulSoupWebReader()

    documents = reader.load_data(
        urls=["https://example.com"],
        custom_hostname="example.com",
        tags=["p", "h1", "h2", "h3", "article"]  # Extract specific tags
    )

    return documents

async def load_entire_website():
    """Load entire website with crawling"""
    reader = WholeSiteReader(
        prefix="https://example.com",
        max_depth=2,  # Crawl depth
        exclude_suffixes=[".pdf", ".jpg", ".png"],  # Skip binary files
        include_suffixes=[".html", ".htm", ".php"]  # Only HTML pages
    )

    documents = await reader.aload_data()

    print(f"Crawled {len(documents)} pages from website")
    return documents

def load_rss_feeds():
    """Load content from RSS feeds"""
    rss_urls = [
        "https://example.com/rss.xml",
        "https://blog.example.com/feed"
    ]

    reader = RssReader()
    documents = reader.load_data(urls=rss_urls)

    print(f"Loaded {len(documents)} RSS items")
    for doc in documents[:3]:
        print(f"- {doc.metadata.get('title', 'No title')} ({doc.metadata.get('publish_date', 'No date')})")

    return documents

# API data loading
def load_from_rest_api():
    """Load data from REST APIs"""
    from llama_index.readers.json import JSONReader
    import requests

    # Fetch data from API
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()

    # Convert to documents
    documents = []
    for item in data:
        text = f"Title: {item['title']}\nBody: {item['body']}"
        doc = Document(
            text=text,
            metadata={
                "source": "jsonplaceholder_api",
                "id": item["id"],
                "user_id": item["userId"],
                "api_endpoint": "/posts"
            },
            id_=f"post_{item['id']}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} items from REST API")
    return documents

# GraphQL API loading
def load_from_graphql_api():
    """Load data from GraphQL APIs"""
    import requests

    query = """
    {
        posts {
            id
            title
            content
            author {
                name
            }
        }
    }
    """

    response = requests.post(
        "https://api.example.com/graphql",
        json={"query": query}
    )

    data = response.json()["data"]["posts"]

    documents = []
    for post in data:
        text = f"Title: {post['title']}\nContent: {post['content']}\nAuthor: {post['author']['name']}"
        doc = Document(
            text=text,
            metadata={
                "source": "graphql_api",
                "id": post["id"],
                "author": post["author"]["name"],
                "api_type": "graphql"
            },
            id_=f"graphql_post_{post['id']}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} items from GraphQL API")
    return documents

# Usage
async def main():
    # Web content
    web_docs = await load_web_pages()
    rss_docs = load_rss_feeds()

    # API content
    rest_docs = load_from_rest_api()
    graphql_docs = load_from_graphql_api()

    all_docs = web_docs + rss_docs + rest_docs + graphql_docs
    print(f"Total documents from web/API sources: {len(all_docs)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🗄️ Database Integration

### SQL Database Loading

```python
from llama_index.readers.database import DatabaseReader
from llama_index.core import Document
import sqlite3
import pandas as pd

def load_from_sqlite():
    """Load data from SQLite database"""
    # Create sample database (in practice, you'd connect to existing DB)
    conn = sqlite3.connect(":memory:")

    # Create sample table
    conn.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            content TEXT,
            category TEXT,
            published_date DATE
        )
    """)

    # Insert sample data
    sample_data = [
        (1, "AI Advances", "Artificial intelligence is transforming industries...", "technology", "2024-01-01"),
        (2, "Machine Learning", "Machine learning algorithms learn from data...", "technology", "2024-01-02"),
        (3, "Data Science", "Data science combines statistics and programming...", "analytics", "2024-01-03")
    ]

    conn.executemany("INSERT INTO articles VALUES (?, ?, ?, ?, ?)", sample_data)
    conn.commit()

    # Load using DatabaseReader
    reader = DatabaseReader(
        uri="sqlite:///:memory:",
        engine=conn  # Pass existing connection
    )

    # Custom query
    query = """
    SELECT id, title, content, category, published_date
    FROM articles
    WHERE category = 'technology'
    ORDER BY published_date DESC
    """

    documents = reader.load_data(query=query)

    print(f"Loaded {len(documents)} records from SQLite")
    for doc in documents:
        metadata = doc.metadata
        print(f"- {metadata['title']} ({metadata['category']})")

    conn.close()
    return documents

def load_from_postgresql():
    """Load data from PostgreSQL database"""
    from sqlalchemy import create_engine

    # Database connection
    engine = create_engine("postgresql://user:password@localhost:5432/mydb")

    reader = DatabaseReader(
        uri="postgresql://user:password@localhost:5432/mydb",
        engine=engine
    )

    # Complex query with joins
    query = """
    SELECT
        a.id,
        a.title,
        a.content,
        a.published_date,
        c.name as category_name,
        u.username as author_name
    FROM articles a
    JOIN categories c ON a.category_id = c.id
    JOIN users u ON a.author_id = u.id
    WHERE a.published_date >= '2024-01-01'
    ORDER BY a.published_date DESC
    LIMIT 100
    """

    documents = reader.load_data(query=query)

    print(f"Loaded {len(documents)} articles from PostgreSQL")
    return documents

def load_from_mysql():
    """Load data from MySQL database"""
    reader = DatabaseReader(
        uri="mysql://user:password@localhost:3306/mydb"
    )

    # Load entire table
    documents = reader.load_data(
        table_name="products",
        text_columns=["name", "description", "features"],  # Columns to include in text
        metadata_columns=["id", "category", "price", "created_at"]  # Columns for metadata
    )

    print(f"Loaded {len(documents)} products from MySQL")
    return documents

# NoSQL Database Loading
def load_from_mongodb():
    """Load data from MongoDB"""
    from llama_index.readers.mongodb import MongoReader

    reader = MongoReader(
        uri="mongodb://localhost:27017",
        db_name="content_db",
        collection_name="articles"
    )

    # Query with filter
    query = {"category": "technology", "published": True}
    fields = ["title", "content", "author", "tags"]

    documents = reader.load_data(
        query=query,
        field_names=fields,
        metadata_names=["author", "tags", "published_date"]
    )

    print(f"Loaded {len(documents)} documents from MongoDB")
    return documents

# Vector Database Integration
def load_from_pinecone():
    """Load data from Pinecone vector database"""
    from llama_index.vector_stores.pinecone import PineconeVectorStore

    # This would be used for loading existing vector data
    # Typically used for querying rather than initial loading
    vector_store = PineconeVectorStore(
        api_key="your-pinecone-api-key",
        index_name="my-index",
        environment="us-east-1"
    )

    # Note: This is typically used for querying existing vectors
    # For initial data loading, you'd use other readers first
    print("Pinecone vector store configured")
    return vector_store

# Usage
if __name__ == "__main__":
    # SQL databases
    sqlite_docs = load_from_sqlite()
    # postgres_docs = load_from_postgresql()  # Requires PostgreSQL setup
    # mysql_docs = load_from_mysql()  # Requires MySQL setup

    # NoSQL databases
    # mongo_docs = load_from_mongodb()  # Requires MongoDB setup

    # Vector databases
    # pinecone_store = load_from_pinecone()  # Requires Pinecone setup

    print("Database loading examples completed")
```

## 📊 Structured Data Loading

### Loading from DataFrames and CSV

```python
import pandas as pd
from llama_index.core import Document

def load_from_dataframe():
    """Load data from pandas DataFrame"""
    # Create sample DataFrame
    data = {
        "title": ["AI Research", "ML Algorithms", "Data Science"],
        "content": [
            "Recent advances in artificial intelligence...",
            "Machine learning algorithms are powerful tools...",
            "Data science combines multiple disciplines..."
        ],
        "category": ["research", "education", "overview"],
        "author": ["Dr. Smith", "Prof. Johnson", "Dr. Brown"],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"]
    }

    df = pd.DataFrame(data)

    documents = []

    for idx, row in df.iterrows():
        # Combine relevant columns into text
        text = f"Title: {row['title']}\nContent: {row['content']}\nAuthor: {row['author']}"

        doc = Document(
            text=text,
            metadata={
                "source": "dataframe",
                "row_id": idx,
                "category": row["category"],
                "author": row["author"],
                "date": row["date"],
                "title": row["title"]
            },
            id_=f"df_row_{idx}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} documents from DataFrame")
    return documents

def load_from_csv_file():
    """Load data from CSV file"""
    # Read CSV file
    df = pd.read_csv("data/articles.csv")

    documents = []

    for idx, row in df.iterrows():
        # Customize text creation based on CSV columns
        if "summary" in df.columns:
            text = f"{row['title']}\n\n{row['summary']}\n\n{row.get('content', '')}"
        else:
            text = f"{row['title']}\n\n{row.get('content', '')}"

        # Extract metadata
        metadata = {}
        for col in df.columns:
            if col not in ["title", "content", "summary"]:  # Don't duplicate in metadata
                metadata[col] = row[col]

        metadata["source"] = "csv_file"
        metadata["row_id"] = idx

        doc = Document(
            text=text,
            metadata=metadata,
            id_=f"csv_row_{idx}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} documents from CSV")
    return documents

def load_from_excel_file():
    """Load data from Excel file"""
    df = pd.read_excel("data/products.xlsx", sheet_name="Products")

    documents = []

    for idx, row in df.iterrows():
        # Create product description
        text = f"Product: {row['name']}\n"
        text += f"Category: {row['category']}\n"
        text += f"Price: ${row['price']}\n"
        text += f"Description: {row.get('description', 'No description available')}"

        if "features" in df.columns and pd.notna(row["features"]):
            text += f"\nFeatures: {row['features']}"

        doc = Document(
            text=text,
            metadata={
                "source": "excel_file",
                "product_id": row.get("id"),
                "category": row["category"],
                "price": row["price"],
                "in_stock": row.get("in_stock", True),
                "row_id": idx
            },
            id_=f"excel_product_{idx}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} products from Excel")
    return documents

# Advanced DataFrame processing
def load_from_dataframe_with_processing():
    """Load DataFrame with advanced processing"""
    df = pd.read_csv("data/complex_data.csv")

    # Data cleaning and preprocessing
    df = df.dropna(subset=["title", "content"])  # Remove rows with missing essential data
    df["content"] = df["content"].str.strip()  # Clean whitespace
    df["word_count"] = df["content"].str.split().str.len()  # Add word count

    # Filter based on criteria
    df = df[df["word_count"] > 50]  # Only include substantial content
    df = df[df["category"].isin(["technology", "science", "business"])]  # Filter categories

    documents = []

    for idx, row in df.iterrows():
        # Create rich text representation
        text_parts = [
            f"Title: {row['title']}",
            f"Category: {row['category']}",
            f"Author: {row.get('author', 'Unknown')}",
            f"Published: {row.get('date', 'Unknown date')}",
            f"Word Count: {row['word_count']}",
            "",
            row["content"]
        ]

        text = "\n".join(text_parts)

        # Rich metadata
        metadata = {
            "source": "processed_dataframe",
            "row_id": idx,
            "category": row["category"],
            "author": row.get("author"),
            "date": row.get("date"),
            "word_count": row["word_count"],
            "title": row["title"],
            "tags": row.get("tags", "").split(",") if pd.notna(row.get("tags")) else []
        }

        doc = Document(
            text=text,
            metadata=metadata,
            id_=f"processed_df_{idx}"
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} processed documents from DataFrame")
    print(f"Average word count: {df['word_count'].mean():.0f}")
    print(f"Categories: {df['category'].value_counts().to_dict()}")

    return documents

# Usage
if __name__ == "__main__":
    # DataFrame loading
    df_docs = load_from_dataframe()

    # CSV loading
    csv_docs = load_from_csv_file()

    # Excel loading
    excel_docs = load_from_excel_file()

    # Advanced processing
    processed_docs = load_from_dataframe_with_processing()

    all_structured_docs = df_docs + csv_docs + excel_docs + processed_docs
    print(f"Total structured documents loaded: {len(all_structured_docs)}")
```

## 🔄 Custom Data Loaders

### Building Custom Readers

```python
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import List

class CustomAPIReader(BaseReader):
    """Custom reader for proprietary API"""

    def __init__(self, api_key: str, base_url: str = "https://api.example.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })

    def load_data(self, endpoint: str, params: dict = None) -> List[Document]:
        """Load data from custom API"""
        url = f"{self.base_url}{endpoint}"

        response = self.session.get(url, params=params or {})
        response.raise_for_status()

        data = response.json()

        documents = []
        for item in data.get("items", []):
            # Customize text extraction based on API response
            text = self._extract_text_from_item(item)

            doc = Document(
                text=text,
                metadata={
                    "source": "custom_api",
                    "endpoint": endpoint,
                    "item_id": item.get("id"),
                    "created_at": item.get("created_at"),
                    "api_response": item  # Store full response for reference
                },
                id_=f"api_{endpoint}_{item.get('id')}"
            )
            documents.append(doc)

        print(f"Loaded {len(documents)} items from {endpoint}")
        return documents

    def _extract_text_from_item(self, item: dict) -> str:
        """Extract text content from API item"""
        text_parts = []

        if "title" in item:
            text_parts.append(f"Title: {item['title']}")

        if "description" in item:
            text_parts.append(f"Description: {item['description']}")

        if "content" in item:
            text_parts.append(f"Content: {item['content']}")

        if "tags" in item:
            text_parts.append(f"Tags: {', '.join(item['tags'])}")

        return "\n\n".join(text_parts)

class SlackReader(BaseReader):
    """Reader for Slack workspace data"""

    def __init__(self, token: str):
        from slack_sdk import WebClient
        self.client = WebClient(token=token)

    def load_data(self, channel_names: List[str] = None, days_back: int = 30) -> List[Document]:
        """Load Slack messages from specified channels"""
        import datetime

        # Get channel list
        channels_response = self.client.conversations_list()
        channels = channels_response["channels"]

        # Filter channels if specified
        if channel_names:
            channels = [c for c in channels if c["name"] in channel_names]

        documents = []

        for channel in channels:
            channel_id = channel["id"]
            channel_name = channel["name"]

            # Calculate timestamp for days_back
            since = datetime.datetime.now() - datetime.timedelta(days=days_back)
            oldest = since.timestamp()

            # Get messages
            messages_response = self.client.conversations_history(
                channel=channel_id,
                oldest=oldest,
                limit=1000
            )

            messages = messages_response["messages"]

            # Group messages by thread
            threads = {}
            for msg in messages:
                thread_ts = msg.get("thread_ts", msg["ts"])
                if thread_ts not in threads:
                    threads[thread_ts] = []
                threads[thread_ts].append(msg)

            # Create documents for each thread
            for thread_ts, thread_messages in threads.items():
                text = self._format_thread(thread_messages)

                # Find thread starter
                thread_starter = next((m for m in thread_messages if m["ts"] == thread_ts), thread_messages[0])

                doc = Document(
                    text=text,
                    metadata={
                        "source": "slack",
                        "channel": channel_name,
                        "channel_id": channel_id,
                        "thread_ts": thread_ts,
                        "message_count": len(thread_messages),
                        "starter_user": thread_starter.get("user"),
                        "timestamp": thread_starter.get("ts"),
                        "has_reactions": any("reactions" in m for m in thread_messages)
                    },
                    id_=f"slack_{channel_name}_{thread_ts}"
                )
                documents.append(doc)

        print(f"Loaded {len(documents)} thread documents from Slack")
        return documents

    def _format_thread(self, messages: List[dict]) -> str:
        """Format thread messages into readable text"""
        formatted = []

        for msg in sorted(messages, key=lambda x: x["ts"]):
            user = msg.get("user", "Unknown")
            text = msg.get("text", "")
            timestamp = msg.get("ts", "")

            formatted.append(f"[{user}] {text}")

            # Include replies
            if "replies" in msg:
                for reply in msg["replies"]:
                    formatted.append(f"  ↳ [{reply['user']}] Reply in thread")

        return "\n".join(formatted)

class GitHubReader(BaseReader):
    """Reader for GitHub repository data"""

    def __init__(self, token: str = None):
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            })

    def load_data(self, repo_owner: str, repo_name: str,
                  include_issues: bool = True, include_prs: bool = True,
                  include_readme: bool = True) -> List[Document]:
        """Load GitHub repository data"""

        documents = []

        # Load README
        if include_readme:
            readme_doc = self._load_readme(repo_owner, repo_name)
            if readme_doc:
                documents.append(readme_doc)

        # Load issues
        if include_issues:
            issue_docs = self._load_issues(repo_owner, repo_name)
            documents.extend(issue_docs)

        # Load pull requests
        if include_prs:
            pr_docs = self._load_pull_requests(repo_owner, repo_name)
            documents.extend(pr_docs)

        print(f"Loaded {len(documents)} documents from GitHub repo {repo_owner}/{repo_name}")
        return documents

    def _load_readme(self, owner: str, repo: str) -> Document:
        """Load repository README"""
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"

        try:
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")

            return Document(
                text=content,
                metadata={
                    "source": "github_readme",
                    "repo": f"{owner}/{repo}",
                    "file_path": data["path"],
                    "size": data["size"],
                    "download_url": data["download_url"]
                },
                id_=f"github_{owner}_{repo}_readme"
            )
        except Exception as e:
            print(f"Failed to load README: {e}")
            return None

    def _load_issues(self, owner: str, repo: str, limit: int = 50) -> List[Document]:
        """Load GitHub issues"""
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {"state": "all", "per_page": min(limit, 100)}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            issues = response.json()
            documents = []

            for issue in issues:
                if "pull_request" in issue:  # Skip pull requests
                    continue

                text = f"Title: {issue['title']}\n\nBody: {issue.get('body', 'No description')}\n\nState: {issue['state']}"

                if issue.get("labels"):
                    labels = [label["name"] for label in issue["labels"]]
                    text += f"\nLabels: {', '.join(labels)}"

                doc = Document(
                    text=text,
                    metadata={
                        "source": "github_issue",
                        "repo": f"{owner}/{repo}",
                        "issue_number": issue["number"],
                        "state": issue["state"],
                        "created_at": issue["created_at"],
                        "updated_at": issue["updated_at"],
                        "comments_count": issue["comments"],
                        "labels": [label["name"] for label in issue.get("labels", [])]
                    },
                    id_=f"github_{owner}_{repo}_issue_{issue['number']}"
                )
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"Failed to load issues: {e}")
            return []

    def _load_pull_requests(self, owner: str, repo: str, limit: int = 30) -> List[Document]:
        """Load GitHub pull requests"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {"state": "all", "per_page": min(limit, 100)}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            prs = response.json()
            documents = []

            for pr in prs:
                text = f"Title: {pr['title']}\n\nBody: {pr.get('body', 'No description')}\n\nState: {pr['state']}"

                if pr.get("labels"):
                    labels = [label["name"] for label in pr["labels"]]
                    text += f"\nLabels: {', '.join(labels)}"

                doc = Document(
                    text=text,
                    metadata={
                        "source": "github_pr",
                        "repo": f"{owner}/{repo}",
                        "pr_number": pr["number"],
                        "state": pr["state"],
                        "created_at": pr["created_at"],
                        "updated_at": pr["updated_at"],
                        "merged": pr.get("merged", False),
                        "comments_count": pr["comments"],
                        "review_comments_count": pr.get("review_comments", 0)
                    },
                    id_=f"github_{owner}_{repo}_pr_{pr['number']}"
                )
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"Failed to load PRs: {e}")
            return []

# Usage
if __name__ == "__main__":
    # Custom API reader
    api_reader = CustomAPIReader(api_key="your-api-key")
    api_docs = api_reader.load_data("/articles", {"limit": 10})

    # Slack reader
    # slack_reader = SlackReader(token="your-slack-token")
    # slack_docs = slack_reader.load_data(["general", "random"], days_back=7)

    # GitHub reader
    github_reader = GitHubReader(token="your-github-token")
    github_docs = github_reader.load_data("run-llama", "llama_index")

    all_custom_docs = api_docs + github_docs
    print(f"Total custom documents loaded: {len(all_custom_docs)}")
```

## 🎯 Best Practices

### Data Loading Best Practices

1. **Source Validation**: Always validate data sources and handle connection errors gracefully
2. **Incremental Loading**: Implement incremental loading for large datasets to avoid memory issues
3. **Metadata Enrichment**: Add comprehensive metadata to documents for better filtering and retrieval
4. **Error Handling**: Implement robust error handling for network requests and data parsing
5. **Rate Limiting**: Respect API rate limits and implement backoff strategies
6. **Data Quality**: Clean and preprocess data during loading to ensure quality
7. **Monitoring**: Track loading performance and success rates
8. **Caching**: Cache frequently accessed data to improve performance

### Performance Optimization

1. **Batch Processing**: Load data in batches to optimize memory usage
2. **Parallel Loading**: Use async operations for concurrent data loading
3. **Chunking Strategy**: Choose appropriate chunking based on content type and use case
4. **Indexing Hints**: Provide indexing hints for better query performance
5. **Compression**: Use compression for large datasets during storage
6. **Lazy Loading**: Implement lazy loading for large document collections
7. **Resource Management**: Properly manage database connections and file handles

## 📈 Next Steps

With data ingestion mastered, you're ready to:

- **[Chapter 3: Indexing & Storage](03-indexing-storage.md)** - Create efficient indexes for fast retrieval
- **[Chapter 4: Query Engines & Retrieval](04-query-engines.md)** - Build sophisticated query and retrieval systems
- **[Chapter 5: Advanced RAG Patterns](05-advanced-rag.md)** - Multi-modal, agent-based, and hybrid approaches

---

**Ready to create efficient indexes for your data? Continue to [Chapter 3: Indexing & Storage](03-indexing-storage.md)!** 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `documents`, `text`, `print` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Data Ingestion & Loading` as an operating subsystem inside **LlamaIndex Tutorial: Building Advanced RAG Systems and Data Frameworks**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `metadata`, `content`, `self` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Data Ingestion & Loading` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `documents`.
2. **Input normalization**: shape incoming data so `text` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `print`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/run-llama/llama_index)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `documents` and `text` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LlamaIndex](01-getting-started.md)
- [Next Chapter: Chapter 3: Indexing & Storage](03-indexing-storage.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
