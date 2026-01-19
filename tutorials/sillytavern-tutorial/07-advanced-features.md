---
layout: default
title: "Chapter 7: Advanced Features"
parent: "SillyTavern Tutorial"
nav_order: 7
---

# Chapter 7: Advanced Features

> Master power user features for complex storytelling and advanced AI interactions.

## Overview

SillyTavern offers numerous advanced features for power users who want to push the boundaries of AI-assisted storytelling. This chapter covers group chats, personas, macros, regex scripts, and more.

## Group Chats

### Multi-Character Conversations

```javascript
// Group chat configuration
const groupChatConfig = {
  // Group metadata
  name: "Academy Council Meeting",
  description: "Monthly meeting of academy department heads",

  // Group members
  members: [
    {
      characterId: "luna_starweaver",
      role: "Headmistress",
      speakingPriority: 1,     // Higher = speaks more often
      required: true           // Must be in every response
    },
    {
      characterId: "prof_ember",
      role: "Fire Magic Professor",
      speakingPriority: 0.7,
      required: false
    },
    {
      characterId: "master_frost",
      role: "Ice Magic Professor",
      speakingPriority: 0.7,
      required: false
    }
  ],

  // Response settings
  responseSettings: {
    maxSpeakers: 3,           // Max characters per response
    minSpeakers: 1,
    allowPrivate: true,       // Characters can have side conversations
    enforceOrder: false       // Don't force turn order
  },

  // Group dynamics
  dynamics: {
    relationships: {
      "luna_starweaver:prof_ember": "mentor",
      "prof_ember:master_frost": "rivalry"
    }
  }
};
```

### Group Response Generation

```javascript
// Group chat response handling
const groupResponseHandler = {
  // Select who speaks next
  selectSpeakers(group, context) {
    const speakers = [];
    const addressedCharacters = this.detectAddressed(context.lastMessage);

    // Add addressed characters first
    for (const charId of addressedCharacters) {
      const member = group.members.find(m => m.characterId === charId);
      if (member) speakers.push(member);
    }

    // Add required characters
    for (const member of group.members) {
      if (member.required && !speakers.includes(member)) {
        speakers.push(member);
      }
    }

    // Fill remaining slots by priority
    const remaining = group.members
      .filter(m => !speakers.includes(m))
      .sort((a, b) => b.speakingPriority - a.speakingPriority);

    while (speakers.length < group.responseSettings.maxSpeakers && remaining.length > 0) {
      if (Math.random() < remaining[0].speakingPriority) {
        speakers.push(remaining.shift());
      } else {
        remaining.shift();
      }
    }

    return speakers;
  },

  // Generate group response
  async generateGroupResponse(group, messages, speakers) {
    const systemPrompt = this.buildGroupSystemPrompt(group, speakers);
    const response = await generateResponse(systemPrompt, messages);
    return this.parseGroupResponse(response, speakers);
  },

  // Build system prompt for group
  buildGroupSystemPrompt(group, speakers) {
    let prompt = `You are simulating a conversation with multiple characters.\n\n`;

    for (const speaker of speakers) {
      const char = getCharacter(speaker.characterId);
      prompt += `[${char.name}]\n${char.description}\nRole: ${speaker.role}\n\n`;
    }

    prompt += `Format each character's response with their name followed by their action/dialogue.\n`;
    prompt += `Example:\n${speakers[0].characterId}: *action* "Dialogue"\n`;

    return prompt;
  }
};
```

## Personas (User Profiles)

### Creating User Personas

```javascript
// Persona structure
const userPersona = {
  name: "Aiden the Apprentice",

  // User's character description
  description: `Aiden is a 19-year-old first-year student at the Crystal Academy.
He comes from a small village where magic was considered dangerous, making
him both eager to learn and somewhat nervous about his abilities. He has
messy brown hair, green eyes, and a tendency to stammer when nervous.`,

  // Personality for AI to reference
  personality: `Curious, determined, sometimes self-doubting. Quick learner
but easily overwhelmed. Has a dry sense of humor that emerges when comfortable.`,

  // Default scenarios with this persona
  defaultScenario: `The story follows Aiden's journey as a magic student,
navigating classes, making friends, and uncovering mysteries at the academy.`,

  // Voice/writing style for user
  userStyle: {
    actionFormat: "*action*",
    speechFormat: '"dialogue"',
    thoughtFormat: "*thought italics*"
  }
};

// Persona manager
const personaManager = {
  personas: new Map(),
  activePersona: null,

  // Create new persona
  create(persona) {
    this.personas.set(persona.name, persona);
    this.save();
    return persona;
  },

  // Activate persona
  activate(name) {
    const persona = this.personas.get(name);
    if (!persona) throw new Error('Persona not found');
    this.activePersona = persona;
    return persona;
  },

  // Get persona prompt injection
  getPromptInjection() {
    if (!this.activePersona) return '';

    return `[User's Character: ${this.activePersona.name}]
${this.activePersona.description}

Personality: ${this.activePersona.personality}`;
  }
};
```

## Macros and Variables

### Built-in Macros

```javascript
// Available macros
const builtInMacros = {
  // Character macros
  '{{char}}': 'Current character name',
  '{{user}}': 'User/persona name',
  '{{charAvatar}}': 'Character avatar URL',

  // Message macros
  '{{lastMessage}}': 'Previous message content',
  '{{lastMessageBy}}': 'Who sent the last message',
  '{{messageCount}}': 'Total messages in chat',

  // Time macros
  '{{time}}': 'Current time (12h)',
  '{{time24h}}': 'Current time (24h)',
  '{{date}}': 'Current date',
  '{{day}}': 'Day of week',

  // Random macros
  '{{random::a,b,c}}': 'Random choice from list',
  '{{roll::d20}}': 'Dice roll result',

  // Conditional macros
  '{{if::condition::then::else}}': 'Conditional text'
};

// Macro processor
const macroProcessor = {
  // Process all macros in text
  process(text, context) {
    let result = text;

    // Character macros
    result = result.replace(/\{\{char\}\}/g, context.characterName);
    result = result.replace(/\{\{user\}\}/g, context.userName);

    // Time macros
    const now = new Date();
    result = result.replace(/\{\{time\}\}/g, now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }));
    result = result.replace(/\{\{date\}\}/g, now.toLocaleDateString());
    result = result.replace(/\{\{day\}\}/g, now.toLocaleDateString('en-US', { weekday: 'long' }));

    // Random macros
    result = result.replace(/\{\{random::([^}]+)\}\}/g, (match, options) => {
      const choices = options.split(',');
      return choices[Math.floor(Math.random() * choices.length)];
    });

    // Dice rolls
    result = result.replace(/\{\{roll::d(\d+)\}\}/g, (match, sides) => {
      return Math.floor(Math.random() * parseInt(sides)) + 1;
    });

    return result;
  }
};
```

### Custom Variables

```javascript
// Variable system
const variableSystem = {
  // Scopes
  global: {},      // Persist across all chats
  chat: {},        // Persist within chat
  message: {},     // Single message scope

  // Set variable
  set(name, value, scope = 'chat') {
    this[scope][name] = value;
    this.save();
  },

  // Get variable
  get(name, scope = 'chat') {
    return this[scope][name] ?? this.global[name] ?? null;
  },

  // Increment/decrement
  increment(name, amount = 1, scope = 'chat') {
    const current = this.get(name, scope) || 0;
    this.set(name, current + amount, scope);
    return this.get(name, scope);
  },

  // Variable macros
  processMacros(text) {
    // Get variable: {{getvar::name}}
    text = text.replace(/\{\{getvar::(\w+)\}\}/g, (match, name) => {
      return this.get(name) ?? '';
    });

    // Set variable: {{setvar::name::value}}
    text = text.replace(/\{\{setvar::(\w+)::([^}]+)\}\}/g, (match, name, value) => {
      this.set(name, value);
      return '';  // Setter returns nothing
    });

    // Increment: {{addvar::name::amount}}
    text = text.replace(/\{\{addvar::(\w+)::(-?\d+)\}\}/g, (match, name, amount) => {
      return this.increment(name, parseInt(amount));
    });

    return text;
  }
};
```

## Regex Scripts

### Response Manipulation

```javascript
// Regex script configuration
const regexScript = {
  name: "Emotion Highlighter",
  enabled: true,

  // Script placement
  placement: {
    affectsPrompt: false,    // Don't modify outgoing prompt
    affectsResponse: true,   // Modify incoming response
    runOnEdit: true          // Also run when editing messages
  },

  // Pattern matching
  patterns: [
    {
      // Add color to emotions in asterisks
      find: /\*([^*]+(?:smile|laugh|grin|happy)[^*]*)\*/gi,
      replace: '<span class="emotion happy">*$1*</span>'
    },
    {
      // Add color to sad emotions
      find: /\*([^*]+(?:frown|sigh|tear|sad)[^*]*)\*/gi,
      replace: '<span class="emotion sad">*$1*</span>'
    },
    {
      // Clean up excessive punctuation
      find: /([!?.]){3,}/g,
      replace: '$1$1'
    }
  ]
};

// Regex script runner
const regexRunner = {
  scripts: new Map(),

  // Add script
  addScript(script) {
    this.scripts.set(script.name, script);
  },

  // Run scripts on text
  process(text, type = 'response') {
    let result = text;

    for (const [name, script] of this.scripts) {
      if (!script.enabled) continue;

      const shouldRun = (type === 'prompt' && script.placement.affectsPrompt) ||
                       (type === 'response' && script.placement.affectsResponse);

      if (!shouldRun) continue;

      for (const pattern of script.patterns) {
        result = result.replace(pattern.find, pattern.replace);
      }
    }

    return result;
  }
};
```

### Common Regex Scripts

```javascript
// Useful regex script examples
const commonScripts = {
  // Clean up common AI artifacts
  cleanArtifacts: {
    name: "Clean AI Artifacts",
    patterns: [
      { find: /^(As an AI|I'm an AI|I cannot)/gm, replace: '' },
      { find: /\*nods\*/g, replace: '*nods thoughtfully*' }
    ]
  },

  // Enforce response format
  formatEnforcer: {
    name: "Format Enforcer",
    patterns: [
      // Ensure actions use asterisks
      { find: /\((.*?doing something.*?)\)/g, replace: '*$1*' },
      // Ensure dialogue uses quotes
      { find: /'([^']{10,})'/g, replace: '"$1"' }
    ]
  },

  // Name consistency
  nameConsistency: {
    name: "Name Consistency",
    patterns: [
      // Fix common name misspellings
      { find: /Luna Star[\s-]?weaver/gi, replace: 'Luna Starweaver' }
    ]
  }
};
```

## Quick Replies

### Configuring Quick Replies

```javascript
// Quick reply configuration
const quickReplies = {
  sets: [
    {
      name: "Roleplay Actions",
      enabled: true,
      replies: [
        {
          label: "Continue",
          message: "*waits expectantly for {{char}} to continue*"
        },
        {
          label: "Describe",
          message: "Can you describe the surroundings in more detail?"
        },
        {
          label: "Say More",
          message: "Tell me more about that."
        },
        {
          label: "OOC Note",
          message: "[OOC: {{input}}]",
          requiresInput: true
        }
      ]
    },
    {
      name: "Narrative Control",
      enabled: true,
      replies: [
        {
          label: "Time Skip",
          message: "[Skip forward {{input}} in time]",
          requiresInput: true
        },
        {
          label: "Scene Change",
          message: "[Change scene to {{input}}]",
          requiresInput: true
        },
        {
          label: "Introduce NPC",
          message: "[A new character enters: {{input}}]",
          requiresInput: true
        }
      ]
    }
  ]
};

// Quick reply handler
const quickReplyHandler = {
  // Execute quick reply
  execute(replyConfig) {
    let message = replyConfig.message;

    // Handle input requirement
    if (replyConfig.requiresInput) {
      const input = promptUser("Enter value:");
      if (!input) return null;
      message = message.replace('{{input}}', input);
    }

    // Process macros
    message = macroProcessor.process(message, getCurrentContext());

    return message;
  }
};
```

## Instruct Mode

### Instruction Formatting

```javascript
// Instruct mode configuration
const instructConfig = {
  // Preset templates
  presets: {
    alpaca: {
      systemPrefix: "### System:\n",
      systemSuffix: "\n\n",
      userPrefix: "### Instruction:\n",
      userSuffix: "\n\n",
      assistantPrefix: "### Response:\n",
      assistantSuffix: "\n\n"
    },
    chatml: {
      systemPrefix: "<|im_start|>system\n",
      systemSuffix: "<|im_end|>\n",
      userPrefix: "<|im_start|>user\n",
      userSuffix: "<|im_end|>\n",
      assistantPrefix: "<|im_start|>assistant\n",
      assistantSuffix: "<|im_end|>\n"
    },
    llama2: {
      systemPrefix: "[INST] <<SYS>>\n",
      systemSuffix: "\n<</SYS>>\n\n",
      userPrefix: "",
      userSuffix: " [/INST] ",
      assistantPrefix: "",
      assistantSuffix: " </s><s>[INST] "
    }
  },

  // Custom template builder
  buildCustom(options) {
    return {
      systemPrefix: options.systemPrefix || "",
      systemSuffix: options.systemSuffix || "\n",
      userPrefix: options.userPrefix || "User: ",
      userSuffix: options.userSuffix || "\n",
      assistantPrefix: options.assistantPrefix || "Assistant: ",
      assistantSuffix: options.assistantSuffix || "\n"
    };
  }
};
```

## Summarization

### Automatic Summarization

```javascript
// Summarization system
const summarizationSystem = {
  config: {
    enabled: true,
    triggerThreshold: 50,    // Messages before summarizing
    targetLength: 500,       // Target summary length in tokens
    preserveRecent: 10,      // Always keep last N messages
    model: 'gpt-3.5-turbo'   // Model for summarization
  },

  // Check if summarization needed
  shouldSummarize(chat) {
    return chat.messages.length > this.config.triggerThreshold;
  },

  // Generate summary
  async generateSummary(messages) {
    const prompt = `Summarize the following conversation, maintaining:
1. Key plot points and story developments
2. Important character moments
3. Established facts and world details
4. Current situation and context

Conversation:
${messages.map(m => `${m.role}: ${m.content}`).join('\n\n')}

Provide a concise summary:`;

    return await callModel(prompt, this.config.model);
  },

  // Apply summarization
  async applySummarization(chat) {
    if (!this.shouldSummarize(chat)) return chat;

    const toSummarize = chat.messages.slice(
      0,
      -this.config.preserveRecent
    );

    const summary = await this.generateSummary(toSummarize);

    // Create summarized chat
    return {
      ...chat,
      messages: [
        {
          role: 'system',
          content: `[Story Summary]\n${summary}`,
          type: 'summary'
        },
        ...chat.messages.slice(-this.config.preserveRecent)
      ]
    };
  }
};
```

## Summary

In this chapter, you've learned:

- **Group Chats**: Managing multi-character conversations
- **Personas**: Creating user character profiles
- **Macros/Variables**: Dynamic text substitution and state tracking
- **Regex Scripts**: Automated response manipulation
- **Quick Replies**: Rapid common interactions
- **Instruct Mode**: Proper formatting for different models
- **Summarization**: Managing long conversation context

## Key Takeaways

1. **Groups expand storytelling**: Multiple characters enable richer narratives
2. **Personas enhance immersion**: Define who "you" are in the story
3. **Macros save time**: Automate repetitive text patterns
4. **Regex is powerful**: Transform responses automatically
5. **Context matters**: Summarization keeps stories coherent over time

## Next Steps

Ready to create your own extensions? Let's explore custom development in Chapter 8: Custom Development.

---

**Ready for Chapter 8?** [Custom Development](08-custom-development.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
