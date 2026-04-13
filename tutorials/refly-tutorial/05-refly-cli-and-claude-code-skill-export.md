---
layout: default
title: "Chapter 5: Refly CLI and Claude Code Skill Export"
nav_order: 5
parent: Refly Tutorial
---


# Chapter 5: Refly CLI and Claude Code Skill Export

Welcome to **Chapter 5: Refly CLI and Claude Code Skill Export**. In this part of **Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter explains how to use the CLI for deterministic workflow operations and how Refly skills connect to Claude Code contexts.

## Learning Goals

- run builder/validation/commit loops from terminal
- use structured CLI output for automation chains
- export/install skills for Claude Code-oriented workflows
- keep orchestration reproducible across environments

## High-Value CLI Flow

```bash
npm install -g @refly/cli
refly init
refly login
refly builder start --name "my-workflow"
refly builder validate
refly builder commit
refly workflow run <workflowId>
```

## Claude Code-Oriented Skill Path

- `refly init` installs skill references into Claude directories
- skill operations can be managed with `refly skill ...` commands
- exported skills can be used in Claude Code and other MCP-capable contexts

## Source References

- [Refly CLI README](https://github.com/refly-ai/refly/blob/main/packages/cli/README.md)
- [CLI Skill Reference](https://github.com/refly-ai/refly/blob/main/packages/cli/skill/SKILL.md)
- [README: Skills for Claude Code](https://github.com/refly-ai/refly/blob/main/README.md#use-case-3-skills-for-claude-code)

## Summary

You now have a deterministic CLI path for building, validating, and exporting workflow capabilities.

Next: [Chapter 6: Observability, Deployment, and Operations](06-observability-deployment-and-operations.md)

## Source Code Walkthrough

### `docs/scripts/convert-webp.js`

The `convertImagesToWebp` function in [`docs/scripts/convert-webp.js`](https://github.com/refly-ai/refly/blob/HEAD/docs/scripts/convert-webp.js) handles a key part of this chapter's functionality:

```js
const imageMap = new Map();

async function convertImagesToWebp() {
  try {
    const files = await fs.readdir(imagesDir);
    const imageFiles = files.filter((file) => {
      const ext = path.extname(file).toLowerCase();
      return ['.png', '.jpg', '.jpeg', '.gif'].includes(ext);
    });

    console.log(`Found ${imageFiles.length} images to convert`);

    for (const file of imageFiles) {
      const inputPath = path.join(imagesDir, file);
      const fileInfo = path.parse(file);
      const outputPath = path.join(imagesDir, `${fileInfo.name}.webp`);

      try {
        // Convert to WebP
        await sharp(inputPath).webp({ quality: 80 }).toFile(outputPath);

        // Store the mapping from original path to WebP path (for use in Markdown replacements)
        const originalRelativePath = path.join('/images', file);
        const webpRelativePath = path.join('/images', `${fileInfo.name}.webp`);
        imageMap.set(originalRelativePath, webpRelativePath);

        // Remove the original file
        await fs.unlink(inputPath);

        console.log(`Converted and replaced: ${file} -> ${fileInfo.name}.webp`);
      } catch (error) {
        console.error(`Error converting ${file}: ${error.message}`);
```

This function is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.

### `docs/scripts/convert-webp.js`

The `findMarkdownFiles` function in [`docs/scripts/convert-webp.js`](https://github.com/refly-ai/refly/blob/HEAD/docs/scripts/convert-webp.js) handles a key part of this chapter's functionality:

```js
}

async function findMarkdownFiles(dir) {
  const result = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      // Skip node_modules and .git directories
      if (entry.name !== 'node_modules' && entry.name !== '.git') {
        const nestedFiles = await findMarkdownFiles(fullPath);
        result.push(...nestedFiles);
      }
    } else if (entry.name.endsWith('.md')) {
      result.push(fullPath);
    }
  }

  return result;
}

async function updateMarkdownFiles() {
  try {
    const markdownFiles = await findMarkdownFiles(rootDir);
    console.log(`Found ${markdownFiles.length} Markdown files to update`);

    for (const file of markdownFiles) {
      let content = await fs.readFile(file, 'utf-8');
      let modified = false;

```

This function is important because it defines how Refly Tutorial: Build Deterministic Agent Skills and Ship Them Across APIs and Claude Code implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[convertImagesToWebp]
    B[findMarkdownFiles]
    A --> B
```
