---
layout: default
title: "Chapter 4: Infrastructure and IaC Workflows"
nav_order: 4
parent: awslabs/mcp Tutorial
---

# Chapter 4: Infrastructure and IaC Workflows

This chapter focuses on infrastructure automation servers (Terraform, CloudFormation, CDK, and related flows).

## Learning Goals

- align IaC server choice to your existing delivery stack
- integrate security scanning into generated infrastructure workflows
- distinguish deprecated versus preferred server paths
- keep deployment ownership and approval boundaries explicit

## IaC Strategy

Use server outputs to accelerate drafting and validation, but keep infrastructure approvals, production applies, and policy exceptions under explicit human governance.

## Source References

- [AWS Terraform MCP Server README](https://github.com/awslabs/mcp/blob/main/src/terraform-mcp-server/README.md)
- [Repository README Infrastructure Sections](https://github.com/awslabs/mcp/blob/main/README.md)
- [Design Guidelines](https://github.com/awslabs/mcp/blob/main/DESIGN_GUIDELINES.md)

## Summary

You now understand how to use IaC-focused MCP servers without weakening deployment controls.

Next: [Chapter 5: Data, Knowledge, and Agent Workflows](05-data-knowledge-and-agent-workflows.md)
