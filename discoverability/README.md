# Discoverability Assets

This directory contains generated assets used to improve organic discoverability for the repository and tutorial catalog.

## Files

- `tutorial-index.json`: machine-readable index of all tutorial tracks with titles, summaries, keywords, and canonical repo URLs.

## Regeneration

Run:

```bash
python3 scripts/generate_discoverability_assets.py
```

The command regenerates:

- `discoverability/tutorial-index.json`
- `llms.txt`
- `llms-full.txt`

These files should be committed whenever the tutorial catalog changes.
