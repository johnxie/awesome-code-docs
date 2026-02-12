---
layout: default
title: "Chapter 6: Setup/Teardown Presets and Automation"
nav_order: 6
parent: Superset Terminal Tutorial
---

# Chapter 6: Setup/Teardown Presets and Automation

Superset supports workspace automation through setup/teardown script presets.

## Preset Configuration

Example `.superset/config.json`:

```json
{
  "setup": ["./.superset/setup.sh"],
  "teardown": ["./.superset/teardown.sh"]
}
```

## Source References

- [Superset README: configuration section](https://github.com/superset-sh/superset/blob/main/README.md)
- [Default preset config](https://github.com/superset-sh/superset/blob/main/.superset/config.json)

## Summary

You now understand how to standardize workspace initialization and cleanup workflows.

Next: [Chapter 7: Runtime and Package Architecture](07-runtime-and-package-architecture.md)
