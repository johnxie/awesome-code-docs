---
layout: default
title: "AG2 Tutorial - Chapter 6: Group Chat & Multi-Agent Collaboration"
nav_order: 6
has_children: false
parent: AG2 Tutorial
---

# Chapter 6: Group Chat & Multi-Agent Collaboration

> Master the art of coordinating multiple agents in group conversations for complex problem-solving.

## Overview

Group chat enables multiple agents to collaborate on complex tasks through structured conversations. This transforms individual agent capabilities into coordinated team performance.

## Basic Group Chat Setup

### Round-Robin Speaker Selection

```python
from ag2 import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Create specialized agents
product_manager = AssistantAgent(
    name="product_manager",
    system_message="""You are a product manager focused on:
    - User needs and requirements
    - Business value and prioritization
    - Product strategy and roadmap
    - Stakeholder management""",
    llm_config=llm_config
)

designer = AssistantAgent(
    name="designer",
    system_message="""You are a UX/UI designer focused on:
    - User experience and interface design
    - Visual design and branding
    - Usability and accessibility
    - Design systems and consistency""",
    llm_config=llm_config
)

developer = AssistantAgent(
    name="developer",
    system_message="""You are a software developer focused on:
    - Technical implementation and architecture
    - Code quality and best practices
    - Performance and scalability
    - Security and reliability""",
    llm_config=llm_config
)

qa_specialist = AssistantAgent(
    name="qa_specialist",
    system_message="""You are a QA specialist focused on:
    - Test planning and execution
    - Quality assurance and validation
    - Bug tracking and resolution
    - Performance and security testing""",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config=False
)

# Create group chat with round-robin speaker selection
group_chat = GroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=12,  # Allow up to 12 conversation turns
    speaker_selection_method="round_robin",
    send_introductions=True  # Agents introduce themselves
)

# Create group chat manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

# Start collaborative discussion
user_proxy.initiate_chat(
    manager,
    message="Design and plan a mobile fitness tracking app with social features."
)
```

### Auto Speaker Selection

Let the LLM decide who should speak next based on conversation context.

```python
# Group chat with automatic speaker selection
auto_group_chat = GroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=15,
    speaker_selection_method="auto",  # LLM decides who speaks next
    allow_repeat_speaker=False       # Prevent same agent speaking twice in a row
)

auto_manager = GroupChatManager(
    groupchat=auto_group_chat,
    llm_config=llm_config
)

# The conversation flows naturally based on who has relevant expertise
user_proxy.initiate_chat(
    auto_manager,
    message="Our e-commerce site is slow. Help me identify and fix performance issues."
)
```

## Custom Speaker Selection

### Role-Based Selection

```python
class RoleBasedGroupChat(GroupChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_phase = "planning"
        self.phase_sequence = {
            "planning": "product_manager",
            "design": "designer",
            "development": "developer",
            "testing": "qa_specialist"
        }

    def select_speaker(self, last_speaker, selector):
        """Select speaker based on project phase"""
        # Check if current phase is complete
        if self._is_phase_complete():
            self._advance_phase()

        # Select speaker for current phase
        target_agent_name = self.phase_sequence[self.current_phase]

        # Find the agent
        for agent in self.agents:
            if agent.name == target_agent_name:
                return agent

        # Fallback to round-robin
        return super().select_speaker(last_speaker, selector)

    def _is_phase_complete(self):
        """Check if current phase has enough discussion"""
        recent_messages = self.messages[-6:]  # Last 6 messages
        phase_keywords = {
            "planning": ["plan", "strategy", "requirements", "goals"],
            "design": ["design", "ui", "ux", "interface", "visual"],
            "development": ["code", "implement", "architecture", "technical"],
            "testing": ["test", "quality", "bugs", "validation"]
        }

        keywords = phase_keywords.get(self.current_phase, [])
        message_text = " ".join([msg.get("content", "") for msg in recent_messages])

        # Count keyword matches
        keyword_count = sum(1 for keyword in keywords if keyword in message_text.lower())

        return keyword_count >= 3  # Phase complete if 3+ keywords found

    def _advance_phase(self):
        """Move to next project phase"""
        phases = list(self.phase_sequence.keys())
        current_index = phases.index(self.current_phase)

        if current_index < len(phases) - 1:
            self.current_phase = phases[current_index + 1]
        else:
            self.current_phase = "completed"

# Create role-based group chat
role_based_chat = RoleBasedGroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=20
)

role_manager = GroupChatManager(
    groupchat=role_based_chat,
    llm_config=llm_config
)
```

### Expertise-Based Selection

```python
class ExpertiseBasedGroupChat(GroupChat):
    def __init__(self, agent_expertise=None, **kwargs):
        super().__init__(**kwargs)
        self.agent_expertise = agent_expertise or {
            "product_manager": ["business", "strategy", "requirements", "planning"],
            "designer": ["ui", "ux", "design", "visual", "user"],
            "developer": ["code", "technical", "implementation", "architecture"],
            "qa_specialist": ["test", "quality", "bugs", "validation", "performance"]
        }

    def select_speaker(self, last_speaker, selector):
        """Select speaker based on conversation topic expertise"""
        if not self.messages:
            return self.agents[0]  # Start with first agent

        # Analyze recent conversation
        recent_content = " ".join([
            msg.get("content", "") for msg in self.messages[-3:]
        ]).lower()

        # Find most relevant expert
        best_agent = None
        best_score = 0

        for agent in self.agents:
            if agent == last_speaker and len(self.messages) > 1:
                continue  # Avoid consecutive turns unless necessary

            expertise = self.agent_expertise.get(agent.name, [])
            score = sum(1 for keyword in expertise if keyword in recent_content)

            if score > best_score:
                best_score = score
                best_agent = agent

        return best_agent or super().select_speaker(last_speaker, selector)

# Create expertise-based group chat
expertise_chat = ExpertiseBasedGroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=15
)

expertise_manager = GroupChatManager(
    groupchat=expertise_chat,
    llm_config=llm_config
)

user_proxy.initiate_chat(
    expertise_manager,
    message="The app crashes when users try to upload images. Help me debug and fix this."
)
```

## Advanced Group Chat Patterns

### Hierarchical Group Chat

```python
class HierarchicalGroupChat:
    def __init__(self, teams):
        self.teams = teams  # Dict of team_name -> GroupChat
        self.coordinators = {}  # Team coordinators

    def create_team_coordinator(self, team_name, coordinator_agent):
        """Create a coordinator for a team"""
        self.coordinators[team_name] = coordinator_agent

    def delegate_to_team(self, team_name, task, context):
        """Delegate task to a specific team"""
        if team_name not in self.teams:
            return {"error": f"Team '{team_name}' not found"}

        team_chat = self.teams[team_name]
        coordinator = self.coordinators.get(team_name)

        if coordinator:
            # Coordinator handles the delegation
            result = coordinator.initiate_chat(
                team_chat.manager if hasattr(team_chat, 'manager') else team_chat,
                message=f"Team task: {task}\nContext: {context}"
            )
        else:
            # Direct team execution
            result = team_chat.agents[0].initiate_chat(
                team_chat,
                message=task
            )

        return result

# Create hierarchical teams
frontend_team = GroupChat(
    agents=[designer, developer],
    messages=[],
    max_round=8,
    speaker_selection_method="auto"
)

backend_team = GroupChat(
    agents=[developer, qa_specialist],
    messages=[],
    max_round=8,
    speaker_selection_method="auto"
)

# Create coordinators
frontend_coordinator = AssistantAgent(
    name="frontend_coordinator",
    system_message="Coordinate frontend development tasks between designers and developers.",
    llm_config=llm_config
)

backend_coordinator = AssistantAgent(
    name="backend_coordinator",
    system_message="Coordinate backend development tasks between developers and QA.",
    llm_config=llm_config
)

# Create hierarchical chat
hierarchical_chat = HierarchicalGroupChat({
    "frontend": frontend_team,
    "backend": backend_team
})

hierarchical_chat.create_team_coordinator("frontend", frontend_coordinator)
hierarchical_chat.create_team_coordinator("backend", backend_coordinator)

# Delegate tasks to teams
frontend_result = hierarchical_chat.delegate_to_team(
    "frontend",
    "Design and implement the user dashboard",
    "User authentication is already implemented"
)

backend_result = hierarchical_chat.delegate_to_team(
    "backend",
    "Implement API endpoints for user data",
    "Database schema is ready"
)
```

### Consensus-Driven Group Chat

```python
class ConsensusGroupChat(GroupChat):
    def __init__(self, consensus_threshold=0.7, **kwargs):
        super().__init__(**kwargs)
        self.consensus_threshold = consensus_threshold
        self.proposals = []
        self.votes = {}

    def propose_solution(self, agent, proposal):
        """Agent proposes a solution"""
        self.proposals.append({
            "agent": agent.name,
            "proposal": proposal,
            "timestamp": time.time(),
            "votes": []
        })

    def vote_on_proposals(self, agent, votes):
        """Agent votes on proposals"""
        self.votes[agent.name] = votes

    def check_consensus(self):
        """Check if consensus is reached"""
        if not self.proposals:
            return False, None

        total_agents = len([a for a in self.agents if a != self.agents[0]])  # Exclude user proxy
        min_votes_needed = int(total_agents * self.consensus_threshold)

        for proposal in self.proposals:
            votes = len(proposal["votes"])
            if votes >= min_votes_needed:
                return True, proposal

        return False, None

    def select_speaker(self, last_speaker, selector):
        """Modified speaker selection for consensus building"""
        consensus_reached, winning_proposal = self.check_consensus()

        if consensus_reached:
            # Consensus reached - select agent to implement
            return self.agent_by_name("developer")
        elif self.proposals and len(self.messages) % 4 == 0:
            # Time for voting round
            return self.agent_by_name("product_manager")  # Moderator
        else:
            # Continue discussion
            return super().select_speaker(last_speaker, selector)

# Create consensus-driven group chat
consensus_chat = ConsensusGroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=20,
    consensus_threshold=0.6  # 60% agreement needed
)

consensus_manager = GroupChatManager(
    groupchat=consensus_chat,
    llm_config=llm_config
)
```

## Group Chat with Tools

### Collaborative Tool Usage

```python
# Create agents with different tool sets
researcher = AssistantAgent(
    name="researcher",
    system_message="Research technical topics and gather information.",
    llm_config=llm_config
)

# Register research tools
def search_technical_docs(query):
    # Mock technical documentation search
    return f"Found documentation for: {query}"

def analyze_codebase(repo_url):
    # Mock codebase analysis
    return f"Analysis of {repo_url}: Well-structured, 85% test coverage"

researcher.register_function(search_technical_docs)
researcher.register_function(analyze_codebase)

developer = AssistantAgent(
    name="developer",
    system_message="Implement technical solutions based on research.",
    llm_config=llm_config
)

# Register development tools
def write_code(specification):
    return f"Code implementation for: {specification}"

def run_tests(code):
    return "All tests passed" if "error" not in code.lower() else "Tests failed"

developer.register_function(write_code)
developer.register_function(run_tests)

# Create collaborative group chat with tools
tool_group_chat = GroupChat(
    agents=[user_proxy, researcher, developer],
    messages=[],
    max_round=10,
    speaker_selection_method="auto"
)

tool_manager = GroupChatManager(
    groupchat=tool_group_chat,
    llm_config=llm_config
)

# Collaborative task with tool usage
user_proxy.initiate_chat(
    tool_manager,
    message="Research and implement a REST API for user management with proper error handling."
)
```

## Monitoring and Analytics

### Group Chat Analytics

```python
class AnalyticsGroupChat(GroupChat):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analytics = {
            "message_count": 0,
            "agent_contributions": {},
            "topic_shifts": [],
            "consensus_points": []
        }

    def send(self, message, recipient, request_reply=True):
        """Override send to track analytics"""
        # Track message
        self.analytics["message_count"] += 1

        # Track agent contributions
        sender_name = message.get("name") if isinstance(message, dict) else "unknown"
        self.analytics["agent_contributions"][sender_name] = \
            self.analytics["agent_contributions"].get(sender_name, 0) + 1

        # Detect topic shifts (simplified)
        content = message.get("content", "") if isinstance(message, dict) else str(message)
        if len(content.split()) > 50:  # Long message might indicate topic shift
            self.analytics["topic_shifts"].append({
                "round": len(self.messages),
                "content_preview": content[:100]
            })

        return super().send(message, recipient, request_reply)

    def get_analytics_report(self):
        """Generate analytics report"""
        total_messages = self.analytics["message_count"]
        contributions = self.analytics["agent_contributions"]

        report = f"""
Group Chat Analytics Report:
===========================
Total Messages: {total_messages}
Topic Shifts: {len(self.analytics['topic_shifts'])}

Agent Contributions:
{chr(10).join(f"- {agent}: {count} messages ({count/total_messages*100:.1f}%)"
               for agent, count in contributions.items())}

Topic Shifts:
{chr(10).join(f"- Round {shift['round']}: {shift['content_preview']}..."
               for shift in self.analytics['topic_shifts'])}
"""
        return report

# Create analytics-enabled group chat
analytics_chat = AnalyticsGroupChat(
    agents=[user_proxy, product_manager, designer, developer, qa_specialist],
    messages=[],
    max_round=15,
    speaker_selection_method="auto"
)

analytics_manager = GroupChatManager(
    groupchat=analytics_chat,
    llm_config=llm_config
)

# Run discussion
user_proxy.initiate_chat(
    analytics_manager,
    message="Design a new feature for our mobile app."
)

# Get analytics report
print(analytics_chat.get_analytics_report())
```

## Best Practices

### Group Composition
- **Diverse Expertise**: Include agents with complementary skills
- **Size Management**: Keep groups to 3-7 agents for optimal collaboration
- **Role Clarity**: Ensure each agent has a clear, non-overlapping role
- **Personality Balance**: Mix different communication styles

### Conversation Management
- **Clear Goals**: Start with specific, achievable objectives
- **Progress Tracking**: Monitor conversation progress and redirect when needed
- **Time Boxing**: Set round limits to prevent runaway discussions
- **Summarization**: Periodically summarize progress and decisions

### Speaker Selection
- **Context Awareness**: Use auto-selection for dynamic, context-aware conversations
- **Fair Participation**: Ensure all agents contribute appropriately
- **Expert Matching**: Route questions to agents with relevant expertise
- **Phase Transitions**: Change speaker selection logic as discussion phases change

### Quality Assurance
- **Decision Tracking**: Log important decisions and rationales
- **Consensus Building**: Ensure decisions have proper buy-in
- **Action Items**: Clearly identify next steps and responsibilities
- **Follow-up**: Schedule follow-up discussions for complex topics

### Performance Optimization
- **Message Limits**: Implement message history limits to manage context
- **Caching**: Cache common agent configurations and responses
- **Parallel Processing**: Use async patterns for independent agent tasks
- **Resource Monitoring**: Track token usage and computational costs

## Summary

In this chapter, we've explored:

- **Basic Group Chat**: Round-robin and auto speaker selection
- **Custom Speaker Selection**: Role-based and expertise-based selection
- **Advanced Patterns**: Hierarchical teams and consensus-driven discussions
- **Tool Integration**: Collaborative tool usage in group settings
- **Analytics**: Monitoring and analyzing group chat performance
- **Best Practices**: Composition, management, and optimization strategies

Next, we'll cover **advanced patterns** - nested chats, caching, and production optimization.

---

**Ready for the next chapter?** [Chapter 7: Advanced Patterns](07-advanced-patterns.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*