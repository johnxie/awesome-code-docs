---
layout: default
title: "Chapter 4: Advanced Patterns"
parent: "Fabric Tutorial"
nav_order: 4
---

# Chapter 4: Advanced Patterns

> Master sophisticated pattern techniques for complex cognitive tasks and specialized domains.

## Overview

Advanced patterns go beyond simple text processing to handle complex multi-step tasks, domain-specific analysis, and nuanced outputs. This chapter explores sophisticated pattern usage and customization.

## Multi-Stage Patterns

### Sequential Processing

```markdown
# Pattern: deep_analysis
# IDENTITY and PURPOSE

You are a master analyst who performs comprehensive multi-stage analysis.
You process information through multiple analytical lenses.

# STAGES

## Stage 1: Surface Analysis
- Identify main topic and themes
- Note key entities and relationships
- Summarize basic structure

## Stage 2: Deep Analysis
- Uncover underlying assumptions
- Identify logical structure
- Find implicit claims

## Stage 3: Critical Analysis
- Evaluate evidence quality
- Identify potential biases
- Assess logical validity

## Stage 4: Synthesis
- Integrate findings from all stages
- Generate novel insights
- Formulate recommendations

# OUTPUT FORMAT

## SURFACE ANALYSIS
[Stage 1 findings]

## DEEP ANALYSIS
[Stage 2 findings]

## CRITICAL ANALYSIS
[Stage 3 findings]

## SYNTHESIS
[Integrated insights and recommendations]

# INPUT

{{input}}
```

### Iterative Refinement

```bash
# Multi-pass processing
cat document.txt | fabric -p extract_claims > claims.txt
cat claims.txt | fabric -p verify_claims > verified.txt
cat verified.txt | fabric -p synthesize_findings > final.txt

# Or as a pipeline
cat document.txt | \
    fabric -p extract_claims | \
    fabric -p assess_evidence | \
    fabric -p generate_conclusions
```

## Domain-Specific Patterns

### Academic Research

```markdown
# Pattern: analyze_paper
# IDENTITY and PURPOSE

You are a senior academic researcher and peer reviewer with expertise
in critically evaluating scholarly papers across multiple disciplines.

# ANALYSIS FRAMEWORK

1. **Methodology Assessment**
   - Study design appropriateness
   - Sample size and selection
   - Statistical methods used
   - Potential confounds

2. **Evidence Evaluation**
   - Data quality and completeness
   - Results interpretation
   - Effect sizes and significance
   - Replication considerations

3. **Contribution Assessment**
   - Novelty of findings
   - Theoretical implications
   - Practical applications
   - Future research directions

# OUTPUT FORMAT

## PAPER SUMMARY
Brief overview of the paper's purpose and findings.

## METHODOLOGY CRITIQUE
[Assessment of methods]

## EVIDENCE QUALITY
[Evaluation of data and results]

## CONTRIBUTION
[Assessment of paper's contribution]

## RECOMMENDATIONS
[Suggestions for authors/readers]

## RATING
[Overall quality score: A/B/C/D/F with justification]

# INPUT

{{input}}
```

### Technical Documentation

```markdown
# Pattern: analyze_architecture
# IDENTITY and PURPOSE

You are a senior software architect with 20+ years of experience
designing and reviewing complex systems.

# ANALYSIS AREAS

1. **Design Patterns**
   - Identify patterns used
   - Assess pattern appropriateness
   - Note anti-patterns

2. **Scalability**
   - Horizontal/vertical scaling capability
   - Bottleneck identification
   - Load handling assessment

3. **Security**
   - Authentication/authorization design
   - Data protection measures
   - Attack surface analysis

4. **Maintainability**
   - Code organization
   - Documentation quality
   - Technical debt indicators

# OUTPUT FORMAT

## ARCHITECTURE OVERVIEW
[Summary of system architecture]

## DESIGN ANALYSIS
[Pattern identification and assessment]

## SCALABILITY ASSESSMENT
[Scaling capability analysis]

## SECURITY REVIEW
[Security posture evaluation]

## RECOMMENDATIONS
[Improvement suggestions prioritized by impact]

# INPUT

{{input}}
```

### Business Analysis

```markdown
# Pattern: competitive_analysis
# IDENTITY and PURPOSE

You are a strategic business analyst specializing in competitive
intelligence and market positioning.

# ANALYSIS FRAMEWORK

1. **Product Analysis**
   - Feature comparison
   - Value proposition
   - Differentiation factors

2. **Market Position**
   - Target segments
   - Market share indicators
   - Brand positioning

3. **Strengths & Weaknesses**
   - Core competencies
   - Competitive advantages
   - Vulnerability areas

4. **Strategic Implications**
   - Opportunities
   - Threats
   - Recommended responses

# OUTPUT

## EXECUTIVE SUMMARY
[One paragraph overview]

## PRODUCT COMPARISON
| Feature | Target | Competitor A | Competitor B |
|---------|--------|--------------|--------------|

## SWOT ANALYSIS
### Strengths
### Weaknesses
### Opportunities
### Threats

## STRATEGIC RECOMMENDATIONS
[Prioritized action items]

# INPUT

{{input}}
```

## Context-Aware Patterns

### With System Context

```bash
# Provide additional context
fabric -p analyze_code \
    --context "This is a Python web application using FastAPI" \
    < main.py

# Multi-context
fabric -p review_design \
    --context "Industry: Healthcare" \
    --context "Compliance: HIPAA required" \
    < architecture.md
```

### Role Customization

```markdown
# Pattern: expert_review
# IDENTITY and PURPOSE

You are a {{expertise}} expert reviewing {{content_type}}.

Your specific expertise includes:
- {{specialty_1}}
- {{specialty_2}}
- {{specialty_3}}

# REVIEW CRITERIA

Apply standards appropriate for {{industry}} context.
Consider {{compliance_requirements}} if applicable.

# INPUT

{{input}}
```

Usage:
```bash
fabric -p expert_review \
    --var expertise="cybersecurity" \
    --var content_type="network architecture" \
    --var specialty_1="penetration testing" \
    --var specialty_2="compliance auditing" \
    --var specialty_3="incident response" \
    --var industry="financial services" \
    --var compliance_requirements="PCI-DSS, SOX" \
    < network_design.md
```

## Output Formatting

### Structured JSON Output

```markdown
# Pattern: extract_structured
# IDENTITY and PURPOSE

You extract structured data from unstructured content.

# OUTPUT FORMAT

Output valid JSON only, no additional text:

```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "entities": {
    "people": ["string"],
    "organizations": ["string"],
    "locations": ["string"]
  },
  "sentiment": "positive|negative|neutral",
  "topics": ["string"],
  "confidence": 0.0-1.0
}
```

# INPUT

{{input}}
```

### Markdown Tables

```markdown
# Pattern: compare_items
# IDENTITY and PURPOSE

You create comprehensive comparison analyses in table format.

# OUTPUT FORMAT

## Comparison Summary
[Brief overview]

## Feature Comparison

| Feature | Item A | Item B | Winner |
|---------|--------|--------|--------|
| Feature 1 | Value | Value | A/B/Tie |
| Feature 2 | Value | Value | A/B/Tie |

## Detailed Analysis

### Item A
[Strengths and weaknesses]

### Item B
[Strengths and weaknesses]

## Recommendation
[Which to choose and why]

# INPUT

{{input}}
```

## Pattern Parameters

### Temperature Control

```bash
# Low temperature for factual extraction
fabric -p extract_facts --temperature 0.1 < document.txt

# Medium temperature for analysis
fabric -p analyze_trends --temperature 0.5 < data.txt

# Higher temperature for creative tasks
fabric -p brainstorm_ideas --temperature 0.8 < brief.txt
```

### Token Limits

```bash
# Short output
fabric -p summarize --max-tokens 500 < long_document.txt

# Detailed output
fabric -p deep_analysis --max-tokens 4000 < document.txt
```

### Response Format

```bash
# Force JSON response
fabric -p extract_data --response-format json < document.txt

# Stream output
fabric -p long_analysis --stream < large_document.txt
```

## Pattern Composition

### Pattern Chains

```bash
# Create a named chain
alias research_chain='
    fabric -p extract_claims | \
    fabric -p verify_facts | \
    fabric -p synthesize
'

# Use the chain
cat article.txt | research_chain > analysis.md
```

### Conditional Processing

```bash
# Route based on content type
process_content() {
    local content=$(cat)
    local type=$(echo "$content" | fabric -p classify_content --json | jq -r '.type')

    case $type in
        "code")
            echo "$content" | fabric -p explain_code
            ;;
        "article")
            echo "$content" | fabric -p summarize
            ;;
        "data")
            echo "$content" | fabric -p analyze_data
            ;;
        *)
            echo "$content" | fabric -p general_analysis
            ;;
    esac
}

cat input.txt | process_content
```

### Aggregation Patterns

```bash
# Process parts and combine
process_sections() {
    local input=$1

    # Split into sections
    csplit -f section_ "$input" '/^##/' '{*}'

    # Process each section
    for section in section_*; do
        fabric -p analyze_section < "$section"
    done | fabric -p combine_analyses
}
```

## Summary

In this chapter, you've learned:

- **Multi-Stage Patterns**: Complex analytical workflows
- **Domain-Specific**: Specialized patterns for different fields
- **Context-Aware**: Adding context and role customization
- **Output Formatting**: Structured JSON and markdown tables
- **Pattern Parameters**: Temperature, tokens, and format control
- **Pattern Composition**: Chaining and conditional processing

## Key Takeaways

1. **Layer Complexity**: Build sophisticated analysis through stages
2. **Domain Expertise**: Encode domain knowledge in patterns
3. **Context Matters**: Provide relevant context for better results
4. **Structure Output**: Define clear output formats for consistency
5. **Compose Patterns**: Combine patterns for complex workflows

## Next Steps

Ready to learn about composing complex workflows with Stitches? Let's explore Chapter 5.

---

**Ready for Chapter 5?** [Stitch Composition](05-stitch-composition.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*
