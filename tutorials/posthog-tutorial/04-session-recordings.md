---
layout: default
title: "Chapter 4: Session Recordings"
parent: "PostHog Tutorial"
nav_order: 4
---

# Chapter 4: Session Recordings

Capture and analyze user sessions to find UX issues and validate hypotheses.

## Objectives
- Enable session recordings
- Filter recordings by events, users, and issues
- Tag and share insights with the team

## Enable Recordings (Web)
```javascript
posthog.init('YOUR_API_KEY', {
  api_host: 'https://app.posthog.com',
  capture_pageview: true,
  disable_session_recording: false,
})
```

## Filter Useful Recordings
- Filter by rage clicks, dead clicks
- Filter by country/device/browser
- Filter by key events (e.g., `checkout_error`)

## Tag & Share
- Add labels for UX issues (e.g., "form confusion")
- Create highlights and share with stakeholders

## Troubleshooting
- No recordings: confirm session recording enabled; check CSP blocking
- Missing events in playback: ensure network calls not blocked; update SDK
- PII concerns: mask inputs; disable recording on sensitive pages

## Performance Notes
- Respect sampling if traffic is high; start small (10–20%)
- Exclude admin/internal traffic

## Security/Privacy
- Mask sensitive fields; avoid recording password/credit card inputs
- Follow regional privacy laws; update privacy policy

## Next Steps
Chapter 5 introduces feature flags and experiments to run controlled rollouts.
