---
layout: default
title: "CopilotKit Tutorial - Chapter 6: CoAgents & LangGraph"
nav_order: 6
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 6: CoAgents & LangGraph - Building Agentic Workflows

> Create sophisticated agentic workflows using CoAgents and LangGraph integration for complex, multi-step processes.

## Overview

CoAgents brings the power of LangGraph to CopilotKit, enabling complex agentic workflows with human-in-the-loop interactions. This chapter covers building sophisticated multi-agent systems and workflow automation.

## CoAgents Fundamentals

### Basic CoAgent Setup

```tsx
// app/components/BasicCoAgent.tsx
"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { useState } from "react";

export function BasicCoAgent() {
  const [workflowState, setWorkflowState] = useState<any>({});
  const [isRunning, setIsRunning] = useState(false);

  // Define a simple workflow agent
  const { runWorkflow, state } = useCoAgent({
    name: "task_planner",
    description: "A simple task planning and execution agent",
    workflow: {
      nodes: {
        analyze: {
          type: "action",
          action: async (input: any) => {
            // Analyze the input and break it down
            const tasks = input.description.split(/[,.]/)
              .map((task: string) => task.trim())
              .filter((task: string) => task.length > 0);

            return {
              analysis: `Found ${tasks.length} tasks to complete`,
              tasks: tasks,
              priority: input.priority || "medium"
            };
          }
        },
        execute: {
          type: "action",
          action: async (input: any) => {
            // Simulate task execution
            const results = [];
            for (const task of input.tasks) {
              results.push({
                task,
                status: "completed",
                duration: Math.floor(Math.random() * 10) + 1
              });
            }

            return {
              execution_results: results,
              total_duration: results.reduce((sum, r) => sum + r.duration, 0)
            };
          }
        },
        report: {
          type: "action",
          action: async (input: any) => {
            // Generate execution report
            return {
              summary: `Completed ${input.execution_results.length} tasks in ${input.total_duration} minutes`,
              details: input.execution_results,
              efficiency: input.execution_results.length / input.total_duration
            };
          }
        }
      },
      edges: [
        { from: "analyze", to: "execute" },
        { from: "execute", to: "report" }
      ]
    }
  });

  const handleStartWorkflow = async () => {
    setIsRunning(true);
    try {
      const result = await runWorkflow({
        description: "Buy groceries, finish report, call dentist, schedule meeting",
        priority: "high"
      });
      setWorkflowState(result);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Basic CoAgent Workflow</h1>

      <div className="space-y-6">
        {/* Workflow Trigger */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Task Planning Agent</h2>
          <p className="text-gray-600 mb-4">
            This CoAgent will analyze tasks, execute them, and generate a report.
          </p>

          <button
            onClick={handleStartWorkflow}
            disabled={isRunning}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isRunning ? "Running Workflow..." : "Start Task Planning Workflow"}
          </button>
        </div>

        {/* Workflow State */}
        {Object.keys(workflowState).length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Workflow Results</h2>

            <div className="space-y-4">
              {workflowState.analysis && (
                <div className="p-3 bg-blue-50 rounded">
                  <h3 className="font-medium text-blue-900">Analysis</h3>
                  <p className="text-blue-800">{workflowState.analysis}</p>
                </div>
              )}

              {workflowState.execution_results && (
                <div className="p-3 bg-green-50 rounded">
                  <h3 className="font-medium text-green-900">Execution Results</h3>
                  <ul className="text-green-800 space-y-1">
                    {workflowState.execution_results.map((result: any, index: number) => (
                      <li key={index}>
                        ✓ {result.task} ({result.duration} min)
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {workflowState.summary && (
                <div className="p-3 bg-purple-50 rounded">
                  <h3 className="font-medium text-purple-900">Summary</h3>
                  <p className="text-purple-800">{workflowState.summary}</p>
                  <p className="text-sm text-purple-700 mt-1">
                    Efficiency: {workflowState.efficiency?.toFixed(2)} tasks/minute
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Current State */}
        {state && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-medium mb-2">Current State</h3>
            <pre className="text-sm text-gray-600 overflow-x-auto">
              {JSON.stringify(state, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
```

### LangGraph Integration

```tsx
// app/components/LangGraphAgent.tsx
"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { useState } from "react";

export function LangGraphAgent() {
  const [researchTopic, setResearchTopic] = useState("");
  const [isResearching, setIsResearching] = useState(false);
  const [researchResults, setResearchResults] = useState<any>({});

  // Advanced research agent using LangGraph
  const { runWorkflow, state } = useCoAgent({
    name: "research_agent",
    description: "Comprehensive research agent using LangGraph workflows",
    workflow: {
      // LangGraph-style workflow definition
      graph: {
        nodes: {
          plan_research: {
            type: "agent",
            agent: "planning_agent",
            prompt: "Create a research plan for the given topic. Break it down into specific research questions and data sources to investigate."
          },
          gather_data: {
            type: "action",
            action: async (input: any) => {
              // Simulate data gathering from multiple sources
              const sources = ["academic_papers", "news_articles", "social_media", "official_reports"];

              const results = {};
              for (const source of sources) {
                results[source] = {
                  count: Math.floor(Math.random() * 10) + 1,
                  quality: ["low", "medium", "high"][Math.floor(Math.random() * 3)],
                  relevance: Math.floor(Math.random() * 100) + 1
                };
              }

              return {
                data_sources: results,
                total_sources: sources.length,
                avg_relevance: Object.values(results).reduce((sum: any, r: any) => sum + r.relevance, 0) / sources.length
              };
            }
          },
          analyze_findings: {
            type: "agent",
            agent: "analysis_agent",
            prompt: "Analyze the gathered data and identify key insights, trends, and conclusions. Provide evidence-based reasoning."
          },
          generate_report: {
            type: "action",
            action: async (input: any) => {
              // Generate comprehensive research report
              return {
                title: `Research Report: ${input.topic}`,
                executive_summary: `Comprehensive analysis of ${input.topic} based on ${input.total_sources} data sources.`,
                key_findings: [
                  "Primary trend identified with supporting evidence",
                  "Secondary insights with data correlations",
                  "Future implications and recommendations"
                ],
                methodology: "Multi-source data collection and analysis",
                confidence_level: "High (85%+ data coverage)",
                recommendations: [
                  "Implement findings in strategic planning",
                  "Further research in identified gaps",
                  "Monitor trends for future developments"
                ]
              };
            }
          },
          peer_review: {
            type: "agent",
            agent: "review_agent",
            prompt: "Review the research report for accuracy, completeness, and soundness of conclusions. Provide constructive feedback."
          }
        },
        edges: [
          { from: "plan_research", to: "gather_data" },
          { from: "gather_data", to: "analyze_findings" },
          { from: "analyze_findings", to: "generate_report" },
          { from: "generate_report", to: "peer_review" }
        ],
        // Conditional routing based on results
        conditional_edges: [
          {
            from: "peer_review",
            condition: (state: any) => state.review_score > 80,
            to: "finalize_report"
          },
          {
            from: "peer_review",
            condition: (state: any) => state.review_score <= 80,
            to: "revise_report"
          }
        ]
      }
    }
  });

  const handleStartResearch = async () => {
    if (!researchTopic.trim()) return;

    setIsResearching(true);
    try {
      const results = await runWorkflow({
        topic: researchTopic,
        depth: "comprehensive",
        sources: ["academic", "news", "social", "official"]
      });
      setResearchResults(results);
    } finally {
      setIsResearching(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">LangGraph Research Agent</h1>

      <div className="space-y-6">
        {/* Research Input */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Research Topic</h2>

          <div className="space-y-4">
            <input
              type="text"
              value={researchTopic}
              onChange={(e) => setResearchTopic(e.target.value)}
              placeholder="Enter research topic (e.g., 'impact of AI on healthcare')"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button
              onClick={handleStartResearch}
              disabled={!researchTopic.trim() || isResearching}
              className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isResearching ? "Researching..." : "Start Comprehensive Research"}
            </button>
          </div>

          <div className="mt-4 text-sm text-gray-600">
            This will execute a multi-step research workflow using LangGraph agents for planning, data gathering, analysis, and reporting.
          </div>
        </div>

        {/* Workflow Progress */}
        {isResearching && (
          <div className="bg-blue-50 p-6 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-3">Research Workflow Progress</h3>
            <div className="space-y-2">
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-blue-800">Planning research approach...</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-gray-300 rounded-full"></div>
                <span className="text-gray-600">Gathering data from sources...</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-gray-300 rounded-full"></div>
                <span className="text-gray-600">Analyzing findings...</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-4 h-4 bg-gray-300 rounded-full"></div>
                <span className="text-gray-600">Generating report...</span>
              </div>
            </div>
          </div>
        )}

        {/* Research Results */}
        {Object.keys(researchResults).length > 0 && (
          <div className="space-y-6">
            {/* Executive Summary */}
            {researchResults.title && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-2xl font-semibold mb-4">{researchResults.title}</h2>
                {researchResults.executive_summary && (
                  <p className="text-gray-700 mb-4">{researchResults.executive_summary}</p>
                )}
              </div>
            )}

            {/* Key Findings */}
            {researchResults.key_findings && (
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-xl font-semibold mb-4">Key Findings</h3>
                <ul className="space-y-3">
                  {researchResults.key_findings.map((finding: string, index: number) => (
                    <li key={index} className="flex items-start space-x-3">
                      <span className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0 mt-0.5">
                        {index + 1}
                      </span>
                      <span className="text-gray-700">{finding}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Methodology */}
            {researchResults.methodology && (
              <div className="bg-green-50 p-6 rounded-lg">
                <h3 className="font-semibold text-green-900 mb-2">Methodology</h3>
                <p className="text-green-800">{researchResults.methodology}</p>
                {researchResults.confidence_level && (
                  <p className="text-sm text-green-700 mt-1">
                    Confidence Level: {researchResults.confidence_level}
                  </p>
                )}
              </div>
            )}

            {/* Recommendations */}
            {researchResults.recommendations && (
              <div className="bg-purple-50 p-6 rounded-lg">
                <h3 className="font-semibold text-purple-900 mb-3">Recommendations</h3>
                <ul className="space-y-2">
                  {researchResults.recommendations.map((rec: string, index: number) => (
                    <li key={index} className="flex items-start space-x-3">
                      <span className="text-purple-800">•</span>
                      <span className="text-purple-800">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Data Sources Summary */}
            {researchResults.data_sources && (
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-3">Data Sources Analyzed</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(researchResults.data_sources).map(([source, data]: [string, any]) => (
                    <div key={source} className="bg-white p-3 rounded border">
                      <div className="font-medium text-gray-900 capitalize">{source.replace('_', ' ')}</div>
                      <div className="text-sm text-gray-600">
                        {data.count} items
                        <br />
                        Quality: {data.quality}
                        <br />
                        Relevance: {data.relevance}%
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-3 text-sm text-gray-600">
                  Average Relevance: {researchResults.avg_relevance?.toFixed(1)}%
                </div>
              </div>
            )}
          </div>
        )}

        {/* Agent State Debug */}
        {state && Object.keys(state).length > 0 && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-medium mb-2">Agent State (Debug)</h3>
            <details>
              <summary className="cursor-pointer text-sm text-gray-600">Show current state</summary>
              <pre className="text-xs text-gray-500 mt-2 overflow-x-auto">
                {JSON.stringify(state, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
```

## Advanced CoAgent Patterns

### Multi-Agent Collaboration

```tsx
// app/components/MultiAgentCollaboration.tsx
"use client";

import { useCoAgent } from "@copilotkit/react-core";
import { useState } from "react";

export function MultiAgentCollaboration() {
  const [project, setProject] = useState<any>({});
  const [isPlanning, setIsPlanning] = useState(false);

  // Multi-agent project planning system
  const { runWorkflow, state } = useCoAgent({
    name: "project_planning_team",
    description: "Multi-agent team for comprehensive project planning",
    workflow: {
      // Define multiple agents with different roles
      agents: {
        product_manager: {
          role: "Product Manager",
          expertise: "Requirements analysis, user stories, prioritization",
          personality: "Strategic, user-focused, business-oriented"
        },
        architect: {
          role: "System Architect",
          expertise: "Technical design, scalability, technology selection",
          personality: "Technical, forward-thinking, risk-aware"
        },
        developer: {
          role: "Lead Developer",
          expertise: "Implementation planning, task breakdown, estimation",
          personality: "Practical, detail-oriented, delivery-focused"
        },
        qa_engineer: {
          role: "QA Engineer",
          expertise: "Testing strategy, quality assurance, risk assessment",
          personality: "Thorough, quality-focused, preventive"
        }
      },

      // Complex workflow with agent interactions
      graph: {
        nodes: {
          requirements_gathering: {
            type: "agent",
            agent: "product_manager",
            prompt: "Analyze the project requirements and create detailed user stories with acceptance criteria."
          },

          technical_design: {
            type: "agent",
            agent: "architect",
            prompt: "Design the system architecture based on requirements. Consider scalability, security, and technology choices."
          },

          implementation_planning: {
            type: "agent",
            agent: "developer",
            prompt: "Break down the technical design into implementable tasks with time estimates and dependencies."
          },

          quality_planning: {
            type: "agent",
            agent: "qa_engineer",
            prompt: "Develop testing strategy and quality assurance plan for the project implementation."
          },

          risk_assessment: {
            type: "action",
            action: async (input: any) => {
              // Cross-agent risk analysis
              const risks = [];

              // Technical risks
              if (input.technical_complexity > 7) {
                risks.push({
                  category: "Technical",
                  level: "High",
                  description: "High technical complexity may impact delivery timeline",
                  mitigation: "Additional senior developer allocation"
                });
              }

              // Business risks
              if (input.market_uncertainty > 6) {
                risks.push({
                  category: "Business",
                  level: "Medium",
                  description: "Market uncertainty requires flexible scoping",
                  mitigation: "Implement MVP-first approach"
                });
              }

              return {
                identified_risks: risks,
                risk_count: risks.length,
                high_priority_risks: risks.filter(r => r.level === "High").length
              };
            }
          },

          final_plan_synthesis: {
            type: "agent",
            agent: "product_manager",
            prompt: "Synthesize all planning inputs into a comprehensive project plan with timeline, milestones, and success criteria."
          }
        },

        edges: [
          { from: "requirements_gathering", to: "technical_design" },
          { from: "technical_design", to: "implementation_planning" },
          { from: "implementation_planning", to: "quality_planning" },
          { from: "quality_planning", to: "risk_assessment" },
          { from: "technical_design", to: "risk_assessment" },
          { from: "requirements_gathering", to: "risk_assessment" },
          { from: "risk_assessment", to: "final_plan_synthesis" },
          { from: "implementation_planning", to: "final_plan_synthesis" },
          { from: "quality_planning", to: "final_plan_synthesis" }
        ]
      }
    }
  });

  const handlePlanProject = async () => {
    const projectIdea = "Build an AI-powered task management application with real-time collaboration features";

    setIsPlanning(true);
    try {
      const plan = await runWorkflow({
        project_idea: projectIdea,
        timeline_weeks: 12,
        team_size: 5,
        budget_level: "medium",
        technical_complexity: 6,
        market_uncertainty: 4
      });
      setProject(plan);
    } finally {
      setIsPlanning(false);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Multi-Agent Project Planning</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Planning Interface */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">AI Planning Team</h2>
            <p className="text-gray-600 mb-4">
              This CoAgent workflow uses multiple AI agents with different roles to create comprehensive project plans.
            </p>

            <div className="space-y-3 mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span className="text-sm">Product Manager - Requirements & Stories</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-sm">System Architect - Technical Design</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                <span className="text-sm">Lead Developer - Implementation Planning</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                <span className="text-sm">QA Engineer - Testing Strategy</span>
              </div>
            </div>

            <button
              onClick={handlePlanProject}
              disabled={isPlanning}
              className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed font-medium"
            >
              {isPlanning ? "Planning in Progress..." : "Start AI Project Planning"}
            </button>
          </div>

          {/* Planning Progress */}
          {isPlanning && (
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-4">Planning Progress</h3>
              <div className="space-y-3">
                {[
                  "Product Manager analyzing requirements...",
                  "System Architect designing architecture...",
                  "Lead Developer planning implementation...",
                  "QA Engineer developing testing strategy...",
                  "Cross-team risk assessment...",
                  "Final plan synthesis..."
                ].map((step, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                    <span className="text-blue-800 text-sm">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Results Display */}
        <div className="space-y-6">
          {Object.keys(project).length > 0 && (
            <>
              {/* Project Overview */}
              {project.final_plan && (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-semibold mb-4">Project Plan Overview</h2>
                  <div className="space-y-3">
                    <div>
                      <span className="font-medium text-gray-700">Timeline:</span>
                      <span className="ml-2 text-gray-900">{project.final_plan.timeline_weeks} weeks</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Team Size:</span>
                      <span className="ml-2 text-gray-900">{project.final_plan.team_size} developers</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Complexity:</span>
                      <span className="ml-2 text-gray-900">{project.final_plan.complexity_level}/10</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Risk Level:</span>
                      <span className="ml-2 text-gray-900">{project.final_plan.risk_assessment}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Technical Architecture */}
              {project.technical_design && (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-semibold mb-3">Technical Architecture</h3>
                  <div className="space-y-2 text-sm">
                    <div><strong>Frontend:</strong> {project.technical_design.frontend}</div>
                    <div><strong>Backend:</strong> {project.technical_design.backend}</div>
                    <div><strong>Database:</strong> {project.technical_design.database}</div>
                    <div><strong>Deployment:</strong> {project.technical_design.deployment}</div>
                  </div>
                </div>
              )}

              {/* Implementation Tasks */}
              {project.implementation_plan && (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h3 className="text-lg font-semibold mb-3">Implementation Plan</h3>
                  <div className="space-y-2">
                    {project.implementation_plan.tasks?.slice(0, 5).map((task: any, index: number) => (
                      <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                        <span className="text-sm">{task.title}</span>
                        <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                          {task.estimated_hours}h
                        </span>
                      </div>
                    ))}
                    {project.implementation_plan.tasks?.length > 5 && (
                      <div className="text-sm text-gray-500 text-center pt-2">
                        +{project.implementation_plan.tasks.length - 5} more tasks
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Risks and Mitigations */}
              {project.risk_assessment && (
                <div className="bg-red-50 p-6 rounded-lg border border-red-200">
                  <h3 className="text-lg font-semibold text-red-900 mb-3">Risk Assessment</h3>
                  <div className="space-y-3">
                    {project.risk_assessment.identified_risks?.map((risk: any, index: number) => (
                      <div key={index} className="bg-white p-3 rounded border border-red-100">
                        <div className="flex justify-between items-start mb-2">
                          <span className="font-medium text-red-900">{risk.category} Risk</span>
                          <span className={`px-2 py-1 text-xs rounded ${
                            risk.level === 'High' ? 'bg-red-100 text-red-800' :
                            risk.level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {risk.level}
                          </span>
                        </div>
                        <p className="text-sm text-red-800 mb-2">{risk.description}</p>
                        <p className="text-sm text-red-700">
                          <strong>Mitigation:</strong> {risk.mitigation}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Empty State */}
          {Object.keys(project).length === 0 && !isPlanning && (
            <div className="bg-gray-50 p-12 rounded-lg border-2 border-dashed border-gray-300 text-center">
              <div className="text-6xl mb-4">🤖</div>
              <h3 className="text-xl font-medium text-gray-900 mb-2">AI Project Planning</h3>
              <p className="text-gray-600 mb-4">
                Click the button to see multiple AI agents collaborate on comprehensive project planning.
              </p>
              <div className="text-sm text-gray-500">
                Uses Product Manager, Architect, Developer, and QA Engineer agents
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

## Summary

In this chapter, we've covered:

- **CoAgents Fundamentals**: Basic agent workflows with nodes and edges
- **LangGraph Integration**: Complex agentic workflows with planning and execution
- **Multi-Agent Collaboration**: Different agents working together on complex tasks
- **Workflow Orchestration**: Coordinating multiple steps and conditional logic
- **Advanced Patterns**: Research workflows, project planning, and risk assessment

## Key Takeaways

1. **Agent Orchestration**: CoAgents coordinate multiple AI agents for complex tasks
2. **LangGraph Power**: Graph-based workflows enable sophisticated agent interactions
3. **Multi-Agent Systems**: Different agents with specialized roles and expertise
4. **Human-in-the-Loop**: Workflows can include approval steps and interventions
5. **Scalable Workflows**: Handle complex, multi-step processes with proper state management
6. **Error Recovery**: Built-in error handling and recovery mechanisms

## Next Steps

Now that you can build complex agentic workflows, let's explore human-in-the-loop interactions and approval workflows.

---

**Ready for Chapter 7?** [Human-in-the-Loop](07-human-in-loop.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*