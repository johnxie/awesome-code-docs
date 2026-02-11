---
layout: default
title: "Chapter 3: Node Development"
nav_order: 3
has_children: false
parent: "Flowise LLM Orchestration"
---

# Chapter 3: Node Development

> Creating custom nodes and extending Flowise's capabilities

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- The node development framework and APIs
- Creating custom node types with specific functionality
- Integrating external APIs and services
- Testing and debugging custom nodes
- Packaging and distributing custom nodes

## 🏗️ Node Development Framework

### **Node Class Structure**

All Flowise nodes extend the base `INode` interface:

```typescript
// Base node interface
interface INode {
  label: string;
  name: string;
  type: NodeType;
  category: string;
  version: number;
  description?: string;
  icon?: string;
  inputs?: INodeParams[];
  outputs?: INodeParams[];
  init?: (nodeData: INodeData, input: string) => Promise<any>;
  run?: (nodeData: INodeData, input: string) => Promise<string | ICommonObject>;
}

// Node implementation
abstract class BaseNode implements INode {
  abstract label: string;
  abstract name: string;
  abstract type: NodeType;
  abstract category: string;
  abstract version: number;
  abstract description: string;
  abstract inputs: INodeParams[];
  abstract outputs: INodeParams[];

  // Optional lifecycle methods
  async init?(nodeData: INodeData, input: string): Promise<any> {
    // Initialization logic
  }

  async run?(nodeData: INodeData, input: string): Promise<string | ICommonObject> {
    // Main execution logic
    throw new Error('run() method must be implemented by subclass');
  }
}

// Node parameters interface
interface INodeParams {
  label: string;
  name: string;
  type: NodeParamsType;
  description?: string;
  default?: any;
  optional?: boolean;
  options?: Array<{ label: string; name: string }>;
  placeholder?: string;
  rows?: number;
  list?: boolean;
  acceptVariable?: boolean;
  id?: string;
}
```

### **Creating a Custom Node**

```typescript
// Example: Custom sentiment analysis node
import { INode, INodeData, INodeParams, ICommonObject } from 'flowise-components';

class SentimentAnalysisNode implements INode {
  label = 'Sentiment Analysis';
  name = 'sentimentAnalysis';
  type = 'action';
  category = 'Analysis';
  version = 1.0;
  description = 'Analyze sentiment of text using various AI models';
  icon = 'sentiment.png';

  inputs: INodeParams[] = [
    {
      label: 'Text Input',
      name: 'textInput',
      type: 'string',
      description: 'Text to analyze for sentiment',
      placeholder: 'Enter text to analyze...'
    },
    {
      label: 'Model',
      name: 'model',
      type: 'options',
      description: 'AI model to use for analysis',
      options: [
        { label: 'GPT-4', name: 'gpt-4' },
        { label: 'Claude', name: 'claude' },
        { label: 'Local Model', name: 'local' }
      ],
      default: 'gpt-4'
    },
    {
      label: 'API Key',
      name: 'apiKey',
      type: 'password',
      description: 'API key for the selected model'
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Sentiment',
      name: 'sentiment',
      type: 'string',
      description: 'Detected sentiment (positive/negative/neutral)'
    },
    {
      label: 'Confidence',
      name: 'confidence',
      type: 'number',
      description: 'Confidence score (0-1)'
    },
    {
      label: 'Full Analysis',
      name: 'fullAnalysis',
      type: 'json',
      description: 'Complete analysis including reasoning'
    }
  ];

  async init(nodeData: INodeData): Promise<any> {
    // Initialize any required resources
    const model = nodeData.inputs?.model as string;
    const apiKey = nodeData.inputs?.apiKey as string;

    // Validate API key format
    if (!apiKey) {
      throw new Error('API key is required');
    }

    // Initialize model client
    return this.initializeModelClient(model, apiKey);
  }

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const textInput = nodeData.inputs?.textInput as string;
    const model = nodeData.inputs?.model as string;

    if (!textInput) {
      throw new Error('Text input is required');
    }

    try {
      // Perform sentiment analysis
      const analysis = await this.analyzeSentiment(textInput, model);

      return {
        sentiment: analysis.sentiment,
        confidence: analysis.confidence,
        fullAnalysis: analysis
      };

    } catch (error) {
      throw new Error(`Sentiment analysis failed: ${error.message}`);
    }
  }

  private async initializeModelClient(model: string, apiKey: string) {
    // Initialize appropriate model client
    switch (model) {
      case 'gpt-4':
        return new OpenAIClient(apiKey);
      case 'claude':
        return new AnthropicClient(apiKey);
      case 'local':
        return new LocalModelClient();
      default:
        throw new Error(`Unsupported model: ${model}`);
    }
  }

  private async analyzeSentiment(text: string, model: string): Promise<SentimentResult> {
    const prompt = `
Analyze the sentiment of the following text. Respond with a JSON object containing:
- sentiment: "positive", "negative", or "neutral"
- confidence: number between 0 and 1
- reasoning: brief explanation

Text: "${text}"
    `;

    // Call the appropriate model
    const client = await this.getModelClient(model);
    const response = await client.generate(prompt, {
      temperature: 0.1,
      maxTokens: 200
    });

    // Parse response
    try {
      const result = JSON.parse(response);
      return {
        sentiment: result.sentiment,
        confidence: result.confidence,
        reasoning: result.reasoning,
        model: model,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      throw new Error('Failed to parse model response');
    }
  }
}

interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  reasoning: string;
  model: string;
  timestamp: string;
}
```

## 🔧 Advanced Node Patterns

### **API Integration Node**

```typescript
// Generic API integration node
class ApiIntegrationNode implements INode {
  label = 'API Integration';
  name = 'apiIntegration';
  type = 'action';
  category = 'Integrations';
  version = 1.0;
  description = 'Make HTTP requests to external APIs';
  icon = 'api.png';

  inputs: INodeParams[] = [
    {
      label: 'Method',
      name: 'method',
      type: 'options',
      options: [
        { label: 'GET', name: 'GET' },
        { label: 'POST', name: 'POST' },
        { label: 'PUT', name: 'PUT' },
        { label: 'DELETE', name: 'DELETE' },
        { label: 'PATCH', name: 'PATCH' }
      ],
      default: 'GET'
    },
    {
      label: 'URL',
      name: 'url',
      type: 'string',
      description: 'API endpoint URL',
      placeholder: 'https://api.example.com/endpoint'
    },
    {
      label: 'Headers',
      name: 'headers',
      type: 'json',
      description: 'Request headers as JSON',
      optional: true
    },
    {
      label: 'Body',
      name: 'body',
      type: 'json',
      description: 'Request body as JSON',
      optional: true
    },
    {
      label: 'Authentication',
      name: 'auth',
      type: 'options',
      options: [
        { label: 'None', name: 'none' },
        { label: 'Bearer Token', name: 'bearer' },
        { label: 'API Key', name: 'apiKey' },
        { label: 'Basic Auth', name: 'basic' }
      ],
      default: 'none',
      optional: true
    },
    {
      label: 'Auth Token',
      name: 'authToken',
      type: 'password',
      description: 'Authentication token/key',
      optional: true
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Response',
      name: 'response',
      type: 'json',
      description: 'API response data'
    },
    {
      label: 'Status Code',
      name: 'statusCode',
      type: 'number',
      description: 'HTTP status code'
    },
    {
      label: 'Headers',
      name: 'responseHeaders',
      type: 'json',
      description: 'Response headers'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const method = nodeData.inputs?.method as string;
    const url = nodeData.inputs?.url as string;
    const headers = nodeData.inputs?.headers as Record<string, string> || {};
    const body = nodeData.inputs?.body as any;
    const auth = nodeData.inputs?.auth as string;
    const authToken = nodeData.inputs?.authToken as string;

    if (!url) {
      throw new Error('URL is required');
    }

    // Add authentication
    if (auth && authToken) {
      headers = await this.addAuthentication(headers, auth, authToken);
    }

    try {
      const response = await this.makeHttpRequest(method, url, headers, body);

      return {
        response: response.data,
        statusCode: response.status,
        responseHeaders: response.headers
      };

    } catch (error) {
      throw new Error(`API request failed: ${error.message}`);
    }
  }

  private async addAuthentication(
    headers: Record<string, string>,
    authType: string,
    token: string
  ): Promise<Record<string, string>> {
    const newHeaders = { ...headers };

    switch (authType) {
      case 'bearer':
        newHeaders['Authorization'] = `Bearer ${token}`;
        break;
      case 'apiKey':
        newHeaders['X-API-Key'] = token;
        break;
      case 'basic':
        const encoded = Buffer.from(token).toString('base64');
        newHeaders['Authorization'] = `Basic ${encoded}`;
        break;
    }

    return newHeaders;
  }

  private async makeHttpRequest(
    method: string,
    url: string,
    headers: Record<string, string>,
    body?: any
  ): Promise<HttpResponse> {
    const axios = require('axios');

    const config = {
      method: method.toLowerCase(),
      url,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Flowise/1.0',
        ...headers
      },
      timeout: 30000 // 30 seconds
    };

    if (body && ['post', 'put', 'patch'].includes(method.toLowerCase())) {
      config.data = body;
    }

    const response = await axios(config);

    return {
      data: response.data,
      status: response.status,
      headers: response.headers
    };
  }
}

interface HttpResponse {
  data: any;
  status: number;
  headers: Record<string, string>;
}
```

### **Conditional Logic Node**

```typescript
// Advanced conditional logic node
class ConditionalLogicNode implements INode {
  label = 'Conditional Logic';
  name = 'conditionalLogic';
  type = 'action';
  category = 'Logic';
  version = 1.0;
  description = 'Execute conditional logic with multiple branches';
  icon = 'logic.png';

  inputs: INodeParams[] = [
    {
      label: 'Condition Type',
      name: 'conditionType',
      type: 'options',
      options: [
        { label: 'Simple Expression', name: 'expression' },
        { label: 'JSON Path', name: 'jsonpath' },
        { label: 'Custom Function', name: 'function' }
      ],
      default: 'expression'
    },
    {
      label: 'Condition',
      name: 'condition',
      type: 'string',
      description: 'Condition to evaluate',
      placeholder: 'e.g., input.value > 10'
    },
    {
      label: 'Input Data',
      name: 'inputData',
      type: 'json',
      description: 'Data to evaluate condition against'
    },
    {
      label: 'Custom Function',
      name: 'customFunction',
      type: 'string',
      description: 'Custom evaluation function (when using function type)',
      optional: true
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Result',
      name: 'result',
      type: 'boolean',
      description: 'Condition evaluation result'
    },
    {
      label: 'True Path',
      name: 'truePath',
      type: 'string',
      description: 'Data passed to true branch'
    },
    {
      label: 'False Path',
      name: 'falsePath',
      type: 'string',
      description: 'Data passed to false branch'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const conditionType = nodeData.inputs?.conditionType as string;
    const condition = nodeData.inputs?.condition as string;
    const inputData = nodeData.inputs?.inputData as any;
    const customFunction = nodeData.inputs?.customFunction as string;

    if (!condition) {
      throw new Error('Condition is required');
    }

    let result: boolean;

    try {
      switch (conditionType) {
        case 'expression':
          result = await this.evaluateExpression(condition, inputData);
          break;
        case 'jsonpath':
          result = await this.evaluateJsonPath(condition, inputData);
          break;
        case 'function':
          result = await this.evaluateCustomFunction(customFunction, inputData);
          break;
        default:
          throw new Error(`Unsupported condition type: ${conditionType}`);
      }

      return {
        result,
        truePath: result ? inputData : null,
        falsePath: result ? null : inputData
      };

    } catch (error) {
      throw new Error(`Condition evaluation failed: ${error.message}`);
    }
  }

  private async evaluateExpression(expression: string, data: any): Promise<boolean> {
    // Create a safe evaluation context
    const context = {
      input: data,
      data: data,
      ...data // Spread data properties for direct access
    };

    // Use a safe evaluation library (e.g., expr-eval)
    const expr = require('expr-eval');

    try {
      const result = expr.Parser.evaluate(expression, context);
      return Boolean(result);
    } catch (error) {
      throw new Error(`Expression evaluation failed: ${error.message}`);
    }
  }

  private async evaluateJsonPath(path: string, data: any): Promise<boolean> {
    const jsonpath = require('jsonpath');

    try {
      const result = jsonpath.query(data, path);
      // Return true if path exists and has truthy value
      return result.length > 0 && Boolean(result[0]);
    } catch (error) {
      throw new Error(`JSONPath evaluation failed: ${error.message}`);
    }
  }

  private async evaluateCustomFunction(functionCode: string, data: any): Promise<boolean> {
    // Create a safe function execution context
    const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;

    try {
      const func = new AsyncFunction('data', 'input', `return (${functionCode})`);
      const result = await func(data, data);
      return Boolean(result);
    } catch (error) {
      throw new Error(`Custom function execution failed: ${error.message}`);
    }
  }
}
```

## 📦 Node Packaging and Distribution

### **Node Package Structure**

```
custom-nodes/
├── package.json
├── tsconfig.json
├── src/
│   ├── nodes/
│   │   ├── sentimentAnalysis.ts
│   │   ├── apiIntegration.ts
│   │   └── conditionalLogic.ts
│   ├── utils/
│   │   ├── httpClient.ts
│   │   └── validation.ts
│   └── index.ts
├── dist/
│   ├── nodes/
│   ├── utils/
│   └── index.js
├── tests/
│   ├── sentimentAnalysis.test.ts
│   ├── apiIntegration.test.ts
│   └── conditionalLogic.test.ts
├── examples/
│   ├── sentimentWorkflow.json
│   └── apiIntegrationWorkflow.json
├── README.md
└── LICENSE
```

### **Package.json Configuration**

```json
{
  "name": "flowise-custom-nodes",
  "version": "1.0.0",
  "description": "Custom nodes for Flowise LLM orchestration platform",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write src/**/*.ts"
  },
  "keywords": ["flowise", "nodes", "llm", "ai", "workflow"],
  "author": "Your Name",
  "license": "MIT",
  "peerDependencies": {
    "flowise-components": "^1.0.0"
  },
  "devDependencies": {
    "@types/jest": "^29.0.0",
    "@types/node": "^18.0.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "@typescript-eslint/parser": "^5.0.0",
    "eslint": "^8.0.0",
    "flowise-components": "^1.0.0",
    "jest": "^29.0.0",
    "prettier": "^2.0.0",
    "typescript": "^4.9.0"
  },
  "dependencies": {
    "axios": "^1.0.0",
    "expr-eval": "^2.0.0",
    "jsonpath": "^1.1.1"
  },
  "flowise": {
    "nodes": [
      "dist/nodes/sentimentAnalysis.js",
      "dist/nodes/apiIntegration.js",
      "dist/nodes/conditionalLogic.js"
    ]
  }
}
```

### **Node Registration**

```typescript
// Main entry point for node package
import { INode } from 'flowise-components';
import SentimentAnalysisNode from './nodes/sentimentAnalysis';
import ApiIntegrationNode from './nodes/apiIntegration';
import ConditionalLogicNode from './nodes/conditionalLogic';

// Export all custom nodes
const customNodes: INode[] = [
  new SentimentAnalysisNode(),
  new ApiIntegrationNode(),
  new ConditionalLogicNode()
];

export default customNodes;

// Named exports for individual nodes
export { SentimentAnalysisNode, ApiIntegrationNode, ConditionalLogicNode };
```

### **Installation and Registration**

```typescript
// In Flowise main application
import customNodes from 'flowise-custom-nodes';

// Register custom nodes
customNodes.forEach(node => {
  app.nodes.register(node.name, node);
});

// Or register individually
import { SentimentAnalysisNode } from 'flowise-custom-nodes';
app.nodes.register('sentimentAnalysis', new SentimentAnalysisNode());
```

## 🧪 Testing Custom Nodes

### **Unit Testing Framework**

```typescript
// Test setup
import { INodeData } from 'flowise-components';
import SentimentAnalysisNode from '../src/nodes/sentimentAnalysis';

describe('SentimentAnalysisNode', () => {
  let node: SentimentAnalysisNode;

  beforeEach(() => {
    node = new SentimentAnalysisNode();
  });

  describe('initialization', () => {
    test('should initialize with correct properties', () => {
      expect(node.label).toBe('Sentiment Analysis');
      expect(node.name).toBe('sentimentAnalysis');
      expect(node.category).toBe('Analysis');
    });

    test('should have required inputs', () => {
      const textInput = node.inputs.find(input => input.name === 'textInput');
      expect(textInput).toBeDefined();
      expect(textInput?.type).toBe('string');
      expect(textInput?.optional).toBeFalsy();
    });
  });

  describe('execution', () => {
    test('should analyze positive sentiment', async () => {
      const nodeData: INodeData = {
        inputs: {
          textInput: 'I love this product! It works great.',
          model: 'gpt-4',
          apiKey: 'test-key'
        }
      };

      // Mock the model client
      jest.spyOn(node, 'analyzeSentiment').mockResolvedValue({
        sentiment: 'positive',
        confidence: 0.95,
        reasoning: 'Positive language and enthusiasm detected'
      });

      const result = await node.run(nodeData);

      expect(result.sentiment).toBe('positive');
      expect(result.confidence).toBe(0.95);
    });

    test('should handle missing input', async () => {
      const nodeData: INodeData = {
        inputs: {
          textInput: '',
          model: 'gpt-4',
          apiKey: 'test-key'
        }
      };

      await expect(node.run(nodeData)).rejects.toThrow('Text input is required');
    });

    test('should handle API errors', async () => {
      const nodeData: INodeData = {
        inputs: {
          textInput: 'Test text',
          model: 'gpt-4',
          apiKey: 'invalid-key'
        }
      };

      jest.spyOn(node, 'analyzeSentiment').mockRejectedValue(
        new Error('API authentication failed')
      );

      await expect(node.run(nodeData)).rejects.toThrow('Sentiment analysis failed');
    });
  });

  describe('input validation', () => {
    test('should validate required fields', () => {
      const invalidData: INodeData = {
        inputs: {
          // Missing required textInput
          model: 'gpt-4'
        }
      };

      expect(() => node.validateInput(invalidData.inputs)).toThrow();
    });

    test('should accept valid inputs', () => {
      const validData: INodeData = {
        inputs: {
          textInput: 'Valid text input',
          model: 'gpt-4',
          apiKey: 'valid-key'
        }
      };

      expect(() => node.validateInput(validData.inputs)).not.toThrow();
    });
  });
});
```

## 🐛 Debugging and Troubleshooting

### **Node Debugging Tools**

```typescript
// Debug utilities for custom nodes
class NodeDebugger {
  private debugLogs: DebugLog[] = [];
  private breakpoints: Map<string, boolean> = new Map();

  enableDebugging(nodeId: string): void {
    this.breakpoints.set(nodeId, true);
  }

  disableDebugging(nodeId: string): void {
    this.breakpoints.delete(nodeId);
  }

  async debugNodeExecution(
    node: INode,
    nodeData: INodeData,
    input: string
  ): Promise<ICommonObject> {
    const nodeId = `${node.name}_${Date.now()}`;

    // Log execution start
    this.log('debug', nodeId, 'execution_start', { nodeData, input });

    if (this.breakpoints.has(node.name)) {
      await this.pauseExecution(nodeId, 'breakpoint_hit');
    }

    try {
      // Execute node with timing
      const startTime = Date.now();
      const result = await node.run(nodeData);
      const executionTime = Date.now() - startTime;

      // Log successful execution
      this.log('debug', nodeId, 'execution_success', {
        result,
        executionTime
      });

      return result;

    } catch (error) {
      // Log execution failure
      this.log('error', nodeId, 'execution_failed', {
        error: error.message,
        stack: error.stack
      });

      throw error;
    }
  }

  private log(level: 'debug' | 'info' | 'warn' | 'error', nodeId: string, event: string, data: any): void {
    const logEntry: DebugLog = {
      timestamp: new Date().toISOString(),
      level,
      nodeId,
      event,
      data
    };

    this.debugLogs.push(logEntry);

    // Also output to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[${level.toUpperCase()}] ${nodeId}: ${event}`, data);
    }
  }

  private async pauseExecution(nodeId: string, reason: string): Promise<void> {
    return new Promise((resolve) => {
      console.log(`⏸️ Execution paused for ${nodeId}: ${reason}`);
      console.log('Press Enter to continue...');

      process.stdin.once('data', () => {
        console.log(`▶️ Resuming execution for ${nodeId}`);
        resolve();
      });
    });
  }

  getDebugLogs(nodeId?: string): DebugLog[] {
    if (nodeId) {
      return this.debugLogs.filter(log => log.nodeId.startsWith(nodeId));
    }
    return this.debugLogs;
  }

  clearDebugLogs(): void {
    this.debugLogs = [];
  }
}

interface DebugLog {
  timestamp: string;
  level: 'debug' | 'info' | 'warn' | 'error';
  nodeId: string;
  event: string;
  data: any;
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 60 minutes**

1. **Create a Simple Custom Node**: Build a node that processes text (e.g., word count, text transformation)
2. **Add External API Integration**: Create a node that calls a weather API or similar service
3. **Implement Conditional Logic**: Build a decision-making node with multiple outputs
4. **Package Your Nodes**: Create a distributable node package with proper documentation
5. **Test and Debug**: Write unit tests and debug your custom nodes

---

**Ready for advanced integrations?** Continue to [Chapter 4: Advanced Integrations](04-advanced-integrations.md)