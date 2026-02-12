---
layout: default
title: "Chapter 4: Configuration and Plugin Loading"
nav_order: 4
parent: Stagewise Tutorial
---

# Chapter 4: Configuration and Plugin Loading

`stagewise.json` governs ports, workspace behavior, and plugin loading strategy.

## Learning Goals

- configure Stagewise with stable project defaults
- control automatic and explicit plugin loading
- understand config precedence and overrides

## Example `stagewise.json`

```json
{
  "port": 3100,
  "appPort": 3000,
  "autoPlugins": true,
  "plugins": [
    "@stagewise/react-plugin",
    {
      "name": "custom-plugin",
      "path": "./plugins/custom-plugin/dist"
    }
  ]
}
```

## Precedence Order

1. command-line flags
2. `stagewise.json`
3. default values

## Source References

- [CLI Deep Dive](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/advanced-usage/cli-deep-dive.mdx)
- [Install Plugins](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/advanced-usage/install-plugins.mdx)

## Summary

You now have a configuration model for predictable per-project Stagewise behavior.

Next: [Chapter 5: Building Plugins with Plugin SDK](05-building-plugins-with-plugin-sdk.md)
