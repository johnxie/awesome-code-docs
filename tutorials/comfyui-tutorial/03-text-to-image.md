---
layout: default
title: "Chapter 3: Text-to-Image Generation"
parent: "ComfyUI Tutorial"
nav_order: 3
---

# Chapter 3: Text-to-Image Generation

Welcome to **Chapter 3: Text-to-Image Generation**. In this part of **ComfyUI Tutorial: Mastering AI Image Generation Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Now that you understand nodes and workflows, let's create stunning images from text prompts! This chapter covers the art and science of text-to-image generation, from basic prompts to advanced techniques.

## Prompt Engineering Fundamentals

### Basic Prompt Structure

```javascript
// Effective prompt components
const promptComponents = {
  subject: "a majestic lion",
  style: "in the style of Salvador Dali",
  quality: "highly detailed, masterpiece",
  lighting: "dramatic lighting, golden hour",
  composition: "centered composition, rule of thirds",
  medium: "oil painting, photorealistic"
};

// Complete prompt example
const examplePrompt = `
A majestic lion standing proudly on a cliff,
in the style of Salvador Dali,
highly detailed masterpiece,
dramatic golden hour lighting,
centered composition,
oil painting, photorealistic,
intricate fur texture, sharp focus
`;
```

### Prompt Weighting Techniques

```javascript
// Weighted prompt syntax
const weightedPrompt = `
(masterpiece:1.2) (best quality:1.1) (highly detailed:1.0)
a beautiful landscape (mountains:1.3) (river:1.2) (forest:1.1)
(dramatic lighting:1.2) (golden hour:1.1)
(oil painting:1.0) (photorealistic:0.9)
--negative
blurry, low quality, distorted, ugly, poorly drawn
`;
```

## Model Selection and Configuration

### Popular Models

```javascript
// Model configurations
const modelConfigs = {
  realisticVision: {
    name: "Realistic_Vision_V5.1",
    type: "realistic",
    recommendedSettings: {
      steps: 20,
      cfg: 7.0,
      sampler: "euler",
      scheduler: "normal"
    }
  },

  dreamShaper: {
    name: "DreamShaper_8",
    type: "artistic",
    recommendedSettings: {
      steps: 25,
      cfg: 8.0,
      sampler: "dpmpp_2m",
      scheduler: "karras"
    }
  },

  anythingV5: {
    name: "Anything_V5",
    type: "anime",
    recommendedSettings: {
      steps: 20,
      cfg: 7.0,
      sampler: "euler_a",
      scheduler: "normal"
    }
  }
};
```

### Sampler Selection

```javascript
// Sampler comparison
const samplerComparison = {
  euler: {
    speed: "fast",
    quality: "good",
    useCase: "general purpose"
  },

  dpmpp_2m: {
    speed: "medium",
    quality: "excellent",
    useCase: "high quality"
  },

  dpmpp_2m_karras: {
    speed: "medium",
    quality: "very high",
    useCase: "premium quality"
  },

  lms: {
    speed: "slow",
    quality: "high",
    useCase: "consistent results"
  }
};
```

## Advanced Generation Parameters

### CFG Scale Optimization

```javascript
// CFG scale effects
const cfgScaleGuide = {
  low: {
    range: "1.0-4.0",
    effect: "creative, varied results",
    useCase: "brainstorming, abstract art"
  },

  medium: {
    range: "5.0-8.0",
    effect: "balanced creativity and adherence",
    useCase: "most general use cases"
  },

  high: {
    range: "9.0-15.0",
    effect: "strict prompt following",
    useCase: "precise requirements, product shots"
  },

  veryHigh: {
    range: "16.0+",
    effect: "over-adherence, potential artifacts",
    useCase: "experimental, specific styles"
  }
};
```

### Step Count Optimization

```javascript
// Steps vs quality relationship
const stepOptimization = {
  fast: {
    steps: "10-15",
    quality: "acceptable",
    useCase: "prototyping, quick iterations"
  },

  standard: {
    steps: "20-25",
    quality: "good",
    useCase: "most applications"
  },

  high: {
    steps: "30-40",
    quality: "excellent",
    useCase: "final renders, portfolio work"
  },

  ultra: {
    steps: "50+",
    quality: "diminishing returns",
    useCase: "research, maximum quality"
  }
};
```

## Seed Control and Reproducibility

### Seed Management

```javascript
// Seed control strategies
const seedStrategies = {
  fixed: {
    seed: 12345,
    advantage: "reproducible results",
    useCase: "consistent character designs"
  },

  random: {
    seed: -1,
    advantage: "varied results",
    useCase: "exploration, batch generation"
  },

  incremental: {
    seed: "previous + 1",
    advantage: "controlled variation",
    useCase: "series generation, A/B testing"
  }
};
```

### Batch Generation

```javascript
// Batch processing setup
const batchConfig = {
  emptyLatentImage: {
    batch_size: 4,
    width: 1024,
    height: 1024
  },

 ksampler: {
    seed: 12345,
    steps: 20,
    cfg: 7.0,
    batch_count: 4,
    batch_size: 1
  },

  saveImage: {
    filename_prefix: "batch_generation",
    output_path: "./output/batch"
  }
};
```

## Style and Aesthetic Control

### Artistic Styles

```javascript
// Style modifiers
const styleModifiers = {
  photography: "photorealistic, sharp focus, professional photography",
  painting: "oil painting, canvas texture, brush strokes",
  digital: "digital art, clean lines, vibrant colors",
  cinematic: "cinematic lighting, movie still, dramatic",
  minimalist: "minimalist, clean design, simple composition"
};
```

### Quality Enhancers

```javascript
// Quality improvement prompts
const qualityEnhancers = {
  technical: "highly detailed, sharp focus, professional",
  artistic: "masterpiece, best quality, award winning",
  lighting: "dramatic lighting, studio lighting, professional lighting",
  composition: "perfect composition, rule of thirds, balanced"
};
```

## Prompt Engineering Techniques

### Prompt Chaining

```javascript
// Multi-step prompt refinement
const promptChain = {
  step1: "basic concept",
  step2: "add style and mood",
  step3: "enhance technical quality",
  step4: "add specific details",
  step5: "optimize for model"
};

const chainedPrompt = `
A serene mountain lake at sunset,
peaceful atmosphere, tranquil mood,
highly detailed, masterpiece quality,
golden hour lighting, dramatic clouds,
sharp focus, professional photography,
intricate reflections, crystal clear water
`;
```

### Negative Prompt Optimization

```javascript
// Effective negative prompts
const negativePrompts = {
  general: "blurry, low quality, distorted, ugly, poorly drawn, bad anatomy",
  realistic: "cartoon, anime, illustration, painting, drawing",
  artistic: "photorealistic, photograph, realistic, photo",
  technical: "artifacts, noise, grain, compression, jpeg, watermark"
};
```

## Workflow Optimization

### Efficient Generation Setup

```javascript
// Optimized workflow configuration
const optimizedWorkflow = {
  model: "Realistic_Vision_V5.1",
  prompt: "masterpiece, best quality, highly detailed",
  negative: "blurry, low quality, distorted",
  settings: {
    steps: 20,
    cfg: 7.0,
    sampler: "euler",
    scheduler: "normal",
    width: 1024,
    height: 1024
  },
  performance: {
    batch_size: 1,
    vae_tiling: true,
    attention_optimization: "xformers"
  }
};
```

### Quality vs Speed Trade-offs

```javascript
// Performance presets
const performancePresets = {
  draft: {
    steps: 10,
    cfg: 6.0,
    resolution: "512x512",
    useCase: "quick previews"
  },

  standard: {
    steps: 20,
    cfg: 7.0,
    resolution: "1024x1024",
    useCase: "most applications"
  },

  premium: {
    steps: 30,
    cfg: 8.0,
    resolution: "1536x1536",
    useCase: "professional work"
  }
};
```

## Troubleshooting Generation Issues

### Common Problems

```javascript
// Issue diagnosis and solutions
const troubleshooting = {
  "blurry results": {
    cause: "Low step count or CFG too low",
    solution: "Increase steps to 20+, CFG to 7.0+"
  },

  "artifacts": {
    cause: "CFG too high or incompatible sampler",
    solution: "Reduce CFG to 8.0 or switch sampler"
  },

  "inconsistent style": {
    cause: "Weak or conflicting prompts",
    solution: "Strengthen style keywords, use weights"
  },

  "poor composition": {
    cause: "Missing composition guidance",
    solution: "Add composition keywords and aspect ratios"
  }
};
```

## Advanced Techniques

### Prompt Templates

```javascript
// Reusable prompt templates
const promptTemplates = {
  portrait: `
(masterpiece, best quality, highly detailed)
portrait of PERSON,
AGE years old, GENDER,
EMOTION expression,
HAIR_STYLE hair, EYE_COLOR eyes,
PROFESSIONAL_PHOTOGRAPHY,
sharp focus, professional lighting
--negative
blurry, low quality, deformed, ugly
  `,

  landscape: `
(masterpiece, best quality, highly detailed)
LOCATION landscape,
TIME_OF_DAY lighting,
WEATHER conditions,
MOOD atmosphere,
PROFESSIONAL_PHOTOGRAPHY,
sharp focus, depth of field
--negative
blurry, low quality, distorted
  `
};
```

### Iterative Refinement

```javascript
// Step-by-step improvement process
const refinementProcess = {
  step1: "Generate initial concept",
  step2: "Refine composition and lighting",
  step3: "Enhance details and quality",
  step4: "Adjust colors and mood",
  step5: "Final polish and optimization"
};
```

## What We've Accomplished

Excellent! 🎨 You've mastered text-to-image generation:

1. **Prompt Engineering** - Effective prompt structure and weighting
2. **Model Selection** - Choosing the right model for your needs
3. **Parameter Optimization** - CFG, steps, and sampler selection
4. **Seed Control** - Reproducible and varied generation
5. **Style Control** - Artistic and aesthetic guidance
6. **Workflow Optimization** - Efficient generation setups
7. **Troubleshooting** - Common issues and solutions
8. **Advanced Techniques** - Templates and iterative refinement

## Next Steps

With strong text-to-image skills, let's explore image manipulation techniques. In [Chapter 4: Image-to-Image & Inpainting](04-image-to-image.md), we'll learn how to modify existing images and perform targeted edits.

---

**Practice what you've learned:**
1. Create a detailed prompt for your favorite subject
2. Experiment with different CFG scales and step counts
3. Generate a batch of images with consistent style
4. Refine a poor result using iterative techniques

*What's the most impressive image you've generated so far?* 🖼️

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `quality`, `useCase`, `lighting` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 3: Text-to-Image Generation` as an operating subsystem inside **ComfyUI Tutorial: Mastering AI Image Generation Workflows**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `steps`, `composition`, `highly` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 3: Text-to-Image Generation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `quality`.
2. **Input normalization**: shape incoming data so `useCase` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `lighting`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/comfyanonymous/ComfyUI)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `quality` and `useCase` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 2: Understanding Nodes & Workflows](02-nodes-workflows.md)
- [Next Chapter: Chapter 4: Image-to-Image & Inpainting](04-image-to-image.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
