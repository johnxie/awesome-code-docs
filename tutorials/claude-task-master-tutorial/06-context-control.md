---
layout: default
title: "Claude Task Master - Chapter 6: Context & Grounding"
nav_order: 6
has_children: false
parent: Claude Task Master Tutorial
---

# Chapter 6: Context Management & Grounding

> Keep Claude focused with system prompts, tight context windows, and source-grounded answers.

## System Prompts for Control

Craft concise, strict system messages:
```text
You are a senior software engineer. Be concise. Cite sources when provided. If unsure, say so.
```
Guidelines:
- Be explicit about role and scope
- Set safety/formatting expectations
- Instruct to cite sources or say “not sure” when missing info

## Context Windows & Summaries

Claude 3 models have large contexts, but you should still:
- **Summarize** long histories regularly (keep bullets of key decisions)
- **Windowing**: keep last N turns + a compact running summary
- **Strip fluff**: remove greetings, filler, unrelated tangents

Example summary policy:
- Every 10 messages: summarize in 5 bullets
- Keep a “facts” section and a “todo/decisions” section

## Source Grounding

Provide source text and demand citations:
```text
Use only the provided sources. If an answer isn’t in the sources, say “not enough info”.

Sources:
[1] README extract: ...
[2] API docs: ...
Question: ...
```

Ask for explicit citations:
```text
Answer with numbered citations like [1], [2]. If no source supports it, say so.
```

## JSON / Structured Outputs

For deterministic automation, prefer JSON:
```text
Return JSON:
{
  "summary": "...",
  "tasks": ["..."],
  "risk": "low|medium|high"
}
```
Set `temperature` low (0.1–0.3) and include an example if critical.

## Guardrails & Refusals

- State disallowed topics (secrets, PII, exploits)
- Instruct to refuse and log when asked for them
- Keep refusal template short and consistent

Refusal template:
```text
I can’t help with that. (Reason)
```

## Prompt Hygiene Checklist

- Single authoritative system prompt
- Remove conflicting instructions from user context
- Keep examples short and relevant
- Set max length expectations (e.g., “3 bullets”)
- Add “don’t guess; say not sure”

## Evaluation Loop

- Create test prompts (edge cases, adversarial)
- Check for hallucinations (absence of citation when required)
- Track token use: shorter context → cheaper, faster

## Example: Grounded Q&A Node

```json
{
  "model": "claude-3-sonnet-20240229",
  "prompt": """
You are a precise assistant. Use only the sources.
Sources:
[1] {{ $json.doc1 }}
[2] {{ $json.doc2 }}
Question: {{ $json.question }}

Rules:
- Answer with citations [1], [2]
- If not in sources, say "Not enough info"
- Be concise (3-5 sentences)
""",
  "temperature": 0.2
}
```

## Best Practices

- Summarize often; keep context lean
- Demand citations; reward “not enough info” when gaps exist
- Use JSON for automation paths
- Lower temperature for accuracy
- Periodically evaluate with a fixed test set

Next: add workflow automation and CI hooks for consistent results.
