---
layout: default
title: "Chapter 3: LLM Provider Configuration"
nav_order: 3
parent: Devika Tutorial
---

# Chapter 3: LLM Provider Configuration

Welcome to **Chapter 3: LLM Provider Configuration**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter covers how to configure Claude 3, GPT-4, Gemini, Mistral, Groq, and local Ollama models in Devika's `config.toml` and how to select the right provider for each agent role.

## Learning Goals

- configure API keys and model identifiers for every supported LLM provider
- understand Devika's model selection mechanism and how to switch providers per project
- evaluate the cost, latency, and quality tradeoffs across providers for autonomous coding tasks
- configure Ollama for fully offline, local LLM operation without external API keys

## Fast Start Checklist

1. open `config.toml` and locate the `[API_KEYS]` and `[API_MODELS]` sections
2. add your API key for at least one cloud provider (Claude, OpenAI, Google, Mistral, or Groq)
3. set the model name for each provider section to a currently available model identifier
4. optionally install and start Ollama with a code-capable model for local operation

## Source References

- [Devika Configuration Section](https://github.com/stitionai/devika#configuration)
- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml)
- [Devika LLM Provider Source](https://github.com/stitionai/devika/tree/main/src/llm)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)

## Summary

You now know how to configure any of Devika's supported LLM providers, select the right model for each use case, and operate Devika in fully local mode using Ollama.

Next: [Chapter 4: Task Planning and Code Generation](04-task-planning-and-code-generation.md)

## Depth Expansion Playbook

<!-- depth-expansion-v2 -->

This chapter is expanded to v1-style depth for production-grade learning and implementation quality.

### Strategic Context

- tutorial: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- tutorial slug: **devika-tutorial**
- chapter focus: **Chapter 3: LLM Provider Configuration**
- system context: **Devika Agentic Software Engineer**
- objective: move from surface-level usage to repeatable engineering operation

### Architecture Decomposition

1. All LLM provider credentials are stored in the `[API_KEYS]` section of `config.toml`; the key names match the provider identifiers used in the `src/llm/` abstraction layer.
2. The `[API_MODELS]` section maps each provider to a specific model string; changing this value affects all agents that use that provider without requiring code changes.
3. Devika's LLM abstraction layer in `src/llm/` wraps each provider SDK (Anthropic, OpenAI, Google GenAI, Mistral, Groq, Ollama) behind a uniform `inference()` interface.
4. Claude 3 models (Haiku, Sonnet, Opus) are accessed via the Anthropic Python SDK; the model string format is `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, or `claude-3-opus-20240229`.
5. GPT-4 and GPT-4-turbo models are accessed via the OpenAI Python SDK; model strings follow the `gpt-4-turbo-preview` format.
6. Gemini models (Gemini Pro, Gemini Ultra) are accessed via the Google GenerativeAI SDK; the model string is `gemini-pro` or `gemini-ultra`.
7. Groq provides access to open-weight models (LLaMA, Mistral, Mixtral) via a fast inference API; model strings are provider-specific like `mixtral-8x7b-32768`.
8. Ollama runs local models such as `codellama`, `deepseek-coder`, or `mistral` on the developer's machine; the Ollama base URL in config.toml must point to the running Ollama server (default: `http://localhost:11434`).

### Operator Decision Matrix

| Decision Area | Low-Risk Path | High-Control Path | Tradeoff |
|:--------------|:--------------|:------------------|:---------|
| Primary provider | Claude 3 Sonnet (balanced quality/cost) | Claude 3 Opus (maximum reasoning quality) | cost vs output quality |
| Local vs cloud | cloud provider for reliability | Ollama for full offline/private operation | uptime vs data privacy |
| Model per agent | same model for all agents | different model per agent role | simplicity vs cost optimization |
| Context window | standard 4k-8k context models | 32k-100k context models for large codebases | cost vs completeness |
| Fallback strategy | no fallback | secondary provider fallback on rate limit | simplicity vs availability |

### Failure Modes and Countermeasures

| Failure Mode | Early Signal | Root Cause Pattern | Countermeasure |
|:-------------|:-------------|:-------------------|:---------------|
| Rate limit hit mid-task | `RateLimitError` or 429 response | sustained high-frequency API calls | add exponential backoff retry in the LLM abstraction layer |
| Model string not recognized | `InvalidModelError` or 404 from provider | deprecated or mistyped model identifier | verify model ID in provider documentation and update config.toml |
| Ollama model not pulled | connection refused or 404 from Ollama | model not downloaded to local Ollama instance | run `ollama pull <model-name>` before starting Devika |
| Context window exceeded | truncated output or provider error | generated context exceeds model's max tokens | switch to a larger context window model or reduce research chunk size |
| API quota exhausted | 429 with quota message | free tier or daily limit reached | upgrade provider plan or switch to an alternative provider temporarily |
| Provider SDK version mismatch | import error on startup | requirements.txt pinned to older SDK version than API supports | update SDK version in requirements.txt and re-run pip install |

### Implementation Runbook

1. Open `config.toml` and locate the `[API_KEYS]` section.
2. For Anthropic Claude: set `ANTHROPIC` to your Anthropic API key from console.anthropic.com.
3. For OpenAI GPT-4: set `OPENAI` to your OpenAI API key from platform.openai.com.
4. For Google Gemini: set `GOOGLE` to your Google AI API key from aistudio.google.com.
5. For Mistral: set `MISTRAL` to your Mistral API key from console.mistral.ai.
6. For Groq: set `GROQ` to your Groq API key from console.groq.com.
7. For Ollama: ensure `OLLAMA_API_BASE` is set to `http://localhost:11434` and run `ollama pull codellama` on your local machine.
8. Set the `[API_MODELS]` values to the specific model identifiers you want to use (e.g., `CLAUDE_3_MODEL = "claude-3-sonnet-20240229"`).
9. Restart the backend after any config.toml change and verify the provider is selected in the project creation UI dropdown.

### Quality Gate Checklist

- [ ] all configured API keys are valid and tested with a minimal ping request before task submission
- [ ] model identifiers in `[API_MODELS]` match currently available models from each provider's documentation
- [ ] Ollama server is running and the target model is pulled before using local LLM mode
- [ ] rate limit handling (retry with backoff) is implemented in the LLM abstraction layer
- [ ] config.toml is excluded from git via `.gitignore` and team secrets are managed via a secrets manager
- [ ] context window limits for each configured model are documented and input budgets are sized accordingly
- [ ] fallback provider logic is defined in the runbook if the primary provider is unavailable
- [ ] provider cost estimates per task are tracked to prevent unexpected billing surprises

### Source Alignment

- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml)
- [Devika Configuration Section](https://github.com/stitionai/devika#configuration)
- [Devika LLM Source Directory](https://github.com/stitionai/devika/tree/main/src/llm)
- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Supported Models List](https://github.com/stitionai/devika#supported-models)

### Cross-Tutorial Connection Map

- [LiteLLM Tutorial](../litellm-tutorial/) — unified LLM proxy that can sit in front of Devika's provider calls
- [Ollama Tutorial](../ollama-tutorial/) — deep dive on running local models that Devika can consume
- [OpenAI Python SDK Tutorial](../openai-python-sdk-tutorial/) — understanding the SDK Devika uses for GPT-4 calls
- [SWE-agent Tutorial](../swe-agent-tutorial/) — comparable model configuration patterns in another autonomous coding agent
- [Aider Tutorial](../aider-tutorial/) — single-agent coding tool with similar provider configuration surface

### Advanced Practice Exercises

1. Configure Devika with three different providers simultaneously and benchmark the same task across all three, measuring token cost, latency, and output quality.
2. Set up a local Ollama instance with `deepseek-coder:33b` and run a complete coding task end-to-end without any external API calls.
3. Implement a provider fallback mechanism in the LLM abstraction layer that switches from Claude to GPT-4 on a rate limit error.
4. Write a config validation script that reads config.toml and tests each configured provider with a minimal API call before Devika starts.
5. Set up a per-agent model configuration where the planner uses Claude 3 Opus for quality, the coder uses Claude 3 Sonnet for balance, and the internal monologue uses Claude 3 Haiku for speed.

### Review Questions

1. Where in config.toml are provider API keys stored and what section contains model name identifiers?
2. What is the Ollama base URL and what command must be run before using a local model with Devika?
3. How does Devika's LLM abstraction layer allow switching providers without changing agent code?
4. What happens if the configured model identifier is deprecated and no longer available from the provider?
5. Why is context window size a critical consideration when choosing models for Devika's coder agent on large codebases?

### Scenario Playbook 1: Switching From Claude to GPT-4 Mid-Project

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: Anthropic API has elevated latency; team needs to continue task execution with minimal disruption
- initial hypothesis: switching provider in config.toml and restarting the backend should redirect all subsequent calls to GPT-4
- immediate action: update `ANTHROPIC` key to leave intact and set `CLAUDE_3_MODEL` blank; ensure `OPENAI` key and `GPT4_MODEL` are set
- engineering control: select GPT-4 in the project settings dropdown in the UI before resubmitting tasks
- verification target: backend logs show calls routing to OpenAI endpoint instead of Anthropic
- rollback trigger: GPT-4 output quality diverges significantly from Claude baseline; revert provider selection
- communication step: notify team of temporary provider switch and expected quality differences in Slack
- learning capture: document provider switching procedure in the operations runbook with timing and quality notes

### Scenario Playbook 2: Ollama Local Model Has Wrong Context Window

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: local Ollama task fails or produces truncated code on projects with many files
- initial hypothesis: the pulled Ollama model has a smaller context window than the research and plan context requires
- immediate action: check the model card for the Ollama model's context window size and compare with actual context usage in logs
- engineering control: switch to `codellama:34b` or a model with explicit 16k+ context; set `num_ctx` parameter in Ollama model options
- verification target: coder agent receives full research context without truncation for benchmark tasks
- rollback trigger: larger context model is too slow for interactive use; fall back to cloud provider
- communication step: update the Ollama model recommendations in the setup guide with context window requirements
- learning capture: add a startup check that warns if the configured Ollama model's context window is below the minimum recommended size

### Scenario Playbook 3: Groq Rate Limit on Batch Tasks

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: multiple parallel tasks hit Groq's tokens-per-minute limit simultaneously
- initial hypothesis: Groq's free tier TPM limit is much lower than cloud providers; concurrent tasks exceed the quota
- immediate action: add sequential queuing for tasks using Groq to prevent concurrent execution
- engineering control: implement exponential backoff with jitter in the Groq LLM client; log rate limit events
- verification target: task queue processes all items without errors when TPM limit is respected
- rollback trigger: sequential queuing makes task throughput unacceptably slow for the team
- communication step: inform team of Groq rate limits and recommend upgrading to a paid plan for higher throughput
- learning capture: add TPM budget tracking per provider and alert when 80% of limit is consumed per minute

### Scenario Playbook 4: Google Gemini API Key Invalid After Rotation

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tasks using Gemini fail with authentication error after a scheduled key rotation
- initial hypothesis: config.toml still contains the old Gemini API key that was revoked
- immediate action: generate a new key in Google AI Studio, update config.toml, and restart the backend
- engineering control: integrate config.toml secrets with a secrets manager (e.g., AWS Secrets Manager or HashiCorp Vault) so key rotation updates config automatically
- verification target: Gemini provider returns successful response on the next task submission after backend restart
- rollback trigger: new key has restricted scopes that don't cover the Generative Language API
- communication step: notify team of key rotation and estimated downtime window; update rotation schedule documentation
- learning capture: automate config.toml secret injection from the secrets manager in the deployment pipeline

### Scenario Playbook 5: Mistral Model Identifier Deprecated

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: task fails with a 404 model-not-found error from Mistral's API
- initial hypothesis: the model string in config.toml references a model name that Mistral has removed or renamed
- immediate action: check the Mistral model availability endpoint and update the model string to the current identifier
- engineering control: add a model availability check to the startup sequence that validates each configured model against the provider's model list API
- verification target: provider model validation passes for all configured providers on each backend startup
- rollback trigger: model list API call itself fails due to network issues; fall back to documentation-based verification
- communication step: post a note to the engineering channel when model identifiers are updated and why
- learning capture: pin model identifier versions with a comment on the expected deprecation date in config.toml

### What Problem Does This Solve?

Devika's multi-provider configuration model solves the vendor lock-in and cost optimization problem for autonomous coding teams. Different LLM providers excel at different tasks — Claude 3 Opus produces superior reasoning for complex planning, Groq provides ultrafast inference for lightweight monologue steps, and Ollama enables fully private operation without any data leaving the local machine. Without a clean provider abstraction and a single config file, teams would need to modify agent code to switch providers, making experimentation and cost optimization impractical.

### How it Works Under the Hood

1. On backend startup, Devika reads `config.toml` and initializes a provider client for each section where an API key is present.
2. The `src/llm/` abstraction layer wraps each provider SDK with a uniform `LLM.inference(prompt, model)` interface.
3. When an agent invokes the LLM, it passes the selected model identifier; the abstraction layer routes to the correct provider client based on the model prefix.
4. Provider-specific error handling (rate limits, authentication errors, context overflow) is caught in the abstraction layer and either retried or surfaced to the orchestrator.
5. For Ollama, the Ollama Python client sends requests to the local server URL configured in `OLLAMA_API_BASE`.
6. The project creation UI reads the available configured providers from the backend and presents them as a model selection dropdown.

### Source Walkthrough

- [Devika config.example.toml](https://github.com/stitionai/devika/blob/main/config.example.toml) — Why it matters: the authoritative template showing every provider key and model configuration option.
- [Devika LLM Directory](https://github.com/stitionai/devika/tree/main/src/llm) — Why it matters: the provider abstraction layer source showing how each SDK is wrapped uniformly.
- [Devika README Configuration](https://github.com/stitionai/devika#configuration) — Why it matters: the quickstart guide to filling in config.toml for a first working setup.
- [Devika README Supported Models](https://github.com/stitionai/devika#supported-models) — Why it matters: the official list of tested and supported model identifiers per provider.

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Architecture and Agent Pipeline](02-architecture-and-agent-pipeline.md)
- [Next Chapter: Chapter 4: Task Planning and Code Generation](04-task-planning-and-code-generation.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)

### Scenario Playbook 1: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 2: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 3: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 4: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 5: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 6: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 7: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 8: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 9: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 10: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 11: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 12: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 13: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 14: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 15: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 16: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 17: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 18: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 19: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 20: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 21: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 22: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 23: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 24: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 25: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: incoming request volume spikes after release
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: introduce adaptive concurrency limits and queue bounds
- verification target: latency p95 and p99 stay within defined SLO windows
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 26: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: tool dependency latency increases under concurrency
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: enable staged retries with jitter and circuit breaker fallback
- verification target: error budget burn rate remains below escalation threshold
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 27: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: schema updates introduce incompatible payloads
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: pin schema versions and add compatibility shims
- verification target: throughput remains stable under target concurrency
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 28: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: environment parity drifts between staging and production
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: restore environment parity via immutable config promotion
- verification target: retry volume stays bounded without feedback loops
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 29: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: access policy changes reduce successful execution rates
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: re-scope credentials and rotate leaked or stale keys
- verification target: data integrity checks pass across write/read cycles
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests

### Scenario Playbook 30: Chapter 3: LLM Provider Configuration

- tutorial context: **Devika Tutorial: Open-Source Autonomous AI Software Engineer**
- trigger condition: background jobs accumulate and exceed processing windows
- initial hypothesis: identify the smallest reproducible failure boundary
- immediate action: protect user-facing stability before optimization work
- engineering control: activate degradation mode to preserve core user paths
- verification target: audit logs capture all control-plane mutations
- rollback trigger: pre-defined quality gate fails for two consecutive checks
- communication step: publish incident status with owner and ETA
- learning capture: add postmortem and convert findings into automated tests
