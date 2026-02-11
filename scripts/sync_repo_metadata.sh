#!/usr/bin/env bash
set -euo pipefail

REPO="johnxie/awesome-code-docs"
DESCRIPTION="World-class deep-dive tutorials for open-source AI agents, vibe coding tools, LLM frameworks, and production systems."
HOMEPAGE="https://github.com/johnxie/awesome-code-docs#-tutorial-catalog"

echo "Updating repository description/homepage for ${REPO}"
gh api "repos/${REPO}" \
  -X PATCH \
  -f description="${DESCRIPTION}" \
  -f homepage="${HOMEPAGE}" >/dev/null

echo "Updating repository topics for ${REPO}"
gh api "repos/${REPO}/topics" \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  --raw-field "names[]=ai-agents" \
  --raw-field "names[]=awesome-list" \
  --raw-field "names[]=awesome-lists" \
  --raw-field "names[]=llm" \
  --raw-field "names[]=ai-coding-assistant" \
  --raw-field "names[]=bolt-diy" \
  --raw-field "names[]=cline" \
  --raw-field "names[]=codebase-analysis" \
  --raw-field "names[]=developer-tools" \
  --raw-field "names[]=documentation" \
  --raw-field "names[]=langchain" \
  --raw-field "names[]=machine-learning" \
  --raw-field "names[]=mcp" \
  --raw-field "names[]=open-source" \
  --raw-field "names[]=openhands" \
  --raw-field "names[]=rag" \
  --raw-field "names[]=roo-code" \
  --raw-field "names[]=technical-writing" \
  --raw-field "names[]=tutorials" \
  --raw-field "names[]=vibe-coding" >/dev/null

echo "Done. Current metadata:"
gh repo view "${REPO}" --json description,homepageUrl,repositoryTopics
