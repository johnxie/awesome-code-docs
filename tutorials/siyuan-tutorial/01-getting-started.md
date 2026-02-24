---
layout: default
title: "Chapter 1: Getting Started with SiYuan"
parent: "SiYuan Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with SiYuan

Welcome to SiYuan! If you're interested in building knowledge management systems that respect user privacy and data ownership, you're in the right place. SiYuan represents a different approach to personal knowledge management - one that prioritizes local storage, open standards, and user control.

## What Makes SiYuan Different?

Traditional knowledge management tools often:
- **Store data in the cloud** - You don't own your data
- **Require subscriptions** - Ongoing costs for basic features
- **Limit customization** - You're stuck with vendor decisions
- **Track user behavior** - Privacy concerns with data collection

SiYuan solves these problems by:
- **Storing everything locally** - Complete data ownership
- **Being completely free** - No subscriptions or hidden costs
- **Offering full customization** - Open-source and extensible
- **Respecting privacy** - No tracking or data collection

## Installing SiYuan

SiYuan is available for all major platforms. Let's get you set up:

### Desktop Installation

```bash
# Download from GitHub releases
# Visit: https://github.com/siyuan-note/siyuan/releases

# For Linux
wget https://github.com/siyuan-note/siyuan/releases/download/v2.12.0/siyuan-2.12.0-linux.tar.gz
tar -xzf siyuan-2.12.0-linux.tar.gz
cd SiYuan-2.12.0
./SiYuan

# For macOS (using Homebrew)
brew install --cask siyuan

# For Windows
# Download the .exe installer from GitHub releases
```

### Docker Installation

```bash
# Run SiYuan in Docker
docker run -d \
  --name siyuan \
  -p 6806:6806 \
  -v ~/SiYuan:/home/siyuan/Documents/SiYuan \
  b3log/siyuan:latest

# Access at http://localhost:6806
```

### Development Setup

```bash
# Clone the repository
git clone https://github.com/siyuan-note/siyuan.git
cd siyuan

# Install dependencies (requires Go and Node.js)
npm install

# Build the application
npm run build

# Start development server
npm run dev
```

## Your First SiYuan Workspace

Let's create your first knowledge base:

### Step 1: Initialize Workspace

```bash
# Create a new workspace directory
mkdir my-knowledge-base
cd my-knowledge-base

# SiYuan will create its database and configuration files here
# The workspace contains:
# - data/ (SQLite database and assets)
# - conf/ (configuration files)
# - log/ (application logs)
```

### Step 2: Create Your First Document

SiYuan uses a block-based system. Let's create a simple document:

```markdown
# Welcome to SiYuan

This is my first SiYuan document. SiYuan uses a unique block-based system where every piece of content is a block.

## What are Blocks?

Blocks are the fundamental unit of content in SiYuan. They can be:
- Paragraphs of text
- Headings
- Lists
- Code blocks
- Tables
- And much more!

## Block References

You can reference blocks using `((block-id))` syntax. This creates bi-directional links between related content.
```

### Step 3: Understanding the Interface

```
┌─────────────────────────────────────┐
│ Menu Bar                            │
├─────────────────────────────────────┤
│ Toolbar                             │
├─────────────────┬───────────────────┤
│ Document Tree  │ Document Pane     │
│                 │                   │
│ • Note 1        │ # Heading         │
│ • Note 2        │                   │
│ • Note 3        │ Content...        │
│                 │                   │
└─────────────────┴───────────────────┘
```

## Core Concepts

### Documents vs. Blocks

**Traditional Systems:**
- File = Document = Unit of storage
- Content is stored in files
- Links are between files

**SiYuan's Approach:**
- Block = Unit of content
- Documents are containers for blocks
- Links are between blocks

```typescript
// SiYuan's data model
interface Block {
  id: string;
  content: string;
  type: BlockType;
  parent?: string;     // Parent block ID
  children?: string[]; // Child block IDs
}

interface Document {
  id: string;
  name: string;
  blocks: Block[];
}
```

### SQL Database Backend

SiYuan uses SQLite for storage, but exposes it through a custom SQL interface:

```sql
-- Query blocks
SELECT * FROM blocks WHERE content LIKE '%search term%';

-- Find block references
SELECT * FROM refs WHERE from_id = 'block-123';

-- Get document structure
SELECT * FROM blocks WHERE root_id = 'doc-456' ORDER BY sort;
```

## How SiYuan Works Under the Hood

### Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   API Layer     │    │   Database      │
│   (HTML/JS)     │◄──►│   (Go)          │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  File System    │    │  Plugin System  │    │   Sync Engine   │
│  (Markdown)     │    │   (Extensions)  │    │   (Git-based)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components

1. **Web Interface**: Built with modern web technologies
2. **Go Backend**: High-performance API server
3. **SQLite Database**: Local data storage
4. **File System**: Markdown export/import
5. **Plugin System**: Extensibility framework
6. **Sync Engine**: Multi-device synchronization

## Basic Operations

### Creating Content

```javascript
// Create a new document
const newDoc = await siyuan.createDoc({
  notebook: "my-notebook",
  path: "/new-document",
  content: "# New Document\n\nWelcome!"
});

// Add a block
const newBlock = await siyuan.insertBlock({
  dataType: "markdown",
  data: "This is a new block",
  parentID: newDoc.id
});
```

### Querying Data

```javascript
// Search for content
const results = await siyuan.search({
  query: "machine learning",
  type: "text"
});

// Get block by ID
const block = await siyuan.getBlockByID("block-id");

// Get document structure
const docTree = await siyuan.getDocTree({
  notebook: "my-notebook"
});
```

## Data Storage Structure

SiYuan stores your data in a structured format:

```
workspace/
├── data/
│   ├── 2023-01-01/
│   │   ├── notebooks/
│   │   │   ├── notebook1.sy
│   │   │   └── notebook2.sy
│   │   └── assets/
│   │       └── image1.png
│   └── siyuan.db
├── conf/
│   ├── conf.json
│   └── key.pem
└── log/
    └── app.log
```

### Database Schema

```sql
-- Main tables
CREATE TABLE blocks (
  id TEXT PRIMARY KEY,
  content TEXT,
  type TEXT,
  parent_id TEXT,
  root_id TEXT,      -- Document ID
  sort INTEGER,      -- Order within parent
  created INTEGER,
  updated INTEGER
);

CREATE TABLE refs (
  from_id TEXT,      -- Source block
  to_id TEXT,        -- Target block
  type TEXT          -- Reference type
);
```

## First Application: Simple Note Taker

Let's build a basic application that demonstrates SiYuan's capabilities:

```javascript
class SimpleNoteTaker {
  constructor(siyuanAPI) {
    this.api = siyuanAPI;
  }

  async createNote(title, content) {
    // Create document
    const doc = await this.api.createDoc({
      notebook: "Notes",
      path: `/${title}`,
      content: `# ${title}\n\n${content}`
    });

    return doc;
  }

  async searchNotes(query) {
    return await this.api.search({
      query: query,
      type: "text"
    });
  }

  async linkNotes(sourceId, targetId, linkText) {
    // Create reference between blocks
    await this.api.insertBlock({
      dataType: "markdown",
      data: `((${targetId} "${linkText}"))`,
      parentID: sourceId
    });
  }
}

// Usage
const noteTaker = new SimpleNoteTaker(siyuanAPI);

// Create notes
const note1 = await noteTaker.createNote("AI Concepts", "Machine learning is...");
const note2 = await noteTaker.createNote("Neural Networks", "Neural networks are...");

// Link them
await noteTaker.linkNotes(note1.id, note2.id, "related to");
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Installed SiYuan** on your system
2. **Created your first workspace** with documents and blocks
3. **Understood the core architecture** and data model
4. **Learned basic operations** for content creation and querying
5. **Built a simple application** demonstrating key features
6. **Explored the database structure** and storage patterns

## Next Steps

Now that you understand SiYuan's basics, let's dive deeper into its unique block-based architecture. In [Chapter 2: Block-Based Architecture](02-block-architecture.md), we'll explore how SiYuan's block system enables powerful knowledge connections.

---

**Practice what you've learned:**
1. Create a few documents with different types of content (text, lists, code)
2. Try creating references between blocks using `((block-id))` syntax
3. Experiment with the search functionality
4. Look at the generated database files in your workspace

*What's the most interesting aspect of SiYuan's privacy-first approach?* 🔒

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `siyuan`, `block`, `SiYuan` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with SiYuan` as an operating subsystem inside **SiYuan Tutorial: Privacy-First Knowledge Management**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `blocks`, `TEXT` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with SiYuan` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `siyuan`.
2. **Input normalization**: shape incoming data so `block` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `SiYuan`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/siyuan-note/siyuan)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `siyuan` and `block` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Block-Based Architecture](02-block-architecture.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
