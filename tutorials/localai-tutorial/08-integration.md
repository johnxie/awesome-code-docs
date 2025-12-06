---
layout: default
title: "LocalAI Tutorial - Chapter 8: Integration"
nav_order: 8
has_children: false
parent: LocalAI Tutorial
---

# Chapter 8: Production Integration and Applications

> Build production applications with LocalAI, integrating with web frameworks, APIs, and enterprise systems.

## Overview

LocalAI's OpenAI-compatible API makes it easy to integrate into existing applications. This chapter covers production integration patterns and real-world applications.

## Web Framework Integration

### FastAPI Application

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import openai
import asyncio
import logging

app = FastAPI(title="AI Assistant API", version="1.0.0")

# Initialize LocalAI client
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"  # LocalAI doesn't require authentication
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    model: str = "phi-2"
    temperature: float = 0.7
    max_tokens: int = 500
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[dict] = None

class ImageRequest(BaseModel):
    prompt: str
    size: str = "512x512"
    n: int = 1

class ImageResponse(BaseModel):
    images: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """Chat endpoint with LocalAI."""
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.message}],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )

        if request.stream:
            # Handle streaming response
            return StreamingResponse(
                stream_chat_response(response),
                media_type="text/plain"
            )

        # Regular response
        content = response.choices[0].message.content

        # Log usage in background
        background_tasks.add_task(log_usage, request.model, response.usage)

        return ChatResponse(
            response=content,
            model=request.model,
            usage=response.usage.model_dump() if response.usage else None
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_chat_response(response):
    """Generator for streaming chat responses."""
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield f"data: {chunk.choices[0].delta.content}\n\n"
        await asyncio.sleep(0.01)  # Small delay to prevent overwhelming client

@app.post("/images", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    """Image generation endpoint."""
    try:
        response = client.images.generate(
            model="stablediffusion",
            prompt=request.prompt,
            size=request.size,
            n=request.n
        )

        images = [data.url for data in response.data]

        return ImageResponse(images=images)

    except Exception as e:
        logger.error(f"Image generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/transcribe")
async def transcribe_audio(audio_file):
    """Audio transcription endpoint."""
    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        return {"text": transcription.text}

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/speak")
async def text_to_speech(text: str, voice: str = "alloy"):
    """Text-to-speech endpoint."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="mp3"
        )

        return StreamingResponse(
            iter([response.content]),
            media_type="audio/mpeg"
        )

    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_usage(model: str, usage: dict):
    """Log API usage for analytics."""
    if usage:
        logger.info(f"Model: {model}, Tokens: {usage.get('total_tokens', 0)}")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test basic connectivity
        response = client.chat.completions.create(
            model="phi-2",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Flask Integration

```python
from flask import Flask, request, jsonify, Response
import openai
import logging

app = Flask(__name__)

# Initialize LocalAI client
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """Flask chat endpoint."""
    try:
        data = request.json
        message = data.get('message', '')
        model = data.get('model', 'phi-2')

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 500)
        )

        return jsonify({
            'response': response.choices[0].message.content,
            'model': model,
            'usage': response.usage.model_dump() if response.usage else None
        })

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stream', methods=['POST'])
def stream():
    """Streaming chat endpoint."""
    data = request.json
    message = data.get('message', '')

    def generate():
        try:
            response = client.chat.completions.create(
                model="phi-2",
                messages=[{"role": "user", "content": message}],
                stream=True,
                max_tokens=500
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: Error: {str(e)}\n\n"

    return Response(generate(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=False)
```

## LangChain Integration

### LocalAI with LangChain

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Initialize LocalAI LLM
llm = OpenAI(
    model="phi-2",
    openai_api_key="dummy",
    openai_api_base="http://localhost:8080/v1",
    temperature=0.7,
    max_tokens=500
)

# Basic chain
template = """Question: {question}

Answer the question based on your knowledge. Keep the answer concise but informative."""

prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=llm, prompt=prompt)

# Conversation with memory
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)

# Embeddings for RAG
embeddings = OpenAIEmbeddings(
    openai_api_key="dummy",
    openai_api_base="http://localhost:8080/v1",
    model="all-minilm-l6-v2"
)

# Create vector store
texts = [
    "LocalAI is a free, open-source alternative to OpenAI.",
    "It runs locally on your machine with no data leaving your device.",
    "LocalAI supports multiple AI models including LLMs, image generation, and audio processing."
]

vectorstore = FAISS.from_texts(texts, embeddings)

# RAG chain
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Usage examples
print("Basic Chain:")
result = chain.run(question="What is the capital of France?")
print(result)

print("\nConversation:")
print(conversation.predict(input="Hello!"))
print(conversation.predict(input="What's my name?"))

print("\nRAG Query:")
result = qa_chain.run("What is LocalAI?")
print(result)
```

## CrewAI Integration

### Multi-Agent System with LocalAI

```python
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI

# Custom LocalAI LLM class for CrewAI
class LocalAILLM:
    def __init__(self, model="phi-2", temperature=0.7):
        self.client = OpenAI(
            model=model,
            openai_api_key="dummy",
            openai_api_base="http://localhost:8080/v1",
            temperature=temperature
        )

    def __call__(self, prompt, **kwargs):
        response = self.client.generate([prompt], **kwargs)
        return response.generations[0][0].text

# Initialize LLM
llm = LocalAILLM()

# Create agents
researcher = Agent(
    role="Research Analyst",
    goal="Analyze and summarize information about AI technologies",
    backstory="You are an expert AI researcher with deep knowledge of machine learning and AI systems.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging articles based on research findings",
    backstory="You are a skilled technical writer who can explain complex topics clearly.",
    llm=llm,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Review and improve written content for clarity and accuracy",
    backstory="You are an experienced editor who ensures content is polished and error-free.",
    llm=llm,
    verbose=True
)

# Create tasks
research_task = Task(
    description="Research the latest developments in multimodal AI systems",
    agent=researcher,
    expected_output="A comprehensive summary of multimodal AI advancements"
)

write_task = Task(
    description="Write a 800-word article about multimodal AI based on the research",
    agent=writer,
    expected_output="An engaging article explaining multimodal AI concepts and applications"
)

edit_task = Task(
    description="Review and edit the article for clarity, accuracy, and engagement",
    agent=editor,
    expected_output="A polished, error-free article ready for publication"
)

# Create and run crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    verbose=True
)

result = crew.kickoff()
print("Final Result:")
print(result)
```

## LlamaIndex Integration

### RAG Application with LocalAI

```python
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    load_index_from_storage
)
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
import os

# Initialize LocalAI LLM
llm = OpenAI(
    model="phi-2",
    api_key="dummy",
    api_base="http://localhost:8080/v1"
)

# Initialize LocalAI embeddings
embed_model = OpenAIEmbedding(
    model="all-minilm-l6-v2",
    api_key="dummy",
    api_base="http://localhost:8080/v1"
)

# Create service context
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model
)

def create_or_load_index(data_dir="./data", index_dir="./index"):
    """Create or load vector index."""

    if os.path.exists(index_dir):
        # Load existing index
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context)
        print("Loaded existing index")
    else:
        # Create new index
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(
            documents,
            service_context=service_context
        )

        # Persist index
        index.storage_context.persist(persist_dir=index_dir)
        print("Created new index")

    return index

# Create query engine
index = create_or_load_index()
query_engine = index.as_query_engine(similarity_top_k=3)

# Query examples
queries = [
    "What are the main benefits of LocalAI?",
    "How does LocalAI compare to cloud AI services?",
    "What models are supported by LocalAI?"
]

for query in queries:
    print(f"\nQuery: {query}")
    response = query_engine.query(query)
    print(f"Response: {response}")
    print("-" * 50)
```

## Web Application Examples

### Streamlit Chat Interface

```python
import streamlit as st
import openai

# Initialize LocalAI client
client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)

st.title("🤖 LocalAI Chat Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            response = client.chat.completions.create(
                model="phi-2",
                messages=st.session_state.messages,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # Add AI response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar with model selection
with st.sidebar:
    st.header("Settings")

    model = st.selectbox(
        "Model",
        ["phi-2", "mistral-7b-instruct", "llama-2-7b-chat"],
        index=0
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
```

### Gradio Interface

```python
import gradio as gr
import openai

client = openai.OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)

def chat(message, history, model, temperature):
    """Chat function for Gradio."""

    # Build conversation
    messages = []
    for human, assistant in history:
        messages.extend([
            {"role": "user", "content": human},
            {"role": "assistant", "content": assistant}
        ])
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=500
        )

        bot_message = response.choices[0].message.content

        # Update history
        history.append((message, bot_message))

        return "", history

    except Exception as e:
        return "", history + [(message, f"Error: {str(e)}")]

# Create interface
with gr.Blocks(title="LocalAI Chat") as demo:
    gr.Markdown("# 🤖 LocalAI Chat Interface")

    chatbot = gr.Chatbot(height=500)

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Type your message here...",
            scale=4
        )
        submit = gr.Button("Send", scale=1)

    with gr.Row():
        model = gr.Dropdown(
            choices=["phi-2", "mistral-7b-instruct", "llama-2-7b-chat"],
            value="phi-2",
            label="Model"
        )
        temperature = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.7,
            step=0.1,
            label="Temperature"
        )

    # Clear button
    clear = gr.Button("Clear Chat")

    # Event handlers
    msg.submit(chat, [msg, chatbot, model, temperature], [msg, chatbot])
    submit.click(chat, [msg, chatbot, model, temperature], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
```

## Production Deployment

### Docker Compose Stack

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  localai:
    image: localai/localai:latest-cpu
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models:cached
      - ./config.yaml:/config.yaml:ro
    environment:
      - DEBUG=false
      - THREADS=8
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/readyz"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - LOCALAI_URL=http://localai:8080
    depends_on:
      - localai
    restart: unless-stopped

  web:
    build: ./web
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
      - api
    restart: unless-stopped
```

## Enterprise Integration

### API Gateway Integration

```yaml
# Kong configuration for LocalAI
services:
  - name: localai-chat
    url: http://localai:8080/v1/chat/completions
    routes:
      - name: chat-route
        paths:
          - /api/chat
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: request-transformer
        config:
          add:
            headers:
              - "Authorization:Bearer ${env.KONG_API_KEY}"

  - name: localai-images
    url: http://localai:8080/v1/images/generations
    routes:
      - name: images-route
        paths:
          - /api/images
    plugins:
      - name: rate-limiting
        config:
          minute: 20
```

### Monitoring Integration

```python
# Prometheus metrics integration
from prometheus_client import Counter, Histogram, generate_latest
import time

# Metrics
REQUEST_COUNT = Counter('localai_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('localai_request_duration_seconds', 'Request duration', ['method'])

def monitor_requests(app):
    """Add monitoring to FastAPI app."""

    @app.middleware("http")
    async def monitor_middleware(request, call_next):
        start_time = time.time()

        response = await call_next(request)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method
        ).observe(time.time() - start_time)

        return response

    @app.get("/metrics")
    def metrics():
        return generate_latest()

# Apply monitoring
monitor_requests(app)
```

## Best Practices

1. **Error Handling**: Implement comprehensive error handling and retries
2. **Rate Limiting**: Protect your LocalAI instance from abuse
3. **Caching**: Cache frequent queries to improve performance
4. **Logging**: Log all requests for debugging and analytics
5. **Health Checks**: Monitor LocalAI health and auto-restart if needed
6. **Resource Limits**: Set appropriate CPU/memory limits
7. **Security**: Use authentication and validate inputs
8. **Scaling**: Consider load balancing for high-traffic applications

LocalAI provides a powerful platform for building AI applications with complete local control and OpenAI compatibility. These integration patterns enable you to build sophisticated AI applications while maintaining privacy and avoiding cloud API costs. 