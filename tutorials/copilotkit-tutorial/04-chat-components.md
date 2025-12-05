---
layout: default
title: "CopilotKit Tutorial - Chapter 4: Chat Components"
nav_order: 4
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 4: Chat Components - Building Chat Interfaces with CopilotChat and CopilotSidebar

> Master CopilotKit's chat UI components for creating conversational AI interfaces in your React applications.

## Overview

CopilotKit provides pre-built chat components that make it easy to add conversational AI interfaces to your applications. This chapter covers CopilotSidebar, CopilotChat, and how to customize these components.

## CopilotSidebar Component

### Basic Sidebar Implementation

```tsx
// app/components/BasicSidebar.tsx
"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

export function BasicSidebar() {
  const [messages, setMessages] = useState<string[]>([]);

  // Share conversation history
  useCopilotReadable({
    description: "The conversation history with the user",
    value: messages,
  });

  // Action to add a message
  useCopilotAction({
    name: "addMessage",
    description: "Add a message to the conversation",
    parameters: [
      {
        name: "message",
        type: "string",
        description: "The message content to add",
        required: true,
      },
    ],
    handler: async ({ message }) => {
      setMessages(prev => [...prev, message]);
      return { success: true, messageCount: messages.length + 1 };
    },
  });

  return (
    <CopilotSidebar
      defaultOpen={true}
      clickOutsideToClose={false}
    >
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Basic Chat Interface</h1>

        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">Conversation History</h3>
            {messages.length === 0 ? (
              <p className="text-blue-700">No messages yet. Start a conversation!</p>
            ) : (
              <ul className="space-y-1">
                {messages.map((message, index) => (
                  <li key={index} className="text-blue-800 text-sm">
                    • {message}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2">Try These Commands:</h3>
            <ul className="text-green-800 text-sm space-y-1">
              <li>• "Add a message saying 'Hello from the sidebar!'"</li>
              <li>• "Add three messages about different topics"</li>
              <li>• "Show me how many messages we have"</li>
            </ul>
          </div>
        </div>
      </div>
    </CopilotSidebar>
  );
}
```

### Sidebar Customization

```tsx
// app/components/CustomSidebar.tsx
"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

export function CustomSidebar() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [theme, setTheme] = useState<"light" | "dark">("light");

  // Share sidebar state
  useCopilotReadable({
    description: "Current sidebar visibility and theme settings",
    value: { isOpen: sidebarOpen, theme },
  });

  // Action to control sidebar
  useCopilotAction({
    name: "toggleSidebar",
    description: "Open or close the sidebar",
    parameters: [
      {
        name: "action",
        type: "string",
        description: "Action to perform: 'open', 'close', or 'toggle'",
        enum: ["open", "close", "toggle"],
        default: "toggle",
      },
    ],
    handler: async ({ action }) => {
      if (action === "open") {
        setSidebarOpen(true);
      } else if (action === "close") {
        setSidebarOpen(false);
      } else if (action === "toggle") {
        setSidebarOpen(prev => !prev);
      }

      return { success: true, isOpen: sidebarOpen };
    },
  });

  // Action to change theme
  useCopilotAction({
    name: "changeTheme",
    description: "Change the sidebar theme",
    parameters: [
      {
        name: "newTheme",
        type: "string",
        description: "New theme to apply",
        enum: ["light", "dark"],
        required: true,
      },
    ],
    handler: async ({ newTheme }) => {
      setTheme(newTheme);
      return { success: true, theme: newTheme };
    },
  });

  return (
    <div className={`min-h-screen ${theme === "dark" ? "bg-gray-900 text-white" : "bg-gray-50 text-gray-900"}`}>
      {/* Custom trigger button */}
      <button
        onClick={() => setSidebarOpen(true)}
        className="fixed top-4 right-4 z-50 px-4 py-2 bg-blue-500 text-white rounded-lg shadow-lg hover:bg-blue-600"
      >
        Open AI Assistant
      </button>

      <CopilotSidebar
        open={sidebarOpen}
        onOpenChange={setSidebarOpen}
        className={theme === "dark" ? "dark" : ""}
      >
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold">Custom AI Assistant</h1>
            <div className="flex gap-2">
              <button
                onClick={() => setTheme(theme === "light" ? "dark" : "light")}
                className="px-3 py-1 text-sm bg-gray-200 rounded hover:bg-gray-300"
              >
                {theme === "light" ? "🌙" : "☀️"}
              </button>
              <button
                onClick={() => setSidebarOpen(false)}
                className="px-3 py-1 text-sm bg-red-200 text-red-800 rounded hover:bg-red-300"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="space-y-4">
            <div className={`p-4 rounded-lg ${theme === "dark" ? "bg-gray-800" : "bg-blue-50"}`}>
              <h3 className={`font-semibold mb-2 ${theme === "dark" ? "text-blue-300" : "text-blue-900"}`}>
                Current Settings
              </h3>
              <div className={`text-sm ${theme === "dark" ? "text-gray-300" : "text-gray-700"}`}>
                <p>Theme: {theme}</p>
                <p>Sidebar: {sidebarOpen ? "Open" : "Closed"}</p>
              </div>
            </div>

            <div className={`p-4 rounded-lg ${theme === "dark" ? "bg-gray-800" : "bg-green-50"}`}>
              <h3 className={`font-semibold mb-2 ${theme === "dark" ? "text-green-300" : "text-green-900"}`}>
                Try These Commands:
              </h3>
              <ul className={`text-sm space-y-1 ${theme === "dark" ? "text-gray-300" : "text-green-800"}`}>
                <li>• "Toggle the sidebar"</li>
                <li>• "Change theme to dark"</li>
                <li>• "Close the sidebar"</li>
                <li>• "What theme are we using?"</li>
              </ul>
            </div>
          </div>
        </div>
      </CopilotSidebar>

      {/* Main content */}
      <main className="p-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-4xl font-bold mb-6">Welcome to AI-Powered App</h1>
          <p className={`text-lg mb-8 ${theme === "dark" ? "text-gray-300" : "text-gray-600"}`}>
            Click the "Open AI Assistant" button to start chatting with AI about your application.
          </p>

          <div className={`p-6 rounded-lg ${theme === "dark" ? "bg-gray-800" : "bg-white"} shadow-lg`}>
            <h2 className="text-2xl font-semibold mb-4">Features</h2>
            <ul className={`space-y-2 ${theme === "dark" ? "text-gray-300" : "text-gray-700"}`}>
              <li>✅ AI-powered chat interface</li>
              <li>✅ Customizable themes</li>
              <li>✅ Context-aware conversations</li>
              <li>✅ Voice and text input</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
```

## CopilotChat Component

### Inline Chat Implementation

```tsx
// app/components/InlineChat.tsx
"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

interface Document {
  id: string;
  title: string;
  content: string;
  category: string;
}

export function InlineChat() {
  const [documents, setDocuments] = useState<Document[]>([
    {
      id: "1",
      title: "Getting Started Guide",
      content: "Welcome to our platform. This guide will help you get started...",
      category: "tutorial"
    },
    {
      id: "2",
      title: "API Reference",
      content: "Complete API reference for developers...",
      category: "reference"
    }
  ]);

  // Share documents for AI context
  useCopilotReadable({
    description: "Available documentation and knowledge base articles",
    value: documents,
  });

  // Action to search documents
  useCopilotAction({
    name: "searchDocuments",
    description: "Search through available documents",
    parameters: [
      {
        name: "query",
        type: "string",
        description: "Search query to find relevant documents",
        required: true,
      },
      {
        name: "category",
        type: "string",
        description: "Optional category filter",
        enum: ["tutorial", "reference", "guide"],
      },
    ],
    handler: async ({ query, category }) => {
      let results = documents.filter(doc =>
        doc.title.toLowerCase().includes(query.toLowerCase()) ||
        doc.content.toLowerCase().includes(query.toLowerCase())
      );

      if (category) {
        results = results.filter(doc => doc.category === category);
      }

      return {
        query,
        category,
        resultsCount: results.length,
        results: results.map(doc => ({
          id: doc.id,
          title: doc.title,
          category: doc.category,
          preview: doc.content.substring(0, 100) + "..."
        })),
      };
    },
  });

  // Action to add new document
  useCopilotAction({
    name: "addDocument",
    description: "Add a new document to the knowledge base",
    parameters: [
      {
        name: "title",
        type: "string",
        description: "Document title",
        required: true,
      },
      {
        name: "content",
        type: "string",
        description: "Document content",
        required: true,
      },
      {
        name: "category",
        type: "string",
        description: "Document category",
        enum: ["tutorial", "reference", "guide"],
        required: true,
      },
    ],
    handler: async ({ title, content, category }) => {
      const newDoc: Document = {
        id: Date.now().toString(),
        title,
        content,
        category,
      };

      setDocuments(prev => [...prev, newDoc]);

      return {
        success: true,
        document: {
          id: newDoc.id,
          title: newDoc.title,
          category: newDoc.category,
        },
      };
    },
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-2xl font-bold text-gray-900">Documentation Portal</h1>
            <div className="text-sm text-gray-500">
              {documents.length} documents available
            </div>
          </div>
        </div>
      </header>

      {/* Main content with inline chat */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Document list */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Available Documents</h2>
            <div className="grid gap-4">
              {documents.map(doc => (
                <div key={doc.id} className="bg-white p-6 rounded-lg shadow-sm border">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-medium text-gray-900">{doc.title}</h3>
                    <span className={`px-2 py-1 text-xs rounded ${
                      doc.category === "tutorial" ? "bg-blue-100 text-blue-800" :
                      doc.category === "reference" ? "bg-green-100 text-green-800" :
                      "bg-purple-100 text-purple-800"
                    }`}>
                      {doc.category}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">
                    {doc.content.substring(0, 150)}...
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Inline chat */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <h2 className="text-xl font-semibold mb-4">AI Assistant</h2>
              <div className="bg-white rounded-lg shadow-sm border h-96">
                <CopilotChat
                  className="h-full"
                  placeholder="Ask me about the documents..."
                  showSuggestions={true}
                  suggestions={[
                    "Search for API documentation",
                    "Add a new tutorial document",
                    "Find guides about authentication"
                  ]}
                />
              </div>

              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <h4 className="text-sm font-medium text-blue-900 mb-1">Try asking:</h4>
                <ul className="text-xs text-blue-800 space-y-1">
                  <li>• "Search for authentication guides"</li>
                  <li>• "Add a document about deployment"</li>
                  <li>• "What tutorial documents do we have?"</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
```

### Advanced Chat Customization

```tsx
// app/components/AdvancedChat.tsx
"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

export function AdvancedChat() {
  const [chatMode, setChatMode] = useState<"casual" | "professional" | "technical">("casual");
  const [conversationHistory, setConversationHistory] = useState<any[]>([]);

  // Share chat configuration
  useCopilotReadable({
    description: "Current chat mode and conversation preferences",
    value: { mode: chatMode, historyLength: conversationHistory.length },
  });

  // Action to change chat mode
  useCopilotAction({
    name: "setChatMode",
    description: "Change the conversation style and tone",
    parameters: [
      {
        name: "mode",
        type: "string",
        description: "Conversation mode to use",
        enum: ["casual", "professional", "technical"],
        required: true,
      },
    ],
    handler: async ({ mode }) => {
      setChatMode(mode);
      return {
        success: true,
        mode,
        description: mode === "casual" ? "Friendly and conversational" :
                    mode === "professional" ? "Formal business communication" :
                    "Technical and detailed explanations"
      };
    },
  });

  // Action to get conversation summary
  useCopilotAction({
    name: "summarizeConversation",
    description: "Provide a summary of our conversation so far",
    parameters: [],
    handler: async () => {
      const summary = {
        totalMessages: conversationHistory.length,
        currentMode: chatMode,
        topics: ["chat customization", "AI assistance", "conversation modes"],
        keyPoints: [
          "Multiple chat modes available",
          "Conversation history tracking",
          "Customizable AI assistance"
        ]
      };

      return summary;
    },
  });

  const getModeConfig = () => {
    switch (chatMode) {
      case "professional":
        return {
          placeholder: "How can I assist you professionally?",
          welcomeMessage: "I'm here to help with your professional needs.",
          suggestions: [
            "Prepare a business proposal",
            "Analyze market trends",
            "Draft professional correspondence"
          ]
        };
      case "technical":
        return {
          placeholder: "What technical problem can I help solve?",
          welcomeMessage: "Ready to dive deep into technical challenges.",
          suggestions: [
            "Debug this error message",
            "Explain this algorithm",
            "Review this code architecture"
          ]
        };
      default: // casual
        return {
          placeholder: "What's on your mind?",
          welcomeMessage: "Hey there! I'm here to chat and help out.",
          suggestions: [
            "Tell me about your project",
            "What's something you're curious about?",
            "Let's brainstorm some ideas"
          ]
        };
    }
  };

  const modeConfig = getModeConfig();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Advanced AI Chat Assistant
            </h1>
            <div className="flex justify-center gap-4 mb-4">
              {["casual", "professional", "technical"].map(mode => (
                <button
                  key={mode}
                  onClick={() => setChatMode(mode as any)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    chatMode === mode
                      ? "bg-indigo-600 text-white"
                      : "bg-white text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  {mode.charAt(0).toUpperCase() + mode.slice(1)}
                </button>
              ))}
            </div>
            <p className="text-lg text-gray-600">
              {modeConfig.welcomeMessage}
            </p>
          </div>

          {/* Chat Interface */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="h-96">
              <CopilotChat
                className="h-full"
                placeholder={modeConfig.placeholder}
                showSuggestions={true}
                suggestions={modeConfig.suggestions}
                onMessage={(message) => {
                  setConversationHistory(prev => [...prev, {
                    role: "user",
                    content: message,
                    timestamp: new Date(),
                    mode: chatMode
                  }]);
                }}
              />
            </div>
          </div>

          {/* Status and Controls */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold text-gray-900 mb-2">Current Mode</h3>
              <p className="text-indigo-600 font-medium capitalize">{chatMode}</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold text-gray-900 mb-2">Conversation</h3>
              <p className="text-gray-600">{conversationHistory.length} messages</p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold text-gray-900 mb-2">AI Status</h3>
              <p className="text-green-600">Online & Ready</p>
            </div>
          </div>

          {/* Help Section */}
          <div className="mt-8 bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Try These Commands:</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Mode Switching:</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "Switch to professional mode"</li>
                  <li>• "Use technical mode for coding questions"</li>
                  <li>• "Change to casual conversation"</li>
                </ul>
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-2">Conversation:</h3>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• "Summarize our conversation"</li>
                  <li>• "What mode are we in?"</li>
                  <li>• "Tell me about your capabilities"</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Custom Chat Components

### Building Custom Chat UI

```tsx
// app/components/CustomChatUI.tsx
"use client";

import { useCopilotChat } from "@copilotkit/react-core";
import { useState, useRef, useEffect } from "react";

export function CustomChatUI() {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { sendMessage, isLoading: chatLoading } = useCopilotChat();

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue("");
    setIsLoading(true);

    // Add user message
    setMessages(prev => [...prev, {
      role: "user",
      content: userMessage,
      timestamp: new Date()
    }]);

    try {
      // Send to CopilotKit
      const response = await sendMessage(userMessage);

      // Add AI response
      setMessages(prev => [...prev, {
        role: "assistant",
        content: response,
        timestamp: new Date()
      }]);
    } catch (error) {
      // Add error message
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date(),
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-6 py-4">
        <h1 className="text-xl font-semibold text-gray-900">Custom AI Chat</h1>
        <p className="text-sm text-gray-600">Powered by CopilotKit</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-20">
            <div className="text-6xl mb-4">💬</div>
            <h3 className="text-lg font-medium mb-2">Start a conversation</h3>
            <p>Type a message below to begin chatting with AI.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.role === "user"
                    ? "bg-blue-500 text-white"
                    : message.isError
                    ? "bg-red-100 text-red-900"
                    : "bg-white text-gray-900 border"
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: "0.1s"}}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: "0.2s"}}></div>
                </div>
                <span className="text-sm text-gray-600">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t px-6 py-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="w-full px-4 py-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={1}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>

        <div className="mt-2 text-xs text-gray-500 text-center">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
}
```

## Summary

In this chapter, we've covered:

- **CopilotSidebar**: Sliding panel chat interface with customization options
- **CopilotChat**: Inline chat components for embedded conversations
- **Advanced Customization**: Themes, custom triggers, and state management
- **Custom Chat UI**: Building completely custom chat interfaces
- **Integration Patterns**: Embedding chat in various application contexts

## Key Takeaways

1. **Component Flexibility**: Choose between sidebar and inline chat components
2. **Full Customization**: Control themes, behavior, and integration points
3. **Context Awareness**: Chat components work with your app's state and actions
4. **User Experience**: Customizable placeholders, suggestions, and welcome messages
5. **Responsive Design**: Components adapt to different screen sizes and contexts
6. **Accessibility**: Built-in keyboard navigation and screen reader support

## Next Steps

Now that you can build chat interfaces, let's explore Generative UI - AI-generated React components.

---

**Ready for Chapter 5?** [Generative UI](05-generative-ui.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*