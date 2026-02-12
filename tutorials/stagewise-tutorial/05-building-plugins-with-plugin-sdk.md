---
layout: default
title: "Chapter 5: Building Plugins with Plugin SDK"
nav_order: 5
parent: Stagewise Tutorial
---

# Chapter 5: Building Plugins with Plugin SDK

Plugins let teams add custom toolbar UX and prompt behavior without forking the core project.

## Learning Goals

- scaffold plugin projects quickly
- implement the `ToolbarPlugin` contract
- test and load local plugins in Stagewise

## Fast Scaffold

```bash
npx create-stagewise-plugin
```

## Minimal Plugin Shape

```tsx
import type { ToolbarPlugin } from '@stagewise/toolbar';

const MyPlugin: ToolbarPlugin = {
  pluginName: 'my-plugin',
  displayName: 'My Plugin',
  description: 'Custom toolbar integration'
};

export default MyPlugin;
```

## Development Notes

- use local path loading for rapid iteration
- validate plugin behavior in a real app workspace
- keep plugin responsibilities narrow and composable

## Source References

- [Build Plugins Guide](https://github.com/stagewise-io/stagewise/blob/main/apps/website/content/docs/developer-guides/build-plugins.mdx)
- [Plugin SDK README](https://github.com/stagewise-io/stagewise/blob/main/toolbar/plugin-sdk/README.md)
- [Create Stagewise Plugin README](https://github.com/stagewise-io/stagewise/blob/main/packages/create-stagewise-plugin/README.md)

## Summary

You now know how to create and iterate on custom Stagewise plugins.

Next: [Chapter 6: Custom Agent Integrations with Agent Interface](06-custom-agent-integrations-with-agent-interface.md)
