---
layout: default
title: "Chapter 4: Dependency Graph and Hierarchy Patterns"
nav_order: 4
parent: Beads Tutorial
---


# Chapter 4: Dependency Graph and Hierarchy Patterns

Welcome to **Chapter 4: Dependency Graph and Hierarchy Patterns**. In this part of **Beads Tutorial: Git-Backed Task Graph Memory for Coding Agents**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter focuses on modeling blocker relationships and hierarchical plans.

## Learning Goals

- represent parent/child and blocking relationships correctly
- use hierarchy IDs for epic decomposition
- avoid cyclic dependencies in planning graphs
- improve ready-task signal quality

## Pattern Guidance

- reserve hierarchy for delivery decomposition
- use relation links for cross-cutting context
- keep dependencies minimal and explicit

## Source References

- [Beads README Hierarchy & Workflow](https://github.com/steveyegge/beads/blob/main/README.md)
- [Beads FAQ](https://github.com/steveyegge/beads/blob/main/docs/FAQ.md)

## Summary

You now can model complex plans as clean, navigable Beads graphs.

Next: [Chapter 5: Agent Integration and AGENTS.md Patterns](05-agent-integration-and-agents-md-patterns.md)

## Source Code Walkthrough

### `cmd/bd/list.go`

The `findAllDescendants` function in [`cmd/bd/list.go`](https://github.com/steveyegge/beads/blob/HEAD/cmd/bd/list.go) handles a key part of this chapter's functionality:

```go

	// Recursively find all descendants
	err = findAllDescendants(ctx, store, dbPath, parentID, allDescendants, 0, 10) // max depth 10
	if err != nil {
		return nil, fmt.Errorf("error finding descendants: %v", err)
	}

	// Convert map to slice for display
	treeIssues := make([]*types.Issue, 0, len(allDescendants))
	for _, issue := range allDescendants {
		treeIssues = append(treeIssues, issue)
	}

	return treeIssues, nil
}

// findAllDescendants recursively finds all descendants using parent filtering
func findAllDescendants(ctx context.Context, store storage.DoltStorage, dbPath string, parentID string, result map[string]*types.Issue, currentDepth, maxDepth int) error {
	if currentDepth >= maxDepth {
		return nil // Prevent infinite recursion
	}

	// Get direct children using the same filter logic as regular --parent
	var children []*types.Issue
	err := withStorage(ctx, store, dbPath, func(s storage.DoltStorage) error {
		filter := types.IssueFilter{
			ParentID: &parentID,
		}
		var err error
		children, err = s.SearchIssues(ctx, "", filter)
		return err
	})
```

This function is important because it defines how Beads Tutorial: Git-Backed Task Graph Memory for Coding Agents implements the patterns covered in this chapter.

### `cmd/bd/list.go`

The `watchIssues` function in [`cmd/bd/list.go`](https://github.com/steveyegge/beads/blob/HEAD/cmd/bd/list.go) handles a key part of this chapter's functionality:

```go
}

// watchIssues polls for changes and re-displays (GH#654)
// Uses polling instead of fsnotify because Dolt stores data in a server-side
// database, not files — file watchers never fire.
func watchIssues(ctx context.Context, store storage.DoltStorage, filter types.IssueFilter, sortBy string, reverse bool) {
	// Initial display
	issues, err := store.SearchIssues(ctx, "", filter)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error querying issues: %v\n", err)
		return
	}
	sortIssues(issues, sortBy, reverse)
	displayPrettyList(issues, true)
	lastSnapshot := issueSnapshot(issues)

	fmt.Fprintf(os.Stderr, "\nWatching for changes... (Press Ctrl+C to exit)\n")

	// Handle Ctrl+C — deferred Stop prevents signal handler leak
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	defer signal.Stop(sigChan)

	pollInterval := 2 * time.Second
	ticker := time.NewTicker(pollInterval)
	defer ticker.Stop()

	for {
		select {
		case <-sigChan:
			fmt.Fprintf(os.Stderr, "\nStopped watching.\n")
			return
```

This function is important because it defines how Beads Tutorial: Git-Backed Task Graph Memory for Coding Agents implements the patterns covered in this chapter.

### `cmd/bd/list.go`

The `issueSnapshot` function in [`cmd/bd/list.go`](https://github.com/steveyegge/beads/blob/HEAD/cmd/bd/list.go) handles a key part of this chapter's functionality:

```go
	sortIssues(issues, sortBy, reverse)
	displayPrettyList(issues, true)
	lastSnapshot := issueSnapshot(issues)

	fmt.Fprintf(os.Stderr, "\nWatching for changes... (Press Ctrl+C to exit)\n")

	// Handle Ctrl+C — deferred Stop prevents signal handler leak
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	defer signal.Stop(sigChan)

	pollInterval := 2 * time.Second
	ticker := time.NewTicker(pollInterval)
	defer ticker.Stop()

	for {
		select {
		case <-sigChan:
			fmt.Fprintf(os.Stderr, "\nStopped watching.\n")
			return
		case <-ticker.C:
			issues, err := store.SearchIssues(ctx, "", filter)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error refreshing issues: %v\n", err)
				continue
			}
			sortIssues(issues, sortBy, reverse)
			snap := issueSnapshot(issues)
			if snap != lastSnapshot {
				lastSnapshot = snap
				displayPrettyList(issues, true)
				fmt.Fprintf(os.Stderr, "\nWatching for changes... (Press Ctrl+C to exit)\n")
```

This function is important because it defines how Beads Tutorial: Git-Backed Task Graph Memory for Coding Agents implements the patterns covered in this chapter.

### `cmd/bd/list.go`

The `sortIssues` function in [`cmd/bd/list.go`](https://github.com/steveyegge/beads/blob/HEAD/cmd/bd/list.go) handles a key part of this chapter's functionality:

```go
		return
	}
	sortIssues(issues, sortBy, reverse)
	displayPrettyList(issues, true)
	lastSnapshot := issueSnapshot(issues)

	fmt.Fprintf(os.Stderr, "\nWatching for changes... (Press Ctrl+C to exit)\n")

	// Handle Ctrl+C — deferred Stop prevents signal handler leak
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	defer signal.Stop(sigChan)

	pollInterval := 2 * time.Second
	ticker := time.NewTicker(pollInterval)
	defer ticker.Stop()

	for {
		select {
		case <-sigChan:
			fmt.Fprintf(os.Stderr, "\nStopped watching.\n")
			return
		case <-ticker.C:
			issues, err := store.SearchIssues(ctx, "", filter)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error refreshing issues: %v\n", err)
				continue
			}
			sortIssues(issues, sortBy, reverse)
			snap := issueSnapshot(issues)
			if snap != lastSnapshot {
				lastSnapshot = snap
```

This function is important because it defines how Beads Tutorial: Git-Backed Task Graph Memory for Coding Agents implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[findAllDescendants]
    B[watchIssues]
    C[issueSnapshot]
    D[sortIssues]
    E[init]
    A --> B
    B --> C
    C --> D
    D --> E
```
