---
layout: default
title: "Continue Tutorial"
nav_order: 26
has_children: true
---

# Continue Tutorial: Open-Source AI Autopilot for Development

> A deep technical walkthrough of Continue covering Open-Source AI Autopilot for Development.

[![Stars](https://img.shields.io/github/stars/continuedev/continue?style=social)](https://github.com/continuedev/continue)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-blue)](https://github.com/continuedev/continue)


Continue<sup>[View Repo](https://github.com/continuedev/continue)</sup> is an open-source autopilot for software development that provides AI-powered coding assistance. It offers a customizable, self-hosted alternative to commercial AI coding tools, with support for multiple AI models, extensive customization options, and seamless integration with popular development environments.

Continue transforms how developers work by providing intelligent code completion, refactoring suggestions, documentation generation, and debugging assistance through a flexible, extensible architecture.

```mermaid
flowchart TD
    A[Developer Input] --> B[Continue Engine]
    B --> C[Code Analysis]
    C --> D[AI Model Processing]
    D --> E[Code Generation]
    E --> F[Output Integration]

    B --> G[Context Gathering]
    G --> H[Project Understanding]
    H --> C

    D --> I[Model Selection]
    I --> J[OpenAI, Anthropic, Local]
    J --> E

    F --> K[Editor Integration]
    K --> L[VS Code, JetBrains, Vim]
    L --> M[Seamless Workflow]

    classDef input fill:#e1f5fe,stroke:#01579b
    classDef processing fill:#f3e5f5,stroke:#4a148c
    classDef output fill:#e8f5e8,stroke:#1b5e20

    class A,G input
    class B,C,D,H,I,J processing
    class E,F,K,L,M output
```

## Tutorial Chapters

Welcome to your journey through AI-powered software development! This tutorial explores how to harness Continue for intelligent coding assistance.

1. **[Chapter 1: Getting Started with Continue](01-getting-started.md)** - Installation, setup, and first AI-assisted coding session
2. **[Chapter 2: Code Completion & Generation](02-code-completion.md)** - Advanced code completion and intelligent suggestions
3. **[Chapter 3: Refactoring & Optimization](03-refactoring-optimization.md)** - AI-powered code refactoring and performance optimization
4. **[Chapter 4: Documentation & Comments](04-documentation-comments.md)** - Automatic documentation generation and code explanation
5. **[Chapter 5: Debugging & Testing](05-debugging-testing.md)** - AI-assisted debugging and test generation
6. **[Chapter 6: Custom Models & Configuration](06-custom-models.md)** - Setting up custom AI models and configurations
7. **[Chapter 7: Team Collaboration](07-team-collaboration.md)** - Multi-developer workflows and collaboration practices
8. **[Chapter 8: Advanced Enterprise](08-advanced-enterprise.md)** - Scaling Continue for teams and organizations

## What You'll Learn

By the end of this tutorial, you'll be able to:

- **Set up Continue** for AI-powered development assistance
- **Master code completion** with context-aware suggestions
- **Perform intelligent refactoring** with AI guidance
- **Generate comprehensive documentation** automatically
- **Debug code efficiently** with AI assistance
- **Configure custom AI models** for specialized tasks
- **Build custom extensions** to extend functionality
- **Deploy Continue at scale** for enterprise environments

## What's New in Continue v0.9 & 2025

> **AI Coding Evolution**: Agent mode acceleration, Plan mode safety, and intelligent editing features mark Continue's latest breakthroughs.

**🚀 v0.9 Release (May 2025):**
- ⚡ **Faster Agent Mode**: AST-based targeted edits instead of full file rewrites
- 🎯 **Mercury-Coder-Small**: Diffusion-based model for instant autocomplete suggestions
- 📝 **Automatic Rules**: AI-generated rules saved to `~/.continue/rules`
- 🔄 **Fast Apply Support**: Enhanced code application with Relace Instant Apply and Morph v0

**🛡️ Plan Mode (July 2025):**
- 🔒 **Read-Only Safety**: Intelligent conversation and code analysis without making changes
- 🧠 **Smart Assistance**: Full AI reasoning capabilities with restricted tool access
- 🎯 **Risk-Free Exploration**: Discuss and analyze code changes before implementation
- 📊 **Planning Phase**: Perfect for architectural discussions and code review

**✏️ Next Edit (September 2025):**
- 🎯 **Pattern Anticipation**: Learns your editing habits and suggests multi-line changes
- 🔮 **Intent Prediction**: Understands development patterns and provides proactive suggestions
- ⚡ **Workflow Acceleration**: Reduces manual editing through intelligent automation
- 🎨 **Context Awareness**: Considers surrounding code when making suggestions

**🔄 Parallel Tool Calling (September 2025):**
- ⚡ **Simultaneous Execution**: Tools run in parallel for faster workflows
- 🚀 **Performance Boost**: Significantly reduced wait times for multi-tool operations
- 🎯 **Efficient Processing**: Optimized resource utilization and responsiveness
- 📈 **Scalability**: Better handling of complex, multi-step development tasks

## Prerequisites

- Basic programming knowledge in any language
- Familiarity with your preferred code editor (VS Code, JetBrains, Vim, etc.)
- Understanding of AI/ML concepts (helpful but not required)

## Learning Path

### 🟢 Beginner Track
Perfect for developers new to AI-assisted coding:
1. Chapters 1-2: Setup and basic code completion
2. Focus on getting started with AI coding assistance

### 🟡 Intermediate Track
For developers enhancing their coding workflow:
1. Chapters 3-5: Refactoring, documentation, and debugging
2. Learn advanced AI-powered development techniques

### 🔴 Advanced Track
For customizing and deploying Continue at scale:
1. Chapters 6-8: Custom models, extensions, and enterprise deployment
2. Master advanced Continue customization and deployment

---

**Ready to supercharge your development workflow with AI? Let's begin with [Chapter 1: Getting Started](01-getting-started.md)!**

*Generated by [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)*
