---
layout: default
title: "Chapter 8: Custom Development"
parent: "SillyTavern Tutorial"
nav_order: 8
---

# Chapter 8: Custom Development

Welcome to **Chapter 8: Custom Development**. In this part of **SillyTavern Tutorial: Advanced LLM Frontend for Power Users**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Learn to create custom extensions, themes, and integrations for SillyTavern.

## Overview

SillyTavern's extensible architecture allows developers to create powerful additions. This chapter covers the extension API, creating themes, building integrations, and contributing to the project.

## Extension Development

### Extension Structure

```
my-extension/
├── manifest.json         # Extension metadata and config
├── index.js              # Main extension logic
├── settings.html         # Settings UI template
├── styles.css           # Extension styles
├── lib/                 # Dependencies
│   └── helper.js
└── assets/              # Images, icons
    └── icon.svg
```

### Creating a Basic Extension

```javascript
// manifest.json
{
  "name": "My Custom Extension",
  "version": "1.0.0",
  "description": "A custom extension for SillyTavern",
  "author": "Your Name",

  "main": "index.js",
  "css": "styles.css",
  "settings": "settings.html",

  "requires": {
    "minVersion": "1.10.0"
  },

  "hooks": [
    "onMessage",
    "onCharacterLoad",
    "onChatChanged"
  ],

  "api_version": 2
}
```

```javascript
// index.js - Extension entry point
(function() {
  // Extension state
  const state = {
    enabled: true,
    settings: {}
  };

  // Extension API reference
  const api = window.SillyTavern;

  // Initialize extension
  async function init() {
    console.log('[MyExtension] Initializing...');

    // Load saved settings
    state.settings = await loadSettings();

    // Register hooks
    api.hooks.register('onMessage', onMessageHandler);
    api.hooks.register('onCharacterLoad', onCharacterLoadHandler);

    // Add UI elements
    addUIElements();

    console.log('[MyExtension] Initialized');
  }

  // Message handler hook
  function onMessageHandler(message) {
    if (!state.enabled) return message;

    // Process message
    console.log('[MyExtension] Message received:', message);

    // Return modified message (or original)
    return {
      ...message,
      metadata: {
        ...message.metadata,
        processedBy: 'MyExtension'
      }
    };
  }

  // Character load handler
  function onCharacterLoadHandler(character) {
    console.log('[MyExtension] Character loaded:', character.name);

    // Perform character-specific setup
    setupForCharacter(character);
  }

  // Add UI elements
  function addUIElements() {
    // Add toolbar button
    api.ui.addToolbarButton({
      id: 'my-extension-btn',
      icon: 'assets/icon.svg',
      tooltip: 'My Extension',
      onClick: togglePanel
    });

    // Add settings panel
    api.ui.addSettingsSection({
      id: 'my-extension-settings',
      title: 'My Extension',
      content: document.getElementById('my-extension-settings-template')
    });
  }

  // Toggle extension panel
  function togglePanel() {
    const panel = document.getElementById('my-extension-panel');
    panel.classList.toggle('visible');
  }

  // Settings management
  async function loadSettings() {
    const saved = await api.storage.get('my_extension_settings');
    return saved || getDefaultSettings();
  }

  async function saveSettings(settings) {
    await api.storage.set('my_extension_settings', settings);
    state.settings = settings;
  }

  function getDefaultSettings() {
    return {
      enabled: true,
      option1: 'default',
      option2: false
    };
  }

  // Initialize on load
  api.ready(init);

  // Export for debugging
  window.MyExtension = { state, togglePanel };
})();
```

### Extension API Reference

```javascript
// SillyTavern Extension API
const ExtensionAPI = {
  // Hooks - Register callbacks for events
  hooks: {
    // Available hooks
    events: [
      'onMessage',           // When message is sent/received
      'onCharacterLoad',     // When character is loaded
      'onChatChanged',       // When chat switches
      'onSettingsOpen',      // When settings panel opens
      'onPreGenerate',       // Before AI generates response
      'onPostGenerate',      // After AI generates response
      'onTokenCount',        // When tokens are counted
      'onUIReady'            // When UI is fully loaded
    ],

    register(event, callback, priority = 0) {
      // Register callback for event
    },

    unregister(event, callback) {
      // Remove callback from event
    }
  },

  // UI - Add UI elements
  ui: {
    addToolbarButton(config) {
      // Add button to toolbar
    },

    addSettingsSection(config) {
      // Add section to settings panel
    },

    addContextMenuItem(config) {
      // Add item to right-click menu
    },

    showNotification(message, type = 'info') {
      // Show notification to user
    },

    showModal(config) {
      // Show modal dialog
    }
  },

  // Storage - Persistent storage
  storage: {
    async get(key) {
      // Get stored value
    },

    async set(key, value) {
      // Store value
    },

    async delete(key) {
      // Remove stored value
    }
  },

  // Characters - Character management
  characters: {
    getCurrent() {
      // Get current character
    },

    getById(id) {
      // Get character by ID
    },

    getAll() {
      // Get all characters
    }
  },

  // Chat - Chat management
  chat: {
    getCurrent() {
      // Get current chat
    },

    getMessages() {
      // Get chat messages
    },

    sendMessage(content, options = {}) {
      // Send message
    },

    insertMessage(content, position = 'end') {
      // Insert message at position
    }
  },

  // Generation - AI generation control
  generation: {
    generate(prompt, options = {}) {
      // Generate AI response
    },

    stop() {
      // Stop current generation
    },

    getSettings() {
      // Get generation settings
    }
  }
};
```

## Theme Development

### Theme Structure

```css
/* styles.css - Complete theme */

/* Color Variables */
:root {
  /* Primary palette */
  --theme-primary: #7c3aed;
  --theme-primary-light: #a78bfa;
  --theme-primary-dark: #5b21b6;

  /* Background colors */
  --theme-bg-primary: #0f0f1a;
  --theme-bg-secondary: #1a1a2e;
  --theme-bg-tertiary: #252540;

  /* Text colors */
  --theme-text-primary: #f8fafc;
  --theme-text-secondary: #cbd5e1;
  --theme-text-muted: #64748b;

  /* Accent colors */
  --theme-accent-success: #22c55e;
  --theme-accent-warning: #f59e0b;
  --theme-accent-error: #ef4444;

  /* Sizes */
  --theme-radius: 12px;
  --theme-radius-small: 6px;
  --theme-spacing: 16px;
}

/* Main Container */
body {
  background: var(--theme-bg-primary);
  color: var(--theme-text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Chat Container */
#chat-container {
  background: var(--theme-bg-secondary);
  border-radius: var(--theme-radius);
  padding: var(--theme-spacing);
}

/* Messages */
.message {
  padding: var(--theme-spacing);
  border-radius: var(--theme-radius);
  margin-bottom: var(--theme-spacing);
  animation: fadeIn 0.3s ease;
}

.message-user {
  background: linear-gradient(135deg, var(--theme-primary), var(--theme-primary-dark));
  margin-left: 15%;
  color: white;
}

.message-bot {
  background: var(--theme-bg-tertiary);
  margin-right: 15%;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Character Avatar */
.character-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 3px solid var(--theme-primary);
  box-shadow: 0 0 15px rgba(124, 58, 237, 0.3);
}

/* Input Area */
#chat-input-container {
  background: var(--theme-bg-secondary);
  border-radius: var(--theme-radius);
  padding: var(--theme-spacing);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

#chat-input {
  background: var(--theme-bg-tertiary);
  border: none;
  color: var(--theme-text-primary);
  padding: 12px 16px;
  border-radius: var(--theme-radius-small);
  width: 100%;
  resize: none;
}

#chat-input:focus {
  outline: 2px solid var(--theme-primary);
}

/* Send Button */
.send-button {
  background: var(--theme-primary);
  border: none;
  color: white;
  padding: 12px 24px;
  border-radius: var(--theme-radius-small);
  cursor: pointer;
  transition: all 0.2s ease;
}

.send-button:hover {
  background: var(--theme-primary-light);
  transform: translateY(-2px);
}

/* Sidebar */
#sidebar {
  background: var(--theme-bg-secondary);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Character Cards */
.character-card {
  background: var(--theme-bg-tertiary);
  border-radius: var(--theme-radius);
  padding: var(--theme-spacing);
  cursor: pointer;
  transition: all 0.2s ease;
}

.character-card:hover {
  transform: translateX(5px);
  border-left: 3px solid var(--theme-primary);
}

.character-card.active {
  background: rgba(124, 58, 237, 0.2);
  border-left: 3px solid var(--theme-primary);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--theme-bg-primary);
}

::-webkit-scrollbar-thumb {
  background: var(--theme-primary);
  border-radius: 4px;
}
```

### Theme Configuration

```javascript
// theme-config.js - Theme customization options
const themeConfig = {
  name: "Cosmic Purple",
  version: "1.0.0",
  author: "Developer Name",

  // Customizable variables
  variables: {
    primary: {
      label: "Primary Color",
      type: "color",
      default: "#7c3aed"
    },
    background: {
      label: "Background",
      type: "color",
      default: "#0f0f1a"
    },
    borderRadius: {
      label: "Border Radius",
      type: "range",
      min: 0,
      max: 24,
      default: 12
    },
    fontFamily: {
      label: "Font",
      type: "select",
      options: ["Inter", "Roboto", "Open Sans", "System"],
      default: "Inter"
    }
  },

  // Generate CSS from config
  generateCSS(values) {
    return `
:root {
  --theme-primary: ${values.primary};
  --theme-bg-primary: ${values.background};
  --theme-radius: ${values.borderRadius}px;
  --font-family: '${values.fontFamily}', sans-serif;
}`;
  }
};
```

## Building Integrations

### External API Integration

```javascript
// Example: Discord webhook integration
const discordIntegration = {
  name: "Discord Integration",

  config: {
    webhookUrl: "",
    enabled: false,
    events: ['onNewChat', 'onMilestone']
  },

  async init() {
    // Register hooks
    api.hooks.register('onMessage', this.onMessage.bind(this));
  },

  async onMessage(message) {
    if (!this.config.enabled) return message;

    // Check for milestones
    if (this.isMilestone(message)) {
      await this.sendToDiscord({
        content: `🎉 Milestone reached in chat with ${message.characterName}!`,
        embeds: [{
          title: "Chat Milestone",
          description: `Message count: ${message.messageNumber}`,
          color: 0x7c3aed
        }]
      });
    }

    return message;
  },

  isMilestone(message) {
    const milestones = [100, 500, 1000, 5000];
    return milestones.includes(message.messageNumber);
  },

  async sendToDiscord(payload) {
    try {
      await fetch(this.config.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } catch (error) {
      console.error('[Discord] Failed to send:', error);
    }
  }
};
```

### Voice Integration

```javascript
// Voice input/output integration
const voiceIntegration = {
  recognition: null,
  synthesis: window.speechSynthesis,

  async init() {
    // Set up speech recognition
    if ('webkitSpeechRecognition' in window) {
      this.recognition = new webkitSpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = true;

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (event.results[0].isFinal) {
          this.onVoiceInput(transcript);
        }
      };
    }

    // Add UI
    this.addVoiceButton();
  },

  addVoiceButton() {
    api.ui.addToolbarButton({
      id: 'voice-input-btn',
      icon: 'microphone',
      tooltip: 'Voice Input',
      onClick: () => this.toggleListening()
    });
  },

  toggleListening() {
    if (this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    } else {
      this.recognition.start();
      this.isListening = true;
    }
  },

  onVoiceInput(text) {
    // Insert transcribed text into input
    const input = document.getElementById('chat-input');
    input.value = text;
  },

  speak(text, options = {}) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = this.getVoice(options.voiceName);
    utterance.rate = options.rate || 1.0;
    utterance.pitch = options.pitch || 1.0;

    this.synthesis.speak(utterance);
  },

  getVoice(name) {
    const voices = this.synthesis.getVoices();
    return voices.find(v => v.name.includes(name)) || voices[0];
  }
};
```

## Testing Extensions

### Test Framework

```javascript
// Extension test utilities
const extensionTester = {
  // Mock API for testing
  mockAPI: {
    hooks: {
      registered: [],
      register(event, callback) {
        this.registered.push({ event, callback });
      },
      trigger(event, data) {
        const handlers = this.registered.filter(h => h.event === event);
        return handlers.map(h => h.callback(data));
      }
    },
    storage: {
      data: new Map(),
      async get(key) { return this.data.get(key); },
      async set(key, value) { this.data.set(key, value); }
    }
  },

  // Run tests
  async runTests(extension) {
    const results = [];

    // Test initialization
    results.push(await this.testInit(extension));

    // Test hooks
    results.push(await this.testHooks(extension));

    // Test settings
    results.push(await this.testSettings(extension));

    return results;
  },

  async testInit(extension) {
    try {
      await extension.init(this.mockAPI);
      return { test: 'init', passed: true };
    } catch (error) {
      return { test: 'init', passed: false, error: error.message };
    }
  },

  async testHooks(extension) {
    const testMessage = { content: 'Test message', role: 'user' };
    const results = this.mockAPI.hooks.trigger('onMessage', testMessage);

    const modified = results.some(r => r !== testMessage);
    return {
      test: 'hooks',
      passed: true,
      modifiesMessages: modified
    };
  }
};
```

## Publishing Extensions

### Preparing for Release

```javascript
// Extension checklist
const releaseChecklist = {
  required: [
    'manifest.json with valid metadata',
    'README.md with installation instructions',
    'LICENSE file',
    'No hardcoded API keys or sensitive data',
    'Version number follows semver',
    'Tested on latest SillyTavern version'
  ],

  recommended: [
    'Screenshots in README',
    'Changelog for versions',
    'Settings UI for configuration',
    'Error handling for edge cases',
    'Loading/error states in UI'
  ],

  // Package for distribution
  async package(extensionPath) {
    const manifest = await loadManifest(extensionPath);

    // Validate
    this.validate(manifest);

    // Create zip
    const zip = new JSZip();
    const files = await getExtensionFiles(extensionPath);

    for (const file of files) {
      zip.file(file.name, file.content);
    }

    return zip.generateAsync({ type: 'blob' });
  },

  validate(manifest) {
    const required = ['name', 'version', 'description', 'main'];
    for (const field of required) {
      if (!manifest[field]) {
        throw new Error(`Missing required field: ${field}`);
      }
    }
  }
};
```

## Contributing to SillyTavern

### Development Setup

```bash
# Fork and clone repository
git clone https://github.com/YOUR_USERNAME/SillyTavern.git
cd SillyTavern

# Install dependencies
npm install

# Create feature branch
git checkout -b feature/my-feature

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Code Guidelines

```javascript
// SillyTavern coding conventions
const codeGuidelines = {
  // Naming conventions
  naming: {
    functions: 'camelCase',      // getUserData()
    classes: 'PascalCase',       // ChatManager
    constants: 'UPPER_SNAKE',    // MAX_MESSAGES
    files: 'kebab-case'          // chat-manager.js
  },

  // Documentation
  documentation: {
    // JSDoc for functions
    example: `
/**
 * Sends a message to the current chat
 * @param {string} content - Message content
 * @param {Object} options - Send options
 * @param {boolean} options.stream - Enable streaming
 * @returns {Promise<Message>} The sent message
 */
async function sendMessage(content, options = {}) {
  // Implementation
}
`
  },

  // Pull request template
  prTemplate: `
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Screenshots
If applicable
`
};
```

## Summary

In this chapter, you've learned:

- **Extension Development**: Creating custom extensions with the API
- **Theme Development**: Building and customizing visual themes
- **Integrations**: Connecting external services and APIs
- **Testing**: Validating extensions before release
- **Publishing**: Preparing extensions for distribution
- **Contributing**: How to contribute to the main project

## Key Takeaways

1. **API is powerful**: The extension API provides deep integration
2. **Themes are CSS**: Customize visuals with standard CSS
3. **Test thoroughly**: Extensions can affect user experience
4. **Document well**: Good documentation helps users and contributors
5. **Community driven**: SillyTavern thrives on contributions

## Tutorial Complete!

Congratulations! 🎉 You've completed the SillyTavern tutorial. You now have the knowledge to:

- Create compelling characters with rich personalities
- Manage complex conversations and storylines
- Craft effective prompts for optimal AI responses
- Utilize extensions to enhance your experience
- Configure multiple AI backends
- Use advanced features for power user scenarios
- Develop custom extensions and themes

## Further Resources

- [Official Documentation](https://docs.sillytavern.app/)
- [GitHub Repository](https://github.com/SillyTavern/SillyTavern)
- [Community Discord](https://discord.gg/sillytavern)
- [Extension Directory](https://github.com/SillyTavern/SillyTavern#extensions)

---

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `theme`, `message`, `primary` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 8: Custom Development` as an operating subsystem inside **SillyTavern Tutorial: Advanced LLM Frontend for Power Users**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `settings`, `radius`, `extension` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 8: Custom Development` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `theme`.
2. **Input normalization**: shape incoming data so `message` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `primary`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/SillyTavern/SillyTavern)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [Extension Directory](https://github.com/SillyTavern/SillyTavern#extensions)
  Why it matters: authoritative reference on `Extension Directory` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `theme` and `message` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 7: Advanced Features](07-advanced-features.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
