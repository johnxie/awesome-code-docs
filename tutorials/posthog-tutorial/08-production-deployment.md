---
layout: default
title: "Chapter 8: Production Deployment"
parent: "PostHog Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

Run PostHog at scale with reliability, compliance, and cost controls.

## Objectives
- Choose hosting model (Cloud vs Self-hosted)
- Secure ingestion and data access
- Monitor performance and costs
- Plan backups and retention

## Hosting Choices
- **Cloud**: fastest setup, managed infra
- **Self-hosted**: full data control; deploy via Helm/Docker Compose

## Ingestion Hardening
- Enforce HTTPS; restrict allowed origins
- Rotate API keys; use project-specific tokens
- Throttle abusive clients; enable WAF when possible

## Monitoring
- Track ingestion latency, 5xx rates, queue depth
- Dashboard key metrics: DAU/WAU/MAU, events/min, recording volume
- Alerts for spikes in error rates or drop in ingestion

## Storage & Retention
- Set retention by event type if needed
- Compress and age out old session recordings
- Plan storage growth; monitor S3/object-store costs

## Backups & DR
- Regular DB backups; test restore flows
- Snapshot object storage for recordings (if self-hosted)
- Document RPO/RTO targets

## Compliance & Privacy
- Honor user deletion/export requests
- Mask PII in events and recordings
- Choose region-appropriate hosting (EU/US)

## Go-Live Checklist
- [ ] HTTPS/WAF configured
- [ ] API keys rotated and least-privilege
- [ ] Monitoring + alerts live
- [ ] Backups tested
- [ ] Retention and privacy policies set

## Next Steps
Continue iterating on experiments and dashboards; integrate with warehouse for advanced modeling.
