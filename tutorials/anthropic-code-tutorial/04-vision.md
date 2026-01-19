---
layout: default
title: "Chapter 4: Vision"
parent: "Anthropic API Tutorial"
nav_order: 4
---

# Chapter 4: Vision

> Process and analyze images with Claude's multimodal capabilities, from basic image understanding to complex visual analysis workflows.

## Overview

Claude's vision capabilities allow you to include images in your conversations for analysis, description, OCR, visual reasoning, and more. This chapter covers how to send images to Claude, supported formats, and practical applications of visual AI.

## Sending Images to Claude

### Base64 Encoded Images

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def encode_image(image_path: str) -> tuple[str, str]:
    """Encode an image file to base64."""
    path = Path(image_path)

    # Determine media type
    extension = path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    media_type = media_types.get(extension, 'image/jpeg')

    # Read and encode
    with open(path, 'rb') as f:
        data = base64.standard_b64encode(f.read()).decode('utf-8')

    return data, media_type

# Send image to Claude
image_data, media_type = encode_image("photo.jpg")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)

print(message.content[0].text)
```

### URL-Based Images

```python
# Send image via URL
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/image.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "Describe this image in detail."
                }
            ]
        }
    ]
)
```

### Multiple Images

```python
# Send multiple images for comparison or analysis
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image1_data
                    }
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image2_data
                    }
                },
                {
                    "type": "text",
                    "text": "Compare these two images. What are the main differences?"
                }
            ]
        }
    ]
)
```

## Supported Formats and Limits

### Image Formats

```python
# Supported formats
SUPPORTED_FORMATS = {
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
    "image/gif": [".gif"],
    "image/webp": [".webp"]
}

# Maximum dimensions and file size
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
MAX_DIMENSION = 8192  # pixels

def validate_image(image_path: str) -> tuple[bool, str]:
    """Validate image before sending to API."""
    from PIL import Image
    import os

    path = Path(image_path)

    # Check extension
    ext = path.suffix.lower()
    valid_extensions = [e for exts in SUPPORTED_FORMATS.values() for e in exts]
    if ext not in valid_extensions:
        return False, f"Unsupported format: {ext}"

    # Check file size
    size = os.path.getsize(path)
    if size > MAX_IMAGE_SIZE:
        return False, f"File too large: {size / 1024 / 1024:.1f}MB (max 20MB)"

    # Check dimensions
    with Image.open(path) as img:
        width, height = img.size
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            return False, f"Image too large: {width}x{height} (max {MAX_DIMENSION}px)"

    return True, "Valid"
```

### Image Optimization

```python
from PIL import Image
import io
import base64

def optimize_image(image_path: str, max_size: int = 1568, quality: int = 85) -> tuple[str, str]:
    """Optimize image for API (reduce size while maintaining quality)."""

    with Image.open(image_path) as img:
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize if too large
        width, height = img.size
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        data = base64.standard_b64encode(buffer.getvalue()).decode('utf-8')

    return data, 'image/jpeg'

# Usage
image_data, media_type = optimize_image("large_photo.png")
```

## Vision Use Cases

### Image Description

```python
def describe_image(image_path: str, detail_level: str = "detailed") -> str:
    """Get a description of an image."""

    image_data, media_type = encode_image(image_path)

    prompts = {
        "brief": "Describe this image in one sentence.",
        "detailed": "Describe this image in detail, including objects, colors, composition, and mood.",
        "exhaustive": """Provide an exhaustive description of this image including:
- Main subjects and objects
- Colors and lighting
- Composition and framing
- Text visible in the image
- Mood and atmosphere
- Any notable details"""
    }

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompts.get(detail_level, prompts["detailed"])
                    }
                ]
            }
        ]
    )

    return message.content[0].text
```

### OCR and Text Extraction

```python
def extract_text_from_image(image_path: str) -> dict:
    """Extract and structure text from an image."""

    image_data, media_type = encode_image(image_path)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """Extract all text from this image. Return as JSON with:
{
    "raw_text": "all text exactly as it appears",
    "structured": {
        "headings": [],
        "paragraphs": [],
        "lists": [],
        "other": []
    },
    "language": "detected language",
    "confidence": "high/medium/low"
}"""
                    }
                ]
            }
        ]
    )

    import json
    try:
        return json.loads(message.content[0].text)
    except json.JSONDecodeError:
        return {"raw_text": message.content[0].text, "structured": None}

# Extract text from receipt
result = extract_text_from_image("receipt.jpg")
print(f"Text found: {result['raw_text']}")
```

### Document Analysis

```python
def analyze_document(image_path: str, document_type: str = "general") -> dict:
    """Analyze a document image (invoice, form, receipt, etc.)."""

    image_data, media_type = encode_image(image_path)

    type_prompts = {
        "invoice": """Analyze this invoice and extract:
- Vendor name and address
- Invoice number and date
- Line items (description, quantity, price)
- Subtotal, tax, total
- Payment terms
Return as structured JSON.""",

        "receipt": """Analyze this receipt and extract:
- Store name and location
- Date and time
- Items purchased with prices
- Payment method
- Total amount
Return as structured JSON.""",

        "form": """Analyze this form and extract:
- Form title/type
- All filled fields with their labels and values
- Any signatures or dates
- Form status (complete/incomplete)
Return as structured JSON.""",

        "general": """Analyze this document and extract:
- Document type
- Key information and data points
- Any important dates or numbers
- Summary of content
Return as structured JSON."""
    }

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": type_prompts.get(document_type, type_prompts["general"])
                    }
                ]
            }
        ]
    )

    import json
    try:
        return json.loads(message.content[0].text)
    except:
        return {"analysis": message.content[0].text}
```

### Visual Q&A

```python
def visual_qa(image_path: str, questions: list[str]) -> dict:
    """Answer multiple questions about an image."""

    image_data, media_type = encode_image(image_path)

    questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": f"""Answer these questions about the image:

{questions_text}

Provide answers in JSON format:
{{"answers": [{{"question": "...", "answer": "..."}}]}}"""
                    }
                ]
            }
        ]
    )

    import json
    try:
        return json.loads(message.content[0].text)
    except:
        return {"raw_response": message.content[0].text}

# Usage
answers = visual_qa("scene.jpg", [
    "How many people are in the image?",
    "What time of day does it appear to be?",
    "What is the main activity happening?"
])
```

### Image Comparison

```python
def compare_images(image_paths: list[str], comparison_type: str = "differences") -> dict:
    """Compare multiple images."""

    images_content = []
    for path in image_paths:
        data, media_type = encode_image(path)
        images_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": data
            }
        })

    comparison_prompts = {
        "differences": "Compare these images and list all differences you can find.",
        "similarities": "Compare these images and describe what they have in common.",
        "progression": "These images show a progression. Describe how things change from one to the next.",
        "quality": "Compare the quality of these images (resolution, clarity, composition, lighting).",
        "content": "Compare the content of these images in detail."
    }

    images_content.append({
        "type": "text",
        "text": comparison_prompts.get(comparison_type, comparison_prompts["differences"])
    })

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": images_content
            }
        ]
    )

    return {"comparison": message.content[0].text}
```

### Code/Diagram Analysis

```python
def analyze_code_screenshot(image_path: str) -> dict:
    """Analyze a code screenshot."""

    image_data, media_type = encode_image(image_path)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """Analyze this code screenshot:

1. Identify the programming language
2. Extract the code as text
3. Explain what the code does
4. Identify any potential issues or improvements
5. Note any visible errors or warnings

Return as JSON:
{
    "language": "...",
    "code": "extracted code",
    "explanation": "...",
    "issues": [...],
    "suggestions": [...]
}"""
                    }
                ]
            }
        ]
    )

    import json
    try:
        return json.loads(message.content[0].text)
    except:
        return {"analysis": message.content[0].text}


def analyze_diagram(image_path: str, diagram_type: str = "auto") -> dict:
    """Analyze a diagram or flowchart."""

    image_data, media_type = encode_image(image_path)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """Analyze this diagram:

1. Identify the diagram type (flowchart, UML, architecture, etc.)
2. List all elements/nodes
3. Describe the relationships/connections
4. Explain the overall purpose/flow
5. Generate equivalent Mermaid or PlantUML code if possible

Return as JSON:
{
    "type": "diagram type",
    "elements": [...],
    "relationships": [...],
    "explanation": "...",
    "mermaid_code": "..."
}"""
                    }
                ]
            }
        ]
    )

    import json
    try:
        return json.loads(message.content[0].text)
    except:
        return {"analysis": message.content[0].text}
```

## Multi-Turn Vision Conversations

```python
class VisionConversation:
    """Maintain a conversation about images."""

    def __init__(self, model="claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.messages = []
        self.images = {}  # Store images by reference

    def add_image(self, image_path: str, name: str = None) -> str:
        """Add an image to the conversation."""
        name = name or f"image_{len(self.images) + 1}"
        data, media_type = encode_image(image_path)
        self.images[name] = {
            "data": data,
            "media_type": media_type
        }
        return name

    def ask(self, question: str, image_names: list[str] = None) -> str:
        """Ask a question, optionally including images."""

        content = []

        # Add specified images
        if image_names:
            for name in image_names:
                if name in self.images:
                    img = self.images[name]
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": img["media_type"],
                            "data": img["data"]
                        }
                    })

        content.append({"type": "text", "text": question})

        self.messages.append({"role": "user", "content": content})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=self.messages
        )

        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

# Usage
conv = VisionConversation()
conv.add_image("room.jpg", "living_room")

print(conv.ask("What's in this image?", ["living_room"]))
print(conv.ask("What style would you call this decor?"))
print(conv.ask("What improvements would you suggest?"))
```

## Vision with Tools

```python
# Combine vision with tool use
def analyze_product_image(image_path: str):
    """Analyze a product image and look up pricing."""

    image_data, media_type = encode_image(image_path)

    tools = [
        {
            "name": "lookup_product",
            "description": "Look up product information by name or barcode",
            "input_schema": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "barcode": {"type": "string"}
                }
            }
        },
        {
            "name": "compare_prices",
            "description": "Compare prices across retailers",
            "input_schema": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"}
                },
                "required": ["product_name"]
            }
        }
    ]

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": "Identify this product and find its current prices."
                    }
                ]
            }
        ]
    )

    # Handle tool calls as shown in Chapter 3
    return message
```

## Best Practices

### Image Quality

```python
# 1. Use appropriate resolution
# - Higher resolution for text/details
# - Lower resolution acceptable for general scenes

# 2. Ensure good lighting and contrast
# - Avoid very dark or overexposed images
# - Ensure text is readable

# 3. Optimize file size
# - Compress images appropriately
# - Use JPEG for photos, PNG for screenshots

def prepare_image_for_api(image_path: str, purpose: str = "general") -> tuple[str, str]:
    """Prepare image based on use case."""

    settings = {
        "general": {"max_size": 1024, "quality": 85},
        "text_extraction": {"max_size": 2048, "quality": 95},
        "detailed_analysis": {"max_size": 1568, "quality": 90},
        "quick_classification": {"max_size": 512, "quality": 80}
    }

    config = settings.get(purpose, settings["general"])
    return optimize_image(image_path, **config)
```

### Prompt Engineering for Vision

```python
# Be specific about what you want
# Bad: "What's this?"
# Good: "Identify all products visible in this image with their brand names and approximate quantities."

# Provide context when helpful
# "This is a medical X-ray. Identify any abnormalities visible."

# Structure expected output
# "List all items in JSON format with fields: name, color, position"

# Ask for confidence levels
# "For each identified object, rate your confidence (high/medium/low)"
```

### Cost Optimization

```python
def estimate_vision_cost(image_path: str, model: str = "claude-sonnet-4-20250514") -> float:
    """Estimate token cost for an image."""

    from PIL import Image

    with Image.open(image_path) as img:
        width, height = img.size

    # Approximate token calculation
    # Images are roughly 1 token per 750 pixels
    pixels = width * height
    image_tokens = pixels // 750

    # Pricing (check current rates)
    rates = {
        "claude-opus-4-20250514": 15.0,
        "claude-sonnet-4-20250514": 3.0,
        "claude-3-5-haiku-20241022": 0.25
    }

    rate = rates.get(model, 3.0)
    cost = (image_tokens / 1_000_000) * rate

    return cost

# Check cost before sending
cost = estimate_vision_cost("large_image.jpg")
print(f"Estimated input cost: ${cost:.4f}")
```

## Summary

In this chapter, you've learned:

- **Sending Images**: Base64 encoding and URL-based image input
- **Format Support**: Supported formats, limits, and optimization
- **Use Cases**: Description, OCR, document analysis, visual Q&A
- **Comparisons**: Analyzing multiple images together
- **Code Analysis**: Processing screenshots and diagrams
- **Multi-Turn**: Maintaining vision conversations
- **Tool Integration**: Combining vision with function calling
- **Best Practices**: Quality, prompting, and cost optimization

## Key Takeaways

1. **Optimize Images**: Resize and compress for better performance
2. **Be Specific**: Clear prompts yield better visual analysis
3. **Multiple Images**: Claude can compare and analyze sets of images
4. **Combine Capabilities**: Vision works well with tools and conversation
5. **Consider Costs**: Image tokens add up, optimize when possible

## Next Steps

Now that you can work with images, let's explore Streaming in Chapter 5 for real-time response delivery.

---

**Ready for Chapter 5?** [Streaming](05-streaming.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
