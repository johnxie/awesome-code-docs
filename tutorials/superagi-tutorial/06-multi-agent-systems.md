---
layout: default
title: "Chapter 6: Multi-Agent Systems"
parent: "SuperAGI Tutorial"
nav_order: 6
---

# Chapter 6: Multi-Agent Systems

Welcome to **Chapter 6: Multi-Agent Systems**. In this part of **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Coordinate multiple agents for complex tasks through communication, collaboration, and orchestration patterns.

## Overview

Multi-agent systems enable complex problem-solving by combining specialized agents that can communicate, collaborate, and coordinate their actions. This chapter covers agent communication, orchestration patterns, and team dynamics.

## Agent Communication

### Message Passing

```python
from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime
from queue import Queue
import uuid

@dataclass
class AgentMessage:
    """Message between agents."""
    id: str
    sender: str
    recipient: str
    type: str  # "request", "response", "broadcast", "notification"
    content: Any
    timestamp: str
    reply_to: Optional[str] = None
    priority: int = 5  # 1-10, higher is more urgent

class MessageBus:
    """Central message bus for agent communication."""

    def __init__(self):
        self.queues = {}  # agent_id -> Queue
        self.message_log = []
        self.subscribers = {}  # topic -> list of agent_ids

    def register_agent(self, agent_id: str):
        """Register an agent on the message bus."""
        self.queues[agent_id] = Queue()

    def send(self, message: AgentMessage):
        """Send a message to an agent."""
        if message.recipient == "broadcast":
            self._broadcast(message)
        elif message.recipient in self.queues:
            self.queues[message.recipient].put(message)
            self.message_log.append(message)
        else:
            raise ValueError(f"Unknown recipient: {message.recipient}")

    def receive(self, agent_id: str, timeout: float = None) -> Optional[AgentMessage]:
        """Receive a message for an agent."""
        if agent_id not in self.queues:
            return None

        try:
            return self.queues[agent_id].get(timeout=timeout)
        except:
            return None

    def subscribe(self, agent_id: str, topic: str):
        """Subscribe an agent to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(agent_id)

    def publish(self, topic: str, message: AgentMessage):
        """Publish a message to a topic."""
        for agent_id in self.subscribers.get(topic, []):
            message_copy = AgentMessage(
                id=str(uuid.uuid4()),
                sender=message.sender,
                recipient=agent_id,
                type=message.type,
                content=message.content,
                timestamp=datetime.now().isoformat()
            )
            self.send(message_copy)

    def _broadcast(self, message: AgentMessage):
        """Broadcast message to all agents."""
        for agent_id, queue in self.queues.items():
            if agent_id != message.sender:
                queue.put(message)
```

### Direct Communication

```python
class CommunicatingAgent:
    """Agent with communication capabilities."""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.message_bus.register_agent(agent_id)
        self.pending_requests = {}

    def send_request(self, recipient: str, content: Any, wait_for_reply: bool = True) -> Optional[Any]:
        """Send a request to another agent."""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            recipient=recipient,
            type="request",
            content=content,
            timestamp=datetime.now().isoformat()
        )

        self.message_bus.send(message)

        if wait_for_reply:
            self.pending_requests[message.id] = None
            return self._wait_for_reply(message.id)

        return None

    def send_response(self, original_message: AgentMessage, content: Any):
        """Send a response to a request."""
        response = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            recipient=original_message.sender,
            type="response",
            content=content,
            timestamp=datetime.now().isoformat(),
            reply_to=original_message.id
        )
        self.message_bus.send(response)

    def broadcast(self, content: Any):
        """Broadcast a message to all agents."""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            recipient="broadcast",
            type="broadcast",
            content=content,
            timestamp=datetime.now().isoformat()
        )
        self.message_bus.send(message)

    def process_messages(self):
        """Process incoming messages."""
        while True:
            message = self.message_bus.receive(self.agent_id, timeout=0.1)
            if not message:
                break

            if message.type == "response" and message.reply_to in self.pending_requests:
                self.pending_requests[message.reply_to] = message.content
            else:
                self._handle_message(message)

    def _handle_message(self, message: AgentMessage):
        """Handle incoming message (override in subclass)."""
        pass

    def _wait_for_reply(self, request_id: str, timeout: float = 30) -> Any:
        """Wait for a reply to a request."""
        import time
        start = time.time()

        while time.time() - start < timeout:
            self.process_messages()
            if self.pending_requests.get(request_id) is not None:
                return self.pending_requests.pop(request_id)
            time.sleep(0.1)

        return None
```

## Orchestration Patterns

### Hierarchical Orchestration

```python
class OrchestratorAgent(CommunicatingAgent):
    """Central orchestrator that coordinates worker agents."""

    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, message_bus)
        self.workers = {}  # worker_id -> worker_info
        self.task_queue = []
        self.task_assignments = {}  # task_id -> worker_id

    def register_worker(self, worker_id: str, capabilities: list):
        """Register a worker agent."""
        self.workers[worker_id] = {
            "id": worker_id,
            "capabilities": capabilities,
            "status": "idle",
            "current_task": None
        }

    def submit_task(self, task: dict):
        """Submit a task for execution."""
        task["id"] = str(uuid.uuid4())
        task["status"] = "pending"
        self.task_queue.append(task)
        self._assign_tasks()

    def _assign_tasks(self):
        """Assign pending tasks to available workers."""
        for task in self.task_queue:
            if task["status"] != "pending":
                continue

            # Find suitable worker
            worker = self._find_suitable_worker(task)
            if worker:
                self._assign_task_to_worker(task, worker)

    def _find_suitable_worker(self, task: dict) -> Optional[dict]:
        """Find a worker capable of handling the task."""
        required_capability = task.get("required_capability")

        for worker in self.workers.values():
            if worker["status"] != "idle":
                continue
            if required_capability and required_capability not in worker["capabilities"]:
                continue
            return worker

        return None

    def _assign_task_to_worker(self, task: dict, worker: dict):
        """Assign a task to a worker."""
        task["status"] = "assigned"
        worker["status"] = "busy"
        worker["current_task"] = task["id"]
        self.task_assignments[task["id"]] = worker["id"]

        # Send task to worker
        self.send_request(
            worker["id"],
            {"type": "execute_task", "task": task},
            wait_for_reply=False
        )

    def _handle_message(self, message: AgentMessage):
        """Handle messages from workers."""
        content = message.content

        if content.get("type") == "task_complete":
            self._handle_task_completion(message.sender, content)
        elif content.get("type") == "task_failed":
            self._handle_task_failure(message.sender, content)

    def _handle_task_completion(self, worker_id: str, content: dict):
        """Handle task completion notification."""
        task_id = content.get("task_id")

        # Update worker status
        if worker_id in self.workers:
            self.workers[worker_id]["status"] = "idle"
            self.workers[worker_id]["current_task"] = None

        # Update task status
        for task in self.task_queue:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["result"] = content.get("result")
                break

        # Assign more tasks
        self._assign_tasks()
```

### Peer-to-Peer Collaboration

```python
class CollaborativeAgent(CommunicatingAgent):
    """Agent that collaborates with peers."""

    def __init__(self, agent_id: str, message_bus: MessageBus, capabilities: list):
        super().__init__(agent_id, message_bus)
        self.capabilities = capabilities
        self.peers = {}  # peer_id -> peer_info
        self.collaboration_requests = []

    def discover_peers(self):
        """Discover other agents on the message bus."""
        self.broadcast({
            "type": "peer_discovery",
            "capabilities": self.capabilities
        })

    def request_collaboration(self, task: dict, required_capabilities: list):
        """Request collaboration for a task."""
        # Find peers with required capabilities
        suitable_peers = []
        for peer_id, peer_info in self.peers.items():
            peer_caps = set(peer_info.get("capabilities", []))
            if set(required_capabilities).intersection(peer_caps):
                suitable_peers.append(peer_id)

        if not suitable_peers:
            return None

        # Send collaboration request
        request_id = str(uuid.uuid4())
        for peer_id in suitable_peers:
            self.send_request(
                peer_id,
                {
                    "type": "collaboration_request",
                    "request_id": request_id,
                    "task": task,
                    "required_capabilities": required_capabilities
                },
                wait_for_reply=False
            )

        return request_id

    def _handle_message(self, message: AgentMessage):
        """Handle incoming messages."""
        content = message.content

        if content.get("type") == "peer_discovery":
            self._handle_peer_discovery(message.sender, content)

        elif content.get("type") == "collaboration_request":
            self._handle_collaboration_request(message)

        elif content.get("type") == "collaboration_accept":
            self._handle_collaboration_accept(message)

    def _handle_peer_discovery(self, peer_id: str, content: dict):
        """Handle peer discovery message."""
        self.peers[peer_id] = {
            "capabilities": content.get("capabilities", []),
            "discovered_at": datetime.now().isoformat()
        }

        # Respond with our capabilities
        self.send_response(
            AgentMessage(
                id="", sender=peer_id, recipient=self.agent_id,
                type="request", content={}, timestamp=""
            ),
            {
                "type": "peer_discovery_response",
                "capabilities": self.capabilities
            }
        )

    def _handle_collaboration_request(self, message: AgentMessage):
        """Handle a collaboration request."""
        content = message.content
        task = content.get("task")

        # Decide whether to accept
        if self._can_handle_task(task):
            self.send_response(message, {
                "type": "collaboration_accept",
                "request_id": content.get("request_id")
            })
        else:
            self.send_response(message, {
                "type": "collaboration_decline",
                "request_id": content.get("request_id"),
                "reason": "Cannot handle task requirements"
            })
```

### Market-Based Coordination

```python
class AuctionCoordinator:
    """Coordinate agents through task auctions."""

    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.auctions = {}  # auction_id -> auction_info
        self.bids = {}  # auction_id -> list of bids

    def create_auction(self, task: dict, deadline: datetime) -> str:
        """Create an auction for a task."""
        auction_id = str(uuid.uuid4())

        self.auctions[auction_id] = {
            "task": task,
            "deadline": deadline,
            "status": "open",
            "winner": None
        }
        self.bids[auction_id] = []

        # Broadcast auction
        self.message_bus.publish("task_auctions", AgentMessage(
            id=str(uuid.uuid4()),
            sender="coordinator",
            recipient="",
            type="broadcast",
            content={
                "type": "new_auction",
                "auction_id": auction_id,
                "task": task,
                "deadline": deadline.isoformat()
            },
            timestamp=datetime.now().isoformat()
        ))

        return auction_id

    def submit_bid(self, auction_id: str, agent_id: str, bid_value: float, details: dict):
        """Submit a bid for an auction."""
        if auction_id not in self.auctions:
            return False

        auction = self.auctions[auction_id]
        if auction["status"] != "open":
            return False

        self.bids[auction_id].append({
            "agent_id": agent_id,
            "value": bid_value,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

        return True

    def close_auction(self, auction_id: str) -> Optional[dict]:
        """Close auction and determine winner."""
        if auction_id not in self.auctions:
            return None

        auction = self.auctions[auction_id]
        bids = self.bids[auction_id]

        if not bids:
            auction["status"] = "no_bids"
            return None

        # Select winner (lowest bid wins in this example)
        winner_bid = min(bids, key=lambda b: b["value"])
        auction["status"] = "closed"
        auction["winner"] = winner_bid["agent_id"]

        # Notify winner
        self.message_bus.send(AgentMessage(
            id=str(uuid.uuid4()),
            sender="coordinator",
            recipient=winner_bid["agent_id"],
            type="notification",
            content={
                "type": "auction_won",
                "auction_id": auction_id,
                "task": auction["task"]
            },
            timestamp=datetime.now().isoformat()
        ))

        return winner_bid


class BiddingAgent(CommunicatingAgent):
    """Agent that participates in task auctions."""

    def __init__(self, agent_id: str, message_bus: MessageBus, capabilities: list):
        super().__init__(agent_id, message_bus)
        self.capabilities = capabilities
        self.message_bus.subscribe(agent_id, "task_auctions")

    def _handle_message(self, message: AgentMessage):
        """Handle auction-related messages."""
        content = message.content

        if content.get("type") == "new_auction":
            self._evaluate_auction(content)
        elif content.get("type") == "auction_won":
            self._handle_auction_win(content)

    def _evaluate_auction(self, auction_info: dict):
        """Evaluate whether to bid on an auction."""
        task = auction_info.get("task")

        # Check if we can handle the task
        if not self._can_handle(task):
            return

        # Calculate bid value based on cost/capability
        bid_value = self._calculate_bid(task)

        # Submit bid
        # (In a real implementation, this would go through the coordinator)
        print(f"Agent {self.agent_id} bidding {bid_value} for auction {auction_info['auction_id']}")

    def _calculate_bid(self, task: dict) -> float:
        """Calculate bid value for a task."""
        base_cost = task.get("estimated_cost", 10)
        # Add factors like current workload, capability match, etc.
        return base_cost * 1.1  # 10% markup
```

## Team Patterns

### Specialized Teams

```python
class AgentTeam:
    """Team of specialized agents working together."""

    def __init__(self, team_id: str, message_bus: MessageBus):
        self.team_id = team_id
        self.message_bus = message_bus
        self.members = {}  # role -> agent
        self.team_memory = {}  # Shared team context

    def add_member(self, role: str, agent: CommunicatingAgent):
        """Add a member to the team."""
        self.members[role] = agent
        self.team_memory[f"{role}_status"] = "idle"

    def execute_project(self, project: dict) -> dict:
        """Execute a project using the team."""
        results = {}

        # Phase 1: Research (if researcher available)
        if "researcher" in self.members:
            research = self._delegate("researcher", {
                "type": "research",
                "topic": project.get("topic"),
                "scope": project.get("research_scope")
            })
            results["research"] = research
            self.team_memory["research_findings"] = research

        # Phase 2: Planning (if planner available)
        if "planner" in self.members:
            plan = self._delegate("planner", {
                "type": "create_plan",
                "project": project,
                "context": self.team_memory
            })
            results["plan"] = plan
            self.team_memory["execution_plan"] = plan

        # Phase 3: Implementation (if implementer available)
        if "implementer" in self.members:
            implementation = self._delegate("implementer", {
                "type": "implement",
                "plan": self.team_memory.get("execution_plan"),
                "context": self.team_memory
            })
            results["implementation"] = implementation

        # Phase 4: Review (if reviewer available)
        if "reviewer" in self.members:
            review = self._delegate("reviewer", {
                "type": "review",
                "implementation": results.get("implementation"),
                "context": self.team_memory
            })
            results["review"] = review

        return results

    def _delegate(self, role: str, task: dict) -> Any:
        """Delegate a task to a team member."""
        agent = self.members.get(role)
        if not agent:
            return None

        self.team_memory[f"{role}_status"] = "working"
        result = agent.send_request(agent.agent_id, task)
        self.team_memory[f"{role}_status"] = "idle"

        return result


# Create specialized team
def create_development_team(message_bus: MessageBus) -> AgentTeam:
    """Create a development team with specialized roles."""
    team = AgentTeam("dev_team", message_bus)

    team.add_member("researcher", ResearchAgent("researcher_1", message_bus))
    team.add_member("planner", PlannerAgent("planner_1", message_bus))
    team.add_member("implementer", CodingAgent("coder_1", message_bus))
    team.add_member("reviewer", ReviewerAgent("reviewer_1", message_bus))

    return team
```

### Dynamic Team Formation

```python
class DynamicTeamManager:
    """Dynamically form teams based on task requirements."""

    def __init__(self, agent_pool: dict, message_bus: MessageBus):
        self.agent_pool = agent_pool  # agent_id -> agent
        self.message_bus = message_bus
        self.active_teams = {}

    def form_team(self, task: dict) -> AgentTeam:
        """Form a team for a specific task."""
        required_roles = self._analyze_required_roles(task)

        team_id = str(uuid.uuid4())
        team = AgentTeam(team_id, self.message_bus)

        # Find best agent for each role
        for role in required_roles:
            agent = self._find_best_agent_for_role(role)
            if agent:
                team.add_member(role, agent)

        self.active_teams[team_id] = team
        return team

    def _analyze_required_roles(self, task: dict) -> list:
        """Analyze task to determine required roles."""
        roles = []

        task_type = task.get("type", "")

        if task_type == "research_project":
            roles = ["researcher", "writer", "reviewer"]
        elif task_type == "software_development":
            roles = ["planner", "developer", "tester", "reviewer"]
        elif task_type == "data_analysis":
            roles = ["data_collector", "analyst", "visualizer"]
        else:
            roles = ["generalist"]

        return roles

    def _find_best_agent_for_role(self, role: str) -> Optional[CommunicatingAgent]:
        """Find the best available agent for a role."""
        best_agent = None
        best_score = 0

        for agent_id, agent in self.agent_pool.items():
            if not self._is_available(agent):
                continue

            score = self._calculate_fit_score(agent, role)
            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent

    def disband_team(self, team_id: str):
        """Disband a team and return agents to pool."""
        if team_id in self.active_teams:
            del self.active_teams[team_id]
```

## Consensus and Voting

```python
class ConsensusManager:
    """Manage consensus among agents."""

    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus

    def propose(self, proposer: str, proposal: dict, voters: list) -> str:
        """Create a proposal for voting."""
        proposal_id = str(uuid.uuid4())

        for voter in voters:
            self.message_bus.send(AgentMessage(
                id=str(uuid.uuid4()),
                sender=proposer,
                recipient=voter,
                type="request",
                content={
                    "type": "vote_request",
                    "proposal_id": proposal_id,
                    "proposal": proposal
                },
                timestamp=datetime.now().isoformat()
            ))

        return proposal_id

    def collect_votes(self, proposal_id: str, timeout: float = 30) -> dict:
        """Collect votes for a proposal."""
        votes = {"approve": 0, "reject": 0, "abstain": 0}
        # Implementation would collect responses
        return votes

    def reach_consensus(self, proposal_id: str, threshold: float = 0.66) -> bool:
        """Check if consensus is reached."""
        votes = self.collect_votes(proposal_id)
        total = sum(votes.values())

        if total == 0:
            return False

        approval_rate = votes["approve"] / total
        return approval_rate >= threshold
```

## Summary

In this chapter, you've learned:

- **Agent Communication**: Message passing and pub/sub patterns
- **Orchestration**: Hierarchical and peer-to-peer coordination
- **Market-Based**: Auctions and bidding for task allocation
- **Team Patterns**: Specialized teams and dynamic formation
- **Consensus**: Voting and agreement protocols

## Key Takeaways

1. **Communication is Key**: Agents need reliable message passing
2. **Choose Orchestration**: Hierarchical for control, P2P for flexibility
3. **Specialize Agents**: Different roles for different capabilities
4. **Dynamic Teams**: Form teams based on task requirements
5. **Reach Agreement**: Consensus mechanisms for decisions

## Next Steps

Now that you can coordinate agents, let's explore Deployment & Scaling in Chapter 7 for production deployments.

---

**Ready for Chapter 7?** [Deployment & Scaling](07-deployment-scaling.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `task`, `message` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Multi-Agent Systems` as an operating subsystem inside **SuperAGI Tutorial: Production-Ready Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `content`, `agent_id`, `message_bus` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Multi-Agent Systems` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `task` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `message`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/TransformerOptimus/SuperAGI)
  Why it matters: authoritative reference on `View Repo` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `task` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Task Planning](05-task-planning.md)
- [Next Chapter: Chapter 7: Deployment & Scaling](07-deployment-scaling.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
