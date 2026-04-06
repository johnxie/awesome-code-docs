<div align="center">

```
   ___                                         ______          __        ____
  / _ |_    _____ ___  ___  __ _  ___          / ____/___  ____/ /__     / __ \____  __________
 / __ | |/|/ / -_|_-< / _ \/  ' \/ -_)        / /   / __ \/ __  / _ \   / / / / __ \/ ___/ ___/
/_/ |_|__,__/\__/___/ \___/_/_/_/\__/        / /___/ /_/ / /_/ /  __/  / /_/ / /_/ / /__(__  )
                                              \____/\____/\__,_/\___/  /_____/\____/\___/____/
```

**Deep-dive tutorials for the world's most popular open-source projects**

*Learn how complex systems actually work — not just what they do*

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![GitHub stars](https://img.shields.io/github/stars/johnxie/awesome-code-docs?style=social)](https://github.com/johnxie/awesome-code-docs)
[![Tutorials](https://img.shields.io/badge/tutorials-191-brightgreen.svg)](#-tutorial-catalog)
[![Sources](https://img.shields.io/badge/source%20repos-191%2F191%20verified-brightgreen.svg)](discoverability/tutorial-source-verification.md)
[![Content Hours](https://img.shields.io/badge/content-2000%2B%20hours-orange.svg)](#-tutorial-catalog)
[![Last Updated](https://img.shields.io/github/last-commit/johnxie/awesome-code-docs?label=updated)](https://github.com/johnxie/awesome-code-docs/commits/main)

[**Browse Tutorials**](#-tutorial-catalog) · [**A-Z Directory**](discoverability/tutorial-directory.md) · [**Query Hub**](discoverability/query-hub.md) · [**Intent Map**](discoverability/search-intent-map.md) · [**Market Signals**](discoverability/trending-vibe-coding.md) · [**Learning Paths**](#-learning-paths) · [**Contributing**](#-contributing) · [**Community**](#-community)

</div>

---

## Why This Exists

Most documentation tells you *what* to do. These tutorials explain *how* and *why* complex systems work under the hood — with architecture diagrams, real code walkthroughs, and production-grade patterns.

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│    📖 Typical Docs          vs.     🔬 Awesome Code Docs    │
│    ─────────────                    ─────────────────────    │
│    "Run this command"               "Here's the pipeline     │
│    "Use this API"                    architecture that makes │
│    "Set this config"                 this work, the design   │
│                                      tradeoffs, and how to   │
│                                      extend it yourself"     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Every tutorial follows a consistent 8-chapter structure:

| Chapter | Focus |
|:--------|:------|
| **1. Getting Started** | Installation, first run, project structure |
| **2. Architecture** | System design, data flow, core abstractions |
| **3-5. Core Systems** | Deep dives into the 3 most important subsystems |
| **6. Extensibility** | Plugins, custom components, APIs |
| **7. Advanced** | Performance, customization, internals |
| **8. Production** | Deployment, monitoring, scaling, security |

Each chapter includes **Mermaid architecture diagrams**, **annotated code examples** from the real codebase, and **summary tables** for quick reference.

---

## 🔎 Find Tutorials by Goal

Use this quick-start map if you searched for a specific outcome.

| Search Intent | Start Here | Then Go To |
|:--------------|:-----------|:-----------|
| open-source vibe coding tools | [Cline](tutorials/cline-tutorial/) | [Roo Code](tutorials/roo-code-tutorial/) → [OpenCode](tutorials/opencode-tutorial/) → [Sweep](tutorials/sweep-tutorial/) → [Tabby](tutorials/tabby-tutorial/) → [Stagewise](tutorials/stagewise-tutorial/) → [bolt.diy](tutorials/bolt-diy-tutorial/) → [VibeSDK](tutorials/vibesdk-tutorial/) → [HAPI](tutorials/hapi-tutorial/) → [Kiro](tutorials/kiro-tutorial/) |
| spec-driven AI delivery workflows | [OpenSpec](tutorials/openspec-tutorial/) | [Claude Task Master](tutorials/claude-task-master-tutorial/) → [Codex CLI](tutorials/codex-cli-tutorial/) → [OpenCode](tutorials/opencode-tutorial/) → [Kiro](tutorials/kiro-tutorial/) |
| build AI agents in production | [LangChain](tutorials/langchain-tutorial/) | [LangGraph](tutorials/langgraph-tutorial/) → [CrewAI](tutorials/crewai-tutorial/) → [OpenHands](tutorials/openhands-tutorial/) → [Claude Flow](tutorials/claude-flow-tutorial/) → [Devika](tutorials/devika-tutorial/) → [BabyAGI](tutorials/babyagi-tutorial/) |
| autonomous AI software engineers | [OpenHands](tutorials/openhands-tutorial/) | [Devika](tutorials/devika-tutorial/) → [SWE-agent](tutorials/swe-agent-tutorial/) → [Aider](tutorials/aider-tutorial/) |
| task-driven autonomous agents | [BabyAGI](tutorials/babyagi-tutorial/) | [AutoGen](tutorials/autogen-tutorial/) → [CrewAI](tutorials/crewai-tutorial/) → [LangGraph](tutorials/langgraph-tutorial/) |
| build RAG systems | [LlamaIndex](tutorials/llamaindex-tutorial/) | [Haystack](tutorials/haystack-tutorial/) → [RAGFlow](tutorials/ragflow-tutorial/) |
| run LLMs locally or at scale | [Ollama](tutorials/ollama-tutorial/) | [llama.cpp](tutorials/llama-cpp-tutorial/) → [vLLM](tutorials/vllm-tutorial/) → [LiteLLM](tutorials/litellm-tutorial/) |
| build AI apps with TypeScript/Next.js | [Vercel AI SDK](tutorials/vercel-ai-tutorial/) | [CopilotKit](tutorials/copilotkit-tutorial/) → [LobeChat](tutorials/lobechat-tutorial/) |
| taskade ai / genesis / mcp workflows | [Taskade](tutorials/taskade-tutorial/) | [Taskade Docs](tutorials/taskade-docs-tutorial/) → [Taskade MCP](tutorials/taskade-mcp-tutorial/) → [Taskade Awesome Vibe Coding](tutorials/taskade-awesome-vibe-coding-tutorial/) → [MCP Servers](tutorials/mcp-servers-tutorial/) |
| build MCP tools and integrations | [MCP Python SDK](tutorials/mcp-python-sdk-tutorial/) | [FastMCP](tutorials/fastmcp-tutorial/) → [MCP Servers](tutorials/mcp-servers-tutorial/) → [MCP Quickstart Resources](tutorials/mcp-quickstart-resources-tutorial/) → [Create Python Server](tutorials/create-python-server-tutorial/) → [MCP Docs Repo](tutorials/mcp-docs-repo-tutorial/) → [Create TypeScript Server](tutorials/create-typescript-server-tutorial/) → [Awesome MCP Servers](tutorials/awesome-mcp-servers-tutorial/) → [Composio](tutorials/composio-tutorial/) → [Daytona](tutorials/daytona-tutorial/) → [GenAI Toolbox](tutorials/genai-toolbox-tutorial/) → [awslabs/mcp](tutorials/awslabs-mcp-tutorial/) → [MCP Inspector](tutorials/mcp-inspector-tutorial/) → [MCP Registry](tutorials/mcp-registry-tutorial/) → [MCP Specification](tutorials/mcp-specification-tutorial/) → [MCP TypeScript SDK](tutorials/mcp-typescript-sdk-tutorial/) → [MCP Go SDK](tutorials/mcp-go-sdk-tutorial/) → [MCP Rust SDK](tutorials/mcp-rust-sdk-tutorial/) → [MCP Java SDK](tutorials/mcp-java-sdk-tutorial/) → [MCP C# SDK](tutorials/mcp-csharp-sdk-tutorial/) → [MCP Swift SDK](tutorials/mcp-swift-sdk-tutorial/) → [MCP Kotlin SDK](tutorials/mcp-kotlin-sdk-tutorial/) → [MCP Ruby SDK](tutorials/mcp-ruby-sdk-tutorial/) → [MCP PHP SDK](tutorials/mcp-php-sdk-tutorial/) → [MCP Ext Apps](tutorials/mcp-ext-apps-tutorial/) → [MCPB](tutorials/mcpb-tutorial/) → [use-mcp](tutorials/use-mcp-tutorial/) → [MCP Use](tutorials/mcp-use-tutorial/) → [MCP Chrome](tutorials/mcp-chrome-tutorial/) → [Firecrawl MCP Server](tutorials/firecrawl-mcp-server-tutorial/) |

---

## 🧭 Navigation UX Layer

To reduce context-switching and dead ends:

- every tutorial index now includes a **Navigation & Backlinks** block
- each block links back to the main catalog, A-Z directory, query hub, and category hubs
- chapter 1 entry links are pinned so readers can jump directly into each track

Quick jump links:

- [Tutorials Workspace Guide](tutorials/README.md)
- [A-Z Tutorial Directory](discoverability/tutorial-directory.md)
- [Query Hub](discoverability/query-hub.md)
- [Search Intent Map](discoverability/search-intent-map.md)
- [Category Hubs](#category-hubs)

---

## ✅ Source Verification Status

All tutorial indexes were re-verified against referenced upstream GitHub repositories on **2026-03-20**:

- tutorials scanned: **191**
- tutorials with source repos: **191**
- tutorials with unverified source repos: **0**
- unique verified source repos: **201**

Verification artifacts:

- [Tutorial Source Verification Report](discoverability/tutorial-source-verification.md)
- [Tutorial Source Verification JSON](discoverability/tutorial-source-verification.json)
- verification script: [`scripts/verify_tutorial_sources.py`](scripts/verify_tutorial_sources.py)

---

## 🧬 Taskade Ecosystem Snapshot (Verified 2026-03-21)

Live repository snapshot for high-intent Taskade/Genesis/AI/MCP searches.

| Taskade Repo | Stars | Last Push | Tutorial Coverage |
|:-------------|------:|:----------|:------------------|
| [`taskade/mcp`](https://github.com/taskade/mcp) | 116+ | 2026-02-13 | [Taskade MCP Tutorial](tutorials/taskade-mcp-tutorial/) |
| [`taskade/docs`](https://github.com/taskade/docs) | 11+ | 2026-03-16 | [Taskade Docs Tutorial](tutorials/taskade-docs-tutorial/) |
| [`taskade/awesome-vibe-coding`](https://github.com/taskade/awesome-vibe-coding) | 8+ | 2026-03-21 | [Taskade Awesome Vibe Coding Tutorial](tutorials/taskade-awesome-vibe-coding-tutorial/) |
| [`taskade/taskade`](https://github.com/taskade/taskade) | 9+ | 2026-02-25 | [Taskade Tutorial](tutorials/taskade-tutorial/) |
| [`taskade/temporal-parser`](https://github.com/taskade/temporal-parser) | 2+ | 2026-02-12 | [Taskade Tutorial (Ecosystem radar)](tutorials/taskade-tutorial/) |

---

<!-- BEGIN: TRENDING_VIBE_CODING -->
## 📈 Trending Vibe-Coding Repos (Auto-updated 2026-04-06)

Live GitHub market signals for high-impact open-source coding-agent and vibe-coding ecosystems with direct tutorial coverage.

| Ecosystem Repo | Tutorial | Stars | Last Push | Why It Matters |
|:---------------|:---------|------:|:----------|:---------------|
| [`anomalyco/opencode`](https://github.com/anomalyco/opencode) | [OpenCode Tutorial](tutorials/opencode-tutorial/) | 137,974 | 2026-04-06 (0d ago) | terminal-native coding agent with strong provider and tool controls |
| [`open-webui/open-webui`](https://github.com/open-webui/open-webui) | [Open WebUI Tutorial](tutorials/open-webui-tutorial/) | 130,255 | 2026-04-03 (3d ago) | self-hosted AI interface and model operations |
| [`browser-use/browser-use`](https://github.com/browser-use/browser-use) | [Browser Use Tutorial](tutorials/browser-use-tutorial/) | 86,189 | 2026-04-06 (0d ago) | browser-native AI automation and agent execution |
| [`daytonaio/daytona`](https://github.com/daytonaio/daytona) | [Daytona Tutorial](tutorials/daytona-tutorial/) | 71,406 | 2026-04-06 (0d ago) | sandbox infrastructure for secure AI code execution |
| [`cline/cline`](https://github.com/cline/cline) | [Cline Tutorial](tutorials/cline-tutorial/) | 59,937 | 2026-04-06 (0d ago) | agentic coding with terminal, browser, and MCP workflows |
| [`Mintplex-Labs/anything-llm`](https://github.com/Mintplex-Labs/anything-llm) | [AnythingLLM Tutorial](tutorials/anything-llm-tutorial/) | 57,737 | 2026-04-05 (1d ago) | self-hosted RAG workspaces and agent workflows |
| [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec) | [OpenSpec Tutorial](tutorials/openspec-tutorial/) | 37,531 | 2026-04-05 (1d ago) | spec-driven workflow layer for predictable AI-assisted delivery |
| [`TabbyML/tabby`](https://github.com/TabbyML/tabby) | [Tabby Tutorial](tutorials/tabby-tutorial/) | 33,304 | 2026-03-02 (35d ago) | self-hosted coding assistant platform for teams |
| [`continuedev/continue`](https://github.com/continuedev/continue) | [Continue Tutorial](tutorials/continue-tutorial/) | 32,315 | 2026-04-06 (0d ago) | IDE-native AI coding assistant architecture |
| [`vercel/ai`](https://github.com/vercel/ai) | [Vercel AI SDK Tutorial](tutorials/vercel-ai-tutorial/) | 23,279 | 2026-04-05 (1d ago) | production TypeScript AI app and agent SDK patterns |
| [`RooCodeInc/Roo-Code`](https://github.com/RooCodeInc/Roo-Code) | [Roo Code Tutorial](tutorials/roo-code-tutorial/) | 22,996 | 2026-04-06 (0d ago) | multi-mode coding agents and approval workflows |
| [`dyad-sh/dyad`](https://github.com/dyad-sh/dyad) | [Dyad Tutorial](tutorials/dyad-tutorial/) | 20,066 | 2026-04-03 (3d ago) | local-first AI app generation workflows |
| [`stackblitz-labs/bolt.diy`](https://github.com/stackblitz-labs/bolt.diy) | [bolt.diy Tutorial](tutorials/bolt-diy-tutorial/) | 19,229 | 2026-02-07 (58d ago) | open-source Bolt-style product builder stack |
| [`sweepai/sweep`](https://github.com/sweepai/sweep) | [Sweep Tutorial](tutorials/sweep-tutorial/) | 7,707 | 2025-09-18 (200d ago) | issue-to-PR coding agent workflows and GitHub automation |
| [`stagewise-io/stagewise`](https://github.com/stagewise-io/stagewise) | [Stagewise Tutorial](tutorials/stagewise-tutorial/) | 6,516 | 2026-04-06 (0d ago) | browser-context frontend coding agent workflows |
| [`cloudflare/vibesdk`](https://github.com/cloudflare/vibesdk) | [VibeSDK Tutorial](tutorials/vibesdk-tutorial/) | 4,928 | 2026-03-31 (6d ago) | Cloudflare-native prompt-to-app platform architecture |

Data source: GitHub REST API (`stargazers_count`, `pushed_at`) via `scripts/refresh_market_signals.py`.
<!-- END: TRENDING_VIBE_CODING -->
## 📚 Tutorial Catalog

```
 ╔════════════════════════════════════════════════════════════╗
 ║  🤖  AI & AGENTS  │  🔧  DEV TOOLS  │  🗄️  DATA  │  🎤 SPEECH  ║
 ║   70+ tutorials    │   46 tutorials  │  14 tutorials │  3 tutorials  ║
 ╚════════════════════════════════════════════════════════════╝
```

### Category Hubs

| Hub | Focus |
|:----|:------|
| [AI & ML Platforms](categories/ai-ml-platforms.md) | agents, RAG, coding assistants, vibe coding, and LLM operations |
| [Databases & Storage](categories/databases-storage.md) | data systems, search engines, query planning, and knowledge platforms |
| [Systems Programming](categories/systems-programming.md) | runtime internals, infrastructure patterns, and architecture mechanics |
| [Web Frameworks](categories/web-frameworks.md) | AI application frameworks, chat stacks, and modern full-stack architecture |

### 🤖 AI Agents & Multi-Agent Systems

Build autonomous AI systems that reason, plan, and collaborate.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[LangChain](tutorials/langchain-tutorial/)** | 100K+ | Python | Chains, agents, RAG, prompt engineering |
| **[LangGraph](tutorials/langgraph-tutorial/)** | 8K+ | Python | Stateful multi-actor graphs, cycles, persistence |
| **[CrewAI](tutorials/crewai-tutorial/)** | 24K+ | Python | Role-based agent teams, task delegation |
| **[AG2](tutorials/ag2-tutorial/)** | 40K+ | Python | Community successor to AutoGen, multi-agent conversations |
| **[AutoGen](tutorials/autogen-tutorial/)** | 40K+ | Python | Conversable agents, group chat, tool integration |
| **[OpenAI Swarm](tutorials/swarm-tutorial/)** | 18K+ | Python | Lightweight agent handoffs, routines |
| **[Smolagents](tutorials/smolagents-tutorial/)** | 14K+ | Python | Hugging Face code agents, tool calling |
| **[Phidata](tutorials/phidata-tutorial/)** | 17K+ | Python | Autonomous agents with memory and tools |
| **[Pydantic AI](tutorials/pydantic-ai-tutorial/)** | 5K+ | Python | Type-safe agent development |
| **[AgentGPT](tutorials/agentgpt-tutorial/)** | 32K+ | Python | Autonomous task planning and execution |
| **[SuperAGI](tutorials/superagi-tutorial/)** | 16K+ | Python | Production autonomous agent framework |
| **[ElizaOS](tutorials/elizaos-tutorial/)** | 17K+ | TypeScript | Multi-agent AI with character system |
| **[OpenClaw](tutorials/openclaw-tutorial/)** | 119K+ | TypeScript | Personal AI assistant, multi-channel |
| **[Deer Flow](tutorials/deer-flow-tutorial/)** | 32.1K+ | Python | Research agent workflows |
| **[Letta](tutorials/letta-tutorial/)** | 14K+ | Python | Stateful agents with long-term memory |
| **[Anthropic Skills](tutorials/anthropic-skills-tutorial/)** | 59K+ | Python/TypeScript | Reusable AI agent capabilities, MCP integration |
| **[Claude Flow](tutorials/claude-flow-tutorial/)** | 14.0K+ | TypeScript | Multi-agent orchestration, MCP server operations, and V2-V3 migration tradeoffs |
| **[Devika](tutorials/devika-tutorial/)** | 19.5K+ | Python | AI software engineer agents, planning pipeline, and production governance |
| **[BabyAGI](tutorials/babyagi-tutorial/)** | 18K+ | Python | Task-driven autonomous agent patterns, memory, and BabyAGI 2o/3 evolution |
| **[AgenticSeek](tutorials/agenticseek-tutorial/)** | 25.4K+ | Python | Local-first autonomous agent with multi-agent planning, browsing, and coding workflows |
| **[Agno](tutorials/agno-tutorial/)** | 38.3K+ | Python | Multi-agent systems with memory, orchestration, and AgentOS runtime |
| **[AutoAgent](tutorials/autoagent-tutorial/)** | 8.6K+ | Python | Zero-code agent creation through natural-language workflows |
| **[ADK Python](tutorials/adk-python-tutorial/)** | 18.1K+ | Python | Production-grade agent engineering with Google's Agent Development Kit |
| **[Qwen-Agent](tutorials/qwen-agent-tutorial/)** | 13.5K+ | Python | Tool-enabled agent framework with MCP, RAG, and multi-modal workflows |
| **[Strands Agents](tutorials/strands-agents-tutorial/)** | 5.2K+ | Python | Model-driven agents with native MCP, hooks, and deployment patterns |
| **[PocketFlow](tutorials/pocketflow-tutorial/)** | 10.1K+ | Python | Minimal LLM framework with graph-based workflows, multi-agent patterns, and RAG |
| **[Mastra](tutorials/mastra-tutorial/)** | 21.6K+ | TypeScript | AI agents and workflows with memory and MCP tooling |
| **[Mini-SWE-Agent](tutorials/mini-swe-agent-tutorial/)** | 3.1K+ | Python | Minimal autonomous code agent design with benchmark-oriented workflows |
| **[SWE-agent](tutorials/swe-agent-tutorial/)** | 18.6K+ | Python | Autonomous repository repair and benchmark-driven software engineering loops |
| **[Open SWE](tutorials/open-swe-tutorial/)** | 5.3K+ | Python | Async cloud coding agent architecture and migration playbook |
| **[HumanLayer](tutorials/humanlayer-tutorial/)** | 9.6K+ | Python | Context engineering and human-governed coding-agent workflows |
| **[Wshobson Agents](tutorials/wshobson-agents-tutorial/)** | 29.9K+ | TypeScript | Pluginized multi-agent workflows with specialist Claude Code agents |
| **[MetaGPT](tutorials/metagpt-tutorial/)** | 66K+ | Python | Multi-agent framework with role-based collaboration (PM, Architect, Engineer) for software generation |
| **[A2A Protocol](tutorials/a2a-protocol-tutorial/)** | 23K+ | Python/TypeScript | Google's Agent-to-Agent protocol for cross-platform agent interoperability and discovery |
| **[OpenAI Agents](tutorials/openai-agents-tutorial/)** | 20K+ | Python | Official OpenAI multi-agent SDK with handoffs, guardrails, and streaming |

### 🧠 LLM Frameworks & RAG

Retrieval-augmented generation, model serving, and LLM tooling.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[LlamaIndex](tutorials/llamaindex-tutorial/)** | 38K+ | Python | Data connectors, indexing, query engines |
| **[Haystack](tutorials/haystack-tutorial/)** | 18K+ | Python | Pipeline-based search and RAG |
| **[DSPy](tutorials/dspy-tutorial/)** | 20K+ | Python | Declarative LLM programming, optimizers |
| **[Instructor](tutorials/instructor-tutorial/)** | 10K+ | Python | Structured output extraction with Pydantic |
| **[Outlines](tutorials/outlines-tutorial/)** | 10K+ | Python | Constrained LLM generation |
| **[Chroma](tutorials/chroma-tutorial/)** | 16K+ | Python | AI-native embedding database |
| **[LanceDB](tutorials/lancedb-tutorial/)** | 5K+ | Python/Rust | Serverless vector database |
| **[RAGFlow](tutorials/ragflow-tutorial/)** | 30K+ | Python | Document-aware RAG engine |
| **[Quivr](tutorials/quivr-tutorial/)** | 37K+ | Python | Second brain with RAG |
| **[Mem0](tutorials/mem0-tutorial/)** | 24K+ | Python | Intelligent memory layer for AI |
| **[HuggingFace](tutorials/huggingface-tutorial/)** | 145K+ | Python | Transformers, model hub, training and inference |
| **[Semantic Kernel](tutorials/semantic-kernel-tutorial/)** | 23K+ | C#/Python | Microsoft's AI orchestration SDK |
| **[Fabric](tutorials/fabric-tutorial/)** | 26K+ | Go/Python | AI prompt pattern framework |
| **[Langflow](tutorials/langflow-tutorial/)** | 145K+ | Python/React | Visual AI agent and workflow platform with flow composition, APIs, and MCP deployment |
| **[Crawl4AI](tutorials/crawl4ai-tutorial/)** | 62K+ | Python | LLM-friendly web crawler for RAG pipelines with markdown generation and structured extraction |

### 🖥️ LLM Infrastructure & Serving

Run, serve, and manage LLMs in production.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Ollama](tutorials/ollama-tutorial/)** | 110K+ | Go | Local LLM serving, model management |
| **[llama.cpp](tutorials/llama-cpp-tutorial/)** | 73K+ | C++ | High-performance local inference |
| **[vLLM](tutorials/vllm-tutorial/)** | 38K+ | Python | PagedAttention, continuous batching |
| **[LiteLLM](tutorials/litellm-tutorial/)** | 15K+ | Python | Unified API gateway for 100+ LLMs |
| **[LocalAI](tutorials/localai-tutorial/)** | 27K+ | Go | Self-hosted multi-modal AI |
| **[Open WebUI](tutorials/open-webui-tutorial/)** | 60K+ | Python/Svelte | Self-hosted ChatGPT alternative |
| **[LLaMA-Factory](tutorials/llama-factory-tutorial/)** | 40K+ | Python | Unified LLM fine-tuning framework |
| **[BentoML](tutorials/bentoml-tutorial/)** | 7K+ | Python | ML model serving and deployment |
| **[Langfuse](tutorials/langfuse-tutorial/)** | 8K+ | TypeScript | LLM observability and tracing |

### 💬 Chat & AI Applications

Full-stack AI chat platforms and copilots.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[LobeChat](tutorials/lobechat-tutorial/)** | 71K+ | Next.js | Modern AI chat, plugins, theming |
| **[Dify](tutorials/dify-tutorial/)** | 60K+ | Python/React | Visual LLM app builder |
| **[Flowise](tutorials/flowise-tutorial/)** | 35K+ | Node.js/React | Visual LLM workflow orchestration |
| **[CopilotKit](tutorials/copilotkit-tutorial/)** | 15K+ | React/TypeScript | In-app AI copilots |
| **[Chatbox](tutorials/chatbox-tutorial/)** | 24K+ | JavaScript/React | Multi-provider chat client |
| **[Vercel AI SDK](tutorials/vercel-ai-tutorial/)** | 21K+ | TypeScript | AI-powered React/Next.js apps |
| **[Perplexica](tutorials/perplexica-tutorial/)** | 19K+ | TypeScript | AI-powered search engine |
| **[SillyTavern](tutorials/sillytavern-tutorial/)** | 9K+ | Node.js | Advanced roleplay chat platform |
| **[Khoj](tutorials/khoj-tutorial/)** | 18K+ | Python/Django | Self-hosted AI personal assistant |
| **[Botpress](tutorials/botpress-tutorial/)** | 13K+ | Node.js | Enterprise chatbot platform |
| **[AnythingLLM](tutorials/anything-llm-tutorial/)** | 30K+ | Node.js | All-in-one AI desktop app |
| **[GPT-OSS](tutorials/gpt-oss-tutorial/)** | 6.4K+ | TypeScript | Open-source GPT implementation |
| **[Claude Quickstarts](tutorials/claude-quickstarts-tutorial/)** | 13.7K+ | Python/TypeScript | Production Claude integration patterns |
| **[Cherry Studio](tutorials/cherry-studio-tutorial/)** | 40.5K+ | TypeScript | Multi-provider AI desktop workspace with assistants, documents, and MCP tools |
| **[AFFiNE](tutorials/affine-tutorial/)** | 66K+ | TypeScript | Open-source Notion + Miro alternative with docs, whiteboards, databases, and AI copilot |
| **[Plane](tutorials/plane-tutorial/)** | 47K+ | Python/TypeScript | AI-native project management with issues, cycles, modules, wiki, and AI features |

### 🔧 Developer Tools & Productivity

AI coding assistants, build systems, and dev infrastructure.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Continue](tutorials/continue-tutorial/)** | 22K+ | TypeScript | Open-source AI coding assistant |
| **[Cline](tutorials/cline-tutorial/)** | 58K+ | TypeScript/VS Code | Agentic coding with terminal, browser, MCP tools |
| **[Roo Code](tutorials/roo-code-tutorial/)** | 22K+ | TypeScript/VS Code | Multi-mode coding agents with checkpoints and MCP |
| **[OpenCode](tutorials/opencode-tutorial/)** | 103.2K+ | Go/TypeScript | Terminal-native coding agent architecture, provider routing, and tool safety controls |
| **[Sweep](tutorials/sweep-tutorial/)** | 7.6K+ | Python/GitHub | Issue-to-PR coding agent workflow with config-driven governance and CI feedback loops |
| **[Tabby](tutorials/tabby-tutorial/)** | 32.9K+ | Rust/TypeScript | Self-hosted code completion and answer platform with editor-agent integrations |
| **[Stagewise](tutorials/stagewise-tutorial/)** | 6.5K+ | TypeScript/CLI | Frontend coding agent proxy with browser context selection, bridge mode, and plugin runtime |
| **[OpenSpec](tutorials/openspec-tutorial/)** | 23.8K+ | TypeScript/CLI | Spec-driven artifact workflow for planning, implementation, validation, and archive governance |
| **[bolt.diy](tutorials/bolt-diy-tutorial/)** | 19K+ | TypeScript/Remix | Open-source Bolt-style AI app builder |
| **[Cloudflare VibeSDK](tutorials/vibesdk-tutorial/)** | 4.7K+ | TypeScript/Cloudflare | Build and operate a cloud-native vibe-coding platform |
| **[HAPI](tutorials/hapi-tutorial/)** | 1.4K+ | TypeScript/CLI | Remote control and approval workflows for local coding agents |
| **[Kiro](tutorials/kiro-tutorial/)** | 3.2K+ | TypeScript/AWS | Spec-driven AI IDE with steering files, hooks, and MCP-native agent workflows |
| **[Daytona](tutorials/daytona-tutorial/)** | 55.3K+ | Go/TypeScript/Python | Secure sandbox infrastructure for AI-generated code and coding-agent execution |
| **[OpenHands](tutorials/openhands-tutorial/)** | 67K+ | Python | AI software engineering agent |
| **[Aider](tutorials/aider-tutorial/)** | 25K+ | Python | AI pair programming in terminal |
| **[Claude Code](tutorials/claude-code-tutorial/)** | 80.7K+ | TypeScript | Anthropic's AI coding CLI |
| **[Anthropic API](tutorials/anthropic-code-tutorial/)** | 1.7K+ | Python/TypeScript | Claude API integration, tool use, streaming |
| **[Claude Task Master](tutorials/claude-task-master-tutorial/)** | 26K+ | TypeScript | AI-powered task management |
| **[CopilotKit](tutorials/copilotkit-tutorial/)** | 15K+ | React | In-app AI assistants |
| **[Nanocoder](tutorials/nanocoder-tutorial/)** | 1.5K+ | TypeScript | AI coding agent internals |
| **[Codex Analysis](tutorials/codex-analysis-tutorial/)** | 108.2K+ | TypeScript | Static analysis platform and LSP architecture |
| **[Turborepo](tutorials/turborepo-tutorial/)** | 27K+ | Rust | High-performance monorepo builds |
| **[n8n AI](tutorials/n8n-ai-tutorial/)** | 52K+ | Node.js | Visual AI workflow automation |
| **[Activepieces](tutorials/activepieces-tutorial/)** | 20.8K+ | TypeScript | Open-source automation platform, custom pieces, and admin governance |
| **[Taskade](tutorials/taskade-tutorial/)** | 10+ | AI/Productivity | AI-native workspace workflows, Genesis app building, and production rollout patterns |
| **[Taskade Docs](tutorials/taskade-docs-tutorial/)** | 10+ | Docs/GitBook | Documentation architecture, API coverage, release timelines, and docs governance for Taskade |
| **[Taskade MCP](tutorials/taskade-mcp-tutorial/)** | 108+ | TypeScript/MCP | Official Taskade MCP server operations, OpenAPI codegen, and multi-client integration |
| **[Taskade Awesome Vibe Coding](tutorials/taskade-awesome-vibe-coding-tutorial/)** | 5+ | Curated List | High-signal tool selection and governance across Genesis, coding agents, and MCP stacks |
| **[Browser Use](tutorials/browser-use-tutorial/)** | 10K+ | Python | AI-powered browser automation |
| **[ComfyUI](tutorials/comfyui-tutorial/)** | 65K+ | Python | Node-based AI art workflows |
| **[MCP Python SDK](tutorials/mcp-python-sdk-tutorial/)** | 21.4K+ | Python | Building MCP servers and tool integrations |
| **[FastMCP](tutorials/fastmcp-tutorial/)** | 22.8K+ | Python | MCP server/client framework, transports, and integration workflows |
| **[MCP Servers](tutorials/mcp-servers-tutorial/)** | 77.6K+ | Multi-lang | Reference MCP server implementations |
| **[MCP Quickstart Resources](tutorials/mcp-quickstart-resources-tutorial/)** | 984+ | Multi-lang | Official cross-language weather server and client quickstart corpus with smoke tests and protocol helpers |
| **[Create Python Server](tutorials/create-python-server-tutorial/)** | 476+ | Python/uv | Archived official scaffold tool for bootstrapping MCP Python servers with template-driven resources/prompts/tools |
| **[MCP Docs Repo](tutorials/mcp-docs-repo-tutorial/)** | 424+ | Docs/MDX | Archived official MCP documentation repository with migration guidance to canonical docs in `modelcontextprotocol/modelcontextprotocol` |
| **[Create TypeScript Server](tutorials/create-typescript-server-tutorial/)** | 172+ | TypeScript/CLI | Archived official TypeScript scaffold tool for generating MCP server projects with resources/tools/prompts templates |
| **[Awesome MCP Servers](tutorials/awesome-mcp-servers-tutorial/)** | 80.7K+ | Curated List | MCP server discovery, evaluation, and operations |
| **[Composio](tutorials/composio-tutorial/)** | 26.5K+ | Python/TypeScript | Agent toolkit integration, auth, providers, and MCP patterns |
| **[GenAI Toolbox](tutorials/genai-toolbox-tutorial/)** | 12.9K+ | Go/Node/Python | MCP-first database tools, `tools.yaml` control plane, and connector operations |
| **[awslabs/mcp](tutorials/awslabs-mcp-tutorial/)** | 8.1K+ | Python | Official AWS MCP server ecosystem, role composition, and governance controls |
| **[MCP Inspector](tutorials/mcp-inspector-tutorial/)** | 8.6K+ | TypeScript/Node | MCP server debugging across UI and CLI with auth/session and transport controls |
| **[MCP Registry](tutorials/mcp-registry-tutorial/)** | 6.4K+ | Go | Registry publication, discovery API consumption, and governance operations |
| **[MCP Specification](tutorials/mcp-specification-tutorial/)** | 7.1K+ | Spec/MDX | Protocol lifecycle, transports, authorization, security model, and governance workflows from the canonical MCP spec |
| **[MCP TypeScript SDK](tutorials/mcp-typescript-sdk-tutorial/)** | 11.6K+ | TypeScript | Client/server split packages, transport strategy, and v1-to-v2 migration planning |
| **[MCP Go SDK](tutorials/mcp-go-sdk-tutorial/)** | 3.8K+ | Go | Official Go client/server SDK patterns, auth middleware, transport operations, and conformance workflows |
| **[MCP Rust SDK](tutorials/mcp-rust-sdk-tutorial/)** | 3.0K+ | Rust | Official rmcp SDK architecture, macro-driven tooling, OAuth support, and async task-oriented runtime patterns |
| **[MCP Java SDK](tutorials/mcp-java-sdk-tutorial/)** | 3.2K+ | Java | Official Java SDK module architecture, reactive transport layers, Spring integrations, and conformance loops |
| **[MCP C# SDK](tutorials/mcp-csharp-sdk-tutorial/)** | 3.9K+ | C#/.NET | Official .NET SDK package layering, ASP.NET Core transport patterns, filters, and task workflows |
| **[MCP Swift SDK](tutorials/mcp-swift-sdk-tutorial/)** | 1.2K+ | Swift | Official Swift MCP client/server setup, sampling controls, batching, and lifecycle-focused runtime operation patterns |
| **[MCP Kotlin SDK](tutorials/mcp-kotlin-sdk-tutorial/)** | 1.3K+ | Kotlin/KMP | Official Kotlin multiplatform MCP SDK with typed core/client/server modules, capability checks, and transport integrations |
| **[MCP Ruby SDK](tutorials/mcp-ruby-sdk-tutorial/)** | 700+ | Ruby | Official Ruby MCP server/client SDK with streamable HTTP sessions, schema-aware primitives, notifications, and release workflows |
| **[MCP PHP SDK](tutorials/mcp-php-sdk-tutorial/)** | 1.3K+ | PHP | Official PHP MCP SDK with attribute discovery, server builder composition, schema controls, and stdio/HTTP transport patterns |
| **[MCP Ext Apps](tutorials/mcp-ext-apps-tutorial/)** | 1.4K+ | TypeScript/Spec | Official MCP Apps extension SDK/spec for interactive UI resources, host bridges, security constraints, and migration workflows |
| **[MCPB](tutorials/mcpb-tutorial/)** | 1.7K+ | TypeScript/CLI | Official MCP bundle packaging format and CLI workflows for manifest authoring, packing, signing, and verification |
| **[use-mcp](tutorials/use-mcp-tutorial/)** | 1.0K+ | TypeScript/React | Archived official React hook for MCP auth, connection lifecycle, and tool/resource/prompt client integration patterns |
| **[MCP Use](tutorials/mcp-use-tutorial/)** | 9.1K+ | Python/TypeScript | Full-stack MCP agents, clients, servers, and inspector workflows across both runtimes |
| **[MCP Chrome](tutorials/mcp-chrome-tutorial/)** | 10.4K+ | TypeScript/Chrome Extension | Real-browser MCP automation with native messaging, network tooling, and semantic tab search |
| **[Firecrawl MCP Server](tutorials/firecrawl-mcp-server-tutorial/)** | 5.5K+ | TypeScript/Node | Official MCP web scraping/search server with retries, versioned endpoints, and multi-client integration paths |
| **[OpenAI Python SDK](tutorials/openai-python-sdk-tutorial/)** | 29.8K+ | Python | GPT API, embeddings, assistants, batch processing |
| **[tiktoken](tutorials/tiktoken-tutorial/)** | 17.1K+ | Python/Rust | Token counting, encoding, cost optimization |

#### Terminal Coding Agents

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[GitHub Copilot CLI](tutorials/copilot-cli-tutorial/)** | 8.9K+ | TypeScript | Copilot agent workflows in the terminal with GitHub context and approval controls |
| **[Gemini CLI](tutorials/gemini-cli-tutorial/)** | 96.2K+ | TypeScript | Terminal-first agent workflows with tooling, MCP extensibility, and headless automation |
| **[Crush](tutorials/crush-tutorial/)** | 20.7K+ | Go/TypeScript | Multi-model terminal coding agent with LSP/MCP integrations and strong controls |
| **[Kimi CLI](tutorials/kimi-cli-tutorial/)** | 6.9K+ | TypeScript | Multi-mode terminal agent with MCP and ACP connectivity |
| **[Mistral Vibe](tutorials/mistral-vibe-tutorial/)** | 3.3K+ | TypeScript | Minimal CLI coding agent with profiles, skills, subagents, and ACP support |
| **[Goose](tutorials/goose-tutorial/)** | 32.1K+ | Python | Extensible open-source coding agent with controlled tool execution and provider flexibility |
| **[gptme](tutorials/gptme-tutorial/)** | 4.2K+ | Python | Local-first terminal agent with extensible tools and automation-friendly modes |
| **[Kilo Code](tutorials/kilocode-tutorial/)** | 16.1K+ | TypeScript | Agentic engineering across IDE and CLI surfaces with multi-mode control loops |
| **[Plandex](tutorials/plandex-tutorial/)** | 15K+ | TypeScript | Large-task coding workflows with strong context management and cumulative diff review |
| **[Codex CLI](tutorials/codex-cli-tutorial/)** | 62.7K+ | Rust/TypeScript | Local terminal agent workflows with sandbox, auth, MCP, and policy controls |

#### Multi-Agent Orchestration

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Claude Squad](tutorials/claude-squad-tutorial/)** | 6.2K+ | Bash/Tmux | Multi-agent terminal session orchestration across isolated workspaces |
| **[Superset Terminal](tutorials/superset-terminal-tutorial/)** | 3.3K+ | TypeScript | Command center for parallel coding agents with centralized monitoring |
| **[Vibe Kanban](tutorials/vibe-kanban-tutorial/)** | 22.2K+ | TypeScript | Multi-agent orchestration board for Claude Code, Codex, Gemini CLI, and more |
| **[CodeMachine CLI](tutorials/codemachine-cli-tutorial/)** | 2.3K+ | Python | Long-running coding-agent workflows with multi-agent coordination and context control |

#### IDE & Visual Interfaces

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Onlook](tutorials/onlook-tutorial/)** | 24.8K+ | TypeScript/React | Visual-first AI coding for Next.js and Tailwind with repo-backed edits |
| **[Opcode](tutorials/opcode-tutorial/)** | 20.7K+ | TypeScript/Electron | GUI command center for Claude Code sessions, agents, and MCP servers |
| **[Shotgun](tutorials/shotgun-tutorial/)** | 625+ | TypeScript | Spec-driven development workflows for large coding changes |
| **[tldraw](tutorials/tldraw-tutorial/)** | 46K+ | TypeScript | Infinite canvas SDK with AI "make-real" feature for generating apps from whiteboard sketches |
| **[Appsmith](tutorials/appsmith-tutorial/)** | 39K+ | TypeScript/Java | Low-code internal tool builder with drag-and-drop UI, 25+ data connectors, and Git sync |
| **[Windmill](tutorials/windmill-tutorial/)** | 16K+ | TypeScript/Rust | Scripts to webhooks, workflows, and UIs — open-source Retool + Temporal alternative |
| **[E2B](tutorials/e2b-tutorial/)** | 11K+ | Python/TypeScript | Secure cloud sandboxes for AI agent code execution with sub-200ms cold start |

#### Memory, Skills & Context

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Cipher](tutorials/cipher-tutorial/)** | 3.5K+ | TypeScript | Shared memory layer for coding agents across IDEs, tools, and teams |
| **[Claude-Mem](tutorials/claude-mem-tutorial/)** | 32.3K+ | Python | Persistent memory compression and retrieval for Claude Code |
| **[Beads](tutorials/beads-tutorial/)** | 17.9K+ | Python | Git-backed task graph memory for structured coding-agent planning |
| **[Planning with Files](tutorials/planning-with-files-tutorial/)** | 15K+ | Markdown/CLI | Persistent file-based planning workflows for coding agents |
| **[Context7](tutorials/context7-tutorial/)** | 47.4K+ | TypeScript | Live version-aware documentation context for coding agents |
| **[OpenSrc](tutorials/opensrc-tutorial/)** | 1K+ | TypeScript | Deep source-code context retrieval for implementation-level agent reasoning |
| **[Serena](tutorials/serena-tutorial/)** | 20.9K+ | Python | Semantic code retrieval toolkit for coding agents on large codebases |
| **[AGENTS.md](tutorials/agents-md-tutorial/)** | 18.4K+ | Markdown | Portable repository guidance standard for coding agents |
| **[Claude Code Router](tutorials/claude-code-router-tutorial/)** | 28.8K+ | TypeScript | Multi-provider routing and control plane for Claude Code |
| **[Claude Plugins Official](tutorials/claude-plugins-official-tutorial/)** | 8.8K+ | TypeScript | Managed plugin directory and contribution standards for Claude Code |
| **[Compound Engineering Plugin](tutorials/compound-engineering-plugin-tutorial/)** | 9.7K+ | TypeScript | Compound engineering workflows across Claude Code and other toolchains |
| **[Everything Claude Code](tutorials/everything-claude-code-tutorial/)** | 57K+ | Markdown | Production configuration patterns for Claude Code agents, hooks, and skills |
| **[Awesome Claude Code](tutorials/awesome-claude-code-tutorial/)** | 25.8K+ | Curated List | High-signal Claude Code resources, commands, hooks, and workflows |
| **[Awesome Claude Skills](tutorials/awesome-claude-skills-tutorial/)** | 39.6K+ | Curated List | Discovery and evaluation of reusable Claude skills for coding workflows |
| **[OpenSkills](tutorials/openskills-tutorial/)** | 8.7K+ | TypeScript | Universal skill loading across Claude Code, Cursor, Codex, and Aider |
| **[Refly](tutorials/refly-tutorial/)** | 6.9K+ | TypeScript | Deterministic agent skills delivered through API, webhook, and CLI surfaces |

#### MCP Servers & Integrations

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Figma Context MCP](tutorials/figma-context-mcp-tutorial/)** | 13.3K+ | TypeScript | Design-to-code context for higher-fidelity coding-agent implementation |
| **[Chrome DevTools MCP](tutorials/chrome-devtools-mcp-tutorial/)** | 27.2K+ | TypeScript | Browser automation, tracing, and deep debugging for coding agents |
| **[Playwright MCP](tutorials/playwright-mcp-tutorial/)** | 28K+ | TypeScript | Structured browser automation through MCP with deterministic actions |
| **[GitHub MCP Server](tutorials/github-mcp-server-tutorial/)** | 27.4K+ | Go | GitHub operations through MCP for repos, issues, PRs, Actions, and security workflows |

#### Legacy & Migration

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[OpenCode AI Legacy](tutorials/opencode-ai-legacy-tutorial/)** | 11.2K+ | TypeScript | Archived terminal agent workflows and migration guidance to newer tooling |

### 🗄️ Databases, Knowledge & Analytics

Data platforms, knowledge management, and observability.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Supabase](tutorials/supabase-tutorial/)** | 75K+ | PostgreSQL/TypeScript | Realtime DB, auth, edge functions |
| **[PostHog](tutorials/posthog-tutorial/)** | 23K+ | Python/TypeScript | Product analytics, feature flags |
| **[NocoDB](tutorials/nocodb-tutorial/)** | 50K+ | Node.js/Vue | Open-source Airtable alternative |
| **[Teable](tutorials/teable-tutorial/)** | 15K+ | TypeScript/PostgreSQL | Multi-dimensional data platform |
| **[SiYuan](tutorials/siyuan-tutorial/)** | 25K+ | Go/TypeScript | Privacy-first knowledge management |
| **[Logseq](tutorials/logseq-tutorial/)** | 34K+ | ClojureScript | Local-first knowledge graph |
| **[OpenBB](tutorials/openbb-tutorial/)** | 35K+ | Python | Open-source financial terminal |
| **[Athens Research](tutorials/athens-research-tutorial/)** | 6.3K+ | ClojureScript | Graph-based knowledge system |
| **[Obsidian Outliner](tutorials/obsidian-outliner-tutorial/)** | 1.3K+ | TypeScript | Obsidian plugin architecture |
| **[ClickHouse](tutorials/clickhouse-tutorial/)** | 39K+ | C++ | Column-oriented analytics DB |
| **[PostgreSQL Planner](tutorials/postgresql-tutorial/)** | 20.4K+ | C | Query planning internals |
| **[MeiliSearch](tutorials/meilisearch-tutorial/)** | 48K+ | Rust | Lightning-fast search engine |
| **[PhotoPrism](tutorials/photoprism-tutorial/)** | 36K+ | Go | AI-powered photo management |
| **[Liveblocks](tutorials/liveblocks-tutorial/)** | 4K+ | TypeScript | Real-time collaboration infra |
| **[Fireproof](tutorials/fireproof-tutorial/)** | 950+ | JavaScript | Local-first document database with encrypted sync and React hooks |

### ⚙️ Systems & Infrastructure

Low-level systems, cloud native, and infrastructure patterns.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Kubernetes Operators](tutorials/kubernetes-operator-tutorial/)** | 7.6K+ | Go | Production-grade K8s operator patterns |
| **[React Fiber](tutorials/react-fiber-tutorial/)** | 244.1K+ | JavaScript | React reconciler internals |
| **[Dyad](tutorials/dyad-tutorial/)** | 19K+ | TypeScript | Local AI app development |
| **[LangChain Architecture](tutorials/langchain-architecture-tutorial/)** | 130.4K+ | Python | LangChain deep architecture guide |
| **[n8n MCP](tutorials/n8n-mcp-tutorial/)** | 180.2K+ | TypeScript | Model Context Protocol with n8n |
| **[Firecrawl](tutorials/firecrawl-tutorial/)** | 22K+ | Python | LLM-ready web data extraction |

### 🎤 Speech & Multimodal AI

Voice recognition, audio processing, and multimodal AI applications.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[OpenAI Whisper](tutorials/openai-whisper-tutorial/)** | 93.9K+ | Python | Speech-to-text, translation, multilingual ASR |
| **[Whisper.cpp](tutorials/whisper-cpp-tutorial/)** | 37K+ | C++ | Speech recognition on edge devices |
| **[OpenAI Realtime Agents](tutorials/openai-realtime-agents-tutorial/)** | 6.7K+ | TypeScript | Voice-first AI agents with WebRTC |

---

## 🗺️ Learning Paths

```
 ┌─────────────────────────────────────────────────────────────┐
 │                    CHOOSE YOUR PATH                         │
 │                                                             │
 │  🟢 Beginner    Start here if you're new to AI/ML          │
 │  🟡 Builder     Ready to build production applications      │
 │  🔴 Architect   Designing systems at scale                  │
 └─────────────────────────────────────────────────────────────┘
```

### 🟢 Path 1: AI Fundamentals

> *"I want to understand how AI applications work"*

```
Ollama ──→ LangChain ──→ Chroma ──→ Open WebUI
 (run       (build        (store      (deploy a
  LLMs       chains)       vectors)    full app)
  locally)
```

### 🟡 Path 2: Agent Builder

> *"I want to build autonomous AI agents"*

```
LangChain ──→ LangGraph ──→ CrewAI ──→ AutoGen/AG2 ──→ Langfuse
 (basics)      (stateful     (teams)    (multi-agent    (monitor
                graphs)                  orchestration)  in prod)
```

### 🟡 Path 3: RAG Engineer

> *"I want to build retrieval-augmented generation systems"*

```
LlamaIndex ──→ Haystack ──→ DSPy ──→ RAGFlow ──→ vLLM
 (indexing &    (pipeline    (optimize  (document   (serve at
  retrieval)     search)      prompts)   processing)  scale)
```

### 🟡 Path 4: Full-Stack AI

> *"I want to build AI-powered web applications"*

```
Vercel AI ──→ CopilotKit ──→ LobeChat ──→ Supabase ──→ n8n
 (AI SDK       (in-app        (full chat   (database    (workflow
  basics)       copilots)       platform)    + auth)      automation)
```

### 🔴 Path 5: LLM Infrastructure

> *"I want to run and scale LLMs in production"*

```
llama.cpp ──→ vLLM ──→ LiteLLM ──→ BentoML ──→ K8s Operators
 (local         (GPU     (unified    (model      (orchestrate
  inference)     serving)  gateway)    packaging)   at scale)
```

### 🔴 Path 6: AI Coding Tools

> *"I want to understand how AI coding assistants work"*

```
Continue ──→ Sweep ──→ OpenHands ──→ OpenCode ──→ Tabby ──→ Stagewise ──→ OpenSpec ──→ Kiro
 (code         (issue      (AI SWE      (terminal        (self-hosted     (frontend       (spec-driven   (spec-driven
  completion)   to PR)      agent)       coding agent)    assistant)       browser agent)  delivery)      AI IDE)
```

### 🔴 Path 7: Autonomous AI Engineers

> *"I want to build and understand autonomous software engineering agents"*

```
OpenHands ──→ Devika ──→ SWE-agent ──→ Mini SWE-agent ──→ Aider ──→ BabyAGI
 (multi-agent   (planning    (SWE bench    (lightweight         (pair         (task-driven
  OS layer)      pipeline)    framework)    agent core)          programming)   autonomy)
```

**Duration:** 30-45 hours | **Difficulty:** Advanced

### 🟡 Path 8: MCP Mastery

> *"I want to build AI tool servers and extend Claude with custom capabilities"*

```
MCP Python SDK ──→ FastMCP ──→ MCP Servers ──→ MCP Quickstart Resources ──→ Create Python Server ──→ MCP Docs Repo ──→ Create TypeScript Server ──→ Awesome MCP Servers ──→ Composio ──→ Daytona ──→ GenAI Toolbox ──→ awslabs/mcp ──→ MCP Inspector ──→ MCP Registry ──→ MCP Specification ──→ MCP TypeScript SDK ──→ MCP Go SDK ──→ MCP Rust SDK ──→ MCP Java SDK ──→ MCP C# SDK ──→ MCP Swift SDK ──→ MCP Kotlin SDK ──→ MCP Ruby SDK ──→ MCP PHP SDK ──→ MCP Ext Apps ──→ MCPB ──→ use-mcp ──→ MCP Use ──→ MCP Chrome ──→ Firecrawl MCP Server
 (build             (build servers      (reference        (multi-lang             (python scaffold        (archived docs        (typescript scaffold      (discovery and          (tool + auth   (sandbox        (db-focused           (aws server          (debug +            (publish +           (protocol             (client/server         (go sdk +            (rust rmcp +         (java sdk +          (csharp sdk +         (swift sdk +          (kmp core +            (ruby server +          (php server +          (interactive ui +      (bundle pack +         (react hook +         (full-stack          (chrome native +      (web scrape +
  servers)           fast)               implementations)  quickstart set)         bootstrap path)         migration map)        bootstrap path)          curation)               runtime)       infra)          mcp control plane)    ecosystem)           transport tests)     discovery ops)        contract deep dive)    sdk internals)         conformance)          task/oauth focus)      spring modules)        aspnet filters)        lifecycle controls)    transport model)        client workflow)        discovery model)        host bridge model)      sign verify)            archived guidance)      mcp workflows)        semantic tabs)        search/crawl)
```

**Duration:** 100-135 hours | **Difficulty:** Intermediate to Advanced

### 🟢 Path 9: Speech & Voice AI

> *"I want to build voice-first AI applications"*

```
OpenAI Whisper ──→ Whisper.cpp ──→ OpenAI Realtime Agents ──→ Voice Apps
 (Python ASR,       (edge            (voice-first             (production
  fine-tuning)       deployment)       conversations)           voice apps)
```

**Duration:** 25-35 hours | **Difficulty:** Intermediate

### 🟡 Path 10: OpenAI Ecosystem

> *"I want to master OpenAI's tools and APIs"*

```
OpenAI Python SDK ──→ tiktoken ──→ OpenAI Whisper ──→ Realtime Agents
 (core API,          (token         (speech              (voice
  embeddings,         optimization)  recognition)         agents)
  assistants)
```

**Duration:** 35-45 hours | **Difficulty:** Beginner to Intermediate

### 🔴 Path 11: Vibe Coding Platforms

> *"I want to build and operate vibe-coding stacks end to end"*

```
Dyad ──→ bolt.diy ──→ Stagewise ──→ Cline ──→ Roo Code ──→ VibeSDK ──→ HAPI
 (local      (OSS app      (frontend      (IDE        (multi-mode    (cloud         (remote
  builder)    builder)      browser agent) agent)      dev team)      platform)      approvals)
```

**Duration:** 35-50 hours | **Difficulty:** Intermediate to Advanced

---

## 📊 Collection Stats

```
╔══════════════════════════════════════════════════════════╗
║                  COLLECTION OVERVIEW                     ║
╠══════════════════════════════════════════════════════════╣
║  📦 Total Tutorials        191                           ║
║  📝 Numbered Chapters      1,528+                        ║
║  📏 Tutorial Markdown      1,048,763 lines               ║
║  ⏱️  Estimated Hours        2,000+                        ║
║  ✅ Local Broken Links      0                             ║
║  🧭 Structure Drift         0 (all root canonical)        ║
╚══════════════════════════════════════════════════════════╝
```

Stats are synchronized against:

- `tutorials/tutorial-manifest.json`
- `scripts/docs_health.py` baseline checks

---

## 🛠️ How Tutorials Are Built

Each tutorial is generated using AI-powered codebase analysis, then reviewed and enhanced for accuracy. The process:

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│  Crawl   │───→│   Identify   │───→│   Generate   │───→│  Review  │
│  Repo    │    │  Abstractions│    │   Chapters   │    │ & Polish │
└──────────┘    └──────────────┘    └──────────────┘    └──────────┘
   Clone &         Find core          Write 8-ch          Verify code
   index files     classes &          tutorials w/         examples &
                   patterns           diagrams             architecture
```

Inspired by [Tutorial-Codebase-Knowledge](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge) by The Pocket.

### Built & Maintained With

| Tool | Purpose |
|:-----|:--------|
| **[Taskade](https://taskade.com)** | Project planning, AI-powered content generation |
| **[Claude Code](https://claude.ai)** | Codebase analysis and tutorial writing |
| **[GitHub Pages](https://pages.github.com)** | Tutorial hosting with Jekyll |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

```
┌─────────────────────────────────────────────────┐
│              WAYS TO CONTRIBUTE                  │
├─────────────────────────────────────────────────┤
│  ⭐  Star the repo to show support              │
│  📝  Suggest a new tutorial via Issues           │
│  🔧  Fix errors or improve existing tutorials    │
│  📖  Write a new tutorial for a project          │
│  💬  Share feedback in Discussions                │
└─────────────────────────────────────────────────┘
```

### What Makes a Great Tutorial?

- **Goes deep** — explains *how* and *why*, not just *what*
- **Real code** — examples from the actual codebase, not toy demos
- **Visual** — architecture diagrams, flow charts, sequence diagrams
- **Progressive** — builds complexity gradually across chapters
- **Production-focused** — covers deployment, monitoring, scaling

**[Open an Issue](https://github.com/johnxie/awesome-code-docs/issues/new)** to suggest a new tutorial or report a problem.

---

## 🌍 Community

| | |
|:--|:--|
| ⭐ **[Star this repo](https://github.com/johnxie/awesome-code-docs)** | Get updates on new tutorials |
| 💬 **[Issues](https://github.com/johnxie/awesome-code-docs/issues)** | Ask questions, report gaps, share suggestions |
| 🐦 **[Twitter @johnxie](https://twitter.com/johnxie)** | Latest updates and highlights |

---

<div align="center">

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   "The best way to learn a codebase is to        │
│    understand the architecture decisions          │
│    that shaped it."                               │
│                                                  │
└──────────────────────────────────────────────────┘
```

**[Browse Tutorials](#-tutorial-catalog)** · **[Pick a Learning Path](#-learning-paths)** · **[Star on GitHub](https://github.com/johnxie/awesome-code-docs)**

</div>
