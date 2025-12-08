---
layout: default
title: "Chapter 2: Event Tracking & Properties"
parent: "PostHog Tutorial"
nav_order: 2
---

# Chapter 2: Event Tracking & Properties

Implement reliable event tracking with clean schemas and useful properties.

## Objectives
- Install PostHog SDK and send events
- Define event/property conventions
- Identify users and manage distinct IDs
- Validate tracking in the PostHog UI

## Quick Start (Web)
```html
<script>
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(o=t.createElement("script"),o.type="text/javascript",o.async=!0,o.src="https://cdn.posthog.com/posthog.js",n=t.getElementsByTagName("script")[0],n.parentNode.insertBefore(o,n),e._i.push([i,s,a]),p="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags reloadFeatureFlags".split(" ");for(r=0;r<p.length;r++)g(e,p[r]);e.__SV=1.2},e.init("YOUR_API_KEY",{api_host:"https://app.posthog.com"}))}(document,window.posthog||[]);

  posthog.capture('pageview', { path: window.location.pathname });
</script>
```

## Identify Users
```javascript
posthog.identify('user_123', { plan: 'pro', email: 'alice@example.com' })
```

## Event Convention Tips
- Name events as actions: `signed_up`, `added_to_cart`, `upgraded_plan`
- Use consistent casing (snake_case or lowerCamel)
- Add properties that explain *why* an action occurred

## Property Examples
- `plan`, `billing_cycle`, `source` (utm_source), `feature_flag`, `error_code`
- Avoid high-cardinality free text; bucket where possible

## Validate Events
- Check Live Events in PostHog UI
- Use `ph_debug=1` query param in dev to inspect
- Ensure distinct_id is stable per user

## Troubleshooting
- Events missing: verify API key and host; check ad-blockers
- Duplicates: ensure only one SDK instance; debounce rapid events
- Wrong user: call `identify` after login, `reset` on logout

## Performance Notes
- Batch events (SDK does this automatically)
- Avoid large payloads; keep properties small

## Security Notes
- Do not send PII in event names; limit sensitive properties
- Use EU/US data residency as required

## Next Steps
Proceed to Chapter 3 to analyze users, funnels, and retention.
