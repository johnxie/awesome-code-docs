---
layout: default
title: "Chapter 7: Multilingual Tokenization"
nav_order: 7
parent: tiktoken Tutorial
---

# Chapter 7: Multilingual Tokenization

Token distributions vary significantly across languages and scripts.

## Key Considerations

- token-to-character ratios differ by language family
- emoji and mixed-script text can inflate token counts
- localization can materially change context budgets

## Testing Strategy

- maintain benchmark prompts per target language
- compare token counts before shipping localized prompts
- alert when localization exceeds model/token budgets

## Summary

You can now plan multilingual prompt budgets with fewer surprises.

Next: [Chapter 8: Cost Governance](08-cost-governance.md)
