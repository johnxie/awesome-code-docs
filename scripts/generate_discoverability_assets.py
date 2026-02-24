#!/usr/bin/env python3
"""Generate discoverability assets for SEO and LLM retrieval.

Outputs:
- discoverability/tutorial-index.json
- discoverability/tutorial-directory.md
- llms.txt
- llms-full.txt
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

TUTORIALS_DIR = "tutorials"
COMMON_STOPWORDS = {
    "a",
    "an",
    "and",
    "the",
    "of",
    "for",
    "to",
    "in",
    "on",
    "with",
    "by",
    "from",
    "how",
    "your",
    "you",
    "guide",
    "tutorial",
    "using",
    "use",
    "learn",
    "build",
    "guide",
    "deep",
    "dive",
    "covering",
    "production",
    "platform",
    "system",
    "systems",
    "project",
    "practical",
    "across",
    "into",
    "from",
    "through",
    "about",
    "this",
    "that",
    "their",
    "its",
    "our",
    "your",
    "these",
    "those",
    "including",
}

SUMMARY_NOISE_PATTERNS = (
    "important notice",
    "project:",
    "latest release",
    "what's new",
    "deprecated",
    "sunset",
)

CLUSTER_RULES: dict[str, tuple[str, ...]] = {
    "ai-coding-agents": (
        "codex",
        "cline",
        "roo",
        "openhands",
        "sweep",
        "continue",
        "aider",
        "agent",
        "coding",
        "claude code",
        "gemini cli",
    ),
    "mcp-ecosystem": (
        "mcp",
        "model context protocol",
        "fastmcp",
        "inspector",
        "registry",
        "server",
        "tool",
    ),
    "rag-and-retrieval": (
        "rag",
        "retrieval",
        "vector",
        "embedding",
        "llamaindex",
        "haystack",
        "chroma",
        "lancedb",
        "mem0",
    ),
    "llm-infra-serving": (
        "ollama",
        "vllm",
        "llama.cpp",
        "llama-cpp",
        "serving",
        "inference",
        "litellm",
        "localai",
    ),
    "ai-app-frameworks": (
        "next.js",
        "react",
        "copilotkit",
        "vercel ai",
        "flowise",
        "dify",
        "chat",
        "ui",
    ),
    "taskade-ecosystem": (
        "taskade",
        "genesis",
        "workspace dna",
        "living dna",
        "taskade mcp",
        "taskade ai",
        "taskade automations",
    ),
    "data-and-storage": (
        "database",
        "postgres",
        "clickhouse",
        "supabase",
        "meilisearch",
        "knowledge",
        "storage",
    ),
    "systems-and-internals": (
        "internals",
        "fiber",
        "operators",
        "runtime",
        "architecture",
        "protocol",
        "planner",
    ),
}

QUERY_HUBS: tuple[dict[str, object], ...] = (
    {
        "id": "open-source-coding-agents",
        "title": "Open-Source Coding Agents",
        "cluster": "ai-coding-agents",
        "intents": ("agentic-coding", "production-operations"),
        "must_have_terms": (),
        "prefer_slugs": (
            "cline-tutorial",
            "roo-code-tutorial",
            "opencode-tutorial",
            "codex-cli-tutorial",
            "continue-tutorial",
            "openhands-tutorial",
            "sweep-tutorial",
            "tabby-tutorial",
            "stagewise-tutorial",
            "daytona-tutorial",
        ),
        "queries": (
            "best open-source coding agent",
            "open-source ai coding assistant",
            "terminal coding agent workflow",
        ),
        "why": "High-commercial-intent comparison and adoption query family.",
    },
    {
        "id": "mcp-servers-and-sdks",
        "title": "MCP Servers and SDKs",
        "cluster": "mcp-ecosystem",
        "intents": ("mcp-integration", "production-operations"),
        "must_have_terms": ("mcp", "model context protocol"),
        "prefer_slugs": (
            "mcp-python-sdk-tutorial",
            "fastmcp-tutorial",
            "mcp-servers-tutorial",
            "mcp-typescript-sdk-tutorial",
            "mcp-go-sdk-tutorial",
            "mcp-rust-sdk-tutorial",
            "mcp-java-sdk-tutorial",
            "mcp-csharp-sdk-tutorial",
            "mcp-registry-tutorial",
            "mcp-inspector-tutorial",
        ),
        "queries": (
            "best mcp servers",
            "how to build mcp server",
            "model context protocol sdk tutorial",
        ),
        "why": "Fast-growing protocol ecosystem with implementation and operations demand.",
    },
    {
        "id": "rag-and-retrieval-systems",
        "title": "RAG and Retrieval Systems",
        "cluster": "rag-and-retrieval",
        "intents": ("rag-implementation", "production-operations"),
        "must_have_terms": ("rag", "retrieval", "vector", "embedding"),
        "prefer_slugs": (
            "llamaindex-tutorial",
            "haystack-tutorial",
            "ragflow-tutorial",
            "chroma-tutorial",
            "lancedb-tutorial",
            "quivr-tutorial",
            "mem0-tutorial",
        ),
        "queries": (
            "how to build rag pipeline",
            "rag framework comparison",
            "vector database tutorial for ai",
        ),
        "why": "Common production AI workload with clear architecture and tooling intent.",
    },
    {
        "id": "llm-infrastructure-serving",
        "title": "LLM Infrastructure and Serving",
        "cluster": "llm-infra-serving",
        "intents": ("production-operations",),
        "must_have_terms": ("inference", "serv", "ollama", "vllm", "litellm", "llama.cpp", "localai"),
        "prefer_slugs": (
            "ollama-tutorial",
            "vllm-tutorial",
            "litellm-tutorial",
            "llama-cpp-tutorial",
            "localai-tutorial",
            "bentoml-tutorial",
        ),
        "queries": (
            "serve llm in production",
            "vllm vs ollama vs litellm",
            "self-hosted llm infrastructure",
        ),
        "why": "Operations-heavy cluster where searchers are close to deployment decisions.",
    },
    {
        "id": "ai-app-frameworks",
        "title": "AI App Frameworks and Product Stacks",
        "cluster": "ai-app-frameworks",
        "intents": ("beginner-onboarding", "production-operations"),
        "must_have_terms": ("app", "framework", "workflow", "chat", "next.js", "react", "copilot", "dify", "flowise", "vercel ai"),
        "prefer_slugs": (
            "vercel-ai-tutorial",
            "copilotkit-tutorial",
            "lobechat-ai-platform",
            "flowise-llm-orchestration",
            "dify-platform-deep-dive",
            "open-webui-tutorial",
            "chatbox-tutorial",
        ),
        "queries": (
            "build ai app with nextjs",
            "open-source ai app framework",
            "ai workflow builder tutorial",
        ),
        "why": "Application-layer queries for teams choosing implementation stack.",
    },
    {
        "id": "taskade-ai-genesis-workflows",
        "title": "Taskade AI, Genesis, and MCP Workflows",
        "cluster": "taskade-ecosystem",
        "intents": ("beginner-onboarding", "mcp-integration", "production-operations"),
        "must_have_terms": ("taskade", "genesis"),
        "prefer_slugs": (
            "taskade-tutorial",
            "taskade-docs-tutorial",
            "taskade-mcp-tutorial",
            "taskade-awesome-vibe-coding-tutorial",
        ),
        "queries": (
            "taskade ai tutorial",
            "taskade genesis app builder",
            "taskade docs",
            "taskade api docs",
            "taskade help center",
            "taskade workspace dna",
            "taskade mcp setup",
            "taskade automation agents",
        ),
        "why": "High-intent Taskade ecosystem journey spanning workspace apps, agents, automations, and MCP integration.",
    },
)


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    parts = text.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[1]
    return text


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def first_quote(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("> "):
            return line[2:].strip()
    return ""


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_summary_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\[\!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", " ", cleaned)
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", cleaned)
    cleaned = cleaned.replace("`", "")
    cleaned = cleaned.replace("*", "")
    cleaned = normalize_whitespace(cleaned)

    if cleaned.lower().startswith("project:"):
        cleaned = cleaned.split(":", 1)[1].strip()
    cleaned = cleaned.rstrip(":").strip()

    return cleaned


def is_noise_summary(text: str) -> bool:
    lowered = clean_summary_text(text).lower()
    if not lowered:
        return True
    if lowered.startswith("http"):
        return True
    if "img src=" in lowered:
        return True
    if lowered.startswith("[!"):
        return True
    return any(pattern in lowered for pattern in SUMMARY_NOISE_PATTERNS)


def first_paragraph(markdown: str) -> str:
    in_fence = False
    paragraph_lines: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            if paragraph_lines:
                break
            continue
        if stripped.startswith(("#", ">", "-", "|", "```")):
            if paragraph_lines:
                break
            continue
        if stripped.startswith("!"):
            continue
        if "<img" in stripped.lower() or stripped.startswith("<"):
            continue
        paragraph_lines.append(stripped)

    return normalize_whitespace(" ".join(paragraph_lines))


def best_summary(markdown: str) -> str:
    quote = clean_summary_text(normalize_whitespace(first_quote(markdown)))
    if quote and not is_noise_summary(quote):
        return quote

    paragraph = clean_summary_text(first_paragraph(markdown))
    if paragraph and not is_noise_summary(paragraph):
        return paragraph

    if quote:
        return quote
    return paragraph


def extract_keywords(slug: str, title: str, summary: str) -> list[str]:
    blob = f"{slug} {title} {summary}".lower()
    tokens = re.findall(r"[a-z0-9]+", blob)

    keywords: list[str] = []
    seen: set[str] = set()
    for t in tokens:
        if len(t) < 3:
            continue
        if t.isdigit():
            continue
        if t in COMMON_STOPWORDS:
            continue
        if t.startswith(("http", "www")):
            continue
        if t in {"github", "com", "johnxie", "main", "tree", "blob", "docs", "repo"}:
            continue
        if t in seen:
            continue
        seen.add(t)
        keywords.append(t)

    # keep compact and deterministic
    return keywords[:18]


def classify_cluster(slug: str, title: str, summary: str, keywords: list[str]) -> str:
    text = " ".join([slug.lower(), title.lower(), summary.lower(), " ".join(keywords)])

    if "taskade" in text or "genesis" in text:
        return "taskade-ecosystem"

    best_cluster = "general-software"
    best_score = 0
    for cluster, terms in CLUSTER_RULES.items():
        score = sum(1 for term in terms if term in text)
        if score > best_score:
            best_score = score
            best_cluster = cluster
    return best_cluster


def infer_intent_signals(title: str, summary: str, cluster: str) -> list[str]:
    text = f"{title.lower()} {summary.lower()}"
    intents: list[str] = []

    if any(token in text for token in ("getting started", "first", "intro", "beginner")):
        intents.append("beginner-onboarding")
    if any(token in text for token in ("production", "deploy", "operations", "scaling", "governance")):
        intents.append("production-operations")
    if any(token in text for token in ("architecture", "internals", "deep dive", "design")):
        intents.append("architecture-deep-dive")
    if any(token in text for token in ("compare", "selection", "catalog", "awesome")):
        intents.append("tool-selection")
    if cluster == "mcp-ecosystem":
        intents.append("mcp-integration")
    if cluster == "ai-coding-agents":
        intents.append("agentic-coding")
    if cluster == "rag-and-retrieval":
        intents.append("rag-implementation")

    if not intents:
        intents.append("general-learning")
    return intents[:5]


def tutorial_dirs(root: Path) -> Iterable[Path]:
    tutorials_root = root / TUTORIALS_DIR
    for path in sorted([p for p in tutorials_root.iterdir() if p.is_dir()], key=lambda p: p.name):
        if (path / "index.md").is_file():
            yield path


def build_records(root: Path) -> list[dict]:
    records: list[dict] = []

    for tdir in tutorial_dirs(root):
        index_path = tdir / "index.md"
        raw = index_path.read_text(encoding="utf-8", errors="ignore")
        body = strip_frontmatter(raw)

        title = first_heading(body) or tdir.name.replace("-", " ").title()
        summary = best_summary(body)
        if not summary:
            summary = f"Deep technical walkthrough of {title}."
        keywords = extract_keywords(tdir.name, title, summary)
        cluster = classify_cluster(tdir.name, title, summary, keywords)
        intent_signals = infer_intent_signals(title, summary, cluster)

        rel_dir = tdir.relative_to(root).as_posix()
        records.append(
            {
                "slug": tdir.name,
                "title": title,
                "summary": summary,
                "path": rel_dir,
                "index_path": f"{rel_dir}/index.md",
                "repo_url": f"https://github.com/johnxie/awesome-code-docs/tree/main/{rel_dir}",
                "file_url": f"https://github.com/johnxie/awesome-code-docs/blob/main/{rel_dir}/index.md",
                "keywords": keywords,
                "cluster": cluster,
                "intent_signals": intent_signals,
            }
        )

    return records


def write_json(output_path: Path, records: list[dict]) -> None:
    payload = {
        "project": "awesome-code-docs",
        "tutorial_count": len(records),
        "tutorials": records,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_llms_txt(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Awesome Code Docs",
        "> Deep-dive tutorials for popular open-source AI, developer-tooling, and data platforms.",
        "",
        "## Start Here",
        "- https://github.com/johnxie/awesome-code-docs",
        "- https://github.com/johnxie/awesome-code-docs/blob/main/README.md",
        "- https://github.com/johnxie/awesome-code-docs/blob/main/CONTRIBUTING.md",
        "- https://github.com/johnxie/awesome-code-docs/tree/main/tutorials",
        "",
        "## Priority Tutorial Clusters",
        "- AI Coding Tools: Cline, Roo Code, bolt.diy, OpenHands, Continue",
        "- Vibe Coding Platforms: Dyad, bolt.diy, VibeSDK, HAPI",
        "- LLM Frameworks: LangChain, LangGraph, LlamaIndex, DSPy",
        "- Infrastructure: Ollama, vLLM, LiteLLM, llama.cpp",
        "",
        "## Tutorial Directory",
    ]

    for record in records:
        lines.append(f"- {record['title']}: {record['repo_url']}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_llms_full_txt(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Awesome Code Docs (Full Tutorial Index)",
        "",
        "Main repository:",
        "- https://github.com/johnxie/awesome-code-docs",
        "",
    ]

    for record in records:
        lines.extend(
            [
                f"## {record['title']}",
                f"- Path: {record['path']}",
                f"- Index: {record['file_url']}",
                f"- Summary: {record['summary'] or 'N/A'}",
                f"- Keywords: {', '.join(record['keywords']) if record['keywords'] else 'N/A'}",
                "",
            ]
        )

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_directory_markdown(output_path: Path, records: list[dict]) -> None:
    lines = [
        "# Tutorial Directory (A-Z)",
        "",
        "This page is auto-generated from the tutorial index and is intended as a fast browse surface for contributors and search crawlers.",
        "",
        f"- Total tutorials: **{len(records)}**",
        "- Source: `scripts/generate_discoverability_assets.py`",
        "",
    ]

    grouped: dict[str, list[dict]] = {}
    for record in records:
        key = record["title"][:1].upper() if record["title"] else "#"
        if not key.isalpha():
            key = "#"
        grouped.setdefault(key, []).append(record)

    for key in sorted(grouped.keys()):
        lines.append(f"## {key}")
        lines.append("")
        for record in grouped[key]:
            summary = record["summary"] or "Deep technical walkthrough."
            lines.append(f"- [{record['title']}]({record['file_url']})")
            lines.append(f"  - {summary}")
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_search_intent_map(output_path: Path, records: list[dict]) -> None:
    grouped: dict[str, list[dict]] = {}
    for record in records:
        grouped.setdefault(record["cluster"], []).append(record)

    lines = [
        "# Search Intent Map",
        "",
        "Auto-generated topical clusters to strengthen internal linking and query-to-tutorial mapping.",
        "",
        f"- Total tutorials: **{len(records)}**",
        f"- Total clusters: **{len(grouped)}**",
        "- Source: `scripts/generate_discoverability_assets.py`",
        "",
    ]

    for cluster in sorted(grouped.keys()):
        rows = sorted(grouped[cluster], key=lambda r: r["title"])
        lines.append(f"## {cluster}")
        lines.append("")
        lines.append(f"- tutorial_count: **{len(rows)}**")
        lines.append("")
        for row in rows[:25]:
            signals = ", ".join(row["intent_signals"])
            lines.append(f"- [{row['title']}]({row['file_url']})")
            lines.append(f"  - intents: {signals}")
        if len(rows) > 25:
            lines.append(f"- ... plus {len(rows) - 25} more tutorials in this cluster")
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_itemlist_schema(output_path: Path, records: list[dict]) -> None:
    payload = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Awesome Code Docs Tutorial Catalog",
        "url": "https://github.com/johnxie/awesome-code-docs",
        "numberOfItems": len(records),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx,
                "name": record["title"],
                "url": record["file_url"],
                "description": record["summary"],
            }
            for idx, record in enumerate(records, start=1)
        ],
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def score_record_for_hub(record: dict, query_terms: tuple[str, ...], intent_preferences: tuple[str, ...]) -> int:
    score = 0
    text = f"{record['title']} {record['summary']}".lower()
    for term in query_terms:
        if term.lower() in text:
            score += 2
    for intent in intent_preferences:
        if intent in record["intent_signals"]:
            score += 2
    if "production-operations" in record["intent_signals"]:
        score += 1
    return score


def select_records_for_hub(records: list[dict], hub: dict[str, object], limit: int = 12) -> list[dict]:
    cluster = str(hub["cluster"])
    query_terms = tuple(str(x) for x in hub["queries"])
    intent_preferences = tuple(str(x) for x in hub["intents"])
    must_have_terms = tuple(str(x).lower() for x in hub.get("must_have_terms", ()))

    filtered = [r for r in records if r["cluster"] == cluster]
    if must_have_terms:
        strict = [
            r
            for r in filtered
            if any(term in f"{r['title']} {r['summary']}".lower() for term in must_have_terms)
        ]
        if strict:
            filtered = strict

    ranked = sorted(
        filtered,
        key=lambda r: (
            -score_record_for_hub(r, query_terms, intent_preferences),
            r["title"].lower(),
        ),
    )

    by_slug = {r["slug"]: r for r in ranked}
    preferred = [str(x) for x in hub.get("prefer_slugs", ())]
    ordered: list[dict] = []
    seen: set[str] = set()

    for slug in preferred:
        if slug in by_slug and slug not in seen:
            ordered.append(by_slug[slug])
            seen.add(slug)

    for row in ranked:
        if row["slug"] in seen:
            continue
        ordered.append(row)
        seen.add(row["slug"])

    return ordered[:limit]


def write_query_hub_markdown(output_path: Path, records: list[dict]) -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = {}
    lines = [
        "# Query Hub",
        "",
        "Auto-generated high-intent query landing surface mapped to the most relevant tutorials.",
        "",
        f"- Total tutorials indexed: **{len(records)}**",
        f"- Query hubs: **{len(QUERY_HUBS)}**",
        "- Source: `scripts/generate_discoverability_assets.py`",
        "",
    ]

    for hub in QUERY_HUBS:
        hub_id = str(hub["id"])
        hub_title = str(hub["title"])
        selected = select_records_for_hub(records, hub)
        coverage[hub_id] = [r["slug"] for r in selected]

        lines.append(f"## {hub_title}")
        lines.append("")
        lines.append(f"- Cluster: `{hub['cluster']}`")
        lines.append(f"- Why this matters: {hub['why']}")
        lines.append("")
        lines.append("Primary search intents:")
        for q in hub["queries"]:
            lines.append(f"- `{q}`")
        lines.append("")

        if selected:
            lines.append("Recommended tutorials:")
            for row in selected:
                lines.append(f"- [{row['title']}]({row['file_url']})")
                lines.append(f"  - {row['summary']}")
        else:
            lines.append("Recommended tutorials:")
            lines.append("- No matching tutorials found for this cluster.")
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return coverage


def write_query_coverage_json(output_path: Path, records: list[dict], coverage: dict[str, list[str]]) -> None:
    by_slug = {r["slug"]: r for r in records}
    hubs = []
    for hub in QUERY_HUBS:
        hub_id = str(hub["id"])
        slugs = coverage.get(hub_id, [])
        hubs.append(
            {
                "id": hub_id,
                "title": hub["title"],
                "cluster": hub["cluster"],
                "queries": list(hub["queries"]),
                "tutorials": [
                    {
                        "slug": slug,
                        "title": by_slug[slug]["title"],
                        "file_url": by_slug[slug]["file_url"],
                        "intent_signals": by_slug[slug]["intent_signals"],
                    }
                    for slug in slugs
                    if slug in by_slug
                ],
            }
        )

    payload = {
        "project": "awesome-code-docs",
        "hub_count": len(hubs),
        "hubs": hubs,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate discoverability assets")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--output-json",
        default="discoverability/tutorial-index.json",
        help="JSON output path",
    )
    parser.add_argument("--llms", default="llms.txt", help="llms.txt output path")
    parser.add_argument("--llms-full", default="llms-full.txt", help="llms-full.txt output path")
    parser.add_argument(
        "--directory-md",
        default="discoverability/tutorial-directory.md",
        help="A-Z markdown directory output path",
    )
    parser.add_argument(
        "--intent-md",
        default="discoverability/search-intent-map.md",
        help="Search intent map markdown output path",
    )
    parser.add_argument(
        "--jsonld",
        default="discoverability/tutorial-itemlist.schema.json",
        help="JSON-LD ItemList output path",
    )
    parser.add_argument(
        "--query-hub-md",
        default="discoverability/query-hub.md",
        help="High-intent query hub markdown output path",
    )
    parser.add_argument(
        "--query-coverage-json",
        default="discoverability/query-coverage.json",
        help="High-intent query coverage JSON output path",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    json_path = (root / args.output_json).resolve()
    llms_path = (root / args.llms).resolve()
    llms_full_path = (root / args.llms_full).resolve()
    directory_md_path = (root / args.directory_md).resolve()
    intent_md_path = (root / args.intent_md).resolve()
    jsonld_path = (root / args.jsonld).resolve()
    query_hub_md_path = (root / args.query_hub_md).resolve()
    query_coverage_json_path = (root / args.query_coverage_json).resolve()

    json_path.parent.mkdir(parents=True, exist_ok=True)
    llms_path.parent.mkdir(parents=True, exist_ok=True)
    llms_full_path.parent.mkdir(parents=True, exist_ok=True)
    directory_md_path.parent.mkdir(parents=True, exist_ok=True)
    intent_md_path.parent.mkdir(parents=True, exist_ok=True)
    jsonld_path.parent.mkdir(parents=True, exist_ok=True)
    query_hub_md_path.parent.mkdir(parents=True, exist_ok=True)
    query_coverage_json_path.parent.mkdir(parents=True, exist_ok=True)

    records = build_records(root)
    write_json(json_path, records)
    write_llms_txt(llms_path, records)
    write_llms_full_txt(llms_full_path, records)
    write_directory_markdown(directory_md_path, records)
    write_search_intent_map(intent_md_path, records)
    write_itemlist_schema(jsonld_path, records)
    coverage = write_query_hub_markdown(query_hub_md_path, records)
    write_query_coverage_json(query_coverage_json_path, records, coverage)

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote llms.txt: {llms_path}")
    print(f"Wrote llms-full.txt: {llms_full_path}")
    print(f"Wrote directory markdown: {directory_md_path}")
    print(f"Wrote search intent map: {intent_md_path}")
    print(f"Wrote JSON-LD item list: {jsonld_path}")
    print(f"Wrote query hub markdown: {query_hub_md_path}")
    print(f"Wrote query coverage JSON: {query_coverage_json_path}")
    print(f"tutorial_count={len(records)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
