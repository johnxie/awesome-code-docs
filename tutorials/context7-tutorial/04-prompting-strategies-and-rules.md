---
layout: default
title: "Chapter 4: Prompting Strategies and Rules"
nav_order: 4
parent: Context7 Tutorial
---

# Chapter 4: Prompting Strategies and Rules

This chapter focuses on prompt discipline so Context7 is reliably invoked with high signal.

## Learning Goals

- trigger Context7 intentionally for API-sensitive tasks
- use library IDs when available to improve retrieval precision
- set reusable client rules for auto invocation
- reduce generic/noisy documentation fetches

## Prompt Patterns

| Pattern | Example |
|:--------|:--------|
| explicit invoke | "Set up Next.js middleware. use context7" |
| direct library ID | "Use library `/vercel/next.js` for app router auth docs" |
| version hint | "How do I configure Next.js 14 middleware? use context7" |

## Rules Automation

Add client rule text to auto trigger docs lookup for library/API questions so users do not have to remember the invoke phrase each time.

## Source References

- [Context7 README: Add a Rule](https://github.com/upstash/context7/blob/master/README.md#add-a-rule)
- [Context7 README: Use Library Id](https://github.com/upstash/context7/blob/master/README.md#use-library-id)

## Summary

You now know how to structure prompts and rules so Context7 activates predictably.

Next: [Chapter 5: API Workflows and SDK Patterns](05-api-workflows-and-sdk-patterns.md)
