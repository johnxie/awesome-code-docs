# Documentation Enhancement Plan

## Current State Analysis

Based on CONTENT_GAPS_ANALYSIS.md:
- 201 tutorials total
- 198 with exactly 8 chapters
- 3 with >8 chapters (n8n-mcp, langchain, ag2)
- 0 with 0 chapters
- 0 with partial chapter coverage

## Enhancement Strategy

### Phase 1: High-Traffic Tutorial Regeneration
**Priority**: Top 10 tutorials by stars from `discoverability/tutorial-source-verification.json`

| Tutorial | Stars | Repo | Status |
|----------|-------|------|--------|
| openclaw/openclaw | 341,130 | openclaw/openclaw | Need regeneration |
| facebook/react | 244,271 | facebook/react | Need regeneration |
| n8n-io/n8n | 181,679 | n8n-io/n8n | Need regeneration |
| ollama/ollama | 166,451 | ollama/ollama | Need regeneration |
| huggingface/transformers | 158,545 | huggingface/transformers | Need regeneration |
| langflow-ai/langflow | 146,399 | langflow-ai/langflow | Need regeneration |
| langgenius/dify | 134,981 | langgenius/dify | Need regeneration |
| anomalyco/opencode | 132,650 | anomalyco/opencode | Need regeneration |
| langchain-ai/langchain | 131,599 | langchain-ai/langchain | Need regeneration |
| open-webui/open-webui | 129,246 | open-webui/open-webui | Need regeneration |

### Phase 2: Missing High-Impact Tutorials
**Priority**: Add tutorials for trending OSS projects not yet covered

**Candidates** (check GitHub for stars > 10K):
- Vercel AI SDK (22K+ stars) - Already covered
- Browser Use (85K+ stars) - Already covered  
- Claude Code (84K+ stars) - Already covered
- Model Context Protocol servers (82K+ stars) - Already covered
- Infiniflow RAGFlow (76K+ stars) - Already covered
- vLLM (74K+ stars) - Already covered

**New additions needed**:
- Check GitHub for trending repos in AI/agents space
- Focus on repos with recent activity (pushed_at in last 30 days)
- Target repos with documentation gaps

### Phase 3: Content Gap Resolution
**Priority**: Fill missing code examples and depth

**Issues to fix**:
1. Tutorials with <100 lines in chapters (already addressed in commit 5bda1be)
2. Missing Mermaid diagrams in architecture chapters
3. Inconsistent code example quality across tutorials
4. Missing production deployment examples

### Phase 4: Source Code Extraction Improvements
**Priority**: Enhance the regeneration script

**Improvements needed**:
1. Better file prioritization (focus on core modules)
2. Handle more file types (`.md`, `.json`, `.yaml`, `.toml`)
3. Better abstraction detection for different languages
4. Add test file extraction for usage examples
5. Better Mermaid diagram generation from code structure

## Execution Plan

### Step 1: Regenerate High-Traffic Tutorials
```bash
# Run regeneration on top 10 tutorials
python scripts/regenerate_tutorial_chapters.py \
  --slugs openclaw,facebook-react,n8n,ollama,huggingface-transformers,langflow,dify,opencode,langchain,open-webui
```

### Step 2: Add New Tutorials
1. Identify 5-10 missing high-impact repos
2. Create tutorial directories with proper structure
3. Add to `llms.txt` and `llms-full.txt`
4. Update `discoverability/tutorial-source-verification.json`

### Step 3: Fix Content Gaps
1. Review tutorials with low chapter counts
2. Add missing code examples from source repos
3. Add Mermaid diagrams where missing
4. Ensure consistent production examples

### Step 4: Improve Source Extraction
1. Update `regenerate_tutorial_chapters.py`
2. Add better file filtering logic
3. Enhance abstraction detection
4. Add diagram generation from code structure

### Step 5: Quality Verification
```bash
# Run health checks
python scripts/docs_health.py
```

## Success Metrics

- [ ] All top 10 tutorials have real code examples from source repos
- [ ] 5-10 new high-impact tutorials added
- [ ] 0 tutorials with placeholder content
- [ ] All tutorials pass docs_health.py checks
- [ ] Source extraction script handles 95%+ of file types
