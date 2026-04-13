---
layout: default
title: "Chapter 3: Computer Use Deep-Dive"
nav_order: 3
parent: Anthropic Quickstarts Tutorial
format_version: v2
source_repo: https://github.com/anthropics/anthropic-quickstarts
---

# Chapter 3: Computer Use Deep-Dive

## What Problem Does This Solve?

Computer use is the most complex Claude capability to implement correctly. The challenge is not just calling an API — it is building a feedback loop where Claude sees the screen, takes an action, observes the result, and continues until a goal is achieved. This chapter explains exactly how `computer-use-demo` implements that loop: the three tools Claude uses, how screenshots are captured and sent, how coordinates are scaled to match API resolution expectations, and how the sampling loop terminates.

## How It Works Under the Hood

Claude does not control the computer directly. Instead, it issues structured action requests that the local Python code executes on its behalf. The cycle is:

```mermaid
sequenceDiagram
    participant Claude
    participant Loop as sampling_loop()
    participant Computer as ComputerTool
    participant Bash as BashTool
    participant Edit as EditTool
    participant Display as Xdotool + gnome-screenshot

    Claude->>Loop: tool_use: computer(screenshot)
    Loop->>Computer: __call__(action="screenshot")
    Computer->>Display: gnome-screenshot -f /tmp/screenshot.png
    Display-->>Computer: PNG file
    Computer-->>Loop: ToolResult(base64_image=...)
    Loop->>Claude: tool_result with base64 PNG

    Claude->>Loop: tool_use: computer(left_click, coordinate=[512, 300])
    Loop->>Computer: __call__(action="left_click", coordinate=[512,300])
    Computer->>Display: xdotool mousemove --sync 384 225 click 1
    Display-->>Computer: exit code 0
    Computer-->>Loop: ToolResult(output="")
    Loop->>Claude: tool_result

    Claude->>Loop: tool_use: bash(command="ls /tmp")
    Loop->>Bash: __call__(command="ls /tmp")
    Bash-->>Loop: ToolResult(output="screenshot.png\n")
    Loop->>Claude: tool_result
```

## The Three Computer Use Tools

### ComputerTool

Defined in `computer_use_demo/tools/computer.py`. There are three versioned classes:

- `ComputerTool20241022` — original set of actions
- `ComputerTool20250124` — adds scroll, hold_key, wait, triple_click, left_mouse_down/up
- `ComputerTool20251124` — adds zoom capability

The Streamlit sidebar exposes a "Tool version" selector to choose between them.

**Action types (ComputerTool20250124):**

| Category | Actions |
|:---------|:--------|
| Mouse | `left_click`, `right_click`, `middle_click`, `double_click`, `mouse_move`, `left_click_drag`, `left_mouse_down`, `left_mouse_up`, `triple_click` |
| Keyboard | `key`, `type`, `hold_key` |
| Scroll | `scroll` (with `coordinate`, `direction`, `amount`) |
| Screen | `screenshot`, `cursor_position` |
| Timing | `wait` |

**Coordinate scaling** is the most subtle part. The API expects coordinates relative to a fixed target resolution (1024×768 for XGA, 1280×800 for WXGA, 1366×768 for FWXGA), but the actual display may be a different size. The tool scales every coordinate before calling xdotool:

```python
# From computer_use_demo/tools/computer.py (simplified)
def scale_coordinates(self, source: ScalingSource, x: int, y: int):
    """Convert coordinates between API space and screen space."""
    if not self._scaling_enabled:
        return x, y
    ratio = self.width / self.height
    # Select target resolution that matches display aspect ratio
    target_dimension = None
    for dimension in MAX_SCALING_TARGETS.values():
        if abs(dimension["width"] / dimension["height"] - ratio) < 0.02:
            if dimension["width"] < self.width:
                target_dimension = dimension
    if target_dimension is None:
        return x, y
    x_scale = self.width / target_dimension["width"]
    y_scale = self.height / target_dimension["height"]
    if source == ScalingSource.API:
        # Claude gave us API coords → convert to screen coords
        return round(x * x_scale), round(y * y_scale)
    else:
        # We have screen coords → convert to API coords for display
        return round(x / x_scale), round(y / y_scale)
```

The recommendation in the README to use XGA resolution (1024×768) in your Docker container is directly related to this: it eliminates the need for scaling by making screen coordinates and API coordinates identical.

### BashTool

Defined in `computer_use_demo/tools/bash.py` as `BashTool20250124`. Maintains a **persistent subprocess** across all tool calls in a session, so environment variables and working directory state persist between commands.

The core challenge: how do you know when a command has finished in a persistent shell? You cannot wait for EOF because the process keeps running. The solution is a **sentinel pattern**:

```python
# From computer_use_demo/tools/bash.py (simplified)
SENTINEL = "<<exit>>"

async def run(self, command: str) -> tuple[str, str]:
    """Run a command and return (stdout, stderr)."""
    # Append sentinel echo so we know when output ends
    self._process.stdin.write(
        command.encode() + f"; echo '{SENTINEL}'\n".encode()
    )
    await self._process.stdin.drain()

    # Read until we see the sentinel
    output = ""
    async for line in self._process.stdout:
        line_str = line.decode("utf-8", errors="replace")
        if SENTINEL in line_str:
            break
        output += line_str

    return output, ""
```

The tool also has a `restart()` method for recovery from timeouts or crashes, and enforces a 120-second timeout per command.

### EditTool

Defined as `EditTool20250728` in `computer_use_demo/tools/edit.py`. API type: `text_editor_20250728`. Supports four commands:

| Command | Description |
|:--------|:------------|
| `view` | Display file contents (with optional line range) or list directory (2 levels deep) |
| `create` | Create a new file with given content |
| `str_replace` | Replace exactly one occurrence of `old_str` with `new_str` |
| `insert` | Insert `new_str` after a specified `insert_line` number |

The `str_replace` command enforces uniqueness: if `old_str` appears zero or more than one time, the tool returns an error. This prevents accidental partial edits.

Output snippets show 4 lines of context around every edit, so Claude can verify its change landed in the right place without taking a full screenshot.

## The Sampling Loop in Detail

`sampling_loop()` in `computer_use_demo/loop.py` is the engine of the entire demo. Simplified structure:

```python
async def sampling_loop(
    *,
    model: str,
    provider: APIProvider,
    system_prompt_suffix: str,
    messages: list[BetaMessageParam],
    output_callback: Callable,
    tool_output_callback: Callable,
    api_response_callback: Callable,
    api_key: str,
    only_n_most_recent_images: int | None = None,
    max_tokens: int = 4096,
    thinking: BetaThinkingConfigParam | None = None,
    tool_version: ToolVersion,
) -> list[BetaMessageParam]:

    tool_collection = ToolCollection(
        ComputerTool(display_width_px, display_height_px, DISPLAY_NUM),
        BashTool(),
        EditTool(),
    )

    system = BetaTextBlockParam(
        type="text",
        text=f"{SYSTEM_PROMPT}{system_prompt_suffix}",
    )

    while True:
        # Optionally trim old screenshots to manage context window
        if only_n_most_recent_images:
            _maybe_filter_to_n_most_recent_images(messages, only_n_most_recent_images)

        # Optionally inject prompt cache breakpoints
        if betas:
            _inject_prompt_caching(messages)

        # Call Claude
        response = client.beta.messages.create(
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            system=[system],
            tools=tool_collection.to_params(),
            betas=betas,
        )

        # Notify UI callback
        await api_response_callback(response)

        # Convert response to message and append
        response_params = _response_to_params(response)
        messages.append({"role": "assistant", "content": response_params})

        # Find tool use blocks
        tool_use_blocks = [b for b in response_params if b["type"] == "tool_use"]
        if not tool_use_blocks:
            return messages   # ← Loop termination: no more tool calls

        # Execute each tool
        tool_result_content = []
        for block in tool_use_blocks:
            result = await tool_collection.run(
                name=block["name"],
                tool_input=block["input"],
            )
            tool_result_content.append(
                _make_api_tool_result(result, block["id"])
            )
            await tool_output_callback(result, block["id"])

        # Append tool results and loop
        messages.append({"role": "user", "content": tool_result_content})
```

## Security Considerations

The README is explicit about risks: computer use is a beta feature with distinct attack surfaces.

**Key precautions the quickstart documents:**

1. Run Claude in an isolated VM with minimal permissions — the Docker container enforces this
2. Avoid exposing sensitive credentials or accounts within the VM
3. Restrict internet access to an approved domain allowlist when possible
4. Require human confirmation for irreversible actions
5. Be alert to prompt injection through webpage content (an adversarial page could instruct Claude to take unintended actions)

The `SYSTEM_PROMPT` in `loop.py` explicitly warns Claude about these risks and instructs it to prefer conservative actions when uncertain.

## Resolution and Performance Tips

- **Use XGA (1024×768)**: Recommended in the README. Eliminates coordinate scaling entirely, which reduces errors from rounding.
- **Image truncation**: The `only_n_most_recent_images` parameter (configurable in the sidebar) drops older screenshots from the context window. Computer use generates many screenshots; without truncation, context costs grow rapidly.
- **Model selection**: The flagship demos use `claude-opus-4-20250514`. For exploratory or budget use, switch to `claude-haiku-4-20250514` in the sidebar — it is significantly faster and cheaper.

## Summary

The computer use demo implements a tight feedback loop: Claude takes a screenshot, issues an action, sees the result, and continues. Three tools — ComputerTool (screenshot + input), BashTool (persistent shell with sentinel detection), and EditTool (file editing) — cover all the capabilities a desktop agent needs. Coordinate scaling handles resolution mismatches between the API and actual display. The sampling loop terminates cleanly when Claude returns a message with no tool use blocks.

Next: [Chapter 4: Tool Use Patterns](04-integration-platforms.md)

---

- [Tutorial Index](README.md)
- [Previous Chapter: Chapter 2: Quickstart Architecture](02-skill-categories.md)
- [Next Chapter: Chapter 4: Tool Use Patterns](04-integration-platforms.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
