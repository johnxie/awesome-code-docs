---
layout: default
title: "CopilotKit Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 1: Getting Started with CopilotKit

Welcome to **Chapter 1: Getting Started with CopilotKit**. In this part of **CopilotKit Tutorial: Building AI Copilots for React Applications**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Set up CopilotKit in your React application and create your first AI copilot with basic functionality.

## Overview

This chapter guides you through installing CopilotKit, setting up your development environment, and building your first AI-powered React application with copilot functionality.

## Prerequisites and Setup

### System Requirements

```bash
# Node.js and npm
node --version  # Should be 18.0 or higher
npm --version   # Should be 8.0 or higher

# React and Next.js
# CopilotKit works best with Next.js 13+ App Router
```

### Create a Next.js Project

```bash
# Create a new Next.js project
npx create-next-app@latest copilotkit-demo --typescript --tailwind --eslint --app
cd copilotkit-demo

# Install CopilotKit
npm install @copilotkit/react-core @copilotkit/react-ui

# Start the development server
npm run dev
```

### Alternative: Add to Existing Project

```bash
# If you have an existing Next.js project
cd your-existing-project

# Install CopilotKit
npm install @copilotkit/react-core @copilotkit/react-ui

# For TypeScript support (recommended)
npm install --save-dev @types/react @types/react-dom
```

## Basic CopilotKit Setup

### Configure the Provider

```tsx
// app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

### Create the Copilot Runtime API

```tsx
// app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotkitStream
} from "@copilotkit/runtime";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const runtime = new CopilotRuntime();

const serviceAdapter = new OpenAIAdapter({
  openai,
  model: "gpt-4o",
});

export async function POST(req: Request) {
  const { handleRequest } = copilotkitStream({
    runtime,
    serviceAdapter,
  });

  return handleRequest(req);
}
```

### Environment Variables

```bash
# .env.local
OPENAI_API_KEY=sk-your-openai-api-key-here

# Or for Anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# For other providers (Groq, etc.)
GROQ_API_KEY=gsk-your-groq-key-here
```

## Your First Copilot Component

### Simple Todo Application

```tsx
// app/page.tsx
"use client";

import { useState } from "react";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

export default function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);

  // Make the todos readable by the copilot
  useCopilotReadable({
    description: "The current list of todo items",
    value: todos,
  });

  // Allow the copilot to add todos
  useCopilotAction({
    name: "addTodo",
    description: "Add a new todo item to the list",
    parameters: [
      {
        name: "text",
        type: "string",
        description: "The text content of the todo item",
        required: true,
      },
    ],
    handler: async ({ text }: { text: string }) => {
      const newTodo: Todo = {
        id: Date.now(),
        text,
        completed: false,
      };
      setTodos(prev => [...prev, newTodo]);
    },
  });

  // Allow the copilot to toggle todo completion
  useCopilotAction({
    name: "toggleTodo",
    description: "Mark a todo item as completed or incomplete",
    parameters: [
      {
        name: "id",
        type: "number",
        description: "The ID of the todo item to toggle",
        required: true,
      },
    ],
    handler: async ({ id }: { id: number }) => {
      setTodos(prev =>
        prev.map(todo =>
          todo.id === id ? { ...todo, completed: !todo.completed } : todo
        )
      );
    },
  });

  return (
    <CopilotSidebar>
      <div className="p-8 max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">AI-Powered Todo App</h1>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Your Todos</h2>

          {todos.length === 0 ? (
            <p className="text-gray-500">No todos yet. Ask the copilot to add some!</p>
          ) : (
            <ul className="space-y-2">
              {todos.map(todo => (
                <li
                  key={todo.id}
                  className={`p-3 rounded border ${
                    todo.completed
                      ? "bg-green-50 border-green-200 line-through text-green-700"
                      : "bg-white border-gray-200"
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={todo.completed}
                      onChange={() => {
                        setTodos(prev =>
                          prev.map(t =>
                            t.id === todo.id ? { ...t, completed: !t.completed } : t
                          )
                        );
                      }}
                      className="rounded"
                    />
                    <span>{todo.text}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• "Add a todo to buy groceries"</li>
            <li>• "Mark the first todo as completed"</li>
            <li>• "Add three more todos for work tasks"</li>
            <li>• "Show me only the completed todos"</li>
          </ul>
        </div>
      </div>
    </CopilotSidebar>
  );
}
```

## Understanding CopilotKit Architecture

### The CopilotKit Runtime

```mermaid
flowchart TD
    A[React Component] --> B[CopilotKit Provider]
    B --> C[useCopilotReadable]
    B --> D[useCopilotAction]
    B --> E[CopilotSidebar/CopilotChat]

    C --> F[Context Sharing]
    D --> G[Action Execution]
    E --> H[User Interaction]

    F --> I[Copilot Runtime]
    G --> I
    H --> I

    I --> J[LLM Service]
    I --> K[State Management]
    I --> L[Action Handlers]

    classDef react fill:#61dafb,stroke:#20232a
    classDef copilot fill:#f3e5f5,stroke:#4a148c
    classDef runtime fill:#fff3e0,stroke:#ef6c00

    class A react
    class B,C,D,E,F,G,H copilot
    class I,K,L runtime
    class J external
```

### Key Concepts

1. **CopilotKit Provider**: Wraps your app and provides copilot functionality
2. **useCopilotReadable**: Makes app state visible to the AI
3. **useCopilotAction**: Allows AI to perform actions in your app
4. **Copilot Runtime**: Handles communication between UI and AI
5. **Copilot UI Components**: Pre-built chat interfaces

## Testing Your First Copilot

### Basic Interaction Test

```bash
# Start your development server
npm run dev

# Open http://localhost:3000

# Try these interactions with the copilot:

# Basic addition
# "Add a todo to buy milk and bread"

# Multiple additions
# "Add three todos: finish report, call client, schedule meeting"

# Status checking
# "How many todos do I have?"
# "Show me the incomplete todos"

# Completion toggling
# "Mark the buy milk todo as completed"
```

### Debugging Common Issues

```typescript
// Add error handling to your components
"use client";

import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

export default function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [error, setError] = useState<string | null>(null);

  useCopilotAction({
    name: "addTodo",
    description: "Add a new todo item",
    parameters: [
      {
        name: "text",
        type: "string",
        description: "The todo text",
        required: true,
      },
    ],
    handler: async ({ text }) => {
      try {
        if (!text || text.trim().length === 0) {
          throw new Error("Todo text cannot be empty");
        }

        const newTodo: Todo = {
          id: Date.now(),
          text: text.trim(),
          completed: false,
        };

        setTodos(prev => [...prev, newTodo]);
        setError(null);

        return { success: true, todo: newTodo };
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to add todo";
        setError(errorMessage);
        throw new Error(errorMessage);
      }
    },
  });

  // ... rest of component
}
```

### Copilot Configuration Options

```tsx
// app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";

export default function RootLayout({ children }) {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      // Optional configuration
      children={children}
    >
      {children}
    </CopilotKit>
  );
}
```

```tsx
// Advanced configuration
import { CopilotKit } from "@copilotkit/react-core";

export default function RootLayout({ children }) {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      // Custom runtime configuration
      runtime={{
        model: "gpt-4o",
        temperature: 0.7,
        maxTokens: 1000,
      }}
      // Enable experimental features
      experimental={{
        generativeUI: true,
        suggestions: true,
      }}
    >
      {children}
    </CopilotKit>
  );
}
```

## Alternative LLM Providers

### Anthropic Claude

```tsx
// app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  AnthropicAdapter,
  copilotkitStream
} from "@copilotkit/runtime";
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const runtime = new CopilotRuntime();

const serviceAdapter = new AnthropicAdapter({
  anthropic,
  model: "claude-3-5-sonnet-20241022",
});

export async function POST(req: Request) {
  const { handleRequest } = copilotkitStream({
    runtime,
    serviceAdapter,
  });

  return handleRequest(req);
}
```

### Groq (Fast Inference)

```tsx
// app/api/copilotkit/route.ts
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotkitStream
} from "@copilotkit/runtime";

// Groq uses OpenAI-compatible API
const groq = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: "https://api.groq.com/openai/v1",
});

const runtime = new CopilotRuntime();

const serviceAdapter = new OpenAIAdapter({
  openai: groq,
  model: "llama3-8b-8192", // Fast Groq model
});

export async function POST(req: Request) {
  const { handleRequest } = copilotkitStream({
    runtime,
    serviceAdapter,
  });

  return handleRequest(req);
}
```

## Advanced First Project

### Note-Taking App with AI

```tsx
// app/page.tsx
"use client";

import { useState } from "react";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  createdAt: Date;
}

export default function NotesApp() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);

  // Make notes readable by the copilot
  useCopilotReadable({
    description: "All user notes with titles, content, and tags",
    value: notes,
  });

  useCopilotReadable({
    description: "The currently selected note",
    value: selectedNote,
  });

  // Create new note
  useCopilotAction({
    name: "createNote",
    description: "Create a new note with title and content",
    parameters: [
      { name: "title", type: "string", description: "Note title", required: true },
      { name: "content", type: "string", description: "Note content", required: true },
      { name: "tags", type: "string[]", description: "Note tags" },
    ],
    handler: async ({ title, content, tags = [] }) => {
      const newNote: Note = {
        id: Date.now().toString(),
        title,
        content,
        tags,
        createdAt: new Date(),
      };
      setNotes(prev => [...prev, newNote]);
      setSelectedNote(newNote);
    },
  });

  // Search notes
  useCopilotAction({
    name: "searchNotes",
    description: "Search notes by content or tags",
    parameters: [
      { name: "query", type: "string", description: "Search query", required: true },
    ],
    handler: async ({ query }) => {
      const results = notes.filter(note =>
        note.title.toLowerCase().includes(query.toLowerCase()) ||
        note.content.toLowerCase().includes(query.toLowerCase()) ||
        note.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
      );
      return { results, count: results.length };
    },
  });

  return (
    <CopilotSidebar>
      <div className="flex h-screen">
        {/* Notes List */}
        <div className="w-1/3 border-r p-4">
          <h2 className="text-xl font-bold mb-4">Notes</h2>
          <button
            onClick={() => setSelectedNote(null)}
            className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            New Note
          </button>

          <div className="space-y-2">
            {notes.map(note => (
              <div
                key={note.id}
                onClick={() => setSelectedNote(note)}
                className={`p-3 border rounded cursor-pointer hover:bg-gray-50 ${
                  selectedNote?.id === note.id ? "border-blue-500 bg-blue-50" : ""
                }`}
              >
                <h3 className="font-medium">{note.title}</h3>
                <p className="text-sm text-gray-600 truncate">{note.content}</p>
                {note.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-1">
                    {note.tags.map(tag => (
                      <span key={tag} className="px-2 py-1 bg-gray-200 text-xs rounded">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Note Editor */}
        <div className="flex-1 p-4">
          {selectedNote ? (
            <div>
              <h2 className="text-2xl font-bold mb-4">{selectedNote.title}</h2>
              <div className="mb-4">
                {selectedNote.tags.map(tag => (
                  <span key={tag} className="mr-2 px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">
                    {tag}
                  </span>
                ))}
              </div>
              <div className="prose max-w-none">
                {selectedNote.content.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 mt-20">
              <h2 className="text-xl mb-4">Create a new note</h2>
              <p>Ask the copilot to create notes, search existing notes, or edit content.</p>
            </div>
          )}
        </div>
      </div>
    </CopilotSidebar>
  );
}
```

## Summary

In this chapter, we've covered:

- **CopilotKit Installation**: Setting up the framework in Next.js projects
- **Provider Configuration**: Setting up the CopilotKit provider and runtime
- **Basic Actions**: Creating simple AI-powered interactions
- **Context Sharing**: Making app state readable by the copilot
- **LLM Integration**: Connecting different AI providers
- **Advanced Examples**: Building more complex applications

## Key Takeaways

1. **Easy Integration**: CopilotKit integrates seamlessly with React applications
2. **Context Awareness**: AI understands your app state through useCopilotReadable
3. **Action Enablement**: AI can perform actions through useCopilotAction
4. **Multiple Providers**: Support for OpenAI, Anthropic, Groq, and others
5. **Flexible UI**: Choose from sidebar, chat, or custom interfaces
6. **Type Safety**: Full TypeScript support for better development experience

## Next Steps

Now that you have a basic copilot running, let's explore how to make your app context visible to the AI in the next chapter.

---

**Ready for Chapter 2?** [Reading App Context](02-app-context.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `text`, `className`, `todo` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with CopilotKit` as an operating subsystem inside **CopilotKit Tutorial: Building AI Copilots for React Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `copilotkit`, `react`, `note` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with CopilotKit` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `text`.
2. **Input normalization**: shape incoming data so `className` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `todo`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/CopilotKit/CopilotKit)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `Awesome Code Docs` (github.com).

Suggested trace strategy:
- search upstream code for `text` and `className` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Reading App Context - Making Your App State Visible to AI](02-app-context.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
