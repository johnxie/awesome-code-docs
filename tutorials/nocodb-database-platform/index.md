---
layout: default
title: "NocoDB Database Platform"
nav_order: 38
has_children: true
---

# NocoDB: Deep Dive Tutorial

> **Project**: [NocoDB](https://github.com/nocodb/nocodb) — An open-source Airtable alternative that turns any database into a smart spreadsheet.

[![Stars](https://img.shields.io/github/stars/nocodb/nocodb?style=social)](https://github.com/nocodb/nocodb)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Node.js](https://img.shields.io/badge/Node.js-Vue.js-green)](https://github.com/nocodb/nocodb)

## What Is NocoDB?

NocoDB transforms any SQL database (MySQL, PostgreSQL, SQL Server, SQLite) into a spreadsheet-like interface with auto-generated REST APIs. It provides a no-code layer over existing databases, enabling teams to build applications without rewriting their data layer.

| Feature | Description |
|---------|-------------|
| **Database Abstraction** | Connect to MySQL, PostgreSQL, SQL Server, SQLite |
| **Spreadsheet UI** | Grid, gallery, kanban, and form views |
| **Auto REST API** | Automatic API generation from database schema |
| **Collaboration** | Real-time multi-user editing with roles and permissions |
| **Plugin System** | Extensible with custom field types and integrations |
| **Self-Hosted** | Full Docker deployment, data stays on your infrastructure |

## Architecture Overview

```mermaid
graph TB
    subgraph Frontend["Vue.js Frontend"]
        GRID[Grid View]
        GALLERY[Gallery View]
        KANBAN[Kanban View]
        FORM[Form Builder]
    end

    subgraph Backend["Node.js Backend"]
        API[REST API Engine]
        QB[Query Builder]
        SCHEMA[Schema Manager]
        AUTH[Auth & Roles]
    end

    subgraph Databases["Connected Databases"]
        PG[(PostgreSQL)]
        MYSQL[(MySQL)]
        SQLITE[(SQLite)]
        MSSQL[(SQL Server)]
    end

    Frontend --> Backend
    Backend --> Databases
```

## Tutorial Structure

| Chapter | Topic | What You'll Learn |
|---------|-------|-------------------|
| [1. System Overview](01-system-overview.md) | Architecture | NocoDB's approach to database abstraction |
| [2. Database Abstraction](02-database-abstraction.md) | Connectors | Multi-database support and schema mapping |
| [3. Schema Management](03-schema-management.md) | Data Model | Dynamic table/field handling and migrations |
| [4. API Generation](04-api-generation.md) | APIs | Automatic REST endpoint creation |
| [5. Query Builder](05-query-builder.md) | Querying | Translating UI/API filters into SQL safely |
| [6. Auth System](06-auth-system.md) | Security | Authentication, RBAC, and auditability |
| [7. Vue Components](07-vue-components.md) | Frontend | Grid/editor component architecture |
| [8. Realtime Features](08-realtime-features.md) | Collaboration | Event streams, optimistic updates, and conflict handling |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Node.js, Express, Knex.js |
| **Frontend** | Vue.js, Nuxt |
| **Databases** | PostgreSQL, MySQL, SQLite, SQL Server |
| **Auth** | JWT, role-based access control |
| **Deployment** | Docker, npm |

---

Ready to begin? Start with [Chapter 1: System Overview](01-system-overview.md).

---

*Built with insights from the [NocoDB repository](https://github.com/nocodb/nocodb) and community documentation.*
