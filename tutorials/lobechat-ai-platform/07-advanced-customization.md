---
layout: default
title: "Chapter 7: Advanced Customization"
nav_order: 7
has_children: false
parent: "LobeChat AI Platform"
---

# Chapter 7: Advanced Customization

Welcome to **Chapter 7: Advanced Customization**. In this part of **LobeChat AI Platform: Deep Dive Tutorial**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Deep dive into LobeChat's theme engine, i18n, monorepo architecture, and component system

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- The theme engine and custom theming
- Internationalization (i18n) system
- Monorepo architecture and package structure
- Custom component development
- Extending the agent/assistant system

## Theme Engine

LobeChat uses Ant Design tokens combined with a custom theme system for comprehensive visual customization.

### Theme Provider Architecture

```typescript
// Theme token structure
interface LobeThemeTokens {
  // Color palette
  colorPrimary: string;
  colorBgLayout: string;
  colorBgContainer: string;
  colorText: string;
  colorTextSecondary: string;

  // Chat-specific tokens
  chatBubbleBg: string;
  chatBubbleUserBg: string;
  chatAvatarSize: number;
  chatMessageMaxWidth: string;

  // Layout tokens
  sidebarWidth: number;
  headerHeight: number;
  borderRadius: number;

  // Typography
  fontFamily: string;
  fontSize: number;
  fontSizeHeading: number;
}

// Theme provider wraps the app
const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { theme, isDark } = useThemeStore();

  const tokens = useMemo(() => ({
    ...defaultTokens,
    ...theme.customTokens,
    colorPrimary: theme.primaryColor,
    algorithm: isDark ? darkAlgorithm : defaultAlgorithm,
  }), [theme, isDark]);

  return (
    <AntdConfigProvider theme={{ token: tokens }}>
      <StyledThemeProvider theme={tokens}>
        {children}
      </StyledThemeProvider>
    </AntdConfigProvider>
  );
};
```

### Creating Custom Themes

```typescript
// Define a custom theme
const oceanTheme: CustomTheme = {
  name: "Ocean",
  primaryColor: "#0077B6",
  appearance: "dark",
  customTokens: {
    colorBgLayout: "#0A1628",
    colorBgContainer: "#0D2137",
    chatBubbleBg: "#163854",
    chatBubbleUserBg: "#0077B6",
    borderRadius: 16,
    fontFamily: "'Inter', system-ui, sans-serif",
  },
};

// Register theme in settings
const themeStore = create<ThemeStore>((set) => ({
  themes: [defaultTheme, darkTheme, oceanTheme],
  activeTheme: "default",

  setTheme: (themeName: string) => {
    set({ activeTheme: themeName });
    // Persist to localStorage
    localStorage.setItem("lobe-theme", themeName);
  },

  addCustomTheme: (theme: CustomTheme) => {
    set((state) => ({
      themes: [...state.themes, theme],
    }));
  },
}));
```

### CSS Variable System

LobeChat exposes theme values as CSS variables:

```css
:root {
  --lobe-primary: #0077b6;
  --lobe-bg-layout: #0a1628;
  --lobe-bg-container: #0d2137;
  --lobe-text: #e2e8f0;
  --lobe-text-secondary: #94a3b8;
  --lobe-chat-bubble: #163854;
  --lobe-chat-user-bubble: #0077b6;
  --lobe-border-radius: 16px;
  --lobe-sidebar-width: 280px;
  --lobe-header-height: 64px;
}

/* Usage in custom components */
.custom-card {
  background: var(--lobe-bg-container);
  color: var(--lobe-text);
  border-radius: var(--lobe-border-radius);
}
```

## Internationalization (i18n)

LobeChat supports 20+ languages through a structured i18n system.

### Translation Architecture

```
src/
├── locales/
│   ├── default/
│   │   ├── chat.ts          # Chat-related strings
│   │   ├── common.ts        # Shared strings
│   │   ├── setting.ts       # Settings strings
│   │   ├── plugin.ts        # Plugin strings
│   │   └── index.ts         # Namespace exports
│   ├── en-US/               # English (base)
│   ├── zh-CN/               # Chinese Simplified
│   ├── ja-JP/               # Japanese
│   ├── de-DE/               # German
│   └── ...                  # 20+ languages
```

### Translation Files

```typescript
// locales/default/chat.ts
export default {
  input: {
    placeholder: "Type a message...",
    send: "Send",
    stop: "Stop generating",
    regenerate: "Regenerate",
  },
  message: {
    copy: "Copy",
    delete: "Delete",
    edit: "Edit",
    retry: "Retry",
  },
  sidebar: {
    newChat: "New Chat",
    history: "Chat History",
    settings: "Settings",
    plugins: "Plugins",
  },
  model: {
    select: "Select Model",
    temperature: "Temperature",
    maxTokens: "Max Tokens",
  },
} as const;
```

### Using Translations in Components

```typescript
import { useTranslation } from "react-i18next";

const ChatInput: React.FC = () => {
  const { t } = useTranslation("chat");

  return (
    <div>
      <textarea placeholder={t("input.placeholder")} />
      <button>{t("input.send")}</button>
    </div>
  );
};
```

### Adding a New Language

```typescript
// 1. Create locale directory: locales/fr-FR/
// 2. Create translation files matching the default structure
// locales/fr-FR/chat.ts
export default {
  input: {
    placeholder: "Tapez un message...",
    send: "Envoyer",
    stop: "Arrêter la génération",
    regenerate: "Régénérer",
  },
  // ... complete translations
};

// 3. Register in the locale index
// locales/index.ts
import frFR from "./fr-FR";

export const locales = {
  "en-US": enUS,
  "fr-FR": frFR,
  // ...
};
```

## Monorepo Architecture

LobeChat is organized as a pnpm workspace monorepo:

```
lobe-chat/
├── src/                    # Main Next.js application
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── services/           # Business logic services
│   ├── store/              # Zustand state stores
│   ├── utils/              # Utility functions
│   └── locales/            # i18n translations
├── packages/               # Shared packages
│   ├── @lobehub/ui/        # UI component library
│   ├── @lobehub/icons/     # Icon set
│   ├── @lobehub/tts/       # Text-to-speech
│   └── @lobehub/lint/      # Linting configs
├── contributing/           # Contributor resources
└── docs/                   # Documentation
```

### State Management (Zustand)

LobeChat uses Zustand with slices pattern:

```typescript
// store/chat/store.ts
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface ChatState {
  messages: ChatMessage[];
  activeSessionId: string | null;
  isGenerating: boolean;
}

interface ChatActions {
  sendMessage: (content: string) => Promise<void>;
  regenerateMessage: (messageId: string) => Promise<void>;
  deleteMessage: (messageId: string) => void;
  clearMessages: () => void;
  setActiveSession: (sessionId: string) => void;
}

type ChatStore = ChatState & ChatActions;

export const useChatStore = create<ChatStore>()(
  devtools(
    persist(
      (set, get) => ({
        messages: [],
        activeSessionId: null,
        isGenerating: false,

        sendMessage: async (content) => {
          const message: ChatMessage = {
            id: crypto.randomUUID(),
            role: "user",
            content,
            timestamp: Date.now(),
          };

          set((state) => ({
            messages: [...state.messages, message],
            isGenerating: true,
          }));

          // Trigger AI response
          await get().generateResponse(message);

          set({ isGenerating: false });
        },

        deleteMessage: (messageId) => {
          set((state) => ({
            messages: state.messages.filter(m => m.id !== messageId),
          }));
        },

        clearMessages: () => set({ messages: [] }),

        setActiveSession: (sessionId) => {
          set({ activeSessionId: sessionId });
        },
      }),
      { name: "lobe-chat-store" }
    )
  )
);
```

## Custom Agent/Assistant Configuration

### Agent Schema

```typescript
interface Agent {
  id: string;
  name: string;
  description: string;
  avatar: string;
  systemPrompt: string;

  // Model configuration
  model: {
    provider: string;
    id: string;
    temperature: number;
    maxTokens: number;
    topP: number;
    frequencyPenalty: number;
    presencePenalty: number;
  };

  // Capabilities
  plugins: string[];           // Enabled plugin IDs
  files: boolean;              // File upload support
  knowledge: string[];         // Knowledge base IDs
  tts: TTSConfig | null;       // Text-to-speech config

  // Behavior
  tags: string[];
  category: string;
  visibility: "public" | "private";
}
```

### Creating Custom Agents

```typescript
const codeReviewAgent: Agent = {
  id: "code-review-agent",
  name: "Code Review Expert",
  description: "Expert code reviewer focusing on security and performance",
  avatar: "🔍",
  systemPrompt: `You are an expert code reviewer. When reviewing code:
1. Check for security vulnerabilities (OWASP Top 10)
2. Identify performance bottlenecks
3. Suggest improvements with specific code examples
4. Rate each finding as Critical/High/Medium/Low
5. Always explain WHY something is a problem, not just WHAT`,
  model: {
    provider: "anthropic",
    id: "claude-sonnet-4-20250514",
    temperature: 0.3,
    maxTokens: 8192,
    topP: 0.9,
    frequencyPenalty: 0,
    presencePenalty: 0,
  },
  plugins: [],
  files: true,
  knowledge: [],
  tts: null,
  tags: ["development", "code-review", "security"],
  category: "development",
  visibility: "private",
};
```

## Custom Component Development

### Chat Bubble Customization

```typescript
// components/ChatBubble/index.tsx
import { memo } from "react";
import { useTheme } from "@lobehub/ui";

interface ChatBubbleProps {
  role: "user" | "assistant";
  content: string;
  timestamp: number;
  actions?: React.ReactNode;
}

export const ChatBubble = memo<ChatBubbleProps>(
  ({ role, content, timestamp, actions }) => {
    const theme = useTheme();

    const isUser = role === "user";

    return (
      <div style={{
        display: "flex",
        flexDirection: isUser ? "row-reverse" : "row",
        gap: "12px",
        maxWidth: "80%",
        alignSelf: isUser ? "flex-end" : "flex-start",
      }}>
        <div style={{
          padding: "12px 16px",
          borderRadius: theme.borderRadius,
          backgroundColor: isUser
            ? theme.chatBubbleUserBg
            : theme.chatBubbleBg,
          color: theme.colorText,
        }}>
          <div dangerouslySetInnerHTML={{
            __html: renderMarkdown(content)
          }} />
          <div style={{
            fontSize: "12px",
            color: theme.colorTextSecondary,
            marginTop: "4px",
          }}>
            {new Date(timestamp).toLocaleTimeString()}
          </div>
        </div>
        {actions && (
          <div style={{ opacity: 0, transition: "opacity 0.2s" }}>
            {actions}
          </div>
        )}
      </div>
    );
  }
);
```

## Environment Configuration

```typescript
// Custom environment overrides
// .env.local
NEXT_PUBLIC_BASE_PATH=/chat
NEXT_PUBLIC_CUSTOM_MODELS=my-model-1,my-model-2
NEXT_PUBLIC_DEFAULT_AGENT_CONFIG={"model":"claude-sonnet-4-20250514","temperature":0.7}
NEXT_PUBLIC_ENABLE_KNOWLEDGE_BASE=true
NEXT_PUBLIC_ANALYTICS_ID=UA-XXXXX
```

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| **Theme Engine** | Ant Design tokens + CSS variables for complete visual customization |
| **i18n** | 20+ languages via react-i18next with namespace-based translation files |
| **Monorepo** | pnpm workspaces with shared packages (@lobehub/ui, icons, tts) |
| **State Management** | Zustand with slices pattern and persistence middleware |
| **Agents** | JSON-configurable with system prompts, model settings, and plugins |
| **Components** | React components with theme-aware styling via token system |

---

**Next Steps**: [Chapter 8: Scaling & Performance](08-scaling-performance.md) — Optimize LobeChat for production with caching, database tuning, and edge deployment.

---

*Built with insights from the [LobeChat repository](https://github.com/lobehub/lobe-chat) and community documentation.*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `theme`, `lobe`, `chat` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Advanced Customization` as an operating subsystem inside **LobeChat AI Platform: Deep Dive Tutorial**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `state`, `locales`, `messages` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Advanced Customization` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `theme`.
2. **Input normalization**: shape incoming data so `lobe` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `chat`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LobeChat](https://github.com/lobehub/lobe-chat)
  Why it matters: authoritative reference on `LobeChat` (github.com).

Suggested trace strategy:
- search upstream code for `theme` and `lobe` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Plugin Development](06-plugin-development.md)
- [Next Chapter: Chapter 8: Scaling & Performance](08-scaling-performance.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
