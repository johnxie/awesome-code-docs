---
layout: default
title: "Chapter 4: Conditional Logic"
parent: "LangGraph Tutorial"
nav_order: 4
---

# Chapter 4: Conditional Logic

Welcome to the decision-making layer of LangGraph! Conditional logic is what makes your graphs intelligent - they can adapt, make decisions, and route execution based on data, context, and complex conditions. This chapter explores advanced routing patterns, decision trees, and dynamic graph modification.

## Understanding Conditional Routing

Conditional routing allows your graph to make intelligent decisions about which path to take based on the current state, external data, or complex business logic.

### Basic Conditional Edges

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class ConditionalState(TypedDict):
    data: dict
    confidence_score: float
    decision_path: str
    processing_steps: list

def analyze_data_node(state: ConditionalState) -> ConditionalState:
    """Analyze data and determine confidence"""
    data = state.get("data", {})
    confidence = analyze_confidence(data)

    return {
        **state,
        "confidence_score": confidence,
        "processing_steps": state.get("processing_steps", []) + ["analysis"]
    }

def route_based_on_confidence(state: ConditionalState) -> str:
    """Route to different nodes based on confidence score"""
    confidence = state.get("confidence_score", 0)

    if confidence >= 0.9:
        return "high_confidence_path"
    elif confidence >= 0.7:
        return "medium_confidence_path"
    elif confidence >= 0.5:
        return "low_confidence_path"
    else:
        return "uncertain_path"

# Create graph with conditional routing
graph = StateGraph(ConditionalState)

# Add nodes
graph.add_node("analyze", analyze_data_node)
graph.add_node("high_confidence", lambda s: {**s, "decision_path": "high"})
graph.add_node("medium_confidence", lambda s: {**s, "decision_path": "medium"})
graph.add_node("low_confidence", lambda s: {**s, "decision_path": "low"})
graph.add_node("uncertain", lambda s: {**s, "decision_path": "uncertain"})

# Set up conditional routing
graph.set_entry_point("analyze")
graph.add_conditional_edges(
    "analyze",
    route_based_on_confidence,
    {
        "high_confidence_path": "high_confidence",
        "medium_confidence_path": "medium_confidence",
        "low_confidence_path": "low_confidence",
        "uncertain_path": "uncertain"
    }
)

# All paths converge to end
graph.add_edge("high_confidence", END)
graph.add_edge("medium_confidence", END)
graph.add_edge("low_confidence", END)
graph.add_edge("uncertain", END)
```

## Advanced Decision Trees

### Multi-Level Decision Making

```python
def create_decision_tree() -> StateGraph:
    """Create a complex decision tree"""

    class DecisionState(TypedDict):
        data: dict
        risk_level: str
        priority: str
        category: str
        recommended_action: str
        decision_factors: list

    graph = StateGraph(DecisionState)

    # Level 1: Risk Assessment
    def assess_risk(state: DecisionState) -> DecisionState:
        data = state.get("data", {})
        risk_score = calculate_risk_score(data)

        risk_level = "high" if risk_score > 0.8 else "medium" if risk_score > 0.5 else "low"

        return {
            **state,
            "risk_level": risk_level,
            "decision_factors": ["risk_assessment"]
        }

    # Level 2: Priority Classification
    def classify_priority(state: DecisionState) -> DecisionState:
        risk_level = state.get("risk_level", "medium")
        urgency = state.get("data", {}).get("urgency", "normal")

        if risk_level == "high" or urgency == "critical":
            priority = "urgent"
        elif risk_level == "medium" or urgency == "high":
            priority = "high"
        else:
            priority = "normal"

        return {
            **state,
            "priority": priority,
            "decision_factors": state.get("decision_factors", []) + ["priority_classification"]
        }

    # Level 3: Category Assignment
    def assign_category(state: DecisionState) -> DecisionState:
        data = state.get("data", {})
        content_type = data.get("type", "general")

        category_mapping = {
            "bug": "technical",
            "feature": "product",
            "billing": "financial",
            "support": "customer_service"
        }

        category = category_mapping.get(content_type, "general")

        return {
            **state,
            "category": category,
            "decision_factors": state.get("decision_factors", []) + ["category_assignment"]
        }

    # Level 4: Action Recommendation
    def recommend_action(state: DecisionState) -> DecisionState:
        risk_level = state.get("risk_level")
        priority = state.get("priority")
        category = state.get("category")

        # Complex decision logic
        if risk_level == "high" and priority == "urgent":
            action = "immediate_escalation"
        elif category == "financial" and priority == "high":
            action = "financial_review"
        elif risk_level == "low" and priority == "normal":
            action = "standard_processing"
        else:
            action = "supervisor_review"

        return {
            **state,
            "recommended_action": action,
            "decision_factors": state.get("decision_factors", []) + ["action_recommendation"]
        }

    # Add all nodes
    graph.add_node("assess_risk", assess_risk)
    graph.add_node("classify_priority", classify_priority)
    graph.add_node("assign_category", assign_category)
    graph.add_node("recommend_action", recommend_action)

    # Define routing functions
    def route_after_risk(state): return "classify_priority"
    def route_after_priority(state): return "assign_category"
    def route_after_category(state): return "recommend_action"

    # Set up the decision tree flow
    graph.set_entry_point("assess_risk")
    graph.add_edge("assess_risk", "classify_priority")
    graph.add_edge("classify_priority", "assign_category")
    graph.add_edge("assign_category", "recommend_action")
    graph.add_edge("recommend_action", END)

    return graph
```

### Dynamic Decision Making

```python
def create_dynamic_decision_graph() -> StateGraph:
    """Graph that makes decisions based on external factors"""

    class DynamicState(TypedDict):
        data: dict
        external_factors: dict
        market_conditions: str
        time_sensitivity: str
        resource_availability: dict
        decision: str

    graph = StateGraph(DynamicState)

    def gather_external_factors(state: DynamicState) -> DynamicState:
        """Gather external factors that influence decisions"""
        # Simulate gathering external data
        market_data = get_market_conditions()
        time_data = get_time_sensitivity(state.get("data", {}))
        resource_data = check_resource_availability()

        return {
            **state,
            "external_factors": {
                "market_conditions": market_data,
                "time_sensitivity": time_data,
                "resource_availability": resource_data
            },
            "market_conditions": market_data["condition"],
            "time_sensitivity": time_data["level"],
            "resource_availability": resource_data
        }

    def make_dynamic_decision(state: DynamicState) -> DynamicState:
        """Make decision based on multiple factors"""
        factors = state.get("external_factors", {})
        data = state.get("data", {})

        # Complex decision algorithm
        decision = calculate_optimal_decision(factors, data)

        return {
            **state,
            "decision": decision,
            "decision_factors": list(factors.keys())
        }

    # Add nodes
    graph.add_node("gather_factors", gather_external_factors)
    graph.add_node("make_decision", make_dynamic_decision)

    # Set up flow
    graph.set_entry_point("gather_factors")
    graph.add_edge("gather_factors", "make_decision")
    graph.add_edge("make_decision", END)

    return graph

def calculate_optimal_decision(factors: dict, data: dict) -> str:
    """Complex decision algorithm"""
    market_condition = factors.get("market_conditions", {}).get("condition", "neutral")
    time_sensitivity = factors.get("time_sensitivity", {}).get("level", "normal")
    resource_available = factors.get("resource_availability", {}).get("available", True)

    # Decision matrix
    if market_condition == "bull" and time_sensitivity == "high" and resource_available:
        return "aggressive_action"
    elif market_condition == "bear" and time_sensitivity == "low":
        return "conservative_approach"
    elif not resource_available:
        return "resource_optimization"
    else:
        return "balanced_approach"
```

## Complex Conditional Patterns

### Pattern Matching Conditions

```python
def create_pattern_matching_graph() -> StateGraph:
    """Graph that uses pattern matching for decisions"""

    class PatternState(TypedDict):
        input_data: dict
        matched_patterns: list
        confidence_scores: dict
        selected_action: str

    graph = StateGraph(PatternState)

    def pattern_analysis_node(state: PatternState) -> PatternState:
        """Analyze input against multiple patterns"""
        input_data = state.get("input_data", {})
        patterns = get_available_patterns()

        matched = []
        scores = {}

        for pattern in patterns:
            match_result = match_pattern(input_data, pattern)
            if match_result["matched"]:
                matched.append(pattern["name"])
                scores[pattern["name"]] = match_result["confidence"]

        return {
            **state,
            "matched_patterns": matched,
            "confidence_scores": scores
        }

    def action_selection_node(state: PatternState) -> PatternState:
        """Select action based on pattern matching results"""
        matched = state.get("matched_patterns", [])
        scores = state.get("confidence_scores", {})

        if not matched:
            action = "default_action"
        else:
            # Select highest confidence pattern
            best_pattern = max(scores.items(), key=lambda x: x[1])
            action = get_action_for_pattern(best_pattern[0])

        return {
            **state,
            "selected_action": action
        }

    # Add nodes
    graph.add_node("analyze_patterns", pattern_analysis_node)
    graph.add_node("select_action", action_selection_node)

    # Set up flow
    graph.set_entry_point("analyze_patterns")
    graph.add_edge("analyze_patterns", "select_action")
    graph.add_edge("select_action", END)

    return graph

def match_pattern(data: dict, pattern: dict) -> dict:
    """Match data against a pattern with confidence scoring"""
    # Implement pattern matching logic
    # This could use regex, fuzzy matching, ML models, etc.
    return {"matched": True, "confidence": 0.85}

def get_available_patterns() -> list:
    """Get list of available patterns"""
    return [
        {"name": "urgent_issue", "criteria": ["priority", "deadline"]},
        {"name": "customer_complaint", "criteria": ["sentiment", "category"]},
        {"name": "feature_request", "criteria": ["type", "complexity"]}
    ]
```

### Probabilistic Decision Making

```python
import random
from collections import defaultdict

def create_probabilistic_decision_graph() -> StateGraph:
    """Graph that makes probabilistic decisions"""

    class ProbabilisticState(TypedDict):
        data: dict
        decision_history: list
        probabilities: dict
        chosen_path: str
        uncertainty_level: float

    graph = StateGraph(ProbabilisticState)

    def probability_assessment_node(state: ProbabilisticState) -> ProbabilisticState:
        """Assess probabilities for different outcomes"""
        data = state.get("data", {})

        # Calculate probabilities based on historical data and current context
        probabilities = calculate_probabilities(data)

        return {
            **state,
            "probabilities": probabilities,
            "uncertainty_level": calculate_uncertainty(probabilities)
        }

    def probabilistic_decision_node(state: ProbabilisticState) -> ProbabilisticState:
        """Make decision based on calculated probabilities"""
        probabilities = state.get("probabilities", {})
        history = state.get("decision_history", [])

        # Apply decision strategy (e.g., maximize expected value)
        chosen_path = select_optimal_path(probabilities, history)

        return {
            **state,
            "chosen_path": chosen_path,
            "decision_history": history + [chosen_path]
        }

    # Add nodes
    graph.add_node("assess_probabilities", probability_assessment_node)
    graph.add_node("make_decision", probabilistic_decision_node)

    # Set up flow
    graph.set_entry_point("assess_probabilities")
    graph.add_edge("assess_probabilities", "make_decision")
    graph.add_edge("make_decision", END)

    return graph

def calculate_probabilities(data: dict) -> dict:
    """Calculate probabilities for different outcomes"""
    # This would typically use statistical models or ML predictions
    return {
        "path_a": 0.6,
        "path_b": 0.3,
        "path_c": 0.1
    }

def select_optimal_path(probabilities: dict, history: list) -> str:
    """Select optimal path based on probabilities and history"""
    # Simple strategy: choose highest probability path
    return max(probabilities.items(), key=lambda x: x[1])[0]
```

## Dynamic Graph Modification

### Runtime Graph Modification

```python
from langgraph.graph import StateGraph
import copy

class DynamicGraphManager:
    """Manager for dynamically modifying graphs at runtime"""

    def __init__(self, base_graph: StateGraph):
        self.base_graph = base_graph
        self.modifications = []

    def add_conditional_branch(self, source_node: str, condition_func, branches: dict):
        """Add a conditional branch at runtime"""
        modification = {
            "type": "add_conditional_branch",
            "source_node": source_node,
            "condition_func": condition_func,
            "branches": branches
        }
        self.modifications.append(modification)

    def add_fallback_path(self, source_node: str, fallback_node: str):
        """Add a fallback path for error handling"""
        modification = {
            "type": "add_fallback",
            "source_node": source_node,
            "fallback_node": fallback_node
        }
        self.modifications.append(modification)

    def create_modified_graph(self, state: dict) -> StateGraph:
        """Create a modified version of the graph based on current state"""
        modified_graph = copy.deepcopy(self.base_graph)

        for mod in self.modifications:
            if mod["type"] == "add_conditional_branch":
                modified_graph.add_conditional_edges(
                    mod["source_node"],
                    mod["condition_func"],
                    mod["branches"]
                )
            elif mod["type"] == "add_fallback":
                # Add fallback logic
                pass

        return modified_graph

# Usage
dynamic_manager = DynamicGraphManager(base_graph)

def adaptive_condition(state):
    """Adaptive condition based on current state"""
    performance = state.get("performance_metrics", {})
    if performance.get("success_rate", 0) > 0.9:
        return "optimized_path"
    else:
        return "standard_path"

dynamic_manager.add_conditional_branch(
    "processing_node",
    adaptive_condition,
    {
        "optimized_path": "fast_processor",
        "standard_path": "standard_processor"
    }
)
```

### Self-Modifying Graphs

```python
def create_self_modifying_graph() -> StateGraph:
    """Graph that can modify itself based on execution results"""

    class SelfModifyingState(TypedDict):
        data: dict
        execution_history: list
        learned_patterns: dict
        graph_modifications: list
        performance_metrics: dict

    graph = StateGraph(SelfModifyingState)

    def learning_node(state: SelfModifyingState) -> SelfModifyingState:
        """Learn from execution history and suggest modifications"""
        history = state.get("execution_history", [])
        current_patterns = state.get("learned_patterns", {})

        # Analyze patterns in execution
        new_patterns = analyze_execution_patterns(history)
        modifications = suggest_graph_modifications(new_patterns, current_patterns)

        return {
            **state,
            "learned_patterns": {**current_patterns, **new_patterns},
            "graph_modifications": modifications
        }

    def modification_node(state: SelfModifyingState) -> SelfModifyingState:
        """Apply suggested modifications to the graph"""
        modifications = state.get("graph_modifications", [])

        # Apply modifications (this would modify the graph structure)
        applied_mods = apply_modifications(modifications)

        return {
            **state,
            "applied_modifications": applied_mods,
            "execution_history": state.get("execution_history", []) + ["modification_applied"]
        }

    # Add nodes
    graph.add_node("learn", learning_node)
    graph.add_node("modify", modification_node)

    # Set up flow
    graph.set_entry_point("learn")
    graph.add_edge("learn", "modify")
    graph.add_edge("modify", END)

    return graph

def analyze_execution_patterns(history: list) -> dict:
    """Analyze execution history for patterns"""
    # Implement pattern analysis logic
    return {"frequent_path": "path_a", "bottleneck_node": "slow_processor"}

def suggest_graph_modifications(new_patterns: dict, existing_patterns: dict) -> list:
    """Suggest modifications based on learned patterns"""
    modifications = []

    if new_patterns.get("bottleneck_node"):
        modifications.append({
            "type": "optimize_node",
            "node": new_patterns["bottleneck_node"],
            "optimization": "parallel_processing"
        })

    return modifications
```

## Advanced Conditional Strategies

### Multi-Criteria Decision Analysis

```python
def create_mcda_graph() -> StateGraph:
    """Graph using Multi-Criteria Decision Analysis"""

    class MCDAState(TypedDict):
        alternatives: list
        criteria: list
        weights: dict
        scores: dict
        ranking: list
        best_alternative: str

    graph = StateGraph(MCDAState)

    def criteria_definition_node(state: MCDAState) -> MCDAState:
        """Define decision criteria and their weights"""
        criteria = [
            {"name": "cost", "weight": 0.3, "type": "minimize"},
            {"name": "quality", "weight": 0.4, "type": "maximize"},
            {"name": "time", "weight": 0.3, "type": "minimize"}
        ]

        weights = {c["name"]: c["weight"] for c in criteria}

        return {
            **state,
            "criteria": criteria,
            "weights": weights
        }

    def scoring_node(state: MCDAState) -> MCDAState:
        """Score alternatives against criteria"""
        alternatives = state.get("alternatives", [])
        criteria = state.get("criteria", [])
        weights = state.get("weights", {})

        scores = {}
        for alt in alternatives:
            alt_scores = {}
            weighted_sum = 0

            for criterion in criteria:
                name = criterion["name"]
                weight = weights.get(name, 0)
                score = calculate_criterion_score(alt, criterion)

                alt_scores[name] = score
                weighted_sum += score * weight

            scores[alt["name"]] = {
                "criteria_scores": alt_scores,
                "weighted_score": weighted_sum
            }

        return {
            **state,
            "scores": scores
        }

    def ranking_node(state: MCDAState) -> MCDAState:
        """Rank alternatives based on scores"""
        scores = state.get("scores", {})

        ranking = sorted(
            scores.items(),
            key=lambda x: x[1]["weighted_score"],
            reverse=True  # Higher scores first
        )

        best_alternative = ranking[0][0] if ranking else None

        return {
            **state,
            "ranking": ranking,
            "best_alternative": best_alternative
        }

    # Add nodes
    graph.add_node("define_criteria", criteria_definition_node)
    graph.add_node("score_alternatives", scoring_node)
    graph.add_node("rank_alternatives", ranking_node)

    # Set up flow
    graph.set_entry_point("define_criteria")
    graph.add_edge("define_criteria", "score_alternatives")
    graph.add_edge("score_alternatives", "rank_alternatives")
    graph.add_edge("rank_alternatives", END)

    return graph

def calculate_criterion_score(alternative: dict, criterion: dict) -> float:
    """Calculate score for a specific criterion"""
    # Implement scoring logic based on criterion type
    value = alternative.get(criterion["name"], 0)

    if criterion["type"] == "maximize":
        return min(value / 100, 1.0)  # Normalize to 0-1
    else:  # minimize
        return max(1 - (value / 100), 0.0)  # Invert and normalize
```

## Error Handling and Recovery in Conditional Logic

```python
def create_resilient_conditional_graph() -> StateGraph:
    """Graph with comprehensive error handling in conditional logic"""

    class ResilientState(TypedDict):
        data: dict
        decision_attempts: int
        fallback_used: bool
        error_history: list
        final_decision: str

    graph = StateGraph(ResilientState)

    def robust_decision_node(state: ResilientState) -> ResilientState:
        """Make decision with error handling and fallbacks"""
        attempts = state.get("decision_attempts", 0)

        try:
            decision = make_decision_with_fallbacks(state.get("data", {}), attempts)

            return {
                **state,
                "final_decision": decision,
                "decision_attempts": attempts + 1
            }

        except Exception as e:
            error_history = state.get("error_history", []) + [str(e)]

            if attempts < 3:
                # Try again with different approach
                return {
                    **state,
                    "error_history": error_history,
                    "decision_attempts": attempts + 1,
                    "fallback_used": True
                }
            else:
                # Give up and use default
                return {
                    **state,
                    "final_decision": "default_decision",
                    "error_history": error_history,
                    "decision_attempts": attempts + 1,
                    "fallback_used": True
                }

    def route_after_decision(state: ResilientState) -> str:
        """Route based on decision outcome"""
        decision = state.get("final_decision")
        fallback_used = state.get("fallback_used", False)

        if fallback_used:
            return "fallback_handler"
        elif decision == "high_priority":
            return "urgent_processor"
        elif decision == "medium_priority":
            return "standard_processor"
        else:
            return "low_priority_handler"

    # Add nodes
    graph.add_node("make_decision", robust_decision_node)
    graph.add_node("fallback_handler", lambda s: {**s, "processed_by": "fallback"})
    graph.add_node("urgent_processor", lambda s: {**s, "processed_by": "urgent"})
    graph.add_node("standard_processor", lambda s: {**s, "processed_by": "standard"})
    graph.add_node("low_priority_handler", lambda s: {**s, "processed_by": "low_priority"})

    # Set up conditional routing
    graph.set_entry_point("make_decision")
    graph.add_conditional_edges(
        "make_decision",
        route_after_decision,
        {
            "fallback_handler": "fallback_handler",
            "urgent_processor": "urgent_processor",
            "standard_processor": "standard_processor",
            "low_priority_handler": "low_priority_handler"
        }
    )

    # All paths lead to end
    graph.add_edge("fallback_handler", END)
    graph.add_edge("urgent_processor", END)
    graph.add_edge("standard_processor", END)
    graph.add_edge("low_priority_handler", END)

    return graph

def make_decision_with_fallbacks(data: dict, attempts: int) -> str:
    """Make decision with different strategies based on attempts"""
    if attempts == 0:
        # Primary decision logic
        return primary_decision_algorithm(data)
    elif attempts == 1:
        # Secondary decision logic
        return secondary_decision_algorithm(data)
    else:
        # Conservative fallback
        return conservative_decision_algorithm(data)
```

## What We've Accomplished

Fantastic! 🎉 You've mastered conditional logic in LangGraph:

1. **Basic conditional routing** - Simple decision-based routing
2. **Advanced decision trees** - Multi-level decision making
3. **Dynamic decision making** - External factor integration
4. **Pattern matching conditions** - Complex pattern-based routing
5. **Probabilistic decisions** - Uncertainty-aware decision making
6. **Dynamic graph modification** - Runtime graph adaptation
7. **Self-modifying graphs** - Learning and self-improvement
8. **Multi-criteria decision analysis** - Sophisticated decision frameworks
9. **Resilient conditional logic** - Error handling and recovery

## Next Steps

Ready to coordinate multiple agents? In [Chapter 5: Multi-Agent Systems](05-multi-agent-systems.md), we'll explore building systems with multiple interacting AI agents!

---

**Practice what you've learned:**
1. Build a decision tree for a complex business process
2. Implement probabilistic routing in your graph
3. Create a self-modifying graph that learns from execution
4. Add multi-criteria decision analysis to a real application
5. Build resilient conditional logic with comprehensive error handling

*What's the most sophisticated decision system you'll build?* 🤔

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `state`, `graph`, `dict` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 4: Conditional Logic` as an operating subsystem inside **LangGraph Tutorial: Building Stateful Multi-Actor Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `add_node`, `add_edge`, `decision` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 4: Conditional Logic` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `state`.
2. **Input normalization**: shape incoming data so `graph` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `dict`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langgraph)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `state` and `graph` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 3: Nodes and Edges](03-nodes-edges.md)
- [Next Chapter: Chapter 5: Multi-Agent Systems](05-multi-agent-systems.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
