---
layout: default
title: "Ollama Tutorial - Chapter 6: Performance & Hardware Tuning"
nav_order: 6
has_children: false
parent: Ollama Tutorial
---

# Chapter 6: Performance, GPU Tuning, and Quantization

> Get faster, more reliable inference by tuning hardware usage, context, and sampling.

## Key Performance Levers

- **Model size/quantization**: smaller quants run faster (Q3/Q4) but lower quality
- **Context window (`num_ctx`)**: larger contexts use more RAM/VRAM
- **Batching (`num_batch`)**: more tokens processed per step (improves throughput)
- **GPU offload**: move layers to GPU for big speedups
- **Threads (`num_thread`)**: match physical cores for CPU-bound runs

## Recommended Settings by Hardware

| Hardware | Suggested Quant | Tips |
|----------|-----------------|------|
| 8–16 GB RAM, CPU-only | Q3_K, Q4_K_M | `num_ctx 2048-4096`, smaller models (phi3:mini) |
| Apple M1/M2/M3 | Q4_K_M | GPU offload auto; keep `num_ctx <= 4096` for speed |
| NVIDIA 8–12 GB | Q4_K_M / Q5_K | Set `num_gpu` to auto; use `mistral`, `llama3:8b` |
| NVIDIA 24 GB+ | Q5_K / Q6_K | Larger ctx (8k), bigger models (llama3:70b) |

## Runtime Options (API `options`)

```json
{
  "num_ctx": 4096,
  "num_predict": 512,
  "num_thread": 8,
  "num_batch": 512,
  "temperature": 0.4,
  "top_p": 0.9,
  "repeat_penalty": 1.1
}
```

- `num_thread`: CPU threads; set to physical cores
- `num_batch`: tokens per forward pass (higher = faster if memory allows)
- `num_gpu`: layers to offload (auto-detected; override if needed)
- `low_vram`: reduces GPU memory use at cost of speed

## GPU Offload

- Default behavior: Ollama auto-detects GPU and offloads layers
- Override per request: `"num_gpu": 20` (approx. layers to GPU)
- For multi-GPU: set `OLLAMA_NUM_GPU` (per docs) or run multiple instances pinning devices

## Quantization Choices

- **Q2_K / Q3_K**: fastest, smallest memory, quality drop
- **Q4_K_M**: balanced default
- **Q5_K_M / Q6_K**: better quality, more memory
- Prefer high-quality quants for reasoning; low quants for draft/utility tasks

## Context Management

- Keep `num_ctx` aligned with model capacity (many community builds are 4k/8k)
- Truncate conversation history when near limit
- For long docs, chunk + RAG instead of huge contexts

## Profiling & Benchmarks

```bash
ollama run mistral "test" --verbose   # shows timing
```
- Compare models/quants on the same prompt
- Measure tokens/sec; adjust `num_batch`, `num_thread`

## Stability Tips

- Reduce `num_batch` if you see OOM
- Lower `num_ctx` for memory savings
- Avoid very high `temperature` with low quants (may increase instability)
- Keep GPU drivers up to date; ensure `ollama serve` sees the GPU (`nvidia-smi`)

## Example Performance Profiles

**Fast utility (CPU-only):**
```json
"options": {"temperature": 0.2, "num_ctx": 2048, "num_batch": 256, "repeat_penalty": 1.1}
```

**Quality-focused (GPU 24 GB):**
```json
"options": {"temperature": 0.5, "num_ctx": 8192, "num_batch": 1024, "num_gpu": 40, "repeat_penalty": 1.05}
```

**Coding assistant (balanced):**
```json
"options": {"temperature": 0.2, "top_p": 0.9, "num_ctx": 4096, "repeat_penalty": 1.15}
```

Next: integrate Ollama with popular frameworks and tools.
