---
layout: default
title: "Chapter 7: Troubleshooting, Anti-Patterns, and Safety Checks"
nav_order: 7
parent: Planning with Files Tutorial
---

# Chapter 7: Troubleshooting, Anti-Patterns, and Safety Checks

This chapter covers common failures and how to avoid workflow degradation.

## Learning Goals

- diagnose template/path/hook failures quickly
- recover from cache and session-persistence issues
- detect anti-patterns like stale plans and repeated failures
- apply completion and safety checks consistently

## High-Frequency Issues

- planning files written to wrong directory
- hooks not triggering due install/config mismatch
- stale plugin cache after updates
- completion blocked by unchecked tasks or missing logs

## Safety Checks

- run status before and after major work bursts
- keep error logs explicit in planning files
- enforce completion checks before marking done

## Source References

- [Troubleshooting Guide](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/troubleshooting.md)
- [README Key Rules](https://github.com/OthmanAdi/planning-with-files/blob/master/README.md#key-rules)
- [SKILL.md Anti-Patterns](https://github.com/OthmanAdi/planning-with-files/blob/master/skills/planning-with-files/SKILL.md)

## Summary

You now have a robust troubleshooting and safety playbook.

Next: [Chapter 8: Contribution Workflow and Team Adoption](08-contribution-workflow-and-team-adoption.md)
