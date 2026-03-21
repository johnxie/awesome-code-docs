/**
 * Teable API Implementation Examples
 * 
 * This file demonstrates core Teable architecture patterns including:
 * - Multi-dimensional data modeling
 * - Real-time collaboration features
 * - Advanced query system implementation
 * - Dynamic field type handling
 * - Performance optimization patterns
 * 
 * Part of the Teable Database Platform Deep Dive Tutorial
 */

import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { Server, Socket } from 'socket.io';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { 
  CreateTableDto, 
  CreateFieldDto, 
  CreateRecordDto,
  UpdateRecordDto,
  QueryRecordsDto,
  FieldType,
  ViewType 
} from '../dto';

// =============================================================================
// Core Data Models & Types
// =============================================================================

interface TeableField {
  id: string;
  name: string;
  type: FieldType;
  tableId: string;
  isPrimary?: boolean;
  isRequired?: boolean;
  options?: FieldOptions;
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}

interface FieldOptions {
  // Single/Multi Select Options
  choices?: string[];
  colors?: string[];
  
  // Number Field Options
  precision?: number;
  format?: 'number' | 'currency' | 'percentage';
  
  // Date/Time Options
  dateFormat?: 'YYYY-MM-DD' | 'MM/DD/YYYY' | 'DD/MM/YYYY';
  includeTime?: boolean;
  timeZone?: string;
  
  // Formula Field Options
  formula?: string;
  dependencies?: string[];
  
  // Relationship Options
  linkedTableId?: string;
  relationshipType?: 'oneToMany' | 'manyToOne' | 'manyToMany';
  symmetricField?: string;
}

interface TeableRecord {
  id: string;
  tableId: string;
  fields: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
  lastModifiedBy: string;
}

interface QueryBuilder {
  filters: FilterCondition[];
  sorts: SortCondition[];
  groupBy?: string[];
  limit?: number;
  offset?: number;
}

interface FilterCondition {
  fieldId: string;
  operator: 'equals' | 'contains' | 'greaterThan' | 'lessThan' | 'in' | 'isNull' | 'isNotNull';
  value: any;
  logicalOperator?: 'AND' | 'OR';
}

interface SortCondition {
  fieldId: string;
  direction: 'asc' | 'desc';
}

// =============================================================================
// Table Management Controller
// =============================================================================

@Controller('api/v1/tables')
@UseGuards(JwtAuthGuard)
export class TableController {
  constructor(private prisma: PrismaService) {}

  @Post()
  async createTable(@Body() createTableDto: CreateTableDto) {
    const { name, description, baseId, icon } = createTableDto;

    // Create table with transaction to ensure consistency
    const result = await this.prisma.$transaction(async (tx) => {
      // Create the table
      const table = await tx.table.create({
        data: {
          name,
          description,
          baseId,
          icon,
        },
      });

      // Create default primary field
      const primaryField = await tx.field.create({
        data: {
          name: 'Name',
          type: FieldType.SINGLE_LINE_TEXT,
          tableId: table.id,
          isPrimary: true,
          isRequired: true,
        },
      });

      // Create default grid view
      const defaultView = await tx.view.create({
        data: {
          name: 'Grid',
          type: ViewType.GRID,
          tableId: table.id,
          isDefault: true,
          configuration: {
            fieldOrder: [primaryField.id],
            fieldWidths: { [primaryField.id]: 200 },
            showRowNumbers: true,
          },
        },
      });

      return { table, primaryField, defaultView };
    });

    return {
      success: true,
      data: result.table,
      message: 'Table created successfully',
    };
  }

  @Get(':tableId/schema')
  async getTableSchema(@Param('tableId') tableId: string) {
    // Get table with all fields and relationships
    const table = await this.prisma.table.findUnique({
      where: { id: tableId },
      include: {
        fields: {
          orderBy: { order: 'asc' },
        },
        views: {
          orderBy: { order: 'asc' },
        },
        _count: {
          select: { records: true },
        },
      },
    });

    if (!table) {
      throw new Error('Table not found');
    }

    // Transform fields with computed properties
    const fieldsWithMeta = await Promise.all(
      table.fields.map(async (field) => {
        const fieldMeta = await this.getFieldMetadata(field);
        return {
          ...field,
          ...fieldMeta,
        };
      })
    );

    return {
      ...table,
      fields: fieldsWithMeta,
      recordCount: table._count.records,
    };
  }

  private async getFieldMetadata(field: TeableField) {
    const metadata: any = {
      canEdit: true,
      canDelete: !field.isPrimary,
      hasValidation: field.isRequired || Boolean(field.options),
    };

    // Add field-specific metadata
    switch (field.type) {
      case FieldType.FORMULA:
        metadata.isComputed = true;
        metadata.dependencies = field.options?.dependencies || [];
        break;
        
      case FieldType.LOOKUP:
        metadata.isLinked = true;
        metadata.sourceTable = field.options?.linkedTableId;
        break;
        
      case FieldType.ROLLUP:
        metadata.isAggregated = true;
        metadata.aggregateFunction = field.options?.aggregateFunction;
        break;
    }

    return metadata;
  }
}

// =============================================================================
// Dynamic Field Management
// =============================================================================

@Controller('api/v1/fields')
@UseGuards(JwtAuthGuard)
export class FieldController {
  constructor(private prisma: PrismaService) {}

  @Post()
  async createField(@Body() createFieldDto: CreateFieldDto) {
    const { name, type, tableId, options, description } = createFieldDto;

    // Validate field type and options
    await this.validateFieldConfiguration(type, options);

    // Get the next order position
    const maxOrder = await this.prisma.field.aggregate({
      where: { tableId },
      _max: { order: true },
    });

    const field = await this.prisma.field.create({
      data: {
        name,
        type,
        tableId,
        options: options || {},
        description,
        order: (maxOrder._max.order || 0) + 1,
      },
    });

    // Handle field creation side effects
    await this.handleFieldCreationEffects(field);

    return {
      success: true,
      data: field,
      message: 'Field created successfully',
    };
  }

  private async validateFieldConfiguration(type: FieldType, options?: FieldOptions) {
    switch (type) {
      case FieldType.SINGLE_SELECT:
      case FieldType.MULTIPLE_SELECT:
        if (!options?.choices || options.choices.length === 0) {
          throw new Error('Select fields must have at least one choice');
        }
        break;

      case FieldType.FORMULA:
        if (!options?.formula) {
          throw new Error('Formula field must have a formula expression');
        }
        // Validate formula syntax
        await this.validateFormulaExpression(options.formula);
        break;

      case FieldType.LOOKUP:
        if (!options?.linkedTableId) {
          throw new Error('Lookup field must specify a linked table');
        }
        break;
    }
  }

  private async validateFormulaExpression(formula: string) {
    // Basic formula validation - in production, use a proper parser
    const allowedFunctions = ['SUM', 'COUNT', 'AVERAGE', 'MAX', 'MIN', 'CONCAT', 'IF'];
    const functionPattern = /([A-Z_]+)\s*\(/g;
    
    let match;
    while ((match = functionPattern.exec(formula)) !== null) {
      const functionName = match[1];
      if (!allowedFunctions.includes(functionName)) {
        throw new Error(`Unknown function: ${functionName}`);
      }
    }
  }

  private async handleFieldCreationEffects(field: TeableField) {
    // If it's a formula field, calculate initial values for existing records
    if (field.type === FieldType.FORMULA) {
      await this.recalculateFormulaField(field.id);
    }

    // If it's a lookup field, establish the relationship
    if (field.type === FieldType.LOOKUP) {
      await this.establishLookupRelationship(field);
    }

    // Update any dependent fields
    await this.updateDependentFields(field.tableId, field.id);
  }

  private async recalculateFormulaField(fieldId: string) {
    // Implementation for formula calculation would go here
    // This is a complex topic involving expression parsing and evaluation
  }

  private async establishLookupRelationship(field: TeableField) {
    // Create bidirectional relationship if needed
  }

  private async updateDependentFields(tableId: string, fieldId: string) {
    // Find and update any fields that depend on this field
  }
}

// =============================================================================
// Advanced Query System
// =============================================================================

@Controller('api/v1/records')
@UseGuards(JwtAuthGuard)
export class RecordController {
  constructor(private prisma: PrismaService) {}

  @Get('table/:tableId')
  async queryRecords(
    @Param('tableId') tableId: string,
    @Query() queryDto: QueryRecordsDto
  ) {
    const {
      filters = [],
      sorts = [],
      groupBy,
      limit = 50,
      offset = 0,
      fieldIds,
      viewId,
    } = queryDto;

    // Build dynamic query
    const queryBuilder = new TeableQueryBuilder(this.prisma);
    
    // Apply filters
    let whereClause = { tableId };
    if (filters.length > 0) {
      whereClause = {
        ...whereClause,
        ...queryBuilder.buildFilterClause(filters),
      };
    }

    // Build select clause
    const selectClause = fieldIds
      ? this.buildSelectClause(fieldIds)
      : this.buildDefaultSelectClause();

    // Execute query with performance optimization
    const [records, totalCount] = await Promise.all([
      this.prisma.record.findMany({
        where: whereClause,
        select: selectClause,
        orderBy: queryBuilder.buildSortClause(sorts),
        skip: offset,
        take: limit,
      }),
      this.prisma.record.count({ where: whereClause }),
    ]);

    // Post-process records (calculate formulas, format values)
    const processedRecords = await this.postProcessRecords(records, tableId);

    return {
      data: processedRecords,
      meta: {
        totalCount,
        hasMore: offset + limit < totalCount,
        offset,
        limit,
      },
    };
  }

  @Post('table/:tableId')
  async createRecord(
    @Param('tableId') tableId: string,
    @Body() createRecordDto: CreateRecordDto
  ) {
    const { fields } = createRecordDto;

    // Validate field values
    await this.validateRecordFields(tableId, fields);

    // Create record with transaction
    const record = await this.prisma.$transaction(async (tx) => {
      const newRecord = await tx.record.create({
        data: {
          tableId,
          fields: fields,
        },
      });

      // Trigger field calculations and updates
      await this.triggerFieldUpdates(tx, newRecord);

      return newRecord;
    });

    // Emit real-time update
    this.emitRecordChange('create', record);

    return {
      success: true,
      data: record,
      message: 'Record created successfully',
    };
  }

  private buildSelectClause(fieldIds: string[]) {
    // Build optimized select clause based on requested fields
    const selectClause: any = {
      id: true,
      createdAt: true,
      updatedAt: true,
    };

    // Only select requested field data
    selectClause.fields = {
      select: fieldIds.reduce((acc, fieldId) => {
        acc[fieldId] = true;
        return acc;
      }, {}),
    };

    return selectClause;
  }

  private buildDefaultSelectClause() {
    return {
      id: true,
      fields: true,
      createdAt: true,
      updatedAt: true,
    };
  }

  private async postProcessRecords(records: any[], tableId: string) {
    // Get table schema for processing
    const fields = await this.prisma.field.findMany({
      where: { tableId },
    });

    const fieldMap = new Map(fields.map(f => [f.id, f]));

    return records.map(record => {
      const processedFields = {};

      for (const [fieldId, value] of Object.entries(record.fields)) {
        const field = fieldMap.get(fieldId);
        if (field) {
          processedFields[fieldId] = this.formatFieldValue(field, value);
        }
      }

      return {
        ...record,
        fields: processedFields,
      };
    });
  }

  private formatFieldValue(field: TeableField, value: any) {
    switch (field.type) {
      case FieldType.DATE:
        return value ? new Date(value).toISOString().split('T')[0] : null;
        
      case FieldType.CURRENCY:
        return value ? `$${parseFloat(value).toFixed(2)}` : null;
        
      case FieldType.PERCENT:
        return value ? `${(parseFloat(value) * 100).toFixed(2)}%` : null;
        
      case FieldType.FORMULA:
        // Formula values are pre-calculated and stored
        return value;
        
      default:
        return value;
    }
  }

  private async validateRecordFields(tableId: string, fields: Record<string, any>) {
    const tableFields = await this.prisma.field.findMany({
      where: { tableId },
    });

    for (const field of tableFields) {
      const value = fields[field.id];

      // Check required fields
      if (field.isRequired && (value === null || value === undefined || value === '')) {
        throw new Error(`Field "${field.name}" is required`);
      }

      // Validate field type
      if (value !== null && value !== undefined) {
        await this.validateFieldValue(field, value);
      }
    }
  }

  private async validateFieldValue(field: TeableField, value: any) {
    switch (field.type) {
      case FieldType.NUMBER:
        if (typeof value !== 'number') {
          throw new Error(`Field "${field.name}" must be a number`);
        }
        break;

      case FieldType.SINGLE_SELECT:
        if (!field.options?.choices?.includes(value)) {
          throw new Error(`Invalid choice for field "${field.name}"`);
        }
        break;

      case FieldType.MULTIPLE_SELECT:
        if (!Array.isArray(value) || !value.every(v => field.options?.choices?.includes(v))) {
          throw new Error(`Invalid choices for field "${field.name}"`);
        }
        break;

      case FieldType.EMAIL:
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          throw new Error(`Invalid email format for field "${field.name}"`);
        }
        break;
    }
  }

  private async triggerFieldUpdates(tx: any, record: TeableRecord) {
    // Update any formula fields that depend on this record
    const formulaFields = await tx.field.findMany({
      where: {
        tableId: record.tableId,
        type: FieldType.FORMULA,
      },
    });

    for (const field of formulaFields) {
      await this.updateFormulaField(tx, field, record);
    }
  }

  private async updateFormulaField(tx: any, field: TeableField, record: TeableRecord) {
    // Calculate formula value - this would involve parsing and evaluating the formula
    const formulaValue = await this.calculateFormula(field.options?.formula, record);
    
    // Update the record with calculated value
    await tx.record.update({
      where: { id: record.id },
      data: {
        fields: {
          ...record.fields,
          [field.id]: formulaValue,
        },
      },
    });
  }

  private async calculateFormula(formula: string, record: TeableRecord): Promise<any> {
    // This is a simplified example - production would use a proper formula engine
    // Parse and evaluate the formula with the record context
    return 'CALCULATED_VALUE';
  }

  private emitRecordChange(action: string, record: TeableRecord) {
    // Emit to WebSocket for real-time updates
    // This would be handled by the WebSocket gateway
  }
}

// =============================================================================
// Query Builder Helper
// =============================================================================

class TeableQueryBuilder {
  constructor(private prisma: PrismaService) {}

  buildFilterClause(filters: FilterCondition[]) {
    const conditions = filters.map(filter => this.buildSingleFilter(filter));
    
    // Group by logical operator
    const andConditions = conditions.filter(c => c.operator !== 'OR');
    const orConditions = conditions.filter(c => c.operator === 'OR');

    if (andConditions.length > 0 && orConditions.length > 0) {
      return {
        AND: andConditions,
        OR: orConditions,
      };
    } else if (orConditions.length > 0) {
      return { OR: orConditions };
    } else {
      return { AND: andConditions };
    }
  }

  private buildSingleFilter(filter: FilterCondition) {
    const { fieldId, operator, value } = filter;

    switch (operator) {
      case 'equals':
        return { [`fields.${fieldId}`]: { equals: value } };
        
      case 'contains':
        return { [`fields.${fieldId}`]: { contains: value, mode: 'insensitive' } };
        
      case 'greaterThan':
        return { [`fields.${fieldId}`]: { gt: value } };
        
      case 'lessThan':
        return { [`fields.${fieldId}`]: { lt: value } };
        
      case 'in':
        return { [`fields.${fieldId}`]: { in: value } };
        
      case 'isNull':
        return { [`fields.${fieldId}`]: null };
        
      case 'isNotNull':
        return { [`fields.${fieldId}`]: { not: null } };
        
      default:
        throw new Error(`Unknown filter operator: ${operator}`);
    }
  }

  buildSortClause(sorts: SortCondition[]) {
    return sorts.map(sort => ({
      [`fields.${sort.fieldId}`]: sort.direction,
    }));
  }
}

// =============================================================================
// Real-time Collaboration WebSocket Gateway
// =============================================================================

@WebSocketGateway({
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  },
  namespace: '/realtime',
})
export class RealtimeGateway {
  @WebSocketServer()
  server: Server;

  private userSessions = new Map<string, Set<string>>(); // userId -> socketIds
  private tableSubscriptions = new Map<string, Set<string>>(); // tableId -> socketIds

  @SubscribeMessage('joinTable')
  async handleJoinTable(
    @MessageBody() data: { tableId: string; userId: string },
    @ConnectedSocket() client: Socket,
  ) {
    const { tableId, userId } = data;

    // Join table room
    client.join(`table:${tableId}`);

    // Track user session
    if (!this.userSessions.has(userId)) {
      this.userSessions.set(userId, new Set());
    }
    this.userSessions.get(userId)!.add(client.id);

    // Track table subscription
    if (!this.tableSubscriptions.has(tableId)) {
      this.tableSubscriptions.set(tableId, new Set());
    }
    this.tableSubscriptions.get(tableId)!.add(client.id);

    // Notify other users
    client.to(`table:${tableId}`).emit('userJoined', {
      userId,
      timestamp: new Date().toISOString(),
    });

    // Send current online users
    const onlineUsers = this.getOnlineUsersForTable(tableId);
    client.emit('onlineUsers', onlineUsers);
  }

  @SubscribeMessage('recordUpdate')
  async handleRecordUpdate(
    @MessageBody() data: {
      tableId: string;
      recordId: string;
      fieldId: string;
      value: any;
      userId: string;
    },
    @ConnectedSocket() client: Socket,
  ) {
    const { tableId, recordId, fieldId, value, userId } = data;

    // Broadcast to all other users in the table
    client.to(`table:${tableId}`).emit('recordChanged', {
      recordId,
      fieldId,
      value,
      userId,
      timestamp: new Date().toISOString(),
      type: 'update',
    });

    // Implement operational transform for conflict resolution
    await this.handleOperationalTransform(data);
  }

  @SubscribeMessage('cursorPosition')
  async handleCursorPosition(
    @MessageBody() data: {
      tableId: string;
      recordId: string;
      fieldId: string;
      userId: string;
      position: { x: number; y: number };
    },
    @ConnectedSocket() client: Socket,
  ) {
    // Broadcast cursor position to other users
    client.to(`table:${data.tableId}`).emit('cursorMoved', {
      ...data,
      timestamp: new Date().toISOString(),
    });
  }

  private async handleOperationalTransform(updateData: any) {
    // Implement conflict resolution using operational transforms
    // This is a complex algorithm that ensures consistency across concurrent edits
    
    // 1. Get current server state
    // 2. Apply transformation rules
    // 3. Resolve conflicts
    // 4. Broadcast resolved state
  }

  private getOnlineUsersForTable(tableId: string): string[] {
    const socketIds = this.tableSubscriptions.get(tableId) || new Set();
    const userIds = new Set<string>();

    for (const [userId, userSockets] of this.userSessions.entries()) {
      for (const socketId of userSockets) {
        if (socketIds.has(socketId)) {
          userIds.add(userId);
          break;
        }
      }
    }

    return Array.from(userIds);
  }

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);

    // Clean up user sessions
    for (const [userId, sockets] of this.userSessions.entries()) {
      sockets.delete(client.id);
      if (sockets.size === 0) {
        this.userSessions.delete(userId);
      }
    }

    // Clean up table subscriptions
    for (const [tableId, sockets] of this.tableSubscriptions.entries()) {
      sockets.delete(client.id);
      if (sockets.size === 0) {
        this.tableSubscriptions.delete(tableId);
      } else {
        // Notify remaining users
        this.server.to(`table:${tableId}`).emit('userLeft', {
          timestamp: new Date().toISOString(),
        });
      }
    }
  }
}

// =============================================================================
// Field Type Enums and Constants
// =============================================================================

export enum FieldType {
  SINGLE_LINE_TEXT = 'singleLineText',
  LONG_TEXT = 'longText',
  NUMBER = 'number',
  CURRENCY = 'currency',
  PERCENT = 'percent',
  DATE = 'date',
  DATETIME = 'datetime',
  SINGLE_SELECT = 'singleSelect',
  MULTIPLE_SELECT = 'multipleSelect',
  CHECKBOX = 'checkbox',
  EMAIL = 'email',
  URL = 'url',
  PHONE = 'phone',
  ATTACHMENT = 'attachment',
  FORMULA = 'formula',
  LOOKUP = 'lookup',
  ROLLUP = 'rollup',
  CREATED_TIME = 'createdTime',
  MODIFIED_TIME = 'modifiedTime',
  CREATED_BY = 'createdBy',
  MODIFIED_BY = 'modifiedBy',
  AUTO_NUMBER = 'autoNumber',
}

export enum ViewType {
  GRID = 'grid',
  KANBAN = 'kanban',
  GALLERY = 'gallery',
  CALENDAR = 'calendar',
  FORM = 'form',
}

// =============================================================================
// Usage Examples and Integration Tests
// =============================================================================

/**
 * Example usage of the Teable API
 */
export class TeableApiUsageExamples {
  constructor(private apiClient: any) {}

  async demonstrateCompleteWorkflow() {
    // 1. Create a new base
    const base = await this.apiClient.post('/api/v1/bases', {
      name: 'Project Management',
      description: 'Sample project management base',
    });

    // 2. Create a table
    const table = await this.apiClient.post('/api/v1/tables', {
      name: 'Tasks',
      baseId: base.id,
      icon: '✅',
    });

    // 3. Add custom fields
    const statusField = await this.apiClient.post('/api/v1/fields', {
      name: 'Status',
      type: FieldType.SINGLE_SELECT,
      tableId: table.id,
      options: {
        choices: ['Todo', 'In Progress', 'Done'],
        colors: ['red', 'yellow', 'green'],
      },
    });

    const priorityField = await this.apiClient.post('/api/v1/fields', {
      name: 'Priority',
      type: FieldType.NUMBER,
      tableId: table.id,
      options: {
        format: 'number',
      },
    });

    // 4. Create records
    const records = await Promise.all([
      this.apiClient.post(`/api/v1/records/table/${table.id}`, {
        fields: {
          [table.primaryField.id]: 'Design new UI',
          [statusField.id]: 'In Progress',
          [priorityField.id]: 1,
        },
      }),
      this.apiClient.post(`/api/v1/records/table/${table.id}`, {
        fields: {
          [table.primaryField.id]: 'Write documentation',
          [statusField.id]: 'Todo',
          [priorityField.id]: 2,
        },
      }),
    ]);

    // 5. Query records with filters and sorting
    const filteredRecords = await this.apiClient.get(
      `/api/v1/records/table/${table.id}`,
      {
        params: {
          filters: JSON.stringify([
            {
              fieldId: statusField.id,
              operator: 'equals',
              value: 'In Progress',
            },
          ]),
          sorts: JSON.stringify([
            {
              fieldId: priorityField.id,
              direction: 'asc',
            },
          ]),
        },
      }
    );

    console.log('Complete workflow demonstrated successfully');
    return { base, table, records: filteredRecords.data };
  }
}
