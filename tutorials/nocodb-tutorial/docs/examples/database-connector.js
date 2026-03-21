/**
 * NocoDB Database Connector Example
 * 
 * This example demonstrates how NocoDB creates a universal interface
 * for different database systems (PostgreSQL, MySQL, SQLite, etc.)
 * 
 * Key concepts:
 * - Database abstraction layer
 * - Dynamic query generation
 * - Schema introspection
 * - Connection management
 */

const knex = require('knex');

/**
 * Base Database Connector
 * Provides common interface for all database types
 */
class DatabaseConnector {
  constructor(config) {
    this.config = config;
    this.knex = null;
    this.dbType = config.client;
  }

  /**
   * Establish database connection
   */
  async connect() {
    try {
      this.knex = knex(this.config);
      
      // Test connection
      await this.knex.raw('SELECT 1');
      console.log(`✅ Connected to ${this.dbType} database`);
      
      return true;
    } catch (error) {
      console.error(`❌ Database connection failed:`, error.message);
      throw error;
    }
  }

  /**
   * Get all tables in the database
   */
  async getTables() {
    const query = this.getTablesQuery();
    const result = await this.knex.raw(query);
    return this.formatTablesResult(result);
  }

  /**
   * Get columns for a specific table
   */
  async getColumns(tableName) {
    const query = this.getColumnsQuery(tableName);
    const result = await this.knex.raw(query);
    return this.formatColumnsResult(result);
  }

  /**
   * Create a new table with dynamic schema
   */
  async createTable(tableName, columns) {
    return this.knex.schema.createTable(tableName, (table) => {
      columns.forEach(column => {
        this.addColumn(table, column);
      });
    });
  }

  /**
   * Add column to existing table
   */
  async addColumn(tableName, columnDef) {
    return this.knex.schema.alterTable(tableName, (table) => {
      this.addColumn(table, columnDef);
    });
  }

  /**
   * Generate REST API endpoints for a table
   */
  generateAPIRoutes(tableName) {
    const routes = {
      // GET /api/v1/{tableName} - List all records
      list: async (req, res) => {
        const { limit = 25, offset = 0, where, sort } = req.query;
        
        let query = this.knex(tableName);
        
        // Add WHERE conditions
        if (where) {
          query = this.applyWhereConditions(query, JSON.parse(where));
        }
        
        // Add sorting
        if (sort) {
          const sortFields = JSON.parse(sort);
          sortFields.forEach(field => {
            query.orderBy(field.column, field.direction);
          });
        }
        
        // Add pagination
        const records = await query.limit(limit).offset(offset);
        const total = await this.knex(tableName).count('* as count');
        
        res.json({
          records,
          pagination: {
            total: total[0].count,
            limit,
            offset,
            hasMore: offset + records.length < total[0].count
          }
        });
      },

      // GET /api/v1/{tableName}/{id} - Get single record
      get: async (req, res) => {
        const { id } = req.params;
        const record = await this.knex(tableName).where('id', id).first();
        
        if (!record) {
          return res.status(404).json({ error: 'Record not found' });
        }
        
        res.json(record);
      },

      // POST /api/v1/{tableName} - Create new record
      create: async (req, res) => {
        const data = req.body;
        
        // Validate data against schema
        const validationErrors = await this.validateData(tableName, data);
        if (validationErrors.length > 0) {
          return res.status(400).json({ errors: validationErrors });
        }
        
        const [newRecord] = await this.knex(tableName).insert(data).returning('*');
        res.status(201).json(newRecord);
      },

      // PUT /api/v1/{tableName}/{id} - Update record
      update: async (req, res) => {
        const { id } = req.params;
        const data = req.body;
        
        // Validate data
        const validationErrors = await this.validateData(tableName, data, id);
        if (validationErrors.length > 0) {
          return res.status(400).json({ errors: validationErrors });
        }
        
        const [updatedRecord] = await this.knex(tableName)
          .where('id', id)
          .update(data)
          .returning('*');
          
        if (!updatedRecord) {
          return res.status(404).json({ error: 'Record not found' });
        }
        
        res.json(updatedRecord);
      },

      // DELETE /api/v1/{tableName}/{id} - Delete record
      delete: async (req, res) => {
        const { id } = req.params;
        
        const deleted = await this.knex(tableName).where('id', id).del();
        
        if (deleted === 0) {
          return res.status(404).json({ error: 'Record not found' });
        }
        
        res.status(204).send();
      }
    };

    return routes;
  }

  /**
   * Database-specific query methods (implemented in subclasses)
   */
  getTablesQuery() {
    throw new Error('getTablesQuery must be implemented by database-specific connector');
  }

  getColumnsQuery(tableName) {
    throw new Error('getColumnsQuery must be implemented by database-specific connector');
  }

  formatTablesResult(result) {
    throw new Error('formatTablesResult must be implemented by database-specific connector');
  }

  formatColumnsResult(result) {
    throw new Error('formatColumnsResult must be implemented by database-specific connector');
  }

  /**
   * Helper methods
   */
  applyWhereConditions(query, conditions) {
    conditions.forEach(condition => {
      const { column, operator, value } = condition;
      
      switch (operator) {
        case 'eq':
          query.where(column, value);
          break;
        case 'ne':
          query.whereNot(column, value);
          break;
        case 'gt':
          query.where(column, '>', value);
          break;
        case 'gte':
          query.where(column, '>=', value);
          break;
        case 'lt':
          query.where(column, '<', value);
          break;
        case 'lte':
          query.where(column, '<=', value);
          break;
        case 'like':
          query.where(column, 'like', `%${value}%`);
          break;
        case 'in':
          query.whereIn(column, value);
          break;
      }
    });
    
    return query;
  }

  addColumnToTable(table, columnDef) {
    const { name, type, nullable = true, defaultValue } = columnDef;
    
    let column;
    
    switch (type) {
      case 'string':
        column = table.string(name, columnDef.length || 255);
        break;
      case 'integer':
        column = table.integer(name);
        break;
      case 'float':
        column = table.float(name);
        break;
      case 'boolean':
        column = table.boolean(name);
        break;
      case 'date':
        column = table.date(name);
        break;
      case 'datetime':
        column = table.datetime(name);
        break;
      case 'text':
        column = table.text(name);
        break;
      case 'json':
        column = table.json(name);
        break;
      default:
        column = table.string(name);
    }
    
    if (!nullable) {
      column.notNullable();
    }
    
    if (defaultValue !== undefined) {
      column.defaultTo(defaultValue);
    }
    
    return column;
  }

  async validateData(tableName, data, recordId = null) {
    const errors = [];
    const columns = await this.getColumns(tableName);
    
    // Check required fields
    columns.forEach(column => {
      if (!column.nullable && data[column.name] === undefined && !recordId) {
        errors.push(`Field '${column.name}' is required`);
      }
    });
    
    // Validate data types and constraints
    Object.keys(data).forEach(fieldName => {
      const column = columns.find(col => col.name === fieldName);
      const value = data[fieldName];
      
      if (!column) {
        errors.push(`Unknown field '${fieldName}'`);
        return;
      }
      
      // Type validation
      if (value !== null && !this.validateFieldType(column.type, value)) {
        errors.push(`Invalid type for field '${fieldName}'. Expected ${column.type}`);
      }
    });
    
    return errors;
  }

  validateFieldType(expectedType, value) {
    switch (expectedType) {
      case 'integer':
        return Number.isInteger(Number(value));
      case 'float':
        return !isNaN(parseFloat(value));
      case 'boolean':
        return typeof value === 'boolean' || value === 'true' || value === 'false';
      case 'date':
      case 'datetime':
        return !isNaN(Date.parse(value));
      case 'json':
        try {
          if (typeof value === 'object') return true;
          JSON.parse(value);
          return true;
        } catch {
          return false;
        }
      default:
        return true; // String types and others
    }
  }

  async disconnect() {
    if (this.knex) {
      await this.knex.destroy();
      console.log('🔌 Database connection closed');
    }
  }
}

/**
 * PostgreSQL-specific connector
 */
class PostgreSQLConnector extends DatabaseConnector {
  getTablesQuery() {
    return `
      SELECT tablename as table_name 
      FROM pg_tables 
      WHERE schemaname = 'public'
      ORDER BY tablename
    `;
  }

  getColumnsQuery(tableName) {
    return `
      SELECT 
        column_name as name,
        data_type as type,
        is_nullable = 'YES' as nullable,
        column_default as default_value,
        character_maximum_length as max_length
      FROM information_schema.columns 
      WHERE table_name = '${tableName}'
      ORDER BY ordinal_position
    `;
  }

  formatTablesResult(result) {
    return result.rows.map(row => row.table_name);
  }

  formatColumnsResult(result) {
    return result.rows.map(row => ({
      name: row.name,
      type: this.mapPostgreSQLType(row.type),
      nullable: row.nullable,
      defaultValue: row.default_value,
      maxLength: row.max_length
    }));
  }

  mapPostgreSQLType(pgType) {
    const typeMap = {
      'character varying': 'string',
      'varchar': 'string',
      'text': 'text',
      'integer': 'integer',
      'bigint': 'integer',
      'smallint': 'integer',
      'numeric': 'float',
      'real': 'float',
      'double precision': 'float',
      'boolean': 'boolean',
      'date': 'date',
      'timestamp': 'datetime',
      'timestamptz': 'datetime',
      'json': 'json',
      'jsonb': 'json'
    };
    
    return typeMap[pgType] || 'string';
  }
}

/**
 * MySQL-specific connector
 */
class MySQLConnector extends DatabaseConnector {
  getTablesQuery() {
    return `
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = DATABASE()
      ORDER BY table_name
    `;
  }

  getColumnsQuery(tableName) {
    return `
      SELECT 
        column_name as name,
        data_type as type,
        is_nullable = 'YES' as nullable,
        column_default as default_value,
        character_maximum_length as max_length
      FROM information_schema.columns 
      WHERE table_name = '${tableName}' 
        AND table_schema = DATABASE()
      ORDER BY ordinal_position
    `;
  }

  formatTablesResult(result) {
    return result[0].map(row => row.table_name);
  }

  formatColumnsResult(result) {
    return result[0].map(row => ({
      name: row.name,
      type: this.mapMySQLType(row.type),
      nullable: row.nullable,
      defaultValue: row.default_value,
      maxLength: row.max_length
    }));
  }

  mapMySQLType(mysqlType) {
    const typeMap = {
      'varchar': 'string',
      'char': 'string',
      'text': 'text',
      'longtext': 'text',
      'int': 'integer',
      'bigint': 'integer',
      'smallint': 'integer',
      'tinyint': 'boolean',
      'decimal': 'float',
      'float': 'float',
      'double': 'float',
      'date': 'date',
      'datetime': 'datetime',
      'timestamp': 'datetime',
      'json': 'json'
    };
    
    return typeMap[mysqlType] || 'string';
  }
}

/**
 * Factory function to create appropriate connector
 */
function createDatabaseConnector(config) {
  switch (config.client) {
    case 'pg':
    case 'postgresql':
      return new PostgreSQLConnector(config);
    case 'mysql':
    case 'mysql2':
      return new MySQLConnector(config);
    default:
      throw new Error(`Unsupported database type: ${config.client}`);
  }
}

module.exports = {
  DatabaseConnector,
  PostgreSQLConnector,
  MySQLConnector,
  createDatabaseConnector
};

/**
 * Usage Example:
 * 
 * const config = {
 *   client: 'pg',
 *   connection: {
 *     host: 'localhost',
 *     user: 'username',
 *     password: 'password',
 *     database: 'myapp'
 *   }
 * };
 * 
 * const connector = createDatabaseConnector(config);
 * await connector.connect();
 * 
 * const tables = await connector.getTables();
 * console.log('Available tables:', tables);
 * 
 * const routes = connector.generateAPIRoutes('users');
 * // Now you can use routes.list, routes.get, etc. in your Express app
 */
