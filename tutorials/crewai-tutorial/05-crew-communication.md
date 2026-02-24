---
layout: default
title: "Chapter 5: Crew Communication"
parent: "CrewAI Tutorial"
nav_order: 5
---

# Chapter 5: Crew Communication

Welcome to **Chapter 5: Crew Communication**. In this part of **CrewAI Tutorial: Building Collaborative AI Agent Teams**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Effective communication is the lifeblood of successful AI crews. This chapter explores how agents communicate, share information, coordinate activities, and maintain context across complex multi-agent workflows.

## Communication Fundamentals

### Communication Architecture

```python
from crewai import Agent, Crew
from typing import Dict, List, Any, Optional
import asyncio

class CommunicationManager:
    def __init__(self):
        self.message_queue = asyncio.Queue()
        self.active_conversations = {}
        self.communication_history = []

    async def send_message(self, sender: Agent, receiver: Agent, message: Dict[str, Any]):
        """Send message between agents"""
        communication = {
            "id": self._generate_message_id(),
            "sender": sender.id,
            "receiver": receiver.id,
            "timestamp": self._get_timestamp(),
            "message": message,
            "conversation_id": self._get_conversation_id(sender, receiver)
        }

        await self.message_queue.put(communication)
        self.communication_history.append(communication)

    async def broadcast_message(self, sender: Agent, receivers: List[Agent], message: Dict[str, Any]):
        """Broadcast message to multiple agents"""
        tasks = []
        for receiver in receivers:
            tasks.append(self.send_message(sender, receiver, message))
        await asyncio.gather(*tasks)

    def _get_conversation_id(self, agent1: Agent, agent2: Agent) -> str:
        """Get or create conversation ID for agent pair"""
        agent_ids = sorted([agent1.id, agent2.id])
        conversation_key = f"{agent_ids[0]}_{agent_ids[1]}"

        if conversation_key not in self.active_conversations:
            self.active_conversations[conversation_key] = self._generate_conversation_id()

        return self.active_conversations[conversation_key]
```

### Message Types

```python
class MessageTypes:
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS_UPDATE = "status_update"
    INFORMATION_SHARE = "information_share"
    COORDINATION_REQUEST = "coordination_request"
    FEEDBACK = "feedback"
    ERROR_REPORT = "error_report"

class Message:
    def __init__(self,
                 type: str,
                 sender: str,
                 content: Any,
                 priority: str = "normal",
                 requires_response: bool = False):

        self.type = type
        self.sender = sender
        self.content = content
        self.priority = priority
        self.requires_response = requires_response
        self.timestamp = self._get_timestamp()
        self.id = self._generate_id()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "sender": self.sender,
            "content": self.content,
            "priority": self.priority,
            "requires_response": self.requires_response,
            "timestamp": self.timestamp
        }
```

## Communication Protocols

### Structured Communication

```python
class CommunicationProtocol:
    def __init__(self):
        self.protocols = {
            "task_delegation": self._task_delegation_protocol,
            "information_sharing": self._information_sharing_protocol,
            "coordination": self._coordination_protocol,
            "feedback": self._feedback_protocol
        }

    async def execute_protocol(self, protocol_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a communication protocol"""
        if protocol_type not in self.protocols:
            raise ValueError(f"Unknown protocol: {protocol_type}")

        return await self.protocols[protocol_type](context)

    async def _task_delegation_protocol(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Protocol for delegating tasks between agents"""
        delegator = context["delegator"]
        delegate = context["delegate"]
        task = context["task"]

        # Send task delegation message
        delegation_message = Message(
            type=MessageTypes.TASK_REQUEST,
            sender=delegator.id,
            content={
                "action": "delegate_task",
                "task": task.to_dict(),
                "requirements": context.get("requirements", {}),
                "deadline": context.get("deadline")
            },
            requires_response=True
        )

        await self.send_message(delegator, delegate, delegation_message)

        # Wait for response
        response = await self.wait_for_response(delegation_message.id, timeout=30)

        return {
            "status": "delegated" if response else "timeout",
            "response": response
        }

    async def _information_sharing_protocol(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Protocol for sharing information between agents"""
        sender = context["sender"]
        receivers = context["receivers"]
        information = context["information"]

        share_message = Message(
            type=MessageTypes.INFORMATION_SHARE,
            sender=sender.id,
            content={
                "action": "share_information",
                "information": information,
                "relevance": context.get("relevance", "general"),
                "urgency": context.get("urgency", "normal")
            }
        )

        await self.broadcast_message(sender, receivers, share_message)

        return {"status": "shared", "recipients": len(receivers)}
```

### Context Management

```python
class ContextManager:
    def __init__(self):
        self.shared_context = {}
        self.agent_contexts = {}
        self.context_history = []

    def update_shared_context(self, key: str, value: Any, agent: Agent):
        """Update shared context accessible to all agents"""
        self.shared_context[key] = {
            "value": value,
            "updated_by": agent.id,
            "timestamp": self._get_timestamp(),
            "version": self._get_next_version(key)
        }

        self.context_history.append({
            "action": "update_shared",
            "key": key,
            "agent": agent.id,
            "timestamp": self._get_timestamp()
        })

    def get_shared_context(self, key: str = None) -> Any:
        """Get shared context"""
        if key:
            return self.shared_context.get(key, {}).get("value")
        return self.shared_context

    def update_agent_context(self, agent_id: str, key: str, value: Any):
        """Update agent-specific context"""
        if agent_id not in self.agent_contexts:
            self.agent_contexts[agent_id] = {}

        self.agent_contexts[agent_id][key] = {
            "value": value,
            "timestamp": self._get_timestamp()
        }

    def get_agent_context(self, agent_id: str, key: str = None) -> Any:
        """Get agent-specific context"""
        if agent_id not in self.agent_contexts:
            return None

        agent_context = self.agent_contexts[agent_id]
        if key:
            return agent_context.get(key, {}).get("value")
        return agent_context

    def get_relevant_context(self, agent: Agent, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get context relevant to current task"""
        relevant_context = {}

        # Add shared context relevant to task
        for key, value in self.shared_context.items():
            if self._is_relevant_to_task(key, task_context):
                relevant_context[f"shared_{key}"] = value["value"]

        # Add agent-specific context
        agent_context = self.get_agent_context(agent.id)
        if agent_context:
            relevant_context.update(agent_context)

        return relevant_context

    def _is_relevant_to_task(self, context_key: str, task_context: Dict[str, Any]) -> bool:
        """Determine if shared context is relevant to current task"""
        # Simple relevance check (could be enhanced with ML)
        task_keywords = str(task_context).lower().split()
        return any(keyword in context_key.lower() for keyword in task_keywords)
```

## Coordination Patterns

### Hierarchical Coordination

```python
class HierarchicalCoordinator:
    def __init__(self, manager_agent: Agent, worker_agents: List[Agent]):
        self.manager = manager_agent
        self.workers = worker_agents
        self.task_assignments = {}

    async def coordinate_task(self, task: Dict[str, Any]):
        """Coordinate task execution hierarchically"""
        # Manager decomposes task
        subtasks = await self._decompose_task(task)

        # Assign subtasks to workers
        assignments = await self._assign_subtasks(subtasks)

        # Monitor execution
        results = await self._monitor_execution(assignments)

        # Synthesize results
        final_result = await self._synthesize_results(results)

        return final_result

    async def _decompose_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Manager decomposes complex task into subtasks"""
        decomposition_prompt = f"""
        Decompose this task into manageable subtasks:
        Task: {task['description']}

        Consider:
        - Required skills/expertise
        - Dependencies between subtasks
        - Estimated effort for each subtask

        Return subtasks as a structured list.
        """

        response = await self.manager.process_message({
            "type": "task_decomposition",
            "content": decomposition_prompt
        })

        return self._parse_subtasks(response)

    async def _assign_subtasks(self, subtasks: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Assign subtasks to appropriate workers"""
        assignments = {}

        for subtask in subtasks:
            best_worker = await self._find_best_worker(subtask)
            assignments[subtask['id']] = {
                "subtask": subtask,
                "worker": best_worker,
                "status": "assigned"
            }

            # Notify worker of assignment
            await self._notify_worker_assignment(best_worker, subtask)

        return assignments

    async def _find_best_worker(self, subtask: Dict[str, Any]) -> Agent:
        """Find best worker for subtask based on skills and availability"""
        best_worker = None
        best_score = 0

        for worker in self.workers:
            score = await self._calculate_worker_score(worker, subtask)
            if score > best_score:
                best_score = score
                best_worker = worker

        return best_worker
```

### Peer-to-Peer Coordination

```python
class PeerCoordinator:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.negotiation_history = []

    async def coordinate_peers(self, task: Dict[str, Any]):
        """Coordinate task execution among peers"""
        # Broadcast task to all agents
        proposals = await self._collect_proposals(task)

        # Negotiate and agree on approach
        agreement = await self._negotiate_approach(proposals)

        # Execute coordinated approach
        result = await self._execute_coordinated_approach(agreement)

        return result

    async def _collect_proposals(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect proposals from all agents"""
        proposals = []

        for agent in self.agents:
            proposal = await agent.process_message({
                "type": "task_proposal_request",
                "content": task
            })

            proposals.append({
                "agent": agent.id,
                "proposal": proposal,
                "timestamp": self._get_timestamp()
            })

        return proposals

    async def _negotiate_approach(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Negotiate and agree on execution approach"""
        # Simple voting mechanism (could be enhanced)
        approach_votes = {}

        for proposal in proposals:
            approach = proposal["proposal"]["approach"]
            if approach not in approach_votes:
                approach_votes[approach] = 0
            approach_votes[approach] += 1

        # Select most voted approach
        best_approach = max(approach_votes, key=approach_votes.get)

        # Find agent who proposed the winning approach
        winning_agent = None
        for proposal in proposals:
            if proposal["proposal"]["approach"] == best_approach:
                winning_agent = proposal["agent"]
                break

        return {
            "approach": best_approach,
            "coordinator": winning_agent,
            "votes": approach_votes
        }
```

## Communication Monitoring

### Communication Analytics

```python
class CommunicationAnalytics:
    def __init__(self):
        self.message_metrics = {}
        self.conversation_metrics = {}
        self.agent_metrics = {}

    def analyze_communication(self, communication_history: List[Dict[str, Any]]):
        """Analyze communication patterns and effectiveness"""
        self._calculate_message_metrics(communication_history)
        self._calculate_conversation_metrics(communication_history)
        self._calculate_agent_metrics(communication_history)

    def _calculate_message_metrics(self, history: List[Dict[str, Any]]):
        """Calculate message-level metrics"""
        total_messages = len(history)
        message_types = {}
        response_times = []

        for msg in history:
            # Count message types
            msg_type = msg["message"]["type"]
            message_types[msg_type] = message_types.get(msg_type, 0) + 1

            # Calculate response times (if applicable)
            if msg.get("response_time"):
                response_times.append(msg["response_time"])

        self.message_metrics = {
            "total_messages": total_messages,
            "message_types": message_types,
            "average_response_time": sum(response_times) / len(response_times) if response_times else 0
        }

    def _calculate_agent_metrics(self, history: List[Dict[str, Any]]):
        """Calculate agent-level communication metrics"""
        agent_stats = {}

        for msg in history:
            sender = msg["sender"]
            receiver = msg["receiver"]

            for agent in [sender, receiver]:
                if agent not in agent_stats:
                    agent_stats[agent] = {
                        "messages_sent": 0,
                        "messages_received": 0,
                        "response_rate": 0,
                        "collaboration_score": 0
                    }

            agent_stats[sender]["messages_sent"] += 1
            agent_stats[receiver]["messages_received"] += 1

        self.agent_metrics = agent_stats

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive communication report"""
        return {
            "message_metrics": self.message_metrics,
            "conversation_metrics": self.conversation_metrics,
            "agent_metrics": self.agent_metrics,
            "insights": self._generate_insights(),
            "recommendations": self._generate_recommendations()
        }

    def _generate_insights(self) -> List[str]:
        """Generate insights from communication analysis"""
        insights = []

        # Message type distribution
        most_common_type = max(self.message_metrics["message_types"],
                             key=self.message_metrics["message_types"].get)
        insights.append(f"Most common message type: {most_common_type}")

        # Response time analysis
        avg_response = self.message_metrics["average_response_time"]
        if avg_response > 60:  # More than 1 minute
            insights.append("Slow response times may indicate communication bottlenecks")

        return insights

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improving communication"""
        recommendations = []

        # Check for uneven participation
        sent_counts = [stats["messages_sent"] for stats in self.agent_metrics.values()]
        if max(sent_counts) / min(sent_counts) > 3:
            recommendations.append("Encourage more balanced participation in discussions")

        # Check response rates
        low_response_agents = [
            agent for agent, stats in self.agent_metrics.items()
            if stats["response_rate"] < 0.5
        ]
        if low_response_agents:
            recommendations.append(f"Improve response rates for agents: {low_response_agents}")

        return recommendations
```

## What We've Accomplished

✅ **Built communication architecture** for multi-agent systems
✅ **Implemented structured messaging** with different message types
✅ **Created communication protocols** for various scenarios
✅ **Developed context management** systems
✅ **Established coordination patterns** (hierarchical and peer-to-peer)
✅ **Set up communication analytics** and monitoring

## Next Steps

Ready to manage different execution processes? In [Chapter 6: Process Management](06-process-management.md), we'll explore different execution patterns and workflows for various types of tasks.

---

**Key Takeaway:** Effective communication is the foundation of successful multi-agent collaboration. Well-designed communication protocols, context management, and coordination patterns enable agents to work together efficiently toward complex objectives.

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `Dict`, `agent` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 5: Crew Communication` as an operating subsystem inside **CrewAI Tutorial: Building Collaborative AI Agent Teams**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `context`, `task`, `sender` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 5: Crew Communication` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `Dict` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `agent`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/crewAIInc/crewAI)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `Dict` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 4: Tool Integration](04-tool-integration.md)
- [Next Chapter: Chapter 6: Process Management](06-process-management.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
