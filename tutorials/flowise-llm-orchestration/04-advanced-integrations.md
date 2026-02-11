---
layout: default
title: "Chapter 4: Advanced Integrations"
nav_order: 4
has_children: false
parent: "Flowise LLM Orchestration"
---

# Chapter 4: Advanced Integrations

> Complex multi-provider workflows and enterprise integrations

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- Building workflows that span multiple AI providers
- Implementing complex data routing and transformation
- Creating enterprise-grade integrations with existing systems
- Handling authentication and security across services
- Optimizing performance for large-scale workflows

## 🤖 Multi-Provider LLM Workflows

### **Provider Selection and Fallback Logic**

```typescript
// Intelligent LLM provider selection
class LLMOrchestrator {
  private providers: Map<string, LLMProvider> = new Map();
  private metrics: ProviderMetrics;

  constructor() {
    this.initializeProviders();
    this.metrics = new ProviderMetrics();
  }

  private initializeProviders() {
    // Initialize multiple LLM providers
    this.providers.set('openai', new OpenAIProvider({
      apiKey: process.env.OPENAI_API_KEY,
      models: ['gpt-4', 'gpt-3.5-turbo']
    }));

    this.providers.set('anthropic', new AnthropicProvider({
      apiKey: process.env.ANTHROPIC_API_KEY,
      models: ['claude-3-opus', 'claude-3-sonnet']
    }));

    this.providers.set('google', new GoogleProvider({
      apiKey: process.env.GOOGLE_API_KEY,
      models: ['gemini-pro', 'gemini-pro-vision']
    }));

    this.providers.set('local', new LocalProvider({
      endpoint: process.env.LOCAL_LLM_ENDPOINT
    }));
  }

  async selectProvider(requirements: ProviderRequirements): Promise<LLMProvider> {
    const candidates = this.rankProviders(requirements);

    for (const candidate of candidates) {
      if (await this.isProviderHealthy(candidate.provider)) {
        return candidate.provider;
      }
    }

    throw new Error('No healthy providers available');
  }

  private rankProviders(requirements: ProviderRequirements): ProviderCandidate[] {
    const candidates: ProviderCandidate[] = [];

    for (const [name, provider] of this.providers) {
      const score = this.calculateProviderScore(provider, requirements);
      candidates.push({ provider, score });
    }

    // Sort by score (highest first)
    return candidates.sort((a, b) => b.score - a.score);
  }

  private calculateProviderScore(provider: LLMProvider, requirements: ProviderRequirements): number {
    let score = 0;

    // Model capability match
    if (requirements.capabilities?.includes('vision') && provider.supportsVision()) {
      score += 30;
    }

    if (requirements.capabilities?.includes('function_calling') && provider.supportsFunctionCalling()) {
      score += 20;
    }

    // Performance metrics
    const metrics = this.metrics.getProviderMetrics(provider.getName());
    score += metrics.successRate * 20; // 0-20 points based on reliability
    score += Math.max(0, 20 - (metrics.averageLatency / 100)); // Lower latency = higher score

    // Cost efficiency
    if (requirements.budgetPriority) {
      score += (1 - metrics.costPerToken) * 15;
    }

    // Provider preferences
    if (requirements.preferredProviders?.includes(provider.getName())) {
      score += 15;
    }

    return score;
  }

  private async isProviderHealthy(provider: LLMProvider): Promise<boolean> {
    try {
      const healthCheck = await provider.healthCheck();
      return healthCheck.status === 'healthy' &&
             healthCheck.latency < 5000; // 5 second timeout
    } catch (error) {
      return false;
    }
  }

  async executeWithFallback(
    prompt: string,
    requirements: ProviderRequirements,
    maxRetries: number = 2
  ): Promise<LLMResponse> {
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const provider = await this.selectProvider(requirements);
        const response = await provider.generate(prompt, requirements);

        // Record success
        this.metrics.recordSuccess(provider.getName(), response.latency);

        return response;

      } catch (error) {
        // Record failure
        this.metrics.recordFailure(provider.getName(), error);

        if (attempt === maxRetries) {
          throw new Error(`All providers failed after ${maxRetries + 1} attempts`);
        }

        // Wait before retry with exponential backoff
        await this.delay(Math.pow(2, attempt) * 1000);
      }
    }
  }
}

interface ProviderRequirements {
  capabilities?: string[];
  maxTokens?: number;
  temperature?: number;
  budgetPriority?: boolean;
  preferredProviders?: string[];
  requiredLatency?: number;
}

interface ProviderCandidate {
  provider: LLMProvider;
  score: number;
}
```

### **Dynamic Provider Switching**

```typescript
// Workflow with dynamic provider selection
class MultiProviderWorkflow extends BaseNode {
  label = 'Multi-Provider LLM';
  name = 'multiProviderLLM';
  type = 'action';
  category = 'LLM';
  version = 1.0;
  description = 'Intelligent LLM selection across multiple providers';

  inputs: INodeParams[] = [
    {
      label: 'Prompt',
      name: 'prompt',
      type: 'string',
      description: 'Text prompt for LLM generation'
    },
    {
      label: 'Task Type',
      name: 'taskType',
      type: 'options',
      options: [
        { label: 'Creative Writing', name: 'creative' },
        { label: 'Code Generation', name: 'code' },
        { label: 'Analysis', name: 'analysis' },
        { label: 'Question Answering', name: 'qa' },
        { label: 'Summarization', name: 'summary' }
      ],
      default: 'analysis'
    },
    {
      label: 'Complexity Level',
      name: 'complexity',
      type: 'options',
      options: [
        { label: 'Simple', name: 'simple' },
        { label: 'Medium', name: 'medium' },
        { label: 'Complex', name: 'complex' }
      ],
      default: 'medium'
    },
    {
      label: 'Budget Priority',
      name: 'budgetPriority',
      type: 'boolean',
      default: false,
      description: 'Prioritize cost efficiency over performance'
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Response',
      name: 'response',
      type: 'string',
      description: 'Generated LLM response'
    },
    {
      label: 'Provider Used',
      name: 'provider',
      type: 'string',
      description: 'Which LLM provider was selected'
    },
    {
      label: 'Confidence',
      name: 'confidence',
      type: 'number',
      description: 'Confidence score of the response'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const prompt = nodeData.inputs?.prompt as string;
    const taskType = nodeData.inputs?.taskType as string;
    const complexity = nodeData.inputs?.complexity as string;
    const budgetPriority = nodeData.inputs?.budgetPriority as boolean;

    if (!prompt) {
      throw new Error('Prompt is required');
    }

    // Determine provider requirements based on task
    const requirements = this.buildRequirements(taskType, complexity, budgetPriority);

    try {
      const orchestrator = new LLMOrchestrator();
      const result = await orchestrator.executeWithFallback(prompt, requirements);

      return {
        response: result.text,
        provider: result.provider,
        confidence: result.confidence || 0.8
      };

    } catch (error) {
      throw new Error(`Multi-provider execution failed: ${error.message}`);
    }
  }

  private buildRequirements(taskType: string, complexity: string, budgetPriority: boolean): ProviderRequirements {
    const requirements: ProviderRequirements = {
      budgetPriority
    };

    // Task-specific requirements
    switch (taskType) {
      case 'creative':
        requirements.capabilities = ['creative_writing'];
        requirements.temperature = 0.8;
        break;
      case 'code':
        requirements.capabilities = ['code_generation'];
        requirements.temperature = 0.1;
        break;
      case 'analysis':
        requirements.capabilities = ['reasoning'];
        requirements.temperature = 0.3;
        break;
      case 'qa':
        requirements.capabilities = ['factual_qa'];
        requirements.temperature = 0.1;
        break;
      case 'summary':
        requirements.capabilities = ['summarization'];
        requirements.maxTokens = 500;
        break;
    }

    // Complexity-based requirements
    switch (complexity) {
      case 'simple':
        requirements.maxTokens = 1000;
        requirements.preferredProviders = ['gpt-3.5-turbo', 'claude-haiku'];
        break;
      case 'medium':
        requirements.maxTokens = 2000;
        requirements.preferredProviders = ['gpt-4', 'claude-sonnet'];
        break;
      case 'complex':
        requirements.maxTokens = 4000;
        requirements.preferredProviders = ['gpt-4', 'claude-opus'];
        break;
    }

    return requirements;
  }
}
```

## 🔄 Complex Data Routing

### **Intelligent Data Router**

```typescript
// Advanced data routing and transformation
class DataRouterNode implements INode {
  label = 'Intelligent Data Router';
  name = 'dataRouter';
  type = 'action';
  category = 'Logic';
  version = 1.0;
  description = 'Route data based on content analysis and rules';

  inputs: INodeParams[] = [
    {
      label: 'Input Data',
      name: 'inputData',
      type: 'json',
      description: 'Data to route'
    },
    {
      label: 'Routing Rules',
      name: 'routingRules',
      type: 'json',
      description: 'Rules for routing decisions',
      placeholder: '{"rules": [{"condition": "data.score > 0.8", "output": "high_quality"}, {"condition": "data.category == \'urgent\'", "output": "priority"}]}'
    },
    {
      label: 'Fallback Route',
      name: 'fallbackRoute',
      type: 'string',
      default: 'default',
      description: 'Default route when no rules match'
    }
  ];

  // Dynamic outputs based on routing rules
  outputs: INodeParams[] = [
    {
      label: 'Routed Data',
      name: 'routedData',
      type: 'json',
      description: 'Data sent to appropriate route'
    },
    {
      label: 'Route Taken',
      name: 'routeTaken',
      type: 'string',
      description: 'Which route the data was sent to'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const inputData = nodeData.inputs?.inputData as any;
    const routingRules = nodeData.inputs?.routingRules as RoutingRules;
    const fallbackRoute = nodeData.inputs?.fallbackRoute as string;

    if (!inputData) {
      throw new Error('Input data is required');
    }

    try {
      const routingDecision = await this.evaluateRoutingRules(inputData, routingRules);
      const selectedRoute = routingDecision.route || fallbackRoute;

      return {
        routedData: inputData,
        routeTaken: selectedRoute,
        routingMetadata: routingDecision.metadata
      };

    } catch (error) {
      throw new Error(`Data routing failed: ${error.message}`);
    }
  }

  private async evaluateRoutingRules(data: any, rules: RoutingRules): Promise<RoutingDecision> {
    if (!rules || !rules.rules) {
      return { route: 'default', metadata: {} };
    }

    // Evaluate each rule in order
    for (const rule of rules.rules) {
      try {
        const conditionMet = await this.evaluateCondition(rule.condition, data);

        if (conditionMet) {
          return {
            route: rule.output,
            metadata: {
              ruleMatched: rule.condition,
              evaluationTime: Date.now()
            }
          };
        }
      } catch (error) {
        // Log condition evaluation error but continue
        console.warn(`Rule evaluation failed: ${rule.condition}`, error);
      }
    }

    // No rules matched
    return {
      route: null,
      metadata: {
        noMatch: true,
        rulesEvaluated: rules.rules.length
      }
    };
  }

  private async evaluateCondition(condition: string, data: any): Promise<boolean> {
    // Create safe evaluation context
    const context = {
      data,
      input: data,
      ...data // Spread data properties for direct access
    };

    // Use expression evaluator for safety
    const expr = require('expr-eval');

    try {
      const result = expr.Parser.evaluate(condition, context);
      return Boolean(result);
    } catch (error) {
      throw new Error(`Condition evaluation failed: ${condition}`);
    }
  }
}

interface RoutingRules {
  rules: Array<{
    condition: string;
    output: string;
  }>;
}

interface RoutingDecision {
  route: string | null;
  metadata: Record<string, any>;
}
```

### **Data Transformation Pipeline**

```typescript
// Complex data transformation workflow
class DataTransformationPipeline implements INode {
  label = 'Data Transformation Pipeline';
  name = 'dataTransformationPipeline';
  type = 'action';
  category = 'Data Processing';
  version = 1.0;
  description = 'Multi-step data transformation with validation';

  inputs: INodeParams[] = [
    {
      label: 'Input Data',
      name: 'inputData',
      type: 'json',
      description: 'Raw data to transform'
    },
    {
      label: 'Transformation Steps',
      name: 'transformationSteps',
      type: 'json',
      description: 'Ordered list of transformation operations',
      placeholder: '[{"type": "filter", "condition": "item.active"}, {"type": "map", "field": "name", "transform": "uppercase"}, {"type": "sort", "field": "created_at", "order": "desc"}]'
    },
    {
      label: 'Validation Rules',
      name: 'validationRules',
      type: 'json',
      optional: true,
      description: 'Data validation rules to apply'
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Transformed Data',
      name: 'transformedData',
      type: 'json',
      description: 'Processed data'
    },
    {
      label: 'Processing Stats',
      name: 'processingStats',
      type: 'json',
      description: 'Transformation statistics'
    },
    {
      label: 'Validation Results',
      name: 'validationResults',
      type: 'json',
      description: 'Validation outcomes'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const inputData = nodeData.inputs?.inputData as any;
    const transformationSteps = nodeData.inputs?.transformationSteps as TransformationStep[];
    const validationRules = nodeData.inputs?.validationRules as ValidationRule[];

    if (!inputData) {
      throw new Error('Input data is required');
    }

    if (!Array.isArray(transformationSteps)) {
      throw new Error('Transformation steps must be an array');
    }

    const stats = {
      startTime: Date.now(),
      stepsProcessed: 0,
      itemsProcessed: 0,
      errors: 0
    };

    try {
      let transformedData = Array.isArray(inputData) ? [...inputData] : [inputData];

      // Apply each transformation step
      for (const step of transformationSteps) {
        transformedData = await this.applyTransformationStep(transformedData, step);
        stats.stepsProcessed++;
      }

      stats.itemsProcessed = transformedData.length;

      // Apply validation if provided
      let validationResults = null;
      if (validationRules && validationRules.length > 0) {
        validationResults = await this.validateData(transformedData, validationRules);
        stats.errors = validationResults.errors?.length || 0;
      }

      stats.endTime = Date.now();
      stats.duration = stats.endTime - stats.startTime;

      return {
        transformedData,
        processingStats: stats,
        validationResults
      };

    } catch (error) {
      throw new Error(`Data transformation failed: ${error.message}`);
    }
  }

  private async applyTransformationStep(data: any[], step: TransformationStep): Promise<any[]> {
    switch (step.type) {
      case 'filter':
        return data.filter(item => this.evaluateCondition(step.condition, item));

      case 'map':
        return data.map(item => this.applyMapping(item, step));

      case 'sort':
        return [...data].sort((a, b) => this.compareItems(a, b, step));

      case 'group':
        return this.groupData(data, step);

      case 'aggregate':
        return [this.aggregateData(data, step)];

      case 'join':
        return await this.joinData(data, step);

      default:
        throw new Error(`Unknown transformation type: ${step.type}`);
    }
  }

  private evaluateCondition(condition: string, item: any): boolean {
    const expr = require('expr-eval');
    const context = { item, ...item };
    return Boolean(expr.Parser.evaluate(condition, context));
  }

  private applyMapping(item: any, step: TransformationStep): any {
    if (step.field && step.transform) {
      const value = this.getNestedValue(item, step.field);
      const transformedValue = this.applyTransform(value, step.transform);
      return this.setNestedValue(item, step.field, transformedValue);
    }
    return item;
  }

  private applyTransform(value: any, transform: string): any {
    switch (transform) {
      case 'uppercase':
        return String(value).toUpperCase();
      case 'lowercase':
        return String(value).toLowerCase();
      case 'trim':
        return String(value).trim();
      case 'number':
        return Number(value);
      case 'boolean':
        return Boolean(value);
      default:
        return value;
    }
  }

  private async validateData(data: any[], rules: ValidationRule[]): Promise<ValidationResult> {
    const results: ValidationResult = {
      valid: true,
      errors: [],
      warnings: []
    };

    for (let i = 0; i < data.length; i++) {
      const item = data[i];

      for (const rule of rules) {
        const isValid = await this.validateRule(item, rule);

        if (!isValid) {
          results.valid = false;
          results.errors.push({
            itemIndex: i,
            rule: rule.name,
            message: rule.errorMessage || `Validation failed: ${rule.name}`
          });
        }
      }
    }

    return results;
  }

  private async validateRule(item: any, rule: ValidationRule): Promise<boolean> {
    switch (rule.type) {
      case 'required':
        return item[rule.field] != null;
      case 'type':
        return typeof item[rule.field] === rule.expectedType;
      case 'range':
        const value = Number(item[rule.field]);
        return value >= rule.min && value <= rule.max;
      case 'pattern':
        return new RegExp(rule.pattern).test(String(item[rule.field]));
      case 'custom':
        return this.evaluateCondition(rule.condition, item);
      default:
        return true;
    }
  }
}

interface TransformationStep {
  type: 'filter' | 'map' | 'sort' | 'group' | 'aggregate' | 'join';
  condition?: string;
  field?: string;
  transform?: string;
  order?: 'asc' | 'desc';
  groupBy?: string;
  aggregateFunction?: string;
  joinType?: 'left' | 'inner' | 'outer';
  joinData?: any[];
  joinKey?: string;
}

interface ValidationRule {
  name: string;
  type: 'required' | 'type' | 'range' | 'pattern' | 'custom';
  field: string;
  expectedType?: string;
  min?: number;
  max?: number;
  pattern?: string;
  condition?: string;
  errorMessage?: string;
}

interface ValidationResult {
  valid: boolean;
  errors: Array<{
    itemIndex: number;
    rule: string;
    message: string;
  }>;
  warnings: string[];
}
```

## 🏢 Enterprise Integrations

### **Database Integration Node**

```typescript
// Enterprise database integration
class EnterpriseDatabaseNode implements INode {
  label = 'Enterprise Database';
  name = 'enterpriseDatabase';
  type = 'action';
  category = 'Databases';
  version = 1.0;
  description = 'Connect to enterprise databases with advanced features';

  inputs: INodeParams[] = [
    {
      label: 'Database Type',
      name: 'dbType',
      type: 'options',
      options: [
        { label: 'PostgreSQL', name: 'postgres' },
        { label: 'MySQL', name: 'mysql' },
        { label: 'SQL Server', name: 'mssql' },
        { label: 'Oracle', name: 'oracle' },
        { label: 'MongoDB', name: 'mongodb' }
      ]
    },
    {
      label: 'Connection String',
      name: 'connectionString',
      type: 'password',
      description: 'Database connection string'
    },
    {
      label: 'Operation',
      name: 'operation',
      type: 'options',
      options: [
        { label: 'Query', name: 'query' },
        { label: 'Insert', name: 'insert' },
        { label: 'Update', name: 'update' },
        { label: 'Delete', name: 'delete' },
        { label: 'Stored Procedure', name: 'procedure' }
      ]
    },
    {
      label: 'Query/SQL',
      name: 'query',
      type: 'string',
      description: 'SQL query or stored procedure name',
      rows: 4
    },
    {
      label: 'Parameters',
      name: 'parameters',
      type: 'json',
      optional: true,
      description: 'Query parameters'
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Result',
      name: 'result',
      type: 'json',
      description: 'Query execution result'
    },
    {
      label: 'Row Count',
      name: 'rowCount',
      type: 'number',
      description: 'Number of affected rows'
    },
    {
      label: 'Execution Time',
      name: 'executionTime',
      type: 'number',
      description: 'Query execution time in milliseconds'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const dbType = nodeData.inputs?.dbType as string;
    const connectionString = nodeData.inputs?.connectionString as string;
    const operation = nodeData.inputs?.operation as string;
    const query = nodeData.inputs?.query as string;
    const parameters = nodeData.inputs?.parameters as any;

    if (!connectionString) {
      throw new Error('Database connection string is required');
    }

    if (!query) {
      throw new Error('Query is required');
    }

    const startTime = Date.now();

    try {
      const dbClient = await this.createDatabaseClient(dbType, connectionString);
      const result = await this.executeOperation(dbClient, operation, query, parameters);
      const executionTime = Date.now() - startTime;

      await dbClient.disconnect();

      return {
        result: result.data,
        rowCount: result.rowCount,
        executionTime
      };

    } catch (error) {
      throw new Error(`Database operation failed: ${error.message}`);
    }
  }

  private async createDatabaseClient(dbType: string, connectionString: string): Promise<DatabaseClient> {
    switch (dbType) {
      case 'postgres':
        return new PostgreSQLClient(connectionString);
      case 'mysql':
        return new MySQLClient(connectionString);
      case 'mssql':
        return new SQLServerClient(connectionString);
      case 'oracle':
        return new OracleClient(connectionString);
      case 'mongodb':
        return new MongoDBClient(connectionString);
      default:
        throw new Error(`Unsupported database type: ${dbType}`);
    }
  }

  private async executeOperation(
    client: DatabaseClient,
    operation: string,
    query: string,
    parameters: any
  ): Promise<DatabaseResult> {
    switch (operation) {
      case 'query':
        return await client.executeQuery(query, parameters);
      case 'insert':
        return await client.executeInsert(query, parameters);
      case 'update':
        return await client.executeUpdate(query, parameters);
      case 'delete':
        return await client.executeDelete(query, parameters);
      case 'procedure':
        return await client.executeProcedure(query, parameters);
      default:
        throw new Error(`Unsupported operation: ${operation}`);
    }
  }
}
```

### **API Gateway Integration**

```typescript
// API Gateway integration for enterprise systems
class ApiGatewayNode implements INode {
  label = 'API Gateway Integration';
  name = 'apiGateway';
  type = 'action';
  category = 'Integrations';
  version = 1.0;
  description = 'Connect to enterprise API gateways with authentication';

  inputs: INodeParams[] = [
    {
      label: 'Gateway Type',
      name: 'gatewayType',
      type: 'options',
      options: [
        { label: 'AWS API Gateway', name: 'aws' },
        { label: 'Azure API Management', name: 'azure' },
        { label: 'Kong Gateway', name: 'kong' },
        { label: 'Custom', name: 'custom' }
      ]
    },
    {
      label: 'Endpoint URL',
      name: 'endpointUrl',
      type: 'string',
      description: 'API Gateway endpoint URL'
    },
    {
      label: 'Authentication',
      name: 'auth',
      type: 'options',
      options: [
        { label: 'API Key', name: 'apiKey' },
        { label: 'OAuth2', name: 'oauth2' },
        { label: 'JWT', name: 'jwt' },
        { label: 'Mutual TLS', name: 'mtls' }
      ]
    },
    {
      label: 'Auth Credentials',
      name: 'authCredentials',
      type: 'json',
      description: 'Authentication credentials'
    },
    {
      label: 'Request Config',
      name: 'requestConfig',
      type: 'json',
      description: 'HTTP request configuration',
      placeholder: '{"method": "POST", "headers": {}, "body": {}}'
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
      label: 'Response Time',
      name: 'responseTime',
      type: 'number',
      description: 'Response time in milliseconds'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const gatewayType = nodeData.inputs?.gatewayType as string;
    const endpointUrl = nodeData.inputs?.endpointUrl as string;
    const authType = nodeData.inputs?.auth as string;
    const authCredentials = nodeData.inputs?.authCredentials as any;
    const requestConfig = nodeData.inputs?.requestConfig as HttpRequestConfig;

    if (!endpointUrl) {
      throw new Error('Endpoint URL is required');
    }

    const startTime = Date.now();

    try {
      const client = this.createGatewayClient(gatewayType);
      const authenticatedConfig = await this.applyAuthentication(
        requestConfig, authType, authCredentials
      );

      const response = await client.makeRequest(endpointUrl, authenticatedConfig);
      const responseTime = Date.now() - startTime;

      return {
        response: response.data,
        statusCode: response.status,
        responseTime
      };

    } catch (error) {
      throw new Error(`API Gateway request failed: ${error.message}`);
    }
  }

  private createGatewayClient(gatewayType: string): GatewayClient {
    switch (gatewayType) {
      case 'aws':
        return new AWSGatewayClient();
      case 'azure':
        return new AzureGatewayClient();
      case 'kong':
        return new KongGatewayClient();
      case 'custom':
        return new CustomGatewayClient();
      default:
        throw new Error(`Unsupported gateway type: ${gatewayType}`);
    }
  }

  private async applyAuthentication(
    config: HttpRequestConfig,
    authType: string,
    credentials: any
  ): Promise<HttpRequestConfig> {
    const authenticatedConfig = { ...config };

    switch (authType) {
      case 'apiKey':
        authenticatedConfig.headers = {
          ...config.headers,
          'X-API-Key': credentials.apiKey
        };
        break;

      case 'oauth2':
        const token = await this.getOAuth2Token(credentials);
        authenticatedConfig.headers = {
          ...config.headers,
          'Authorization': `Bearer ${token}`
        };
        break;

      case 'jwt':
        authenticatedConfig.headers = {
          ...config.headers,
          'Authorization': `Bearer ${credentials.token}`
        };
        break;

      case 'mtls':
        // Configure mutual TLS
        authenticatedConfig.cert = credentials.cert;
        authenticatedConfig.key = credentials.key;
        authenticatedConfig.ca = credentials.ca;
        break;
    }

    return authenticatedConfig;
  }

  private async getOAuth2Token(credentials: OAuth2Credentials): Promise<string> {
    // Implement OAuth2 token retrieval
    const response = await fetch(credentials.tokenUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Basic ${Buffer.from(`${credentials.clientId}:${credentials.clientSecret}`).toString('base64')}`
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        scope: credentials.scope || ''
      })
    });

    const data = await response.json();
    return data.access_token;
  }
}

interface HttpRequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  headers?: Record<string, string>;
  body?: any;
  timeout?: number;
}

interface OAuth2Credentials {
  tokenUrl: string;
  clientId: string;
  clientSecret: string;
  scope?: string;
}
```

## 🔐 Security and Compliance

### **Enterprise Authentication**

```typescript
// Enterprise authentication node
class EnterpriseAuthNode implements INode {
  label = 'Enterprise Authentication';
  name = 'enterpriseAuth';
  type = 'action';
  category = 'Security';
  version = 1.0;
  description = 'Enterprise-grade authentication with SSO and MFA';

  inputs: INodeParams[] = [
    {
      label: 'Auth Provider',
      name: 'authProvider',
      type: 'options',
      options: [
        { label: 'Azure AD', name: 'azuread' },
        { label: 'AWS Cognito', name: 'cognito' },
        { label: 'Okta', name: 'okta' },
        { label: 'Auth0', name: 'auth0' },
        { label: 'LDAP', name: 'ldap' },
        { label: 'SAML', name: 'saml' }
      ]
    },
    {
      label: 'Credentials',
      name: 'credentials',
      type: 'json',
      description: 'Authentication credentials or configuration'
    },
    {
      label: 'MFA Required',
      name: 'mfaRequired',
      type: 'boolean',
      default: false,
      description: 'Require multi-factor authentication'
    }
  ];

  outputs: INodeParams[] = [
    {
      label: 'Authenticated',
      name: 'authenticated',
      type: 'boolean',
      description: 'Authentication success status'
    },
    {
      label: 'User Info',
      name: 'userInfo',
      type: 'json',
      description: 'User profile and permissions'
    },
    {
      label: 'Token',
      name: 'token',
      type: 'string',
      description: 'Access token for subsequent requests'
    }
  ];

  async run(nodeData: INodeData): Promise<ICommonObject> {
    const authProvider = nodeData.inputs?.authProvider as string;
    const credentials = nodeData.inputs?.credentials as any;
    const mfaRequired = nodeData.inputs?.mfaRequired as boolean;

    if (!credentials) {
      throw new Error('Authentication credentials are required');
    }

    try {
      const authClient = this.createAuthClient(authProvider);
      const authResult = await authClient.authenticate(credentials, mfaRequired);

      return {
        authenticated: authResult.success,
        userInfo: authResult.userInfo,
        token: authResult.token
      };

    } catch (error) {
      throw new Error(`Authentication failed: ${error.message}`);
    }
  }

  private createAuthClient(provider: string): AuthClient {
    switch (provider) {
      case 'azuread':
        return new AzureADClient();
      case 'cognito':
        return new CognitoClient();
      case 'okta':
        return new OktaClient();
      case 'auth0':
        return new Auth0Client();
      case 'ldap':
        return new LDAPClient();
      case 'saml':
        return new SAMLClient();
      default:
        throw new Error(`Unsupported auth provider: ${provider}`);
    }
  }
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 75 minutes**

1. **Multi-Provider Workflow**: Create a workflow that uses different LLM providers based on task requirements
2. **Complex Data Routing**: Build a data router that analyzes content and routes to appropriate processing paths
3. **Enterprise Integration**: Connect to a database and API gateway in a single workflow
4. **Authentication Flow**: Implement enterprise authentication with MFA validation
5. **Performance Optimization**: Monitor and optimize a complex multi-service workflow

---

**Ready for production deployment?** Continue to [Chapter 5: Production Deployment](05-production-deployment.md)