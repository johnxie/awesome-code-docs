---
layout: default
title: "Phidata Tutorial - Chapter 6: Advanced Reasoning"
nav_order: 6
has_children: false
parent: Phidata Tutorial
---

# Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving

Welcome to **Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving**. In this part of **Phidata Tutorial: Building Autonomous AI Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


> Implement sophisticated reasoning patterns, chain-of-thought processing, and multi-step problem-solving strategies in Phidata agents.

## Chain-of-Thought Reasoning

### Structured Reasoning Process

```python
from phidata.agent import Agent
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class ReasoningStep(BaseModel):
    step_number: int
    description: str
    reasoning: str
    conclusion: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)

class ChainOfThoughtAgent(Agent):
    """Agent with structured chain-of-thought reasoning."""

    def __init__(self, reasoning_steps: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.reasoning_steps = reasoning_steps or [
            "analyze_problem",
            "gather_information",
            "evaluate_options",
            "make_decision",
            "plan_implementation"
        ]

    def reason_step_by_step(self, problem: str) -> Dict[str, Any]:
        """Execute structured reasoning process."""

        reasoning_trace = []
        current_context = f"Problem: {problem}"

        for i, step_name in enumerate(self.reasoning_steps, 1):
            # Execute reasoning step
            step_prompt = self._create_step_prompt(step_name, current_context, i)

            step_result = self.run(step_prompt)

            # Parse step result (simplified)
            step_analysis = ReasoningStep(
                step_number=i,
                description=step_name.replace("_", " ").title(),
                reasoning=step_result,
                conclusion=self._extract_conclusion(step_result),
                confidence=self._assess_confidence(step_result),
                evidence=self._extract_evidence(step_result)
            )

            reasoning_trace.append(step_analysis)

            # Update context for next step
            current_context += f"\n\nStep {i} ({step_name}): {step_result}"

        # Final synthesis
        synthesis = self._synthesize_reasoning(reasoning_trace, problem)

        return {
            "problem": problem,
            "reasoning_trace": reasoning_trace,
            "final_answer": synthesis["answer"],
            "confidence": synthesis["confidence"],
            "alternative_considerations": synthesis["alternatives"]
        }

    def _create_step_prompt(self, step_name: str, context: str, step_number: int) -> str:
        """Create prompt for specific reasoning step."""

        step_instructions = {
            "analyze_problem": """
            Break down the problem into its core components:
            1. What is the main question or challenge?
            2. What are the key constraints and requirements?
            3. What information do we have vs. what do we need?
            4. What are the success criteria?
            """,

            "gather_information": """
            Identify what additional information would be helpful:
            1. What facts or data do we need?
            2. What assumptions are we making?
            3. What are the potential sources of information?
            4. How can we validate the information we gather?
            """,

            "evaluate_options": """
            Consider different approaches or solutions:
            1. What are the possible options?
            2. What are the pros and cons of each?
            3. What are the risks and trade-offs?
            4. How do they align with our constraints and goals?
            """,

            "make_decision": """
            Choose the best option based on the analysis:
            1. Which option best meets our criteria?
            2. What evidence supports this choice?
            3. What are the potential downsides?
            4. Are there any deal-breakers?
            """,

            "plan_implementation": """
            Create a concrete plan for execution:
            1. What are the specific steps needed?
            2. What resources are required?
            3. What is the timeline?
            4. How will we measure success?
            """
        }

        instructions = step_instructions.get(step_name, "Analyze this step carefully.")

        return f"""
        Context so far:
        {context}

        Current Step {step_number}: {step_name.replace("_", " ").title()}

        Instructions:
        {instructions}

        Provide a clear, reasoned analysis for this step.
        """

    def _extract_conclusion(self, step_result: str) -> str:
        """Extract key conclusion from step result."""
        # Simple extraction - look for conclusion markers
        lines = step_result.split('\n')
        for line in lines:
            if any(marker in line.lower() for marker in ["conclusion:", "therefore:", "thus:", "so:"]):
                return line.strip()

        # Return last meaningful sentence
        sentences = [s.strip() for s in step_result.split('.') if s.strip()]
        return sentences[-1] if sentences else step_result[:100]

    def _assess_confidence(self, step_result: str) -> float:
        """Assess confidence level in the reasoning."""
        confidence_indicators = {
            "certain": 0.9,
            "confident": 0.8,
            "likely": 0.7,
            "probably": 0.6,
            "possible": 0.5,
            "uncertain": 0.4,
            "unlikely": 0.3,
            "doubtful": 0.2
        }

        result_lower = step_result.lower()
        for indicator, score in confidence_indicators.items():
            if indicator in result_lower:
                return score

        return 0.5  # Default moderate confidence

    def _extract_evidence(self, step_result: str) -> List[str]:
        """Extract evidence or supporting points."""
        evidence_markers = ["because", "since", "due to", "evidence:", "based on", "according to"]
        evidence = []

        lines = step_result.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(marker in line_lower for marker in evidence_markers):
                evidence.append(line.strip())

        return evidence[:3]  # Limit to top 3 pieces of evidence

    def _synthesize_reasoning(self, reasoning_trace: List[ReasoningStep], original_problem: str) -> Dict[str, Any]:
        """Synthesize final answer from reasoning trace."""

        synthesis_prompt = f"""
        Based on this step-by-step reasoning process, provide a final answer:

        Original Problem: {original_problem}

        Reasoning Steps:
        {chr(10).join([f"{step.step_number}. {step.description}: {step.conclusion}" for step in reasoning_trace])}

        Provide:
        1. A clear final answer
        2. Overall confidence level (0-1)
        3. Any alternative considerations or caveats
        4. Key evidence supporting the conclusion

        Format as JSON.
        """

        synthesis_result = self.run(synthesis_prompt)

        # Parse JSON response (simplified)
        try:
            import json
            parsed = json.loads(synthesis_result)
            return {
                "answer": parsed.get("final_answer", synthesis_result),
                "confidence": parsed.get("confidence", 0.5),
                "alternatives": parsed.get("alternative_considerations", [])
            }
        except:
            return {
                "answer": synthesis_result,
                "confidence": 0.5,
                "alternatives": []
            }

# Create chain-of-thought agent
cot_agent = ChainOfThoughtAgent(
    name="ReasoningAgent",
    instructions="You are an expert at structured reasoning and problem-solving.",
    model="gpt-4"
)

# Demonstrate chain-of-thought reasoning
complex_problem = """
Should our company invest $2M in developing a new AI-powered customer service chatbot?
Consider market demand, technical feasibility, ROI projections, competitive landscape,
and potential risks.
"""

print("Solving complex problem with chain-of-thought reasoning...")
reasoning_result = cot_agent.reason_step_by_step(complex_problem)

print(f"Problem: {reasoning_result['problem'][:100]}...")
print(f"\nReasoning Steps: {len(reasoning_result['reasoning_trace'])}")
print(f"Final Answer: {reasoning_result['final_answer'][:200]}...")
print(f"Confidence: {reasoning_result['confidence']}")

# Show detailed reasoning trace
print("\nDetailed Reasoning Trace:")
for step in reasoning_result['reasoning_trace']:
    print(f"\nStep {step.step_number}: {step.description}")
    print(f"Conclusion: {step.conclusion}")
    print(f"Confidence: {step.confidence}")
    if step.evidence:
        print(f"Evidence: {step.evidence[0]}")
```

## Tree-of-Thought Reasoning

### Branching Reasoning Paths

```python
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio

@dataclass
class ReasoningBranch:
    branch_id: str
    parent_id: Optional[str]
    depth: int
    hypothesis: str
    evidence: List[str]
    confidence: float
    children: List['ReasoningBranch'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

class TreeOfThoughtAgent(Agent):
    """Agent implementing tree-of-thought reasoning."""

    def __init__(self, max_depth: int = 3, branching_factor: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.max_depth = max_depth
        self.branching_factor = branching_factor

    async def reason_tree_of_thought(self, problem: str) -> Dict[str, Any]:
        """Execute tree-of-thought reasoning."""

        # Create root branch
        root = ReasoningBranch(
            branch_id="root",
            parent_id=None,
            depth=0,
            hypothesis=f"Initial problem: {problem}",
            evidence=[],
            confidence=0.5
        )

        # Build reasoning tree
        await self._expand_tree(root, problem)

        # Evaluate and select best path
        best_path = self._find_best_path(root)

        # Synthesize final answer
        final_answer = await self._synthesize_from_path(best_path, problem)

        return {
            "problem": problem,
            "reasoning_tree": root,
            "best_path": best_path,
            "final_answer": final_answer,
            "tree_stats": self._analyze_tree(root)
        }

    async def _expand_tree(self, branch: ReasoningBranch, original_problem: str):
        """Recursively expand reasoning tree."""

        if branch.depth >= self.max_depth:
            return

        # Generate hypotheses for this branch
        hypotheses = await self._generate_hypotheses(branch, original_problem)

        # Create child branches
        for i, hypothesis in enumerate(hypotheses[:self.branching_factor]):
            child_branch = ReasoningBranch(
                branch_id=f"{branch.branch_id}_{i}",
                parent_id=branch.branch_id,
                depth=branch.depth + 1,
                hypothesis=hypothesis,
                evidence=[],  # Will be populated
                confidence=0.5
            )

            # Evaluate hypothesis and gather evidence
            evaluation = await self._evaluate_hypothesis(child_branch, original_problem)
            child_branch.confidence = evaluation["confidence"]
            child_branch.evidence = evaluation["evidence"]

            branch.children.append(child_branch)

            # Recursively expand
            await self._expand_tree(child_branch, original_problem)

    async def _generate_hypotheses(self, branch: ReasoningBranch, problem: str) -> List[str]:
        """Generate possible hypotheses or next steps."""

        hypothesis_prompt = f"""
        Based on this reasoning branch, generate {self.branching_factor} possible next steps or hypotheses:

        Current branch: {branch.hypothesis}
        Problem: {problem}

        Generate diverse, plausible hypotheses that could advance the reasoning.
        Each hypothesis should be a clear statement or proposed action.
        """

        response = self.run(hypothesis_prompt)

        # Parse hypotheses (simplified - assume numbered list)
        lines = response.split('\n')
        hypotheses = []

        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Extract hypothesis text
                if line[0].isdigit():
                    hypothesis = line.split('.', 1)[1].strip() if '.' in line else line
                else:
                    hypothesis = line[1:].strip()

                hypotheses.append(hypothesis)

        return hypotheses[:self.branching_factor]

    async def _evaluate_hypothesis(self, branch: ReasoningBranch, problem: str) -> Dict[str, Any]:
        """Evaluate hypothesis and gather supporting evidence."""

        evaluation_prompt = f"""
        Evaluate this hypothesis in the context of the problem:

        Problem: {problem}
        Hypothesis: {branch.hypothesis}

        Provide:
        1. Confidence score (0-1) for this hypothesis
        2. Key evidence supporting it
        3. Potential counter-evidence or limitations

        Be thorough but concise.
        """

        response = self.run(evaluation_prompt)

        # Parse evaluation (simplified)
        confidence = 0.5  # Default
        evidence = []

        lines = response.split('\n')
        for line in lines:
            line_lower = line.lower()
            if 'confidence' in line_lower:
                # Extract number
                import re
                numbers = re.findall(r'0\.\d+', line)
                if numbers:
                    confidence = float(numbers[0])

            if any(word in line_lower for word in ['evidence', 'support', 'because']):
                evidence.append(line.strip())

        return {
            "confidence": confidence,
            "evidence": evidence[:3]  # Limit evidence
        }

    def _find_best_path(self, root: ReasoningBranch) -> List[ReasoningBranch]:
        """Find the path with highest confidence."""

        def traverse_and_score(branch: ReasoningBranch) -> tuple[float, List[ReasoningBranch]]:
            if not branch.children:
                return branch.confidence, [branch]

            best_score = 0
            best_path = []

            for child in branch.children:
                child_score, child_path = traverse_and_score(child)
                combined_score = (branch.confidence + child_score) / 2

                if combined_score > best_score:
                    best_score = combined_score
                    best_path = [branch] + child_path

            return best_score, best_path

        _, best_path = traverse_and_score(root)
        return best_path

    async def _synthesize_from_path(self, path: List[ReasoningBranch], problem: str) -> str:
        """Synthesize final answer from best reasoning path."""

        path_summary = "\n".join([
            f"Step {i+1}: {branch.hypothesis} (confidence: {branch.confidence:.2f})"
            for i, branch in enumerate(path)
        ])

        synthesis_prompt = f"""
        Based on this reasoning path, provide a final answer to the problem:

        Problem: {problem}

        Reasoning Path:
        {path_summary}

        Provide a clear, well-reasoned final answer that synthesizes the key insights from the reasoning process.
        """

        return self.run(synthesis_prompt)

    def _analyze_tree(self, root: ReasoningBranch) -> Dict[str, Any]:
        """Analyze reasoning tree statistics."""

        def count_nodes(branch: ReasoningBranch) -> int:
            return 1 + sum(count_nodes(child) for child in branch.children)

        def max_depth(branch: ReasoningBranch) -> int:
            if not branch.children:
                return branch.depth
            return max(max_depth(child) for child in branch.children)

        def avg_confidence(branch: ReasoningBranch) -> float:
            confidences = []

            def collect_confidences(b: ReasoningBranch):
                confidences.append(b.confidence)
                for child in b.children:
                    collect_confidences(child)

            collect_confidences(branch)
            return sum(confidences) / len(confidences) if confidences else 0

        return {
            "total_nodes": count_nodes(root),
            "max_depth": max_depth(root),
            "avg_confidence": avg_confidence(root)
        }

# Create tree-of-thought agent
tot_agent = TreeOfThoughtAgent(
    name="TreeOfThoughtAgent",
    instructions="You are an expert at complex reasoning and exploring multiple solution paths.",
    model="gpt-4",
    max_depth=2,
    branching_factor=2
)

# Demonstrate tree-of-thought reasoning
complex_reasoning_problem = """
Design a strategy for a startup to enter the AI-powered education market.
Consider current market trends, competitive landscape, technical requirements,
monetization models, and potential risks.
"""

print("Solving complex problem with tree-of-thought reasoning...")
tot_result = asyncio.run(tot_agent.reason_tree_of_thought(complex_reasoning_problem))

print(f"Problem: {tot_result['problem'][:100]}...")
print(f"Reasoning Tree: {tot_result['tree_stats']['total_nodes']} nodes")
print(f"Max Depth: {tot_result['tree_stats']['max_depth']}")
print(f"Average Confidence: {tot_result['tree_stats']['avg_confidence']:.2f}")
print(f"Best Path Length: {len(tot_result['best_path'])}")
print(f"\nFinal Answer: {tot_result['final_answer'][:300]}...")
```

## Self-Reflection and Meta-Reasoning

### Reflective Reasoning Agent

```python
class ReflectiveAgent(Agent):
    """Agent that can reflect on its own reasoning and improve."""

    def __init__(self, reflection_model: str = "gpt-3.5-turbo", **kwargs):
        super().__init__(**kwargs)
        self.reflection_model = reflection_model
        self.reasoning_history = []
        self.performance_metrics = {
            "total_reasoning_sessions": 0,
            "average_confidence": 0,
            "success_rate": 0,
            "common_errors": []
        }

    async def reflective_reason(self, problem: str, max_iterations: int = 3) -> Dict[str, Any]:
        """Execute reasoning with self-reflection and improvement."""

        reasoning_session = {
            "problem": problem,
            "iterations": [],
            "final_answer": None,
            "reflection_insights": []
        }

        current_answer = None
        current_confidence = 0

        for iteration in range(max_iterations):
            # Generate answer
            iteration_prompt = self._create_iteration_prompt(
                problem, current_answer, current_confidence, iteration
            )

            new_answer = self.run(iteration_prompt)

            # Evaluate answer
            evaluation = await self._reflect_on_answer(new_answer, problem)

            reasoning_session["iterations"].append({
                "iteration": iteration + 1,
                "answer": new_answer,
                "evaluation": evaluation
            })

            # Check if we should continue
            if evaluation["confidence"] > 0.8 and evaluation["should_stop"]:
                break

            current_answer = new_answer
            current_confidence = evaluation["confidence"]

        # Final reflection
        final_reflection = await self._final_reflection(reasoning_session)

        reasoning_session.update({
            "final_answer": final_reflection["best_answer"],
            "confidence": final_reflection["confidence"],
            "reflection_insights": final_reflection["insights"]
        })

        # Update performance metrics
        self._update_performance_metrics(reasoning_session)

        return reasoning_session

    def _create_iteration_prompt(self, problem: str, previous_answer: str = None,
                               previous_confidence: float = 0, iteration: int = 0) -> str:
        """Create prompt for reasoning iteration."""

        base_prompt = f"""
        Solve this problem: {problem}

        This is reasoning iteration {iteration + 1}.
        """

        if previous_answer:
            base_prompt += f"""

            Your previous answer (confidence: {previous_confidence:.2f}):
            {previous_answer}

            Reflect on this answer and provide an improved solution.
            Consider what might be wrong or incomplete in the previous reasoning.
            """

        base_prompt += """

        Provide a clear, well-reasoned answer with your confidence level.
        """

        return base_prompt

    async def _reflect_on_answer(self, answer: str, problem: str) -> Dict[str, Any]:
        """Reflect on the quality of an answer."""

        reflection_prompt = f"""
        Evaluate this answer to the problem:

        Problem: {problem}
        Answer: {answer}

        Provide an evaluation including:
        1. Strengths of the answer
        2. Weaknesses or potential issues
        3. Confidence level (0-1)
        4. Whether you should continue refining (yes/no)
        5. Specific suggestions for improvement

        Be critical but constructive.
        """

        # Use reflection model for evaluation
        reflection_agent = Agent(
            name="ReflectionAgent",
            instructions="You are an expert at evaluating reasoning and problem-solving.",
            model=self.reflection_model
        )

        reflection = reflection_agent.run(reflection_prompt)

        # Parse reflection (simplified)
        confidence = 0.5
        should_stop = False

        reflection_lower = reflection.lower()
        if "confiden" in reflection_lower:
            # Extract confidence number
            import re
            numbers = re.findall(r'0\.\d+', reflection)
            if numbers:
                confidence = float(numbers[0])

        if any(word in reflection_lower for word in ["good enough", "satisfactory", "should stop", "final"]):
            should_stop = True

        return {
            "reflection": reflection,
            "confidence": confidence,
            "should_stop": should_stop,
            "strengths": [],  # Would parse from reflection
            "weaknesses": [],  # Would parse from reflection
            "suggestions": []  # Would parse from reflection
        }

    async def _final_reflection(self, reasoning_session: Dict[str, Any]) -> Dict[str, Any]:
        """Provide final reflection on the reasoning process."""

        iterations_summary = "\n".join([
            f"Iteration {it['iteration']}: {it['answer'][:100]}... (confidence: {it['evaluation']['confidence']:.2f})"
            for it in reasoning_session["iterations"]
        ])

        final_reflection_prompt = f"""
        Review this reasoning process and provide final insights:

        Problem: {reasoning_session['problem']}

        Reasoning Iterations:
        {iterations_summary}

        Provide:
        1. The best final answer
        2. Overall confidence in the solution
        3. Key insights gained during the reasoning process
        4. Lessons learned for future reasoning
        """

        final_reflection = self.run(final_reflection_prompt)

        # Parse final reflection (simplified)
        return {
            "best_answer": final_reflection,
            "confidence": 0.8,  # Would parse from reflection
            "insights": ["Iterative improvement", "Self-reflection"]  # Would parse from reflection
        }

    def _update_performance_metrics(self, reasoning_session: Dict[str, Any]):
        """Update performance tracking."""

        self.performance_metrics["total_reasoning_sessions"] += 1

        session_confidence = reasoning_session.get("confidence", 0.5)
        current_avg = self.performance_metrics["average_confidence"]
        total_sessions = self.performance_metrics["total_reasoning_sessions"]

        # Update running average
        self.performance_metrics["average_confidence"] = (
            (current_avg * (total_sessions - 1)) + session_confidence
        ) / total_sessions

# Create reflective agent
reflective_agent = ReflectiveAgent(
    name="ReflectiveReasoningAgent",
    instructions="You are an expert at complex reasoning with self-reflection capabilities.",
    model="gpt-4",
    reflection_model="gpt-3.5-turbo"
)

# Demonstrate reflective reasoning
reflection_problem = """
Design a comprehensive strategy for a company to adopt AI technologies.
Consider organizational culture, technical infrastructure, talent acquisition,
change management, and ROI measurement.
"""

print("Solving problem with reflective reasoning...")
reflection_result = asyncio.run(reflective_agent.reflective_reason(reflection_problem, max_iterations=2))

print(f"Problem: {reflection_result['problem'][:100]}...")
print(f"Iterations: {len(reflection_result['iterations'])}")
print(f"Final Confidence: {reflection_result['confidence']}")
print(f"Key Insights: {reflection_result['reflection_insights']}")
print(f"\nFinal Answer: {reflection_result['final_answer'][:300]}...")

# Show performance metrics
print("
Agent Performance Metrics:")
for metric, value in reflective_agent.performance_metrics.items():
    print(f"{metric}: {value}")
```

## Reasoning Pattern Libraries

### Specialized Reasoning Templates

```python
from typing import Dict, List, Any, Callable
from abc import ABC, abstractmethod

class ReasoningPattern(ABC):
    """Base class for reasoning patterns."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def apply_pattern(self, agent: Agent, problem: str) -> Dict[str, Any]:
        """Apply the reasoning pattern."""
        pass

class SWOTAnalysis(ReasoningPattern):
    """SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis."""

    @property
    def name(self) -> str:
        return "swot_analysis"

    @property
    def description(self) -> str:
        return "Analyze situation using Strengths, Weaknesses, Opportunities, Threats framework"

    def apply_pattern(self, agent: Agent, problem: str) -> Dict[str, Any]:
        swot_prompt = f"""
        Conduct a SWOT analysis for this situation:

        Situation: {problem}

        Provide a structured analysis covering:

        STRENGTHS (Internal positive factors):
        - List key strengths

        WEAKNESSES (Internal negative factors):
        - List key weaknesses

        OPPORTUNITIES (External positive factors):
        - List key opportunities

        THREATS (External negative factors):
        - List key threats

        Then provide strategic recommendations based on the SWOT analysis.
        """

        analysis = agent.run(swot_prompt)

        return {
            "pattern": self.name,
            "analysis": analysis,
            "structured_output": self._parse_swot(analysis)
        }

    def _parse_swot(self, analysis: str) -> Dict[str, List[str]]:
        """Parse SWOT analysis into structured format."""
        sections = {
            "strengths": [],
            "weaknesses": [],
            "opportunities": [],
            "threats": []
        }

        current_section = None
        lines = analysis.split('\n')

        for line in lines:
            line = line.strip().upper()
            if "STRENGTH" in line:
                current_section = "strengths"
            elif "WEAKNESSE" in line:
                current_section = "weaknesses"
            elif "OPPORTUNIT" in line:
                current_section = "opportunities"
            elif "THREAT" in line:
                current_section = "threats"
            elif current_section and line.startswith('-'):
                sections[current_section].append(line[1:].strip())

        return sections

class DecisionTreeAnalysis(ReasoningPattern):
    """Decision tree analysis for complex choices."""

    @property
    def name(self) -> str:
        return "decision_tree"

    @property
    def description(self) -> str:
        return "Analyze decision using structured decision tree approach"

    def apply_pattern(self, agent: Agent, problem: str) -> Dict[str, Any]:
        dt_prompt = f"""
        Create a decision tree analysis for this decision:

        Decision: {problem}

        Structure your analysis as follows:

        1. INITIAL DECISION POINT
           - What is the main decision to make?

        2. KEY FACTORS
           - What are the critical factors influencing the decision?

        3. POSSIBLE OPTIONS
           - List main alternatives

        4. DECISION BRANCHES
           For each option, analyze:
           - Likely outcomes
           - Probability of success
           - Resource requirements
           - Risk factors

        5. RECOMMENDED DECISION
           - Which option do you recommend?
           - Why?
           - What are the key trade-offs?

        Be thorough and consider both quantitative and qualitative factors.
        """

        analysis = agent.run(dt_prompt)

        return {
            "pattern": self.name,
            "analysis": analysis
        }

class RootCauseAnalysis(ReasoningPattern):
    """5-Why root cause analysis."""

    @property
    def name(self) -> str:
        return "root_cause"

    @property
    def description(self) -> str:
        return "Apply 5-Why technique to identify root causes"

    def apply_pattern(self, agent: Agent, problem: str) -> Dict[str, Any]:
        rca_prompt = f"""
        Apply 5-Why root cause analysis to this problem:

        Problem: {problem}

        Use the 5-Why technique:
        1. Start with the problem statement
        2. Ask "Why?" to dig deeper
        3. Continue asking "Why?" until you reach the root cause
        4. Aim for 5 levels of analysis

        Structure your analysis as:

        PROBLEM: [Initial problem]

        WHY 1: [First level reason]
        WHY 2: [Why did that happen?]
        WHY 3: [Why did that happen?]
        WHY 4: [Why did that happen?]
        WHY 5: [Root cause]

        Then provide recommendations to address the root cause.
        """

        analysis = agent.run(rca_prompt)

        return {
            "pattern": self.name,
            "analysis": analysis,
            "root_cause": self._extract_root_cause(analysis)
        }

    def _extract_root_cause(self, analysis: str) -> str:
        """Extract the root cause from 5-Why analysis."""
        lines = analysis.split('\n')
        for line in lines:
            if line.upper().startswith('WHY 5:') or 'ROOT CAUSE' in line.upper():
                return line.split(':', 1)[1].strip() if ':' in line else line.strip()

        return "Root cause not clearly identified"

class ReasoningPatternLibrary:
    """Library of reasoning patterns."""

    def __init__(self):
        self.patterns: Dict[str, ReasoningPattern] = {}

    def register_pattern(self, pattern: ReasoningPattern):
        """Register a reasoning pattern."""
        self.patterns[pattern.name] = pattern

    def get_pattern(self, name: str) -> ReasoningPattern:
        """Get a reasoning pattern."""
        return self.patterns.get(name)

    def list_patterns(self) -> Dict[str, str]:
        """List available patterns."""
        return {name: pattern.description for name, pattern in self.patterns.items()}

    def apply_pattern(self, agent: Agent, pattern_name: str, problem: str) -> Dict[str, Any]:
        """Apply a reasoning pattern."""
        pattern = self.get_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern {pattern_name} not found")

        return pattern.apply_pattern(agent, problem)

# Create pattern library
pattern_library = ReasoningPatternLibrary()

# Register patterns
pattern_library.register_pattern(SWOTAnalysis())
pattern_library.register_pattern(DecisionTreeAnalysis())
pattern_library.register_pattern(RootCauseAnalysis())

# Demonstrate pattern usage
reasoning_agent = Agent(
    name="PatternReasoningAgent",
    instructions="You are an expert at applying structured reasoning patterns.",
    model="gpt-4"
)

# Apply different patterns to the same problem
problem = "Our company's customer satisfaction scores have dropped 15% in the last quarter."

patterns_to_apply = ["swot_analysis", "root_cause"]

print("Applying reasoning patterns to problem analysis...")
for pattern_name in patterns_to_apply:
    print(f"\n=== Applying {pattern_name.replace('_', ' ').title()} ===")

    result = pattern_library.apply_pattern(reasoning_agent, pattern_name, problem)

    print(f"Pattern: {result['pattern']}")
    print(f"Analysis: {result['analysis'][:300]}...")

    if 'structured_output' in result:
        print(f"Structured Output: {result['structured_output']}")

    if 'root_cause' in result:
        print(f"Root Cause: {result['root_cause']}")

print(f"\nAvailable patterns: {list(pattern_library.list_patterns().keys())}")
```

This advanced reasoning chapter demonstrates sophisticated reasoning techniques including chain-of-thought, tree-of-thought, self-reflection, and specialized reasoning patterns that enable agents to tackle complex problems systematically. 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `problem`, `reasoning` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving` as an operating subsystem inside **Phidata Tutorial: Building Autonomous AI Agents**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `confidence`, `line`, `branch` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 6: Advanced Reasoning - Complex Decision Making and Problem Solving` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `problem` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `reasoning`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/phidatahq/phidata)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `problem` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 5: Multi-Agent Systems - Coordinating Teams of AI Agents](05-multi-agent-systems.md)
- [Next Chapter: Chapter 7: Integrations - Connecting Phidata Agents to External Systems](07-integrations.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
