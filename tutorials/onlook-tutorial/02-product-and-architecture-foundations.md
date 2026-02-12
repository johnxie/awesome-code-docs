---
layout: default
title: "Chapter 2: Product and Architecture Foundations"
nav_order: 2
parent: Onlook Tutorial
---

# Chapter 2: Product and Architecture Foundations

This chapter explains how Onlook's architecture maps visual interaction to real code changes.

## Learning Goals

- understand core architectural flow
- identify responsibilities of editor, preview, and code layers
- reason about portability and framework scope
- map architecture to debugging strategy

## High-Level Flow

From Onlook docs and README:

1. app code runs in a containerized runtime
2. editor renders preview in an iFrame
3. editor indexes and maps DOM elements to code locations
4. edits are applied in preview, then persisted to source
5. AI tools also operate against code-aware context

## Why This Matters

- keeps developers in control of source code outputs
- supports rapid visual iteration without abandoning engineering rigor
- creates a path to collaboration and reproducibility through action history

## Source References

- [Onlook README: How it works](https://github.com/onlook-dev/onlook/blob/main/README.md#how-it-works)
- [Onlook Architecture Docs](https://docs.onlook.com/developers/architecture)

## Summary

You now have a systems-level model for how Onlook transforms edits into code.

Next: [Chapter 3: Visual Editing and Code Mapping](03-visual-editing-and-code-mapping.md)
