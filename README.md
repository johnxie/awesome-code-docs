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
[![Tutorials](https://img.shields.io/badge/tutorials-94-brightgreen.svg)](#-tutorial-catalog)
[![Content Hours](https://img.shields.io/badge/content-1100%2B%20hours-orange.svg)](#-tutorial-catalog)
[![Last Updated](https://img.shields.io/github/last-commit/johnxie/awesome-code-docs?label=updated)](https://github.com/johnxie/awesome-code-docs/commits/main)

[**Browse Tutorials**](#-tutorial-catalog) · [**Learning Paths**](#-learning-paths) · [**Contributing**](#-contributing) · [**Community**](#-community)

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

## 📚 Tutorial Catalog

```
 ╔════════════════════════════════════════════════════════════╗
 ║  🤖  AI & AGENTS  │  🔧  DEV TOOLS  │  🗄️  DATA  │  🎤 SPEECH  ║
 ║   57+ tutorials    │   21 tutorials  │  14 tutorials │  3 tutorials  ║
 ╚════════════════════════════════════════════════════════════╝
```

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
| **[Deer Flow](tutorials/deer-flow-tutorial/)** | - | Python | Research agent workflows |
| **[Letta](tutorials/letta-tutorial/)** | 14K+ | Python | Stateful agents with long-term memory |
| **[Anthropic Skills](tutorials/anthropic-skills-tutorial/)** | 59K+ | Python/TypeScript | Reusable AI agent capabilities, MCP integration |

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
| **[LobeChat](tutorials/lobechat-ai-platform/)** | 71K+ | Next.js | Modern AI chat, plugins, theming |
| **[Dify](tutorials/dify-platform-deep-dive/)** | 60K+ | Python/React | Visual LLM app builder |
| **[Flowise](tutorials/flowise-llm-orchestration/)** | 35K+ | Node.js/React | Visual LLM workflow orchestration |
| **[CopilotKit](tutorials/copilotkit-tutorial/)** | 15K+ | React/TypeScript | In-app AI copilots |
| **[Chatbox](tutorials/chatbox-tutorial/)** | 24K+ | JavaScript/React | Multi-provider chat client |
| **[Vercel AI SDK](tutorials/vercel-ai-tutorial/)** | 21K+ | TypeScript | AI-powered React/Next.js apps |
| **[Perplexica](tutorials/perplexica-tutorial/)** | 19K+ | TypeScript | AI-powered search engine |
| **[SillyTavern](tutorials/sillytavern-tutorial/)** | 9K+ | Node.js | Advanced roleplay chat platform |
| **[Khoj](tutorials/khoj-tutorial/)** | 18K+ | Python/Django | Self-hosted AI personal assistant |
| **[Botpress](tutorials/botpress-tutorial/)** | 13K+ | Node.js | Enterprise chatbot platform |
| **[AnythingLLM](tutorials/anything-llm-tutorial/)** | 30K+ | Node.js | All-in-one AI desktop app |
| **[GPT-OSS](tutorials/gpt-oss-tutorial/)** | - | TypeScript | Open-source GPT implementation |
| **[Claude Quickstarts](tutorials/claude-quickstarts-tutorial/)** | 13.7K+ | Python/TypeScript | Production Claude integration patterns |

### 🔧 Developer Tools & Productivity

AI coding assistants, build systems, and dev infrastructure.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Continue](tutorials/continue-tutorial/)** | 22K+ | TypeScript | Open-source AI coding assistant |
| **[Cline](tutorials/cline-tutorial/)** | 58K+ | TypeScript/VS Code | Agentic coding with terminal, browser, MCP tools |
| **[Roo Code](tutorials/roo-code-tutorial/)** | 22K+ | TypeScript/VS Code | Multi-mode coding agents with checkpoints and MCP |
| **[bolt.diy](tutorials/bolt-diy-tutorial/)** | 19K+ | TypeScript/Remix | Open-source Bolt-style AI app builder |
| **[OpenHands](tutorials/openhands-tutorial/)** | 67K+ | Python | AI software engineering agent |
| **[Aider](tutorials/aider-tutorial/)** | 25K+ | Python | AI pair programming in terminal |
| **[Claude Code](tutorials/claude-code-tutorial/)** | - | TypeScript | Anthropic's AI coding CLI |
| **[Anthropic API](tutorials/anthropic-code-tutorial/)** | - | Python/TypeScript | Claude API integration, tool use, streaming |
| **[Claude Task Master](tutorials/claude-task-master-tutorial/)** | - | TypeScript | AI-powered task management |
| **[CopilotKit](tutorials/copilotkit-tutorial/)** | 15K+ | React | In-app AI assistants |
| **[Nanocoder](tutorials/nanocoder-tutorial/)** | - | TypeScript | AI coding agent internals |
| **[Codex Analysis](tutorials/codex-analysis-platform/)** | - | TypeScript | Static analysis platform and LSP architecture |
| **[Turborepo](tutorials/turborepo-tutorial/)** | 27K+ | Rust | High-performance monorepo builds |
| **[n8n AI](tutorials/n8n-ai-tutorial/)** | 52K+ | Node.js | Visual AI workflow automation |
| **[Taskade](tutorials/taskade-tutorial/)** | - | AI/Productivity | AI-powered project management |
| **[Browser Use](tutorials/browser-use-tutorial/)** | 10K+ | Python | AI-powered browser automation |
| **[ComfyUI](tutorials/comfyui-tutorial/)** | 65K+ | Python | Node-based AI art workflows |
| **[MCP Python SDK](tutorials/mcp-python-sdk-tutorial/)** | 21.4K+ | Python | Building MCP servers and tool integrations |
| **[MCP Servers](tutorials/mcp-servers-tutorial/)** | 77.6K+ | Multi-lang | Reference MCP server implementations |
| **[OpenAI Python SDK](tutorials/openai-python-sdk-tutorial/)** | 29.8K+ | Python | GPT API, embeddings, assistants, batch processing |
| **[tiktoken](tutorials/tiktoken-tutorial/)** | 17.1K+ | Python/Rust | Token counting, encoding, cost optimization |

### 🗄️ Databases, Knowledge & Analytics

Data platforms, knowledge management, and observability.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Supabase](tutorials/supabase-tutorial/)** | 75K+ | PostgreSQL/TypeScript | Realtime DB, auth, edge functions |
| **[PostHog](tutorials/posthog-tutorial/)** | 23K+ | Python/TypeScript | Product analytics, feature flags |
| **[NocoDB](tutorials/nocodb-database-platform/)** | 50K+ | Node.js/Vue | Open-source Airtable alternative |
| **[Teable](tutorials/teable-database-platform/)** | 15K+ | TypeScript/PostgreSQL | Multi-dimensional data platform |
| **[SiYuan](tutorials/siyuan-tutorial/)** | 25K+ | Go/TypeScript | Privacy-first knowledge management |
| **[Logseq](tutorials/logseq-knowledge-management/)** | 34K+ | ClojureScript | Local-first knowledge graph |
| **[OpenBB](tutorials/openbb-tutorial/)** | 35K+ | Python | Open-source financial terminal |
| **[Athens Research](tutorials/athens-research-knowledge-graph/)** | - | ClojureScript | Graph-based knowledge system |
| **[Obsidian Outliner](tutorials/obsidian-outliner-plugin/)** | - | TypeScript | Obsidian plugin architecture |
| **[ClickHouse](tutorials/clickhouse-tutorial/)** | 39K+ | C++ | Column-oriented analytics DB |
| **[PostgreSQL Planner](tutorials/postgresql-query-planner/)** | - | C | Query planning internals |
| **[MeiliSearch](tutorials/meilisearch-tutorial/)** | 48K+ | Rust | Lightning-fast search engine |
| **[PhotoPrism](tutorials/photoprism-tutorial/)** | 36K+ | Go | AI-powered photo management |
| **[Liveblocks](tutorials/liveblocks-tutorial/)** | 4K+ | TypeScript | Real-time collaboration infra |

### ⚙️ Systems & Infrastructure

Low-level systems, cloud native, and infrastructure patterns.

| Tutorial | Stars | Stack | What You'll Learn |
|:---------|:-----:|:------|:------------------|
| **[Kubernetes Operators](tutorials/kubernetes-operator-patterns/)** | - | Go | Production-grade K8s operator patterns |
| **[React Fiber](tutorials/react-fiber-internals/)** | - | JavaScript | React reconciler internals |
| **[Dyad](tutorials/dyad-tutorial/)** | 19K+ | TypeScript | Local AI app development |
| **[LangChain Architecture](tutorials/langchain-architecture-guide/)** | - | Python | LangChain deep architecture guide |
| **[n8n MCP](tutorials/n8n-mcp-tutorial/)** | - | TypeScript | Model Context Protocol with n8n |
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
Continue ──→ Aider ──→ OpenHands ──→ Browser Use ──→ Claude Code
 (code         (pair     (AI SWE      (browser        (CLI
  completion)   prog)     agent)       automation)      agent)
```

### 🟡 Path 7: MCP Mastery

> *"I want to build AI tool servers and extend Claude with custom capabilities"*

```
MCP Python SDK ──→ MCP Servers ──→ Anthropic Skills ──→ n8n MCP ──→ Claude Code
 (build             (reference        (reusable            (production   (use MCP
  servers)           implementations)  capabilities)        patterns)      tools)
```

**Duration:** 40-50 hours | **Difficulty:** Intermediate to Advanced

### 🟢 Path 8: Speech & Voice AI

> *"I want to build voice-first AI applications"*

```
OpenAI Whisper ──→ Whisper.cpp ──→ OpenAI Realtime Agents ──→ Voice Apps
 (Python ASR,       (edge            (voice-first             (production
  fine-tuning)       deployment)       conversations)           voice apps)
```

**Duration:** 25-35 hours | **Difficulty:** Intermediate

### 🟡 Path 9: OpenAI Ecosystem

> *"I want to master OpenAI's tools and APIs"*

```
OpenAI Python SDK ──→ tiktoken ──→ OpenAI Whisper ──→ Realtime Agents
 (core API,          (token         (speech              (voice
  embeddings,         optimization)  recognition)         agents)
  assistants)
```

**Duration:** 35-45 hours | **Difficulty:** Beginner to Intermediate

---

## 📊 Collection Stats

```
╔══════════════════════════════════════════════════════════╗
║                  COLLECTION OVERVIEW                     ║
╠══════════════════════════════════════════════════════════╣
║  📦 Total Tutorials        94                            ║
║  📝 Total Chapters         784+                          ║
║  📏 Lines of Content       520,000+                      ║
║  ⏱️  Estimated Hours        1,100+                        ║
║  🏗️  Architecture Diagrams  550+                          ║
║  💻 Code Examples           2,400+                        ║
╚══════════════════════════════════════════════════════════╝
```

| Category | Tutorials | Status |
|:---------|:---------:|:------:|
| 🤖 AI Agents & Multi-Agent | 15 | Complete |
| 🧠 LLM Frameworks & RAG | 12 | Complete |
| 🖥️ LLM Infrastructure | 9 | Complete |
| 💬 Chat & AI Apps | 13 | Complete |
| 🔧 Developer Tools | 20 | Complete |
| 🗄️ Data & Analytics | 14 | Complete |
| ⚙️ Systems & Infra | 6 | Complete |
| 🎤 Speech & Multimodal AI | 3 | Complete |

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
| 💬 **[Discussions](https://github.com/johnxie/awesome-code-docs/discussions)** | Ask questions, share insights |
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
