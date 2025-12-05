---
layout: default
title: "CopilotKit Tutorial - Chapter 3: Copilot Actions"
nav_order: 3
has_children: false
parent: CopilotKit Tutorial
---

# Chapter 3: Copilot Actions - Enabling AI to Take Actions in Your App

> Master useCopilotAction to allow AI to perform operations, modify state, and interact with your application's backend.

## Overview

Copilot actions enable AI to actively modify your application's state, perform operations, and interact with external systems. The `useCopilotAction` hook defines actions that the AI can call with parameters.

## Basic Action Creation

### Simple State Modification

```tsx
// app/components/ActionTodoList.tsx
"use client";

import { useState } from "react";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

interface Todo {
  id: string;
  text: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
}

export function ActionTodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);

  // Share current state
  useCopilotReadable({
    description: "Current todo list with completion status and priorities",
    value: todos,
  });

  // Action to add a new todo
  useCopilotAction({
    name: "addTodo",
    description: "Add a new todo item to the list",
    parameters: [
      {
        name: "text",
        type: "string",
        description: "The text content of the todo item",
        required: true,
      },
      {
        name: "priority",
        type: "string",
        description: "Priority level (low, medium, high)",
        enum: ["low", "medium", "high"],
        default: "medium",
      },
    ],
    handler: async ({ text, priority = "medium" }: { text: string; priority?: string }) => {
      const newTodo: Todo = {
        id: Date.now().toString(),
        text: text.trim(),
        completed: false,
        priority: priority as "low" | "medium" | "high",
      };

      setTodos(prev => [...prev, newTodo]);
      return { success: true, todo: newTodo };
    },
  });

  // Action to toggle completion
  useCopilotAction({
    name: "toggleTodo",
    description: "Mark a todo item as completed or incomplete",
    parameters: [
      {
        name: "id",
        type: "string",
        description: "The ID of the todo item to toggle",
        required: true,
      },
    ],
    handler: async ({ id }: { id: string }) => {
      setTodos(prev =>
        prev.map(todo =>
          todo.id === id ? { ...todo, completed: !todo.completed } : todo
        )
      );
      return { success: true };
    },
  });

  // Action to delete a todo
  useCopilotAction({
    name: "deleteTodo",
    description: "Remove a todo item from the list",
    parameters: [
      {
        name: "id",
        type: "string",
        description: "The ID of the todo item to delete",
        required: true,
      },
    ],
    handler: async ({ id }: { id: string }) => {
      setTodos(prev => prev.filter(todo => todo.id !== id));
      return { success: true };
    },
  });

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">AI-Powered Todo List</h1>

      <div className="space-y-4 mb-6">
        {todos.map(todo => (
          <div
            key={todo.id}
            className={`p-4 border rounded-lg flex items-center gap-3 ${
              todo.completed ? "bg-green-50 border-green-200" : "bg-white border-gray-200"
            }`}
          >
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
        ))}

        {todos.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>No todos yet. Ask the copilot to add some!</p>
          </div>
        )}
      </div>

      <div className="p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Add a todo to finish the project report with high priority"</li>
          <li>• "Mark the first todo as completed"</li>
          <li>• "Delete the todo about buying groceries"</li>
          <li>• "Add three new todos for work tasks"</li>
          <li>• "Show me only the high priority incomplete todos"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Complex Actions with Validation

### Form Data Handling

```tsx
// app/components/ContactManager.tsx
"use client";

import { useState } from "react";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

interface Contact {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  tags: string[];
  notes: string;
  lastContacted: Date | null;
}

export function ContactManager() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [errors, setErrors] = useState<string[]>([]);

  // Share contacts data
  useCopilotReadable({
    description: "List of all contacts with their information and interaction history",
    value: contacts,
  });

  // Share validation errors
  useCopilotReadable({
    description: "Current validation errors or issues",
    value: errors,
  });

  // Action to add a new contact with validation
  useCopilotAction({
    name: "addContact",
    description: "Add a new contact to the address book with validation",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "Full name of the contact",
        required: true,
      },
      {
        name: "email",
        type: "string",
        description: "Email address (must be valid format)",
        required: true,
      },
      {
        name: "phone",
        type: "string",
        description: "Phone number (optional)",
      },
      {
        name: "company",
        type: "string",
        description: "Company or organization name",
      },
      {
        name: "tags",
        type: "string[]",
        description: "Tags for categorizing the contact (e.g., client, vendor, friend)",
      },
      {
        name: "notes",
        type: "string",
        description: "Additional notes about the contact",
      },
    ],
    handler: async (params: {
      name: string;
      email: string;
      phone?: string;
      company?: string;
      tags?: string[];
      notes?: string;
    }) => {
      const newErrors: string[] = [];

      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(params.email)) {
        newErrors.push("Invalid email format");
      }

      // Check for duplicate email
      const existingContact = contacts.find(c => c.email.toLowerCase() === params.email.toLowerCase());
      if (existingContact) {
        newErrors.push("A contact with this email already exists");
      }

      // Validate phone format (basic)
      if (params.phone && !/^[\+]?[\d\s\-\(\)]{10,}$/.test(params.phone)) {
        newErrors.push("Invalid phone number format");
      }

      if (newErrors.length > 0) {
        setErrors(newErrors);
        throw new Error(`Validation failed: ${newErrors.join(", ")}`);
      }

      const newContact: Contact = {
        id: Date.now().toString(),
        name: params.name.trim(),
        email: params.email.toLowerCase().trim(),
        phone: params.phone?.trim() || "",
        company: params.company?.trim() || "",
        tags: params.tags || [],
        notes: params.notes?.trim() || "",
        lastContacted: null,
      };

      setContacts(prev => [...prev, newContact]);
      setErrors([]);

      return {
        success: true,
        contact: newContact,
        message: `Contact ${params.name} added successfully`
      };
    },
  });

  // Action to search contacts
  useCopilotAction({
    name: "searchContacts",
    description: "Search contacts by name, email, company, or tags",
    parameters: [
      {
        name: "query",
        type: "string",
        description: "Search query (can match name, email, company, or tags)",
        required: true,
      },
    ],
    handler: async ({ query }: { query: string }) => {
      const searchTerm = query.toLowerCase();

      const results = contacts.filter(contact =>
        contact.name.toLowerCase().includes(searchTerm) ||
        contact.email.toLowerCase().includes(searchTerm) ||
        contact.company.toLowerCase().includes(searchTerm) ||
        contact.tags.some(tag => tag.toLowerCase().includes(searchTerm))
      );

      return {
        query,
        totalResults: results.length,
        results: results.map(contact => ({
          id: contact.id,
          name: contact.name,
          email: contact.email,
          company: contact.company,
          tags: contact.tags,
        })),
      };
    },
  });

  // Action to update contact information
  useCopilotAction({
    name: "updateContact",
    description: "Update an existing contact's information",
    parameters: [
      {
        name: "contactId",
        type: "string",
        description: "ID of the contact to update",
        required: true,
      },
      {
        name: "updates",
        type: "object",
        description: "Fields to update (name, email, phone, company, tags, notes)",
        required: true,
      },
    ],
    handler: async ({ contactId, updates }: { contactId: string; updates: Partial<Contact> }) => {
      const contactIndex = contacts.findIndex(c => c.id === contactId);

      if (contactIndex === -1) {
        throw new Error("Contact not found");
      }

      // Validate updates if they include email
      if (updates.email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(updates.email)) {
          throw new Error("Invalid email format");
        }

        // Check for duplicate email (excluding current contact)
        const duplicate = contacts.find(c =>
          c.id !== contactId && c.email.toLowerCase() === updates.email!.toLowerCase()
        );
        if (duplicate) {
          throw new Error("Another contact with this email already exists");
        }
      }

      const updatedContact = {
        ...contacts[contactIndex],
        ...updates,
        id: contactId, // Ensure ID doesn't change
      };

      setContacts(prev => {
        const newContacts = [...prev];
        newContacts[contactIndex] = updatedContact;
        return newContacts;
      });

      return {
        success: true,
        contact: updatedContact,
        message: "Contact updated successfully"
      };
    },
  });

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Contact Manager</h1>

      {/* Error Display */}
      {errors.length > 0 && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-semibold text-red-900 mb-2">Validation Errors:</h3>
          <ul className="text-sm text-red-800 space-y-1">
            {errors.map((error, index) => (
              <li key={index}>• {error}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Contacts List */}
      <div className="grid gap-4 mb-6">
        {contacts.map(contact => (
          <div key={contact.id} className="p-4 border rounded-lg">
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold">{contact.name}</h3>
              <div className="flex gap-2 flex-wrap">
                {contact.tags.map(tag => (
                  <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600">
              <div>📧 {contact.email}</div>
              {contact.phone && <div>📞 {contact.phone}</div>}
              {contact.company && <div>🏢 {contact.company}</div>}
              {contact.lastContacted && (
                <div>📅 Last contacted: {contact.lastContacted.toLocaleDateString()}</div>
              )}
            </div>

            {contact.notes && (
              <div className="mt-2 text-sm text-gray-700">
                <strong>Notes:</strong> {contact.notes}
              </div>
            )}
          </div>
        ))}

        {contacts.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <p>No contacts yet. Ask the copilot to add some!</p>
          </div>
        )}
      </div>

      <div className="p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Add a contact named John Doe with email john@example.com"</li>
          <li>• "Search for contacts who work at Google"</li>
          <li>• "Update John's phone number to 555-0123"</li>
          <li>• "Add tags 'client' and 'tech' to the John Doe contact"</li>
          <li>• "Find all contacts with the 'client' tag"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Asynchronous Actions

### API Integration Actions

```tsx
// app/components/APIManager.tsx
"use client";

import { useState } from "react";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

interface APIEndpoint {
  id: string;
  name: string;
  url: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  description: string;
  lastCalled?: Date;
  responseTime?: number;
  statusCode?: number;
}

export function APIManager() {
  const [endpoints, setEndpoints] = useState<APIEndpoint[]>([]);
  const [callHistory, setCallHistory] = useState<any[]>([]);

  // Share API endpoints
  useCopilotReadable({
    description: "List of configured API endpoints with their specifications",
    value: endpoints,
  });

  // Share call history
  useCopilotReadable({
    description: "History of API calls made through this interface",
    value: callHistory,
  });

  // Action to add API endpoint
  useCopilotAction({
    name: "addAPIEndpoint",
    description: "Add a new API endpoint to the collection",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "Descriptive name for the endpoint",
        required: true,
      },
      {
        name: "url",
        type: "string",
        description: "Full URL of the API endpoint",
        required: true,
      },
      {
        name: "method",
        type: "string",
        description: "HTTP method (GET, POST, PUT, DELETE)",
        enum: ["GET", "POST", "PUT", "DELETE"],
        default: "GET",
      },
      {
        name: "description",
        type: "string",
        description: "What this endpoint does",
      },
    ],
    handler: async ({ name, url, method = "GET", description = "" }) => {
      // Validate URL format
      try {
        new URL(url);
      } catch {
        throw new Error("Invalid URL format");
      }

      const newEndpoint: APIEndpoint = {
        id: Date.now().toString(),
        name: name.trim(),
        url: url.trim(),
        method: method as "GET" | "POST" | "PUT" | "DELETE",
        description: description.trim(),
      };

      setEndpoints(prev => [...prev, newEndpoint]);

      return {
        success: true,
        endpoint: newEndpoint,
        message: `API endpoint "${name}" added successfully`
      };
    },
  });

  // Action to call API endpoint
  useCopilotAction({
    name: "callAPIEndpoint",
    description: "Make an HTTP request to a configured API endpoint",
    parameters: [
      {
        name: "endpointId",
        type: "string",
        description: "ID of the endpoint to call",
        required: true,
      },
      {
        name: "data",
        type: "object",
        description: "Request body data for POST/PUT requests",
      },
      {
        name: "headers",
        type: "object",
        description: "Additional HTTP headers",
      },
    ],
    handler: async ({ endpointId, data = {}, headers = {} }) => {
      const endpoint = endpoints.find(e => e.id === endpointId);

      if (!endpoint) {
        throw new Error(`Endpoint with ID ${endpointId} not found`);
      }

      const startTime = Date.now();

      try {
        // Make the API call
        const response = await fetch(endpoint.url, {
          method: endpoint.method,
          headers: {
            "Content-Type": "application/json",
            ...headers,
          },
          body: ["POST", "PUT"].includes(endpoint.method) ? JSON.stringify(data) : undefined,
        });

        const responseTime = Date.now() - startTime;

        let responseData;
        const contentType = response.headers.get("content-type");

        if (contentType && contentType.includes("application/json")) {
          responseData = await response.json();
        } else {
          responseData = await response.text();
        }

        // Update endpoint with call results
        setEndpoints(prev =>
          prev.map(e =>
            e.id === endpointId
              ? { ...e, lastCalled: new Date(), responseTime, statusCode: response.status }
              : e
          )
        );

        // Add to call history
        const callRecord = {
          id: Date.now().toString(),
          endpointId,
          endpointName: endpoint.name,
          method: endpoint.method,
          url: endpoint.url,
          statusCode: response.status,
          responseTime,
          timestamp: new Date(),
          success: response.ok,
        };

        setCallHistory(prev => [callRecord, ...prev.slice(0, 49)]); // Keep last 50 calls

        return {
          success: response.ok,
          statusCode: response.status,
          responseTime,
          data: responseData,
          callRecord,
        };

      } catch (error) {
        const responseTime = Date.now() - startTime;

        // Record failed call
        const callRecord = {
          id: Date.now().toString(),
          endpointId,
          endpointName: endpoint.name,
          method: endpoint.method,
          url: endpoint.url,
          error: error.message,
          responseTime,
          timestamp: new Date(),
          success: false,
        };

        setCallHistory(prev => [callRecord, ...prev.slice(0, 49)]);

        throw new Error(`API call failed: ${error.message}`);
      }
    },
  });

  // Action to test all endpoints
  useCopilotAction({
    name: "testAllEndpoints",
    description: "Test all configured API endpoints and report results",
    parameters: [],
    handler: async () => {
      const results = [];

      for (const endpoint of endpoints) {
        try {
          const result = await fetch(endpoint.url, {
            method: endpoint.method,
            headers: { "Content-Type": "application/json" },
          });

          results.push({
            endpoint: endpoint.name,
            statusCode: result.status,
            success: result.ok,
            responseTime: 0, // Would need to measure this properly
          });
        } catch (error) {
          results.push({
            endpoint: endpoint.name,
            error: error.message,
            success: false,
          });
        }
      }

      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      return {
        totalEndpoints: totalCount,
        successfulTests: successCount,
        failedTests: totalCount - successCount,
        successRate: totalCount > 0 ? (successCount / totalCount) * 100 : 0,
        detailedResults: results,
      };
    },
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">API Manager</h1>

      {/* Endpoints List */}
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">API Endpoints</h2>
        <div className="grid gap-4">
          {endpoints.map(endpoint => (
            <div key={endpoint.id} className="p-4 border rounded-lg">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold">{endpoint.name}</h3>
                <span className={`px-2 py-1 rounded text-sm ${
                  endpoint.method === "GET" ? "bg-blue-100 text-blue-800" :
                  endpoint.method === "POST" ? "bg-green-100 text-green-800" :
                  endpoint.method === "PUT" ? "bg-yellow-100 text-yellow-800" :
                  "bg-red-100 text-red-800"
                }`}>
                  {endpoint.method}
                </span>
              </div>

              <div className="text-sm text-gray-600 mb-2">{endpoint.url}</div>

              {endpoint.description && (
                <div className="text-sm text-gray-700 mb-2">{endpoint.description}</div>
              )}

              {endpoint.lastCalled && (
                <div className="text-xs text-gray-500">
                  Last called: {endpoint.lastCalled.toLocaleString()}
                  {endpoint.responseTime && ` (${endpoint.responseTime}ms)`}
                  {endpoint.statusCode && ` - Status: ${endpoint.statusCode}`}
                </div>
              )}
            </div>
          ))}

          {endpoints.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>No API endpoints configured. Ask the copilot to add some!</p>
            </div>
          )}
        </div>
      </div>

      {/* Call History */}
      {callHistory.length > 0 && (
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-4">Recent API Calls</h2>
          <div className="space-y-2">
            {callHistory.slice(0, 10).map(call => (
              <div key={call.id} className="p-3 border rounded text-sm">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-medium">{call.endpointName}</span>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      call.success ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                    }`}>
                      {call.success ? "Success" : "Failed"}
                    </span>
                    <span className="text-gray-500">{call.method}</span>
                    {call.statusCode && <span className="text-gray-500">{call.statusCode}</span>}
                  </div>
                </div>

                <div className="text-gray-600 text-xs">
                  {call.timestamp.toLocaleString()} • {call.responseTime}ms
                </div>

                {call.error && (
                  <div className="text-red-600 text-xs mt-1">Error: {call.error}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="p-4 bg-blue-50 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-2">Try asking the copilot:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Add an API endpoint for user data at https://jsonplaceholder.typicode.com/users"</li>
          <li>• "Call the user data endpoint we just added"</li>
          <li>• "Add a POST endpoint for creating posts"</li>
          <li>• "Test all the API endpoints we have configured"</li>
          <li>• "Show me the history of API calls made"</li>
        </ul>
      </div>
    </div>
  );
}
```

## Error Handling and Validation

### Robust Action Implementation

```tsx
// app/hooks/useRobustCopilotAction.ts
import { useCopilotAction } from "@copilotkit/react-core";
import { useCallback } from "react";

export function useRobustCopilotAction(actionConfig: {
  name: string;
  description: string;
  parameters: any[];
  handler: (params: any) => Promise<any>;
  validateInput?: (params: any) => string | null;
  handleErrors?: (error: Error) => any;
  retries?: number;
}) {
  const {
    name,
    description,
    parameters,
    handler,
    validateInput,
    handleErrors,
    retries = 0,
  } = actionConfig;

  const robustHandler = useCallback(async (params: any) => {
    // Input validation
    if (validateInput) {
      const validationError = validateInput(params);
      if (validationError) {
        throw new Error(`Validation failed: ${validationError}`);
      }
    }

    let lastError: Error | null = null;

    // Retry logic
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const result = await handler(params);

        // Validate result if needed
        if (result && typeof result === 'object' && 'success' in result) {
          if (!result.success) {
            throw new Error(result.message || 'Operation failed');
          }
        }

        return result;

      } catch (error) {
        lastError = error as Error;

        // Don't retry on validation errors or the last attempt
        if (attempt === retries ||
            error.message?.includes('Validation failed') ||
            error.message?.includes('Invalid input')) {
          break;
        }

        // Exponential backoff
        const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    // Handle errors
    if (handleErrors && lastError) {
      return handleErrors(lastError);
    }

    throw lastError || new Error('Unknown error occurred');
  }, [handler, validateInput, handleErrors, retries]);

  useCopilotAction({
    name,
    description,
    parameters,
    handler: robustHandler,
  });
}
```

## Summary

In this chapter, we've covered:

- **Basic Actions**: Simple state modifications with useCopilotAction
- **Complex Actions**: Multi-parameter actions with validation
- **Asynchronous Operations**: API calls and external integrations
- **Error Handling**: Validation, retries, and error recovery
- **Action Patterns**: CRUD operations, searches, and updates
- **Robust Implementation**: Input validation and error handling

## Key Takeaways

1. **Parameter Definition**: Clearly define action parameters with types and descriptions
2. **Validation**: Always validate inputs before processing
3. **Error Handling**: Provide meaningful error messages and recovery options
4. **Async Operations**: Handle API calls and external services properly
5. **State Management**: Actions should modify app state and return results
6. **User Feedback**: Provide clear success/failure responses

## Next Steps

Now that the AI can perform actions in your app, let's explore the different chat UI components available in CopilotKit.

---

**Ready for Chapter 4?** [Chat Components](04-chat-components.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*