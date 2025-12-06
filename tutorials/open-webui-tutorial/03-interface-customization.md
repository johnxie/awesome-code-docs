---
layout: default
title: "Open WebUI Tutorial - Chapter 3: Interface Customization"
nav_order: 3
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 3: Interface Customization & Personalization

> Transform Open WebUI into your perfect AI chat interface with custom themes, prompts, and workflows.

## Theme System

### Built-in Themes

Open WebUI comes with several built-in themes:

```javascript
// Available themes
const themes = [
  'default',      // Clean, modern interface
  'dark',         // Dark mode for eye comfort
  'auto',         // Follows system preference
  'custom'        // Fully customizable
];
```

### Custom CSS Themes

Create custom themes using CSS:

```css
/* custom-theme.css */
:root {
  /* Color palette */
  --primary-color: #6366f1;
  --secondary-color: #8b5cf6;
  --background-color: #0f0f23;
  --surface-color: #1a1a2e;
  --text-color: #e2e8f0;
  --text-secondary: #94a3b8;

  /* Chat interface */
  --chat-bubble-user: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --chat-bubble-assistant: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --chat-input-bg: rgba(255, 255, 255, 0.05);

  /* Borders and shadows */
  --border-radius: 12px;
  --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Chat bubbles */
.message.user {
  background: var(--chat-bubble-user);
  color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
}

.message.assistant {
  background: var(--chat-bubble-assistant);
  color: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
}

/* Input area */
.chat-input {
  background: var(--chat-input-bg);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--background-color);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--secondary-color);
}
```

### Theme Configuration

```javascript
// theme-config.json
{
  "name": "Cyberpunk Neon",
  "version": "1.0.0",
  "colors": {
    "primary": "#00ff41",
    "secondary": "#ff0080",
    "accent": "#00ffff",
    "background": "#0a0a0a",
    "surface": "#1a1a1a",
    "text": "#ffffff",
    "text-secondary": "#b0b0b0"
  },
  "fonts": {
    "primary": "JetBrains Mono",
    "secondary": "Inter"
  },
  "effects": {
    "glow": true,
    "animations": true,
    "glassmorphism": true
  }
}
```

## Custom Prompts & Templates

### Prompt Management

```javascript
// Custom prompt templates
const promptTemplates = {
  coding: {
    name: "Code Assistant",
    template: `You are an expert software developer with deep knowledge of multiple programming languages and frameworks.

Context: {context}
Language: {language}
Task: {task}

Please provide:
1. A clear solution with well-commented code
2. Explanation of the approach
3. Potential improvements or alternatives

Code:`,
    variables: ["context", "language", "task"]
  },

  writing: {
    name: "Writing Assistant",
    template: `You are a professional writer and editor skilled in various writing styles and genres.

Style: {style}
Topic: {topic}
Audience: {audience}
Length: {length}

Please write a {style} piece about {topic} for {audience}, approximately {length} words long.

Focus on:
- Engaging introduction
- Clear structure
- Compelling content
- Strong conclusion

Content:`,
    variables: ["style", "topic", "audience", "length"]
  },

  analysis: {
    name: "Data Analyst",
    template: `You are an experienced data analyst skilled in statistical analysis, data visualization, and business intelligence.

Dataset: {dataset_description}
Analysis Type: {analysis_type}
Key Questions: {questions}

Please provide:
1. Data overview and quality assessment
2. Key findings and insights
3. Visualizations recommendations
4. Actionable recommendations

Analysis:`,
    variables: ["dataset_description", "analysis_type", "questions"]
  }
};
```

### Dynamic Prompt Injection

```javascript
class PromptManager {
  constructor() {
    this.templates = new Map();
    this.variables = new Map();
  }

  registerTemplate(name, template, variables = []) {
    this.templates.set(name, { template, variables });
  }

  setVariable(name, value) {
    this.variables.set(name, value);
  }

  renderPrompt(templateName, customVars = {}) {
    const template = this.templates.get(templateName);
    if (!template) throw new Error(`Template ${templateName} not found`);

    let prompt = template.template;

    // Replace variables from global context
    for (const [key, value] of this.variables) {
      prompt = prompt.replace(new RegExp(`{${key}}`, 'g'), value);
    }

    // Replace custom variables
    for (const [key, value] of Object.entries(customVars)) {
      prompt = prompt.replace(new RegExp(`{${key}}`, 'g'), value);
    }

    return prompt;
  }

  createQuickActions() {
    return {
      "Explain Code": {
        template: "coding",
        variables: {
          context: "selected_code",
          language: "detected_language",
          task: "Explain how this code works"
        }
      },
      "Refactor Code": {
        template: "coding",
        variables: {
          context: "selected_code",
          language: "detected_language",
          task: "Refactor this code for better performance and readability"
        }
      },
      "Write Tests": {
        template: "coding",
        variables: {
          context: "selected_code",
          language: "detected_language",
          task: "Write comprehensive unit tests for this code"
        }
      }
    };
  }
}

// Usage
const promptManager = new PromptManager();

// Register templates
Object.entries(promptTemplates).forEach(([name, config]) => {
  promptManager.registerTemplate(name, config.template, config.variables);
});

// Set global variables
promptManager.setVariable('user_name', 'Alice');
promptManager.setVariable('current_date', new Date().toISOString().split('T')[0]);

// Render prompt
const prompt = promptManager.renderPrompt('coding', {
  context: 'React component for user authentication',
  language: 'TypeScript',
  task: 'Create a secure login form'
});
```

## Custom Workflows & Pipelines

### Chat Workflow Builder

```javascript
class WorkflowBuilder {
  constructor() {
    this.workflows = new Map();
    this.steps = new Map();
  }

  defineStep(name, handler, config = {}) {
    this.steps.set(name, { handler, config });
  }

  createWorkflow(name, steps) {
    this.workflows.set(name, {
      name,
      steps: steps.map(step => ({
        ...step,
        stepDef: this.steps.get(step.step)
      }))
    });
  }

  async executeWorkflow(workflowName, initialInput) {
    const workflow = this.workflows.get(workflowName);
    if (!workflow) throw new Error(`Workflow ${workflowName} not found`);

    let currentInput = initialInput;
    const results = [];

    for (const step of workflow.steps) {
      try {
        const stepDef = step.stepDef;
        const result = await stepDef.handler(currentInput, step.config);
        results.push({ step: step.step, result });

        // Pass result to next step
        currentInput = step.passResult ? result : currentInput;

      } catch (error) {
        console.error(`Step ${step.step} failed:`, error);
        if (step.continueOnError !== true) {
          throw error;
        }
      }
    }

    return results;
  }
}

// Define workflow steps
const builder = new WorkflowBuilder();

// Step: Analyze user intent
builder.defineStep('analyze_intent', async (input) => {
  const response = await generateResponse([
    { role: 'system', content: 'Analyze the user\'s intent and categorize it.' },
    { role: 'user', content: input }
  ]);

  return {
    intent: response.content,
    confidence: 0.85
  };
});

// Step: Route to appropriate handler
builder.defineStep('route_request', async (analysis) => {
  const intent = analysis.intent.toLowerCase();

  if (intent.includes('code')) return 'coding_assistant';
  if (intent.includes('write') || intent.includes('article')) return 'writing_assistant';
  if (intent.includes('analyze') || intent.includes('data')) return 'analysis_assistant';

  return 'general_assistant';
});

// Step: Generate response
builder.defineStep('generate_response', async (input, config) => {
  const assistant = config.assistant || 'general_assistant';
  const prompt = promptManager.renderPrompt(assistant, { query: input });

  return await generateResponse([
    { role: 'system', content: prompt },
    { role: 'user', content: input }
  ]);
});

// Create workflow
builder.createWorkflow('smart_assistant', [
  { step: 'analyze_intent', passResult: true },
  { step: 'route_request', passResult: true, continueOnError: true },
  { step: 'generate_response', passResult: true }
]);

// Execute workflow
const result = await builder.executeWorkflow('smart_assistant', userQuery);
```

### Conditional Response Logic

```javascript
class ConditionalResponder {
  constructor() {
    this.conditions = new Map();
    this.responses = new Map();
  }

  addCondition(name, conditionFn, responseFn) {
    this.conditions.set(name, conditionFn);
    this.responses.set(name, responseFn);
  }

  async respond(input, context = {}) {
    // Check all conditions
    for (const [name, conditionFn] of this.conditions) {
      if (await conditionFn(input, context)) {
        const responseFn = this.responses.get(name);
        return await responseFn(input, context);
      }
    }

    // Default response
    return await this.defaultResponse(input, context);
  }

  async defaultResponse(input, context) {
    return await generateResponse([
      { role: 'user', content: input }
    ]);
  }
}

// Define conditional responses
const responder = new ConditionalResponder();

// Code-related queries
responder.addCondition(
  'code_help',
  (input) => input.toLowerCase().includes('code') || input.includes('function'),
  async (input) => {
    return await generateResponse([
      { role: 'system', content: 'You are a coding assistant. Provide clear, working code examples.' },
      { role: 'user', content: input }
    ]);
  }
);

// Math questions
responder.addCondition(
  'math_help',
  (input) => /\d+[\+\-\*\/]\d+/.test(input) || input.toLowerCase().includes('calculate'),
  async (input) => {
    return await generateResponse([
      { role: 'system', content: 'You are a math tutor. Show your work and explain each step.' },
      { role: 'user', content: input }
    ]);
  }
);

// File upload handling
responder.addCondition(
  'file_upload',
  (input, context) => context.hasFileUpload === true,
  async (input, context) => {
    const fileAnalysis = await analyzeFile(context.uploadedFile);
    return await generateResponse([
      { role: 'system', content: `File uploaded: ${fileAnalysis.description}. Provide relevant assistance.` },
      { role: 'user', content: input }
    ]);
  }
);
```

## Custom Chat Commands

### Command System

```javascript
class ChatCommandSystem {
  constructor() {
    this.commands = new Map();
    this.aliases = new Map();
  }

  registerCommand(name, handler, options = {}) {
    this.commands.set(name, {
      handler,
      description: options.description || '',
      usage: options.usage || '',
      aliases: options.aliases || []
    });

    // Register aliases
    if (options.aliases) {
      options.aliases.forEach(alias => {
        this.aliases.set(alias, name);
      });
    }
  }

  async executeCommand(input, context = {}) {
    const trimmed = input.trim();

    // Check if it's a command (starts with /)
    if (!trimmed.startsWith('/')) {
      return null; // Not a command
    }

    const parts = trimmed.slice(1).split(' ');
    const commandName = parts[0].toLowerCase();
    const args = parts.slice(1);

    // Resolve alias
    const actualCommand = this.aliases.get(commandName) || commandName;

    const command = this.commands.get(actualCommand);
    if (!command) {
      throw new Error(`Unknown command: ${commandName}`);
    }

    return await command.handler(args, context);
  }

  getHelp() {
    const help = ['Available commands:'];

    for (const [name, command] of this.commands) {
      const aliases = command.aliases.length > 0 ? ` (${command.aliases.join(', ')})` : '';
      help.push(`/${name}${aliases} - ${command.description}`);
      if (command.usage) {
        help.push(`  Usage: ${command.usage}`);
      }
    }

    return help.join('\n');
  }
}

// Register commands
const commands = new ChatCommandSystem();

// Help command
commands.registerCommand('help', async () => {
  return commands.getHelp();
}, {
  description: 'Show available commands'
});

// Clear chat
commands.registerCommand('clear', async (args, context) => {
  context.clearChat();
  return 'Chat cleared.';
}, {
  description: 'Clear the current chat'
});

// Model switch
commands.registerCommand('model', async (args) => {
  const modelName = args[0];
  if (!modelName) {
    return 'Current model: ' + getCurrentModel();
  }

  await switchModel(modelName);
  return `Switched to model: ${modelName}`;
}, {
  description: 'Switch or show current model',
  usage: '/model [model_name]',
  aliases: ['m']
});

// Save conversation
commands.registerCommand('save', async (args, context) => {
  const filename = args[0] || `chat_${Date.now()}.json`;
  await saveConversation(context.chatHistory, filename);
  return `Conversation saved as ${filename}`;
}, {
  description: 'Save current conversation',
  usage: '/save [filename]',
  aliases: ['export']
});

// Time command
commands.registerCommand('time', async () => {
  return `Current time: ${new Date().toLocaleString()}`;
}, {
  description: 'Show current time'
});

// Usage command
commands.registerCommand('usage', async (args, context) => {
  const stats = context.getUsageStats();
  return `Tokens used: ${stats.totalTokens}\nCost: $${stats.totalCost.toFixed(4)}`;
}, {
  description: 'Show usage statistics'
});
```

### Advanced Command Features

```javascript
// Command chaining and piping
class AdvancedCommandSystem extends ChatCommandSystem {
  async executeCommand(input, context = {}) {
    // Support for command chaining with |
    if (input.includes('|')) {
      const commands = input.split('|').map(cmd => cmd.trim());
      let result = null;

      for (const cmd of commands) {
        if (result !== null) {
          // Pass previous result as input to next command
          result = await this.executeSingleCommand(`${cmd} ${result}`, context);
        } else {
          result = await this.executeSingleCommand(cmd, context);
        }
      }

      return result;
    }

    return await this.executeSingleCommand(input, context);
  }

  async executeSingleCommand(input, context) {
    // Original command execution logic
    return await super.executeCommand(input, context);
  }
}

// Variable system
class VariableSystem {
  constructor() {
    this.variables = new Map();
  }

  set(name, value) {
    this.variables.set(name, value);
  }

  get(name) {
    return this.variables.get(name);
  }

  interpolate(text) {
    return text.replace(/\$(\w+)/g, (match, varName) => {
      return this.get(varName) || match;
    });
  }
}

// Enhanced commands with variables
const vars = new VariableSystem();

// Set variable command
commands.registerCommand('set', async (args) => {
  const [name, ...valueParts] = args;
  const value = valueParts.join(' ');
  vars.set(name, value);
  return `Set $${name} = ${value}`;
}, {
  description: 'Set a variable',
  usage: '/set <name> <value>'
});

// Get variable command
commands.registerCommand('get', async (args) => {
  const name = args[0];
  const value = vars.get(name);
  return value ? `$${name} = ${value}` : `Variable $${name} not found`;
}, {
  description: 'Get a variable value',
  usage: '/get <name>'
});

// Use variables in prompts
commands.registerCommand('prompt', async (args, context) => {
  const templateName = args[0];
  const interpolatedPrompt = vars.interpolate(args.slice(1).join(' '));

  const response = await generateResponse([
    { role: 'system', content: promptManager.renderPrompt(templateName) },
    { role: 'user', content: interpolatedPrompt }
  ]);

  return response.content;
}, {
  description: 'Use a prompt template with variable interpolation',
  usage: '/prompt <template> <message with $variables>'
});
```

## Plugin System

### Custom Plugin Architecture

```javascript
class PluginSystem {
  constructor() {
    this.plugins = new Map();
    this.hooks = new Map();
  }

  registerPlugin(name, plugin) {
    this.plugins.set(name, plugin);

    // Register hooks
    if (plugin.hooks) {
      for (const [hookName, hookFn] of Object.entries(plugin.hooks)) {
        if (!this.hooks.has(hookName)) {
          this.hooks.set(hookName, []);
        }
        this.hooks.get(hookName).push({ plugin: name, fn: hookFn });
      }
    }
  }

  async executeHook(hookName, ...args) {
    const hooks = this.hooks.get(hookName) || [];

    for (const hook of hooks) {
      try {
        await hook.fn(...args);
      } catch (error) {
        console.error(`Plugin ${hook.plugin} hook ${hookName} failed:`, error);
      }
    }
  }

  getPlugin(name) {
    return this.plugins.get(name);
  }
}

// Example plugin
const codeHighlightPlugin = {
  name: 'code_highlighter',
  version: '1.0.0',

  hooks: {
    'message_rendered': async (messageElement, message) => {
      // Add syntax highlighting to code blocks
      const codeBlocks = messageElement.querySelectorAll('pre code');
      codeBlocks.forEach(block => {
        // Apply syntax highlighting
        hljs.highlightElement(block);
      });
    },

    'before_send': async (message) => {
      // Preprocess code in user messages
      if (message.includes('```')) {
        // Add language hints if missing
        message = message.replace(/```(\w+)?\n/g, (match, lang) => {
          return lang ? match : '```python\n';
        });
      }
      return message;
    }
  },

  commands: {
    'highlight': {
      description: 'Toggle syntax highlighting',
      handler: async () => {
        // Toggle highlighting feature
      }
    }
  }
};

// Register plugin
const plugins = new PluginSystem();
plugins.registerPlugin('code_highlighter', codeHighlightPlugin);
```

### Theme Plugin Example

```javascript
const darkThemePlugin = {
  name: 'dark_theme_enhancer',
  version: '1.0.0',

  hooks: {
    'interface_loaded': async () => {
      // Apply dark theme enhancements
      const style = document.createElement('style');
      style.textContent = `
        .chat-container {
          background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        }

        .message.user {
          background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%);
          box-shadow: 0 4px 15px rgba(15, 52, 96, 0.3);
        }

        .message.assistant {
          background: linear-gradient(135deg, #e94560 0%, #0f3460 100%);
          box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
        }
      `;
      document.head.appendChild(style);
    },

    'theme_changed': async (newTheme) => {
      if (newTheme === 'dark') {
        // Apply additional dark theme customizations
        document.body.classList.add('enhanced-dark');
      } else {
        document.body.classList.remove('enhanced-dark');
      }
    }
  }
};

plugins.registerPlugin('dark_theme_enhancer', darkThemePlugin);
```

## Keyboard Shortcuts & Accessibility

### Custom Keyboard Shortcuts

```javascript
class KeyboardShortcutManager {
  constructor() {
    this.shortcuts = new Map();
    this.activeModifiers = new Set();

    document.addEventListener('keydown', this.handleKeyDown.bind(this));
    document.addEventListener('keyup', this.handleKeyUp.bind(this));
  }

  registerShortcut(keys, callback, description = '') {
    const keyCombo = this.normalizeKeyCombo(keys);
    this.shortcuts.set(keyCombo, { callback, description });
  }

  normalizeKeyCombo(keys) {
    // Convert to sorted, normalized format
    const parts = keys.toLowerCase().split('+').map(k => k.trim());
    return parts.sort().join('+');
  }

  handleKeyDown(event) {
    // Track modifier keys
    if (['Control', 'Alt', 'Shift', 'Meta'].includes(event.key)) {
      this.activeModifiers.add(event.key.toLowerCase());
      return;
    }

    // Build current key combo
    const modifiers = Array.from(this.activeModifiers).sort();
    const keyCombo = [...modifiers, event.key.toLowerCase()].join('+');

    const shortcut = this.shortcuts.get(keyCombo);
    if (shortcut) {
      event.preventDefault();
      shortcut.callback(event);
    }
  }

  handleKeyUp(event) {
    if (['Control', 'Alt', 'Shift', 'Meta'].includes(event.key)) {
      this.activeModifiers.delete(event.key.toLowerCase());
    }
  }

  getHelp() {
    const help = ['Keyboard Shortcuts:'];

    for (const [combo, shortcut] of this.shortcuts) {
      if (shortcut.description) {
        help.push(`${combo}: ${shortcut.description}`);
      }
    }

    return help.join('\n');
  }
}

// Register shortcuts
const shortcuts = new KeyboardShortcutManager();

// Navigation
shortcuts.registerShortcut('ctrl+k', () => {
  // Focus search/command input
  document.querySelector('.command-input').focus();
}, 'Focus command input');

shortcuts.registerShortcut('ctrl+l', () => {
  // Clear chat
  clearChat();
}, 'Clear current chat');

shortcuts.registerShortcut('ctrl+enter', () => {
  // Send message
  sendMessage();
}, 'Send message');

// Model switching
shortcuts.registerShortcut('ctrl+1', () => switchModel('gpt-4'), 'Switch to GPT-4');
shortcuts.registerShortcut('ctrl+2', () => switchModel('claude-3'), 'Switch to Claude-3');
shortcuts.registerShortcut('ctrl+3', () => switchModel('ollama'), 'Switch to local model');

// UI controls
shortcuts.registerShortcut('ctrl+b', () => toggleSidebar(), 'Toggle sidebar');
shortcuts.registerShortcut('ctrl+shift+c', () => copyLastResponse(), 'Copy last response');
shortcuts.registerShortcut('ctrl+shift+s', () => saveChat(), 'Save current chat');
```

### Accessibility Features

```javascript
class AccessibilityManager {
  constructor() {
    this.highContrast = false;
    this.largeText = false;
    this.screenReader = false;

    this.initAccessibility();
  }

  initAccessibility() {
    // Add ARIA labels and roles
    this.addAriaLabels();

    // Keyboard navigation
    this.enableKeyboardNavigation();

    // Focus management
    this.manageFocus();

    // Screen reader support
    this.setupScreenReaderSupport();
  }

  addAriaLabels() {
    // Add ARIA labels to interactive elements
    const elements = [
      { selector: '.chat-input', label: 'Chat message input' },
      { selector: '.send-button', label: 'Send message' },
      { selector: '.model-selector', label: 'Select AI model' },
      { selector: '.new-chat-button', label: 'Start new conversation' }
    ];

    elements.forEach(({ selector, label }) => {
      const element = document.querySelector(selector);
      if (element) {
        element.setAttribute('aria-label', label);
      }
    });
  }

  enableKeyboardNavigation() {
    // Make all interactive elements keyboard accessible
    const focusableElements = document.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    focusableElements.forEach(element => {
      element.setAttribute('tabindex', '0');
    });

    // Chat navigation with arrow keys
    document.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowUp' && event.ctrlKey) {
        event.preventDefault();
        this.navigateChat('up');
      } else if (event.key === 'ArrowDown' && event.ctrlKey) {
        event.preventDefault();
        this.navigateChat('down');
      }
    });
  }

  navigateChat(direction) {
    const messages = document.querySelectorAll('.message');
    const focusedMessage = document.activeElement.closest('.message');

    if (!focusedMessage) {
      // Focus first message
      messages[0]?.focus();
      return;
    }

    const currentIndex = Array.from(messages).indexOf(focusedMessage);
    const nextIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;

    if (nextIndex >= 0 && nextIndex < messages.length) {
      messages[nextIndex].focus();
    }
  }

  manageFocus() {
    // Trap focus in modals
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Tab') {
        const modal = document.querySelector('.modal.active');
        if (modal) {
          this.trapFocusInModal(modal, event);
        }
      }
    });
  }

  trapFocusInModal(modal, event) {
    const focusableElements = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (event.shiftKey) {
      if (document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  }

  setupScreenReaderSupport() {
    // Announce dynamic content changes
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          // Announce new messages
          const newMessages = Array.from(mutation.addedNodes)
            .filter(node => node.classList?.contains('message'));

          if (newMessages.length > 0) {
            this.announceToScreenReader('New message received');
          }
        }
      });
    });

    observer.observe(document.querySelector('.chat-container'), {
      childList: true,
      subtree: true
    });
  }

  announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }

  toggleHighContrast() {
    this.highContrast = !this.highContrast;
    document.body.classList.toggle('high-contrast', this.highContrast);
  }

  toggleLargeText() {
    this.largeText = !this.largeText;
    document.body.classList.toggle('large-text', this.largeText);
  }
}

// Initialize accessibility
const accessibility = new AccessibilityManager();
```

This comprehensive customization system transforms Open WebUI from a basic chat interface into a powerful, personalized AI assistant tailored to your specific needs and preferences. 🚀