---
layout: default
title: "Plane Tutorial - Chapter 1: Getting Started"
nav_order: 1
has_children: false
parent: Plane Tutorial
---

# Chapter 1: Getting Started

Welcome to **Chapter 1** of the **Plane Tutorial**. This chapter walks you through installing Plane, creating your first workspace, and setting up a project. By the end, you will have a running Plane instance ready for issue tracking and project management.

> Install Plane, create a workspace, and launch your first project in minutes.

## What Problem Does This Solve?

Teams need a project management tool they can control. SaaS solutions like Jira and Linear lock you into their infrastructure and pricing. Plane gives you a full-featured PM platform you can self-host, customize, and extend — without vendor lock-in.

## Installation Options

### Docker Compose (Recommended)

The fastest way to get Plane running locally is with Docker Compose. Plane ships an official `docker-compose.yml` that bundles all services.

```bash
# Clone the Plane repository
git clone https://github.com/makeplane/plane.git
cd plane

# Copy the environment template
cp .env.example .env

# Start all services (web, API, worker, database, redis)
docker compose up -d
```

This starts the following services:

| Service | Port | Description |
|:--------|:-----|:------------|
| **Web (Next.js)** | 3000 | Frontend application |
| **API (Django)** | 8000 | Backend REST API |
| **Worker (Celery)** | — | Background task processing |
| **PostgreSQL** | 5432 | Primary database |
| **Redis** | 6379 | Cache and message broker |
| **MinIO** | 9000 | Object storage for attachments |

### Environment Configuration

The `.env` file controls all service configuration. Key variables to set:

```bash
# .env — Core configuration
# ----------------------------

# Database
PGHOST=plane-db
PGDATABASE=plane
POSTGRES_USER=plane
POSTGRES_PASSWORD=plane
POSTGRES_DB=plane
DATABASE_URL=postgresql://plane:plane@plane-db:5432/plane

# Redis
REDIS_HOST=plane-redis
REDIS_PORT=6379
REDIS_URL=redis://plane-redis:6379/

# Application
SECRET_KEY=your-secret-key-here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
WEB_URL=http://localhost:3000

# Storage (MinIO)
AWS_S3_BUCKET_NAME=uploads
AWS_ACCESS_KEY_ID=access-key
AWS_SECRET_ACCESS_KEY=secret-key
AWS_S3_ENDPOINT_URL=http://plane-minio:9000
```

### Local Development Setup

If you want to develop on Plane itself, run the backend and frontend separately.

#### Backend (Django)

```bash
# Navigate to the API server directory
cd apiserver

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver 0.0.0.0:8000
```

#### Frontend (Next.js)

```bash
# Navigate to the web app directory
cd web

# Install dependencies
yarn install

# Start the development server
yarn dev
```

The frontend will be available at `http://localhost:3000`.

## Creating Your First Workspace

Once Plane is running, open your browser and navigate to the web URL. You will be guided through onboarding.

### Step 1: Sign Up

Create your admin account. In self-hosted mode, the first user becomes the workspace owner.

### Step 2: Create a Workspace

A **Workspace** is the top-level container in Plane. It represents your organization or team.

```
Workspace
  ├── Project A
  │     ├── Issues
  │     ├── Cycles
  │     ├── Modules
  │     └── Pages
  ├── Project B
  └── Settings
```

### Step 3: Create a Project

Inside your workspace, create your first project. Each project has its own:

- **Issue tracker** with states, labels, and priorities
- **Cycles** for sprint planning
- **Modules** for feature grouping
- **Pages** for documentation and wiki

### Step 4: Invite Team Members

Plane supports role-based access control:

| Role | Permissions |
|:-----|:------------|
| **Owner** | Full workspace control |
| **Admin** | Manage projects and members |
| **Member** | Create and manage issues |
| **Guest** | View-only access |

## How It Works Under the Hood

When you create a workspace or project, the Django backend processes the request through a layered architecture.

```mermaid
sequenceDiagram
    participant U as User Browser
    participant W as Next.js Web App
    participant A as Django API
    participant DB as PostgreSQL
    participant R as Redis

    U->>W: Create Workspace
    W->>A: POST /api/v1/workspaces/
    A->>DB: INSERT workspace record
    A->>R: Cache workspace metadata
    A-->>W: 201 Created (workspace JSON)
    W-->>U: Redirect to workspace dashboard

    U->>W: Create Project
    W->>A: POST /api/v1/workspaces/{slug}/projects/
    A->>DB: INSERT project + default states
    A->>DB: INSERT default labels
    A-->>W: 201 Created (project JSON)
    W-->>U: Show project board
```

### Django Model: Workspace

The workspace model is the root entity in the Plane data model:

```python
# apiserver/plane/db/models/workspace.py

class Workspace(BaseModel):
    name = models.CharField(max_length=80)
    logo = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=48, unique=True)
    owner = models.ForeignKey(
        "db.User",
        on_delete=models.CASCADE,
        related_name="owner_workspace",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workspaces"
        ordering = ("-created_at",)
```

### Django Model: Project

Projects belong to a workspace and hold all issue-tracking data:

```python
# apiserver/plane/db/models/project.py

class Project(BaseModel):
    NETWORK_CHOICES = ((0, "Secret"), (2, "Public"))

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    workspace = models.ForeignKey(
        "db.Workspace",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    identifier = models.CharField(max_length=12)
    network = models.PositiveSmallIntegerField(
        default=2, choices=NETWORK_CHOICES
    )
    default_assignee = models.ForeignKey(
        "db.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [["workspace", "identifier"]]
        ordering = ("-created_at",)
```

## Verifying Your Setup

After installation, confirm all services are healthy:

```bash
# Check running containers
docker compose ps

# Verify API health
curl http://localhost:8000/api/v1/health/

# Check database connectivity
docker compose exec plane-api python manage.py dbshell -c "SELECT 1;"
```

## Key Takeaways

- Plane runs as a multi-service stack: Next.js frontend, Django API, Celery workers, PostgreSQL, and Redis.
- Docker Compose is the recommended way to get started quickly.
- Workspaces are the top-level organizational unit; projects live inside workspaces.
- The Django backend uses standard model patterns with ForeignKey relationships between Workspace, Project, and User.

## Cross-References

- **Next chapter:** [Chapter 2: System Architecture](02-system-architecture.md) dives deeper into the Django + Next.js stack.
- **Issue tracking:** [Chapter 3: Issue Tracking](03-issue-tracking.md) covers creating your first issues.
- **Deployment:** [Chapter 8: Self-Hosting and Deployment](08-self-hosting-and-deployment.md) covers production configuration.

---

*Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)*
