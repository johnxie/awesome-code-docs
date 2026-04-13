---
layout: default
title: "Chapter 6: Persistence and Long-Running Jobs"
nav_order: 6
parent: CodeMachine CLI Tutorial
---


# Chapter 6: Persistence and Long-Running Jobs

Welcome to **Chapter 6: Persistence and Long-Running Jobs**. In this part of **CodeMachine CLI Tutorial: Orchestrating Long-Running Coding Agent Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


CodeMachine supports workflows that can run for long durations without manual babysitting.

## Durability Checklist

- persist workflow state after each major step
- support resumable execution after interruption
- define timeout and retry policy per step

## Summary

You now have a durability model for running long-horizon coding workflows.

Next: [Chapter 7: Engine Integrations and Compatibility](07-engine-integrations-and-compatibility.md)

## Source Code Walkthrough

### `src/workflows/preflight.ts`

The `checkWorkflowCanStart` function in [`src/workflows/preflight.ts`](https://github.com/moazbuilds/CodeMachine-CLI/blob/HEAD/src/workflows/preflight.ts) handles a key part of this chapter's functionality:

```ts
 * Returns onboarding needs if user configuration is required
 */
export async function checkWorkflowCanStart(options: { cwd?: string } = {}): Promise<OnboardingNeeds> {
  const cwd = options.cwd ? path.resolve(options.cwd) : process.cwd();

  // First check specification requirement (throws if invalid)
  await checkSpecificationRequired({ cwd });

  // Then check onboarding requirements (returns needs, doesn't throw)
  return checkOnboardingRequired({ cwd });
}

/**
 * Quick check if any onboarding is needed
 * Useful for UI to decide whether to show onboarding flow
 */
export function needsOnboarding(needs: OnboardingNeeds): boolean {
  return (
    needs.needsProjectName ||
    needs.needsTrackSelection ||
    needs.needsConditionsSelection ||
    needs.needsControllerSelection
  );
}

```

This function is important because it defines how CodeMachine CLI Tutorial: Orchestrating Long-Running Coding Agent Workflows implements the patterns covered in this chapter.

### `src/workflows/preflight.ts`

The `needsOnboarding` function in [`src/workflows/preflight.ts`](https://github.com/moazbuilds/CodeMachine-CLI/blob/HEAD/src/workflows/preflight.ts) handles a key part of this chapter's functionality:

```ts
 * Useful for UI to decide whether to show onboarding flow
 */
export function needsOnboarding(needs: OnboardingNeeds): boolean {
  return (
    needs.needsProjectName ||
    needs.needsTrackSelection ||
    needs.needsConditionsSelection ||
    needs.needsControllerSelection
  );
}

```

This function is important because it defines how CodeMachine CLI Tutorial: Orchestrating Long-Running Coding Agent Workflows implements the patterns covered in this chapter.

### `src/workflows/preflight.ts`

The `OnboardingNeeds` interface in [`src/workflows/preflight.ts`](https://github.com/moazbuilds/CodeMachine-CLI/blob/HEAD/src/workflows/preflight.ts) handles a key part of this chapter's functionality:

```ts
 * Onboarding requirements - what the user needs to configure before workflow can start
 */
export interface OnboardingNeeds {
  needsProjectName: boolean;
  needsTrackSelection: boolean;
  needsConditionsSelection: boolean;
  needsControllerSelection: boolean;
  /** @deprecated Controller is now pre-specified via controller() function */
  controllerAgents: AgentDefinition[];
  /** The loaded template for reference */
  template: WorkflowTemplate;
}

/**
 * Check what onboarding steps are needed before workflow can start
 * Does NOT throw - returns the requirements for the UI to handle
 */
export async function checkOnboardingRequired(options: { cwd?: string } = {}): Promise<OnboardingNeeds> {
  const cwd = options.cwd ? path.resolve(options.cwd) : process.cwd();
  const cmRoot = path.join(cwd, '.codemachine');

  // Ensure workspace structure exists
  await ensureWorkspaceStructure({ cwd });

  // Ensure imported agents are registered before loading template
  // This allows resolveStep() to find agents from imported packages
  ensureImportedAgentsRegistered();

  // Load template
  const templatePath = await getTemplatePathFromTracking(cmRoot);
  const { template } = await loadTemplateWithPath(cwd, templatePath);

```

This interface is important because it defines how CodeMachine CLI Tutorial: Orchestrating Long-Running Coding Agent Workflows implements the patterns covered in this chapter.

### `src/workflows/run.ts`

The `runWorkflow` function in [`src/workflows/run.ts`](https://github.com/moazbuilds/CodeMachine-CLI/blob/HEAD/src/workflows/run.ts) handles a key part of this chapter's functionality:

```ts
 * Note: Pre-flight checks (specification validation) should be done via preflight.ts before calling this
 */
export async function runWorkflow(options: RunWorkflowOptions = {}): Promise<void> {
  const cwd = options.cwd ? path.resolve(options.cwd) : process.cwd();

  // Ensure workspace structure exists (creates .codemachine folder tree)
  await ensureWorkspaceStructure({ cwd });

  // Auto-register agents from all installed imports
  // This ensures imported agents/modules are available before template loading
  clearImportedAgents();
  const importedPackages = getAllInstalledImports();
  for (const imp of importedPackages) {
    registerImportedAgents(imp.resolvedPaths.config);
  }
  debug('[Workflow] Registered agents from %d imported packages', importedPackages.length);

  // Load template
  const cmRoot = path.join(cwd, '.codemachine');
  const templatePath = options.templatePath || (await getTemplatePathFromTracking(cmRoot));
  const { template } = await loadTemplateWithPath(cwd, templatePath);

  // Ensure template.json exists with correct activeTemplate before any setter functions are called
  // This prevents setControllerView/setSelectedTrack/etc from creating file with empty activeTemplate
  const templateFileName = path.basename(templatePath);
  await setActiveTemplate(cmRoot, templateFileName, template.autonomousMode);

  // Clear screen for TUI
  if (process.stdout.isTTY) {
    process.stdout.write('\x1b[2J\x1b[H');
  }

```

This function is important because it defines how CodeMachine CLI Tutorial: Orchestrating Long-Running Coding Agent Workflows implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[checkWorkflowCanStart]
    B[needsOnboarding]
    C[OnboardingNeeds]
    D[runWorkflow]
    A --> B
    B --> C
    C --> D
```
