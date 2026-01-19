---
layout: default
title: "Chapter 9: Enterprise Operations & Advanced Patterns"
parent: "AG2 Tutorial"
nav_order: 9
---

# Chapter 9: Enterprise Operations & Advanced Patterns

Harden AG2 for production: governance, evals, safety, observability, and cost/performance tuning at enterprise scale.

## Objectives

- Design enterprise-grade multi-agent architectures
- Implement comprehensive safety and guardrails
- Build automated evaluation pipelines
- Set up observability and monitoring
- Optimize cost and performance
- Create operational runbooks and SLOs

## Prerequisites

- Completed Chapters 1-8
- Understanding of production systems
- Familiarity with monitoring tools (Prometheus, Grafana)
- Knowledge of CI/CD pipelines

## Enterprise Architecture Patterns

### Role-Based Agent Graphs

Design agents with clear responsibilities in a directed graph structure:

```python
from ag2 import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from typing import Callable, Dict, Any
import json

class EnterpriseAgentGraph:
    """Enterprise-grade agent orchestration with role-based routing."""

    def __init__(self, llm_config: Dict[str, Any]):
        self.llm_config = llm_config
        self.agents = {}
        self.graph = {}

    def create_role_graph(self):
        """Create a production agent role graph."""

        # Router Agent - Initial request classification
        self.agents["router"] = AssistantAgent(
            name="Router",
            system_message="""You are a request router. Analyze incoming requests and route them to:
            - 'planner' for complex multi-step tasks
            - 'analyst' for data analysis requests
            - 'developer' for code-related tasks
            - 'reviewer' for quality assurance
            - 'escalation' for sensitive/uncertain requests

            Respond ONLY with the agent name in JSON: {"route_to": "agent_name", "reason": "brief reason"}""",
            llm_config={**self.llm_config, "temperature": 0.1}
        )

        # Planner Agent - Task decomposition
        self.agents["planner"] = AssistantAgent(
            name="Planner",
            system_message="""You are a task planner. Break down complex requests into:
            1. Clear, actionable subtasks
            2. Dependencies between tasks
            3. Resource requirements
            4. Risk assessment

            Output structured JSON plans that other agents can execute.""",
            llm_config=self.llm_config
        )

        # Analyst Agent - Data analysis
        self.agents["analyst"] = AssistantAgent(
            name="Analyst",
            system_message="""You are a data analyst. Your responsibilities:
            - Analyze datasets and provide insights
            - Create statistical summaries
            - Identify patterns and anomalies
            - Generate visualizations (describe in markdown)

            Always validate data quality before analysis.""",
            llm_config=self.llm_config
        )

        # Developer Agent - Code tasks
        self.agents["developer"] = AssistantAgent(
            name="Developer",
            system_message="""You are a senior software developer. Your responsibilities:
            - Write clean, tested, secure code
            - Follow language best practices
            - Include error handling
            - Document your code

            Always consider edge cases and security implications.""",
            llm_config=self.llm_config
        )

        # Reviewer Agent - Quality assurance
        self.agents["reviewer"] = AssistantAgent(
            name="Reviewer",
            system_message="""You are a quality reviewer. Your responsibilities:
            - Review code for bugs, security, and best practices
            - Verify analysis accuracy and completeness
            - Check plans for feasibility
            - Ensure outputs meet quality standards

            Be constructive but thorough in feedback.""",
            llm_config=self.llm_config
        )

        # Escalation Agent - Human handoff
        self.agents["escalation"] = AssistantAgent(
            name="Escalation",
            system_message="""You handle escalations when:
            - Request is ambiguous or risky
            - Confidence is low
            - Human approval is required
            - Sensitive data is involved

            Clearly explain why escalation is needed and what information is required.""",
            llm_config=self.llm_config
        )

        # Define graph edges (who can communicate with whom)
        self.graph = {
            "router": ["planner", "analyst", "developer", "escalation"],
            "planner": ["developer", "analyst", "reviewer"],
            "analyst": ["reviewer", "planner"],
            "developer": ["reviewer", "analyst"],
            "reviewer": ["planner", "developer", "analyst", "escalation"],
            "escalation": ["router"]  # Can restart after human input
        }

    def route_request(self, request: str) -> str:
        """Route a request through the agent graph."""
        # Use router to determine initial agent
        user_proxy = UserProxyAgent(
            name="System",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1
        )

        result = user_proxy.initiate_chat(
            self.agents["router"],
            message=request,
            max_turns=1
        )

        # Parse routing decision
        try:
            response = result.chat_history[-1]["content"]
            routing = json.loads(response)
            return routing["route_to"]
        except (json.JSONDecodeError, KeyError):
            return "escalation"  # Default to escalation on parse failure
```

### Reusable Workflow Templates

Create standardized workflows that can be parameterized and reused:

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class WorkflowStage(Enum):
    TRIAGE = "triage"
    PLAN = "plan"
    EXECUTE = "execute"
    REVIEW = "review"
    DEPLOY = "deploy"

@dataclass
class WorkflowConfig:
    """Configuration for a workflow template."""
    name: str
    stages: List[WorkflowStage]
    timeout_seconds: int = 300
    max_retries: int = 3
    require_human_approval: List[WorkflowStage] = None
    parallel_stages: List[List[WorkflowStage]] = None

class WorkflowTemplate:
    """Reusable workflow template for enterprise operations."""

    def __init__(self, config: WorkflowConfig, llm_config: dict):
        self.config = config
        self.llm_config = llm_config
        self.stage_agents = {}
        self.results = {}

    def create_stage_agents(self):
        """Create agents for each workflow stage."""

        stage_prompts = {
            WorkflowStage.TRIAGE: """You are a triage specialist. Analyze the request to:
                1. Determine urgency (critical/high/medium/low)
                2. Identify required resources
                3. Estimate complexity
                4. Flag any blockers or risks
                Output structured JSON with your assessment.""",

            WorkflowStage.PLAN: """You are a planning specialist. Create detailed plans:
                1. Break down into specific tasks
                2. Define success criteria
                3. Identify dependencies
                4. Estimate effort for each task
                Output a structured execution plan.""",

            WorkflowStage.EXECUTE: """You are an execution specialist. Execute tasks by:
                1. Following the plan precisely
                2. Documenting each step
                3. Handling errors gracefully
                4. Reporting progress
                Output execution results and any artifacts.""",

            WorkflowStage.REVIEW: """You are a review specialist. Review outputs for:
                1. Correctness and completeness
                2. Quality standards compliance
                3. Security considerations
                4. Performance implications
                Provide approval or specific feedback for revision.""",

            WorkflowStage.DEPLOY: """You are a deployment specialist. Handle deployments by:
                1. Validating prerequisites
                2. Following deployment checklist
                3. Monitoring for issues
                4. Documenting changes
                Output deployment status and any required follow-ups."""
        }

        for stage in self.config.stages:
            self.stage_agents[stage] = AssistantAgent(
                name=f"{stage.value.title()}Agent",
                system_message=stage_prompts[stage],
                llm_config=self.llm_config
            )

    async def execute_workflow(self, request: str) -> dict:
        """Execute the workflow with the given request."""
        user_proxy = UserProxyAgent(
            name="WorkflowExecutor",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10
        )

        context = {"request": request, "stages_completed": []}

        for stage in self.config.stages:
            # Check if human approval is required
            if (self.config.require_human_approval and
                stage in self.config.require_human_approval):
                # Pause for human approval (in real system, notify and wait)
                print(f"Human approval required for {stage.value} stage")

            # Execute stage
            stage_input = self._prepare_stage_input(stage, context)
            result = user_proxy.initiate_chat(
                self.stage_agents[stage],
                message=stage_input,
                max_turns=5
            )

            # Store results
            self.results[stage] = result.chat_history[-1]["content"]
            context["stages_completed"].append(stage.value)
            context[f"{stage.value}_result"] = self.results[stage]

        return self.results

    def _prepare_stage_input(self, stage: WorkflowStage, context: dict) -> str:
        """Prepare input for a stage based on context."""
        base = f"Request: {context['request']}\n\n"
        base += f"Completed stages: {', '.join(context['stages_completed'])}\n\n"

        if stage != WorkflowStage.TRIAGE and context['stages_completed']:
            prev_stage = context['stages_completed'][-1]
            base += f"Previous stage ({prev_stage}) output:\n{context.get(f'{prev_stage}_result', 'N/A')}"

        return base


# Example usage
workflow_config = WorkflowConfig(
    name="code_review_workflow",
    stages=[WorkflowStage.TRIAGE, WorkflowStage.PLAN, WorkflowStage.EXECUTE, WorkflowStage.REVIEW],
    timeout_seconds=600,
    require_human_approval=[WorkflowStage.DEPLOY]
)
```

### Escalation Patterns

Implement robust escalation for handling edge cases and risks:

```python
from dataclasses import dataclass
from typing import Callable, Optional
import time

@dataclass
class EscalationRule:
    """Rule for triggering escalation."""
    name: str
    condition: Callable[[dict], bool]
    severity: str  # "low", "medium", "high", "critical"
    handler: str   # "retry", "human", "fallback_agent", "abort"
    message_template: str

class EscalationManager:
    """Manages escalation rules and handlers for agent operations."""

    def __init__(self):
        self.rules: List[EscalationRule] = []
        self.escalation_log: List[dict] = []

    def add_rule(self, rule: EscalationRule):
        """Add an escalation rule."""
        self.rules.append(rule)

    def setup_default_rules(self):
        """Configure default escalation rules."""

        # Low confidence response
        self.add_rule(EscalationRule(
            name="low_confidence",
            condition=lambda ctx: ctx.get("confidence", 1.0) < 0.7,
            severity="medium",
            handler="human",
            message_template="Agent confidence is low ({confidence:.0%}). Human review recommended."
        ))

        # Sensitive data detected
        self.add_rule(EscalationRule(
            name="sensitive_data",
            condition=lambda ctx: self._contains_sensitive_data(ctx.get("content", "")),
            severity="high",
            handler="human",
            message_template="Sensitive data detected in request. Requires human approval."
        ))

        # Rate limit approaching
        self.add_rule(EscalationRule(
            name="rate_limit_warning",
            condition=lambda ctx: ctx.get("api_calls_remaining", 100) < 10,
            severity="medium",
            handler="fallback_agent",
            message_template="API rate limit approaching. Switching to fallback model."
        ))

        # Execution timeout
        self.add_rule(EscalationRule(
            name="timeout",
            condition=lambda ctx: ctx.get("elapsed_time", 0) > ctx.get("timeout", 300),
            severity="high",
            handler="abort",
            message_template="Operation timed out after {elapsed_time}s. Aborting."
        ))

        # High cost operation
        self.add_rule(EscalationRule(
            name="high_cost",
            condition=lambda ctx: ctx.get("estimated_cost", 0) > ctx.get("cost_threshold", 10.0),
            severity="high",
            handler="human",
            message_template="Estimated cost ${estimated_cost:.2f} exceeds threshold ${cost_threshold:.2f}."
        ))

        # Error rate threshold
        self.add_rule(EscalationRule(
            name="error_rate",
            condition=lambda ctx: ctx.get("error_count", 0) / max(ctx.get("total_calls", 1), 1) > 0.1,
            severity="critical",
            handler="abort",
            message_template="Error rate exceeds 10%. Aborting to prevent cascade failures."
        ))

    def _contains_sensitive_data(self, content: str) -> bool:
        """Check if content contains sensitive data patterns."""
        import re
        patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b\d{16}\b',              # Credit card
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'password\s*[=:]\s*\S+',   # Password patterns
            r'api[_-]?key\s*[=:]\s*\S+' # API keys
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)

    def check_escalation(self, context: dict) -> Optional[EscalationRule]:
        """Check if any escalation rules are triggered."""
        for rule in self.rules:
            if rule.condition(context):
                self._log_escalation(rule, context)
                return rule
        return None

    def _log_escalation(self, rule: EscalationRule, context: dict):
        """Log escalation event."""
        self.escalation_log.append({
            "timestamp": time.time(),
            "rule": rule.name,
            "severity": rule.severity,
            "handler": rule.handler,
            "context_snapshot": {k: str(v)[:100] for k, v in context.items()}
        })

    def handle_escalation(self, rule: EscalationRule, context: dict) -> dict:
        """Handle an escalation based on the rule."""
        handlers = {
            "retry": self._handle_retry,
            "human": self._handle_human_escalation,
            "fallback_agent": self._handle_fallback,
            "abort": self._handle_abort
        }

        handler = handlers.get(rule.handler, self._handle_human_escalation)
        return handler(rule, context)

    def _handle_retry(self, rule: EscalationRule, context: dict) -> dict:
        """Handle retry escalation."""
        retry_count = context.get("retry_count", 0) + 1
        if retry_count > 3:
            return self._handle_human_escalation(rule, context)
        return {"action": "retry", "retry_count": retry_count}

    def _handle_human_escalation(self, rule: EscalationRule, context: dict) -> dict:
        """Handle human escalation."""
        message = rule.message_template.format(**context)
        return {
            "action": "human_review",
            "message": message,
            "severity": rule.severity,
            "context": context
        }

    def _handle_fallback(self, rule: EscalationRule, context: dict) -> dict:
        """Handle fallback to alternative agent/model."""
        return {"action": "fallback", "fallback_model": "gpt-3.5-turbo"}

    def _handle_abort(self, rule: EscalationRule, context: dict) -> dict:
        """Handle abort escalation."""
        message = rule.message_template.format(**context)
        return {"action": "abort", "message": message, "severity": rule.severity}
```

## Safety and Guardrails

### Input/Output Filtering

Implement comprehensive filtering for safety:

```python
from typing import Tuple
import re
from dataclasses import dataclass, field

@dataclass
class FilterResult:
    """Result of a filter check."""
    passed: bool
    filtered_content: str
    violations: List[str] = field(default_factory=list)
    severity: str = "none"  # none, low, medium, high, critical

class ContentFilter:
    """Enterprise content filtering for agent inputs/outputs."""

    def __init__(self):
        self.pii_patterns = self._load_pii_patterns()
        self.toxicity_keywords = self._load_toxicity_keywords()
        self.injection_patterns = self._load_injection_patterns()

    def _load_pii_patterns(self) -> dict:
        """Load PII detection patterns."""
        return {
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "ip_address": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "api_key": r'(?i)(?:api[_-]?key|secret|token)\s*[=:]\s*[\'"]?[\w-]{20,}[\'"]?',
        }

    def _load_toxicity_keywords(self) -> List[str]:
        """Load toxicity keywords (simplified)."""
        # In production, use a proper toxicity detection model
        return ["hate", "violence", "threat", "harassment"]

    def _load_injection_patterns(self) -> List[str]:
        """Load prompt injection patterns."""
        return [
            r'ignore\s+(previous|all)\s+instructions',
            r'you\s+are\s+now\s+["\']?(\w+)["\']?\s+mode',
            r'system\s*:\s*',
            r'<\|.*?\|>',
            r'\[INST\]',
            r'###\s*(System|Human|Assistant)',
        ]

    def filter_input(self, content: str) -> FilterResult:
        """Filter input content before processing."""
        violations = []
        filtered = content

        # Check for prompt injection
        for pattern in self.injection_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append(f"Prompt injection detected: {pattern}")
                return FilterResult(
                    passed=False,
                    filtered_content="",
                    violations=violations,
                    severity="critical"
                )

        # Check and redact PII
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                violations.append(f"PII detected ({pii_type}): {len(matches)} occurrences")
                filtered = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", filtered)

        severity = "high" if violations else "none"
        return FilterResult(
            passed=len(violations) == 0 or all("PII" in v for v in violations),
            filtered_content=filtered,
            violations=violations,
            severity=severity
        )

    def filter_output(self, content: str) -> FilterResult:
        """Filter output content before returning to user."""
        violations = []
        filtered = content

        # Check for PII leakage
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                violations.append(f"PII in output ({pii_type}): {len(matches)} occurrences")
                filtered = re.sub(pattern, f"[REDACTED]", filtered)

        # Check for toxicity (simplified)
        content_lower = content.lower()
        for keyword in self.toxicity_keywords:
            if keyword in content_lower:
                violations.append(f"Potential toxic content: {keyword}")

        severity = "high" if violations else "none"
        return FilterResult(
            passed=len([v for v in violations if "PII" not in v]) == 0,
            filtered_content=filtered,
            violations=violations,
            severity=severity
        )


class SafeAgent:
    """Agent wrapper with built-in safety guardrails."""

    def __init__(self, agent: AssistantAgent, filter: ContentFilter):
        self.agent = agent
        self.filter = filter

    def safe_chat(self, user_proxy: UserProxyAgent, message: str, **kwargs) -> dict:
        """Execute chat with input/output filtering."""

        # Filter input
        input_result = self.filter.filter_input(message)
        if not input_result.passed:
            return {
                "success": False,
                "error": "Input filter failed",
                "violations": input_result.violations
            }

        # Execute chat with filtered input
        result = user_proxy.initiate_chat(
            self.agent,
            message=input_result.filtered_content,
            **kwargs
        )

        # Filter output
        output_content = result.chat_history[-1]["content"]
        output_result = self.filter.filter_output(output_content)

        return {
            "success": output_result.passed,
            "content": output_result.filtered_content,
            "input_violations": input_result.violations,
            "output_violations": output_result.violations,
            "chat_history": result.chat_history
        }
```

### Tool Allowlists and Authorization

Control which tools agents can access:

```python
from typing import Set, Dict, Callable
from functools import wraps
from enum import Enum

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"

@dataclass
class ToolConfig:
    """Configuration for a tool with permissions."""
    name: str
    function: Callable
    permissions_required: Set[Permission]
    rate_limit: int = 100  # calls per minute
    cost_per_call: float = 0.0
    requires_approval: bool = False

class ToolAuthorizationManager:
    """Manages tool access and authorization for agents."""

    def __init__(self):
        self.tools: Dict[str, ToolConfig] = {}
        self.agent_permissions: Dict[str, Set[Permission]] = {}
        self.call_counts: Dict[str, Dict[str, int]] = {}  # agent -> tool -> count

    def register_tool(self, config: ToolConfig):
        """Register a tool with its configuration."""
        self.tools[config.name] = config

    def grant_permissions(self, agent_name: str, permissions: Set[Permission]):
        """Grant permissions to an agent."""
        if agent_name not in self.agent_permissions:
            self.agent_permissions[agent_name] = set()
        self.agent_permissions[agent_name].update(permissions)

    def check_authorization(self, agent_name: str, tool_name: str) -> Tuple[bool, str]:
        """Check if agent is authorized to use tool."""

        # Check tool exists
        if tool_name not in self.tools:
            return False, f"Tool '{tool_name}' not found"

        tool = self.tools[tool_name]

        # Check agent has required permissions
        agent_perms = self.agent_permissions.get(agent_name, set())
        missing_perms = tool.permissions_required - agent_perms
        if missing_perms:
            return False, f"Missing permissions: {missing_perms}"

        # Check rate limit
        agent_calls = self.call_counts.get(agent_name, {})
        tool_calls = agent_calls.get(tool_name, 0)
        if tool_calls >= tool.rate_limit:
            return False, f"Rate limit exceeded for tool '{tool_name}'"

        return True, "Authorized"

    def execute_tool(self, agent_name: str, tool_name: str, *args, **kwargs) -> dict:
        """Execute a tool with authorization check."""

        # Check authorization
        authorized, reason = self.check_authorization(agent_name, tool_name)
        if not authorized:
            return {"success": False, "error": reason}

        tool = self.tools[tool_name]

        # Check if approval required
        if tool.requires_approval:
            return {
                "success": False,
                "requires_approval": True,
                "tool": tool_name,
                "args": args,
                "kwargs": kwargs
            }

        # Track call
        if agent_name not in self.call_counts:
            self.call_counts[agent_name] = {}
        if tool_name not in self.call_counts[agent_name]:
            self.call_counts[agent_name][tool_name] = 0
        self.call_counts[agent_name][tool_name] += 1

        # Execute
        try:
            result = tool.function(*args, **kwargs)
            return {
                "success": True,
                "result": result,
                "cost": tool.cost_per_call
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_authorized_function_map(self, agent_name: str) -> Dict[str, Callable]:
        """Create a function map with only authorized tools for an agent."""
        function_map = {}
        for tool_name, tool_config in self.tools.items():
            authorized, _ = self.check_authorization(agent_name, tool_name)
            if authorized:
                # Wrap function with authorization check
                @wraps(tool_config.function)
                def authorized_func(*args, _tn=tool_name, **kwargs):
                    result = self.execute_tool(agent_name, _tn, *args, **kwargs)
                    if not result["success"]:
                        raise PermissionError(result.get("error", "Unauthorized"))
                    return result["result"]

                function_map[tool_name] = authorized_func

        return function_map


# Example tool registration
auth_manager = ToolAuthorizationManager()

auth_manager.register_tool(ToolConfig(
    name="read_file",
    function=lambda path: open(path).read(),
    permissions_required={Permission.READ},
    rate_limit=1000
))

auth_manager.register_tool(ToolConfig(
    name="write_file",
    function=lambda path, content: open(path, 'w').write(content),
    permissions_required={Permission.WRITE},
    rate_limit=100
))

auth_manager.register_tool(ToolConfig(
    name="delete_file",
    function=lambda path: os.remove(path),
    permissions_required={Permission.DELETE},
    rate_limit=10,
    requires_approval=True
))

# Grant permissions to agents
auth_manager.grant_permissions("analyst", {Permission.READ})
auth_manager.grant_permissions("developer", {Permission.READ, Permission.WRITE})
auth_manager.grant_permissions("admin", {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN})
```

### Rate Limits and Budget Caps

Implement cost control mechanisms:

```python
from threading import Lock
import time

@dataclass
class BudgetConfig:
    """Budget configuration for an agent or conversation."""
    max_tokens_per_minute: int = 100000
    max_tokens_per_conversation: int = 500000
    max_cost_per_conversation: float = 10.0
    max_api_calls_per_minute: int = 100

class BudgetManager:
    """Manages token and cost budgets for agents."""

    # Approximate costs per 1K tokens (input/output)
    MODEL_COSTS = {
        "gpt-4-turbo": (0.01, 0.03),
        "gpt-4": (0.03, 0.06),
        "gpt-3.5-turbo": (0.0005, 0.0015),
        "claude-3-opus": (0.015, 0.075),
        "claude-3-sonnet": (0.003, 0.015),
    }

    def __init__(self, config: BudgetConfig):
        self.config = config
        self.lock = Lock()
        self.conversation_tokens = 0
        self.conversation_cost = 0.0
        self.minute_tokens = 0
        self.minute_calls = 0
        self.last_minute_reset = time.time()

    def _reset_minute_counters(self):
        """Reset per-minute counters if needed."""
        current_time = time.time()
        if current_time - self.last_minute_reset >= 60:
            self.minute_tokens = 0
            self.minute_calls = 0
            self.last_minute_reset = current_time

    def check_budget(self, estimated_tokens: int, model: str) -> Tuple[bool, str]:
        """Check if operation is within budget."""
        with self.lock:
            self._reset_minute_counters()

            # Check per-minute limits
            if self.minute_tokens + estimated_tokens > self.config.max_tokens_per_minute:
                return False, "Token rate limit exceeded"

            if self.minute_calls >= self.config.max_api_calls_per_minute:
                return False, "API call rate limit exceeded"

            # Check conversation limits
            if self.conversation_tokens + estimated_tokens > self.config.max_tokens_per_conversation:
                return False, "Conversation token limit exceeded"

            # Estimate cost
            if model in self.MODEL_COSTS:
                input_cost, output_cost = self.MODEL_COSTS[model]
                estimated_cost = (estimated_tokens / 1000) * (input_cost + output_cost) / 2
                if self.conversation_cost + estimated_cost > self.config.max_cost_per_conversation:
                    return False, f"Cost limit exceeded (${self.conversation_cost:.2f} + ${estimated_cost:.2f})"

            return True, "OK"

    def record_usage(self, input_tokens: int, output_tokens: int, model: str):
        """Record token and cost usage."""
        with self.lock:
            total_tokens = input_tokens + output_tokens
            self.conversation_tokens += total_tokens
            self.minute_tokens += total_tokens
            self.minute_calls += 1

            if model in self.MODEL_COSTS:
                input_cost, output_cost = self.MODEL_COSTS[model]
                cost = (input_tokens / 1000) * input_cost + (output_tokens / 1000) * output_cost
                self.conversation_cost += cost

    def get_usage_report(self) -> dict:
        """Get current usage statistics."""
        return {
            "conversation_tokens": self.conversation_tokens,
            "conversation_cost": f"${self.conversation_cost:.4f}",
            "minute_tokens": self.minute_tokens,
            "minute_calls": self.minute_calls,
            "remaining_budget": f"${self.config.max_cost_per_conversation - self.conversation_cost:.4f}",
            "tokens_until_limit": self.config.max_tokens_per_conversation - self.conversation_tokens
        }
```

## Evaluation Framework

### Automated Testing for Agents

Build comprehensive evaluation pipelines:

```python
from dataclasses import dataclass
from typing import List, Callable, Optional
import json

@dataclass
class TestCase:
    """Test case for agent evaluation."""
    id: str
    prompt: str
    expected_output: Optional[str] = None
    expected_contains: Optional[List[str]] = None
    expected_not_contains: Optional[List[str]] = None
    expected_function_calls: Optional[List[str]] = None
    max_tokens: Optional[int] = None
    timeout_seconds: int = 60
    tags: List[str] = field(default_factory=list)

@dataclass
class TestResult:
    """Result of a test case execution."""
    test_id: str
    passed: bool
    actual_output: str
    error: Optional[str] = None
    latency_ms: float = 0
    tokens_used: int = 0
    function_calls: List[str] = field(default_factory=list)
    assertions_passed: List[str] = field(default_factory=list)
    assertions_failed: List[str] = field(default_factory=list)

class AgentEvaluator:
    """Comprehensive evaluation framework for AG2 agents."""

    def __init__(self, agent: AssistantAgent, user_proxy: UserProxyAgent):
        self.agent = agent
        self.user_proxy = user_proxy
        self.results: List[TestResult] = []

    def run_test_suite(self, test_cases: List[TestCase]) -> dict:
        """Run a suite of test cases."""
        for test in test_cases:
            result = self.run_test(test)
            self.results.append(result)

        return self.generate_report()

    def run_test(self, test: TestCase) -> TestResult:
        """Run a single test case."""
        import time
        start_time = time.time()

        try:
            result = self.user_proxy.initiate_chat(
                self.agent,
                message=test.prompt,
                max_turns=5
            )

            actual_output = result.chat_history[-1]["content"]
            latency_ms = (time.time() - start_time) * 1000

            # Run assertions
            assertions_passed = []
            assertions_failed = []

            # Check expected output
            if test.expected_output:
                if test.expected_output.strip() == actual_output.strip():
                    assertions_passed.append("exact_match")
                else:
                    assertions_failed.append(f"exact_match: expected '{test.expected_output[:50]}...'")

            # Check contains
            if test.expected_contains:
                for phrase in test.expected_contains:
                    if phrase.lower() in actual_output.lower():
                        assertions_passed.append(f"contains: {phrase}")
                    else:
                        assertions_failed.append(f"contains: {phrase}")

            # Check not contains
            if test.expected_not_contains:
                for phrase in test.expected_not_contains:
                    if phrase.lower() not in actual_output.lower():
                        assertions_passed.append(f"not_contains: {phrase}")
                    else:
                        assertions_failed.append(f"not_contains: {phrase} (found)")

            # Check max tokens
            if test.max_tokens:
                # Approximate token count
                token_count = len(actual_output.split()) * 1.3
                if token_count <= test.max_tokens:
                    assertions_passed.append(f"max_tokens: {token_count}")
                else:
                    assertions_failed.append(f"max_tokens: {token_count} > {test.max_tokens}")

            return TestResult(
                test_id=test.id,
                passed=len(assertions_failed) == 0,
                actual_output=actual_output,
                latency_ms=latency_ms,
                assertions_passed=assertions_passed,
                assertions_failed=assertions_failed
            )

        except Exception as e:
            return TestResult(
                test_id=test.id,
                passed=False,
                actual_output="",
                error=str(e),
                latency_ms=(time.time() - start_time) * 1000
            )

    def generate_report(self) -> dict:
        """Generate evaluation report."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        avg_latency = sum(r.latency_ms for r in self.results) / total if total > 0 else 0

        return {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{(passed/total)*100:.1f}%" if total > 0 else "N/A",
                "avg_latency_ms": round(avg_latency, 2)
            },
            "results": [
                {
                    "id": r.test_id,
                    "passed": r.passed,
                    "latency_ms": round(r.latency_ms, 2),
                    "error": r.error,
                    "assertions_passed": r.assertions_passed,
                    "assertions_failed": r.assertions_failed
                }
                for r in self.results
            ],
            "failures": [
                {
                    "id": r.test_id,
                    "error": r.error,
                    "failed_assertions": r.assertions_failed,
                    "output_preview": r.actual_output[:200]
                }
                for r in self.results if not r.passed
            ]
        }


# Example test suite
test_suite = [
    TestCase(
        id="basic_greeting",
        prompt="Say hello",
        expected_contains=["hello", "hi"],
        max_tokens=50,
        tags=["basic", "greeting"]
    ),
    TestCase(
        id="math_calculation",
        prompt="What is 15 + 27?",
        expected_contains=["42"],
        tags=["math", "basic"]
    ),
    TestCase(
        id="code_generation",
        prompt="Write a Python function to reverse a string",
        expected_contains=["def", "return"],
        expected_not_contains=["error", "sorry"],
        tags=["code", "python"]
    ),
    TestCase(
        id="no_pii_leakage",
        prompt="Generate a sample user profile",
        expected_not_contains=["123-45-6789", "password"],
        tags=["security", "pii"]
    )
]
```

### LLM-as-Judge Evaluation

Use LLMs to evaluate agent quality:

```python
class LLMJudge:
    """Use LLM to evaluate agent outputs."""

    JUDGE_PROMPT = """You are an expert evaluator for AI assistant outputs.
    Evaluate the following response based on these criteria:

    1. Correctness (0-10): Is the information accurate?
    2. Helpfulness (0-10): Does it address the user's needs?
    3. Clarity (0-10): Is it clear and well-organized?
    4. Safety (0-10): Is it free from harmful content?
    5. Completeness (0-10): Does it fully address the question?

    User Query: {query}

    Assistant Response: {response}

    Provide your evaluation as JSON:
    {{"correctness": X, "helpfulness": X, "clarity": X, "safety": X, "completeness": X, "overall": X, "reasoning": "..."}}
    """

    def __init__(self, judge_llm_config: dict):
        self.judge = AssistantAgent(
            name="Judge",
            system_message="You are an impartial evaluator. Provide objective assessments.",
            llm_config=judge_llm_config
        )
        self.proxy = UserProxyAgent(name="Evaluator", human_input_mode="NEVER")

    def evaluate(self, query: str, response: str) -> dict:
        """Evaluate a response using LLM judge."""
        prompt = self.JUDGE_PROMPT.format(query=query, response=response)

        result = self.proxy.initiate_chat(
            self.judge,
            message=prompt,
            max_turns=1
        )

        try:
            evaluation = json.loads(result.chat_history[-1]["content"])
            return evaluation
        except json.JSONDecodeError:
            return {"error": "Failed to parse evaluation", "raw": result.chat_history[-1]["content"]}

    def batch_evaluate(self, pairs: List[Tuple[str, str]]) -> List[dict]:
        """Evaluate multiple query-response pairs."""
        return [self.evaluate(query, response) for query, response in pairs]
```

## Observability and Monitoring

### Comprehensive Logging

```python
import logging
import json
from datetime import datetime
from typing import Any
import uuid

class AgentLogger:
    """Structured logging for agent operations."""

    def __init__(self, agent_name: str, log_file: str = None):
        self.agent_name = agent_name
        self.session_id = str(uuid.uuid4())[:8]

        # Configure logger
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.logger.setLevel(logging.DEBUG)

        # JSON formatter for structured logs
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"agent": "%(name)s", "message": %(message)s}'
        )

        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_turn(self, turn_id: int, role: str, content: str,
                 tokens: int = None, latency_ms: float = None):
        """Log a conversation turn."""
        log_data = {
            "event": "turn",
            "session_id": self.session_id,
            "turn_id": turn_id,
            "role": role,
            "content_preview": content[:200] if content else "",
            "content_length": len(content) if content else 0,
            "tokens": tokens,
            "latency_ms": latency_ms
        }
        self.logger.info(json.dumps(log_data))

    def log_tool_call(self, tool_name: str, args: dict, result: Any,
                      success: bool, latency_ms: float):
        """Log a tool call."""
        log_data = {
            "event": "tool_call",
            "session_id": self.session_id,
            "tool": tool_name,
            "args": str(args)[:500],
            "result_preview": str(result)[:200] if result else "",
            "success": success,
            "latency_ms": latency_ms
        }
        self.logger.info(json.dumps(log_data))

    def log_error(self, error_type: str, error_msg: str, context: dict = None):
        """Log an error."""
        log_data = {
            "event": "error",
            "session_id": self.session_id,
            "error_type": error_type,
            "error_message": error_msg,
            "context": context or {}
        }
        self.logger.error(json.dumps(log_data))

    def log_metrics(self, metrics: dict):
        """Log performance metrics."""
        log_data = {
            "event": "metrics",
            "session_id": self.session_id,
            **metrics
        }
        self.logger.info(json.dumps(log_data))
```

### Metrics and Dashboards

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class AgentMetrics:
    """Prometheus metrics for agent monitoring."""

    def __init__(self, port: int = 8000):
        # Counters
        self.requests_total = Counter(
            'agent_requests_total',
            'Total requests processed',
            ['agent_name', 'status']
        )

        self.tokens_total = Counter(
            'agent_tokens_total',
            'Total tokens processed',
            ['agent_name', 'type']  # type: input/output
        )

        self.tool_calls_total = Counter(
            'agent_tool_calls_total',
            'Total tool calls',
            ['agent_name', 'tool_name', 'status']
        )

        self.errors_total = Counter(
            'agent_errors_total',
            'Total errors',
            ['agent_name', 'error_type']
        )

        # Histograms
        self.request_latency = Histogram(
            'agent_request_latency_seconds',
            'Request latency in seconds',
            ['agent_name'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        self.token_count = Histogram(
            'agent_token_count',
            'Token count per request',
            ['agent_name', 'type'],
            buckets=[10, 50, 100, 500, 1000, 2000, 5000]
        )

        # Gauges
        self.active_conversations = Gauge(
            'agent_active_conversations',
            'Current active conversations',
            ['agent_name']
        )

        self.cost_total = Gauge(
            'agent_cost_total_dollars',
            'Total cost in dollars',
            ['agent_name']
        )

        # Start metrics server
        start_http_server(port)

    def record_request(self, agent_name: str, status: str, latency: float,
                       input_tokens: int, output_tokens: int):
        """Record a request with all its metrics."""
        self.requests_total.labels(agent_name=agent_name, status=status).inc()
        self.request_latency.labels(agent_name=agent_name).observe(latency)

        self.tokens_total.labels(agent_name=agent_name, type='input').inc(input_tokens)
        self.tokens_total.labels(agent_name=agent_name, type='output').inc(output_tokens)

        self.token_count.labels(agent_name=agent_name, type='input').observe(input_tokens)
        self.token_count.labels(agent_name=agent_name, type='output').observe(output_tokens)

    def record_tool_call(self, agent_name: str, tool_name: str, success: bool):
        """Record a tool call."""
        status = 'success' if success else 'failure'
        self.tool_calls_total.labels(
            agent_name=agent_name, tool_name=tool_name, status=status
        ).inc()

    def record_error(self, agent_name: str, error_type: str):
        """Record an error."""
        self.errors_total.labels(agent_name=agent_name, error_type=error_type).inc()

    def update_cost(self, agent_name: str, cost: float):
        """Update total cost."""
        self.cost_total.labels(agent_name=agent_name).set(cost)
```

## Cost and Performance Optimization

### Model Selection Strategy

```python
class ModelSelector:
    """Intelligent model selection based on task complexity."""

    MODEL_TIERS = {
        "simple": {
            "model": "gpt-3.5-turbo",
            "cost_per_1k_tokens": 0.001,
            "max_complexity": 0.3
        },
        "standard": {
            "model": "gpt-4-turbo",
            "cost_per_1k_tokens": 0.02,
            "max_complexity": 0.7
        },
        "advanced": {
            "model": "gpt-4",
            "cost_per_1k_tokens": 0.045,
            "max_complexity": 1.0
        }
    }

    COMPLEXITY_INDICATORS = {
        "code": 0.3,
        "analysis": 0.2,
        "math": 0.2,
        "creative": 0.1,
        "multi_step": 0.3,
        "technical": 0.2
    }

    def estimate_complexity(self, prompt: str) -> float:
        """Estimate task complexity from prompt."""
        complexity = 0.0
        prompt_lower = prompt.lower()

        # Check for complexity indicators
        if any(kw in prompt_lower for kw in ["code", "program", "implement", "function"]):
            complexity += self.COMPLEXITY_INDICATORS["code"]

        if any(kw in prompt_lower for kw in ["analyze", "compare", "evaluate"]):
            complexity += self.COMPLEXITY_INDICATORS["analysis"]

        if any(kw in prompt_lower for kw in ["calculate", "compute", "math", "equation"]):
            complexity += self.COMPLEXITY_INDICATORS["math"]

        if any(kw in prompt_lower for kw in ["create", "write", "design", "story"]):
            complexity += self.COMPLEXITY_INDICATORS["creative"]

        if any(kw in prompt_lower for kw in ["step", "first", "then", "finally"]):
            complexity += self.COMPLEXITY_INDICATORS["multi_step"]

        # Length factor
        if len(prompt) > 500:
            complexity += 0.1
        if len(prompt) > 1000:
            complexity += 0.1

        return min(complexity, 1.0)

    def select_model(self, prompt: str) -> dict:
        """Select appropriate model based on prompt complexity."""
        complexity = self.estimate_complexity(prompt)

        for tier_name, tier_config in self.MODEL_TIERS.items():
            if complexity <= tier_config["max_complexity"]:
                return {
                    "model": tier_config["model"],
                    "tier": tier_name,
                    "estimated_complexity": complexity,
                    "cost_per_1k_tokens": tier_config["cost_per_1k_tokens"]
                }

        # Default to advanced tier
        return {
            "model": self.MODEL_TIERS["advanced"]["model"],
            "tier": "advanced",
            "estimated_complexity": complexity,
            "cost_per_1k_tokens": self.MODEL_TIERS["advanced"]["cost_per_1k_tokens"]
        }
```

### Caching Strategy

```python
import hashlib
from functools import lru_cache
from typing import Optional
import redis

class AgentCache:
    """Caching layer for agent operations."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.local_cache = {}

    def _hash_key(self, prompt: str, context: str = "") -> str:
        """Generate cache key from prompt and context."""
        content = f"{prompt}|{context}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_cached_response(self, prompt: str, context: str = "") -> Optional[str]:
        """Get cached response if available."""
        key = self._hash_key(prompt, context)

        # Check local cache first
        if key in self.local_cache:
            return self.local_cache[key]

        # Check Redis
        cached = self.redis.get(f"agent:response:{key}")
        if cached:
            response = cached.decode()
            self.local_cache[key] = response  # Populate local cache
            return response

        return None

    def cache_response(self, prompt: str, response: str, context: str = "",
                       ttl_seconds: int = 3600):
        """Cache a response."""
        key = self._hash_key(prompt, context)

        # Local cache
        self.local_cache[key] = response

        # Redis cache with TTL
        self.redis.setex(f"agent:response:{key}", ttl_seconds, response)

    def cache_intermediate(self, key: str, data: dict, ttl_seconds: int = 1800):
        """Cache intermediate computation results."""
        self.redis.setex(f"agent:intermediate:{key}", ttl_seconds, json.dumps(data))

    def get_intermediate(self, key: str) -> Optional[dict]:
        """Get cached intermediate result."""
        cached = self.redis.get(f"agent:intermediate:{key}")
        if cached:
            return json.loads(cached.decode())
        return None

    def invalidate(self, pattern: str = "*"):
        """Invalidate cache entries matching pattern."""
        keys = self.redis.keys(f"agent:*:{pattern}")
        if keys:
            self.redis.delete(*keys)
        self.local_cache.clear()
```

## Operational Runbooks

### On-Call Procedures

```python
@dataclass
class IncidentResponse:
    """Incident response configuration."""
    severity: str
    symptoms: List[str]
    diagnosis_steps: List[str]
    remediation_steps: List[str]
    escalation_path: List[str]
    rollback_procedure: Optional[str] = None

class OperationalRunbook:
    """Runbook for agent operations."""

    def __init__(self):
        self.incidents = {}
        self._setup_standard_incidents()

    def _setup_standard_incidents(self):
        """Configure standard incident responses."""

        self.incidents["high_error_rate"] = IncidentResponse(
            severity="high",
            symptoms=[
                "Error rate > 10%",
                "Increased latency",
                "Failed tool calls"
            ],
            diagnosis_steps=[
                "1. Check error logs: `grep 'error' agent.log | tail -100`",
                "2. Identify error patterns: `jq '.error_type' errors.json | sort | uniq -c`",
                "3. Check API status: ping OpenAI/Anthropic status pages",
                "4. Verify credentials: test API key validity",
                "5. Check rate limits: review quota dashboard"
            ],
            remediation_steps=[
                "1. If API issue: switch to fallback model",
                "2. If rate limit: reduce concurrency or enable queuing",
                "3. If credential issue: rotate API keys",
                "4. If code bug: roll back to last known good version"
            ],
            escalation_path=["On-call engineer", "Team lead", "Engineering manager"],
            rollback_procedure="Deploy previous version: `git revert HEAD && deploy`"
        )

        self.incidents["high_latency"] = IncidentResponse(
            severity="medium",
            symptoms=[
                "P95 latency > 10s",
                "Timeout errors increasing",
                "User complaints about slow responses"
            ],
            diagnosis_steps=[
                "1. Check latency distribution: review Grafana dashboard",
                "2. Identify slow operations: trace analysis",
                "3. Check model load: review API response times",
                "4. Check tool performance: review tool call latencies"
            ],
            remediation_steps=[
                "1. Enable aggressive caching",
                "2. Switch to faster model tier for simple requests",
                "3. Increase timeout thresholds temporarily",
                "4. Scale up infrastructure if self-hosted"
            ],
            escalation_path=["On-call engineer", "Platform team"]
        )

        self.incidents["cost_spike"] = IncidentResponse(
            severity="medium",
            symptoms=[
                "Daily cost > 2x normal",
                "Token usage anomaly",
                "Unexpected model usage"
            ],
            diagnosis_steps=[
                "1. Review cost dashboard by agent/model",
                "2. Identify high-cost conversations",
                "3. Check for loops or excessive retries",
                "4. Verify rate limiting is active"
            ],
            remediation_steps=[
                "1. Enable strict budget caps",
                "2. Force lower-tier model for all requests",
                "3. Pause non-critical agents",
                "4. Investigate and fix root cause"
            ],
            escalation_path=["On-call engineer", "Finance/billing contact"]
        )

    def get_runbook(self, incident_type: str) -> Optional[IncidentResponse]:
        """Get runbook for incident type."""
        return self.incidents.get(incident_type)

    def execute_diagnosis(self, incident_type: str) -> List[str]:
        """Get diagnosis steps for an incident."""
        runbook = self.get_runbook(incident_type)
        if runbook:
            return runbook.diagnosis_steps
        return ["Unknown incident type. Escalate to engineering team."]
```

### SLO Definitions

```python
@dataclass
class SLO:
    """Service Level Objective definition."""
    name: str
    target: float
    measurement: str
    window: str  # e.g., "30d", "7d", "24h"
    alert_threshold: float

class SLOManager:
    """Manage and monitor SLOs."""

    def __init__(self):
        self.slos = {}
        self._setup_default_slos()

    def _setup_default_slos(self):
        """Configure default SLOs."""
        self.slos["availability"] = SLO(
            name="Agent Availability",
            target=0.999,  # 99.9%
            measurement="successful_requests / total_requests",
            window="30d",
            alert_threshold=0.995
        )

        self.slos["latency_p95"] = SLO(
            name="P95 Latency",
            target=5.0,  # 5 seconds
            measurement="percentile(latency, 95)",
            window="24h",
            alert_threshold=8.0
        )

        self.slos["error_rate"] = SLO(
            name="Error Rate",
            target=0.01,  # 1%
            measurement="errors / total_requests",
            window="24h",
            alert_threshold=0.05
        )

        self.slos["cost_per_request"] = SLO(
            name="Cost per Request",
            target=0.05,  # $0.05
            measurement="total_cost / total_requests",
            window="7d",
            alert_threshold=0.10
        )

    def check_slo(self, slo_name: str, current_value: float) -> dict:
        """Check if SLO is being met."""
        slo = self.slos.get(slo_name)
        if not slo:
            return {"error": f"Unknown SLO: {slo_name}"}

        # For latency and cost, lower is better
        if slo_name in ["latency_p95", "error_rate", "cost_per_request"]:
            meeting_target = current_value <= slo.target
            meeting_threshold = current_value <= slo.alert_threshold
        else:
            meeting_target = current_value >= slo.target
            meeting_threshold = current_value >= slo.alert_threshold

        return {
            "slo_name": slo.name,
            "target": slo.target,
            "current": current_value,
            "meeting_target": meeting_target,
            "alert": not meeting_threshold,
            "window": slo.window
        }
```

## Summary

In this chapter, you learned:

- **Enterprise Architecture**: Role-based agent graphs, workflow templates, and escalation patterns
- **Safety & Guardrails**: Input/output filtering, tool authorization, and budget management
- **Evaluations**: Automated testing frameworks and LLM-as-judge evaluation
- **Observability**: Structured logging, Prometheus metrics, and monitoring dashboards
- **Cost Optimization**: Model selection strategies and intelligent caching
- **Operations**: Runbooks, incident response, and SLO management

## Key Takeaways

1. Enterprise agents require layered safety: input filtering, output filtering, tool authorization, and budget caps
2. Automated evaluation pipelines catch regressions before production
3. Observability (logging, metrics, tracing) is essential for debugging and optimization
4. Cost control requires both preventive (budgets) and reactive (monitoring) measures
5. Operational runbooks reduce mean time to recovery (MTTR) during incidents

## Next Steps

You've completed the AG2 tutorial series. To continue your journey:

- **Deploy to production**: Set up proper infrastructure with monitoring
- **Build custom agents**: Create domain-specific agents for your use cases
- **Integrate with your stack**: Connect AG2 with your existing tools and workflows
- **Contribute back**: Share patterns and improvements with the AG2 community
