# SEO and Discoverability Plan

Last updated: February 11, 2026

## Goals

- increase organic discovery for "awesome code docs" and high-intent tutorial queries
- improve crawlability and internal link clarity across README, category hubs, and tutorial indexes
- publish machine-readable indices for search systems and LLM retrieval

## Principles (aligned to primary-source guidance)

- people-first, helpful content with clear intent and summaries
- descriptive page titles/headings and visible contextual snippets
- strong internal linking between related content clusters
- crawl-friendly index/sitemap style assets with stable URLs

Reference guidance:

- Google Search Essentials: <https://developers.google.com/search/docs/fundamentals/seo-starter-guide>
- Helpful, reliable, people-first content: <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- Sitemaps and crawl hints: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap>
- GitHub repository topics: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics>

## Priority Backlog

1. README intent optimization
- align top sections with common user intents (learn X, compare Y, build Z)
- keep key repository stats accurate and synchronized
- strengthen anchor text for high-value tutorial clusters

2. Category hub modernization
- replace stale status labels with current catalog counts
- add "best starting points" and cross-links to learning paths
- include trend clusters (vibe coding, MCP, agents, RAG infra)

3. Tutorial index consistency
- ensure each index includes: what it is, current snapshot, chapter map, related tutorials
- prioritize high-traffic tracks for periodic refreshes

4. Machine-readable discoverability
- maintain `discoverability/tutorial-index.json`
- maintain `llms.txt` and `llms-full.txt`
- enforce regeneration in CI

5. Repository metadata hygiene
- keep repository description, homepage, and topics aligned with current scope
- review metadata quarterly as catalog scope evolves

## Measurement Plan

Track monthly:

- repository views and unique visitors (GitHub traffic)
- top external referrers and search terms (where available)
- stars and forks velocity
- issue/discussion volume from organic discovery
- click-through patterns from README to tutorial directories

## Editorial Cadence

Weekly:

- verify top-level stats and latest additions in README
- refresh stale star/release snapshots for top 20 tutorials

Monthly:

- refresh category hub summaries and trend clusters
- run link and discoverability asset validation

Quarterly:

- prune low-value sections
- rebalance learning paths based on current project ecosystem

## Execution Notes

- prefer small, focused PRs so changes are auditable
- keep generated assets deterministic
- avoid adding SEO content that does not improve user learning quality
