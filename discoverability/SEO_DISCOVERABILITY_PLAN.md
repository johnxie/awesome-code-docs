# SEO and Discoverability Plan

Last updated: auto-updated by workflow refreshes and manual review.

## Objective

Improve discoverability for high-intent queries around open-source coding agents, MCP, RAG systems, and architecture tutorials.

Ranking note: no maintainer can guarantee a permanent #1 Google position. The practical goal is consistent top-tier relevance, high click quality, and compounding authority.

## Core Principles

- people-first content with clear user intent and practical outcomes
- accurate freshness signals (remove stale claims, automate updates)
- strong internal linking across topic clusters and learning paths
- machine-readable assets for search systems and LLM retrieval

## Source Guidance

- Google SEO Starter Guide: <https://developers.google.com/search/docs/fundamentals/seo-starter-guide>
- Helpful, reliable, people-first content: <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- Structured data basics: <https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data>
- Sitemaps and crawl hints: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap>
- GitHub repository topics: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics>

## Active Workstreams

1. README search-intent surface
- keep "Find Tutorials by Goal" current and high-signal
- maintain live market snapshot block from GitHub API data
- ensure new tracks are linked from category hubs and learning paths

2. Discoverability data assets
- maintain `discoverability/tutorial-index.json`
- maintain `discoverability/tutorial-directory.md`
- maintain `discoverability/query-hub.md` + `discoverability/query-coverage.json`
- maintain `discoverability/search-intent-map.md`
- maintain `llms.txt` and `llms-full.txt`

3. Freshness governance
- run `scripts/staleness_audit.py` on high-impact docs surfaces
- remove static date claims where automation is a better fit
- refresh competitive market signals weekly
- publish `release-claims-report.json` so stale snapshot lines are visible and fixable

4. Metadata hygiene
- keep repository description/homepage/topics aligned to scope
- reapply metadata contract using `scripts/sync_repo_metadata.sh`

## Measurement

Track monthly:

- GitHub views and unique visitors
- star/fork growth velocity
- issue and discussion volume from organic discovery
- README to tutorial click patterns (where measurable)

## Cadence

Weekly:

- automated refresh PR for generated discoverability files
- stale-marker audit on core docs surfaces

Monthly:

- review search-intent clusters and internal-link coverage
- prune low-value copy that does not improve learning outcomes

Quarterly:

- retune topic clusters based on ecosystem shifts
- revise metadata topics and README positioning

## Operating Rules

- prefer deterministic generated assets over manual snapshots
- keep PRs focused and auditable
- avoid SEO filler that does not improve user learning quality
