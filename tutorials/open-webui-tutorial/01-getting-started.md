---
layout: default
title: "Open WebUI Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Open WebUI Tutorial
---

# Chapter 1: Getting Started with Open WebUI

> Deploy your own ChatGPT alternative with Open WebUI - self-hosted, privacy-focused, and feature-rich.

## Installation Options

### Docker Installation (Recommended)

The easiest way to get started is using Docker:

```bash
# Pull the latest image
docker pull ghcr.io/open-webui/open-webui:latest

# Run with basic configuration
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:latest
```

Access Open WebUI at `http://localhost:3000`

### Docker Compose (Production Ready)

For a more robust setup with persistent data and environment configuration:

```yaml
# docker-compose.yml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui-data:/app/backend/data
    environment:
      - WEBUI_SECRET_KEY=your-secret-key-here
      - OPENAI_API_KEY=your-openai-key
    restart: unless-stopped

volumes:
  open-webui-data:
```

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f open-webui
```

### Manual Installation

For development or custom deployments:

```bash
# Clone the repository
git clone https://github.com/open-webui/open-webui.git
cd open-webui

# Install dependencies
npm install
npm run build

# Install Python backend
cd backend
pip install -r requirements.txt

# Run the application
bash start.sh
```

## First Login and Setup

1. **Access the Web Interface**
   - Open `http://localhost:3000` in your browser
   - You'll see the welcome screen

2. **Initial Configuration**
   ```bash
   # Set admin credentials on first login
   Username: admin
   Password: (set your password)
   ```

3. **Basic Settings**
   - Go to Settings (⚙️) > Account
   - Configure your preferences
   - Set up API keys for external services

## Connecting Your First Model

### Option 1: OpenAI API

```python
# In Open WebUI Settings > Connections
# Add OpenAI API Key
OPENAI_API_KEY=sk-your-key-here

# Select models to enable
- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo
```

### Option 2: Local Ollama Models

First, install Ollama:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

Pull and run models:

```bash
# Pull a model
ollama pull llama2:7b

# Start Ollama server
ollama serve
```

In Open WebUI:
- Settings > Connections > Ollama
- API Base URL: `http://localhost:11434`
- The models will auto-discover

### Option 3: Other Backends

**Anthropic Claude:**
```
ANTHROPIC_API_KEY=your-key-here
Models: claude-3-opus, claude-3-sonnet, claude-3-haiku
```

**Google Gemini:**
```
GOOGLE_API_KEY=your-key-here
Models: gemini-pro, gemini-pro-vision
```

**LocalAI:**
```bash
# Run LocalAI server first
docker run -p 8080:8080 localai/localai:latest

# Then configure in Open WebUI
API Base URL: http://localhost:8080
```

## Your First Conversation

1. **Select a Model**
   - Click the model selector in the top-left
   - Choose your preferred model (e.g., GPT-4, Llama2)

2. **Start Chatting**
   ```
   User: Hello! Can you help me understand how Open WebUI works?
   Assistant: I'd be happy to help you understand Open WebUI! It's a self-hosted web interface for Large Language Models that provides...
   ```

3. **Explore Features**
   - Try different models
   - Use the sidebar for chat history
   - Experiment with the settings

## Basic Configuration

### Environment Variables

Create a `.env` file for configuration:

```bash
# Security
WEBUI_SECRET_KEY=your-very-long-random-secret-key-here

# OpenAI
OPENAI_API_KEY=sk-your-openai-key
OPENAI_API_BASE_URL=https://api.openai.com/v1

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Ollama
OLLAMA_BASE_URL=http://localhost:11434

# WebUI Settings
WEBUI_NAME=Your Custom Name
WEBUI_URL=http://localhost:3000
ENABLE_SIGNUP=false
```

### Docker with Environment File

```yaml
# docker-compose.yml with env file
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    env_file:
      - .env
    ports:
      - "3000:8080"
    volumes:
      - ./data:/app/backend/data
    restart: unless-stopped
```

## Troubleshooting Common Issues

### Connection Issues

**Ollama not connecting:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve

# Check Open WebUI logs
docker logs open-webui
```

**API Key Issues:**
```bash
# Test OpenAI API directly
curl -H "Authorization: Bearer sk-your-key" \
     -H "Content-Type: application/json" \
     https://api.openai.com/v1/models
```

### Port Conflicts

```bash
# Find what's using port 3000
lsof -i :3000

# Change port in docker-compose.yml
ports:
  - "3001:8080"
```

### Permission Issues

```bash
# Fix Docker volume permissions
sudo chown -R 1000:1000 ./data

# Or run container as current user
docker run --user $(id -u):$(id -g) ...
```

## Next Steps

Now that you have Open WebUI running, let's explore:

- **[Chapter 2: Model Management](02-model-management.md)** - Connect multiple backends and manage models
- **[Chapter 3: Interface Customization](03-interface-customization.md)** - Personalize your chat experience

## Quick Start Checklist

- [ ] Install Docker or Ollama
- [ ] Run Open WebUI container
- [ ] Access web interface
- [ ] Set admin password
- [ ] Connect at least one model
- [ ] Send your first message
- [ ] Explore basic settings

You're now ready to explore the full power of self-hosted AI chat interfaces! 🚀