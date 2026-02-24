---
layout: default
title: "Chapter 2: Data Preparation"
parent: "LLaMA Factory Tutorial"
nav_order: 2
---

# Chapter 2: Data Preparation

Welcome to the crucial phase of fine-tuning: data preparation. The quality and format of your training data directly impacts the performance of your fine-tuned model. This chapter covers data collection, preprocessing, and formatting for LLaMA Factory.

## Understanding Data Requirements

LLaMA Factory expects data in specific formats depending on the task type:

### Supported Data Formats

```json
// Instruction tuning format
{
  "instruction": "Calculate the sum of 15 and 27",
  "input": "",
  "output": "42"
}

// Conversation format
{
  "conversations": [
    {"from": "human", "value": "Hello, how are you?"},
    {"from": "assistant", "value": "I'm doing well, thank you! How can I help you today?"}
  ]
}

// Text-to-SQL format
{
  "instruction": "Convert this natural language query to SQL",
  "input": "Show me all users who signed up in January",
  "output": "SELECT * FROM users WHERE signup_date >= '2024-01-01' AND signup_date < '2024-02-01'"
}
```

## Data Collection Strategies

### Curating High-Quality Datasets

```python
import json
from typing import List, Dict, Any
from datasets import load_dataset

class DataCurator:
    """Curate and filter training data"""

    def __init__(self, min_length: int = 10, max_length: int = 2048):
        self.min_length = min_length
        self.max_length = max_length

    def filter_by_length(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter examples by text length"""
        filtered = []
        for example in dataset:
            text = self._extract_text(example)
            if self.min_length <= len(text) <= self.max_length:
                filtered.append(example)
        return filtered

    def remove_duplicates(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate examples"""
        seen = set()
        unique = []

        for example in dataset:
            text = self._extract_text(example)
            if text not in seen:
                seen.add(text)
                unique.append(example)

        return unique

    def filter_by_quality(self, dataset: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter by content quality"""
        filtered = []

        for example in dataset:
            if self._passes_quality_checks(example):
                filtered.append(example)

        return filtered

    def _extract_text(self, example: Dict[str, Any]) -> str:
        """Extract text content from example"""
        if 'instruction' in example and 'output' in example:
            return f"{example['instruction']} {example.get('input', '')} {example['output']}"
        elif 'conversations' in example:
            return ' '.join([msg['value'] for msg in example['conversations']])
        else:
            return str(example)

    def _passes_quality_checks(self, example: Dict[str, Any]) -> bool:
        """Check if example passes quality criteria"""
        text = self._extract_text(example)

        # Check for common issues
        if len(text.strip()) == 0:
            return False

        if text.count('?') > 10:  # Too many questions
            return False

        if any(word in text.lower() for word in ['lorem ipsum', 'test data']):
            return False

        return True

# Usage
curator = DataCurator(min_length=20, max_length=1024)
raw_data = load_dataset("your-dataset")['train']

# Apply filters
filtered_data = curator.filter_by_length(raw_data)
unique_data = curator.remove_duplicates(filtered_data)
quality_data = curator.filter_by_quality(unique_data)

print(f"Original: {len(raw_data)}, Filtered: {len(quality_data)}")
```

## Data Formatting and Conversion

### Converting Between Formats

```python
class DataFormatter:
    """Convert data between different formats"""

    @staticmethod
    def alpaca_to_conversation(alpaca_data: List[Dict]) -> List[Dict]:
        """Convert Alpaca format to conversation format"""
        conversations = []

        for item in alpaca_data:
            conversation = {
                "conversations": [
                    {"from": "human", "value": item["instruction"] + (item.get("input", "") and f"\n{item['input']}" or "")},
                    {"from": "assistant", "value": item["output"]}
                ]
            }
            conversations.append(conversation)

        return conversations

    @staticmethod
    def conversation_to_alpaca(conversation_data: List[Dict]) -> List[Dict]:
        """Convert conversation format to Alpaca format"""
        alpaca = []

        for item in conversation_data:
            messages = item["conversations"]
            if len(messages) >= 2:
                human_msg = messages[0]["value"]
                assistant_msg = messages[1]["value"]

                # Try to split instruction and input
                if "\n" in human_msg:
                    instruction, input_text = human_msg.split("\n", 1)
                else:
                    instruction = human_msg
                    input_text = ""

                alpaca.append({
                    "instruction": instruction,
                    "input": input_text,
                    "output": assistant_msg
                })

        return alpaca

    @staticmethod
    def standardize_format(data: List[Dict], target_format: str) -> List[Dict]:
        """Standardize data to target format"""
        if target_format == "alpaca":
            return DataFormatter.conversation_to_alpaca(data)
        elif target_format == "conversation":
            return DataFormatter.alpaca_to_conversation(data)
        else:
            return data

# Usage
formatter = DataFormatter()
alpaca_data = [
    {
        "instruction": "Explain quantum computing",
        "input": "in simple terms",
        "output": "Quantum computing uses quantum mechanics..."
    }
]

conversation_data = formatter.alpaca_to_conversation(alpaca_data)
print(conversation_data[0])
```

## Data Augmentation Techniques

### Synthetic Data Generation

```python
from langchain_openai import ChatOpenAI
import random

class DataAugmentor:
    """Generate synthetic training data"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.7)

    def generate_variations(self, base_instruction: str, num_variations: int = 5) -> List[str]:
        """Generate variations of an instruction"""
        prompt = f"""
        Generate {num_variations} different ways to phrase this instruction:
        "{base_instruction}"

        Make them natural and diverse. Return as a numbered list.
        """

        response = self.llm.invoke(prompt)
        variations = self._parse_numbered_list(response.content)

        return variations

    def create_counterfactuals(self, original_data: List[Dict]) -> List[Dict]:
        """Create counterfactual examples"""
        counterfactuals = []

        for item in original_data:
            if "instruction" in item:
                # Generate wrong answer
                prompt = f"""
                For the instruction: "{item['instruction']}"
                Current correct answer: "{item['output']}"

                Generate a plausible but incorrect answer:
                """

                wrong_answer = self.llm.invoke(prompt).content.strip()

                counterfactual = {
                    "instruction": item["instruction"],
                    "input": item.get("input", ""),
                    "output": wrong_answer,
                    "is_counterfactual": True
                }

                counterfactuals.append(counterfactual)

        return counterfactuals

    def augment_with_paraphrases(self, data: List[Dict]) -> List[Dict]:
        """Augment data with paraphrased versions"""
        augmented = []

        for item in data:
            augmented.append(item)  # Keep original

            # Generate paraphrases
            if "instruction" in item:
                paraphrases = self.generate_variations(item["instruction"], 2)

                for paraphrase in paraphrases:
                    new_item = item.copy()
                    new_item["instruction"] = paraphrase
                    new_item["is_paraphrase"] = True
                    augmented.append(new_item)

        return augmented

    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse numbered list from LLM response"""
        lines = text.strip().split('\n')
        items = []

        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                if line[0].isdigit():
                    line = line.split('.', 1)[-1].strip()
                elif line.startswith('-'):
                    line = line[1:].strip()

                items.append(line)

        return items

# Usage
augmentor = DataAugmentor()

# Generate variations
variations = augmentor.generate_variations("Explain how photosynthesis works")
print("Variations:", variations)

# Create counterfactuals
original_data = [
    {"instruction": "What is 2+2?", "output": "4"}
]
counterfactuals = augmentor.create_counterfactuals(original_data)
print("Counterfactuals:", counterfactuals)
```

## Data Validation and Quality Assurance

### Comprehensive Validation Suite

```python
import re
from typing import Dict, List, Any

class DataValidator:
    """Validate training data quality"""

    def __init__(self):
        self.validation_rules = {
            'min_length': 10,
            'max_length': 2048,
            'has_instruction': True,
            'has_output': True,
            'no_empty_fields': True,
            'no_placeholder_text': True,
            'proper_grammar': True,
            'appropriate_content': True
        }

    def validate_dataset(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run comprehensive validation on dataset"""
        results = {
            'total_examples': len(dataset),
            'passed_validation': 0,
            'failed_validation': 0,
            'errors': [],
            'warnings': []
        }

        for i, example in enumerate(dataset):
            is_valid, errors, warnings = self.validate_example(example)

            if is_valid:
                results['passed_validation'] += 1
            else:
                results['failed_validation'] += 1
                results['errors'].extend([f"Example {i}: {error}" for error in errors])

            results['warnings'].extend([f"Example {i}: {warning}" for warning in warnings])

        return results

    def validate_example(self, example: Dict[str, Any]) -> tuple[bool, List[str], List[str]]:
        """Validate a single example"""
        errors = []
        warnings = []

        # Check required fields
        if self.validation_rules['has_instruction']:
            if 'instruction' not in example or not example['instruction'].strip():
                errors.append("Missing or empty instruction field")

        if self.validation_rules['has_output']:
            if 'output' not in example or not example['output'].strip():
                errors.append("Missing or empty output field")

        # Check content quality
        text_content = self._extract_full_text(example)

        if len(text_content) < self.validation_rules['min_length']:
            errors.append(f"Content too short ({len(text_content)} chars, min {self.validation_rules['min_length']})")

        if len(text_content) > self.validation_rules['max_length']:
            errors.append(f"Content too long ({len(text_content)} chars, max {self.validation_rules['max_length']})")

        # Check for placeholder text
        if self.validation_rules['no_placeholder_text']:
            placeholders = ['lorem ipsum', 'placeholder', 'test data', 'example text']
            if any(placeholder in text_content.lower() for placeholder in placeholders):
                errors.append("Contains placeholder text")

        # Check for empty fields
        if self.validation_rules['no_empty_fields']:
            for key, value in example.items():
                if isinstance(value, str) and not value.strip():
                    warnings.append(f"Empty or whitespace-only field: {key}")

        # Basic grammar check (simple heuristic)
        if self.validation_rules['proper_grammar']:
            if text_content.count('?') > 5:
                warnings.append("Too many questions - may indicate poor quality")

        return len(errors) == 0, errors, warnings

    def _extract_full_text(self, example: Dict[str, Any]) -> str:
        """Extract all text content from example"""
        texts = []

        for key, value in example.items():
            if isinstance(value, str):
                texts.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and 'value' in item:
                        texts.append(item['value'])

        return ' '.join(texts)

# Usage
validator = DataValidator()
validation_results = validator.validate_dataset(your_dataset)

print(f"Validation Results:")
print(f"Total: {validation_results['total_examples']}")
print(f"Passed: {validation_results['passed_validation']}")
print(f"Failed: {validation_results['failed_validation']}")
print(f"Errors: {len(validation_results['errors'])}")
```

## Splitting Data for Training

### Stratified Splitting Strategy

```python
from sklearn.model_selection import train_test_split
import pandas as pd

class DataSplitter:
    """Split data for training, validation, and testing"""

    def __init__(self, train_ratio: float = 0.7, val_ratio: float = 0.2, test_ratio: float = 0.1):
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio

    def stratified_split(self, dataset: List[Dict], stratify_by: str = None) -> Dict[str, List]:
        """Perform stratified split based on a field"""
        if not stratify_by:
            return self.random_split(dataset)

        # Group by stratification field
        groups = {}
        for item in dataset:
            key = item.get(stratify_by, 'unknown')
            if key not in groups:
                groups[key] = []
            groups[key].append(item)

        train_data, val_data, test_data = [], [], []

        for group_items in groups.values():
            if len(group_items) < 3:
                # Not enough samples for stratification
                train_data.extend(group_items)
                continue

            # Split this group
            train_group, temp_group = train_test_split(
                group_items,
                train_size=self.train_ratio,
                random_state=42
            )

            val_group, test_group = train_test_split(
                temp_group,
                train_size=self.val_ratio / (self.val_ratio + self.test_ratio),
                random_state=42
            )

            train_data.extend(train_group)
            val_data.extend(val_group)
            test_data.extend(test_group)

        return {
            'train': train_data,
            'validation': val_data,
            'test': test_data
        }

    def random_split(self, dataset: List[Dict]) -> Dict[str, List]:
        """Perform random split"""
        train_data, temp_data = train_test_split(
            dataset,
            train_size=self.train_ratio,
            random_state=42
        )

        val_data, test_data = train_test_split(
            temp_data,
            train_size=self.val_ratio / (self.val_ratio + self.test_ratio),
            random_state=42
        )

        return {
            'train': train_data,
            'validation': val_data,
            'test': test_data
        }

    def save_splits(self, splits: Dict[str, List], output_dir: str):
        """Save data splits to files"""
        import json

        for split_name, data in splits.items():
            filename = f"{output_dir}/{split_name}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"Saved {len(data)} examples to {filename}")

# Usage
splitter = DataSplitter()
splits = splitter.stratified_split(dataset, stratify_by='category')
splitter.save_splits(splits, './data')
```

## Data Pipeline Automation

### Complete Data Preparation Pipeline

```python
from typing import List, Dict, Any
import json

class DataPreparationPipeline:
    """Automated data preparation pipeline"""

    def __init__(self):
        self.curator = DataCurator()
        self.formatter = DataFormatter()
        self.augmentor = DataAugmentor()
        self.validator = DataValidator()
        self.splitter = DataSplitter()

    def process_dataset(self, raw_data: List[Dict], config: Dict) -> Dict[str, List]:
        """Run complete data preparation pipeline"""
        print("Starting data preparation pipeline...")

        # Step 1: Initial curation
        print("Step 1: Curating data...")
        curated = self.curator.filter_by_length(raw_data)
        curated = self.curator.remove_duplicates(curated)
        curated = self.curator.filter_by_quality(curated)
        print(f"Curated: {len(curated)} examples")

        # Step 2: Format conversion
        if config.get('target_format'):
            print(f"Step 2: Converting to {config['target_format']} format...")
            curated = self.formatter.standardize_format(curated, config['target_format'])

        # Step 3: Data augmentation
        if config.get('augmentation_enabled'):
            print("Step 3: Augmenting data...")
            if config.get('use_paraphrases'):
                curated = self.augmentor.augment_with_paraphrases(curated)
            if config.get('use_counterfactuals'):
                counterfactuals = self.augmentor.create_counterfactuals(curated[:100])  # Sample
                curated.extend(counterfactuals)
            print(f"Augmented: {len(curated)} examples")

        # Step 4: Validation
        print("Step 4: Validating data...")
        validation_results = self.validator.validate_dataset(curated)
        print(f"Validation: {validation_results['passed_validation']}/{validation_results['total_examples']} passed")

        # Filter out invalid examples
        valid_data = [item for i, item in enumerate(curated)
                     if i < len(validation_results.get('errors', [])) or True]  # Simplified

        # Step 5: Splitting
        print("Step 5: Splitting data...")
        stratify_by = config.get('stratify_by')
        splits = self.splitter.stratified_split(valid_data, stratify_by)

        print("Pipeline completed!")
        print(f"Train: {len(splits['train'])}, Val: {len(splits['validation'])}, Test: {len(splits['test'])}")

        return splits

# Configuration
pipeline_config = {
    'target_format': 'alpaca',
    'augmentation_enabled': True,
    'use_paraphrases': True,
    'use_counterfactuals': False,
    'stratify_by': 'category'
}

# Run pipeline
pipeline = DataPreparationPipeline()
final_splits = pipeline.process_dataset(raw_dataset, pipeline_config)

# Save results
for split_name, data in final_splits.items():
    with open(f'processed_{split_name}.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

## What We've Accomplished

Excellent! 🎯 You've mastered data preparation for LLaMA Factory:

1. **Data curation** - Quality filtering and deduplication
2. **Format conversion** - Converting between different data formats
3. **Data augmentation** - Synthetic data generation and paraphrasing
4. **Quality validation** - Comprehensive data quality checks
5. **Strategic splitting** - Proper train/validation/test splits
6. **Automated pipelines** - End-to-end data preparation workflows

## Next Steps

Ready to start training? In [Chapter 3: Model Configuration](03-model-configuration.md), we'll explore setting up and configuring your LLaMA models for fine-tuning!

---

**Practice what you've learned:**
1. Prepare a dataset for a specific task (e.g., code generation, creative writing)
2. Implement custom data validation rules for your domain
3. Create a data augmentation strategy for low-resource scenarios
4. Build an automated data preparation pipeline for continuous learning
5. Experiment with different data splitting strategies

*What's the most challenging dataset you've prepared?* 📊

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `self`, `example`, `Dict` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 2: Data Preparation` as an operating subsystem inside **LLaMA-Factory Tutorial: Unified Framework for LLM Training and Fine-tuning**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `List`, `item`, `instruction` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 2: Data Preparation` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `self`.
2. **Input normalization**: shape incoming data so `example` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `Dict`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/hiyouga/LLaMA-Factory)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `self` and `example` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 1: Getting Started with LLaMA-Factory](01-getting-started.md)
- [Next Chapter: Chapter 3: Model Configuration](03-model-configuration.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
