---
layout: default
title: "Ollama Tutorial - Chapter 7: Integrations"
nav_order: 7
has_children: false
parent: Ollama Tutorial
---

# Chapter 7: Integrations with OpenAI API, LangChain, and LlamaIndex

> Use Ollama with common AI frameworks and OpenAI-compatible SDKs.

## OpenAI-Compatible SDKs

Set `baseURL` to Ollama and supply any API key (not enforced by Ollama).

**Python (openai package):**
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

resp = client.chat.completions.create(
    model="llama3",
    messages=[{"role": "user", "content": "Give me 3 bullet tips on prompts"}],
)
print(resp.choices[0].message.content)
```

**Node:**
```javascript
import OpenAI from "openai";
const client = new OpenAI({ baseURL: "http://localhost:11434/v1", apiKey: "ollama" });
const r = await client.chat.completions.create({
  model: "mistral",
  messages: [{ role: "user", content: "Summarize RAG in 2 lines" }],
});
console.log(r.choices[0].message.content);
```

## LangChain

**Python:**
```python
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

llm = Ollama(model="llama3", base_url="http://localhost:11434")
prompt = PromptTemplate.from_template("Explain {topic} in 3 bullets")
print((prompt | llm).invoke({"topic": "vector databases"}))
```

**Chat + Streaming:**
```python
from langchain_community.chat_models import ChatOllama
chat = ChatOllama(model="mistral", base_url="http://localhost:11434", streaming=True)
for chunk in chat.stream([("user", "Write a short poem")]):
    print(chunk.content, end="", flush=True)
```

**Node (LangChainJS):**
```javascript
import { ChatOllama } from "@langchain/community/chat_models/ollama";
const chat = new ChatOllama({ model: "llama3", baseUrl: "http://localhost:11434" });
const res = await chat.invoke(["Explain embeddings in 2 bullets"]);
console.log(res.content);
```

## LlamaIndex

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

llm = Ollama(model="llama3", request_timeout=120)
embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Build index
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents, llm=llm, embed_model=embed_model)

query_engine = index.as_query_engine()
print(query_engine.query("What is Ollama?"))
```

## LiteLLM / OpenAI-Compatible Clients

- Set `base_url=http://localhost:11434/v1`
- Use any `api_key`

Example (curl):
```bash
curl http://localhost:11434/v1/models
```

## Other Integrations

- **FastAPI / Flask**: point your OpenAI client to Ollama base URL
- **RAG stacks**: use Ollama embeddings + Chroma/Qdrant/Pinecone
- **Automation**: n8n/Make/Zapier via HTTP nodes hitting Ollama API

## Tips

- Keep `model` names consistent across services
- Tune `num_ctx` and sampling options per integration
- For streaming UIs, ensure your framework reads Server-Sent Events (SSE) or streamed chunks

Next: production deployment, Docker, security, and monitoring.
