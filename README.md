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
[![Tutorials](https://img.shields.io/badge/tutorials-181-brightgreen.svg)](#-tutorial-catalog)
[![Content Hours](https://img.shields.io/badge/content-1940%2B%20hours-orange.svg)](#-tutorial-catalog)
[![Last Updated](https://img.shields.io/github/last-commit/johnxie/awesome-code-docs?label=updated)](https://github.com/johnxie/awesome-code-docs/commits/main)

[**Browse Tutorials**](#-tutorial-catalog) · [**A-Z Directory**](discoverability/tutorial-directory.md) · [**Learning Paths**](#-learning-paths) · [**Contributing**](#-contributing) · [**Community**](#-community)

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
| open-source vibe coding tools | [Cline](tutorials/cline-tutorial/) | [Roo Code](tutorials/roo-code-tutorial/) → [OpenCode](tutorials/opencode-tutorial/) → [Tabby](tutorials/tabby-tutorial/) → [bolt.diy](tutorials/bolt-diy-tutorial/) → [VibeSDK](tutorials/vibesdk-tutorial/) → [HAPI](tutorials/hapi-tutorial/) |
| spec-driven AI delivery workflows | [OpenSpec](tutorials/openspec-tutorial/) | [Claude Task Master](tutorials/claude-task-master-tutorial/) → [Codex CLI](tutorials/codex-cli-tutorial/) → [OpenCode](tutorials/opencode-tutorial/) |
| build AI agents in production | [LangChain](tutorials/langchain-tutorial/) | [LangGraph](tutorials/langgraph-tutorial/) → [CrewAI](tutorials/crewai-tutorial/) → [OpenHands](tutorials/openhands-tutorial/) → [Claude Flow](tutorials/claude-flow-tutorial/) |
| build RAG systems | [LlamaIndex](tutorials/llamaindex-tutorial/) | [Haystack](tutorials/haystack-tutorial/) → [RAGFlow](tutorials/ragflow-tutorial/) |
| run LLMs locally or at scale | [Ollama](tutorials/ollama-tutorial/) | [llama.cpp](tutorials/llama-cpp-tutorial/) → [vLLM](tutorials/vllm-tutorial/) → [LiteLLM](tutorials/litellm-tutorial/) |
| build AI apps with TypeScript/Next.js | [Vercel AI SDK](tutorials/vercel-ai-tutorial/) | [CopilotKit](tutorials/copilotkit-tutorial/) → [LobeChat](tutorials/lobechat-ai-platform/) |
| build MCP tools and integrations | [MCP Python SDK](tutorials/mcp-python-sdk-tutorial/) | [FastMCP](tutorials/fastmcp-tutorial/) → [MCP Servers](tutorials/mcp-servers-tutorial/) → [MCP Quickstart Resources](tutorials/mcp-quickstart-resources-tutorial/) → [Create Python Server](tutorials/create-python-server-tutorial/) → [MCP Docs Repo](tutorials/mcp-docs-repo-tutorial/) → [Create TypeScript Server](tutorials/create-typescript-server-tutorial/) → [Awesome MCP Servers](tutorials/awesome-mcp-servers-tutorial/) → [Composio](tutorials/composio-tutorial/) → [Daytona](tutorials/daytona-tutorial/) → [GenAI Toolbox](tutorials/genai-toolbox-tutorial/) → [awslabs/mcp](tutorials/awslabs-mcp-tutorial/) → [MCP Inspector](tutorials/mcp-inspector-tutorial/) → [MCP Registry](tutorials/mcp-registry-tutorial/) → [MCP Specification](tutorials/mcp-specification-tutorial/) → [MCP TypeScript SDK](tutorials/mcp-typescript-sdk-tutorial/) → [MCP Go SDK](tutorials/mcp-go-sdk-tutorial/) → [MCP Rust SDK](tutorials/mcp-rust-sdk-tutorial/) → [MCP Java SDK](tutorials/mcp-java-sdk-tutorial/) → [MCP C# SDK](tutorials/mcp-csharp-sdk-tutorial/) → [MCP Swift SDK](tutorials/mcp-swift-sdk-tutorial/) → [MCP Kotlin SDK](tutorials/mcp-kotlin-sdk-tutorial/) → [MCP Ruby SDK](tutorials/mcp-ruby-sdk-tutorial/) → [MCP PHP SDK](tutorials/mcp-php-sdk-tutorial/) → [MCP Ext Apps](tutorials/mcp-ext-apps-tutorial/) → [MCPB](tutorials/mcpb-tutorial/) → [use-mcp](tutorials/use-mcp-tutorial/) → [MCP Use](tutorials/mcp-use-tutorial/) |

---

## 📈 Trending Vibe-Coding Repos (Verified February 12, 2026)

This section tracks high-impact open-source vibe-coding and coding-agent ecosystems with direct tutorial coverage.

| Ecosystem Repo | Tutorial | Stars | Why It Matters |
|:---------------|:---------|------:|:---------------|
| [`dyad-sh/dyad`](https://github.com/dyad-sh/dyad) | [Dyad Tutorial](tutorials/dyad-tutorial/) | 19,591 | local-first AI app generation workflows |
| [`stackblitz-labs/bolt.diy`](https://github.com/stackblitz-labs/bolt.diy) | [bolt.diy Tutorial](tutorials/bolt-diy-tutorial/) | 18,997 | open-source Bolt-style product builder stack |
| [`cloudflare/vibesdk`](https://github.com/cloudflare/vibesdk) | [VibeSDK Tutorial](tutorials/vibesdk-tutorial/) | 4,762 | Cloudflare-native prompt-to-app platform architecture |
| [`vercel/ai`](https://github.com/vercel/ai) | [Vercel AI SDK Tutorial](tutorials/vercel-ai-tutorial/) | 21,688 | production TypeScript AI app and agent SDK patterns |
| [`cline/cline`](https://github.com/cline/cline) | [Cline Tutorial](tutorials/cline-tutorial/) | 57,809 | agentic coding with terminal/browser/MCP tools |
| [`RooCodeInc/Roo-Code`](https://github.com/RooCodeInc/Roo-Code) | [Roo Code Tutorial](tutorials/roo-code-tutorial/) | 22,198 | multi-mode coding agents and approval workflows |
| [`continuedev/continue`](https://github.com/continuedev/continue) | [Continue Tutorial](tutorials/continue-tutorial/) | 31,348 | IDE-native AI coding assistant architecture |
| [`anomalyco/opencode`](https://github.com/anomalyco/opencode) | [OpenCode Tutorial](tutorials/opencode-tutorial/) | 103,218 | terminal-native coding agent with strong provider and tool controls |
| [`TabbyML/tabby`](https://github.com/TabbyML/tabby) | [Tabby Tutorial](tutorials/tabby-tutorial/) | 32,884 | self-hosted coding assistant platform for teams and enterprises |
| [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec) | [OpenSpec Tutorial](tutorials/openspec-tutorial/) | 23,765 | spec-driven workflow layer for predictable AI-assisted delivery |
| [`Nano-Collective/nanocoder`](https://github.com/Nano-Collective/nanocoder) | [Nanocoder Tutorial](tutorials/nanocoder-tutorial/) | 1,318 | local-first coding-agent internals and tool loops |
| [`browser-use/browser-use`](https://github.com/browser-use/browser-use) | [Browser Use Tutorial](tutorials/browser-use-tutorial/) | 78,191 | browser-native AI automation and agent execution |
| [`open-webui/open-webui`](https://github.com/open-webui/open-webui) | [Open WebUI Tutorial](tutorials/open-webui-tutorial/) | 123,601 | self-hosted AI interface and model operations |
| [`Mintplex-Labs/anything-llm`](https://github.com/Mintplex-Labs/anything-llm) | [AnythingLLM Tutorial](tutorials/anything-llm-tutorial/) | 54,477 | self-hosted RAG workspaces and agent workflows |

---

## 📚 Tutorial Catalog

```
 ╔════════════════════════════════════════════════════════════╗
 ║  🤖  AI & AGENTS  │  🔧  DEV TOOLS  │  🗄️  DATA  │  🎤 SPEECH  ║
 ║   67+ tutorials    │   41 tutorials  │  14 tutorials │  3 tutorials  ║
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
| **[Deer Flow](tutorials/deer-flow-tutorial/)** | - | Python | Research agent workflows |
| **[Letta](tutorials/letta-tutorial/)** | 14K+ | Python | Stateful agents with long-term memory |
| **[Anthropic Skills](tutorials/anthropic-skills-tutorial/)** | 59K+ | Python/TypeScript | Reusable AI agent capabilities, MCP integration |
| **[Claude Flow](tutorials/claude-flow-tutorial/)** | 14.0K+ | TypeScript | Multi-agent orchestration, MCP server operations, and V2-V3 migration tradeoffs |

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
| **[OpenCode](tutorials/opencode-tutorial/)** | 103.2K+ | Go/TypeScript | Terminal-native coding agent architecture, provider routing, and tool safety controls |
| **[Tabby](tutorials/tabby-tutorial/)** | 32.9K+ | Rust/TypeScript | Self-hosted code completion and answer platform with editor-agent integrations |
| **[OpenSpec](tutorials/openspec-tutorial/)** | 23.8K+ | TypeScript/CLI | Spec-driven artifact workflow for planning, implementation, validation, and archive governance |
| **[bolt.diy](tutorials/bolt-diy-tutorial/)** | 19K+ | TypeScript/Remix | Open-source Bolt-style AI app builder |
| **[Cloudflare VibeSDK](tutorials/vibesdk-tutorial/)** | 4.7K+ | TypeScript/Cloudflare | Build and operate a cloud-native vibe-coding platform |
| **[HAPI](tutorials/hapi-tutorial/)** | 1.4K+ | TypeScript/CLI | Remote control and approval workflows for local coding agents |
| **[Daytona](tutorials/daytona-tutorial/)** | 55.3K+ | Go/TypeScript/Python | Secure sandbox infrastructure for AI-generated code and coding-agent execution |
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
| **[Activepieces](tutorials/activepieces-tutorial/)** | 20.8K+ | TypeScript | Open-source automation platform, custom pieces, and admin governance |
| **[Taskade](tutorials/taskade-tutorial/)** | - | AI/Productivity | AI-powered project management |
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
Continue ──→ Aider ──→ OpenHands ──→ OpenCode ──→ Tabby ──→ OpenSpec
 (code         (pair     (AI SWE      (terminal        (self-hosted     (spec-driven
  completion)   prog)     agent)       coding agent)    assistant)       delivery)
```

### 🟡 Path 7: MCP Mastery

> *"I want to build AI tool servers and extend Claude with custom capabilities"*

```
MCP Python SDK ──→ FastMCP ──→ MCP Servers ──→ MCP Quickstart Resources ──→ Create Python Server ──→ MCP Docs Repo ──→ Create TypeScript Server ──→ Awesome MCP Servers ──→ Composio ──→ Daytona ──→ GenAI Toolbox ──→ awslabs/mcp ──→ MCP Inspector ──→ MCP Registry ──→ MCP Specification ──→ MCP TypeScript SDK ──→ MCP Go SDK ──→ MCP Rust SDK ──→ MCP Java SDK ──→ MCP C# SDK ──→ MCP Swift SDK ──→ MCP Kotlin SDK ──→ MCP Ruby SDK ──→ MCP PHP SDK ──→ MCP Ext Apps ──→ MCPB ──→ use-mcp ──→ MCP Use
 (build             (build servers      (reference        (multi-lang             (python scaffold        (archived docs        (typescript scaffold      (discovery and          (tool + auth   (sandbox        (db-focused           (aws server          (debug +            (publish +           (protocol             (client/server         (go sdk +            (rust rmcp +         (java sdk +          (csharp sdk +         (swift sdk +          (kmp core +            (ruby server +          (php server +          (interactive ui +      (bundle pack +         (react hook +         (full-stack
  servers)           fast)               implementations)  quickstart set)         bootstrap path)         migration map)        bootstrap path)          curation)               runtime)       infra)          mcp control plane)    ecosystem)           transport tests)     discovery ops)        contract deep dive)    sdk internals)         conformance)          task/oauth focus)      spring modules)        aspnet filters)        lifecycle controls)    transport model)        client workflow)        discovery model)        host bridge model)      sign verify)            archived guidance)      mcp workflows)
```

**Duration:** 100-135 hours | **Difficulty:** Intermediate to Advanced

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

### 🔴 Path 10: Vibe Coding Platforms

> *"I want to build and operate vibe-coding stacks end to end"*

```
Dyad ──→ bolt.diy ──→ Cline ──→ Roo Code ──→ VibeSDK ──→ HAPI
 (local      (OSS app      (IDE        (multi-mode    (cloud         (remote
  builder)    builder)      agent)      dev team)      platform)      approvals)
```

**Duration:** 35-50 hours | **Difficulty:** Intermediate to Advanced

---

## 📊 Collection Stats

```
╔══════════════════════════════════════════════════════════╗
║                  COLLECTION OVERVIEW                     ║
╠══════════════════════════════════════════════════════════╣
║  📦 Total Tutorials        181                           ║
║  📝 Numbered Chapters      1,451                         ║
║  📏 Tutorial Markdown      475,000+ lines                ║
║  ⏱️  Estimated Hours        1,940+                        ║
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
