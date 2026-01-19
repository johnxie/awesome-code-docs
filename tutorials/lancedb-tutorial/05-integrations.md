---
layout: default
title: "Chapter 5: Integrations"
parent: "LanceDB Tutorial"
nav_order: 5
---

# Chapter 5: Integrations

> Connect LanceDB with LangChain, LlamaIndex, embedding providers, and other tools in the AI ecosystem.

## Overview

LanceDB integrates seamlessly with popular AI frameworks and tools. This chapter covers integrations with LangChain, LlamaIndex, various embedding providers, and other components of the modern AI stack.

## LangChain Integration

### Basic Setup

```python
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAIEmbeddings
import lancedb

# Create LanceDB connection
db = lancedb.connect("./langchain_lancedb")

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vector_store = LanceDB(
    connection=db,
    embedding=embeddings,
    table_name="langchain_docs"
)
```

### Adding Documents

```python
from langchain.schema import Document

# Create documents
docs = [
    Document(
        page_content="LanceDB is a vector database",
        metadata={"source": "docs", "category": "database"}
    ),
    Document(
        page_content="LangChain helps build LLM applications",
        metadata={"source": "docs", "category": "framework"}
    ),
]

# Add to vector store
vector_store.add_documents(docs)

# Or add texts directly
texts = ["First document", "Second document"]
metadatas = [{"id": 1}, {"id": 2}]
vector_store.add_texts(texts, metadatas=metadatas)
```

### Similarity Search

```python
# Basic similarity search
results = vector_store.similarity_search(
    "What is a vector database?",
    k=5
)

for doc in results:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print("---")

# Search with scores
results_with_scores = vector_store.similarity_search_with_score(
    "vector database",
    k=5
)

for doc, score in results_with_scores:
    print(f"Score: {score:.4f} - {doc.page_content[:50]}...")

# Search with filter
results = vector_store.similarity_search(
    "database",
    k=5,
    filter={"category": "database"}
)
```

### As Retriever

```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Create retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Use in chain
llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

response = qa_chain.invoke("What is LanceDB?")
print(response)
```

### Advanced LangChain Patterns

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Load and split documents
loader = TextLoader("./documents/guide.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = splitter.split_documents(documents)

# Create vector store from splits
vector_store = LanceDB.from_documents(
    documents=splits,
    embedding=embeddings,
    connection=db,
    table_name="chunked_docs"
)
```

## LlamaIndex Integration

### Basic Setup

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.lancedb import LanceDBVectorStore
import lancedb

# Connect to LanceDB
db = lancedb.connect("./llamaindex_lancedb")

# Create vector store
vector_store = LanceDBVectorStore(
    uri="./llamaindex_lancedb",
    table_name="llama_docs"
)

# Create storage context
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)
```

### Creating Index

```python
from llama_index.core import SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Or create empty index and add documents later
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store
)
index.insert_nodes(documents)
```

### Querying

```python
# Create query engine
query_engine = index.as_query_engine()

# Query
response = query_engine.query("What is LanceDB?")
print(response)

# With retrieval parameters
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="tree_summarize"
)
```

### Chat Engine

```python
from llama_index.core.memory import ChatMemoryBuffer

# Create chat engine with memory
memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    similarity_top_k=5
)

# Chat
response = chat_engine.chat("What is LanceDB?")
print(response)

response = chat_engine.chat("Tell me more about its features")
print(response)
```

## Embedding Providers

### OpenAI Embeddings

```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

# Using built-in OpenAI embeddings
openai = get_registry().get("openai").create(
    name="text-embedding-3-small",
    # api_key="..."  # Or use OPENAI_API_KEY env var
)

class Document(LanceModel):
    text: str = openai.SourceField()
    vector: Vector(openai.ndims()) = openai.VectorField()

db = lancedb.connect("./my_lancedb")
table = db.create_table("openai_docs", schema=Document)

# Add documents (auto-embedded)
table.add([{"text": "Hello world"}])

# Search (auto-embedded)
results = table.search("greeting").limit(5).to_pandas()
```

### Sentence Transformers

```python
from lancedb.embeddings import get_registry

# Sentence Transformers embeddings
st = get_registry().get("sentence-transformers").create(
    name="all-MiniLM-L6-v2"
)

class STDocument(LanceModel):
    text: str = st.SourceField()
    vector: Vector(st.ndims()) = st.VectorField()

table = db.create_table("st_docs", schema=STDocument)
```

### Cohere Embeddings

```python
from lancedb.embeddings import get_registry

cohere = get_registry().get("cohere").create(
    name="embed-english-v3.0",
    # api_key="..."  # Or use COHERE_API_KEY env var
)

class CohereDocument(LanceModel):
    text: str = cohere.SourceField()
    vector: Vector(cohere.ndims()) = cohere.VectorField()
```

### Ollama Embeddings

```python
from lancedb.embeddings import get_registry

ollama = get_registry().get("ollama").create(
    name="nomic-embed-text",
    host="http://localhost:11434"
)

class OllamaDocument(LanceModel):
    text: str = ollama.SourceField()
    vector: Vector(ollama.ndims()) = ollama.VectorField()
```

### Custom Embedding Function

```python
from lancedb.embeddings import EmbeddingFunction, register
import numpy as np

@register("my-embedder")
class MyEmbedder(EmbeddingFunction):
    """Custom embedding function."""

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self._model = None
        self._ndims = 384

    def ndims(self) -> int:
        return self._ndims

    def compute_source_embeddings(self, texts: list[str]) -> list[np.ndarray]:
        # Your embedding logic here
        return [np.random.rand(self._ndims) for _ in texts]

    def compute_query_embeddings(self, query: str) -> np.ndarray:
        return self.compute_source_embeddings([query])[0]

# Usage
my_embedder = get_registry().get("my-embedder").create()
```

## Pandas Integration

### From DataFrame

```python
import lancedb
import pandas as pd
import numpy as np

db = lancedb.connect("./my_lancedb")

# Create DataFrame
df = pd.DataFrame({
    "id": range(100),
    "text": [f"Document {i}" for i in range(100)],
    "category": np.random.choice(["A", "B", "C"], 100),
    "vector": [np.random.rand(384).tolist() for _ in range(100)]
})

# Create table from DataFrame
table = db.create_table("from_pandas", df)

# Add more data from DataFrame
new_df = pd.DataFrame({...})
table.add(new_df)
```

### To DataFrame

```python
# Export entire table to DataFrame
df = table.to_pandas()

# Search results to DataFrame
results_df = table.search(query_vector).limit(10).to_pandas()

# With SQL
df = db.execute_sql("SELECT * FROM my_table WHERE category = 'A'").to_pandas()
```

## Polars Integration

```python
import lancedb
import polars as pl
import numpy as np

db = lancedb.connect("./my_lancedb")

# Create Polars DataFrame
df = pl.DataFrame({
    "id": range(100),
    "text": [f"Document {i}" for i in range(100)],
    "vector": [np.random.rand(384).tolist() for _ in range(100)]
})

# Create table from Polars (converts to Arrow)
table = db.create_table("from_polars", df.to_arrow())

# Search results to Polars
arrow_table = table.search(query_vector).limit(10).to_arrow()
results_pl = pl.from_arrow(arrow_table)
```

## DuckDB Integration

```python
import lancedb
import duckdb

# Connect to LanceDB
db = lancedb.connect("./my_lancedb")
table = db.open_table("my_table")

# Export to Arrow
arrow_table = table.to_arrow()

# Query with DuckDB
result = duckdb.query("""
    SELECT category, COUNT(*) as count
    FROM arrow_table
    GROUP BY category
    ORDER BY count DESC
""").to_df()

print(result)
```

## FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import lancedb
import numpy as np

app = FastAPI()
db = lancedb.connect("./api_lancedb")

class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    filter: str = None

class Document(BaseModel):
    text: str
    metadata: dict = {}

@app.post("/documents")
async def add_document(doc: Document):
    table = db.open_table("documents")
    vector = embed_text(doc.text)
    table.add([{
        "text": doc.text,
        "vector": vector,
        "metadata": doc.metadata
    }])
    return {"status": "added"}

@app.post("/search")
async def search(request: SearchRequest):
    table = db.open_table("documents")
    query_vector = embed_text(request.query)

    search = table.search(query_vector).limit(request.limit)

    if request.filter:
        search = search.where(request.filter)

    results = search.to_list()
    return {"results": results}

@app.get("/health")
async def health():
    return {"status": "healthy", "tables": db.table_names()}
```

## Gradio Integration

```python
import gradio as gr
import lancedb

db = lancedb.connect("./gradio_lancedb")
table = db.open_table("documents")

def search(query: str, top_k: int = 5):
    """Search function for Gradio."""
    query_vector = embed_text(query)
    results = table.search(query_vector).limit(top_k).to_list()

    output = []
    for r in results:
        output.append(f"**Score:** {1 - r['_distance']:.4f}\n{r['content']}\n---")

    return "\n".join(output)

# Create Gradio interface
demo = gr.Interface(
    fn=search,
    inputs=[
        gr.Textbox(label="Search Query"),
        gr.Slider(1, 20, value=5, label="Number of Results")
    ],
    outputs=gr.Markdown(label="Results"),
    title="LanceDB Search Demo"
)

demo.launch()
```

## Streamlit Integration

```python
import streamlit as st
import lancedb

@st.cache_resource
def get_db():
    return lancedb.connect("./streamlit_lancedb")

def main():
    st.title("LanceDB Search")

    db = get_db()
    table = db.open_table("documents")

    query = st.text_input("Enter your search query:")

    if query:
        query_vector = embed_text(query)
        results = table.search(query_vector).limit(10).to_pandas()

        st.subheader("Results")
        for _, row in results.iterrows():
            with st.expander(f"Score: {1 - row['_distance']:.4f}"):
                st.write(row['content'])
                st.json(row.get('metadata', {}))

if __name__ == "__main__":
    main()
```

## Summary

In this chapter, you've learned:

- **LangChain**: Vector stores, retrievers, and chains
- **LlamaIndex**: Indexes, query engines, and chat
- **Embedding Providers**: OpenAI, Sentence Transformers, Cohere, Ollama
- **Custom Embeddings**: Building your own embedding functions
- **Data Tools**: Pandas, Polars, and DuckDB integration
- **Web Frameworks**: FastAPI, Gradio, and Streamlit

## Key Takeaways

1. **Framework Support**: LanceDB works with major AI frameworks
2. **Flexible Embeddings**: Many providers supported out of the box
3. **Custom Integration**: Easy to build custom embedding functions
4. **Data Ecosystem**: Seamless with pandas/polars/arrow
5. **Web Ready**: Simple to add to web applications

## Next Steps

Now that you know how to integrate LanceDB, let's explore Performance in Chapter 6 for optimizing your deployments.

---

**Ready for Chapter 6?** [Performance](06-performance.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
