---
layout: default
title: "Chapter 3: Basic Usage"
parent: "Fabric Tutorial"
nav_order: 3
---

# Chapter 3: Basic Usage

> Master core commands and workflows for everyday cognitive augmentation with Fabric.

## Overview

This chapter covers the fundamental ways to use Fabric for daily tasks. You'll learn command-line operations, input/output handling, and common workflow patterns.

## Command-Line Basics

### Core Syntax

```bash
# Basic pattern execution
fabric -p <pattern_name> [options] [input]

# Common flags
fabric --help                    # Show help
fabric --list                    # List all patterns
fabric -p pattern --show         # View pattern content
fabric --version                 # Show version
```

### Input Methods

```bash
# Pipe input (most common)
echo "text content" | fabric -p summarize

# File input
fabric -p summarize < document.txt
fabric -p summarize -i document.txt

# URL input
fabric -p summarize --url https://example.com/article

# Interactive input
fabric -p summarize
# Then type content, Ctrl+D to end

# Clipboard (macOS)
pbpaste | fabric -p summarize

# Clipboard (Linux with xclip)
xclip -selection clipboard -o | fabric -p summarize
```

### Output Methods

```bash
# Standard output
cat file.txt | fabric -p summarize

# File output
cat file.txt | fabric -p summarize > output.txt
cat file.txt | fabric -p summarize -o output.txt

# Clipboard (macOS)
cat file.txt | fabric -p summarize | pbcopy

# Append to file
cat file.txt | fabric -p summarize >> notes.txt

# Tee for display and file
cat file.txt | fabric -p summarize | tee output.txt
```

## Common Workflows

### Content Summarization

```bash
# Summarize an article
curl -s https://example.com/article | fabric -p summarize

# Summarize a PDF (extract text first)
pdftotext document.pdf - | fabric -p summarize

# Summarize meeting notes
fabric -p summarize < meeting_notes.txt

# Quick micro-summary
cat long_document.txt | fabric -p summarize_micro
```

### Research Workflows

```bash
# Extract key insights from content
cat research_paper.txt | fabric -p extract_wisdom

# Analyze claims in an article
cat news_article.txt | fabric -p analyze_claims

# Extract references
cat paper.txt | fabric -p extract_references

# Generate study questions
cat chapter.txt | fabric -p extract_questions
```

### Writing Assistance

```bash
# Improve writing quality
cat draft.txt | fabric -p improve_writing

# Create an outline
echo "Topic: AI in Healthcare" | fabric -p create_outline

# Expand bullet points to prose
cat bullets.txt | fabric -p write_essay

# Proofread and edit
cat document.txt | fabric -p improve_writing --style professional
```

### Code Workflows

```bash
# Explain code
cat script.py | fabric -p explain_code

# Code review
cat pull_request.diff | fabric -p review_code

# Generate tests
cat module.py | fabric -p write_tests

# Document code
cat function.py | fabric -p create_docs
```

## Chaining Commands

### Unix Pipes

```bash
# Extract wisdom then summarize
cat article.txt | fabric -p extract_wisdom | fabric -p summarize

# Analyze claims then rate credibility
cat news.txt | fabric -p analyze_claims | fabric -p rate_content

# Process multiple files
for f in articles/*.txt; do
    fabric -p summarize < "$f" > "summaries/$(basename $f)"
done
```

### Processing Pipelines

```bash
# Research pipeline
curl -s https://example.com/paper | \
    fabric -p extract_wisdom | \
    fabric -p create_outline | \
    tee research_notes.md

# Content improvement pipeline
cat draft.txt | \
    fabric -p improve_writing | \
    fabric -p summarize_micro > improved_with_summary.txt

# Analysis pipeline
cat article.txt | \
    fabric -p analyze_claims > claims.md && \
    fabric -p extract_wisdom < article.txt > wisdom.md
```

### Batch Processing

```bash
# Process directory of files
find ./documents -name "*.txt" -exec sh -c '
    fabric -p summarize < "{}" > "./summaries/$(basename {}).summary.md"
' \;

# Parallel processing (using GNU parallel)
ls articles/*.txt | parallel 'fabric -p summarize < {} > summaries/{/.}.md'

# Aggregate results
cat summaries/*.md | fabric -p create_synthesis > final_synthesis.md
```

## Model Configuration

### Selecting Models

```bash
# Use GPT-4
fabric -p summarize --model gpt-4 < input.txt

# Use GPT-4 Turbo
fabric -p summarize --model gpt-4-turbo-preview < input.txt

# Use Claude 3 Opus
fabric -p summarize --model claude-3-opus-20240229 < input.txt

# Use Claude 3 Sonnet
fabric -p summarize --model claude-3-sonnet-20240229 < input.txt

# Use local model (Ollama)
fabric -p summarize --model ollama:llama2 < input.txt
fabric -p summarize --model ollama:mistral < input.txt
```

### Model Environment

```bash
# Set default model in config
fabric --setup

# Environment variables
export FABRIC_MODEL="gpt-4"
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Per-command override
FABRIC_MODEL="claude-3-opus-20240229" fabric -p summarize < input.txt
```

### Model Comparison

```bash
# Compare outputs from different models
echo "Content here" | fabric -p summarize --model gpt-4 > gpt4_summary.txt
echo "Content here" | fabric -p summarize --model claude-3-opus > claude_summary.txt

# Diff results
diff gpt4_summary.txt claude_summary.txt
```

## Configuration

### Setup Wizard

```bash
# Run initial setup
fabric --setup

# Configure API keys
# Follow prompts for:
# - OpenAI API key
# - Anthropic API key
# - Local model settings
```

### Configuration File

```bash
# Config location
~/.config/fabric/config.yaml

# Example configuration
cat > ~/.config/fabric/config.yaml << 'EOF'
default_model: gpt-4
temperature: 0.7
max_tokens: 4096
api_keys:
  openai: ${OPENAI_API_KEY}
  anthropic: ${ANTHROPIC_API_KEY}
patterns_dir: ~/.config/fabric/patterns
EOF
```

### Environment Variables

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export FABRIC_MODEL="gpt-4"
export FABRIC_PATTERNS_DIR="$HOME/.config/fabric/patterns"
```

## Practical Examples

### Daily Workflow Examples

```bash
# Morning news digest
curl -s https://news.site/rss | \
    fabric -p summarize | \
    mail -s "News Digest" you@email.com

# Meeting prep
cat meeting_agenda.txt | fabric -p extract_questions > prep_questions.md

# Email drafting
echo "Decline politely: Meeting request from vendor" | \
    fabric -p write_email --tone professional

# Quick research
curl -s "https://en.wikipedia.org/api/rest_v1/page/summary/Topic" | \
    jq -r '.extract' | \
    fabric -p extract_wisdom
```

### Developer Workflows

```bash
# Code review helper
git diff HEAD~1 | fabric -p review_code

# Commit message generator
git diff --cached | fabric -p create_commit_message

# Documentation update
cat api_changes.md | fabric -p update_docs

# Debug assistant
cat error_log.txt | fabric -p analyze_error
```

### Learning Workflows

```bash
# Study material processing
cat textbook_chapter.txt | fabric -p extract_wisdom > study_notes.md
cat textbook_chapter.txt | fabric -p extract_questions > quiz.md

# Concept explanation
echo "Explain: Quantum Entanglement" | fabric -p explain_concept

# Vocabulary building
cat article.txt | fabric -p extract_vocabulary > vocab_list.md
```

## Shell Integration

### Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias sum='fabric -p summarize'
alias wis='fabric -p extract_wisdom'
alias claims='fabric -p analyze_claims'
alias improve='fabric -p improve_writing'
alias codex='fabric -p explain_code'

# Usage
cat article.txt | sum
cat research.txt | wis
```

### Functions

```bash
# Smart summarize function
sumurl() {
    curl -s "$1" | fabric -p summarize
}

# Research function
research() {
    echo "$1" | fabric -p create_outline > outline.md
    curl -s "https://en.wikipedia.org/api/rest_v1/page/summary/$1" | \
        jq -r '.extract' | fabric -p extract_wisdom >> outline.md
}

# Usage
sumurl https://example.com/article
research "Machine Learning"
```

## Summary

In this chapter, you've learned:

- **Command-Line Basics**: Core syntax and flags
- **Input/Output**: Multiple methods for feeding and capturing content
- **Common Workflows**: Summarization, research, writing, coding
- **Chaining**: Building powerful pipelines with Unix pipes
- **Model Configuration**: Selecting and configuring AI models
- **Shell Integration**: Aliases and functions for efficiency

## Key Takeaways

1. **Pipes are Powerful**: Unix philosophy applies perfectly to Fabric
2. **Choose the Right Pattern**: Match pattern to task
3. **Batch Processing**: Scale workflows with loops and parallel
4. **Model Flexibility**: Switch models for different tasks
5. **Integrate Daily**: Add Fabric to your shell for quick access

## Next Steps

Ready to explore advanced pattern usage? Let's dive into Chapter 4.

---

**Ready for Chapter 4?** [Advanced Patterns](04-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
