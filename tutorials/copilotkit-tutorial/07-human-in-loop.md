---
layout: default
title: "CopilotKit Tutorial - Chapter 7: Human-in-the-Loop"
nav_order: 7
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 7: Human-in-the-Loop - User Approval Flows and Interrupts

> Implement human-in-the-loop workflows where AI agents request user approval for critical actions and handle interruptions gracefully.

## Overview

Human-in-the-loop (HITL) workflows ensure that AI agents can request user approval for important actions, handle interruptions, and maintain user control over critical operations. This chapter covers implementing approval flows, interruption handling, and user-guided AI interactions.

## Basic Approval Flows

### Simple Action Approval

```tsx
// app/components/ApprovalWorkflow.tsx
"use client";

import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { useState } from "react";

interface ApprovalRequest {
  id: string;
  action: string;
  details: any;
  status: "pending" | "approved" | "rejected";
  timestamp: Date;
}

export function ApprovalWorkflow() {
  const [requests, setRequests] = useState<ApprovalRequest[]>([]);
  const [pendingRequest, setPendingRequest] = useState<ApprovalRequest | null>(null);

  // Share current approval state
  useCopilotReadable({
    description: "Current approval requests and their status",
    value: { requests, pendingRequest }
  });

  // Action that requires approval
  useCopilotAction({
    name: "sendEmail",
    description: "Send an email to a recipient (requires user approval)",
    parameters: [
      {
        name: "to",
        type: "string",
        description: "Email recipient address",
        required: true,
      },
      {
        name: "subject",
        type: "string",
        description: "Email subject line",
        required: true,
      },
      {
        name: "body",
        type: "string",
        description: "Email body content",
        required: true,
      },
    ],
    requiresApproval: true, // Enable human-in-the-loop
    handler: async ({ to, subject, body }) => {
      // This will be called after user approval
      console.log(`Sending email to ${to}: ${subject}`);

      // Simulate email sending
      await new Promise(resolve => setTimeout(resolve, 1000));

      return {
        success: true,
        message: `Email sent to ${to}`,
        recipient: to,
        subject: subject
      };
    },
  });

  // Action to process approval decisions
  useCopilotAction({
    name: "handleApproval",
    description: "Process user approval or rejection of pending actions",
    parameters: [
      {
        name: "requestId",
        type: "string",
        description: "ID of the approval request",
        required: true,
      },
      {
        name: "decision",
        type: "string",
        description: "Approval decision: 'approve' or 'reject'",
        enum: ["approve", "reject"],
        required: true,
      },
      {
        name: "reason",
        type: "string",
        description: "Optional reason for the decision",
      },
    ],
    handler: async ({ requestId, decision, reason }) => {
      const request = requests.find(r => r.id === requestId);
      if (!request) {
        throw new Error("Approval request not found");
      }

      // Update request status
      const updatedRequests = requests.map(r =>
        r.id === requestId
          ? { ...r, status: decision as "approved" | "rejected", reason }
          : r
      );

      setRequests(updatedRequests);

      if (decision === "approved") {
        // Execute the approved action
        // In a real implementation, this would trigger the actual action
        console.log(`Approved action: ${request.action}`);
      }

      setPendingRequest(null);

      return {
        success: true,
        decision,
        requestId,
        action: request.action
      };
    },
  });

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Human-in-the-Loop Approval System</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Approval Interface */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Approval Requests</h2>

            {requests.length === 0 ? (
              <p className="text-gray-500">No approval requests yet. Try asking the AI to send an email.</p>
            ) : (
              <div className="space-y-3">
                {requests.map(request => (
                  <div
                    key={request.id}
                    className={`p-4 border rounded-lg ${
                      request.status === "approved" ? "border-green-200 bg-green-50" :
                      request.status === "rejected" ? "border-red-200 bg-red-50" :
                      "border-yellow-200 bg-yellow-50"
                    }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium">{request.action}</h3>
                      <span className={`px-2 py-1 text-xs rounded ${
                        request.status === "approved" ? "bg-green-100 text-green-800" :
                        request.status === "rejected" ? "bg-red-100 text-red-800" :
                        "bg-yellow-100 text-yellow-800"
                      }`}>
                        {request.status}
                      </span>
                    </div>

                    <div className="text-sm text-gray-600 mb-2">
                      {new Date(request.timestamp).toLocaleString()}
                    </div>

                    {request.details && (
                      <div className="text-sm mb-2">
                        <strong>Details:</strong>
                        <pre className="mt-1 text-xs bg-gray-100 p-2 rounded overflow-x-auto">
                          {JSON.stringify(request.details, null, 2)}
                        </pre>
                      </div>
                    )}

                    {request.reason && (
                      <div className="text-sm">
                        <strong>Reason:</strong> {request.reason}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Pending Approval Modal */}
          {pendingRequest && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white p-6 rounded-lg shadow-xl max-w-md w-full mx-4">
                <h3 className="text-lg font-semibold mb-4">Approval Required</h3>

                <div className="mb-4">
                  <p className="text-gray-700 mb-2">
                    <strong>Action:</strong> {pendingRequest.action}
                  </p>

                  {pendingRequest.details && (
                    <div className="bg-gray-50 p-3 rounded text-sm">
                      <pre className="overflow-x-auto">
                        {JSON.stringify(pendingRequest.details, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => {
                      // Approve action
                      const updatedRequests = requests.map(r =>
                        r.id === pendingRequest.id
                          ? { ...r, status: "approved" as const }
                          : r
                      );
                      setRequests(updatedRequests);
                      setPendingRequest(null);
                    }}
                    className="flex-1 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                  >
                    Approve
                  </button>

                  <button
                    onClick={() => {
                      // Reject action
                      const updatedRequests = requests.map(r =>
                        r.id === pendingRequest.id
                          ? { ...r, status: "rejected" as const }
                          : r
                      );
                      setRequests(updatedRequests);
                      setPendingRequest(null);
                    }}
                    className="flex-1 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    Reject
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        <div className="space-y-6">
          <div className="bg-blue-50 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">How It Works</h2>

            <div className="space-y-4 text-blue-800">
              <div>
                <h3 className="font-medium mb-1">1. AI Requests Approval</h3>
                <p className="text-sm">When the AI wants to perform a sensitive action (like sending emails), it creates an approval request.</p>
              </div>

              <div>
                <h3 className="font-medium mb-1">2. User Reviews Request</h3>
                <p className="text-sm">You review the action details and decide whether to approve or reject it.</p>
              </div>

              <div>
                <h3 className="font-medium mb-1">3. Action Execution</h3>
                <p className="text-sm">If approved, the action is executed. If rejected, it's cancelled with an optional reason.</p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-green-900 mb-4">Try These Commands:</h2>

            <ul className="text-green-800 text-sm space-y-2">
              <li>• "Send an email to john@example.com about the project update"</li>
              <li>• "Email the team about the meeting tomorrow at 2 PM"</li>
              <li>• "Send a follow-up email to the client"</li>
            </ul>

            <div className="mt-4 p-3 bg-green-100 rounded">
              <p className="text-sm text-green-700">
                <strong>Note:</strong> These actions will create approval requests that you can review and approve.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### Interrupt Handling

```tsx
// app/components/InterruptHandler.tsx
"use client";

import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { useState, useCallback } from "react";

interface WorkflowState {
  currentStep: string;
  progress: number;
  data: any;
  canInterrupt: boolean;
}

export function InterruptHandler() {
  const [workflowState, setWorkflowState] = useState<WorkflowState>({
    currentStep: "idle",
    progress: 0,
    data: {},
    canInterrupt: false
  });

  const [interruptions, setInterruptions] = useState<any[]>([]);

  // Share workflow state
  useCopilotReadable({
    description: "Current workflow state and progress",
    value: workflowState
  });

  // Share interruption history
  useCopilotReadable({
    description: "History of workflow interruptions and resolutions",
    value: interruptions
  });

  // Long-running workflow action
  useCopilotAction({
    name: "complexAnalysis",
    description: "Perform complex data analysis (can be interrupted)",
    parameters: [
      {
        name: "dataset",
        type: "string",
        description: "Type of dataset to analyze",
        enum: ["sales", "user-behavior", "performance"],
        required: true,
      },
      {
        name: "analysisType",
        type: "string",
        description: "Type of analysis to perform",
        enum: ["summary", "trends", "anomalies", "predictions"],
        required: true,
      },
    ],
    interruptible: true, // Allow interruptions
    handler: async ({ dataset, analysisType }) => {
      const steps = [
        "Loading dataset",
        "Preprocessing data",
        "Running analysis",
        "Generating insights",
        "Creating visualizations"
      ];

      for (let i = 0; i < steps.length; i++) {
        // Check for interruptions before each step
        if (workflowState.currentStep === "interrupted") {
          throw new Error("Workflow was interrupted by user");
        }

        setWorkflowState(prev => ({
          ...prev,
          currentStep: steps[i],
          progress: ((i + 1) / steps.length) * 100,
          canInterrupt: true
        }));

        // Simulate work
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Check again for interruptions
        if (workflowState.currentStep === "interrupted") {
          throw new Error("Workflow interrupted during execution");
        }
      }

      return {
        success: true,
        dataset,
        analysisType,
        insights: [
          "Found significant trend in Q4",
          "Anomaly detected in user engagement",
          "Predicted 15% growth for next quarter"
        ]
      };
    },
  });

  // Interrupt action
  useCopilotAction({
    name: "interruptWorkflow",
    description: "Interrupt the currently running workflow",
    parameters: [
      {
        name: "reason",
        type: "string",
        description: "Reason for interrupting the workflow",
        required: true,
      },
    ],
    handler: async ({ reason }) => {
      if (workflowState.currentStep === "idle") {
        throw new Error("No workflow is currently running");
      }

      const interruption = {
        timestamp: new Date(),
        reason,
        interruptedStep: workflowState.currentStep,
        progressAtInterruption: workflowState.progress
      };

      setInterruptions(prev => [...prev, interruption]);

      setWorkflowState(prev => ({
        ...prev,
        currentStep: "interrupted",
        canInterrupt: false
      }));

      return {
        success: true,
        message: "Workflow interrupted successfully",
        interruption
      };
    },
  });

  // Resume workflow
  useCopilotAction({
    name: "resumeWorkflow",
    description: "Resume a previously interrupted workflow",
    parameters: [
      {
        name: "fromStep",
        type: "string",
        description: "Step to resume from",
        enum: ["continue", "restart"],
        default: "continue",
      },
    ],
    handler: async ({ fromStep }) => {
      if (workflowState.currentStep !== "interrupted") {
        throw new Error("No interrupted workflow to resume");
      }

      if (fromStep === "restart") {
        setWorkflowState({
          currentStep: "idle",
          progress: 0,
          data: {},
          canInterrupt: false
        });
        return { success: true, message: "Workflow restarted" };
      } else {
        // Continue from interruption point
        setWorkflowState(prev => ({
          ...prev,
          currentStep: "resuming",
          canInterrupt: true
        }));
        return { success: true, message: "Workflow resumed from interruption point" };
      }
    },
  });

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Interruptible Workflow System</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Workflow Control */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Workflow Status</h2>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>Current Step:</span>
                  <span className={`font-medium ${
                    workflowState.currentStep === "idle" ? "text-gray-500" :
                    workflowState.currentStep === "interrupted" ? "text-red-600" :
                    "text-blue-600"
                  }`}>
                    {workflowState.currentStep}
                  </span>
                </div>
              </div>

              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Progress:</span>
                  <span>{workflowState.progress.toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${workflowState.progress}%` }}
                  ></div>
                </div>
              </div>

              {workflowState.canInterrupt && (
                <div className="p-3 bg-yellow-50 border border-yellow-200 rounded">
                  <p className="text-sm text-yellow-800">
                    ⚠️ Workflow is running and can be interrupted
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Control Buttons */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Workflow Controls</h2>

            <div className="space-y-3">
              <button
                onClick={() => {
                  // Simulate starting analysis
                  setWorkflowState(prev => ({
                    ...prev,
                    currentStep: "Starting analysis...",
                    progress: 0,
                    canInterrupt: true
                  }));
                }}
                disabled={workflowState.currentStep !== "idle" && workflowState.currentStep !== "interrupted"}
                className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                Start Analysis Workflow
              </button>

              {workflowState.canInterrupt && (
                <button
                  onClick={() => {
                    setWorkflowState(prev => ({
                      ...prev,
                      currentStep: "interrupted",
                      canInterrupt: false
                    }));
                  }}
                  className="w-full px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Interrupt Workflow
                </button>
              )}

              {workflowState.currentStep === "interrupted" && (
                <div className="space-y-2">
                  <button
                    onClick={() => {
                      setWorkflowState(prev => ({
                        ...prev,
                        currentStep: "resuming",
                        canInterrupt: true
                      }));
                    }}
                    className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                  >
                    Resume Workflow
                  </button>

                  <button
                    onClick={() => {
                      setWorkflowState({
                        currentStep: "idle",
                        progress: 0,
                        data: {},
                        canInterrupt: false
                      });
                    }}
                    className="w-full px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                  >
                    Restart Workflow
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Interruption History */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Interruption History</h2>

            {interruptions.length === 0 ? (
              <p className="text-gray-500">No interruptions recorded yet.</p>
            ) : (
              <div className="space-y-3">
                {interruptions.map((interruption, index) => (
                  <div key={index} className="p-3 bg-red-50 border border-red-200 rounded">
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium">Interrupted at:</span>
                      <span>{interruption.interruptedStep}</span>
                    </div>
                    <div className="text-sm text-red-800 mb-1">
                      <strong>Reason:</strong> {interruption.reason}
                    </div>
                    <div className="text-xs text-red-600">
                      {interruption.timestamp.toLocaleString()} • {interruption.progressAtInterruption}% complete
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="bg-blue-50 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">Try These Commands:</h2>

            <ul className="text-blue-800 text-sm space-y-2">
              <li>• "Start analyzing the sales data for trends"</li>
              <li>• "Interrupt the current analysis" (during execution)</li>
              <li>• "Resume the interrupted workflow"</li>
              <li>• "Start a new analysis from the beginning"</li>
            </ul>

            <div className="mt-4 p-3 bg-blue-100 rounded">
              <p className="text-sm text-blue-700">
                <strong>Tip:</strong> Try interrupting workflows to see how the system handles user interventions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Advanced Approval Patterns

### Multi-Level Approvals

```tsx
// app/components/MultiLevelApproval.tsx
"use client";

import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";
import { useState } from "react";

interface ApprovalLevel {
  id: string;
  name: string;
  requiredRole: string;
  description: string;
}

interface ApprovalRequest {
  id: string;
  action: string;
  details: any;
  approvalLevels: ApprovalLevel[];
  currentLevel: number;
  status: "pending" | "approved" | "rejected" | "partial";
  approvals: any[];
  timestamp: Date;
}

export function MultiLevelApproval() {
  const [requests, setRequests] = useState<ApprovalRequest[]>([]);
  const [userRole, setUserRole] = useState("employee");

  // Share user context
  useCopilotReadable({
    description: "Current user's role and permissions",
    value: { role: userRole, canApprove: ["manager", "director", "admin"].includes(userRole) }
  });

  // Share approval requests
  useCopilotReadable({
    description: "Multi-level approval requests and their current status",
    value: requests
  });

  // Action requiring multi-level approval
  useCopilotAction({
    name: "requestBudgetIncrease",
    description: "Request a budget increase (requires multiple approvals)",
    parameters: [
      {
        name: "amount",
        type: "number",
        description: "Requested budget increase amount",
        required: true,
      },
      {
        name: "reason",
        type: "string",
        description: "Reason for the budget increase",
        required: true,
      },
      {
        name: "department",
        type: "string",
        description: "Department requesting the increase",
        required: true,
      },
    ],
    requiresApproval: true,
    approvalLevels: [
      {
        id: "manager",
        name: "Department Manager",
        requiredRole: "manager",
        description: "Initial approval from department manager"
      },
      {
        id: "director",
        name: "Department Director",
        requiredRole: "director",
        description: "Secondary approval from department director"
      },
      {
        id: "finance",
        name: "Finance Review",
        requiredRole: "admin",
        description: "Final approval from finance department"
      }
    ],
    handler: async ({ amount, reason, department }) => {
      const approvalLevels = [
        {
          id: "manager",
          name: "Department Manager",
          requiredRole: "manager",
          description: "Initial approval from department manager"
        },
        {
          id: "director",
          name: "Department Director",
          requiredRole: "director",
          description: "Secondary approval from department director"
        },
        {
          id: "finance",
          name: "Finance Review",
          requiredRole: "admin",
          description: "Final approval from finance department"
        }
      ];

      const request: ApprovalRequest = {
        id: Date.now().toString(),
        action: `Budget increase request: $${amount.toLocaleString()}`,
        details: { amount, reason, department },
        approvalLevels,
        currentLevel: 0,
        status: "pending",
        approvals: [],
        timestamp: new Date()
      };

      setRequests(prev => [...prev, request]);

      return {
        success: true,
        requestId: request.id,
        message: "Budget increase request submitted for approval",
        nextApprover: approvalLevels[0].name
      };
    },
  });

  // Action to process approvals
  useCopilotAction({
    name: "processApproval",
    description: "Approve or reject an approval request at your level",
    parameters: [
      {
        name: "requestId",
        type: "string",
        description: "ID of the approval request",
        required: true,
      },
      {
        name: "decision",
        type: "string",
        description: "Approval decision",
        enum: ["approve", "reject"],
        required: true,
      },
      {
        name: "comments",
        type: "string",
        description: "Optional comments about the decision",
      },
    ],
    handler: async ({ requestId, decision, comments }) => {
      const request = requests.find(r => r.id === requestId);
      if (!request) {
        throw new Error("Approval request not found");
      }

      const currentLevel = request.approvalLevels[request.currentLevel];
      if (!currentLevel) {
        throw new Error("No more approval levels");
      }

      // Check if user has required role
      if (currentLevel.requiredRole !== userRole) {
        throw new Error(`You don't have the required role (${currentLevel.requiredRole}) to approve this request`);
      }

      const approval = {
        level: request.currentLevel,
        approverRole: userRole,
        decision,
        comments: comments || "",
        timestamp: new Date()
      };

      const updatedRequests = requests.map(r => {
        if (r.id === requestId) {
          const newApprovals = [...r.approvals, approval];

          let newStatus = r.status;
          let newCurrentLevel = r.currentLevel;

          if (decision === "reject") {
            newStatus = "rejected";
          } else if (r.currentLevel + 1 >= r.approvalLevels.length) {
            newStatus = "approved";
          } else {
            newCurrentLevel = r.currentLevel + 1;
            newStatus = "partial";
          }

          return {
            ...r,
            approvals: newApprovals,
            currentLevel: newCurrentLevel,
            status: newStatus
          };
        }
        return r;
      });

      setRequests(updatedRequests);

      return {
        success: true,
        decision,
        level: currentLevel.name,
        nextLevel: decision === "approve" && request.currentLevel + 1 < request.approvalLevels.length
          ? request.approvalLevels[request.currentLevel + 1].name
          : null
      };
    },
  });

  const getPendingRequestsForUser = () => {
    return requests.filter(request =>
      request.status === "pending" || request.status === "partial"
    ).filter(request => {
      const currentLevel = request.approvalLevels[request.currentLevel];
      return currentLevel && currentLevel.requiredRole === userRole;
    });
  };

  const pendingRequests = getPendingRequestsForUser();

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Multi-Level Approval System</h1>

      {/* Role Selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Your Role (for testing different approval levels):
        </label>
        <select
          value={userRole}
          onChange={(e) => setUserRole(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md"
        >
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="director">Director</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Approval Requests */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">All Requests</h2>

            {requests.length === 0 ? (
              <p className="text-gray-500">No approval requests yet.</p>
            ) : (
              <div className="space-y-4">
                {requests.map(request => (
                  <div
                    key={request.id}
                    className={`p-4 border rounded-lg ${
                      request.status === "approved" ? "border-green-200 bg-green-50" :
                      request.status === "rejected" ? "border-red-200 bg-red-50" :
                      request.status === "partial" ? "border-yellow-200 bg-yellow-50" :
                      "border-blue-200 bg-blue-50"
                    }`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium">{request.action}</h3>
                      <span className={`px-2 py-1 text-xs rounded ${
                        request.status === "approved" ? "bg-green-100 text-green-800" :
                        request.status === "rejected" ? "bg-red-100 text-red-800" :
                        request.status === "partial" ? "bg-yellow-100 text-yellow-800" :
                        "bg-blue-100 text-blue-800"
                      }`}>
                        {request.status}
                      </span>
                    </div>

                    <div className="text-sm text-gray-600 mb-2">
                      {request.details.department} • ${request.details.amount.toLocaleString()}
                    </div>

                    <div className="text-sm mb-3">
                      <strong>Reason:</strong> {request.details.reason}
                    </div>

                    {/* Approval Progress */}
                    <div className="space-y-2">
                      <div className="text-sm font-medium">Approval Progress:</div>
                      {request.approvalLevels.map((level, index) => {
                        const approval = request.approvals.find(a => a.level === index);
                        return (
                          <div key={index} className="flex items-center space-x-2 text-sm">
                            <div className={`w-4 h-4 rounded-full ${
                              approval ? (approval.decision === "approve" ? "bg-green-500" : "bg-red-500") :
                              index < request.currentLevel ? "bg-gray-400" :
                              index === request.currentLevel ? "bg-blue-500" : "bg-gray-200"
                            }`}></div>
                            <span className={approval ? "line-through" : ""}>{level.name}</span>
                            {approval && (
                              <span className="text-xs">
                                ({approval.decision === "approve" ? "✓" : "✗"})
                              </span>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Pending Approvals */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Your Pending Approvals</h2>

            {pendingRequests.length === 0 ? (
              <p className="text-gray-500">No pending approvals for your role.</p>
            ) : (
              <div className="space-y-4">
                {pendingRequests.map(request => {
                  const currentLevel = request.approvalLevels[request.currentLevel];
                  return (
                    <div key={request.id} className="p-4 border border-blue-200 bg-blue-50 rounded-lg">
                      <h3 className="font-medium mb-2">{request.action}</h3>

                      <div className="text-sm text-gray-600 mb-3">
                        <div>Department: {request.details.department}</div>
                        <div>Amount: ${request.details.amount.toLocaleString()}</div>
                        <div>Reason: {request.details.reason}</div>
                      </div>

                      <div className="mb-4 p-3 bg-white rounded">
                        <div className="text-sm">
                          <strong>Current Level:</strong> {currentLevel.name}
                        </div>
                        <div className="text-sm text-gray-600 mt-1">
                          {currentLevel.description}
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            const updatedRequests = requests.map(r =>
                              r.id === request.id ? {
                                ...r,
                                approvals: [...r.approvals, {
                                  level: r.currentLevel,
                                  approverRole: userRole,
                                  decision: "approve",
                                  comments: "",
                                  timestamp: new Date()
                                }],
                                currentLevel: r.currentLevel + 1,
                                status: r.currentLevel + 1 >= r.approvalLevels.length ? "approved" : "partial"
                              } : r
                            );
                            setRequests(updatedRequests);
                          }}
                          className="flex-1 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 text-sm"
                        >
                          Approve
                        </button>

                        <button
                          onClick={() => {
                            const updatedRequests = requests.map(r =>
                              r.id === request.id ? {
                                ...r,
                                approvals: [...r.approvals, {
                                  level: r.currentLevel,
                                  approverRole: userRole,
                                  decision: "reject",
                                  comments: "",
                                  timestamp: new Date()
                                }],
                                status: "rejected"
                              } : r
                            );
                            setRequests(updatedRequests);
                          }}
                          className="flex-1 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <div className="bg-green-50 p-6 rounded-lg">
            <h2 className="text-xl font-semibold text-green-900 mb-4">Try These Commands:</h2>

            <ul className="text-green-800 text-sm space-y-2">
              <li>• "Request a $50,000 budget increase for the marketing department because we need to launch a new campaign"</li>
              <li>• "Change my role to manager to test the approval flow"</li>
              <li>• "As a director, approve the pending budget request"</li>
              <li>• "Submit another budget request for $25,000 for IT infrastructure"</li>
            </ul>

            <div className="mt-4 p-3 bg-green-100 rounded">
              <p className="text-sm text-green-700">
                <strong>Note:</strong> Change your role using the dropdown to test different approval levels.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Summary

In this chapter, we've covered:

- **Basic Approval Flows**: Simple user confirmation for actions
- **Interrupt Handling**: Graceful workflow interruption and resumption
- **Multi-Level Approvals**: Complex approval chains with different roles
- **User Control**: Maintaining human oversight over AI actions
- **State Management**: Tracking approval status and workflow progress
- **Error Recovery**: Handling approval failures and edge cases

## Key Takeaways

1. **User Control**: Human-in-the-loop ensures AI actions have proper oversight
2. **Flexible Approvals**: Different approval patterns for different action types
3. **Interrupt Capability**: Workflows can be safely interrupted and resumed
4. **Multi-Level Security**: Complex approval chains for high-stakes actions
5. **State Persistence**: Approval and interruption state is maintained
6. **Error Handling**: Robust handling of approval failures and edge cases

## Next Steps

Now that you can implement human-in-the-loop workflows, let's explore production deployment considerations.

---

**Ready for Chapter 8?** [Production Deployment](08-production.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*