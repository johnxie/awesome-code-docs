---
layout: default
title: "CopilotKit Tutorial - Chapter 5: Generative UI"
nav_order: 5
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 5: Generative UI - AI-Generated React Components

> Enable AI to generate and modify React components dynamically through natural language conversations.

## Overview

Generative UI is a powerful CopilotKit feature that allows AI to create, modify, and enhance React components through natural language. This chapter covers implementing generative UI capabilities and building dynamic interfaces.

## Basic Generative UI Setup

### Enabling Generative UI

```tsx
// app/layout.tsx
import { CopilotKit } from "@copilotkit/react-core";

export default function RootLayout({ children }) {
  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      experimental={{
        generativeUI: true,  // Enable generative UI
      }}
    >
      {children}
    </CopilotKit>
  );
}
```

### Simple Generative Component

```tsx
// app/components/GenerativeDashboard.tsx
"use client";

import { useCopilotGenerativeUI } from "@copilotkit/react-core";
import { useState } from "react";

export function GenerativeDashboard() {
  const [data, setData] = useState([
    { name: "Sales", value: 1200, change: 12 },
    { name: "Users", value: 450, change: -3 },
    { name: "Revenue", value: 8900, change: 8 },
  ]);

  // Share data for generative UI
  useCopilotReadable({
    description: "Dashboard data including metrics and KPIs",
    value: data,
  });

  // Enable generative UI for this component
  const generativeUI = useCopilotGenerativeUI({
    description: "Generate dashboard components based on the data",
    initialState: {
      showCharts: true,
      theme: "light",
      layout: "grid",
    },
  });

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Generative Dashboard</h1>

      {/* Static content */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Current Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.map((item, index) => (
            <div key={index} className="bg-white p-4 rounded-lg shadow">
              <h3 className="font-semibold text-gray-900">{item.name}</h3>
              <p className="text-2xl font-bold text-blue-600">{item.value.toLocaleString()}</p>
              <p className={`text-sm ${item.change >= 0 ? "text-green-600" : "text-red-600"}`}>
                {item.change >= 0 ? "+" : ""}{item.change}%
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Generative UI area */}
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <h2 className="text-xl font-semibold mb-4">AI-Generated Components</h2>
        <p className="text-gray-600 mb-4">
          Ask the AI to generate charts, tables, or other components based on the data above.
        </p>

        {generativeUI ? (
          <div className="bg-white rounded-lg shadow-sm">
            {generativeUI}
          </div>
        ) : (
          <div className="text-gray-500">
            <p>No generative components yet.</p>
            <p className="text-sm mt-2">Try asking: "Generate a chart showing the data trends"</p>
          </div>
        )}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Generate a bar chart showing the metrics"</li>
          <li>• "Create a table with the data and add sorting"</li>
          <li>• "Add a line chart showing trends over time"</li>
          <li>• "Generate a summary card with key insights"</li>
          <li>• "Create a pie chart for the revenue breakdown"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Advanced Generative UI Patterns

### Dynamic Component Generation

```tsx
// app/components/DynamicFormBuilder.tsx
"use client";

import { useCopilotGenerativeUI, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

interface FormField {
  name: string;
  type: "text" | "email" | "number" | "select" | "checkbox";
  label: string;
  required: boolean;
  options?: string[];
}

interface FormConfig {
  title: string;
  fields: FormField[];
  submitAction: string;
}

export function DynamicFormBuilder() {
  const [forms, setForms] = useState<FormConfig[]>([]);
  const [selectedForm, setSelectedForm] = useState<FormConfig | null>(null);

  // Share forms data
  useCopilotReadable({
    description: "Available form configurations",
    value: forms,
  });

  // Action to create new form
  useCopilotAction({
    name: "createForm",
    description: "Create a new form configuration",
    parameters: [
      {
        name: "title",
        type: "string",
        description: "Form title",
        required: true,
      },
      {
        name: "fields",
        type: "string",
        description: "JSON description of form fields",
        required: true,
      },
    ],
    handler: async ({ title, fields }) => {
      try {
        const parsedFields = JSON.parse(fields);
        const formConfig: FormConfig = {
          title,
          fields: parsedFields,
          submitAction: "submitForm",
        };

        setForms(prev => [...prev, formConfig]);
        setSelectedForm(formConfig);

        return { success: true, form: formConfig };
      } catch (error) {
        throw new Error("Invalid JSON format for fields");
      }
    },
  });

  // Generative UI for form rendering
  const generativeForm = useCopilotGenerativeUI({
    description: "Generate a React form component based on the form configuration",
    initialState: selectedForm,
    dependencies: [selectedForm], // Regenerate when form changes
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Dynamic Form Builder</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form List */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Available Forms</h2>

          <div className="space-y-3 mb-6">
            {forms.map((form, index) => (
              <div
                key={index}
                onClick={() => setSelectedForm(form)}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  selectedForm === form
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:bg-gray-50"
                }`}
              >
                <h3 className="font-medium">{form.title}</h3>
                <p className="text-sm text-gray-600">
                  {form.fields.length} fields
                </p>
              </div>
            ))}

            {forms.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p>No forms created yet.</p>
                <p className="text-sm mt-2">Ask the copilot to create a form!</p>
              </div>
            )}
          </div>

          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2">Try creating forms:</h3>
            <ul className="text-sm text-green-800 space-y-1">
              <li>• "Create a contact form with name, email, and message fields"</li>
              <li>• "Make a survey form with rating scales and checkboxes"</li>
              <li>• "Build a registration form with validation"</li>
            </ul>
          </div>
        </div>

        {/* Generated Form */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Generated Form</h2>

          {selectedForm ? (
            <div className="space-y-4">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold mb-2">{selectedForm.title}</h3>
                <div className="text-sm text-gray-600 mb-4">
                  Fields: {selectedForm.fields.map(f => f.label).join(", ")}
                </div>
              </div>

              {generativeForm ? (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h4 className="font-medium mb-4">AI-Generated Form:</h4>
                  {generativeForm}
                </div>
              ) : (
                <div className="bg-gray-50 p-6 rounded-lg border-2 border-dashed border-gray-300">
                  <p className="text-gray-600 text-center">
                    Ask the copilot to generate a form component for "{selectedForm.title}"
                  </p>
                  <p className="text-sm text-gray-500 text-center mt-2">
                    Try: "Generate a React form component for this form configuration"
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-gray-50 p-8 rounded-lg border-2 border-dashed border-gray-300 text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Form</h3>
              <p className="text-gray-600">
                Choose a form from the list to see its AI-generated component.
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Advanced generative UI commands:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Generate a beautiful form with validation and error handling"</li>
          <li>• "Create a form with a modern design and animations"</li>
          <li>• "Add form persistence and draft saving"</li>
          <li>• "Generate a multi-step form with progress indicators"</li>
        </ul>
      </div>
    </div>
  );
}
```

### Generative UI with Data Visualization

```tsx
// app/components/DataVisualizer.tsx
"use client";

import { useCopilotGenerativeUI, useCopilotReadable } from "@copilotkit/react-core";
import { useState, useEffect } from "react";

interface DataPoint {
  label: string;
  value: number;
  category: string;
  timestamp: Date;
}

export function DataVisualizer() {
  const [data, setData] = useState<DataPoint[]>([]);
  const [selectedMetric, setSelectedMetric] = useState<string>("all");

  // Generate sample data
  useEffect(() => {
    const sampleData: DataPoint[] = [
      { label: "Page Views", value: 12500, category: "traffic", timestamp: new Date() },
      { label: "Unique Visitors", value: 3200, category: "traffic", timestamp: new Date() },
      { label: "Bounce Rate", value: 34.5, category: "engagement", timestamp: new Date() },
      { label: "Conversion Rate", value: 3.2, category: "conversion", timestamp: new Date() },
      { label: "Avg Session", value: 245, category: "engagement", timestamp: new Date() },
      { label: "Revenue", value: 15600, category: "revenue", timestamp: new Date() },
    ];
    setData(sampleData);
  }, []);

  // Share data for generative UI
  useCopilotReadable({
    description: "Analytics and KPI data for visualization",
    value: data,
  });

  useCopilotReadable({
    description: "Currently selected metric filter",
    value: selectedMetric,
  });

  // Generative UI for data visualization
  const generativeVisualization = useCopilotGenerativeUI({
    description: "Generate data visualization components (charts, graphs, dashboards) based on the analytics data",
    initialState: {
      data: data,
      filter: selectedMetric,
      chartType: "auto", // Let AI choose best visualization
    },
    dependencies: [data, selectedMetric],
  });

  const filteredData = selectedMetric === "all"
    ? data
    : data.filter(item => item.category === selectedMetric);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">AI Data Visualizer</h1>

      {/* Controls */}
      <div className="mb-6 flex gap-4">
        <select
          value={selectedMetric}
          onChange={(e) => setSelectedMetric(e.target.value)}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="all">All Metrics</option>
          <option value="traffic">Traffic</option>
          <option value="engagement">Engagement</option>
          <option value="conversion">Conversion</option>
          <option value="revenue">Revenue</option>
        </select>

        <div className="text-sm text-gray-600 py-2">
          Showing {filteredData.length} of {data.length} metrics
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-lg shadow mb-6 overflow-hidden">
        <div className="px-6 py-4 border-b">
          <h2 className="text-xl font-semibold">Raw Data</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Metric
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Value
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredData.map((item, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.label}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {typeof item.value === 'number' && item.value > 100
                      ? item.value.toLocaleString()
                      : item.value
                    }
                    {item.category === 'revenue' && '$'}
                    {item.category === 'engagement' && item.label.includes('Rate') && '%'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      item.category === 'traffic' ? 'bg-blue-100 text-blue-800' :
                      item.category === 'engagement' ? 'bg-green-100 text-green-800' :
                      item.category === 'conversion' ? 'bg-purple-100 text-purple-800' :
                      'bg-orange-100 text-orange-800'
                    }`}>
                      {item.category}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Generative Visualization */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">AI-Generated Visualizations</h2>

        {generativeVisualization ? (
          <div className="space-y-6">
            {generativeVisualization}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-lg font-medium mb-2">Ready for Visualization</h3>
            <p>Ask the AI to generate charts and graphs based on the data above.</p>
          </div>
        )}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking for visualizations:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Generate a bar chart comparing all metrics"</li>
          <li>• "Create a pie chart showing category distribution"</li>
          <li>• "Make a line chart for the traffic metrics over time"</li>
          <li>• "Build a dashboard with multiple chart types"</li>
          <li>• "Create a gauge chart for the conversion rate"</li>
          <li>• "Generate a heatmap for correlation between metrics"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Interactive Generative Components

### Dynamic Component Modification

```tsx
// app/components/InteractiveGenerator.tsx
"use client";

import { useCopilotGenerativeUI, useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

interface ComponentSpec {
  type: "button" | "input" | "card" | "table" | "chart";
  properties: Record<string, any>;
  style?: Record<string, any>;
}

export function InteractiveGenerator() {
  const [components, setComponents] = useState<ComponentSpec[]>([]);
  const [selectedComponent, setSelectedComponent] = useState<ComponentSpec | null>(null);

  // Action to add component
  useCopilotAction({
    name: "addComponent",
    description: "Add a new UI component to the collection",
    parameters: [
      {
        name: "type",
        type: "string",
        description: "Component type",
        enum: ["button", "input", "card", "table", "chart"],
        required: true,
      },
      {
        name: "description",
        type: "string",
        description: "What the component should do or display",
        required: true,
      },
    ],
    handler: async ({ type, description }) => {
      const component: ComponentSpec = {
        type: type as ComponentSpec["type"],
        properties: { description },
        style: {},
      };

      setComponents(prev => [...prev, component]);
      setSelectedComponent(component);

      return { success: true, component };
    },
  });

  // Action to modify component
  useCopilotAction({
    name: "modifyComponent",
    description: "Modify an existing component's properties or style",
    parameters: [
      {
        name: "componentIndex",
        type: "number",
        description: "Index of the component to modify (0-based)",
        required: true,
      },
      {
        name: "modifications",
        type: "string",
        description: "JSON description of modifications to apply",
        required: true,
      },
    ],
    handler: async ({ componentIndex, modifications }) => {
      if (componentIndex < 0 || componentIndex >= components.length) {
        throw new Error("Invalid component index");
      }

      try {
        const parsedMods = JSON.parse(modifications);

        setComponents(prev => {
          const newComponents = [...prev];
          newComponents[componentIndex] = {
            ...newComponents[componentIndex],
            ...parsedMods,
          };
          return newComponents;
        });

        setSelectedComponent(components[componentIndex]);

        return { success: true, modifiedComponent: components[componentIndex] };
      } catch (error) {
        throw new Error("Invalid JSON format for modifications");
      }
    },
  });

  // Generative UI for component rendering
  const generativeComponent = useCopilotGenerativeUI({
    description: "Generate a React component based on the component specification",
    initialState: selectedComponent,
    dependencies: [selectedComponent],
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Interactive Component Generator</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Component Library */}
        <div className="lg:col-span-1">
          <h2 className="text-xl font-semibold mb-4">Component Library</h2>

          <div className="space-y-3 mb-6">
            {components.map((component, index) => (
              <div
                key={index}
                onClick={() => setSelectedComponent(component)}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  selectedComponent === component
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium capitalize">{component.type}</h3>
                  <span className="text-xs text-gray-500">#{index}</span>
                </div>
                <p className="text-sm text-gray-600">
                  {component.properties.description || "No description"}
                </p>
                {Object.keys(component.style || {}).length > 0 && (
                  <div className="mt-2 text-xs text-gray-500">
                    Styled component
                  </div>
                )}
              </div>
            ))}

            {components.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                <p>No components yet.</p>
                <p className="text-sm mt-2">Ask the copilot to add components!</p>
              </div>
            )}
          </div>

          <div className="p-4 bg-green-50 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2">Try adding components:</h3>
            <ul className="text-sm text-green-800 space-y-1">
              <li>• "Add a submit button"</li>
              <li>• "Create a search input field"</li>
              <li>• "Add a data display card"</li>
              <li>• "Create a sortable table"</li>
              <li>• "Add a metrics chart"</li>
            </ul>
          </div>
        </div>

        {/* Generated Component */}
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Generated Component</h2>

          {selectedComponent ? (
            <div className="space-y-6">
              {/* Component Info */}
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-semibold mb-2">
                  {selectedComponent.type.charAt(0).toUpperCase() + selectedComponent.type.slice(1)} Component
                </h3>
                <div className="text-sm text-gray-600">
                  <p><strong>Description:</strong> {selectedComponent.properties.description}</p>
                  {selectedComponent.style && Object.keys(selectedComponent.style).length > 0 && (
                    <p><strong>Custom Styling:</strong> {Object.keys(selectedComponent.style).join(", ")}</p>
                  )}
                </div>
              </div>

              {/* Generated Component */}
              {generativeComponent ? (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h4 className="font-medium mb-4">AI-Generated Component:</h4>
                  <div className="border rounded-lg p-4 bg-gray-50">
                    {generativeComponent}
                  </div>
                </div>
              ) : (
                <div className="bg-gray-50 p-8 rounded-lg border-2 border-dashed border-gray-300 text-center">
                  <h4 className="font-medium mb-2">Ready for Generation</h4>
                  <p className="text-gray-600 mb-4">
                    Ask the AI to generate a React component for this {selectedComponent.type}.
                  </p>
                  <div className="text-sm text-gray-500">
                    Try: "Generate a beautiful React component for this {selectedComponent.type}"
                  </div>
                </div>
              )}

              {/* Modification Options */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Modify Component:</h4>
                <ul className="text-sm text-blue-800 space-y-1">
                  <li>• "Make it larger and add hover effects"</li>
                  <li>• "Add validation and error states"</li>
                  <li>• "Change the color scheme to dark mode"</li>
                  <li>• "Add animations and transitions"</li>
                  <li>• "Make it responsive for mobile"</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="bg-gray-50 p-12 rounded-lg border-2 border-dashed border-gray-300 text-center">
              <div className="text-6xl mb-4">🎨</div>
              <h3 className="text-xl font-medium text-gray-900 mb-2">Select a Component</h3>
              <p className="text-gray-600">
                Choose a component from the library to see its AI-generated implementation.
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="mt-8 p-4 bg-purple-50 rounded-lg">
        <h3 className="font-semibold text-purple-900 mb-2">Advanced generative commands:</h3>
        <ul className="text-sm text-purple-800 space-y-1">
          <li>• "Generate a complete form with validation, error handling, and submission"</li>
          <li>• "Create a data table with sorting, filtering, and pagination"</li>
          <li>• "Build a dashboard with multiple charts and real-time updates"</li>
          <li>• "Design a navigation component with dropdown menus and routing"</li>
          <li>• "Create a modal dialog system with different variants"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Summary

In this chapter, we've covered:

- **Basic Generative UI**: Enabling AI component generation in CopilotKit
- **Dynamic Components**: Creating forms and interfaces through conversation
- **Data Visualization**: AI-generated charts and graphs from data
- **Interactive Generation**: Modifying and enhancing generated components
- **Advanced Patterns**: Complex component generation and customization

## Key Takeaways

1. **Conversational Development**: Build UI components through natural language
2. **Dynamic Generation**: Components adapt based on data and requirements
3. **Iterative Refinement**: Modify and improve generated components
4. **Integration**: Generated components work seamlessly with existing code
5. **Customization**: Control styling, behavior, and functionality
6. **Rapid Prototyping**: Quickly create and test UI concepts

## Next Steps

Now that you can generate UI components, let's explore CoAgents and LangGraph integration for complex agentic workflows.

---

**Ready for Chapter 6?** [CoAgents & LangGraph](06-coagents.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*