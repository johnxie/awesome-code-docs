# Discoverability Assets

This directory contains generated assets used to improve organic discoverability for the repository and tutorial catalog.

## Files

- `tutorial-index.json`: machine-readable index of all tutorial tracks with summaries, keywords, clusters, and intent signals.
- `tutorial-directory.md`: human-readable A-Z tutorial listing with one-line summaries.
- `query-hub.md`: high-intent query landing page mapped to core tutorial tracks.
- `query-coverage.json`: machine-readable mapping of search intents to selected tutorials.
- `search-intent-map.md`: cluster-level map from user intent to tutorial tracks.
- `tutorial-itemlist.schema.json`: JSON-LD `ItemList` representation of the catalog.
- `market-signals.json`: live GitHub signals for tracked competitive ecosystems.
- `trending-vibe-coding.md`: markdown snapshot derived from `market-signals.json`.
- `staleness-report.json`: freshness-marker audit report from `scripts/staleness_audit.py`.
- `release-claims-report.json`: stale release/activity claim report from tutorial indexes.
- `SEO_DISCOVERABILITY_PLAN.md`: SEO backlog, cadence, and measurement framework.
- `REPOSITORY_METADATA.md`: canonical GitHub description/homepage/topics contract.

## Regeneration

Run:

```bash
python3 scripts/generate_discoverability_assets.py
```

The command regenerates:

- `discoverability/tutorial-index.json`
- `discoverability/tutorial-directory.md`
- `discoverability/query-hub.md`
- `discoverability/query-coverage.json`
- `discoverability/search-intent-map.md`
- `discoverability/tutorial-itemlist.schema.json`
- `llms.txt`
- `llms-full.txt`

These files should be committed whenever the tutorial catalog changes.

To refresh live market signals and rewrite the README trending block:

```bash
python3 scripts/refresh_market_signals.py
```

This command regenerates:

- `discoverability/market-signals.json`
- `discoverability/trending-vibe-coding.md`
- `README.md` (trending block only)

To generate a report of stale `latest release` / `recent activity` claims in tutorial indexes:

```bash
python3 scripts/release_claims_audit.py --json-output discoverability/release-claims-report.json
```

## Repository Metadata Sync

To reapply canonical repository metadata (description, homepage, topics):

```bash
bash scripts/sync_repo_metadata.sh
```

## Weekly Automation

- Workflow: `.github/workflows/weekly-refresh.yml`
- Regenerates manifests, discoverability assets, README market signals, and freshness report.
