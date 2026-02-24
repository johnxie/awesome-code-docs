---
layout: default
title: "Open WebUI Tutorial - Chapter 4: Advanced Chat Features"
nav_order: 4
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 4: Advanced Chat Features & Multi-Modal Conversations

Welcome to **Chapter 4: Advanced Chat Features & Multi-Modal Conversations**. In this part of **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Unlock the full potential of Open WebUI with voice input, image generation, function calling, and advanced conversation patterns.

## Voice Input & Speech Synthesis

### Speech-to-Text Integration

```javascript
class VoiceInputManager {
  constructor() {
    this.recognition = null;
    this.isListening = false;
    this.transcript = '';
    this.initSpeechRecognition();
  }

  initSpeechRecognition() {
    // Check for browser support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.warn('Speech recognition not supported');
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.lang = 'en-US';

    this.recognition.onstart = () => {
      this.isListening = true;
      this.showListeningIndicator();
    };

    this.recognition.onresult = (event) => {
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      this.transcript = finalTranscript;
      this.updateTranscriptDisplay(finalTranscript, interimTranscript);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      this.hideListeningIndicator();
    };

    this.recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      this.handleRecognitionError(event.error);
    };
  }

  startListening() {
    if (!this.recognition) return;

    try {
      this.recognition.start();
    } catch (error) {
      console.error('Failed to start speech recognition:', error);
    }
  }

  stopListening() {
    if (!this.recognition) return;

    this.recognition.stop();
  }

  showListeningIndicator() {
    // Add visual feedback
    const indicator = document.createElement('div');
    indicator.id = 'voice-indicator';
    indicator.innerHTML = `
      <div class="voice-pulse">
        <div class="pulse-ring"></div>
        <div class="pulse-ring"></div>
        <div class="pulse-ring"></div>
        <span>Listening...</span>
      </div>
    `;
    document.body.appendChild(indicator);
  }

  hideListeningIndicator() {
    const indicator = document.getElementById('voice-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  updateTranscriptDisplay(final, interim) {
    // Update the chat input with transcript
    const input = document.querySelector('.chat-input textarea');
    if (input) {
      input.value = final + interim;
      input.focus();
    }
  }

  handleRecognitionError(error) {
    const errorMessages = {
      'no-speech': 'No speech detected. Please try again.',
      'audio-capture': 'Audio capture failed. Check microphone permissions.',
      'not-allowed': 'Microphone access denied. Please enable permissions.',
      'network': 'Network error. Check your connection.',
      'service-not-allowed': 'Speech service not allowed.'
    };

    const message = errorMessages[error] || `Speech recognition error: ${error}`;
    this.showError(message);
  }

  showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'voice-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #ff4757;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      z-index: 1000;
    `;

    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
  }
}

// Initialize voice input
const voiceManager = new VoiceInputManager();

// Add voice button to chat interface
function addVoiceButton() {
  const inputContainer = document.querySelector('.chat-input-container');
  const voiceButton = document.createElement('button');
  voiceButton.id = 'voice-button';
  voiceButton.innerHTML = '🎤';
  voiceButton.title = 'Voice input (Ctrl+Shift+V)';
  voiceButton.onclick = () => {
    if (voiceManager.isListening) {
      voiceManager.stopListening();
    } else {
      voiceManager.startListening();
    }
  };

  inputContainer.appendChild(voiceButton);
}

// Keyboard shortcut
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.shiftKey && e.key === 'V') {
    e.preventDefault();
    if (voiceManager.isListening) {
      voiceManager.stopListening();
    } else {
      voiceManager.startListening();
    }
  }
});
```

### Text-to-Speech Output

```javascript
class TextToSpeechManager {
  constructor() {
    this.synthesis = window.speechSynthesis;
    this.voices = [];
    this.currentVoice = null;
    this.isSpeaking = false;

    this.initVoices();
  }

  initVoices() {
    // Load available voices
    const loadVoices = () => {
      this.voices = this.synthesis.getVoices();

      // Set default voice (prefer English voices)
      this.currentVoice = this.voices.find(voice =>
        voice.lang.startsWith('en') && voice.name.includes('Female')
      ) || this.voices[0];
    };

    loadVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = loadVoices;
    }
  }

  speak(text, options = {}) {
    if (!this.synthesis) {
      console.warn('Text-to-speech not supported');
      return;
    }

    // Stop any current speech
    this.stop();

    const utterance = new SpeechSynthesisUtterance(text);

    // Apply options
    utterance.voice = options.voice || this.currentVoice;
    utterance.rate = options.rate || 1.0; // 0.1 to 10
    utterance.pitch = options.pitch || 1.0; // 0 to 2
    utterance.volume = options.volume || 1.0; // 0 to 1

    utterance.onstart = () => {
      this.isSpeaking = true;
      this.showSpeakingIndicator();
    };

    utterance.onend = () => {
      this.isSpeaking = false;
      this.hideSpeakingIndicator();
    };

    utterance.onerror = (event) => {
      console.error('TTS error:', event.error);
      this.isSpeaking = false;
      this.hideSpeakingIndicator();
    };

    this.synthesis.speak(utterance);
  }

  stop() {
    if (this.synthesis) {
      this.synthesis.cancel();
      this.isSpeaking = false;
      this.hideSpeakingIndicator();
    }
  }

  pause() {
    if (this.synthesis) {
      this.synthesis.pause();
    }
  }

  resume() {
    if (this.synthesis) {
      this.synthesis.resume();
    }
  }

  showSpeakingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'tts-indicator';
    indicator.innerHTML = `
      <div class="tts-indicator">
        <div class="sound-wave">
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
        </div>
        <span>Speaking...</span>
      </div>
    `;
    document.body.appendChild(indicator);
  }

  hideSpeakingIndicator() {
    const indicator = document.getElementById('tts-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  getAvailableVoices() {
    return this.voices.map(voice => ({
      name: voice.name,
      lang: voice.lang,
      default: voice.default
    }));
  }

  setVoice(voiceName) {
    const voice = this.voices.find(v => v.name === voiceName);
    if (voice) {
      this.currentVoice = voice;
    }
  }
}

// Initialize TTS
const ttsManager = new TextToSpeechManager();

// Auto-speak assistant responses
function setupAutoSpeak() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        const newMessages = mutation.addedNodes;
        newMessages.forEach((node) => {
          if (node.classList && node.classList.contains('message') &&
              node.classList.contains('assistant')) {
            // Auto-speak new assistant messages
            const text = node.textContent;
            ttsManager.speak(text, { rate: 1.1 });
          }
        });
      }
    });
  });

  const chatContainer = document.querySelector('.chat-container');
  if (chatContainer) {
    observer.observe(chatContainer, { childList: true });
  }
}

// Add TTS controls to message bubbles
function addTTSControls() {
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('tts-button')) {
      const messageElement = e.target.closest('.message');
      const text = messageElement.textContent;

      if (ttsManager.isSpeaking) {
        ttsManager.stop();
      } else {
        ttsManager.speak(text);
      }
    }
  });
}
```

## Image Generation & Vision

### DALL-E Integration

```javascript
class ImageGenerationManager {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = 'https://api.openai.com/v1/images/generations';
  }

  async generateImage(prompt, options = {}) {
    const requestBody = {
      prompt: prompt,
      n: options.count || 1,
      size: options.size || '1024x1024',
      model: options.model || 'dall-e-3',
      quality: options.quality || 'standard',
      style: options.style || 'vivid'
    };

    try {
      const response = await fetch(this.baseURL, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        throw new Error(`Image generation failed: ${response.status}`);
      }

      const result = await response.json();
      return result.data.map(img => img.url);

    } catch (error) {
      console.error('Image generation error:', error);
      throw error;
    }
  }

  async editImage(imageFile, maskFile, prompt, options = {}) {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', prompt);

    if (maskFile) {
      formData.append('mask', maskFile);
    }

    if (options.size) formData.append('size', options.size);
    if (options.n) formData.append('n', options.n.toString());

    try {
      const response = await fetch('https://api.openai.com/v1/images/edits', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Image edit failed: ${response.status}`);
      }

      const result = await response.json();
      return result.data.map(img => img.url);

    } catch (error) {
      console.error('Image edit error:', error);
      throw error;
    }
  }

  async createVariation(imageFile, options = {}) {
    const formData = new FormData();
    formData.append('image', imageFile);

    if (options.n) formData.append('n', options.n.toString());
    if (options.size) formData.append('size', options.size);

    try {
      const response = await fetch('https://api.openai.com/v1/images/variations', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Image variation failed: ${response.status}`);
      }

      const result = await response.json();
      return result.data.map(img => img.url);

    } catch (error) {
      console.error('Image variation error:', error);
      throw error;
    }
  }
}

// Usage in chat interface
const imageGen = new ImageGenerationManager(process.env.OPENAI_API_KEY);

// Add image generation command
commands.registerCommand('image', async (args) => {
  const prompt = args.join(' ');
  if (!prompt) {
    return 'Usage: /image <description>';
  }

  try {
    const imageUrls = await imageGen.generateImage(prompt);

    // Display images in chat
    const imageHtml = imageUrls.map(url =>
      `<img src="${url}" alt="${prompt}" style="max-width: 100%; border-radius: 8px; margin: 10px 0;">`
    ).join('');

    return `Generated image(s) for: "${prompt}"\n\n${imageHtml}`;

  } catch (error) {
    return `Failed to generate image: ${error.message}`;
  }
}, {
  description: 'Generate images using DALL-E',
  usage: '/image <description>'
});
```

### Vision Model Integration

```javascript
class VisionManager {
  constructor() {
    this.supportedModels = ['gpt-4-vision-preview', 'claude-3-opus'];
  }

  async analyzeImage(imageUrl, prompt, model = 'gpt-4-vision-preview') {
    if (model.startsWith('gpt-4')) {
      return await this.analyzeWithGPT4Vision(imageUrl, prompt);
    } else if (model.includes('claude')) {
      return await this.analyzeWithClaudeVision(imageUrl, prompt);
    }

    throw new Error(`Unsupported vision model: ${model}`);
  }

  async analyzeWithGPT4Vision(imageUrl, prompt) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-4-vision-preview',
        messages: [
          {
            role: 'user',
            content: [
              { type: 'text', text: prompt },
              {
                type: 'image_url',
                image_url: { url: imageUrl }
              }
            ]
          }
        ],
        max_tokens: 500
      })
    });

    if (!response.ok) {
      throw new Error(`GPT-4 Vision API error: ${response.status}`);
    }

    const result = await response.json();
    return result.choices[0].message.content;
  }

  async analyzeWithClaudeVision(imageUrl, prompt) {
    // Download image and convert to base64
    const imageResponse = await fetch(imageUrl);
    const imageBuffer = await imageResponse.arrayBuffer();
    const base64Image = Buffer.from(imageBuffer).toString('base64');

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'claude-3-opus-20240229',
        max_tokens: 500,
        messages: [
          {
            role: 'user',
            content: [
              { type: 'text', text: prompt },
              {
                type: 'image',
                source: {
                  type: 'base64',
                  media_type: 'image/jpeg',
                  data: base64Image
                }
              }
            ]
          }
        ]
      })
    });

    if (!response.ok) {
      throw new Error(`Claude Vision API error: ${response.status}`);
    }

    const result = await response.json();
    return result.content[0].text;
  }

  async extractTextFromImage(imageUrl, model = 'gpt-4-vision-preview') {
    const prompt = "Extract all visible text from this image. Return only the text, nothing else.";
    return await this.analyzeImage(imageUrl, prompt, model);
  }

  async describeImage(imageUrl, model = 'gpt-4-vision-preview') {
    const prompt = "Describe this image in detail, including objects, colors, composition, and any text visible.";
    return await this.analyzeImage(imageUrl, prompt, model);
  }

  async answerQuestionAboutImage(imageUrl, question, model = 'gpt-4-vision-preview') {
    return await this.analyzeImage(imageUrl, question, model);
  }
}

// Integrate vision into chat
const vision = new VisionManager();

// Handle image uploads with analysis
function setupImageAnalysis() {
  const fileInput = document.querySelector('.file-input');

  fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Show loading indicator
    showLoading('Analyzing image...');

    try {
      // Convert to data URL for API
      const reader = new FileReader();
      reader.onload = async (e) => {
        const imageUrl = e.target.result;

        // Auto-analyze based on context or user preference
        const analysis = await vision.describeImage(imageUrl);

        // Add to chat as assistant message
        addMessage('assistant', `Image Analysis: ${analysis}`);

        // Store image for future reference
        storeImage(file, analysis);
      };

      reader.readAsDataURL(file);

    } catch (error) {
      addMessage('assistant', `Image analysis failed: ${error.message}`);
    } finally {
      hideLoading();
    }
  });
}

// Vision commands
commands.registerCommand('analyze', async (args, context) => {
  if (!context.lastImage) {
    return 'No image to analyze. Upload an image first.';
  }

  const prompt = args.join(' ') || 'Describe this image in detail';
  const analysis = await vision.analyzeImage(context.lastImage, prompt);

  return analysis;
}, {
  description: 'Analyze the last uploaded image',
  usage: '/analyze [question about the image]'
});

commands.registerCommand('ocr', async (args, context) => {
  if (!context.lastImage) {
    return 'No image to process. Upload an image first.';
  }

  const text = await vision.extractTextFromImage(context.lastImage);
  return `Extracted text:\n${text}`;
}, {
  description: 'Extract text from the last uploaded image'
});
```

## Function Calling & Tools

### Custom Function Definitions

```javascript
class FunctionCallingManager {
  constructor() {
    this.functions = new Map();
    this.functionSchemas = [];
  }

  registerFunction(name, handler, schema) {
    this.functions.set(name, handler);
    this.functionSchemas.push({
      name: name,
      description: schema.description,
      parameters: schema.parameters
    });
  }

  getFunctionSchemas() {
    return this.functionSchemas;
  }

  async executeFunction(name, args) {
    const handler = this.functions.get(name);
    if (!handler) {
      throw new Error(`Function ${name} not found`);
    }

    return await handler(args);
  }

  async handleFunctionCall(response) {
    const functionCalls = [];

    if (response.choices[0].message.tool_calls) {
      for (const toolCall of response.choices[0].message.tool_calls) {
        const functionName = toolCall.function.name;
        const functionArgs = JSON.parse(toolCall.function.arguments);

        try {
          const result = await this.executeFunction(functionName, functionArgs);
          functionCalls.push({
            id: toolCall.id,
            name: functionName,
            result: result
          });
        } catch (error) {
          console.error(`Function ${functionName} failed:`, error);
          functionCalls.push({
            id: toolCall.id,
            name: functionName,
            error: error.message
          });
        }
      }
    }

    return functionCalls;
  }
}

// Initialize function manager
const functionManager = new FunctionCallingManager();

// Register useful functions
functionManager.registerFunction('get_weather', async (args) => {
  const { location } = args;
  // Implement weather API call
  return await fetchWeatherData(location);
}, {
  description: "Get current weather for a location",
  parameters: {
    type: "object",
    properties: {
      location: {
        type: "string",
        description: "City name or location"
      }
    },
    required: ["location"]
  }
});

functionManager.registerFunction('search_web', async (args) => {
  const { query, num_results = 5 } = args;
  // Implement web search
  return await searchWeb(query, num_results);
}, {
  description: "Search the web for information",
  parameters: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query"
      },
      num_results: {
        type: "number",
        description: "Number of results to return"
      }
    },
    required: ["query"]
  }
});

functionManager.registerFunction('calculate', async (args) => {
  const { expression } = args;
  // Safe math evaluation
  return evaluateMathExpression(expression);
}, {
  description: "Calculate mathematical expressions",
  parameters: {
    type: "object",
    properties: {
      expression: {
        type: "string",
        description: "Mathematical expression to evaluate"
      }
    },
    required: ["expression"]
  }
});

functionManager.registerFunction('send_email', async (args) => {
  const { to, subject, body } = args;
  // Implement email sending
  return await sendEmail(to, subject, body);
}, {
  description: "Send an email",
  parameters: {
    type: "object",
    properties: {
      to: {
        type: "string",
        description: "Recipient email address"
      },
      subject: {
        type: "string",
        description: "Email subject"
      },
      body: {
        type: "string",
        description: "Email body"
      }
    },
    required: ["to", "subject", "body"]
  }
});

functionManager.registerFunction('create_task', async (args) => {
  const { title, description, assignee, due_date } = args;
  // Create task in your task management system
  return await createTask(title, description, assignee, due_date);
}, {
  description: "Create a new task",
  parameters: {
    type: "object",
    properties: {
      title: {
        type: "string",
        description: "Task title"
      },
      description: {
        type: "string",
        description: "Task description"
      },
      assignee: {
        type: "string",
        description: "Person to assign the task to"
      },
      due_date: {
        type: "string",
        description: "Due date (YYYY-MM-DD)"
      }
    },
    required: ["title"]
  }
});
```

### Advanced Conversation Patterns

### Conversation Branching

```javascript
class ConversationBranchingManager {
  constructor() {
    this.branches = new Map();
    this.currentBranch = 'main';
    this.branchHistory = [];
  }

  createBranch(branchName, fromMessageId = null) {
    const currentMessages = this.getCurrentBranchMessages();
    const branchPoint = fromMessageId || currentMessages[currentMessages.length - 1]?.id;

    this.branches.set(branchName, {
      messages: [...currentMessages],
      parentBranch: this.currentBranch,
      branchPoint: branchPoint,
      createdAt: new Date()
    });

    return branchName;
  }

  switchBranch(branchName) {
    if (!this.branches.has(branchName)) {
      throw new Error(`Branch ${branchName} does not exist`);
    }

    this.branchHistory.push(this.currentBranch);
    this.currentBranch = branchName;

    // Update UI to show branched conversation
    this.updateConversationDisplay();
  }

  mergeBranch(branchName, strategy = 'append') {
    const branch = this.branches.get(branchName);
    if (!branch) {
      throw new Error(`Branch ${branchName} does not exist`);
    }

    const mainMessages = this.getCurrentBranchMessages();

    if (strategy === 'append') {
      // Append branch messages to main
      const mergedMessages = [...mainMessages, ...branch.messages];
      this.branches.set(this.currentBranch, {
        ...this.branches.get(this.currentBranch),
        messages: mergedMessages
      });
    } else if (strategy === 'replace') {
      // Replace main with branch
      this.branches.set(this.currentBranch, branch);
    }

    // Mark branch as merged
    branch.merged = true;
    branch.mergedAt = new Date();
  }

  getCurrentBranchMessages() {
    return this.branches.get(this.currentBranch)?.messages || [];
  }

  getAllBranches() {
    return Array.from(this.branches.entries()).map(([name, branch]) => ({
      name,
      messageCount: branch.messages.length,
      createdAt: branch.createdAt,
      isActive: name === this.currentBranch
    }));
  }

  updateConversationDisplay() {
    const messages = this.getCurrentBranchMessages();
    const branches = this.getAllBranches();

    // Update UI
    renderMessages(messages);
    renderBranchSelector(branches);
  }
}

// Commands for branching
commands.registerCommand('branch', async (args) => {
  const branchName = args[0];
  if (!branchName) {
    return 'Usage: /branch <name>';
  }

  conversationManager.createBranch(branchName);
  conversationManager.switchBranch(branchName);

  return `Created and switched to branch: ${branchName}`;
}, {
  description: 'Create a new conversation branch',
  usage: '/branch <name>'
});

commands.registerCommand('branches', async () => {
  const branches = conversationManager.getAllBranches();
  const branchList = branches.map(b =>
    `${b.name} (${b.messageCount} messages) ${b.isActive ? '[ACTIVE]' : ''}`
  ).join('\n');

  return `Conversation branches:\n${branchList}`;
}, {
  description: 'List all conversation branches'
});

commands.registerCommand('switch', async (args) => {
  const branchName = args[0];
  if (!branchName) {
    return 'Usage: /switch <branch_name>';
  }

  conversationManager.switchBranch(branchName);
  return `Switched to branch: ${branchName}`;
}, {
  description: 'Switch to a different conversation branch',
  usage: '/switch <branch_name>'
});

commands.registerCommand('merge', async (args) => {
  const branchName = args[0];
  const strategy = args[1] || 'append';

  if (!branchName) {
    return 'Usage: /merge <branch_name> [append|replace]';
  }

  conversationManager.mergeBranch(branchName, strategy);
  return `Merged branch ${branchName} using ${strategy} strategy`;
}, {
  description: 'Merge a branch back to main conversation',
  usage: '/merge <branch_name> [append|replace]'
});
```

### Collaborative Features

```javascript
class CollaborationManager {
  constructor() {
    this.sharedChats = new Map();
    this.activeUsers = new Map();
    this.websocket = null;
  }

  async createSharedChat(chatId, creator) {
    const sharedChat = {
      id: chatId,
      creator: creator,
      participants: [creator],
      messages: [],
      createdAt: new Date(),
      settings: {
        allowEditing: true,
        allowInviting: true,
        realTimeUpdates: true
      }
    };

    this.sharedChats.set(chatId, sharedChat);
    return sharedChat;
  }

  async joinSharedChat(chatId, user) {
    const chat = this.sharedChats.get(chatId);
    if (!chat) {
      throw new Error('Chat not found');
    }

    if (!chat.participants.includes(user)) {
      chat.participants.push(user);
      this.broadcastToChat(chatId, {
        type: 'user_joined',
        user: user,
        timestamp: new Date()
      });
    }

    return chat;
  }

  async addMessageToSharedChat(chatId, message, user) {
    const chat = this.sharedChats.get(chatId);
    if (!chat) {
      throw new Error('Chat not found');
    }

    if (!chat.participants.includes(user)) {
      throw new Error('User not in chat');
    }

    const messageObj = {
      id: `msg_${Date.now()}_${Math.random()}`,
      user: user,
      content: message,
      timestamp: new Date(),
      type: 'message'
    };

    chat.messages.push(messageObj);

    // Broadcast to all participants
    this.broadcastToChat(chatId, messageObj);

    return messageObj;
  }

  broadcastToChat(chatId, message) {
    const chat = this.sharedChats.get(chatId);
    if (!chat) return;

    chat.participants.forEach(userId => {
      const userWs = this.activeUsers.get(userId);
      if (userWs && userWs.readyState === WebSocket.OPEN) {
        userWs.send(JSON.stringify(message));
      }
    });
  }

  async inviteToChat(chatId, inviter, invitee) {
    const chat = this.sharedChats.get(chatId);
    if (!chat) {
      throw new Error('Chat not found');
    }

    if (chat.creator !== inviter && !chat.settings.allowInviting) {
      throw new Error('Not authorized to invite users');
    }

    // Send invitation
    const invitation = {
      type: 'invitation',
      chatId: chatId,
      inviter: inviter,
      invitee: invitee,
      chatName: chat.name || `Chat by ${chat.creator}`,
      timestamp: new Date()
    };

    const inviteeWs = this.activeUsers.get(invitee);
    if (inviteeWs) {
      inviteeWs.send(JSON.stringify(invitation));
    }

    return invitation;
  }

  getChatSummary(chatId) {
    const chat = this.sharedChats.get(chatId);
    if (!chat) return null;

    return {
      id: chat.id,
      creator: chat.creator,
      participants: chat.participants,
      messageCount: chat.messages.length,
      lastActivity: chat.messages.length > 0 ?
        chat.messages[chat.messages.length - 1].timestamp : chat.createdAt,
      settings: chat.settings
    };
  }
}

// Commands for collaboration
commands.registerCommand('share', async (args, context) => {
  const chatId = `shared_${Date.now()}`;
  const sharedChat = await collaborationManager.createSharedChat(chatId, context.userId);

  return `Shared chat created! Share this link: ${window.location.origin}/chat/${chatId}`;
}, {
  description: 'Create a shareable chat session'
});

commands.registerCommand('invite', async (args, context) => {
  const [chatId, userEmail] = args;
  if (!chatId || !userEmail) {
    return 'Usage: /invite <chat_id> <user_email>';
  }

  await collaborationManager.inviteToChat(chatId, context.userId, userEmail);
  return `Invitation sent to ${userEmail}`;
}, {
  description: 'Invite a user to a shared chat',
  usage: '/invite <chat_id> <user_email>'
});

commands.registerCommand('who', async (args, context) => {
  const chatId = args[0] || context.currentChatId;
  const summary = collaborationManager.getChatSummary(chatId);

  if (!summary) {
    return 'Chat not found';
  }

  return `Chat: ${chatId}
Creator: ${summary.creator}
Participants: ${summary.participants.join(', ')}
Messages: ${summary.messageCount}
Last activity: ${summary.lastActivity}`;
}, {
  description: 'Show chat participants and info',
  usage: '/who [chat_id]'
});
```

This advanced feature set transforms Open WebUI from a simple chat interface into a powerful multi-modal AI assistant capable of voice interaction, image processing, function calling, and collaborative conversations. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `chat`, `error`, `description` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Advanced Chat Features & Multi-Modal Conversations` as an operating subsystem inside **Open WebUI Tutorial: Self-Hosted AI Workspace and Chat Interface**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `args`, `chatId`, `prompt` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Advanced Chat Features & Multi-Modal Conversations` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `chat`.
2. **Input normalization**: shape incoming data so `error` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `description`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [Open WebUI Repository](https://github.com/open-webui/open-webui)
  Why it matters: authoritative reference on `Open WebUI Repository` (github.com).
- [Open WebUI Releases](https://github.com/open-webui/open-webui/releases)
  Why it matters: authoritative reference on `Open WebUI Releases` (github.com).
- [Open WebUI Docs](https://docs.openwebui.com/)
  Why it matters: authoritative reference on `Open WebUI Docs` (docs.openwebui.com).

Suggested trace strategy:
- search upstream code for `chat` and `error` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Interface Customization & Personalization](03-interface-customization.md)
- [Next Chapter: Chapter 5: Data, Knowledge Bases & RAG Implementation](05-data-knowledge.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
