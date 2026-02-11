---
layout: default
title: "Chapter 4: Development Setup"
nav_order: 4
has_children: false
parent: "Logseq Knowledge Management"
---

# Logseq Development Environment Setup

## Prerequisites & System Requirements

### Hardware Requirements
- **Memory**: Minimum 8GB RAM (16GB recommended for large knowledge bases)
- **Storage**: 5GB+ available space for development environment
- **CPU**: Multi-core processor (development compilation can be CPU intensive)
- **Display**: 1920x1080+ recommended for graph visualization development

### Operating System Support
- **macOS**: 10.15+ (Catalina or newer)
- **Linux**: Ubuntu 20.04+, Fedora 34+, or equivalent
- **Windows**: Windows 10+ with WSL2 recommended for optimal development experience

### Core Development Stack
- **Node.js 18.x or higher** with npm/yarn package management
- **Java 11+** (OpenJDK recommended, required for ClojureScript compilation)
- **Git 2.30+** with proper SSH key configuration
- **Clojure CLI Tools** or Leiningen for ClojureScript project management

### Optional but Recommended Tools
- **VS Code** with Calva extension (excellent ClojureScript support)
- **IntelliJ IDEA** with Cursive plugin (professional ClojureScript IDE)
- **Electron Fiddle** for Electron API experimentation
- **React DevTools** browser extension for debugging

## Installation Guide

### Step 1: Core Dependencies Setup

#### Node.js Installation
```bash
# Using Node Version Manager (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
nvm alias default 18

# Verify installation
node --version  # Should show v18.x.x
npm --version   # Should show 9.x.x or higher
```

#### Java Development Kit Setup
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk

# macOS with Homebrew
brew install openjdk@11

# Windows (use Chocolatey)
choco install openjdk11

# Verify installation
java -version
javac -version
```

#### Clojure CLI Tools Installation
```bash
# Linux/macOS
curl -O https://download.clojure.org/install/linux-install-1.11.1.1413.sh
chmod +x linux-install-1.11.1.1413.sh
sudo ./linux-install-1.11.1.1413.sh

# macOS with Homebrew (alternative)
brew install clojure/tools/clojure

# Windows (PowerShell as Administrator)
Invoke-RestMethod -Uri https://download.clojure.org/install/win-install-1.11.1.1413.ps1 -Outfile win-install-1.11.1.1413.ps1
PowerShell -ExecutionPolicy Bypass -File win-install-1.11.1.1413.ps1

# Verify installation
clj -version
```

### Step 2: Logseq Repository Setup

#### Clone and Initial Setup
```bash
# Clone the main repository
git clone https://github.com/logseq/logseq.git
cd logseq

# Install Node.js dependencies (this may take several minutes)
yarn install

# Verify the installation
yarn --version  # Should show 1.22.x or higher
```

#### Environment Configuration
```bash
# Create development environment configuration
cp .env.example .env.local

# Edit environment variables for development
cat >> .env.local << EOF
# Development Configuration
NODE_ENV=development
DEBUG=logseq:*
ENABLE_PLUGINS=true
ENABLE_ELECTRON_UPDATER=false
LOGSEQ_LOG_LEVEL=debug

# Optional: Custom paths for development
LOGSEQ_GRAPH_PATH=./dev-graph
LOGSEQ_PLUGINS_PATH=./dev-plugins
EOF
```

### Step 3: Development Workflow Setup

#### Shadow-cljs Configuration
```bash
# Create shadow-cljs development configuration
cat > shadow-cljs.dev.edn << 'EOF'
{:deps true
 :dev-http {3001 {:root "public"
                  :handler shadow.http.push-state/handle}}
 :nrepl {:port 9000}
 :builds
 {:electron
  {:target :node-script
   :main logseq.electron.core
   :output-to "static/electron.js"
   :devtools {:console-support true}}
  
  :app  
  {:target :browser
   :output-dir "static/js"
   :asset-path "/static/js"
   :module-hash-names true
   :dev {:compiler-options {:closure-warnings {:check-types :off}
                            :reader-features #{:dev}}
         :devtools {:http-root "public"
                    :http-port 3001}}
   :modules {:main {:entries [logseq.core]}}}}}
EOF
```

#### Development Scripts Setup
```bash
# Create convenient development scripts
mkdir -p scripts

# Script for starting development environment
cat > scripts/dev-start.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 Starting Logseq development environment..."

# Start shadow-cljs watch in background
echo "Starting ClojureScript compilation..."
npx shadow-cljs watch app electron &
SHADOW_PID=$!

# Wait for compilation to complete
echo "Waiting for initial compilation..."
sleep 30

# Start Electron app
echo "Starting Electron application..."
yarn electron:dev &
ELECTRON_PID=$!

# Handle cleanup on script termination
cleanup() {
    echo "🛑 Shutting down development environment..."
    kill $SHADOW_PID 2>/dev/null || true
    kill $ELECTRON_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "✅ Development environment started!"
echo "📝 Edit ClojureScript files in src/"
echo "🔧 Electron DevTools available in app"
echo "🌐 Web version at http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop..."

# Keep script running
wait
EOF

chmod +x scripts/dev-start.sh

# Script for building production version
cat > scripts/build-prod.sh << 'EOF'
#!/bin/bash
set -e

echo "🏗️  Building Logseq for production..."

# Clean previous builds
rm -rf static/js/
rm -rf static/electron.js

# Build ClojureScript
echo "Compiling ClojureScript..."
npx shadow-cljs release app electron

# Build Electron app
echo "Building Electron application..."
yarn electron:make

echo "✅ Production build completed!"
echo "📦 Built application available in out/"
EOF

chmod +x scripts/build-prod.sh
```

### Step 4: IDE and Editor Configuration

#### VS Code with Calva Setup
```json
// .vscode/settings.json
{
  "calva.replConnectSequences": [
    {
      "name": "Logseq Development",
      "projectType": "shadow-cljs",
      "builds": ["app", "electron"],
      "afterCLJReplJackInCode": [
        "(require '[shadow.cljs.devtools.api :as shadow])",
        "(shadow/watch :app)",
        "(shadow/watch :electron)"
      ]
    }
  ],
  "calva.autoSelectForTerminalREPL": true,
  "calva.showDocstringInParameterHelp": true,
  "calva.paredit.defaultKeyMap": "strict",
  "files.associations": {
    "*.cljs": "clojure",
    "*.cljc": "clojure",
    "*.edn": "clojure"
  },
  "editor.formatOnSave": true,
  "editor.wordSeparators": " ()\"':,;~@#$%^&{}[]`",
  "[clojure]": {
    "editor.defaultFormatter": "betterthantomorrow.calva",
    "editor.tabSize": 2
  }
}

// .vscode/extensions.json  
{
  "recommendations": [
    "betterthantomorrow.calva",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode"
  ]
}
```

#### IntelliJ IDEA with Cursive Setup
```xml
<!-- .idea/workspace.xml configuration for Cursive -->
<component name="CursiveREPLConsole">
  <option name="configType" value="shadow-cljs" />
  <option name="builds" value="app,electron" />
  <option name="autostartREPL" value="true" />
</component>
```

### Step 5: Development Environment Testing

#### Verify ClojureScript Compilation
```bash
# Test ClojureScript compilation
npx shadow-cljs compile app

# Should output something like:
# shadow-cljs - HTTP server available at http://localhost:8200
# shadow-cljs - config: /path/to/logseq/shadow-cljs.edn
# [:app] Compiling ...
# [:app] Build completed. (143 files, 2 compiled, 0 warnings, 3.45s)
```

#### Test Electron Integration
```bash
# Start development environment
./scripts/dev-start.sh

# In another terminal, check if services are running
ps aux | grep -E "(shadow-cljs|electron)"

# Test API endpoints
curl http://localhost:3001/static/js/main.js | head -n 10
```

#### Verify File System Access
```bash
# Create test graph directory
mkdir -p dev-graph

# Create test files
cat > dev-graph/test-page.md << 'EOF'
# Test Page

This is a test page for [[Logseq Development]].

## Block Testing
- This is a block
  - With nested content
  - And more [[Links]]

## Code Testing  
```javascript
console.log("Hello Logseq!");
```
EOF

# Start Logseq and verify it can read the test graph
```

### Step 6: Plugin Development Setup

#### Plugin Development Environment
```bash
# Create plugin development directory
mkdir logseq-plugins && cd logseq-plugins

# Initialize plugin development template
npx @logseq/create-plugin@latest my-first-plugin
cd my-first-plugin

# Install plugin development dependencies
npm install

# Start plugin development server
npm run dev
```

#### Plugin Development Configuration
```javascript
// logseq-plugins/my-first-plugin/vite.config.ts
import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    target: 'es2018',
    minify: false,
    rollupOptions: {
      input: resolve(__dirname, 'src/index.ts'),
      output: {
        entryFileNames: 'index.js',
        format: 'iife'
      },
      external: ['@logseq/libs']
    }
  },
  define: {
    'process.env.NODE_ENV': '"development"'
  }
})
```

### Step 7: Performance and Debugging Setup

#### Memory and Performance Monitoring
```bash
# Create performance monitoring script
cat > scripts/monitor-performance.sh << 'EOF'
#!/bin/bash

echo "🔍 Logseq Performance Monitor"
echo "============================="

# Monitor Electron main process
echo "Electron Main Process:"
ps aux | grep -E "electron.*main" | awk '{print "PID: " $2 ", CPU: " $3 "%, Memory: " $4 "%"}'

# Monitor renderer processes
echo "Electron Renderer Processes:"
ps aux | grep -E "electron.*renderer" | awk '{print "PID: " $2 ", CPU: " $3 "%, Memory: " $4 "%"}'

# Monitor ClojureScript compilation
echo "ClojureScript Compiler:"
ps aux | grep shadow-cljs | awk '{print "PID: " $2 ", CPU: " $3 "%, Memory: " $4 "%"}'

# Check file handles (important for large graphs)
echo "Open File Handles:"
lsof -p $(pgrep -f "electron") | wc -l

# Memory usage details
echo "Memory Usage Details:"
if command -v smem >/dev/null; then
    smem -t -P logseq
else
    echo "Install 'smem' for detailed memory analysis"
fi
EOF

chmod +x scripts/monitor-performance.sh
```

#### Debug Logging Configuration
```javascript
// src/main/debug-config.cljs
(ns main.debug-config
  (:require [electron :refer [app]]))

(defn setup-debug-logging []
  (when (= js/process.env.NODE_ENV "development")
    ;; Enable Chrome DevTools
    (.setPath app "userData" (str (.getPath app "userData") "-dev"))
    
    ;; Debug IPC communication
    (set! js/process.env.DEBUG "logseq:*")
    
    ;; Enable source maps
    (js/require "source-map-support/register")))
```

## Development Workflow

### Daily Development Routine

#### Starting Development Session
```bash
# 1. Update repository
git pull origin master

# 2. Update dependencies if needed
yarn install

# 3. Start development environment
./scripts/dev-start.sh

# 4. Open IDE and connect REPL
code .  # VS Code with Calva auto-connects
```

#### Making Changes and Testing
```clojure
;; In REPL, test changes interactively
(require '[logseq.core :as core])
(require '[logseq.db.model :as db-model])

;; Test block operations
(db-model/get-block-by-uuid "test-uuid")

;; Test graph operations
(core/get-graph-data)

;; Hot reload specific namespaces
(require '[your.namespace :as ns] :reload)
```

#### Performance Testing with Large Graphs
```bash
# Generate large test graph for performance testing
cat > scripts/generate-test-graph.sh << 'EOF'
#!/bin/bash

GRAPH_DIR="./performance-test-graph"
mkdir -p $GRAPH_DIR

echo "Generating large test graph..."

# Create pages with interconnected links
for i in {1..1000}; do
    cat > "$GRAPH_DIR/page-$i.md" << EOL
# Page $i

This is page $i with links to [[Page $((i+1))]] and [[Page $((i-1))]].

## Blocks
- Block 1 for page $i
  - Nested block with reference to [[Page $((RANDOM % 1000 + 1))]]
- Block 2 with #tag$i
- Block 3 with [[Random Link $((RANDOM % 100))]]

## Properties
tags:: page$i, test
created:: $(date -Iseconds)
modified:: $(date -Iseconds)
EOL
done

echo "Generated $i pages in $GRAPH_DIR"
EOF

chmod +x scripts/generate-test-graph.sh
./scripts/generate-test-graph.sh
```

### Debugging Common Issues

#### ClojureScript Compilation Issues
```bash
# Clear compilation cache
rm -rf .shadow-cljs/
npx shadow-cljs clean

# Check for conflicting dependencies
npx shadow-cljs classpath
```

#### Electron Issues
```bash
# Clear Electron cache
rm -rf node_modules/.cache/
rm -rf ~/.cache/electron/

# Rebuild native dependencies
npm rebuild --runtime=electron --disturl=https://electronjs.org/headers

# Check Electron process status
ps aux | grep electron
lsof -i :3001  # Check port usage
```

#### Performance Issues
```bash
# Profile ClojureScript compilation
time npx shadow-cljs compile app

# Monitor file system usage
./scripts/monitor-performance.sh

# Check for memory leaks
heap-profile electron-app.js
```

## Production Build Process

### Building for Distribution
```bash
# Build for all platforms
./scripts/build-prod.sh

# Platform-specific builds
yarn electron:make --platform=darwin   # macOS
yarn electron:make --platform=win32    # Windows  
yarn electron:make --platform=linux    # Linux

# Code signing (requires certificates)
yarn electron:make --platform=darwin --publish=never
```

### Testing Production Builds
```bash
# Install built application
open out/make/zip/darwin/x64/Logseq-1.0.0-darwin-x64.zip  # macOS
start out/make/squirrel.windows/x64/Logseq-1.0.0 Setup.exe  # Windows
dpkg -i out/make/deb/x64/Logseq_1.0.0_amd64.deb  # Ubuntu

# Test application functionality
./test-production-build.sh
```

## Getting Help and Troubleshooting

### Community Resources
- **Official Discord**: [Logseq Community](https://discord.gg/logseq)
- **GitHub Discussions**: [Logseq Discussions](https://github.com/logseq/logseq/discussions)
- **Documentation**: [Logseq Docs](https://docs.logseq.com/)

### Common Issues and Solutions

#### "Java not found" Error
```bash
# Check Java installation
java -version
which java

# Set JAVA_HOME if needed
export JAVA_HOME=$(/usr/libexec/java_home)  # macOS
echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.bashrc
```

#### "shadow-cljs command not found"
```bash
# Install shadow-cljs globally
npm install -g shadow-cljs

# Or use npx (recommended)
npx shadow-cljs --help
```

#### Slow Compilation Issues
```bash
# Increase JVM memory for compilation
export CLJ_JVM_OPTS="-Xmx4g -XX:+UseG1GC"

# Use faster compilation options for development
echo '{:compiler-options {:optimizations :none}}' > dev.clj
```

### Advanced Development Setup

#### Custom Graph Storage Backend
```clojure
;; Example: Custom storage implementation
(defprotocol GraphStorage
  (save-block [this block])
  (load-block [this block-id])
  (query-blocks [this query]))

(defrecord FileSystemStorage [base-path]
  GraphStorage
  (save-block [this block]
    ;; Implementation for file system storage
    )
  (load-block [this block-id]
    ;; Implementation for loading from files
    )
  (query-blocks [this query]
    ;; Implementation for querying blocks
    ))
```

#### Performance Monitoring Integration
```javascript
// Performance monitoring setup
const { performance } = require('perf_hooks');

class LogseqProfiler {
  constructor() {
    this.metrics = new Map();
  }
  
  startTiming(label) {
    this.metrics.set(label, performance.now());
  }
  
  endTiming(label) {
    const start = this.metrics.get(label);
    if (start) {
      console.log(`${label}: ${performance.now() - start}ms`);
      this.metrics.delete(label);
    }
  }
}

// Usage in development
const profiler = new LogseqProfiler();
profiler.startTiming('graph-render');
// ... graph rendering code
profiler.endTiming('graph-render');
```

---

**✅ Development Environment Ready? Continue to [Knowledge Management Principles](01-knowledge-management-principles.md)**

*This comprehensive setup guide ensures you have a fully functional Logseq development environment with advanced debugging, performance monitoring, and production build capabilities.*
