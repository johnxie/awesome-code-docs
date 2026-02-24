---
layout: default
title: "LiteLLM Tutorial - Chapter 6: Cost Tracking"
nav_order: 6
has_children: false
parent: LiteLLM Tutorial
---

# Chapter 6: Cost Tracking

Welcome to **Chapter 6: Cost Tracking**. In this part of **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Monitor, analyze, and optimize your LLM spending across all providers with detailed cost insights.

## Overview

Understanding and controlling costs is crucial for production LLM applications. LiteLLM provides comprehensive cost tracking that works across all providers, giving you detailed insights into your spending patterns.

## Basic Cost Tracking

Enable automatic cost calculation:

```python
import litellm
from litellm import completion_cost

# Enable cost tracking globally
litellm.completion_cost = completion_cost

# Make a request with cost tracking
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain machine learning in simple terms"}]
)

# Access cost information
print(f"Cost: ${response._hidden_params.get('response_cost', 0):.4f}")
print(f"Usage: {response.usage}")
```

## Setting Up Cost Tracking Database

Use a database to persist cost data:

```python
import sqlite3
import json
from datetime import datetime

class CostTracker:
    def __init__(self, db_path="costs.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the cost tracking database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS costs (
                    id INTEGER PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    total_tokens INTEGER,
                    cost_usd REAL,
                    user_id TEXT,
                    api_key_hash TEXT,
                    metadata TEXT
                )
            ''')

            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_model ON costs(model)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON costs(timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON costs(user_id)')

    def log_cost(self, response, user_id=None, metadata=None):
        """Log cost information to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO costs (model, input_tokens, output_tokens, total_tokens, cost_usd, user_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                response.model,
                response.usage.prompt_tokens if response.usage else 0,
                response.usage.completion_tokens if response.usage else 0,
                response.usage.total_tokens if response.usage else 0,
                response._hidden_params.get('response_cost', 0),
                user_id,
                json.dumps(metadata) if metadata else None
            ))

# Initialize cost tracker
cost_tracker = CostTracker()
```

## Integrating Cost Tracking

Modify completion calls to automatically log costs:

```python
def completion_with_cost_tracking(model, messages, user_id=None, **kwargs):
    """Completion with automatic cost tracking."""
    response = litellm.completion(model=model, messages=messages, **kwargs)

    # Log the cost
    cost_tracker.log_cost(response, user_id=user_id)

    return response

# Usage
response = completion_with_cost_tracking(
    model="gpt-4",
    messages=[{"role": "user", "content": "Write a Python function"}],
    user_id="user123"
)
```

## Cost Analysis Queries

Analyze your spending patterns:

```python
class CostAnalyzer:
    def __init__(self, db_path="costs.db"):
        self.db_path = db_path

    def get_total_cost(self, days=30):
        """Get total cost for the last N days."""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute('''
                SELECT SUM(cost_usd)
                FROM costs
                WHERE timestamp >= date('now', '-{} days')
            '''.format(days)).fetchone()

            return result[0] or 0

    def get_cost_by_model(self, days=30):
        """Get cost breakdown by model."""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute('''
                SELECT model, SUM(cost_usd), COUNT(*)
                FROM costs
                WHERE timestamp >= date('now', '-{} days')
                GROUP BY model
                ORDER BY SUM(cost_usd) DESC
            '''.format(days)).fetchall()

            return [{"model": r[0], "cost": r[1], "requests": r[2]} for r in results]

    def get_cost_by_user(self, days=30, limit=10):
        """Get top users by cost."""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute('''
                SELECT user_id, SUM(cost_usd), COUNT(*)
                FROM costs
                WHERE timestamp >= date('now', '-{} days') AND user_id IS NOT NULL
                GROUP BY user_id
                ORDER BY SUM(cost_usd) DESC
                LIMIT {}
            '''.format(days, limit)).fetchall()

            return [{"user_id": r[0], "cost": r[1], "requests": r[2]} for r in results]

    def get_daily_costs(self, days=30):
        """Get daily cost breakdown."""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute('''
                SELECT DATE(timestamp), SUM(cost_usd)
                FROM costs
                WHERE timestamp >= date('now', '-{} days')
                GROUP BY DATE(timestamp)
                ORDER BY DATE(timestamp)
            '''.format(days)).fetchall()

            return [{"date": r[0], "cost": r[1]} for r in results]

    def get_cost_efficiency(self, days=30):
        """Analyze cost efficiency (cost per token)."""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute('''
                SELECT model, SUM(cost_usd) / SUM(total_tokens) as cost_per_token,
                       AVG(total_tokens) as avg_tokens_per_request
                FROM costs
                WHERE timestamp >= date('now', '-{} days') AND total_tokens > 0
                GROUP BY model
                ORDER BY cost_per_token
            '''.format(days)).fetchall()

            return [{
                "model": r[0],
                "cost_per_token": r[1],
                "avg_tokens_per_request": r[2]
            } for r in results]

# Usage
analyzer = CostAnalyzer()

print(f"Total cost (30 days): ${analyzer.get_total_cost():.2f}")

print("\nCost by model:")
for model_cost in analyzer.get_cost_by_model():
    print(f"  {model_cost['model']}: ${model_cost['cost']:.2f} ({model_cost['requests']} requests)")

print("\nTop users by cost:")
for user_cost in analyzer.get_cost_by_user():
    print(f"  {user_cost['user_id']}: ${user_cost['cost']:.2f}")
```

## Real-Time Cost Monitoring

Monitor costs in real-time:

```python
class CostMonitor:
    def __init__(self, analyzer, alert_thresholds=None):
        self.analyzer = analyzer
        self.alert_thresholds = alert_thresholds or {
            "daily_limit": 100.0,
            "user_limit": 10.0,
            "model_limit": 50.0
        }

    def check_alerts(self):
        """Check for cost alerts."""
        alerts = []

        # Daily spending alert
        daily_cost = self.analyzer.get_total_cost(days=1)
        if daily_cost >= self.alert_thresholds["daily_limit"]:
            alerts.append(f"Daily spending alert: ${daily_cost:.2f} (limit: ${self.alert_thresholds['daily_limit']:.2f})")

        # User spending alerts
        user_costs = self.analyzer.get_cost_by_user(days=1)
        for user in user_costs:
            if user["cost"] >= self.alert_thresholds["user_limit"]:
                alerts.append(f"User {user['user_id']} spending alert: ${user['cost']:.2f}")

        # Model spending alerts
        model_costs = self.analyzer.get_cost_by_model(days=1)
        for model in model_costs:
            if model["cost"] >= self.alert_thresholds["model_limit"]:
                alerts.append(f"Model {model['model']} spending alert: ${model['cost']:.2f}")

        return alerts

    def generate_report(self):
        """Generate a comprehensive cost report."""
        report = {
            "period": "30 days",
            "total_cost": self.analyzer.get_total_cost(),
            "daily_breakdown": self.analyzer.get_daily_costs(),
            "cost_by_model": self.analyzer.get_cost_by_model(),
            "cost_by_user": self.analyzer.get_cost_by_user(limit=20),
            "cost_efficiency": self.analyzer.get_cost_efficiency(),
            "alerts": self.check_alerts()
        }

        return report

# Usage
monitor = CostMonitor(analyzer)
alerts = monitor.check_alerts()

if alerts:
    print("🚨 Cost Alerts:")
    for alert in alerts:
        print(f"  {alert}")
else:
    print("✅ No cost alerts")

# Generate full report
report = monitor.generate_report()
print(f"\nTotal 30-day cost: ${report['total_cost']:.2f}")
```

## Cost Optimization Strategies

Implement intelligent cost management:

```python
class CostOptimizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        # Cost per 1K tokens (approximate, update based on your pricing)
        self.model_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
            "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
        }

    def estimate_cost(self, model, input_tokens, output_tokens):
        """Estimate cost for a request."""
        if model not in self.model_costs:
            return float('inf')

        costs = self.model_costs[model]
        input_cost = (input_tokens / 1000) * costs["input"]
        output_cost = (output_tokens / 1000) * costs["output"]

        return input_cost + output_cost

    def select_best_model(self, task_description, input_tokens, max_output_tokens=1000, budget=None):
        """Select the best model for the task within budget."""

        task_lower = task_description.lower()

        # Determine quality requirements
        needs_high_quality = any(keyword in task_lower for keyword in [
            "analyze", "research", "complex", "critical", "important"
        ])

        # Filter suitable models
        candidates = []
        for model, costs in self.model_costs.items():
            estimated_cost = self.estimate_cost(model, input_tokens, max_output_tokens)

            if budget and estimated_cost > budget:
                continue

            # Score based on quality and cost
            quality_score = 1.0
            if "gpt-4" in model:
                quality_score = 1.0
            elif "claude-3-opus" in model:
                quality_score = 0.95
            elif "claude-3-sonnet" in model or "gpt-4-turbo" in model:
                quality_score = 0.8
            elif "claude-3-haiku" in model or "gpt-3.5-turbo" in model:
                quality_score = 0.6

            if needs_high_quality and quality_score < 0.8:
                continue

            candidates.append({
                "model": model,
                "estimated_cost": estimated_cost,
                "quality_score": quality_score,
                "efficiency": quality_score / estimated_cost if estimated_cost > 0 else 0
            })

        if not candidates:
            return "gpt-3.5-turbo"  # Safe fallback

        # Return most efficient model
        return max(candidates, key=lambda x: x["efficiency"])["model"]

    def optimize_request(self, messages, task_description=None, budget=None):
        """Optimize a request for cost efficiency."""

        # Estimate input tokens
        input_text = " ".join([msg["content"] for msg in messages])
        estimated_input_tokens = len(input_text.split()) * 1.3  # Rough estimate

        # Select optimal model
        optimal_model = self.select_best_model(
            task_description or "general task",
            estimated_input_tokens,
            budget=budget
        )

        # Make optimized request
        response = litellm.completion(
            model=optimal_model,
            messages=messages,
            max_tokens=1000 if not budget else min(1000, int(budget * 1000))  # Rough token limit
        )

        # Log cost
        cost_tracker.log_cost(response, metadata={"optimized": True, "task": task_description})

        return response, optimal_model

# Usage
optimizer = CostOptimizer(analyzer)

response, selected_model = optimizer.optimize_request(
    messages=[{"role": "user", "content": "Write a simple function to reverse a string"}],
    task_description="code generation",
    budget=0.01  # $0.01 max
)

print(f"Selected model: {selected_model}")
print(f"Response: {response.choices[0].message.content[:100]}...")
```

## Budget Management

Implement user and project budgets:

```python
class BudgetManager:
    def __init__(self, analyzer, db_path="costs.db"):
        self.analyzer = analyzer
        self.db_path = db_path

        # Budget configurations
        self.user_budgets = {
            "free": 1.0,      # $1/month
            "basic": 10.0,    # $10/month
            "pro": 100.0,     # $100/month
            "enterprise": float('inf')
        }

    def get_user_spending(self, user_id, days=30):
        """Get user's spending in the last N days."""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute('''
                SELECT SUM(cost_usd)
                FROM costs
                WHERE user_id = ? AND timestamp >= date('now', '-{} days')
            '''.format(days), (user_id,)).fetchone()

            return result[0] or 0

    def check_budget(self, user_id, plan="free"):
        """Check if user is within budget."""
        budget = self.user_budgets.get(plan, 0)
        spending = self.get_user_spending(user_id)

        remaining = budget - spending
        within_budget = remaining > 0

        return {
            "within_budget": within_budget,
            "budget": budget,
            "spending": spending,
            "remaining": max(0, remaining)
        }

    def completion_with_budget_check(self, model, messages, user_id, user_plan="free", **kwargs):
        """Completion that checks budget before proceeding."""

        budget_status = self.check_budget(user_id, user_plan)

        if not budget_status["within_budget"]:
            raise Exception(f"Budget exceeded for {user_plan} plan. "
                          f"Spent: ${budget_status['spending']:.2f}, "
                          f"Budget: ${budget_status['budget']:.2f}")

        # Check if this request would exceed budget
        # (Rough estimation - could be improved)
        estimated_cost = 0.01  # Conservative estimate

        if budget_status["remaining"] < estimated_cost:
            raise Exception(f"Insufficient budget remaining (${budget_status['remaining']:.4f}) "
                          f"for estimated cost (${estimated_cost:.4f})")

        # Proceed with request
        response = litellm.completion(model=model, messages=messages, **kwargs)

        # Log cost
        cost_tracker.log_cost(response, user_id=user_id, metadata={"plan": user_plan})

        return response

# Usage
budget_manager = BudgetManager(analyzer)

try:
    response = budget_manager.completion_with_budget_check(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}],
        user_id="user123",
        user_plan="basic"
    )
    print("Request successful")
except Exception as e:
    print(f"Budget error: {e}")
```

## Cost Dashboards

Create simple cost visualization:

```python
import matplotlib.pyplot as plt
import pandas as pd

class CostDashboard:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def plot_daily_costs(self, days=30):
        """Plot daily cost trends."""
        daily_costs = self.analyzer.get_daily_costs(days)

        if not daily_costs:
            print("No cost data available")
            return

        df = pd.DataFrame(daily_costs)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['cost'], marker='o')
        plt.title(f'Daily Costs - Last {days} Days')
        plt.xlabel('Date')
        plt.ylabel('Cost ($)')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('daily_costs.png', dpi=150, bbox_inches='tight')
        plt.show()

    def plot_model_comparison(self, days=30):
        """Compare costs across models."""
        model_costs = self.analyzer.get_cost_by_model(days)

        if not model_costs:
            print("No cost data available")
            return

        df = pd.DataFrame(model_costs)

        plt.figure(figsize=(10, 6))
        bars = plt.bar(df['model'], df['cost'])
        plt.title(f'Model Cost Comparison - Last {days} Days')
        plt.xlabel('Model')
        plt.ylabel('Cost ($)')
        plt.xticks(rotation=45)

        # Add value labels on bars
        for bar, cost in zip(bars, df['cost']):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'${cost:.2f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()

# Usage (requires matplotlib and pandas)
# dashboard = CostDashboard(analyzer)
# dashboard.plot_daily_costs()
# dashboard.plot_model_comparison()
```

## Best Practices

1. **Monitor Regularly**: Set up daily cost reports and alerts
2. **Set Budgets**: Define spending limits for users and projects
3. **Optimize Models**: Use cheaper models for simpler tasks
4. **Cache Results**: Avoid redundant requests for the same content
5. **Track Efficiency**: Monitor cost per quality score
6. **User Education**: Show users their spending and encourage cost awareness
7. **Anomaly Detection**: Alert on unusual spending patterns

## Export and Integration

Export cost data for external analysis:

```python
def export_costs_to_csv(filename="costs_export.csv", days=30):
    """Export cost data to CSV."""
    with sqlite3.connect("costs.db") as conn:
        # Get all cost data
        df = pd.read_sql_query('''
            SELECT * FROM costs
            WHERE timestamp >= date('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days), conn)

        df.to_csv(filename, index=False)
        print(f"Exported {len(df)} records to {filename}")

# Integration with external systems
def send_cost_alerts_to_slack(webhook_url, alerts):
    """Send cost alerts to Slack."""
    import requests

    for alert in alerts:
        payload = {
            "text": f"💰 Cost Alert: {alert}",
            "username": "Cost Monitor",
            "icon_emoji": ":money_with_wings:"
        }

        requests.post(webhook_url, json=payload)

# Usage
# export_costs_to_csv()
# send_cost_alerts_to_slack("https://hooks.slack.com/...", alerts)
```

Cost tracking is essential for sustainable LLM applications. With proper monitoring and optimization, you can maintain high-quality AI functionality while controlling expenses effectively.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `model`, `cost` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Cost Tracking` as an operating subsystem inside **LiteLLM Tutorial: Unified LLM Gateway and Routing Layer**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `days`, `analyzer`, `response` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Cost Tracking` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `model` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `cost`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [LiteLLM Repository](https://github.com/BerriAI/litellm)
  Why it matters: authoritative reference on `LiteLLM Repository` (github.com).
- [LiteLLM Releases](https://github.com/BerriAI/litellm/releases)
  Why it matters: authoritative reference on `LiteLLM Releases` (github.com).
- [LiteLLM Docs](https://docs.litellm.ai/)
  Why it matters: authoritative reference on `LiteLLM Docs` (docs.litellm.ai).

Suggested trace strategy:
- search upstream code for `self` and `model` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Fallbacks & Retries](05-fallbacks.md)
- [Next Chapter: Chapter 7: LiteLLM Proxy](07-proxy.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
