---
layout: default
title: "CopilotKit Tutorial - Chapter 2: Reading App Context"
nav_order: 2
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 2: Reading App Context - Making Your App State Visible to AI

> Master useCopilotReadable to share application state, data, and context with your AI copilot for intelligent interactions.

## Overview

For AI to provide truly helpful assistance, it needs to understand your application's current state, data, and context. The `useCopilotReadable` hook makes your app's state visible to the copilot, enabling contextual and intelligent interactions.

## Basic Context Sharing

### Simple State Sharing

```tsx
// app/components/TodoList.tsx
"use client";

import { useState } from "react";
import { useCopilotReadable } from "@copilotkit/react-core";

interface Todo {
  id: number;
  text: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
}

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([
    { id: 1, text: "Buy groceries", completed: false, priority: "medium" },
    { id: 2, text: "Finish report", completed: true, priority: "high" },
    { id: 3, text: "Call dentist", completed: false, priority: "low" },
  ]);

  const [filter, setFilter] = useState<"all" | "active" | "completed">("all");

  // Share the current todos with the copilot
  useCopilotReadable({
    description: "The current list of todo items with their completion status and priority",
    value: todos,
  });

  // Share the current filter state
  useCopilotReadable({
    description: "The current filter applied to the todo list (all, active, or completed)",
    value: filter,
  });

  // Share computed values
  const activeTodos = todos.filter(todo => !todo.completed);
  const completedTodos = todos.filter(todo => todo.completed);

  useCopilotReadable({
    description: "Number of active (incomplete) todos",
    value: activeTodos.length,
  });

  useCopilotReadable({
    description: "Number of completed todos",
    value: completedTodos.length,
  });

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Todo List</h1>

      {/* Filter Controls */}
      <div className="mb-6 flex gap-2">
        {["all", "active", "completed"].map(filterOption => (
          <button
            key={filterOption}
            onClick={() => setFilter(filterOption as any)}
            className={`px-4 py-2 rounded ${
              filter === filterOption
                ? "bg-blue-500 text-white"
                : "bg-gray-200 text-gray-700"
            }`}
          >
            {filterOption.charAt(0).toUpperCase() + filterOption.slice(1)}
          </button>
        ))}
      </div>

      {/* Todo Items */}
      <div className="space-y-3">
        {todos
          .filter(todo => {
            if (filter === "active") return !todo.completed;
            if (filter === "completed") return todo.completed;
            return true;
          })
          .map(todo => (
            <div
              key={todo.id}
              className={`p-4 border rounded-lg ${
                todo.completed ? "bg-green-50 border-green-200" : "bg-white border-gray-200"
              }`}
            >
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => {
                    setTodos(prev =>
                      prev.map(t =>
                        t.id === todo.id ? { ...t, completed: !t.completed } : t
                      )
                    );
                  }}
                  className="w-5 h-5"
                />
                <span className={`flex-1 ${todo.completed ? "line-through text-gray-500" : ""}`}>
                  {todo.text}
                </span>
                <span className={`px-2 py-1 rounded text-sm ${
                  todo.priority === "high" ? "bg-red-100 text-red-800" :
                  todo.priority === "medium" ? "bg-yellow-100 text-yellow-800" :
                  "bg-green-100 text-green-800"
                }`}>
                  {todo.priority}
                </span>
              </div>
            </div>
          ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "How many active todos do I have?"</li>
          <li>• "Show me all high priority todos"</li>
          <li>• "What's my completion rate?"</li>
          <li>• "Which todos are marked as completed?"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Advanced Context Sharing

### Structured Data Context

```tsx
// app/components/ProjectDashboard.tsx
"use client";

import { useState, useEffect } from "react";
import { useCopilotReadable } from "@copilotkit/react-core";

interface Project {
  id: string;
  name: string;
  status: "planning" | "active" | "completed" | "on-hold";
  team: string[];
  deadline: Date;
  progress: number;
  tasks: Task[];
}

interface Task {
  id: string;
  title: string;
  assignee: string;
  status: "todo" | "in-progress" | "review" | "done";
  priority: "low" | "medium" | "high";
  estimatedHours: number;
  actualHours?: number;
}

export function ProjectDashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  // Share all projects
  useCopilotReadable({
    description: "Complete list of all projects with their current status, team members, deadlines, and progress",
    value: projects,
  });

  // Share selected project details
  useCopilotReadable({
    description: "Currently selected project with full details including all tasks",
    value: selectedProject,
  });

  // Share computed analytics
  const projectStats = {
    totalProjects: projects.length,
    activeProjects: projects.filter(p => p.status === "active").length,
    completedProjects: projects.filter(p => p.status === "completed").length,
    overdueProjects: projects.filter(p => p.deadline < new Date() && p.status !== "completed").length,
    totalTasks: projects.reduce((sum, p) => sum + p.tasks.length, 0),
    completedTasks: projects.reduce((sum, p) => sum + p.tasks.filter(t => t.status === "done").length, 0),
  };

  useCopilotReadable({
    description: "Project portfolio statistics and analytics",
    value: projectStats,
  });

  // Share team information
  const teamMembers = [...new Set(projects.flatMap(p => p.team))];
  useCopilotReadable({
    description: "All team members across all projects",
    value: teamMembers,
  });

  // Share upcoming deadlines
  const upcomingDeadlines = projects
    .filter(p => p.status !== "completed")
    .sort((a, b) => a.deadline.getTime() - b.deadline.getTime())
    .slice(0, 5);

  useCopilotReadable({
    description: "Next 5 upcoming project deadlines",
    value: upcomingDeadlines.map(p => ({
      name: p.name,
      deadline: p.deadline.toISOString(),
      daysUntilDeadline: Math.ceil((p.deadline.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
      status: p.status,
    })),
  });

  // Mock data loading
  useEffect(() => {
    const mockProjects: Project[] = [
      {
        id: "1",
        name: "E-commerce Platform",
        status: "active",
        team: ["Alice", "Bob", "Charlie"],
        deadline: new Date("2024-03-15"),
        progress: 75,
        tasks: [
          { id: "1", title: "Design product catalog", assignee: "Alice", status: "done", priority: "high", estimatedHours: 20, actualHours: 18 },
          { id: "2", title: "Implement payment system", assignee: "Bob", status: "in-progress", priority: "high", estimatedHours: 40, actualHours: 35 },
          { id: "3", title: "Add user authentication", assignee: "Charlie", status: "todo", priority: "medium", estimatedHours: 16 },
        ]
      },
      // More projects...
    ];
    setProjects(mockProjects);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Project Dashboard</h1>

      {/* Project Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{projectStats.totalProjects}</div>
          <div className="text-sm text-blue-800">Total Projects</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{projectStats.activeProjects}</div>
          <div className="text-sm text-green-800">Active</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">{projectStats.completedTasks}</div>
          <div className="text-sm text-purple-800">Tasks Done</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">{projectStats.overdueProjects}</div>
          <div className="text-sm text-orange-800">Overdue</div>
        </div>
      </div>

      {/* Projects List */}
      <div className="grid gap-4">
        {projects.map(project => (
          <div
            key={project.id}
            onClick={() => setSelectedProject(project)}
            className="p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{project.name}</h3>
              <span className={`px-2 py-1 rounded text-sm ${
                project.status === "active" ? "bg-green-100 text-green-800" :
                project.status === "completed" ? "bg-blue-100 text-blue-800" :
                project.status === "planning" ? "bg-yellow-100 text-yellow-800" :
                "bg-gray-100 text-gray-800"
              }`}>
                {project.status}
              </span>
            </div>
            <div className="text-sm text-gray-600 mb-2">
              Team: {project.team.join(", ")}
            </div>
            <div className="text-sm text-gray-600 mb-2">
              Deadline: {project.deadline.toLocaleDateString()}
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${project.progress}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">{project.progress}% complete</div>
          </div>
        ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Which projects are overdue?"</li>
          <li>• "Who is working on the most tasks?"</li>
          <li>• "What are the upcoming deadlines?"</li>
          <li>• "Show me the active projects"</li>
          <li>• "What's the overall completion rate?"</li>
        </ul>
      </div>
    </div>
  );
}
```

### Dynamic Context Updates

```tsx
// app/components/LiveDataDashboard.tsx
"use client";

import { useState, useEffect } from "react";
import { useCopilotReadable } from "@copilotkit/react-core";

interface SensorData {
  id: string;
  name: string;
  value: number;
  unit: string;
  status: "normal" | "warning" | "critical";
  lastUpdated: Date;
}

export function LiveDataDashboard() {
  const [sensors, setSensors] = useState<SensorData[]>([]);
  const [alerts, setAlerts] = useState<string[]>([]);

  // Share current sensor readings
  useCopilotReadable({
    description: "Current readings from all sensors with their status and last update time",
    value: sensors,
  });

  // Share active alerts
  useCopilotReadable({
    description: "Current active alerts and warnings from the sensor network",
    value: alerts,
  });

  // Share system health summary
  const systemHealth = {
    totalSensors: sensors.length,
    healthySensors: sensors.filter(s => s.status === "normal").length,
    warningSensors: sensors.filter(s => s.status === "warning").length,
    criticalSensors: sensors.filter(s => s.status === "critical").length,
    activeAlerts: alerts.length,
    lastUpdate: sensors.length > 0 ? Math.max(...sensors.map(s => s.lastUpdated.getTime())) : null,
  };

  useCopilotReadable({
    description: "Overall system health summary with sensor counts and alert status",
    value: systemHealth,
  });

  // Simulate live data updates
  useEffect(() => {
    const initialSensors: SensorData[] = [
      { id: "temp-1", name: "Server Room Temperature", value: 22.5, unit: "°C", status: "normal", lastUpdated: new Date() },
      { id: "cpu-1", name: "Main Server CPU", value: 45.2, unit: "%", status: "normal", lastUpdated: new Date() },
      { id: "mem-1", name: "Memory Usage", value: 78.3, unit: "%", status: "warning", lastUpdated: new Date() },
      { id: "disk-1", name: "Disk Usage", value: 92.1, unit: "%", status: "critical", lastUpdated: new Date() },
    ];

    setSensors(initialSensors);
    setAlerts(["High disk usage on main server", "Memory usage above threshold"]);

    // Simulate live updates
    const interval = setInterval(() => {
      setSensors(prev => prev.map(sensor => ({
        ...sensor,
        value: sensor.value + (Math.random() - 0.5) * 2, // Small random change
        lastUpdated: new Date(),
        status: sensor.value > 90 ? "critical" :
                sensor.value > 75 ? "warning" : "normal"
      })));

      // Update alerts based on sensor values
      setAlerts(prev => {
        const newAlerts = [];
        const criticalSensors = sensors.filter(s => s.status === "critical");
        if (criticalSensors.length > 0) {
          newAlerts.push(`${criticalSensors.length} sensors in critical state`);
        }
        return newAlerts;
      });
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Live Sensor Dashboard</h1>

      {/* System Health Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{systemHealth.healthySensors}</div>
          <div className="text-sm text-green-800">Healthy</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-yellow-600">{systemHealth.warningSensors}</div>
          <div className="text-sm text-yellow-800">Warning</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-red-600">{systemHealth.criticalSensors}</div>
          <div className="text-sm text-red-800">Critical</div>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{systemHealth.activeAlerts}</div>
          <div className="text-sm text-blue-800">Active Alerts</div>
        </div>
      </div>

      {/* Active Alerts */}
      {alerts.length > 0 && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-semibold text-red-900 mb-2">Active Alerts</h3>
          <ul className="text-sm text-red-800 space-y-1">
            {alerts.map((alert, index) => (
              <li key={index}>• {alert}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Sensor Readings */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {sensors.map(sensor => (
          <div key={sensor.id} className="p-4 border rounded-lg">
            <h3 className="font-semibold mb-2">{sensor.name}</h3>
            <div className="text-2xl font-bold mb-1">
              {sensor.value.toFixed(1)} {sensor.unit}
            </div>
            <div className={`text-sm px-2 py-1 rounded inline-block ${
              sensor.status === "normal" ? "bg-green-100 text-green-800" :
              sensor.status === "warning" ? "bg-yellow-100 text-yellow-800" :
              "bg-red-100 text-red-800"
            }`}>
              {sensor.status}
            </div>
            <div className="text-xs text-gray-500 mt-2">
              Updated: {sensor.lastUpdated.toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Which sensors are in critical status?"</li>
          <li>• "What are the current active alerts?"</li>
          <li>• "Show me sensors with values above 80"</li>
          <li>• "What's the overall system health?"</li>
          <li>• "When was the last sensor update?"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Context Hierarchies

### Nested Context Sharing

```tsx
// app/components/OrganizationDashboard.tsx
"use client";

import { useCopilotReadable } from "@copilotkit/react-core";
import { DepartmentView } from "./DepartmentView";

interface Organization {
  name: string;
  departments: Department[];
}

interface Department {
  name: string;
  manager: string;
  employees: Employee[];
  projects: Project[];
  budget: number;
}

interface Employee {
  id: string;
  name: string;
  role: string;
  department: string;
  skills: string[];
}

interface Project {
  id: string;
  name: string;
  status: "planning" | "active" | "completed";
  team: string[];
  budget: number;
  deadline: Date;
}

export function OrganizationDashboard() {
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [selectedDepartment, setSelectedDepartment] = useState<Department | null>(null);

  // Share organization overview
  useCopilotReadable({
    description: "High-level organization information including all departments and key metrics",
    value: organization ? {
      name: organization.name,
      departmentCount: organization.departments.length,
      totalEmployees: organization.departments.reduce((sum, dept) => sum + dept.employees.length, 0),
      activeProjects: organization.departments.reduce((sum, dept) => sum + dept.projects.filter(p => p.status === "active").length, 0),
      totalBudget: organization.departments.reduce((sum, dept) => sum + dept.budget, 0),
    } : null,
  });

  // Share detailed department information
  useCopilotReadable({
    description: "Detailed information about all departments including managers, employees, projects, and budgets",
    value: organization?.departments.map(dept => ({
      name: dept.name,
      manager: dept.manager,
      employeeCount: dept.employees.length,
      activeProjects: dept.projects.filter(p => p.status === "active").length,
      budget: dept.budget,
      skills: [...new Set(dept.employees.flatMap(emp => emp.skills))],
    })) || [],
  });

  // Share selected department details
  useCopilotReadable({
    description: "Currently selected department with full employee and project details",
    value: selectedDepartment,
  });

  // Share project portfolio
  const allProjects = organization?.departments.flatMap(dept => dept.projects) || [];
  useCopilotReadable({
    description: "Complete project portfolio across all departments",
    value: allProjects.map(project => ({
      ...project,
      department: organization?.departments.find(dept =>
        dept.projects.some(p => p.id === project.id)
      )?.name,
    })),
  });

  // Share employee directory
  const allEmployees = organization?.departments.flatMap(dept => dept.employees) || [];
  useCopilotReadable({
    description: "Complete employee directory with roles, departments, and skills",
    value: allEmployees,
  });

  // Share budget analytics
  const budgetAnalytics = organization ? {
    totalBudget: organization.departments.reduce((sum, dept) => sum + dept.budget, 0),
    departmentBudgets: organization.departments.map(dept => ({
      department: dept.name,
      budget: dept.budget,
      percentage: (dept.budget / organization.departments.reduce((sum, d) => sum + d.budget, 0)) * 100,
    })),
    projectBudgets: allProjects.reduce((sum, project) => sum + project.budget, 0),
    avgProjectBudget: allProjects.length > 0 ? allProjects.reduce((sum, p) => sum + p.budget, 0) / allProjects.length : 0,
  } : null;

  useCopilotReadable({
    description: "Budget analytics and financial overview of the organization",
    value: budgetAnalytics,
  });

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Organization Dashboard</h1>

      {organization && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Organization Overview */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Overview</h2>
            <div className="space-y-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{organization.departments.length}</div>
                <div className="text-sm text-blue-800">Departments</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {organization.departments.reduce((sum, dept) => sum + dept.employees.length, 0)}
                </div>
                <div className="text-sm text-green-800">Employees</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {organization.departments.reduce((sum, dept) => sum + dept.projects.filter(p => p.status === "active").length, 0)}
                </div>
                <div className="text-sm text-purple-800">Active Projects</div>
              </div>
            </div>
          </div>

          {/* Departments List */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Departments</h2>
            <div className="space-y-3">
              {organization.departments.map(dept => (
                <div
                  key={dept.name}
                  onClick={() => setSelectedDepartment(dept)}
                  className="p-4 border rounded-lg cursor-pointer hover:bg-gray-50"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium">{dept.name}</h3>
                    <span className="text-sm text-gray-500">{dept.manager}</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    {dept.employees.length} employees • {dept.projects.filter(p => p.status === "active").length} active projects
                  </div>
                  <div className="text-sm text-gray-600">
                    Budget: ${dept.budget.toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Department Details */}
      {selectedDepartment && (
        <DepartmentView department={selectedDepartment} />
      )}

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Which department has the most employees?"</li>
          <li>• "Show me all active projects across the organization"</li>
          <li>• "What's the total budget allocation?"</li>
          <li>• "Who are the project managers in the engineering department?"</li>
          <li>• "Find employees with React skills"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Context Optimization

### Selective Context Sharing

```tsx
// app/hooks/useOptimizedCopilotReadable.ts
import { useCopilotReadable } from "@copilotkit/react-core";
import { useMemo } from "react";

export function useOptimizedCopilotReadable(data: any, description: string, enabled: boolean = true) {
  // Only share context if enabled and data exists
  const optimizedData = useMemo(() => {
    if (!enabled || !data) return null;

    // For large datasets, provide summary instead of full data
    if (Array.isArray(data) && data.length > 100) {
      return {
        summary: `${data.length} items`,
        sample: data.slice(0, 5),
        type: 'large-dataset'
      };
    }

    // For complex objects, provide structured summary
    if (typeof data === 'object' && data !== null) {
      const keys = Object.keys(data);
      if (keys.length > 10) {
        return {
          summary: `${keys.length} properties`,
          mainKeys: keys.slice(0, 5),
          type: 'complex-object'
        };
      }
    }

    return data;
  }, [data, enabled]);

  useCopilotReadable({
    description,
    value: optimizedData,
  });

  return optimizedData;
}
```

### Context Versioning

```tsx
// app/hooks/useVersionedCopilotReadable.ts
import { useCopilotReadable } from "@copilotkit/react-core";
import { useRef, useEffect } from "react";

export function useVersionedCopilotReadable(data: any, description: string) {
  const versionRef = useRef(0);
  const previousDataRef = useRef<any>(null);

  // Only update context if data actually changed
  useEffect(() => {
    if (JSON.stringify(previousDataRef.current) !== JSON.stringify(data)) {
      versionRef.current += 1;
      previousDataRef.current = data;
    }
  }, [data]);

  useCopilotReadable({
    description: `${description} (version ${versionRef.current})`,
    value: data,
  });

  return versionRef.current;
}
```

## Summary

In this chapter, we've covered:

- **Basic Context Sharing**: Making app state visible to AI with useCopilotReadable
- **Advanced Context**: Sharing computed values, analytics, and structured data
- **Dynamic Updates**: Real-time context updates as app state changes
- **Context Hierarchies**: Sharing data at different levels of granularity
- **Nested Components**: Context sharing across component trees
- **Optimization Techniques**: Selective sharing and versioned updates

## Key Takeaways

1. **Context is Key**: AI needs to understand your app state to provide relevant assistance
2. **Structured Data**: Share data in formats that AI can easily understand and analyze
3. **Computed Values**: Share derived analytics and summaries, not just raw data
4. **Dynamic Updates**: Context should update as your app state changes
5. **Performance Matters**: Optimize context sharing for large datasets
6. **Versioning**: Use versioning to track context changes and avoid confusion

## Next Steps

Now that the AI can see your app context, let's explore how to enable AI to take actions in your app using copilot actions.

---

**Ready for Chapter 3?** [Copilot Actions](03-copilot-actions.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*