---
layout: default
title: "Chapter 7: Advanced Chains"
parent: "LangChain Tutorial"
nav_order: 7
---

# Chapter 7: Advanced Chains

Welcome to advanced LangChain chains! In this chapter, we'll explore complex workflow patterns, custom chain development, and sophisticated implementations that go beyond basic sequential chains. You'll learn how to build production-ready, scalable chain architectures.

## Custom Chain Development

### Base Chain Classes

```python
from langchain.chains.base import Chain
from langchain.schema import BaseLanguageModel, BaseOutputParser
from typing import Dict, Any, List, Optional
from langchain.prompts import BasePromptTemplate
from langchain.callbacks.manager import CallbackManagerForChainRun

class CustomChain(Chain):
    """Base class for custom chains"""

    llm: BaseLanguageModel
    prompt: BasePromptTemplate
    output_parser: Optional[BaseOutputParser] = None

    @property
    def input_keys(self) -> List[str]:
        """Input keys for the chain"""
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        """Output keys for the chain"""
        return ["output"]

    def _call(self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None) -> Dict[str, Any]:
        """Execute the chain"""
        # Format the prompt
        formatted_prompt = self.prompt.format(**inputs)

        # Call the LLM
        if run_manager:
            response = run_manager.run_sync(self.llm.predict, formatted_prompt)
        else:
            response = self.llm.predict(formatted_prompt)

        # Parse output if parser is provided
        if self.output_parser:
            parsed_output = self.output_parser.parse(response)
            return {"output": parsed_output}
        else:
            return {"output": response}

    async def _acall(self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None) -> Dict[str, Any]:
        """Async version of _call"""
        # Format the prompt
        formatted_prompt = self.prompt.format(**inputs)

        # Call the LLM asynchronously
        if run_manager:
            response = await run_manager.run_async(self.llm.apredict, formatted_prompt)
        else:
            response = await self.llm.apredict(formatted_prompt)

        # Parse output if parser is provided
        if self.output_parser:
            parsed_output = self.output_parser.parse(response)
            return {"output": parsed_output}
        else:
            return {"output": response}
```

### Specialized Chain Types

```python
from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.prompts import PromptTemplate
from typing import Dict, Any, List

class ResearchAnalysisChain(CustomChain):
    """A chain that performs research and analysis"""

    def __init__(self, llm, research_prompt=None, analysis_prompt=None, **kwargs):
        super().__init__(llm=llm, **kwargs)

        self.research_prompt = research_prompt or PromptTemplate(
            input_variables=["topic"],
            template="""Research the following topic thoroughly:

Topic: {topic}

Provide comprehensive information including:
- Key concepts and definitions
- Current trends and developments
- Important facts and statistics
- Relevant examples and case studies

Research:"""
        )

        self.analysis_prompt = analysis_prompt or PromptTemplate(
            input_variables=["research_results"],
            template="""Analyze the following research results:

{research_results}

Provide:
1. Key insights and findings
2. Patterns and trends identified
3. Implications and recommendations
4. Areas for further investigation

Analysis:"""
        )

    @property
    def input_keys(self) -> List[str]:
        return ["topic"]

    @property
    def output_keys(self) -> List[str]:
        return ["research", "analysis", "summary"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        # Step 1: Research
        research_input = self.research_prompt.format(**inputs)
        research_results = self.llm.predict(research_input)

        # Step 2: Analysis
        analysis_input = self.analysis_prompt.format(research_results=research_results)
        analysis_results = self.llm.predict(analysis_input)

        # Step 3: Summary
        summary_prompt = f"""Create a concise summary of this research and analysis:

Research: {research_results[:500]}...
Analysis: {analysis_results[:500]}...

Summary:"""

        summary = self.llm.predict(summary_prompt)

        return {
            "research": research_results,
            "analysis": analysis_results,
            "summary": summary
        }

# Usage
research_chain = ResearchAnalysisChain(llm)
result = research_chain.run(topic="artificial intelligence in healthcare")
print(result["summary"])
```

## Complex Chain Architectures

### Multi-Branch Chains

```python
from langchain.chains.router import MultiRouteChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

class MultiBranchChain(Chain):
    """A chain that can route to different branches based on input"""

    def __init__(self, llm, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm
        self.branches = {}
        self.router_prompt = PromptTemplate(
            input_variables=["input"],
            template="""Analyze this input and determine the most appropriate branch:

Input: {input}

Available branches:
- research: For research and information gathering tasks
- analysis: For data analysis and interpretation tasks
- creative: For creative writing and content generation tasks
- technical: For technical problem solving and coding tasks

Respond with only the branch name:"""
        )

    def add_branch(self, name: str, chain: Chain):
        """Add a branch to the multi-branch chain"""
        self.branches[name] = chain

    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["branch", "result"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        # Determine the appropriate branch
        router_input = self.router_prompt.format(**inputs)
        branch_name = self.llm.predict(router_input).strip().lower()

        # Get the appropriate branch
        if branch_name not in self.branches:
            branch_name = "general"  # fallback

        branch_chain = self.branches.get(branch_name, self.branches.get("general"))

        if branch_chain:
            # Execute the branch
            branch_result = branch_chain.run(**inputs)
            return {
                "branch": branch_name,
                "result": branch_result
            }
        else:
            return {
                "branch": "none",
                "result": "No appropriate branch found for this input"
            }

# Usage
multi_branch = MultiBranchChain(llm)

# Add branches
multi_branch.add_branch("research", ResearchAnalysisChain(llm))
multi_branch.add_branch("creative", LLMChain(llm=llm, prompt=PromptTemplate(
    input_variables=["input"],
    template="Write a creative response to: {input}"
)))

result = multi_branch.run(input="Research the latest developments in quantum computing")
print(f"Used branch: {result['branch']}")
```

### Parallel Processing Chains

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain.chains import LLMChain

class ParallelProcessingChain(Chain):
    """A chain that processes multiple inputs in parallel"""

    def __init__(self, llm, processing_chain: Chain, max_workers: int = 4, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm
        self.processing_chain = processing_chain
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    @property
    def input_keys(self) -> List[str]:
        return ["inputs"]  # List of inputs to process

    @property
    def output_keys(self) -> List[str]:
        return ["results"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        input_list = inputs["inputs"]

        # Process inputs in parallel
        futures = []
        for single_input in input_list:
            future = self.executor.submit(
                self._process_single_input,
                single_input
            )
            futures.append(future)

        # Collect results
        results = []
        for future in futures:
            result = future.result()
            results.append(result)

        return {"results": results}

    def _process_single_input(self, input_data: Any) -> Any:
        """Process a single input using the processing chain"""
        if isinstance(input_data, dict):
            return self.processing_chain.run(**input_data)
        else:
            return self.processing_chain.run(input=input_data)

    async def _acall(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        """Async version with true parallelism"""
        input_list = inputs["inputs"]

        # Process in parallel using asyncio
        tasks = []
        for single_input in input_list:
            task = asyncio.create_task(
                self._aprocess_single_input(single_input)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return {"results": results}

    async def _aprocess_single_input(self, input_data: Any) -> Any:
        """Async version of single input processing"""
        if isinstance(input_data, dict):
            return await self.processing_chain.arun(**input_data)
        else:
            return await self.processing_chain.arun(input=input_data)

# Usage
parallel_chain = ParallelProcessingChain(
    llm=llm,
    processing_chain=LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            input_variables=["topic"],
            template="Summarize the key points about: {topic}"
        )
    )
)

results = parallel_chain.run(inputs=[
    {"topic": "Machine Learning"},
    {"topic": "Deep Learning"},
    {"topic": "Natural Language Processing"},
    {"topic": "Computer Vision"}
])

for i, result in enumerate(results["results"]):
    print(f"Summary {i+1}: {result[:100]}...")
```

## Chain Composition Patterns

### Chain of Chains

```python
class ChainOfChains(Chain):
    """A meta-chain that orchestrates multiple chains"""

    def __init__(self, chains: List[Chain], orchestration_logic=None, **kwargs):
        super().__init__(**kwargs)
        self.chains = chains
        self.orchestration_logic = orchestration_logic or self._default_orchestration

    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["final_result", "chain_results"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        chain_results = []
        current_input = inputs["input"]

        for i, chain in enumerate(self.chains):
            # Apply orchestration logic
            chain_input = self.orchestration_logic(current_input, chain_results, i)

            # Execute chain
            if isinstance(chain_input, dict):
                result = chain.run(**chain_input)
            else:
                result = chain.run(input=chain_input)

            chain_results.append(result)

            # Update input for next chain
            current_input = result

        # Generate final result
        final_result = self._synthesize_results(chain_results)

        return {
            "final_result": final_result,
            "chain_results": chain_results
        }

    def _default_orchestration(self, current_input: Any, previous_results: List, chain_index: int):
        """Default orchestration logic"""
        if chain_index == 0:
            return current_input
        else:
            # Pass the result from the previous chain
            return previous_results[-1]

    def _synthesize_results(self, chain_results: List) -> str:
        """Synthesize results from all chains"""
        synthesis_prompt = f"""Synthesize the results from this chain execution:

Chain Results:
{chr(10).join([f"Chain {i+1}: {str(result)[:200]}..." for i, result in enumerate(chain_results)])}

Provide a comprehensive final result:"""

        return self.llm.predict(synthesis_prompt)

# Usage
chains = [
    LLMChain(llm=llm, prompt=PromptTemplate(
        input_variables=["input"],
        template="Research and gather information about: {input}"
    )),
    LLMChain(llm=llm, prompt=PromptTemplate(
        input_variables=["input"],
        template="Analyze this information: {input}"
    )),
    LLMChain(llm=llm, prompt=PromptTemplate(
        input_variables=["input"],
        template="Create recommendations based on this analysis: {input}"
    ))
]

chain_of_chains = ChainOfChains(chains)
result = chain_of_chains.run(input="artificial intelligence trends")
print(result["final_result"])
```

### Dynamic Chain Builder

```python
class DynamicChainBuilder:
    """Builds chains dynamically based on requirements"""

    def __init__(self, llm):
        self.llm = llm
        self.chain_templates = {}

    def register_template(self, name: str, template_config: Dict[str, Any]):
        """Register a chain template"""
        self.chain_templates[name] = template_config

    def build_chain(self, requirements: Dict[str, Any]) -> Chain:
        """Build a chain based on requirements"""
        chain_type = requirements.get("type", "sequential")

        if chain_type == "research":
            return self._build_research_chain(requirements)
        elif chain_type == "analysis":
            return self._build_analysis_chain(requirements)
        elif chain_type == "creative":
            return self._build_creative_chain(requirements)
        else:
            return self._build_default_chain(requirements)

    def _build_research_chain(self, requirements: Dict[str, Any]) -> Chain:
        """Build a research-focused chain"""
        steps = requirements.get("steps", ["gather_info", "analyze", "summarize"])

        chains = []
        for step in steps:
            if step == "gather_info":
                chain = LLMChain(
                    llm=self.llm,
                    prompt=PromptTemplate(
                        input_variables=["topic"],
                        template="Gather comprehensive information about: {topic}"
                    )
                )
            elif step == "analyze":
                chain = LLMChain(
                    llm=self.llm,
                    prompt=PromptTemplate(
                        input_variables=["info"],
                        template="Analyze this information: {info}"
                    )
                )
            elif step == "summarize":
                chain = LLMChain(
                    llm=self.llm,
                    prompt=PromptTemplate(
                        input_variables=["analysis"],
                        template="Create a summary of this analysis: {analysis}"
                    )
                )
            chains.append(chain)

        return SequentialChain(
            chains=chains,
            input_variables=["topic"],
            output_variables=["analysis", "summary"]
        )

    def _build_analysis_chain(self, requirements: Dict[str, Any]) -> Chain:
        """Build an analysis-focused chain"""
        analysis_type = requirements.get("analysis_type", "general")

        if analysis_type == "data":
            return LLMChain(
                llm=self.llm,
                prompt=PromptTemplate(
                    input_variables=["data"],
                    template="Analyze this data and provide insights: {data}"
                )
            )
        else:
            return LLMChain(
                llm=self.llm,
                prompt=PromptTemplate(
                    input_variables=["content"],
                    template="Analyze this content: {content}"
                )
            )

# Usage
builder = DynamicChainBuilder(llm)

# Register templates
builder.register_template("research_template", {
    "type": "research",
    "steps": ["gather_info", "analyze", "summarize"]
})

# Build chains dynamically
research_chain = builder.build_chain({
    "type": "research",
    "steps": ["gather_info", "analyze", "summarize"]
})

result = research_chain.run(topic="renewable energy")
```

## Advanced Chain Features

### Chain with Memory Integration

```python
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

class MemoryEnhancedChain(Chain):
    """A chain that integrates with memory systems"""

    def __init__(self, llm, memory_type="buffer", memory_size=10, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm

        if memory_type == "buffer":
            self.memory = ConversationBufferWindowMemory(k=memory_size)
        elif memory_type == "summary":
            from langchain.memory import ConversationSummaryMemory
            self.memory = ConversationSummaryMemory(llm=llm)
        else:
            self.memory = ConversationBufferWindowMemory(k=memory_size)

        self.conversation_chain = ConversationChain(
            llm=llm,
            memory=self.memory,
            verbose=True
        )

    @property
    def input_keys(self) -> List[str]:
        return ["input"]

    @property
    def output_keys(self) -> List[str]:
        return ["response", "memory"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        # Get conversation history
        history = self.memory.load_memory_variables({})

        # Enhance input with context
        enhanced_input = f"""Context from previous conversations:
{history.get('history', '')}

Current input: {inputs['input']}

Please provide a response that takes into account our previous conversation:"""

        # Generate response
        response = self.llm.predict(enhanced_input)

        # Save to memory
        self.memory.save_context({"input": inputs["input"]}, {"output": response})

        return {
            "response": response,
            "memory": self.memory.load_memory_variables({})
        }

# Usage
memory_chain = MemoryEnhancedChain(llm, memory_type="buffer", memory_size=5)

# Have a conversation
result1 = memory_chain.run(input="Hello, I'm interested in learning about AI")
result2 = memory_chain.run(input="What did I just ask about?")
print(result2["response"])  # Should remember the previous context
```

### Chain with Error Handling and Retry Logic

```python
class ResilientChain(Chain):
    """A chain with built-in error handling and retry logic"""

    def __init__(self, base_chain: Chain, max_retries: int = 3, backoff_factor: float = 1.5, **kwargs):
        super().__init__(**kwargs)
        self.base_chain = base_chain
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    @property
    def input_keys(self) -> List[str]:
        return self.base_chain.input_keys

    @property
    def output_keys(self) -> List[str]:
        return self.base_chain.output_keys + ["retries", "errors"]

    def _call(self, inputs: Dict[str, Any], run_manager=None) -> Dict[str, Any]:
        errors = []
        last_result = None

        for attempt in range(self.max_retries + 1):
            try:
                result = self.base_chain._call(inputs, run_manager)
                return {
                    **result,
                    "retries": attempt,
                    "errors": errors
                }

            except Exception as e:
                error_info = {
                    "attempt": attempt + 1,
                    "error": str(e),
                    "timestamp": time.time()
                }
                errors.append(error_info)

                if attempt < self.max_retries:
                    # Exponential backoff
                    delay = self.backoff_factor ** attempt
                    time.sleep(delay)
                else:
                    # Final attempt failed
                    return {
                        "error": f"Chain failed after {self.max_retries + 1} attempts",
                        "last_result": last_result,
                        "retries": attempt,
                        "errors": errors
                    }

# Usage
base_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms"
    )
)

resilient_chain = ResilientChain(base_chain, max_retries=2)

result = resilient_chain.run(topic="quantum computing")
if "error" in result:
    print(f"Chain failed: {result['error']}")
    print(f"Errors: {result['errors']}")
else:
    print(f"Success after {result['retries']} retries")
    print(result["text"])
```

## Chain Monitoring and Optimization

### Performance Monitoring

```python
class ChainPerformanceMonitor:
    """Monitor chain performance and provide optimization suggestions"""

    def __init__(self):
        self.performance_data = {}
        self.chain_usage = {}

    def monitor_chain_execution(self, chain_name: str, execution_time: float, input_tokens: int, output_tokens: int, success: bool):
        """Monitor chain execution"""
        if chain_name not in self.performance_data:
            self.performance_data[chain_name] = {
                "executions": [],
                "total_time": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "success_count": 0
            }

        data = self.performance_data[chain_name]
        data["executions"].append({
            "time": execution_time,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "success": success,
            "timestamp": time.time()
        })

        data["total_time"] += execution_time
        data["total_input_tokens"] += input_tokens
        data["total_output_tokens"] += output_tokens

        if success:
            data["success_count"] += 1

    def get_chain_metrics(self, chain_name: str) -> Dict[str, Any]:
        """Get performance metrics for a chain"""
        if chain_name not in self.performance_data:
            return {}

        data = self.performance_data[chain_name]
        executions = len(data["executions"])

        return {
            "total_executions": executions,
            "success_rate": data["success_count"] / executions if executions > 0 else 0,
            "average_execution_time": data["total_time"] / executions if executions > 0 else 0,
            "average_input_tokens": data["total_input_tokens"] / executions if executions > 0 else 0,
            "average_output_tokens": data["total_output_tokens"] / executions if executions > 0 else 0,
            "total_tokens": data["total_input_tokens"] + data["total_output_tokens"]
        }

    def get_optimization_suggestions(self, chain_name: str) -> List[str]:
        """Provide optimization suggestions"""
        metrics = self.get_chain_metrics(chain_name)
        suggestions = []

        if metrics.get("average_execution_time", 0) > 10:
            suggestions.append("Consider optimizing prompts to reduce response time")

        if metrics.get("success_rate", 1) < 0.8:
            suggestions.append("Review error patterns and improve error handling")

        if metrics.get("average_input_tokens", 0) > 1000:
            suggestions.append("Consider breaking large inputs into smaller chunks")

        return suggestions

# Usage
monitor = ChainPerformanceMonitor()

# Monitor chain execution
monitor.monitor_chain_execution("ResearchChain", 5.2, 150, 300, True)
monitor.monitor_chain_execution("AnalysisChain", 8.1, 200, 400, False)

# Get metrics and suggestions
metrics = monitor.get_chain_metrics("ResearchChain")
suggestions = monitor.get_optimization_suggestions("ResearchChain")

print("Chain Metrics:", metrics)
print("Optimization Suggestions:", suggestions)
```

## What We've Accomplished

Congratulations! 🎉 You've successfully learned about:

1. **Custom Chain Development** - Base classes and specialized chains
2. **Complex Chain Architectures** - Multi-branch and parallel processing
3. **Chain Composition Patterns** - Chain of chains and dynamic builders
4. **Advanced Chain Features** - Memory integration and error handling
5. **Chain Monitoring and Optimization** - Performance tracking and suggestions

## Next Steps

Now that you understand advanced chains, let's explore production deployment considerations. In [Chapter 8: Production Deployment](08-production-deployment.md), we'll learn how to deploy LangChain applications at scale with proper monitoring, security, and performance optimization.

---

**Practice what you've learned:**
1. Create a custom chain that combines multiple processing steps
2. Build a multi-branch chain that routes based on input characteristics
3. Implement a parallel processing chain for batch operations
4. Add performance monitoring and optimization to your chains

*What kind of advanced chain will you build first?* 🔗

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `chain`, `result` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Advanced Chains` as an operating subsystem inside **LangChain Tutorial: Building AI Applications with Large Language Models**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `input`, `inputs`, `Dict` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Advanced Chains` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `chain` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `result`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/langchain-ai/langchain)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `chain` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: Agents & Tools](06-agents-tools.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
