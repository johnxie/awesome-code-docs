---
layout: default
title: "Chapter 4: Docker Web Mode and CLI Operations"
nav_order: 4
parent: AgenticSeek Tutorial
---


# Chapter 4: Docker Web Mode and CLI Operations

Welcome to **Chapter 4: Docker Web Mode and CLI Operations**. In this part of **AgenticSeek Tutorial: Local-First Autonomous Agent Operations**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter compares the two primary execution surfaces and shows how to operate each reliably.

## Learning Goals

- choose web mode or CLI mode based on workload
- run service startup paths correctly for each mode
- understand `SEARXNG_BASE_URL` differences between host and Docker contexts
- verify startup readiness before issuing expensive tasks

## Web Mode (Default)

Use this when you want browser-based interaction and full Docker orchestration.

```bash
./start_services.sh full
```

Expected behavior:

- backend + frontend + searxng + redis start together
- UI available at `http://localhost:3000`
- first startup may take several minutes

## CLI Mode

Use this when you need terminal-native execution and host-installed dependencies.

```bash
./install.sh
./start_services.sh
uv run python -m ensurepip
uv run cli.py
```

CLI mode requires host-aware values like:

- `SEARXNG_BASE_URL="http://localhost:8080"`

## Mode Selection Heuristics

- use web mode for team demos and visual monitoring
- use CLI mode for terminal automation and fast iteration
- use explicit prompts in both modes to improve routing reliability

## Source References

- [README Start Services and Run](https://github.com/Fosowl/agenticSeek/blob/main/README.md#start-services-and-run)
- [CLI Entrypoint](https://github.com/Fosowl/agenticSeek/blob/main/cli.py)
- [Windows Startup Script](https://github.com/Fosowl/agenticSeek/blob/main/start_services.cmd)

## Summary

You now know how to operate both web and CLI execution modes safely.

Next: [Chapter 5: Tools, Browser Automation, and Workspace Governance](05-tools-browser-automation-and-workspace-governance.md)

## Source Code Walkthrough

### `sources/browser.py`

The `create_driver` function in [`sources/browser.py`](https://github.com/Fosowl/agenticSeek/blob/HEAD/sources/browser.py) handles a key part of this chapter's functionality:

```py
    return driver

def create_driver(headless=False, stealth_mode=True, crx_path="./crx/nopecha.crx", lang="en") -> webdriver.Chrome:
    """Create a Chrome WebDriver with specified options."""
    # Warn if trying to run non-headless in Docker
    if not headless and os.path.exists('/.dockerenv'):
        print("[WARNING] Running non-headless browser in Docker may fail!")
        print("[WARNING] Consider setting headless=True or headless_browser=True in config.ini")
    
    chrome_options = create_chrome_options(headless, stealth_mode, crx_path, lang)
    chromedriver_path = install_chromedriver()
    service = Service(chromedriver_path)
    
    if stealth_mode:
        driver = create_undetected_chromedriver(service, chrome_options)
        user_agent = get_random_user_agent()
        stealth(driver,
            languages=["en-US", "en"],
            vendor=user_agent["vendor"],
            platform="Win64" if "windows" in user_agent["ua"].lower() else "MacIntel" if "mac" in user_agent["ua"].lower() else "Linux x86_64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver
    else:
        return webdriver.Chrome(service=service, options=chrome_options)

class Browser:
    def __init__(self, driver, anticaptcha_manual_install=False):
        """Initialize the browser with optional AntiCaptcha installation."""
        self.js_scripts_folder = "./sources/web_scripts/" if not __name__ == "__main__" else "./web_scripts/"
```

This function is the entry point for browser-based agent operation in Docker and web mode — the `/.dockerenv` detection ensures headless mode is enforced in containers, which is a key operational detail for Docker deployments described in Chapter 4.
