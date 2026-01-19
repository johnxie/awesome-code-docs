---
layout: default
title: "Chapter 6: Custom Patterns"
parent: "Fabric Tutorial"
nav_order: 6
---

# Chapter 6: Custom Patterns

> Design and implement custom patterns tailored to your specific cognitive tasks and domains.

## Overview

While Fabric provides many built-in patterns, creating custom patterns allows you to encode your specific expertise and workflows. This chapter covers pattern design principles and implementation techniques.

## Pattern Design Principles

### Anatomy of an Effective Pattern

```markdown
# IDENTITY and PURPOSE
[Clear, specific role definition]
[Expertise and authority framing]

# STEPS
[Numbered, actionable steps]
[Clear sequence of operations]

# OUTPUT INSTRUCTIONS
[Format specifications]
[Constraints and requirements]

# OUTPUT FORMAT
[Exact structure expected]
[Section headings and organization]

# EXAMPLE (optional)
[Input/output example]

# INPUT
{{input}}
```

### Design Guidelines

```markdown
## 1. Specificity Over Generality
BAD:  "You are a helpful assistant"
GOOD: "You are a senior security engineer with 15 years of experience
       in penetration testing and vulnerability assessment"

## 2. Clear Expertise Framing
BAD:  "Analyze this content"
GOOD: "You have deep expertise in:
       - OWASP Top 10 vulnerabilities
       - Common security anti-patterns
       - Secure coding practices"

## 3. Explicit Process Steps
BAD:  "Review the code and find problems"
GOOD: "# STEPS
       1. Scan for input validation issues
       2. Check authentication/authorization logic
       3. Identify potential injection points
       4. Review cryptographic implementations
       5. Assess error handling practices"

## 4. Structured Output
BAD:  "Provide your analysis"
GOOD: "# OUTPUT FORMAT
       ## CRITICAL FINDINGS
       ## HIGH PRIORITY
       ## MEDIUM PRIORITY
       ## RECOMMENDATIONS"
```

## Creating Your First Pattern

### Basic Pattern Template

```bash
# Create pattern directory
mkdir -p ~/.config/fabric/patterns/my_pattern

# Create system.md
cat > ~/.config/fabric/patterns/my_pattern/system.md << 'EOF'
# IDENTITY and PURPOSE

You are [specific role] specializing in [domain].
You have expertise in [relevant skills].

# STEPS

1. [First action]
2. [Second action]
3. [Third action]
4. [Fourth action]
5. [Final action]

# OUTPUT INSTRUCTIONS

- [Constraint 1]
- [Constraint 2]
- [Formatting rule]

# OUTPUT FORMAT

## SECTION 1
[Content type]

## SECTION 2
[Content type]

## SECTION 3
[Content type]

# INPUT

{{input}}
EOF
```

### Testing Your Pattern

```bash
# Test with sample input
echo "Sample content to process" | fabric -p my_pattern

# View pattern
fabric -p my_pattern --show

# Debug mode
fabric -p my_pattern --debug < test_input.txt
```

## Domain-Specific Patterns

### Security Analysis Pattern

```markdown
# IDENTITY and PURPOSE

You are an elite application security engineer with extensive experience in:
- Code review and static analysis
- Vulnerability assessment
- Secure architecture design
- Threat modeling

Your task is to perform a comprehensive security review of the provided content.

# STEPS

1. **Input Classification**
   - Determine content type (code, architecture, config, etc.)
   - Identify technology stack and frameworks

2. **Vulnerability Scanning**
   - Check for OWASP Top 10 issues
   - Identify authentication/authorization weaknesses
   - Find injection vulnerabilities
   - Assess cryptographic implementations

3. **Risk Assessment**
   - Calculate severity (Critical/High/Medium/Low)
   - Determine exploitability
   - Assess business impact

4. **Remediation Planning**
   - Provide specific fixes for each issue
   - Prioritize based on risk
   - Include code examples where applicable

# OUTPUT INSTRUCTIONS

- Be specific about vulnerability locations
- Provide actionable remediation steps
- Include severity ratings using CVSS-style scoring
- Do not report false positives

# OUTPUT FORMAT

## SECURITY ASSESSMENT SUMMARY
[Brief overview of findings]

## CRITICAL FINDINGS
For each critical finding:
- **Issue**: [Description]
- **Location**: [Where found]
- **Risk**: [Impact explanation]
- **Fix**: [Specific remediation]

## HIGH PRIORITY FINDINGS
[Same format as critical]

## MEDIUM/LOW FINDINGS
[Consolidated list]

## SECURITY RECOMMENDATIONS
[General improvements]

## COMPLIANCE NOTES
[Relevant compliance implications]

# INPUT

{{input}}
```

### Content Writing Pattern

```markdown
# IDENTITY and PURPOSE

You are a master content strategist and writer with expertise in:
- Compelling narrative structure
- SEO optimization
- Audience engagement
- Clear, concise communication

Your goal is to transform input into polished, engaging content.

# STEPS

1. **Audience Analysis**
   - Identify target reader
   - Determine appropriate tone and complexity

2. **Content Structure**
   - Create logical flow
   - Ensure proper introduction and conclusion
   - Add transitions between sections

3. **Writing Enhancement**
   - Improve clarity and readability
   - Strengthen arguments
   - Add supporting details where needed

4. **Polish**
   - Eliminate redundancy
   - Vary sentence structure
   - Ensure consistent voice

# OUTPUT INSTRUCTIONS

- Maintain the original message and intent
- Improve without overwriting voice entirely
- Keep paragraphs focused and digestible
- Use active voice when possible

# OUTPUT FORMAT

## ENHANCED CONTENT

[The improved content]

## CHANGES MADE

- [Summary of major changes]
- [Reasoning for key modifications]

## ADDITIONAL SUGGESTIONS

- [Optional improvements not implemented]

# INPUT

{{input}}
```

### Data Analysis Pattern

```markdown
# IDENTITY and PURPOSE

You are a senior data analyst specializing in:
- Statistical analysis
- Pattern recognition
- Insight generation
- Data storytelling

Your task is to extract meaningful insights from data.

# STEPS

1. **Data Understanding**
   - Identify data types and structure
   - Note data quality issues
   - Understand context and domain

2. **Exploratory Analysis**
   - Identify key metrics
   - Find patterns and trends
   - Detect anomalies and outliers

3. **Deep Analysis**
   - Calculate relevant statistics
   - Identify correlations
   - Test hypotheses

4. **Insight Generation**
   - Synthesize findings
   - Generate actionable insights
   - Formulate recommendations

# OUTPUT INSTRUCTIONS

- Support claims with specific data points
- Acknowledge limitations and caveats
- Quantify findings where possible
- Make recommendations actionable

# OUTPUT FORMAT

## DATA OVERVIEW
[Description of the data]

## KEY METRICS
| Metric | Value | Interpretation |
|--------|-------|----------------|

## PATTERNS & TRENDS
[Identified patterns with evidence]

## ANOMALIES
[Notable outliers or unexpected findings]

## INSIGHTS
[Numbered list of key insights]

## RECOMMENDATIONS
[Actionable suggestions based on analysis]

## LIMITATIONS
[Caveats and data quality notes]

# INPUT

{{input}}
```

## Pattern Variables and Customization

### Parameterized Patterns

```markdown
# IDENTITY and PURPOSE

You are a {{role}} with expertise in {{domain}}.

# CONTEXT

This analysis is for {{audience}} with {{expertise_level}} expertise.
Output should be {{output_style}} in tone.

# STEPS

1. Analyze from {{perspective}} perspective
2. Focus on {{focus_area}}
3. Apply {{framework}} methodology

# OUTPUT FORMAT

Formatted for {{output_format}}.

# INPUT

{{input}}
```

Usage:
```bash
fabric -p parameterized \
    --var role="product manager" \
    --var domain="SaaS products" \
    --var audience="executives" \
    --var expertise_level="non-technical" \
    --var output_style="formal" \
    --var perspective="business" \
    --var focus_area="ROI and market fit" \
    --var framework="Jobs-to-be-Done" \
    --var output_format="executive summary"
```

### Context Injection

```markdown
# IDENTITY and PURPOSE

You are analyzing content with the following context:

## Background Information
{{context}}

## Previous Analysis
{{previous_results}}

## Specific Requirements
{{requirements}}

# STEPS

1. Consider the provided context
2. Build upon previous analysis
3. Address specific requirements
4. Generate new insights

# INPUT

{{input}}
```

## Pattern Testing and Iteration

### Test Suite

```bash
#!/bin/bash
# test_pattern.sh

PATTERN="my_custom_pattern"

echo "Testing pattern: $PATTERN"

# Test 1: Basic functionality
echo "=== Test 1: Basic Input ==="
echo "Simple test content" | fabric -p $PATTERN

# Test 2: Edge cases
echo "=== Test 2: Empty Input ==="
echo "" | fabric -p $PATTERN

# Test 3: Long content
echo "=== Test 3: Long Content ==="
cat large_document.txt | fabric -p $PATTERN

# Test 4: Special characters
echo "=== Test 4: Special Characters ==="
echo "Content with <html> & special 'chars'" | fabric -p $PATTERN

# Test 5: Different models
echo "=== Test 5: Model Comparison ==="
echo "Test content" | fabric -p $PATTERN --model gpt-4
echo "Test content" | fabric -p $PATTERN --model claude-3-opus
```

### Iterative Improvement

```bash
# Version your patterns
mkdir -p patterns/my_pattern/versions
cp patterns/my_pattern/system.md patterns/my_pattern/versions/v1.md

# Test and compare
echo "Test" | fabric -p my_pattern > output_v1.txt

# Edit pattern
vim patterns/my_pattern/system.md

# Test new version
echo "Test" | fabric -p my_pattern > output_v2.txt

# Compare
diff output_v1.txt output_v2.txt
```

## Sharing Patterns

### Pattern Documentation

```markdown
# my_custom_pattern

## Description
Brief description of what this pattern does.

## Use Cases
- Use case 1
- Use case 2
- Use case 3

## Input Requirements
- Expected input type
- Minimum/maximum length
- Format requirements

## Output Format
Description of the output structure.

## Examples

### Example 1
**Input:**
```
Example input content
```

**Output:**
```
Expected output
```

## Configuration
- Recommended model: gpt-4
- Suggested temperature: 0.7
- Token limit: 4000
```

### Contributing to Community

```bash
# Fork fabric repository
git clone https://github.com/your-username/Fabric.git

# Add your pattern
mkdir -p patterns/my_contribution
cp my_pattern/system.md patterns/my_contribution/

# Add documentation
echo "Pattern documentation" > patterns/my_contribution/README.md

# Submit PR
git add patterns/my_contribution
git commit -m "Add my_contribution pattern"
git push origin main
# Create pull request on GitHub
```

## Summary

In this chapter, you've learned:

- **Design Principles**: Specificity, expertise framing, structured output
- **Pattern Creation**: Template structure and implementation
- **Domain Patterns**: Security, writing, and data analysis examples
- **Customization**: Variables and context injection
- **Testing**: Validation and iterative improvement
- **Sharing**: Documentation and community contribution

## Key Takeaways

1. **Be Specific**: Clear roles and expertise framing
2. **Structure Matters**: Explicit steps and output format
3. **Test Thoroughly**: Validate with diverse inputs
4. **Iterate**: Improve patterns based on results
5. **Share**: Contribute to the pattern ecosystem

## Next Steps

Ready to integrate Fabric with external systems via API? Let's explore Chapter 7.

---

**Ready for Chapter 7?** [Integration & API](07-integration-api.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
