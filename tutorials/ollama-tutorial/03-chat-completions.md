---
layout: default
title: "Ollama Tutorial - Chapter 3: Chat & Completions"
nav_order: 3
has_children: false
parent: Ollama Tutorial
---

# Chapter 3: Chat, Completions, and Parameters

> Build chats and completions with streaming, JSON output, and safe parameter tuning.

## Chat Completions (OpenAI-Compatible)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Explain RAG in 3 bullets"}
  ]
}'
```

Python:
```python
import requests
resp = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3",
    "messages": [
        {"role": "system", "content": "You are concise."},
        {"role": "user", "content": "Summarize Ollama."}
    ]
})
print(resp.json()["message"]["content"])
```

Node (OpenAI client):
```javascript
import OpenAI from "openai";
const client = new OpenAI({ baseURL: "http://localhost:11434/v1", apiKey: "ollama" });
const chat = await client.chat.completions.create({
  model: "llama3",
  messages: [{ role: "user", content: "List 3 MLOps tools" }],
});
console.log(chat.choices[0].message.content);
```

## Streaming Responses

```bash
curl -N http://localhost:11434/api/chat -d '{
  "model": "mistral",
  "messages": [{"role": "user", "content": "Tell a short story"}],
  "stream": true
}'
```
Each chunk includes `message.content`. Stop tokens by client abort.

## Completions Endpoint (Legacy Style)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Write a haiku about databases",
  "stream": false
}'
```

## Parameters That Matter

- `temperature`: randomness (0.1 factual, 0.7 creative)
- `top_p`, `top_k`: sampling controls
- `repeat_penalty`: reduce repetition (1.05–1.2)
- `presence_penalty`, `frequency_penalty`: encourage topic diversity
- `num_ctx`: context window (e.g., 4096–8192 depending on model)
- `num_predict`: max new tokens

Example with options:
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "options": {
    "temperature": 0.3,
    "top_p": 0.9,
    "repeat_penalty": 1.1,
    "num_ctx": 4096,
    "num_predict": 256
  },
  "messages": [{"role": "user", "content": "Give me 5 bullet best practices for prompts"}]
}'
```

## Structured / JSON Output

Use a template or Modelfile with `FORMAT json`, and keep temperature low.
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [{
    "role": "user",
    "content": "Return JSON with fields: title, bullets (array of 3)."
  }],
  "options": {"temperature": 0.2}
}'
```

## Safety & Quality Tips

- Lower `temperature` for factual tasks
- Set `num_predict` to avoid runaways
- Use `repeat_penalty` ~1.1 to reduce loops
- Prefer chat format over raw prompt for clarity
- Include concise system messages to steer behavior

## Troubleshooting

- **Empty / short outputs**: increase `num_predict`; lower `repeat_penalty`
- **Hallucinations**: lower `temperature`; add system constraints; provide context
- **Slow responses**: use smaller model (phi3:mini); reduce `num_ctx`; ensure GPU is used

Next: generate embeddings and build simple RAG with Ollama.
