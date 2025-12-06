---
layout: default
title: "Ollama Tutorial - Chapter 8: Production Deployment"
nav_order: 8
has_children: false
parent: Ollama Tutorial
---

# Chapter 8: Production Deployment, Security, and Monitoring

> Run Ollama reliably in production with Docker, GPU support, security controls, and observability.

## Deployment Options

### Docker (CPU)
```bash
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama:latest
```

### Docker (NVIDIA GPU)
```bash
docker run -d --gpus all --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama:latest
```

### docker-compose
```yaml
version: "3.8"
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
volumes:
  ollama-data:
```

### Systemd (bare metal)
```ini
[Service]
ExecStart=/usr/local/bin/ollama serve
Restart=always
Environment=OLLAMA_HOST=0.0.0.0:11434
```

## Security & Access Control

- **Network exposure**: bind to localhost or place behind a reverse proxy (Nginx/Traefik)
- **Auth**: Ollama has no built-in auth; use proxy basic auth or an API gateway
- **TLS**: terminate TLS at proxy/load balancer
- **Model permissions**: restrict who can pull/run models via network ACLs
- **Resource limits**: cgroup/container limits to prevent OOM

Example Nginx snippet:
```nginx
location / {
  proxy_pass http://localhost:11434;
  auth_basic "Protected";
  auth_basic_user_file /etc/nginx/.htpasswd;
}
```

## Persistence & Backups

- Persist `~/.ollama/models` (or `/root/.ollama` in container) via volume
- Back up volumes regularly (models + Modelfiles)

## Monitoring & Observability

- **Logs**: `~/.ollama/logs` or container stdout
- **Health**: simple check `curl -f http://localhost:11434/api/tags`
- **Metrics**: not exposed natively; scrape logs or wrap API with custom metrics
- **Tracing**: front with gateway that emits request metrics (e.g., Envoy/NGINX + Prometheus)

## Scaling Patterns

- **Vertical first**: choose appropriate model sizes/quantization
- **Horizontal**: run multiple Ollama instances behind a load balancer; pin heavy models to specific nodes
- **Per-team instances**: isolate workloads and models
- **Caching**: reuse responses in your app layer; keep model set lean

## Performance Hardening

- Choose appropriate quant (Q4_K_M default; Q5/Q6 for quality, Q3 for speed)
- Set `num_ctx` to practical limits (4k–8k) to reduce memory
- Tune `num_batch`/`num_thread` for throughput; validate with tokens/sec
- Keep GPU drivers current; verify with `nvidia-smi`

## Cost & Resource Controls

- Prefer smaller models for routine tasks; reserve large models for premium flows
- Cap `num_predict` in API options to avoid runaway generations
- Use RAG to keep prompts small instead of huge contexts

## High-Availability Checklist

- Health checks on `/api/tags` or a lightweight chat probe
- Restart policy (`always`) and backoff
- Persistent volume for models
- Reverse proxy with auth + TLS
- Alert on downtime and high latency

## Example Production Stack

- **Ollama**: core LLM runtime
- **API Gateway**: Nginx/Traefik with auth & TLS
- **RAG Service**: Chroma/Qdrant + embeddings
- **App Layer**: your API/UI using OpenAI-compatible SDK
- **Monitoring**: Prometheus + Grafana (via gateway metrics) + logs

With these practices, you can operate Ollama safely in production, delivering local, private, and fast LLM capabilities to your applications.
