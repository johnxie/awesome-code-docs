---
layout: default
title: "Chapter 8: Production Operations and Security"
nav_order: 8
parent: gptme Tutorial
---

# Chapter 8: Production Operations and Security

Production gptme workflows require clear policy on tool permissions, secret handling, and trusted repositories.

## Security Checklist

1. treat repo-local config as code and review before execution
2. keep secret keys in env/local override files, not committed config
3. restrict dangerous tools in shared CI environments
4. validate generated changes with tests before merge

## Source References

- [gptme security docs](https://github.com/gptme/gptme/blob/master/docs/security.rst)
- [Configuration docs](https://github.com/gptme/gptme/blob/master/docs/config.rst)

## Summary

You now have a security and operations baseline for running gptme in production environments.
