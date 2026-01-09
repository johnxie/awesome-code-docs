---
layout: default
title: "Chapter 8: Discovery Tools - Finding n8n Nodes"
parent: "n8n-MCP Tutorial"
nav_order: 8
---

# Chapter 8: Discovery Tools - Finding n8n Nodes

Welcome to the discovery layer! In [Chapter 7](07_mcp_tools.md), we explored the overall MCP tools architecture. Now let's dive deep into the discovery tools—the capabilities that enable AI assistants to find and explore n8n's vast ecosystem of 1,000+ nodes.

The discovery tools are like a sophisticated library catalog system. Instead of wandering through endless documentation, AI assistants can instantly find exactly the nodes they need for their workflow automation tasks.

## The Challenge of Node Discovery

With 1,000+ n8n nodes across 537 core and 547 community integrations, finding the right node is complex:

- **Overwhelming Choice**: Which email node to use? Gmail, Outlook, SendGrid?
- **Unfamiliar Categories**: What does "Data & Storage" include?
- **Hidden Capabilities**: Which nodes support AI features?
- **Version Differences**: Which nodes work with different n8n versions?

The `search_nodes` tool solves these challenges with intelligent search and filtering.

## The search_nodes Tool

This is the primary discovery tool that AI assistants use to explore n8n's capabilities:

### Tool Signature
```typescript
Tool Name: search_nodes
Description: Search through n8n nodes using text queries and filters

Parameters:
- query?: string        // Text search across names, descriptions, categories
- category?: string     // Filter by node category
- is_ai_tool?: boolean  // Filter for AI-capable nodes only
- limit?: number        // Maximum results (default: 10, max: 50)
- offset?: number       // Pagination offset (default: 0)

Returns: Array of matching nodes with metadata
```

### Search Capabilities

#### Text Search
The tool searches across multiple fields simultaneously:
- **Node names**: "Gmail", "HTTP Request", "OpenAI"
- **Descriptions**: Full-text search of node descriptions
- **Categories**: "Communication", "Data & Storage"
- **Package names**: "n8n-nodes-base", community packages

```typescript
// Example searches
"email automation"     // Finds Gmail, Outlook, SendGrid nodes
"spreadsheet"         // Finds Google Sheets, Excel, Airtable
"social media"        // Finds Twitter, Facebook, LinkedIn nodes
"database"           // Finds MySQL, PostgreSQL, MongoDB nodes
```

#### Category Filtering
Nodes are organized into logical categories:

```typescript
const categories = [
  'Communication',     // Email, SMS, Chat
  'Data & Storage',    // Databases, Files, APIs
  'Productivity',      // Calendars, Documents, Tasks
  'Marketing',         // CRM, Analytics, Advertising
  'Development',       // Code, APIs, Webhooks
  'Miscellaneous'      // Everything else
];
```

#### AI Tool Filtering
Special filter for nodes with AI capabilities:

```typescript
// Find all AI-capable nodes
{ "is_ai_tool": true }

// Find AI tools in communication category
{ "query": "communication", "is_ai_tool": true }
```

### Response Format

The tool returns structured node information:

```typescript
interface SearchResult {
  nodeType: string;           // "n8n-nodes-base.gmail"
  packageName: string;        // "n8n-nodes-base"
  displayName: string;        // "Gmail"
  description: string;        // "Send emails via Gmail"
  category: string;           // "Communication"
  isAiTool: boolean;          // true/false
  isTrigger: boolean;         // Can start workflows
  isWebhook: boolean;         // Has webhook capabilities
  developmentStyle: 'declarative' | 'programmatic';
  version?: string;           // Node version
}
```

## Intelligent Search Algorithm

The search uses a sophisticated ranking system:

### Relevance Scoring
```typescript
function calculateRelevance(node: NodeData, query: string): number {
  let score = 0;

  // Exact matches get highest score
  if (node.displayName.toLowerCase() === query.toLowerCase()) {
    score += 100;
  }

  // Starts with query gets high score
  if (node.displayName.toLowerCase().startsWith(query.toLowerCase())) {
    score += 50;
  }

  // Contains query gets medium score
  if (node.displayName.toLowerCase().includes(query.toLowerCase())) {
    score += 25;
  }

  // Description matches get lower score
  if (node.description.toLowerCase().includes(query.toLowerCase())) {
    score += 10;
  }

  return score;
}
```

### Result Ranking
Results are ordered by:
1. **Relevance score** (highest first)
2. **Popularity** (commonly used nodes)
3. **Alphabetical** (as tiebreaker)

## Real-World Usage Examples

### Example 1: Finding Email Nodes
```
AI Assistant: "I need to send automated emails"
Tool Call: search_nodes({"query": "email", "limit": 5})

Response:
[
  {
    "nodeType": "n8n-nodes-base.gmail",
    "displayName": "Gmail",
    "description": "Send and receive emails via Gmail",
    "category": "Communication",
    "isAiTool": false
  },
  {
    "nodeType": "n8n-nodes-base.emailSend",
    "displayName": "Send Email",
    "description": "Send emails via SMTP",
    "category": "Communication",
    "isAiTool": false
  },
  {
    "nodeType": "n8n-nodes-base.outlook",
    "displayName": "Microsoft Outlook",
    "description": "Work with Outlook emails and calendar",
    "category": "Communication",
    "isAiTool": false
  }
]
```

### Example 2: AI-Powered Content Creation
```
AI Assistant: "I need AI tools for content creation"
Tool Call: search_nodes({"query": "content", "is_ai_tool": true})

Response: AI content creation nodes like OpenAI, Anthropic, etc.
```

### Example 3: Social Media Automation
```
AI Assistant: "Help me automate social media posting"
Tool Call: search_nodes({"category": "Communication", "query": "social"})

Response: Twitter, Facebook, LinkedIn, Instagram nodes
```

### Example 4: Database Integration
```
AI Assistant: "I need to connect to a PostgreSQL database"
Tool Call: search_nodes({"query": "postgresql"})

Response:
[
  {
    "nodeType": "n8n-nodes-base.postgres",
    "displayName": "PostgreSQL",
    "description": "Connect to PostgreSQL database",
    "category": "Data & Storage"
  }
]
```

## Advanced Search Patterns

### Combining Filters
```typescript
// AI tools in productivity category
{
  "category": "Productivity",
  "is_ai_tool": true
}

// Communication tools that are triggers
{
  "category": "Communication",
  "is_trigger": true  // This would be a custom filter if supported
}
```

### Pagination for Large Result Sets
```typescript
// Get first 10 results
{ "query": "api", "limit": 10, "offset": 0 }

// Get next 10 results
{ "query": "api", "limit": 10, "offset": 10 }
```

## Performance Optimizations

### Database Indexing Strategy
The search leverages multiple indexes for speed:

```sql
-- Full-text search index
CREATE VIRTUAL TABLE nodes_fts USING fts5(
  display_name, description, category
);

-- Filtered search indexes
CREATE INDEX idx_category_ai ON nodes(category, is_ai_tool);
CREATE INDEX idx_ai_tool ON nodes(is_ai_tool);
CREATE INDEX idx_trigger ON nodes(is_trigger);
```

### Query Execution Plan
```typescript
async function executeSearch(params: SearchParams): Promise<SearchResult[]> {
  const { query, category, is_ai_tool, limit = 10, offset = 0 } = params;

  // Use FTS for text queries
  if (query) {
    return this.executeFTSSearch(query, category, is_ai_tool, limit, offset);
  }

  // Use indexed queries for filters only
  return this.executeFilterSearch(category, is_ai_tool, limit, offset);
}
```

### Caching Strategy
```typescript
class SearchCache {
  // Cache popular searches
  @Cache({ ttl: 300000 }) // 5 minutes
  async searchPopular(query: string): Promise<NodeData[]> {
    // Implementation
  }

  // Cache category lists (changes infrequently)
  @Cache({ ttl: 3600000 }) // 1 hour
  async getCategoryNodes(category: string): Promise<NodeData[]> {
    // Implementation
  }
}
```

## Integration with Other Tools

The `search_nodes` tool works seamlessly with other MCP tools:

### Search → Get Node Details
```typescript
// 1. Search for nodes
const results = await search_nodes({ query: "gmail" });

// 2. Get detailed information
const details = await get_node({ node_type: results[0].nodeType });
```

### Search → Validate Configuration
```typescript
// 1. Find appropriate node
const nodes = await search_nodes({ query: "webhook" });

// 2. Validate configuration
const validation = await validate_node({
  node_type: nodes[0].nodeType,
  configuration: userConfig
});
```

## Error Handling and Edge Cases

### Empty Results
```typescript
// No matches found
{
  "success": true,
  "data": [],
  "metadata": {
    "totalMatches": 0,
    "searchTime": 15
  }
}
```

### Invalid Parameters
```typescript
// Limit too high
{
  "success": false,
  "errors": ["Limit cannot exceed 50"],
  "metadata": { "executionTime": 2 }
}
```

### Database Connection Issues
```typescript
// Automatic retry with fallback
try {
  return await this.searchWithRetry(params);
} catch (error) {
  // Return cached results or empty array
  return this.getCachedResults(params) || [];
}
```

## Analytics and Usage Insights

The tool collects usage analytics:

```typescript
interface SearchAnalytics {
  query: string;
  filters: SearchFilters;
  resultCount: number;
  executionTime: number;
  timestamp: Date;
  sessionId: string;
  instanceId?: string;
}

// Track popular searches
function recordSearchUsage(analytics: SearchAnalytics) {
  // Store for analysis
  this.db.insert('search_analytics', analytics);

  // Update popularity scores
  this.updateNodePopularity(analytics.query);
}
```

## Testing Strategy

Comprehensive testing ensures reliability:

```typescript
describe('search_nodes tool', () => {
  it('should find exact matches', async () => {
    const results = await search_nodes({ query: 'Gmail' });
    expect(results[0].displayName).toBe('Gmail');
  });

  it('should filter by category', async () => {
    const results = await search_nodes({
      category: 'Communication',
      limit: 5
    });
    expect(results.every(r => r.category === 'Communication')).toBe(true);
  });

  it('should handle AI tool filtering', async () => {
    const results = await search_nodes({ is_ai_tool: true });
    expect(results.every(r => r.isAiTool)).toBe(true);
  });

  it('should respect pagination', async () => {
    const page1 = await search_nodes({ limit: 2, offset: 0 });
    const page2 = await search_nodes({ limit: 2, offset: 2 });

    expect(page1).toHaveLength(2);
    expect(page2).toHaveLength(2);
    expect(page1[1]).not.toEqual(page2[0]);
  });
});
```

## Future Enhancements

### Semantic Search
```typescript
// Natural language understanding
{
  "query": "send emails when something happens",
  "intent": "trigger-based-email"
}
```

### Personalized Recommendations
```typescript
// Based on usage history
{
  "query": "email",
  "userId": "user123",
  "recommendations": true
}
```

### Visual Search
```typescript
// Search by workflow patterns
{
  "pattern": "webhook -> filter -> email",
  "findSimilar": true
}
```

Congratulations! You now understand how the discovery tools power n8n-MCP's ability to instantly find relevant nodes from n8n's extensive catalog. The `search_nodes` tool transforms the overwhelming task of node discovery into an intuitive, fast experience.

In our final chapter, we'll explore the [workflow management tools](09_workflow_management.md)—the capabilities that let AI assistants directly create, modify, and manage n8n workflows.