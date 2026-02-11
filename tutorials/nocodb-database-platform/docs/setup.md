# NocoDB Development Environment Setup

## Prerequisites

### Required Software
- **Node.js 18+** with npm
- **Git** for version control
- **Database** (PostgreSQL, MySQL, or SQLite for development)
- **Docker** (optional, for containerized development)

### Recommended Tools
- **VS Code** with Vue.js and Node.js extensions
- **Postman** or similar for API testing
- **Database client** (DBeaver, pgAdmin, or similar)

## Installation Options

### Option 1: Local Development (Recommended)

```bash
# Clone the repository
git clone https://github.com/nocodb/nocodb.git
cd nocodb

# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# Edit .env file with your database credentials
# DB_TYPE=pg (or mysql, sqlite)
# DB_HOST=localhost
# DB_PORT=5432
# DB_USERNAME=your_username
# DB_PASSWORD=your_password
# DB_DATABASE=nocodb_dev

# Run database migrations
npm run migrate

# Start development server
npm run dev
```

### Option 2: Docker Development

```bash
# Clone the repository
git clone https://github.com/nocodb/nocodb.git
cd nocodb

# Start with Docker Compose
docker-compose up -d

# Access the application
# - Web UI: http://localhost:8080
# - API: http://localhost:8080/api/v1
```

## Environment Configuration

### Database Configuration

**PostgreSQL:**
```env
DB_TYPE=pg
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_DATABASE=nocodb_dev
```

**MySQL:**
```env
DB_TYPE=mysql2
DB_HOST=localhost  
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=your_password
DB_DATABASE=nocodb_dev
```

**SQLite (Development Only):**
```env
DB_TYPE=sqlite3
DB_PATH=./nocodb.db
```

### Application Settings

```env
# Application
PORT=8080
NODE_ENV=development

# Security
JWT_SECRET=your_jwt_secret_here
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_admin_password

# File Storage
FILE_STORAGE=local
# Or for cloud storage:
# FILE_STORAGE=s3
# AWS_ACCESS_KEY_ID=your_key
# AWS_SECRET_ACCESS_KEY=your_secret
# AWS_BUCKET=your_bucket
```

## Project Structure Overview

```
nocodb/
├── packages/
│   ├── nc-gui/          # Vue.js frontend
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Route-based page components
│   │   └── store/       # Vuex state management
│   ├── nocodb/          # Node.js backend
│   │   ├── src/
│   │   │   ├── lib/     # Core business logic
│   │   │   ├── models/  # Database models
│   │   │   └── routes/  # API endpoints
│   └── nc-common/       # Shared utilities
├── docker-compose.yml
└── package.json
```

## Verification Steps

### 1. Backend Health Check

```bash
# Check if API server is running
curl http://localhost:8080/api/v1/health

# Should return: {"status": "ok"}
```

### 2. Database Connection

```bash
# Test database connection
npm run test:db

# Should show successful connection message
```

### 3. Frontend Development

```bash
# Start frontend in development mode
cd packages/nc-gui
npm run dev

# Frontend should be available at http://localhost:3000
```

## Development Workflow

### Making Backend Changes

```bash
# Navigate to backend package
cd packages/nocodb

# Install new dependencies
npm install package-name

# Run tests
npm test

# Start backend in watch mode
npm run dev
```

### Making Frontend Changes

```bash
# Navigate to frontend package
cd packages/nc-gui

# Install new dependencies
npm install package-name

# Start development server with hot reload
npm run dev
```

### Database Schema Changes

```bash
# Create new migration
npm run migration:create migration_name

# Run pending migrations
npm run migrate

# Rollback migration
npm run migrate:rollback
```

## Common Development Tasks

### Adding a New Database Connector

1. Create connector class in `src/lib/db/`
2. Implement required interface methods
3. Add tests in `test/unit/db/`
4. Update configuration schema

### Creating Custom Components

1. Add component to `packages/nc-gui/components/`
2. Register in component index
3. Add to Storybook for documentation
4. Write unit tests

### API Endpoint Development

1. Define route in `src/routes/`
2. Implement controller logic
3. Add input validation middleware
4. Write integration tests

## Debugging Setup

### VS Code Configuration

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug NocoDB Backend",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/packages/nocodb/src/index.js",
      "env": {
        "NODE_ENV": "development"
      },
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/packages/nocodb"
    }
  ]
}
```

### Browser DevTools

For frontend debugging:
1. Install Vue.js DevTools extension
2. Enable source maps in Vue config
3. Use browser debugger for component inspection

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9
```

**Database Connection Failed:**
```bash
# Check database status
systemctl status postgresql
# or
systemctl status mysql
```

**Permission Errors:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod -R 755 .
```

**Node Version Issues:**
```bash
# Use Node Version Manager
nvm install 18
nvm use 18
```

## Next Steps

Once your environment is set up:

1. **Explore the UI** - Create your first base and table
2. **Check the API** - Test auto-generated endpoints
3. **Review the Code** - Start with core models and routes
4. **Read Architecture Guide** - [System Overview](../01-system-overview.md)

## Getting Help

- **Setup Issues**: [Open an issue](https://github.com/johnxie/awesome-code-docs/issues) with `[nocodb-setup]` tag
- **NocoDB Community**: [Official Discord](https://discord.gg/5RgZmkW)
- **Development Questions**: [GitHub Discussions](https://github.com/nocodb/nocodb/discussions)

---

**✅ Environment ready? Continue to [System Overview](../01-system-overview.md)**
