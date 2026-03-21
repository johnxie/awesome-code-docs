---
layout: default
title: "Chapter 4: Sandbox and Preview Runtime"
nav_order: 4
parent: VibeSDK Tutorial
---


# Chapter 4: Sandbox and Preview Runtime

Welcome to **Chapter 4: Sandbox and Preview Runtime**. In this part of **VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


VibeSDK runs generated projects in isolated preview runtimes so users can validate behavior before publishing.

## Learning Goals

By the end of this chapter, you should be able to:

- explain how generated code becomes a live preview URL
- tune sandbox capacity and runtime controls
- separate sandbox/runtime failures from generation-quality issues
- design a basic incident response flow for preview instability

## Runtime Flow

1. agent finishes a generation stage with runnable outputs
2. sandbox orchestration spins up or assigns a runtime instance
3. preview routing returns a URL to user session
4. runtime logs and errors feed back into fix loops
5. stable results can be promoted to deployment actions

## Isolation Model

```mermaid
graph TD
    A[Generation Agent] --> B[Sandbox Orchestrator]
    B --> C[Container Runtime]
    C --> D[Preview URL]
    D --> E[User Feedback]
    E --> A
```

## Core Runtime Controls

| Control | Why It Exists | Tuning Guidance |
|:--------|:--------------|:----------------|
| `SANDBOX_INSTANCE_TYPE` | defines CPU/RAM profile | start conservative, raise only when startup/latency data justifies |
| `MAX_SANDBOX_INSTANCES` | caps concurrent preview capacity | align with expected user concurrency and budget limits |
| tunnel/preview settings | controls preview reachability | keep defaults initially, change only with verified need |
| dispatch/deployment bindings | enables app handoff from preview to deploy | validate early in staging to avoid late surprises |

## Operational Baseline Metrics

Track these together, not in isolation:

- preview startup latency (p50 and p95)
- runtime restart/crash rate
- concurrent active preview count
- preview availability success rate
- cost per preview hour

## Triage: Generation vs Runtime

| Symptom | Likely Layer | First Check |
|:--------|:-------------|:------------|
| files look wrong before preview | generation pipeline | phase outputs and model routing |
| preview never starts | runtime/orchestration | sandbox logs and instance quotas |
| preview starts then dies | runtime stability | container restarts and resource pressure |
| preview works, deploy fails | deployment bindings/policy | dispatch namespace and credentials |

## Hardening Practices

- enforce idle cleanup and timeout policies
- isolate noisy tenant workloads when concurrency spikes
- keep a safe fallback instance profile
- include preview health in user-visible status telemetry

## Source References

- [VibeSDK Setup Guide](https://github.com/cloudflare/vibesdk/blob/main/docs/setup.md)
- [Architecture Diagrams](https://github.com/cloudflare/vibesdk/blob/main/docs/architecture-diagrams.md)

## Summary

You now have a runtime model for sandbox previews and a practical baseline for stability tuning.

Next: [Chapter 5: Data Layer and Persistence](05-data-layer-and-persistence.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `debug-tools/ai_request_analyzer_v2.py`

The `class` class in [`debug-tools/ai_request_analyzer_v2.py`](https://github.com/cloudflare/vibesdk/blob/HEAD/debug-tools/ai_request_analyzer_v2.py) handles a key part of this chapter's functionality:

```py
import sys
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Union, TypedDict, Protocol
from pathlib import Path
import argparse
from collections import defaultdict, Counter
import math
from enum import Enum
from abc import ABC, abstractmethod


class ContentType(Enum):
    """Enumeration for content types."""
    SOURCE_CODE = "source_code"
    JSON_DATA = "json_data" 
    MARKDOWN_STRUCTURED = "markdown_structured"
    LARGE_TEXT = "large_text"
    METADATA = "metadata"
    PROSE = "prose"


class ComponentName(Enum):
    """Enumeration for component names."""
    ROLE_SECTION = "role_section"
    GOAL_SECTION = "goal_section"
    CONTEXT_SECTION = "context_section"
    CLIENT_REQUEST = "client_request"
    BLUEPRINT = "blueprint"
    DEPENDENCIES = "dependencies"
    UI_GUIDELINES = "ui_guidelines"
    STRATEGY = "strategy"
```

This class is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `debug-tools/ai_request_analyzer_v2.py`

The `class` class in [`debug-tools/ai_request_analyzer_v2.py`](https://github.com/cloudflare/vibesdk/blob/HEAD/debug-tools/ai_request_analyzer_v2.py) handles a key part of this chapter's functionality:

```py
import sys
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Union, TypedDict, Protocol
from pathlib import Path
import argparse
from collections import defaultdict, Counter
import math
from enum import Enum
from abc import ABC, abstractmethod


class ContentType(Enum):
    """Enumeration for content types."""
    SOURCE_CODE = "source_code"
    JSON_DATA = "json_data" 
    MARKDOWN_STRUCTURED = "markdown_structured"
    LARGE_TEXT = "large_text"
    METADATA = "metadata"
    PROSE = "prose"


class ComponentName(Enum):
    """Enumeration for component names."""
    ROLE_SECTION = "role_section"
    GOAL_SECTION = "goal_section"
    CONTEXT_SECTION = "context_section"
    CLIENT_REQUEST = "client_request"
    BLUEPRINT = "blueprint"
    DEPENDENCIES = "dependencies"
    UI_GUIDELINES = "ui_guidelines"
    STRATEGY = "strategy"
```

This class is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `debug-tools/ai_request_analyzer_v2.py`

The `class` class in [`debug-tools/ai_request_analyzer_v2.py`](https://github.com/cloudflare/vibesdk/blob/HEAD/debug-tools/ai_request_analyzer_v2.py) handles a key part of this chapter's functionality:

```py
import sys
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Union, TypedDict, Protocol
from pathlib import Path
import argparse
from collections import defaultdict, Counter
import math
from enum import Enum
from abc import ABC, abstractmethod


class ContentType(Enum):
    """Enumeration for content types."""
    SOURCE_CODE = "source_code"
    JSON_DATA = "json_data" 
    MARKDOWN_STRUCTURED = "markdown_structured"
    LARGE_TEXT = "large_text"
    METADATA = "metadata"
    PROSE = "prose"


class ComponentName(Enum):
    """Enumeration for component names."""
    ROLE_SECTION = "role_section"
    GOAL_SECTION = "goal_section"
    CONTEXT_SECTION = "context_section"
    CLIENT_REQUEST = "client_request"
    BLUEPRINT = "blueprint"
    DEPENDENCIES = "dependencies"
    UI_GUIDELINES = "ui_guidelines"
    STRATEGY = "strategy"
```

This class is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.

### `debug-tools/ai_request_analyzer_v2.py`

The `BaseAnalyzer` class in [`debug-tools/ai_request_analyzer_v2.py`](https://github.com/cloudflare/vibesdk/blob/HEAD/debug-tools/ai_request_analyzer_v2.py) handles a key part of this chapter's functionality:

```py


class BaseAnalyzer(ABC):
    """Abstract base class for analyzers to ensure consistent interface."""
    
    @abstractmethod
    def analyze(self, content: str) -> Any:
        """Analyze content and return results."""
        pass


class SCOFParser(BaseAnalyzer):
    """Type-safe SCOF format parser."""
    
    SCOF_FILE_PATTERN = re.compile(
        r'# Creating new file: ([^\n]+)\n'
        r'# File Purpose: ([^\n]*(?:\n# [^\n]*)*)\n*'
        r'cat > [^\n]+ << \'EOF\'\n'
        r'(.*?)\n'
        r'EOF',
        re.DOTALL | re.MULTILINE
    )
    
    SCOF_DIFF_PATTERN = re.compile(
        r'# Applying diff to file: ([^\n]+)\n'
        r'# File Purpose: ([^\n]*(?:\n# [^\n]*)*)\n*'
        r'cat << \'EOF\' \| patch [^\n]+\n'
        r'(.*?)\n'
        r'EOF',
        re.DOTALL | re.MULTILINE
    )
    
```

This class is important because it defines how VibeSDK Tutorial: Build a Vibe-Coding Platform on Cloudflare implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[class]
    B[class]
    C[class]
    D[BaseAnalyzer]
    E[for]
    A --> B
    B --> C
    C --> D
    D --> E
```
