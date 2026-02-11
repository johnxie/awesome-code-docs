---
layout: default
title: "Chapter 3: Setup Environment"
nav_order: 3
has_children: false
parent: "Teable Database Platform"
---

# Teable Development Environment Setup

## Prerequisites Overview

### System Requirements
- **Operating System**: macOS, Linux, or Windows with WSL2
- **Memory**: Minimum 8GB RAM (16GB recommended for optimal performance)
- **Storage**: 10GB+ free space for development environment
- **Network**: Stable internet connection for package downloads and API testing

### Required Software Stack
- **Node.js 18.x or higher** with npm/yarn package management
- **PostgreSQL 14+** for primary data storage
- **Redis 6+** for caching and real-time features
- **Docker & Docker Compose** for containerized development
- **Git** for version control and repository management

### Recommended Development Tools
- **VS Code** with Teable-specific extensions
- **PostgreSQL Client** (pgAdmin, TablePlus, or similar)
- **Redis CLI** or visual Redis client
- **Postman/Insomnia** for API testing
- **React Developer Tools** browser extension

## Installation Options

### Option 1: Docker Development Environment (Recommended)

**Advantages:**
- Consistent environment across different development machines
- Automatic service orchestration and dependency management
- Isolated development without affecting system packages
- Easy cleanup and environment reset

**Getting Started:**

```bash
# Clone the Teable repository
git clone https://github.com/teableio/teable.git
cd teable

# Copy environment configuration
cp .env.example .env

# Review and configure environment variables
nano .env  # or use your preferred editor

# Start the complete development stack
docker-compose -f docker-compose.dev.yml up -d

# Verify all services are running
docker-compose ps

# View service logs
docker-compose logs -f teable-backend
```

**Service Overview:**
```yaml
# Services started by Docker Compose
services:
  - teable-frontend:3000    # Next.js React application
  - teable-backend:3333     # NestJS API server
  - postgres:5432           # PostgreSQL database
  - redis:6379             # Redis cache and sessions
  - nginx:80               # Reverse proxy and load balancer
```

### Option 2: Local Development Setup

**Advantages:**
- Faster iteration cycles during development
- Direct access to debugging tools and processes
- More control over individual service configuration
- Better performance on development machines

**Backend API Setup:**

```bash
# Navigate to backend directory
cd apps/nestjs-backend

# Install dependencies
npm install

# Configure database connection
cp .env.example .env
# Edit .env with your local PostgreSQL credentials

# Set up database schema
npm run prisma:generate
npm run prisma:migrate:dev

# Seed development data (optional)
npm run prisma:db:seed

# Start development server with hot reload
npm run start:dev

# API will be available at http://localhost:3333
```

**Frontend Application Setup:**

```bash
# In a new terminal, navigate to frontend directory
cd apps/nextjs-app

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local with API endpoint and other settings

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

## Environment Configuration

### PostgreSQL Database Setup

**Using Docker (Recommended):**
```bash
# Start PostgreSQL container
docker run -d \
  --name teable-postgres \
  -e POSTGRES_DB=teable \
  -e POSTGRES_USER=teable \
  -e POSTGRES_PASSWORD=your_secure_password \
  -p 5432:5432 \
  postgres:14

# Verify connection
docker exec -it teable-postgres psql -U teable -d teable
```

**Local Installation:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql-14 postgresql-contrib

# macOS with Homebrew
brew install postgresql@14
brew services start postgresql@14

# Create database and user
createdb teable
createuser -s teable
psql -d teable -c "ALTER USER teable WITH PASSWORD 'your_secure_password';"
```

### Redis Configuration

**Docker Setup:**
```bash
# Start Redis container
docker run -d \
  --name teable-redis \
  -p 6379:6379 \
  redis:6-alpine \
  redis-server --appendonly yes

# Test connection
docker exec -it teable-redis redis-cli ping
# Should return PONG
```

**Local Installation:**
```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server

# macOS with Homebrew
brew install redis
brew services start redis

# Verify installation
redis-cli ping
```

### Environment Variables Configuration

**Backend Environment (.env):**
```bash
# Database Configuration
DATABASE_URL="postgresql://teable:password@localhost:5432/teable"
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=teable
DB_PASSWORD=your_secure_password
DB_DATABASE=teable

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Application Settings
NODE_ENV=development
PORT=3333
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRES_IN=24h

# File Upload Settings
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,pdf,doc,docx,xls,xlsx

# Email Configuration (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# External API Keys (optional)
OPENAI_API_KEY=sk-your-openai-key-here
WEBHOOK_SECRET=your_webhook_secret
```

**Frontend Environment (.env.local):**
```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3333
NEXT_PUBLIC_WS_URL=ws://localhost:3333

# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# Feature Flags
NEXT_PUBLIC_ENABLE_REALTIME=true
NEXT_PUBLIC_ENABLE_AI_FEATURES=false
NEXT_PUBLIC_MAX_UPLOAD_SIZE=10485760

# Analytics (optional)
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id

# Development Settings
NEXT_PUBLIC_DEBUG=true
```

## Development Workflow Setup

### VS Code Configuration

**Required Extensions:**
```json
{
  "recommendations": [
    "bradlc.vscode-tailwindcss",
    "prisma.prisma",
    "ms-vscode.vscode-typescript-next",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

**Settings (.vscode/settings.json):**
```json
{
  "typescript.preferences.includePackageJsonAutoImports": "auto",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "tailwindCSS.experimental.classRegex": [
    "clsx\\(([^)]*)\\)",
    "className={`([^`]*)`}"
  ],
  "prisma.showPrismaDataPlatformNotification": false,
  "files.exclude": {
    "**/node_modules": true,
    "**/.next": true,
    "**/dist": true
  }
}
```

### Database Development Tools

**Prisma Studio (Built-in):**
```bash
# Start Prisma Studio for visual database management
cd apps/nestjs-backend
npx prisma studio

# Opens browser interface at http://localhost:5555
```

**Database Migration Workflow:**
```bash
# Create new migration
npx prisma migrate dev --name add_new_feature

# Reset database (development only)
npx prisma migrate reset

# Deploy to production
npx prisma migrate deploy

# Generate Prisma client after schema changes
npx prisma generate
```

## Verification & Testing

### Health Check Scripts

**Backend Health Check:**
```bash
#!/bin/bash
# Save as scripts/check-backend.sh

echo "Checking backend health..."

# Check database connection
curl -s http://localhost:3333/health/db || echo "❌ Database connection failed"

# Check Redis connection  
curl -s http://localhost:3333/health/redis || echo "❌ Redis connection failed"

# Check API endpoints
curl -s http://localhost:3333/api/v1/health || echo "❌ API health check failed"

echo "✅ Backend health check completed"
```

**Frontend Health Check:**
```bash
#!/bin/bash
# Save as scripts/check-frontend.sh

echo "Checking frontend health..."

# Check if Next.js server is running
curl -s http://localhost:3000 > /dev/null || echo "❌ Frontend server not responding"

# Check if API connection is working
curl -s http://localhost:3000/api/health > /dev/null || echo "❌ Frontend API connection failed"

echo "✅ Frontend health check completed"
```

### Sample Data Setup

**Development Seed Data:**
```typescript
// apps/nestjs-backend/prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Create sample base
  const sampleBase = await prisma.base.create({
    data: {
      name: 'Sample Project Management',
      description: 'A sample base for learning Teable',
      icon: '📊',
    },
  });

  // Create sample table
  const taskTable = await prisma.table.create({
    data: {
      name: 'Tasks',
      baseId: sampleBase.id,
      description: 'Task management table',
    },
  });

  // Create sample fields
  const fields = await Promise.all([
    prisma.field.create({
      data: {
        name: 'Task Name',
        type: 'singleLineText',
        tableId: taskTable.id,
        isPrimary: true,
      },
    }),
    prisma.field.create({
      data: {
        name: 'Status',
        type: 'singleSelect',
        tableId: taskTable.id,
        options: {
          choices: ['Todo', 'In Progress', 'Done'],
          colors: ['red', 'yellow', 'green'],
        },
      },
    }),
    prisma.field.create({
      data: {
        name: 'Due Date',
        type: 'date',
        tableId: taskTable.id,
      },
    }),
  ]);

  console.log('✅ Sample data created successfully');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

**Run Seed Script:**
```bash
cd apps/nestjs-backend
npm run prisma:db:seed
```

## Development Commands

### Essential Commands Reference

```bash
# Backend Development
cd apps/nestjs-backend
npm run start:dev          # Start development server with hot reload
npm run start:debug        # Start with debugging enabled
npm run test               # Run unit tests
npm run test:e2e          # Run end-to-end tests
npm run lint              # Run ESLint
npm run format            # Format code with Prettier

# Frontend Development  
cd apps/nextjs-app
npm run dev               # Start development server
npm run build             # Build for production
npm run start             # Start production server
npm run lint              # Run Next.js linter
npm run type-check        # TypeScript type checking

# Database Management
npx prisma studio         # Visual database editor
npx prisma generate       # Generate Prisma client
npx prisma migrate dev    # Create and apply migration
npx prisma migrate reset  # Reset database (dev only)
npx prisma db push        # Push schema changes (prototyping)

# Docker Commands
docker-compose up -d      # Start all services in background
docker-compose down       # Stop all services
docker-compose logs -f    # Follow logs from all services
docker-compose ps         # List running services
```

## Troubleshooting Common Issues

### Port Conflicts
```bash
# Check what's using port 3000
lsof -i :3000

# Kill process on port
kill -9 $(lsof -ti:3000)

# Use alternative ports in docker-compose.yml
ports:
  - "3001:3000"  # Frontend
  - "3334:3333"  # Backend
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection manually
psql -h localhost -p 5432 -U teable -d teable

# Reset database permissions
sudo -u postgres psql -c "ALTER USER teable CREATEDB;"
```

### Node.js Version Issues
```bash
# Install Node Version Manager (if not installed)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node.js 18
nvm install 18
nvm use 18
nvm alias default 18
```

### Permission Issues (Linux/macOS)
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Fix Docker permissions
sudo usermod -aG docker $USER
# Logout and login again
```

## Performance Optimization for Development

### Database Optimization
```sql
-- Add useful indexes for development
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_records_table_id ON records(table_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_fields_table_id ON fields(table_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_views_table_id ON views(table_id);

-- Configure PostgreSQL for development
-- Add to postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
max_connections = 100
shared_buffers = 256MB
work_mem = 4MB
```

### Redis Optimization
```bash
# Configure Redis for development
# Add to redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

## Next Steps

Once your development environment is running:

1. **Explore the Database Schema** - Use Prisma Studio to understand data relationships
2. **Test API Endpoints** - Use the built-in OpenAPI documentation at `/api/docs`
3. **Examine Frontend Components** - Navigate through the React component structure
4. **Create Your First Table** - Use the web interface to create a sample data table
5. **Review Real-time Features** - Open multiple browser tabs to test collaboration

## Getting Help

- **Setup Issues**: [Open GitHub Issue](https://github.com/johnxie/awesome-code-docs/issues) with `[teable-setup]` tag
- **Development Questions**: [Join Teable Discord](https://discord.gg/teable)
- **Database Problems**: Check PostgreSQL logs with `docker-compose logs postgres`
- **Build Issues**: Clear `node_modules` and rebuild: `rm -rf node_modules && npm install`

---

**✅ Environment Ready? Continue to [System Overview](01-system-overview.md)**

*This setup guide ensures you have a fully functional Teable development environment with all necessary tools and configurations for building scalable database applications.*
