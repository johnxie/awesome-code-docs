# Discoverability Assets

This directory contains generated assets used to improve organic discoverability for the repository and tutorial catalog.

## Files

- `tutorial-index.json`: machine-readable index of all tutorial tracks with titles, summaries, keywords, and canonical repo URLs.
- `tutorial-directory.md`: human-readable A-Z tutorial listing with one-line summaries.
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
- `llms.txt`
- `llms-full.txt`

These files should be committed whenever the tutorial catalog changes.

## Repository Metadata Sync

To reapply canonical repository metadata (description, homepage, topics):

```bash
bash scripts/sync_repo_metadata.sh
```
