---
layout: default
title: "Chapter 7: Integration & API"
parent: "Fabric Tutorial"
nav_order: 7
---

# Chapter 7: Integration & API

Welcome to **Chapter 7: Integration & API**. In this part of **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Integrate Fabric into applications, automate workflows, and build custom tools using Fabric's API.

## Overview

Fabric can be integrated into larger systems through its REST API, Python SDK, and various automation interfaces. This chapter covers integration patterns for building AI-augmented applications.

## REST API

### Starting the API Server

```bash
# Start Fabric API server
fabric --serve --port 8080

# With authentication
fabric --serve --port 8080 --api-key your-secret-key

# Background mode
fabric --serve --port 8080 --daemon

# Check status
curl http://localhost:8080/health
```

### API Endpoints

```bash
# List available patterns
curl http://localhost:8080/api/patterns

# Execute a pattern
curl -X POST http://localhost:8080/api/execute \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your-api-key" \
    -d '{
        "pattern": "summarize",
        "input": "Content to summarize...",
        "options": {
            "model": "gpt-4",
            "temperature": 0.7
        }
    }'

# Execute a stitch
curl -X POST http://localhost:8080/api/stitch \
    -H "Content-Type: application/json" \
    -d '{
        "stitch": "research_pipeline",
        "input": "Research topic content",
        "variables": {
            "depth": "deep"
        }
    }'

# Stream response
curl -X POST http://localhost:8080/api/execute \
    -H "Content-Type: application/json" \
    -H "Accept: text/event-stream" \
    -d '{
        "pattern": "summarize",
        "input": "Long content...",
        "stream": true
    }'
```

### API Response Format

```json
{
    "success": true,
    "pattern": "summarize",
    "model": "gpt-4",
    "output": "The summarized content...",
    "metadata": {
        "tokens_used": 1523,
        "processing_time_ms": 2450,
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## Python Integration

### Basic Usage

```python
from fabric import Fabric, Pattern

# Initialize Fabric
fab = Fabric(api_key="your-openai-key")

# Execute a pattern
result = fab.execute(
    pattern="summarize",
    input="Content to process..."
)
print(result.output)

# With options
result = fab.execute(
    pattern="extract_wisdom",
    input=content,
    model="gpt-4",
    temperature=0.7
)
```

### Pattern Management

```python
from fabric import Fabric, Pattern

fab = Fabric()

# List patterns
patterns = fab.list_patterns()
for p in patterns:
    print(f"{p.name}: {p.description}")

# Get pattern details
pattern = fab.get_pattern("summarize")
print(pattern.system_prompt)

# Create custom pattern
custom = Pattern(
    name="my_analyzer",
    system_prompt="""
    # IDENTITY and PURPOSE
    You are a specialized analyzer...

    # INPUT
    {{input}}
    """
)
fab.register_pattern(custom)
```

### Async Operations

```python
import asyncio
from fabric import AsyncFabric

async def process_documents(documents):
    fab = AsyncFabric()

    # Process multiple documents concurrently
    tasks = [
        fab.execute_async(
            pattern="summarize",
            input=doc
        )
        for doc in documents
    ]

    results = await asyncio.gather(*tasks)
    return results

# Usage
documents = ["doc1...", "doc2...", "doc3..."]
summaries = asyncio.run(process_documents(documents))
```

### Streaming Responses

```python
from fabric import Fabric

fab = Fabric()

# Stream output
for chunk in fab.stream(
    pattern="long_analysis",
    input=content
):
    print(chunk, end="", flush=True)
```

## JavaScript/TypeScript Integration

### Node.js Client

```typescript
import { Fabric, Pattern } from 'fabric-ai';

// Initialize
const fabric = new Fabric({
    apiKey: process.env.OPENAI_API_KEY
});

// Execute pattern
async function summarize(content: string): Promise<string> {
    const result = await fabric.execute({
        pattern: 'summarize',
        input: content,
        options: {
            model: 'gpt-4'
        }
    });
    return result.output;
}

// Batch processing
async function processBatch(items: string[]): Promise<string[]> {
    const promises = items.map(item =>
        fabric.execute({ pattern: 'extract_wisdom', input: item })
    );
    const results = await Promise.all(promises);
    return results.map(r => r.output);
}
```

### Browser Integration

```html
<!DOCTYPE html>
<html>
<head>
    <title>Fabric Web Integration</title>
</head>
<body>
    <textarea id="input" placeholder="Enter content..."></textarea>
    <select id="pattern">
        <option value="summarize">Summarize</option>
        <option value="extract_wisdom">Extract Wisdom</option>
        <option value="analyze_claims">Analyze Claims</option>
    </select>
    <button onclick="process()">Process</button>
    <div id="output"></div>

    <script>
        async function process() {
            const input = document.getElementById('input').value;
            const pattern = document.getElementById('pattern').value;

            const response = await fetch('http://localhost:8080/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ pattern, input })
            });

            const result = await response.json();
            document.getElementById('output').innerText = result.output;
        }
    </script>
</body>
</html>
```

## Automation Integrations

### GitHub Actions

```yaml
# .github/workflows/analyze-pr.yml
name: Analyze PR with Fabric

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Fabric
        run: pip install fabric-ai

      - name: Get PR Diff
        id: diff
        run: |
          git fetch origin ${{ github.base_ref }}
          git diff origin/${{ github.base_ref }}...HEAD > diff.txt

      - name: Analyze Code Changes
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cat diff.txt | fabric -p review_code > review.md

      - name: Post Review Comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### Slack Integration

```python
from slack_bolt import App
from fabric import Fabric

app = App(token="xoxb-your-token")
fabric = Fabric()

@app.message("summarize this:")
def handle_summarize(message, say):
    content = message['text'].replace("summarize this:", "").strip()

    result = fabric.execute(
        pattern="summarize",
        input=content
    )

    say(f"Summary:\n{result.output}")

@app.command("/analyze")
def handle_analyze(ack, body, respond):
    ack()

    content = body['text']
    result = fabric.execute(
        pattern="analyze_claims",
        input=content
    )

    respond(result.output)

if __name__ == "__main__":
    app.start(port=3000)
```

### Zapier/Make Integration

```python
# Webhook endpoint for Zapier
from flask import Flask, request, jsonify
from fabric import Fabric

app = Flask(__name__)
fabric = Fabric()

@app.route('/webhook/fabric', methods=['POST'])
def fabric_webhook():
    data = request.json

    pattern = data.get('pattern', 'summarize')
    content = data.get('content', '')

    result = fabric.execute(
        pattern=pattern,
        input=content
    )

    return jsonify({
        'output': result.output,
        'pattern': pattern,
        'success': True
    })

if __name__ == '__main__':
    app.run(port=5000)
```

## Building Custom Tools

### CLI Tool with Fabric

```python
#!/usr/bin/env python3
"""Custom research tool using Fabric."""

import argparse
import sys
from fabric import Fabric

def main():
    parser = argparse.ArgumentParser(description='Research Assistant')
    parser.add_argument('command', choices=['summarize', 'analyze', 'research'])
    parser.add_argument('--input', '-i', type=str, help='Input file')
    parser.add_argument('--url', '-u', type=str, help='URL to process')
    parser.add_argument('--output', '-o', type=str, help='Output file')

    args = parser.parse_args()
    fabric = Fabric()

    # Get input
    if args.input:
        with open(args.input) as f:
            content = f.read()
    elif args.url:
        import requests
        content = requests.get(args.url).text
    else:
        content = sys.stdin.read()

    # Process based on command
    pattern_map = {
        'summarize': 'summarize',
        'analyze': 'analyze_claims',
        'research': 'extract_wisdom'
    }

    result = fabric.execute(
        pattern=pattern_map[args.command],
        input=content
    )

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result.output)
    else:
        print(result.output)

if __name__ == '__main__':
    main()
```

### VS Code Extension

```typescript
// extension.ts
import * as vscode from 'vscode';
import { Fabric } from 'fabric-ai';

const fabric = new Fabric();

export function activate(context: vscode.ExtensionContext) {

    // Command: Explain selected code
    let explainCode = vscode.commands.registerCommand(
        'fabric.explainCode',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selection = editor.document.getText(editor.selection);

            const result = await fabric.execute({
                pattern: 'explain_code',
                input: selection
            });

            // Show in panel
            const panel = vscode.window.createWebviewPanel(
                'fabricExplain',
                'Code Explanation',
                vscode.ViewColumn.Beside,
                {}
            );
            panel.webview.html = `<pre>${result.output}</pre>`;
        }
    );

    // Command: Improve writing
    let improveWriting = vscode.commands.registerCommand(
        'fabric.improveWriting',
        async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) return;

            const selection = editor.document.getText(editor.selection);

            const result = await fabric.execute({
                pattern: 'improve_writing',
                input: selection
            });

            // Replace selection
            editor.edit(editBuilder => {
                editBuilder.replace(editor.selection, result.output);
            });
        }
    );

    context.subscriptions.push(explainCode, improveWriting);
}
```

## Summary

In this chapter, you've learned:

- **REST API**: Server setup and endpoint usage
- **Python SDK**: Sync and async integration
- **JavaScript**: Node.js and browser integration
- **Automation**: GitHub Actions, Slack, Zapier
- **Custom Tools**: CLI tools and VS Code extensions

## Key Takeaways

1. **API First**: Fabric's API enables integration anywhere
2. **Async for Scale**: Use async operations for batch processing
3. **Automation Ready**: Integrate with CI/CD and chat platforms
4. **Build Custom Tools**: Create domain-specific applications
5. **Streaming**: Use streaming for better UX with long outputs

## Next Steps

Ready to deploy Fabric for enterprise use? Let's explore Chapter 8.

---

**Ready for Chapter 8?** [Enterprise Deployment](08-enterprise-deployment.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `pattern`, `fabric`, `input` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Integration & API` as an operating subsystem inside **Fabric Tutorial: Open-Source Framework for Augmenting Humans with AI**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Fabric`, `result`, `content` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Integration & API` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `pattern`.
2. **Input normalization**: shape incoming data so `fabric` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `input`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/danielmiessler/Fabric)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [Pattern Library](https://github.com/danielmiessler/fabric/tree/main/data/patterns)
  Why it matters: authoritative reference on `Pattern Library` (github.com).
- [Community Patterns](https://github.com/danielmiessler/Fabric#community-patterns)
  Why it matters: authoritative reference on `Community Patterns` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `pattern` and `fabric` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Custom Patterns](06-custom-patterns.md)
- [Next Chapter: Chapter 8: Enterprise Deployment](08-enterprise-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
