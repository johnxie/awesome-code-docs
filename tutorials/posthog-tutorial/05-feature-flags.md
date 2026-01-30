---
layout: default
title: "Chapter 5: Feature Flags & Experiments"
parent: "PostHog Tutorial"
nav_order: 5
---

# Chapter 5: Feature Flags & Experiments

In [Chapter 4](04-session-recordings.md), you learned how to watch real user sessions to understand friction points. Now it is time to fix those problems -- safely. Feature flags let you ship code to production without exposing it to every user, and experiments let you measure whether your changes actually improve the metrics that matter.

This chapter covers the full lifecycle of feature flags and A/B tests in PostHog: creating flags, evaluating them on the client and server, targeting specific cohorts, running statistically rigorous experiments, and managing the cleanup that keeps your codebase from drowning in flag conditionals.

## What You Will Learn

- Create and manage feature flags in PostHog
- Evaluate flags on the client (JavaScript) and server (Node.js, Python)
- Target flags to specific user segments and cohorts
- Design, run, and analyze A/B experiments
- Implement guardrails, kill switches, and gradual rollouts
- Clean up flags after rollout is complete

## Feature Flags Overview

A feature flag is a runtime switch that controls whether a user sees a particular feature. Flags decouple deployment from release, which means you can merge code to main, deploy to production, and then decide who sees the feature and when.

```mermaid
flowchart LR
    Deploy["Code deployed<br/>to production"] --> Flag{"Feature flag<br/>enabled?"}
    Flag -->|Yes| New["User sees<br/>new feature"]
    Flag -->|No| Old["User sees<br/>old feature"]
    Flag -->|Error| Old

    classDef deploy fill:#e1f5fe,stroke:#01579b
    classDef decision fill:#fff3e0,stroke:#ef6c00
    classDef outcome fill:#e8f5e8,stroke:#1b5e20

    class Deploy deploy
    class Flag decision
    class New,Old outcome
```

### Types of Feature Flags

| Type | Description | Use Case |
|------|-------------|----------|
| **Boolean** | On or off | Simple feature toggle |
| **Multivariate** | Multiple string variants | A/B/C testing, theme selection |
| **Percentage rollout** | Enabled for N% of users | Gradual rollout |
| **User targeting** | Enabled for specific users/cohorts | Beta access, internal testing |
| **Release toggle** | Temporary flag for a release | Ship safely, remove after |
| **Ops toggle** | Controls operational behavior | Circuit breaker, kill switch |

## Creating Feature Flags

### In the PostHog UI

1. Navigate to **Feature Flags** in the sidebar
2. Click **New Feature Flag**
3. Enter a flag key (e.g., `new-checkout-flow`)
4. Choose the flag type:
   - **Boolean**: on/off
   - **Multivariate**: define variants (e.g., `control`, `variant-a`, `variant-b`)
5. Set rollout conditions:
   - Percentage of users (e.g., 25%)
   - Property filters (e.g., `plan = growth`)
   - Cohort membership (e.g., "Beta Testers")
6. Click **Save**

### Via the API

```typescript
// Create a feature flag via the PostHog API
const response = await fetch(
  'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/feature_flags/',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_PERSONAL_API_KEY'
    },
    body: JSON.stringify({
      key: 'new-checkout-flow',
      name: 'New Checkout Flow',
      filters: {
        groups: [
          {
            properties: [
              { key: 'plan', value: 'growth', type: 'person' }
            ],
            rollout_percentage: 50
          }
        ],
        multivariate: null  // null for boolean flags
      },
      active: true
    })
  }
)

const flag = await response.json()
console.log(`Created flag: ${flag.key} (ID: ${flag.id})`)
```

```python
import requests

response = requests.post(
    'https://app.posthog.com/api/projects/YOUR_PROJECT_ID/feature_flags/',
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_PERSONAL_API_KEY',
    },
    json={
        'key': 'new-checkout-flow',
        'name': 'New Checkout Flow',
        'filters': {
            'groups': [
                {
                    'properties': [
                        {'key': 'plan', 'value': 'growth', 'type': 'person'}
                    ],
                    'rollout_percentage': 50,
                }
            ],
        },
        'active': True,
    }
)

flag = response.json()
print(f"Created flag: {flag['key']}")
```

## Evaluating Feature Flags

### Client-Side (JavaScript / TypeScript)

```typescript
import posthog from 'posthog-js'

// ---- Boolean flag ----
if (posthog.isFeatureEnabled('new-checkout-flow')) {
  renderNewCheckout()
} else {
  renderLegacyCheckout()
}

// ---- Multivariate flag ----
const variant = posthog.getFeatureFlagPayload('homepage-hero')
// variant might be: { headline: "Ship faster", cta: "Start free trial" }

switch (posthog.getFeatureFlag('homepage-hero')) {
  case 'control':
    renderOriginalHero()
    break
  case 'variant-a':
    renderHeroWithTestimonials()
    break
  case 'variant-b':
    renderHeroWithVideo()
    break
  default:
    renderOriginalHero()
}

// ---- Wait for flags to load ----
posthog.onFeatureFlags((flags) => {
  // Called once flags are loaded from the server
  console.log('Feature flags loaded:', flags)

  if (posthog.isFeatureEnabled('new-checkout-flow')) {
    showNewCheckoutBanner()
  }
})

// ---- Reload flags (e.g., after user upgrades plan) ----
posthog.reloadFeatureFlags()
```

### React Hook Integration

```tsx
import { useFeatureFlagEnabled, useFeatureFlagPayload } from 'posthog-js/react'

function CheckoutPage() {
  const isNewCheckout = useFeatureFlagEnabled('new-checkout-flow')
  const checkoutConfig = useFeatureFlagPayload('new-checkout-flow')

  if (isNewCheckout === undefined) {
    return <LoadingSpinner />  // flags still loading
  }

  if (isNewCheckout) {
    return <NewCheckout config={checkoutConfig} />
  }

  return <LegacyCheckout />
}

function PricingPage() {
  const variant = useFeatureFlagEnabled('pricing-experiment')

  return (
    <div>
      {variant === 'annual-first' ? (
        <AnnualPricingFirst />
      ) : (
        <MonthlyPricingFirst />
      )}
    </div>
  )
}
```

### Server-Side (Node.js)

Server-side evaluation is essential for backend logic, API responses, and server-rendered pages.

```typescript
import { PostHog } from 'posthog-node'

const client = new PostHog('YOUR_API_KEY', {
  host: 'https://app.posthog.com'
})

// ---- Evaluate a boolean flag ----
async function getCheckoutVersion(userId: string): Promise<string> {
  const isEnabled = await client.isFeatureEnabled(
    'new-checkout-flow',
    userId
  )
  return isEnabled ? 'v2' : 'v1'
}

// ---- Evaluate a multivariate flag ----
async function getHomepageVariant(userId: string) {
  const variant = await client.getFeatureFlag(
    'homepage-hero',
    userId
  )
  return variant  // 'control' | 'variant-a' | 'variant-b'
}

// ---- Get flag payload ----
async function getCheckoutConfig(userId: string) {
  const payload = await client.getFeatureFlagPayload(
    'new-checkout-flow',
    userId
  )
  return payload  // JSON object defined in PostHog UI
}

// ---- Batch evaluation (all flags for a user) ----
async function getAllFlags(userId: string) {
  const flags = await client.getAllFlags(userId)
  // { 'new-checkout-flow': true, 'homepage-hero': 'variant-a', ... }
  return flags
}

// Express.js middleware example
import { Request, Response, NextFunction } from 'express'

async function featureFlagMiddleware(
  req: Request, res: Response, next: NextFunction
) {
  const userId = req.user?.id || req.sessionID

  res.locals.featureFlags = await client.getAllFlags(userId)
  next()
}
```

### Server-Side (Python)

```python
from posthog import Posthog

posthog_client = Posthog(
    api_key='YOUR_API_KEY',
    host='https://app.posthog.com'
)

# Boolean flag evaluation
def get_checkout_version(user_id: str) -> str:
    is_enabled = posthog_client.feature_enabled(
        key='new-checkout-flow',
        distinct_id=user_id
    )
    return 'v2' if is_enabled else 'v1'

# Multivariate flag evaluation
def get_homepage_variant(user_id: str) -> str:
    variant = posthog_client.get_feature_flag(
        key='homepage-hero',
        distinct_id=user_id
    )
    return variant or 'control'

# Flag with payload
def get_checkout_config(user_id: str) -> dict:
    payload = posthog_client.get_feature_flag_payload(
        key='new-checkout-flow',
        distinct_id=user_id
    )
    return payload or {}

# Django view example
from django.http import JsonResponse

def pricing_view(request):
    user_id = str(request.user.id) if request.user.is_authenticated else request.session.session_key

    variant = posthog_client.get_feature_flag(
        key='pricing-experiment',
        distinct_id=user_id,
        person_properties={
            'plan': request.user.plan if request.user.is_authenticated else 'anonymous',
            'country': request.META.get('HTTP_CF_IPCOUNTRY', 'unknown'),
        }
    )

    return JsonResponse({'pricing_variant': variant or 'control'})
```

## Targeting and Rollout Strategies

### Rollout Progression

A safe rollout starts small and expands gradually as you gain confidence.

```mermaid
flowchart LR
    A["Internal only<br/>(1%)"] --> B["Beta users<br/>(5%)"]
    B --> C["Growth plan<br/>(25%)"]
    C --> D["All users<br/>(50%)"]
    D --> E["Full rollout<br/>(100%)"]
    E --> F["Remove flag<br/>from code"]

    classDef early fill:#fff3e0,stroke:#ef6c00
    classDef mid fill:#e1f5fe,stroke:#01579b
    classDef full fill:#e8f5e8,stroke:#1b5e20

    class A,B early
    class C,D mid
    class E,F full
```

### Targeting Conditions

| Condition Type | Example | Use Case |
|---------------|---------|----------|
| **Percentage** | 25% of all users | Gradual rollout |
| **Person property** | `plan = enterprise` | Plan-based features |
| **Cohort** | "Beta Testers" cohort | Controlled beta access |
| **Group property** | `company.employee_count > 100` | B2B feature gating |
| **Multiple conditions** | 100% of enterprise + 10% of growth | Tiered rollout |

### Multi-Condition Flag Configuration

```typescript
// Flag with multiple rollout groups (configured in UI)
// Group 1: 100% of internal team
// Group 2: 100% of beta testers cohort
// Group 3: 25% of growth plan users
// Group 4: 0% of free plan users

// The SDK evaluates groups in order; first match wins
const result = posthog.isFeatureEnabled('new-dashboard')
// true if user matches any of the above groups
```

## Running A/B Experiments

Experiments build on feature flags by adding statistical rigor. An experiment is a multivariate flag with a defined primary metric, sample size requirement, and statistical significance threshold.

### Experiment Lifecycle

```mermaid
flowchart TD
    A["Define hypothesis"] --> B["Choose primary metric"]
    B --> C["Calculate sample size"]
    C --> D["Create experiment<br/>(flag + variants)"]
    D --> E["Launch experiment"]
    E --> F{"Monitor results"}
    F -->|"Significant"| G["Ship winner"]
    F -->|"Not yet"| F
    F -->|"Negative"| H["Roll back"]
    G --> I["Remove flag"]
    H --> I

    classDef plan fill:#e1f5fe,stroke:#01579b
    classDef run fill:#fff3e0,stroke:#ef6c00
    classDef result fill:#e8f5e8,stroke:#1b5e20

    class A,B,C plan
    class D,E,F run
    class G,H,I result
```

### Creating an Experiment

In the PostHog UI:

1. Navigate to **Experiments** and click **New Experiment**
2. **Name**: "Checkout Flow Redesign"
3. **Hypothesis**: "The simplified checkout flow will increase purchase completion by 15%"
4. **Feature flag**: Select or create `checkout-experiment`
5. **Variants**:
   - `control` (existing checkout)
   - `test` (new simplified checkout)
6. **Primary metric**: `completed_purchase` event (unique users)
7. **Secondary metrics**: `checkout_time_seconds` (average), `cart_abandonment` (count)
8. **Minimum sample size**: Auto-calculated based on desired MDE (minimum detectable effect)
9. Click **Launch**

### Implementing Experiment Variants

```typescript
// Client-side experiment implementation
import posthog from 'posthog-js'

function CheckoutPage({ cartItems }: { cartItems: CartItem[] }) {
  const variant = posthog.getFeatureFlag('checkout-experiment')

  // Track that the user was exposed to the experiment
  // PostHog does this automatically when you call getFeatureFlag
  // but you can add custom exposure tracking:
  posthog.capture('$feature_flag_called', {
    $feature_flag: 'checkout-experiment',
    $feature_flag_response: variant
  })

  switch (variant) {
    case 'test':
      return <SimplifiedCheckout items={cartItems} />
    case 'control':
    default:
      return <OriginalCheckout items={cartItems} />
  }
}

// Track the primary metric
function handlePurchaseComplete(orderId: string, total: number) {
  posthog.capture('completed_purchase', {
    order_id: orderId,
    total_cents: Math.round(total * 100),
    item_count: cartItems.length
  })
}
```

```python
# Server-side experiment for API-driven features
from posthog import Posthog

posthog_client = Posthog(
    api_key='YOUR_API_KEY',
    host='https://app.posthog.com'
)

def get_pricing_page(user_id: str) -> dict:
    variant = posthog_client.get_feature_flag(
        key='pricing-experiment',
        distinct_id=user_id
    )

    if variant == 'annual-first':
        return {
            'default_billing': 'annual',
            'highlight_savings': True,
            'show_monthly_toggle': True,
        }
    else:
        # control
        return {
            'default_billing': 'monthly',
            'highlight_savings': False,
            'show_monthly_toggle': True,
        }
```

### Reading Experiment Results

PostHog calculates statistical significance automatically. Key metrics to understand:

| Metric | Meaning | Action Threshold |
|--------|---------|-----------------|
| **Conversion rate** | % of exposed users who completed the goal | -- |
| **Relative lift** | % change vs. control | Positive lift is good |
| **Confidence interval** | Range of plausible true effects | Narrow is better |
| **Statistical significance** | Probability the result is not due to chance | > 95% to ship |
| **Sample size** | Number of users exposed | Must meet minimum |

### When to Stop an Experiment

| Scenario | Action |
|----------|--------|
| Significance reached, positive lift | Ship the winning variant |
| Significance reached, negative lift | Roll back to control |
| Sample size met, no significance | Result is inconclusive; ship based on qualitative data or run longer |
| Guardrail metric degraded | Stop immediately regardless of primary metric |
| Critical bug in variant | Kill switch; stop experiment |

## Guardrails and Safety

### Kill Switches

A kill switch is a boolean flag that can instantly disable a feature across all users.

```typescript
// Wrap risky features with a kill switch
async function processPayment(paymentData: PaymentData) {
  // Check kill switch first
  const paymentsEnabled = await client.isFeatureEnabled(
    'payments-kill-switch',
    paymentData.userId
  )

  if (!paymentsEnabled) {
    throw new Error('Payments temporarily disabled')
  }

  // Proceed with payment processing
  return await stripe.charges.create(paymentData)
}
```

### Guardrail Metrics

Always track negative metrics alongside your primary experiment metric.

```typescript
// Track guardrail metrics during experiments
posthog.capture('page_load_time', {
  duration_ms: performance.now(),
  page: 'checkout'
})

posthog.capture('client_error', {
  error_type: 'checkout_error',
  message: error.message,
  variant: posthog.getFeatureFlag('checkout-experiment')
})
```

| Guardrail | Threshold | Action if Breached |
|-----------|-----------|-------------------|
| Error rate | > 2x baseline | Auto-disable flag |
| Page load time | > 500ms increase | Investigate |
| Customer support tickets | > 1.5x baseline | Review recordings |
| Revenue per user | > 5% decrease | Stop experiment |

### Gradual Rollout with Monitoring

```mermaid
flowchart TD
    A["Day 1: 5% rollout"] --> B{"Error rate<br/>normal?"}
    B -->|Yes| C["Day 3: 25% rollout"]
    B -->|No| Z["Roll back to 0%"]
    C --> D{"Metrics<br/>stable?"}
    D -->|Yes| E["Day 7: 50% rollout"]
    D -->|No| Z
    E --> F{"Confident?"}
    F -->|Yes| G["Day 14: 100% rollout"]
    F -->|No| H["Hold and investigate"]

    classDef safe fill:#e8f5e8,stroke:#1b5e20
    classDef check fill:#fff3e0,stroke:#ef6c00
    classDef danger fill:#ffebee,stroke:#c62828

    class A,C,E,G safe
    class B,D,F check
    class Z,H danger
```

## Flag Lifecycle and Cleanup

Feature flags are meant to be temporary. Permanent flags accumulate technical debt.

### Flag States

| State | Description | Action |
|-------|-------------|--------|
| **Draft** | Created but not active | Finalize targeting |
| **Active** | Being evaluated for users | Monitor metrics |
| **Rolled out** | 100% of users see the feature | Remove flag from code |
| **Stale** | Active but not evaluated in 30+ days | Archive or delete |
| **Archived** | Disabled and hidden | Clean up code references |

### Cleanup Workflow

1. **Experiment concludes**: ship the winner or roll back
2. **Set flag to 100%**: all users see the winning variant
3. **Remove flag checks from code**: replace conditionals with the winning path
4. **Deploy code cleanup**: no more flag evaluation calls
5. **Archive the flag in PostHog**: keep for historical reference

```typescript
// BEFORE cleanup: flag check in code
function CheckoutPage() {
  if (posthog.isFeatureEnabled('new-checkout-flow')) {
    return <NewCheckout />
  }
  return <LegacyCheckout />
}

// AFTER cleanup: flag removed, winning variant is the default
function CheckoutPage() {
  return <NewCheckout />
}
// Delete LegacyCheckout component entirely
```

### Tracking Flag Debt

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Active flags | < 20 | PostHog feature flags list |
| Stale flags (30+ days unused) | 0 | Audit monthly |
| Average flag age | < 30 days | Track creation dates |
| Flags without owner | 0 | Require owner field |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Flag always returns false | Flag not active or user does not match conditions | Check flag status and targeting rules |
| Different result on client vs. server | Person properties differ | Pass same properties to both evaluations |
| Flag value does not update | Flags cached on client | Call `posthog.reloadFeatureFlags()` |
| Experiment shows no data | `$feature_flag_called` event not firing | Ensure flag is evaluated, not just checked |
| Uneven variant distribution | Hash collision or small sample | Wait for more users; check targeting filters |
| User sees different variant on return | distinct_id changed (e.g., logged out) | Ensure consistent ID; use `posthog.identify()` |

## Performance Considerations

- **Local evaluation**: Use PostHog's local evaluation mode on the server to avoid network calls for every flag check. The SDK downloads flag definitions periodically and evaluates them locally.
- **Caching**: Client-side flags are cached in the browser. Server-side SDKs support in-memory caching with configurable TTL.
- **Avoid hot-path checks**: Do not evaluate flags inside tight loops or on every render. Cache the result in a variable or React state.
- **Payload size**: Flag payloads (JSON data attached to flags) should be small. Avoid embedding large configuration objects.

```typescript
// Local evaluation for high-performance server-side checks
import { PostHog } from 'posthog-node'

const client = new PostHog('YOUR_API_KEY', {
  host: 'https://app.posthog.com',
  personalApiKey: 'YOUR_PERSONAL_API_KEY',  // enables local evaluation
  featureFlagsPollingInterval: 30000          // refresh every 30 seconds
})

// Now isFeatureEnabled() evaluates locally without network calls
const isEnabled = await client.isFeatureEnabled('new-checkout-flow', 'user_123')
```

## Summary

Feature flags and experiments are the bridge between insight and action. Flags let you ship code safely with gradual rollouts and instant rollback. Experiments add statistical rigor so you can prove -- not just hope -- that your changes improve the metrics that matter. Combined with the funnels, retention analysis, and session recordings from earlier chapters, you now have a complete toolkit for making data-driven product decisions.

## Key Takeaways

1. **Decouple deployment from release** -- merge to main confidently knowing flags control who sees what.
2. **Start every rollout small** -- internal users first, then beta, then a percentage, then 100%.
3. **Define your primary metric before launching an experiment** -- a test without a clear goal produces ambiguous results.
4. **Always set guardrail metrics** -- monitor error rates, latency, and revenue to catch regressions before they hurt.
5. **Clean up flags aggressively** -- stale flags are technical debt. Archive them within 30 days of full rollout.

## Next Steps

With feature flags and experiments in your toolkit, you need a way to present all these insights to stakeholders and your team. In [Chapter 6: Dashboards & Insights](06-dashboards-insights.md), you will learn how to build dashboards that tell a coherent story about your product's health, growth, and user experience.

---

*Built with insights from the [PostHog](https://github.com/PostHog/posthog) project.*
