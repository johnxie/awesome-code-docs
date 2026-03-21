---
layout: default
title: "Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts"
nav_order: 3
parent: GenAI Toolbox Tutorial
---


# Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts

Welcome to **Chapter 3: `tools.yaml`: Sources, Tools, Toolsets, Prompts**. In this part of **GenAI Toolbox Tutorial: MCP-First Database Tooling with Config-Driven Control Planes**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on building maintainable configuration contracts in `tools.yaml`.

## Learning Goals

- model sources cleanly and avoid hardcoded secrets
- define tools with safe parameters and clear descriptions
- group capabilities into toolsets for context-specific loading
- add prompt templates for repeatable model instruction patterns

## Configuration Rule

Treat `tools.yaml` as a versioned interface contract. Keep it small, explicit, and environment-variable driven to avoid hidden coupling and credential leakage.

## Source References

- [Configuration Guide](https://github.com/googleapis/genai-toolbox/blob/main/docs/en/getting-started/configure.md)
- [README Configuration](https://github.com/googleapis/genai-toolbox/blob/main/README.md)

## Summary

You can now design `tools.yaml` schemas that stay readable and stable as capabilities grow.

Next: [Chapter 4: MCP Connectivity and Client Integration](04-mcp-connectivity-and-client-integration.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `internal/server/config.go`

The `UnmarshalYAMLToolsetConfig` function in [`internal/server/config.go`](https://github.com/googleapis/genai-toolbox/blob/HEAD/internal/server/config.go) handles a key part of this chapter's functionality:

```go
			toolConfigs[name] = c
		case "toolsets":
			c, err := UnmarshalYAMLToolsetConfig(ctx, name, resource)
			if err != nil {
				return nil, nil, nil, nil, nil, nil, fmt.Errorf("error unmarshaling %s: %s", kind, err)
			}
			if toolsetConfigs == nil {
				toolsetConfigs = make(ToolsetConfigs)
			}
			toolsetConfigs[name] = c
		case "embeddingModels":
			c, err := UnmarshalYAMLEmbeddingModelConfig(ctx, name, resource)
			if err != nil {
				return nil, nil, nil, nil, nil, nil, fmt.Errorf("error unmarshaling %s: %s", kind, err)
			}
			if embeddingModelConfigs == nil {
				embeddingModelConfigs = make(EmbeddingModelConfigs)
			}
			embeddingModelConfigs[name] = c
		case "prompts":
			c, err := UnmarshalYAMLPromptConfig(ctx, name, resource)
			if err != nil {
				return nil, nil, nil, nil, nil, nil, fmt.Errorf("error unmarshaling %s: %s", kind, err)
			}
			if promptConfigs == nil {
				promptConfigs = make(PromptConfigs)
			}
			promptConfigs[name] = c
		default:
			return nil, nil, nil, nil, nil, nil, fmt.Errorf("invalid kind %s", kind)
		}
	}
```

This function is important because it defines how GenAI Toolbox Tutorial: MCP-First Database Tooling with Config-Driven Control Planes implements the patterns covered in this chapter.

### `internal/server/config.go`

The `UnmarshalYAMLPromptConfig` function in [`internal/server/config.go`](https://github.com/googleapis/genai-toolbox/blob/HEAD/internal/server/config.go) handles a key part of this chapter's functionality:

```go
			embeddingModelConfigs[name] = c
		case "prompts":
			c, err := UnmarshalYAMLPromptConfig(ctx, name, resource)
			if err != nil {
				return nil, nil, nil, nil, nil, nil, fmt.Errorf("error unmarshaling %s: %s", kind, err)
			}
			if promptConfigs == nil {
				promptConfigs = make(PromptConfigs)
			}
			promptConfigs[name] = c
		default:
			return nil, nil, nil, nil, nil, nil, fmt.Errorf("invalid kind %s", kind)
		}
	}
	return sourceConfigs, authServiceConfigs, embeddingModelConfigs, toolConfigs, toolsetConfigs, promptConfigs, nil
}

func UnmarshalYAMLSourceConfig(ctx context.Context, name string, r map[string]any) (sources.SourceConfig, error) {
	resourceType, ok := r["type"].(string)
	if !ok {
		return nil, fmt.Errorf("missing 'type' field or it is not a string")
	}
	dec, err := util.NewStrictDecoder(r)
	if err != nil {
		return nil, fmt.Errorf("error creating decoder: %w", err)
	}
	sourceConfig, err := sources.DecodeConfig(ctx, resourceType, name, dec)
	if err != nil {
		return nil, err
	}
	return sourceConfig, nil
}
```

This function is important because it defines how GenAI Toolbox Tutorial: MCP-First Database Tooling with Config-Driven Control Planes implements the patterns covered in this chapter.

### `internal/server/config.go`

The `NameValidation` function in [`internal/server/config.go`](https://github.com/googleapis/genai-toolbox/blob/HEAD/internal/server/config.go) handles a key part of this chapter's functionality:

```go
// Tool names SHOULD NOT contain spaces, commas, or other special characters.
// Tool names SHOULD be unique within a server.
func NameValidation(name string) error {
	strLen := len(name)
	if strLen < 1 || strLen > 128 {
		return fmt.Errorf("resource name SHOULD be between 1 and 128 characters in length (inclusive)")
	}
	validChars := regexp.MustCompile("^[a-zA-Z0-9_.-]+$")
	isValid := validChars.MatchString(name)
	if !isValid {
		return fmt.Errorf("invalid character for resource name; only uppercase and lowercase ASCII letters (A-Z, a-z), digits (0-9), underscore (_), hyphen (-), and dot (.) is allowed")
	}
	return nil
}

```

This function is important because it defines how GenAI Toolbox Tutorial: MCP-First Database Tooling with Config-Driven Control Planes implements the patterns covered in this chapter.

### `internal/server/config.go`

The `the` interface in [`internal/server/config.go`](https://github.com/googleapis/genai-toolbox/blob/HEAD/internal/server/config.go) handles a key part of this chapter's functionality:

```go
// Copyright 2024 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//	http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package server

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"regexp"
	"strings"

	yaml "github.com/goccy/go-yaml"
	"github.com/googleapis/genai-toolbox/internal/auth"
	"github.com/googleapis/genai-toolbox/internal/auth/google"
	"github.com/googleapis/genai-toolbox/internal/embeddingmodels"
	"github.com/googleapis/genai-toolbox/internal/embeddingmodels/gemini"
	"github.com/googleapis/genai-toolbox/internal/prompts"
	"github.com/googleapis/genai-toolbox/internal/sources"
	"github.com/googleapis/genai-toolbox/internal/tools"
	"github.com/googleapis/genai-toolbox/internal/util"
```

This interface is important because it defines how GenAI Toolbox Tutorial: MCP-First Database Tooling with Config-Driven Control Planes implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[UnmarshalYAMLToolsetConfig]
    B[UnmarshalYAMLPromptConfig]
    C[NameValidation]
    D[the]
    E[InitializeConfigs]
    A --> B
    B --> C
    C --> D
    D --> E
```
