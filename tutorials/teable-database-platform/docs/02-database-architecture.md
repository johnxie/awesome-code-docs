---
layout: default
title: "Chapter 2: Database Architecture"
nav_order: 2
has_children: false
parent: "Teable Database Platform"
---

# Chapter 2: Database Architecture

> PostgreSQL optimization, indexing strategies, and high-performance data operations in Teable

## 🎯 Learning Objectives

By the end of this chapter, you'll understand:
- PostgreSQL schema design for multi-dimensional data
- Advanced indexing strategies for complex queries
- Query optimization and execution planning
- Connection pooling and performance monitoring
- Data partitioning and scaling strategies

## 🏗️ PostgreSQL Schema Design

### **Core Table Structure**

Teable uses a flexible schema that supports dynamic tables and fields:

```sql
-- Base table for all records
CREATE TABLE records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_id UUID NOT NULL,
    data JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID,
    version INTEGER DEFAULT 1
);

-- Table metadata
CREATE TABLE tables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    base_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID
);

-- Field definitions
CREATE TABLE fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_id UUID NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    config JSONB DEFAULT '{}',
    order_index INTEGER DEFAULT 0,
    is_computed BOOLEAN DEFAULT FALSE,
    computation JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID
);

-- Views for different data perspectives
CREATE TABLE views (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_id UUID NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) DEFAULT 'grid',
    config JSONB DEFAULT '{}',
    filters JSONB DEFAULT '[]',
    sorts JSONB DEFAULT '[]',
    groupings JSONB DEFAULT '[]',
    field_order JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID,
    updated_by UUID
);
```

### **JSONB for Flexible Data Storage**

PostgreSQL's JSONB type enables dynamic field storage:

```sql
-- Insert flexible record data
INSERT INTO records (table_id, data, created_by)
VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    '{
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "tags": ["developer", "typescript"],
        "metadata": {
            "source": "web_form",
            "campaign": "summer_2024"
        }
    }'::jsonb,
    'user-uuid'
);

-- Query JSONB fields
SELECT
    id,
    data->>'name' as name,
    data->>'email' as email,
    data->'tags' as tags,
    data->'metadata'->>'source' as source
FROM records
WHERE table_id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
  AND data->>'status' = 'active';

-- Update nested JSONB data
UPDATE records
SET data = jsonb_set(data, '{metadata,campaign}', '"winter_2024"')
WHERE id = 'record-uuid';
```

### **Computed Fields and Triggers**

Teable supports dynamic field calculations:

```sql
-- Function for computed field calculations
CREATE OR REPLACE FUNCTION calculate_computed_field(
    record_data JSONB,
    computation JSONB
) RETURNS JSONB AS $$
DECLARE
    result JSONB;
    field_refs TEXT[];
    field_values JSONB := '{}';
BEGIN
    -- Extract referenced field names
    SELECT array_agg(jsonb_object_keys(computation->'references'))
    INTO field_refs
    FROM jsonb_object_keys(computation->'references') AS ref;

    -- Build field values object
    FOREACH ref IN ARRAY field_refs LOOP
        field_values := jsonb_set(field_values, ARRAY[ref], record_data->ref);
    END LOOP;

    -- Execute computation (simplified example)
    CASE computation->>'type'
        WHEN 'formula' THEN
            result := execute_formula(computation->>'expression', field_values);
        WHEN 'concat' THEN
            result := execute_concat(computation->'fields', field_values);
        WHEN 'lookup' THEN
            result := execute_lookup(computation, field_values);
        ELSE
            result := 'null'::jsonb;
    END CASE;

    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update computed fields
CREATE OR REPLACE FUNCTION update_computed_fields()
RETURNS TRIGGER AS $$
DECLARE
    computed_field RECORD;
    new_value JSONB;
BEGIN
    -- Update computed fields for this table
    FOR computed_field IN
        SELECT id, computation
        FROM fields
        WHERE table_id = NEW.table_id
          AND is_computed = true
    LOOP
        new_value := calculate_computed_field(NEW.data, computed_field.computation);
        NEW.data := jsonb_set(NEW.data, ARRAY[computed_field.id::text], new_value);
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to records table
CREATE TRIGGER trigger_update_computed_fields
    BEFORE INSERT OR UPDATE ON records
    FOR EACH ROW EXECUTE FUNCTION update_computed_fields();
```

## 📊 Advanced Indexing Strategies

### **GIN Indexes for JSONB Queries**

```sql
-- GIN index for JSONB data
CREATE INDEX idx_records_data_gin ON records USING GIN (data);

-- Specialized indexes for common query patterns
CREATE INDEX idx_records_data_name ON records ((data->>'name')) WHERE data ? 'name';
CREATE INDEX idx_records_data_email ON records ((data->>'email')) WHERE data ? 'email';
CREATE INDEX idx_records_data_status ON records ((data->>'status')) WHERE data ? 'status';
CREATE INDEX idx_records_data_created_at ON records ((data->>'created_at')) WHERE data ? 'created_at';

-- Index for array operations
CREATE INDEX idx_records_tags ON records USING GIN ((data->'tags')) WHERE jsonb_typeof(data->'tags') = 'array';

-- Index for numeric range queries
CREATE INDEX idx_records_age ON records ((data->>'age')::int) WHERE data ? 'age';

-- Composite index for common filter combinations
CREATE INDEX idx_records_status_priority ON records (
    (data->>'status'),
    (data->>'priority')
) WHERE data ?& array['status', 'priority'];
```

### **Partial Indexes for Performance**

```sql
-- Partial index for active records only
CREATE INDEX idx_records_active_only ON records (table_id, updated_at DESC)
WHERE data->>'status' != 'archived';

-- Partial index for recent records
CREATE INDEX idx_records_recent ON records (table_id, updated_at DESC)
WHERE updated_at > NOW() - INTERVAL '30 days';

-- Partial index for high-priority items
CREATE INDEX idx_records_high_priority ON records (table_id, (data->>'priority'), updated_at DESC)
WHERE data->>'priority' IN ('urgent', 'high');

-- Partial index for records with attachments
CREATE INDEX idx_records_with_attachments ON records USING GIN ((data->'attachments'))
WHERE jsonb_array_length(data->'attachments') > 0;
```

### **Expression Indexes for Computed Values**

```sql
-- Index on computed full name
CREATE INDEX idx_records_full_name ON records (
    ((data->>'first_name') || ' ' || (data->>'last_name'))
) WHERE data ?& array['first_name', 'last_name'];

-- Index on lowercase email for case-insensitive search
CREATE INDEX idx_records_email_lower ON records (lower(data->>'email'))
WHERE data ? 'email';

-- Index on date parts
CREATE INDEX idx_records_created_year ON records (
    EXTRACT(YEAR FROM (data->>'created_at')::timestamp)
) WHERE data ? 'created_at';

CREATE INDEX idx_records_created_month ON records (
    EXTRACT(MONTH FROM (data->>'created_at')::timestamp)
) WHERE data ? 'created_at';
```

### **Index Maintenance and Monitoring**

```sql
-- Monitor index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index bloat analysis
SELECT
    schemaname,
    tablename,
    indexname,
    ROUND(100 * (n_dead_tup::float / n_live_tup), 2) as bloat_ratio
FROM pg_stat_user_indexes
JOIN pg_index ON indexrelid = pg_stat_user_indexes.indexrelid
JOIN pg_class ON relname = tablename
WHERE schemaname = 'public'
  AND n_dead_tup > 0
ORDER BY bloat_ratio DESC;
```

## 🔍 Query Optimization

### **Query Planning and Execution**

Teable optimizes queries based on access patterns:

```typescript
// Query optimizer
class QueryOptimizer {
  private queryAnalyzer: QueryAnalyzer;
  private indexAdvisor: IndexAdvisor;
  private cacheManager: QueryCache;

  async optimizeQuery(query: QuerySpec): Promise<OptimizedQuery> {
    // Analyze query structure
    const analysis = await this.queryAnalyzer.analyze(query);

    // Generate query plan
    const plan = this.generateQueryPlan(analysis);

    // Apply optimizations
    const optimizedPlan = await this.applyOptimizations(plan);

    // Add execution hints
    const hints = this.generateExecutionHints(optimizedPlan);

    return {
      sql: this.generateSQL(optimizedPlan),
      hints,
      estimatedCost: optimizedPlan.cost,
      recommendedIndexes: await this.indexAdvisor.suggestIndexes(query)
    };
  }

  private generateQueryPlan(analysis: QueryAnalysis): QueryPlan {
    const plan: QueryPlan = {
      type: 'select',
      table: analysis.table,
      projections: analysis.fields,
      filters: [],
      sorts: [],
      cost: 0
    };

    // Optimize filter order
    plan.filters = this.optimizeFilterOrder(analysis.filters);

    // Choose optimal join strategy
    if (analysis.joins.length > 0) {
      plan.joins = this.optimizeJoinStrategy(analysis.joins);
    }

    // Optimize sort operations
    if (analysis.sorts.length > 0) {
      plan.sorts = this.optimizeSortOrder(analysis.sorts);
    }

    // Estimate cost
    plan.cost = this.estimateQueryCost(plan);

    return plan;
  }

  private optimizeFilterOrder(filters: Filter[]): Filter[] {
    // Order filters by selectivity and index availability
    return filters.sort((a, b) => {
      const aSelectivity = this.estimateFilterSelectivity(a);
      const bSelectivity = this.estimateFilterSelectivity(b);
      const aHasIndex = this.hasIndexForFilter(a);
      const bHasIndex = this.hasIndexForFilter(b);

      // Prefer indexed filters with higher selectivity
      if (aHasIndex && !bHasIndex) return -1;
      if (!aHasIndex && bHasIndex) return 1;

      return aSelectivity - bSelectivity; // Lower selectivity first
    });
  }

  private estimateFilterSelectivity(filter: Filter): number {
    // Estimate how many rows pass this filter (0-1)
    switch (filter.operator) {
      case 'eq': return 0.01;  // 1% selectivity for equality
      case 'gt':
      case 'lt': return 0.33;  // 33% selectivity for range
      case 'like': return 0.1;  // 10% selectivity for pattern match
      case 'in': return filter.value.length / 100; // Based on IN list size
      default: return 0.5;     // 50% default
    }
  }

  private hasIndexForFilter(filter: Filter): boolean {
    // Check if there's an index for this filter
    const indexKey = `${filter.tableId}.${filter.field}`;
    return this.indexAdvisor.hasIndex(indexKey);
  }

  private estimateQueryCost(plan: QueryPlan): number {
    let cost = 0;

    // Base table scan cost
    cost += this.getTableScanCost(plan.table);

    // Filter costs
    for (const filter of plan.filters) {
      cost += this.hasIndexForFilter(filter) ? 1 : 10; // Index scan vs table scan
    }

    // Sort cost
    if (plan.sorts.length > 0) {
      cost += plan.sorts.length * 5;
    }

    // Join costs
    for (const join of plan.joins || []) {
      cost += this.estimateJoinCost(join);
    }

    return cost;
  }

  private generateSQL(plan: QueryPlan): string {
    let sql = 'SELECT ';

    // Projections
    if (plan.projections.length === 0) {
      sql += '*';
    } else {
      sql += plan.projections.map(p => this.quoteIdentifier(p)).join(', ');
    }

    sql += ` FROM ${this.quoteIdentifier(plan.table)}`;

    // Joins
    if (plan.joins) {
      for (const join of plan.joins) {
        sql += ` ${join.type} JOIN ${this.quoteIdentifier(join.table)}`;
        sql += ` ON ${join.condition}`;
      }
    }

    // Filters
    if (plan.filters.length > 0) {
      const whereClause = plan.filters
        .map(f => this.generateFilterSQL(f))
        .join(' AND ');
      sql += ` WHERE ${whereClause}`;
    }

    // Sorts
    if (plan.sorts.length > 0) {
      const orderClause = plan.sorts
        .map(s => `${this.quoteIdentifier(s.field)} ${s.direction}`)
        .join(', ');
      sql += ` ORDER BY ${orderClause}`;
    }

    // Pagination
    if (plan.limit) {
      sql += ` LIMIT ${plan.limit}`;
    }
    if (plan.offset) {
      sql += ` OFFSET ${plan.offset}`;
    }

    return sql;
  }

  private generateFilterSQL(filter: Filter): string {
    const field = this.quoteIdentifier(filter.field);
    const operator = this.mapOperator(filter.operator);

    if (filter.operator === 'in') {
      const values = filter.value.map(v => this.quoteValue(v)).join(', ');
      return `${field} IN (${values})`;
    }

    const value = this.quoteValue(filter.value);
    return `${field} ${operator} ${value}`;
  }

  private mapOperator(operator: string): string {
    const operatorMap: Record<string, string> = {
      'eq': '=',
      'neq': '!=',
      'gt': '>',
      'gte': '>=',
      'lt': '<',
      'lte': '<=',
      'like': 'ILIKE',
      'contains': '@>',
      'in': 'IN'
    };
    return operatorMap[operator] || operator;
  }

  private quoteIdentifier(identifier: string): string {
    return `"${identifier.replace(/"/g, '""')}"`;
  }

  private quoteValue(value: any): string {
    if (typeof value === 'string') {
      return `'${value.replace(/'/g, "''")}'`;
    }
    return String(value);
  }
}
```

### **Query Result Caching**

```typescript
// Query result caching
class QueryCache {
  private redis: any;
  private localCache: Map<string, CacheEntry> = new Map();

  constructor(redisClient: any) {
    this.redis = redisClient;
  }

  async get(queryKey: string): Promise<any> {
    // Check local cache first
    const localEntry = this.localCache.get(queryKey);
    if (localEntry && !this.isExpired(localEntry)) {
      return localEntry.data;
    }

    // Check Redis cache
    try {
      const redisData = await this.redis.get(`query:${queryKey}`);
      if (redisData) {
        const data = JSON.parse(redisData);
        // Populate local cache
        this.localCache.set(queryKey, {
          data,
          expiry: Date.now() + 300000 // 5 minutes
        });
        return data;
      }
    } catch (error) {
      console.warn('Redis cache error:', error);
    }

    return null;
  }

  async set(queryKey: string, data: any, ttl: number = 300): Promise<void> {
    // Cache locally
    this.localCache.set(queryKey, {
      data,
      expiry: Date.now() + (ttl * 1000)
    });

    // Cache in Redis
    try {
      await this.redis.setex(`query:${queryKey}`, ttl, JSON.stringify(data));
    } catch (error) {
      console.warn('Redis cache set error:', error);
    }
  }

  async invalidate(queryKey: string): Promise<void> {
    this.localCache.delete(queryKey);
    try {
      await this.redis.del(`query:${queryKey}`);
    } catch (error) {
      console.warn('Redis cache delete error:', error);
    }
  }

  private isExpired(entry: CacheEntry): boolean {
    return Date.now() > entry.expiry;
  }

  generateQueryKey(query: QuerySpec): string {
    // Generate deterministic key from query
    const keyData = {
      table: query.table,
      fields: query.fields?.sort(),
      filters: query.filters?.sort((a, b) => a.field.localeCompare(b.field)),
      sorts: query.sorts,
      limit: query.limit,
      offset: query.offset
    };
    return require('crypto').createHash('md5').update(JSON.stringify(keyData)).digest('hex');
  }
}

interface CacheEntry {
  data: any;
  expiry: number;
}
```

## 🔗 Connection Pooling and Management

### **Advanced Connection Pooling**

```typescript
// Connection pool manager
class ConnectionPoolManager {
  private pools: Map<string, Pool> = new Map();
  private healthChecks: Map<string, HealthCheck> = new Map();

  constructor(private poolConfig: PoolConfig) {}

  async getPool(databaseUrl: string): Promise<Pool> {
    if (!this.pools.has(databaseUrl)) {
      const pool = await this.createPool(databaseUrl);
      this.pools.set(databaseUrl, pool);

      // Start health monitoring
      this.startHealthCheck(databaseUrl, pool);
    }

    return this.pools.get(databaseUrl)!;
  }

  private async createPool(databaseUrl: string): Promise<Pool> {
    const pool = new Pool({
      connectionString: databaseUrl,
      max: this.poolConfig.maxConnections,
      min: this.poolConfig.minConnections,
      idleTimeoutMillis: this.poolConfig.idleTimeout,
      connectionTimeoutMillis: this.poolConfig.connectionTimeout,
      acquireTimeoutMillis: this.poolConfig.acquireTimeout,
      ssl: this.poolConfig.ssl
    });

    // Pool event handlers
    pool.on('connect', (client) => {
      console.log('New database connection established');
    });

    pool.on('error', (err, client) => {
      console.error('Unexpected error on idle client', err);
    });

    pool.on('remove', (client) => {
      console.log('Database connection removed from pool');
    });

    return pool;
  }

  private startHealthCheck(databaseUrl: string, pool: Pool): void {
    const healthCheck = setInterval(async () => {
      try {
        const isHealthy = await this.checkPoolHealth(pool);
        this.healthChecks.set(databaseUrl, {
          healthy: isHealthy,
          lastChecked: new Date(),
          responseTime: Date.now() - startTime
        });

        if (!isHealthy) {
          console.warn(`Database pool ${databaseUrl} is unhealthy`);
          await this.recreatePool(databaseUrl);
        }
      } catch (error) {
        console.error(`Health check failed for ${databaseUrl}:`, error);
        this.healthChecks.set(databaseUrl, {
          healthy: false,
          lastChecked: new Date(),
          error: error.message
        });
      }
    }, this.poolConfig.healthCheckInterval);

    this.healthChecks.set(databaseUrl, {
      healthy: true,
      lastChecked: new Date(),
      checkInterval: healthCheck
    });
  }

  private async checkPoolHealth(pool: Pool): Promise<boolean> {
    const client = await pool.connect();
    const startTime = Date.now();

    try {
      await client.query('SELECT 1');
      return true;
    } catch (error) {
      return false;
    } finally {
      client.release();
    }
  }

  private async recreatePool(databaseUrl: string): Promise<void> {
    const oldPool = this.pools.get(databaseUrl);
    if (oldPool) {
      await oldPool.end();
    }

    const newPool = await this.createPool(databaseUrl);
    this.pools.set(databaseUrl, newPool);
  }

  async executeQuery(databaseUrl: string, query: QuerySpec): Promise<QueryResult> {
    const pool = await this.getPool(databaseUrl);
    const client = await pool.connect();

    try {
      const optimizedQuery = await this.queryOptimizer.optimizeQuery(query);
      const startTime = Date.now();

      const result = await client.query(optimizedQuery.sql);

      const executionTime = Date.now() - startTime;

      return {
        rows: result.rows,
        rowCount: result.rowCount,
        executionTime,
        queryPlan: optimizedQuery.hints
      };

    } finally {
      client.release();
    }
  }

  getPoolStats(databaseUrl: string): PoolStats {
    const pool = this.pools.get(databaseUrl);
    const health = this.healthChecks.get(databaseUrl);

    if (!pool) {
      return { status: 'not_found' };
    }

    return {
      status: 'active',
      totalConnections: pool.totalCount,
      idleConnections: pool.idleCount,
      waitingClients: pool.waitingCount,
      health: health ? {
        healthy: health.healthy,
        lastChecked: health.lastChecked,
        responseTime: health.responseTime
      } : null
    };
  }

  async closeAllPools(): Promise<void> {
    const closePromises = Array.from(this.pools.entries()).map(
      ([url, pool]) => pool.end()
    );

    await Promise.all(closePromises);
    this.pools.clear();

    // Clear health check intervals
    for (const health of this.healthChecks.values()) {
      if (health.checkInterval) {
        clearInterval(health.checkInterval);
      }
    }
    this.healthChecks.clear();
  }
}

interface PoolConfig {
  maxConnections: number;
  minConnections: number;
  idleTimeout: number;
  connectionTimeout: number;
  acquireTimeout: number;
  ssl?: boolean | object;
  healthCheckInterval: number;
}

interface HealthCheck {
  healthy: boolean;
  lastChecked: Date;
  responseTime?: number;
  error?: string;
  checkInterval?: NodeJS.Timeout;
}

interface PoolStats {
  status: 'active' | 'not_found';
  totalConnections?: number;
  idleConnections?: number;
  waitingClients?: number;
  health?: {
    healthy: boolean;
    lastChecked: Date;
    responseTime?: number;
  };
}
```

## 📊 Performance Monitoring

### **Database Performance Metrics**

```typescript
// Database performance monitoring
class DatabaseMonitor {
  private metrics: Map<string, QueryMetrics> = new Map();
  private slowQueryThreshold: number = 1000; // 1 second

  recordQueryMetrics(queryId: string, metrics: QueryMetrics): void {
    this.metrics.set(queryId, metrics);

    // Log slow queries
    if (metrics.executionTime > this.slowQueryThreshold) {
      console.warn(`Slow query detected:`, {
        queryId,
        executionTime: metrics.executionTime,
        query: metrics.query.substring(0, 100) + '...',
        timestamp: new Date().toISOString()
      });
    }

    // Clean old metrics (keep last 1000)
    if (this.metrics.size > 1000) {
      const oldestKey = this.metrics.keys().next().value;
      this.metrics.delete(oldestKey);
    }
  }

  getPerformanceStats(timeRange: number = 3600000): PerformanceStats {
    const cutoff = Date.now() - timeRange;
    const recentMetrics = Array.from(this.metrics.values())
      .filter(m => m.timestamp > cutoff);

    const executionTimes = recentMetrics.map(m => m.executionTime);

    return {
      totalQueries: recentMetrics.length,
      averageExecutionTime: executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length,
      medianExecutionTime: this.calculateMedian(executionTimes),
      p95ExecutionTime: this.calculatePercentile(executionTimes, 95),
      p99ExecutionTime: this.calculatePercentile(executionTimes, 99),
      slowQueries: recentMetrics.filter(m => m.executionTime > this.slowQueryThreshold).length,
      queryTypes: this.groupByQueryType(recentMetrics)
    };
  }

  private calculateMedian(values: number[]): number {
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0
      ? (sorted[mid - 1] + sorted[mid]) / 2
      : sorted[mid];
  }

  private calculatePercentile(values: number[], percentile: number): number {
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  private groupByQueryType(metrics: QueryMetrics[]): Record<string, number> {
    const groups: Record<string, number> = {};

    for (const metric of metrics) {
      const type = this.classifyQueryType(metric.query);
      groups[type] = (groups[type] || 0) + 1;
    }

    return groups;
  }

  private classifyQueryType(query: string): string {
    const upperQuery = query.toUpperCase();

    if (upperQuery.includes('SELECT')) return 'SELECT';
    if (upperQuery.includes('INSERT')) return 'INSERT';
    if (upperQuery.includes('UPDATE')) return 'UPDATE';
    if (upperQuery.includes('DELETE')) return 'DELETE';

    return 'OTHER';
  }

  getSlowQueries(limit: number = 10): QueryMetrics[] {
    return Array.from(this.metrics.values())
      .filter(m => m.executionTime > this.slowQueryThreshold)
      .sort((a, b) => b.executionTime - a.executionTime)
      .slice(0, limit);
  }

  getQueryOptimizationSuggestions(): OptimizationSuggestion[] {
    const stats = this.getPerformanceStats();
    const suggestions: OptimizationSuggestion[] = [];

    // Suggest indexing for slow queries
    const slowQueries = this.getSlowQueries(5);
    for (const query of slowQueries) {
      if (this.needsIndex(query)) {
        suggestions.push({
          type: 'add_index',
          description: `Consider adding an index for slow query: ${query.query.substring(0, 50)}...`,
          impact: 'high',
          queryId: query.queryId
        });
      }
    }

    // Suggest query optimization
    if (stats.averageExecutionTime > 500) {
      suggestions.push({
        type: 'optimize_queries',
        description: `Average query time is high (${stats.averageExecutionTime}ms). Consider query optimization.`,
        impact: 'medium'
      });
    }

    return suggestions;
  }

  private needsIndex(queryMetrics: QueryMetrics): boolean {
    // Simple heuristic: queries without WHERE clauses on indexed fields
    const query = queryMetrics.query.toLowerCase();
    return query.includes('where') && !query.includes('indexed_field');
  }
}

interface QueryMetrics {
  queryId: string;
  query: string;
  executionTime: number;
  timestamp: number;
  resultCount: number;
  cacheHit: boolean;
}

interface PerformanceStats {
  totalQueries: number;
  averageExecutionTime: number;
  medianExecutionTime: number;
  p95ExecutionTime: number;
  p99ExecutionTime: number;
  slowQueries: number;
  queryTypes: Record<string, number>;
}

interface OptimizationSuggestion {
  type: string;
  description: string;
  impact: 'low' | 'medium' | 'high';
  queryId?: string;
}
```

## 🧪 Hands-On Exercise

**Estimated Time: 60 minutes**

1. **Database Schema Design**: Create optimized PostgreSQL tables for a Teable-like system
2. **Indexing Strategy**: Implement GIN, partial, and expression indexes for query performance
3. **Query Optimization**: Write and optimize complex queries with proper indexing
4. **Connection Pooling**: Set up and monitor database connection pools
5. **Performance Monitoring**: Implement query metrics and identify optimization opportunities

---

**Ready for real-time collaboration?** Continue to [Chapter 3: Real-Time Collaboration](03-realtime-collaboration.md)