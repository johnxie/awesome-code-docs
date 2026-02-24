---
layout: default
title: "Chapter 1: Getting Started with Supabase"
parent: "Supabase Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with Supabase

Welcome to Supabase! If you've ever wanted to build modern applications with a complete backend infrastructure without managing servers, databases, or complex configurations, you're in the right place. Supabase provides everything you need to build scalable, secure applications with minimal setup.

## What Makes Supabase Powerful?

Supabase revolutionizes backend development by:
- **Complete Backend Stack** - Database, auth, storage, real-time, and edge functions
- **PostgreSQL Power** - Enterprise-grade database with advanced features
- **Instant API Generation** - Automatic REST and GraphQL APIs from your database
- **Real-time Subscriptions** - Live data synchronization across clients
- **Built-in Security** - Authentication, authorization, and data protection
- **Developer Experience** - Excellent tooling and documentation
- **Open Source** - Full control and customization capabilities

## Project Setup Options

### Option 1: Supabase Cloud (Recommended for Beginners)

1. **Create Account**: Visit [supabase.com](https://supabase.com) and sign up
2. **Create Project**:
   - Click "New Project"
   - Choose your organization
   - Enter project details
   - Select region (choose closest to your users)
   - Set database password

3. **Wait for Setup**: Project creation takes 2-3 minutes

### Option 2: Local Development with Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init

# Start local Supabase stack
supabase start

# Access local dashboard at http://localhost:54323
```

### Option 3: Self-Hosted Supabase

```bash
# Clone Supabase repository
git clone https://github.com/supabase/supabase
cd supabase

# Use Docker Compose for local deployment
docker-compose up -d
```

## Your First Supabase Application

Let's create a simple task management application:

### Step 1: Project Initialization

```bash
# Create a new project directory
mkdir supabase-tasks
cd supabase-tasks

# Initialize with your preferred framework
# For React:
npx create-react-app . --template typescript
# For Next.js:
npx create-next-app . --typescript
# For Vue:
npm create vue@latest .
```

### Step 2: Install Supabase Client

```bash
# Install Supabase JavaScript client
npm install @supabase/supabase-js

# For React hooks (optional)
npm install @supabase/auth-helpers-react @supabase/auth-helpers-nextjs
```

### Step 3: Configure Supabase Client

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'your-project-url'
const supabaseKey = 'your-anon-key'

export const supabase = createClient(supabaseUrl, supabaseKey)

// Types for better TypeScript support
export type Database = {
  public: {
    Tables: {
      tasks: {
        Row: {
          id: number
          title: string
          description: string | null
          completed: boolean
          created_at: string
          user_id: string
        }
        Insert: {
          title: string
          description?: string | null
          completed?: boolean
          user_id: string
        }
        Update: {
          title?: string
          description?: string | null
          completed?: boolean
        }
      }
    }
  }
}
```

### Step 4: Create Database Schema

```sql
-- Run this in Supabase SQL Editor
CREATE TABLE tasks (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE
);

-- Enable Row Level Security
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see only their own tasks
CREATE POLICY "Users can view own tasks" ON tasks
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks" ON tasks
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tasks" ON tasks
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own tasks" ON tasks
  FOR DELETE USING (auth.uid() = user_id);
```

### Step 5: Implement Basic CRUD Operations

```typescript
// src/hooks/useTasks.ts
import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import type { Database } from '../lib/supabase'

type Task = Database['public']['Tables']['tasks']['Row']
type TaskInsert = Database['public']['Tables']['tasks']['Insert']

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  // Fetch tasks
  useEffect(() => {
    fetchTasks()
  }, [])

  async function fetchTasks() {
    try {
      const { data, error } = await supabase
        .from('tasks')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      setTasks(data || [])
    } catch (error) {
      console.error('Error fetching tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  // Add task
  async function addTask(task: TaskInsert) {
    try {
      const { data, error } = await supabase
        .from('tasks')
        .insert([task])
        .select()
        .single()

      if (error) throw error
      setTasks(prev => [data, ...prev])
      return data
    } catch (error) {
      console.error('Error adding task:', error)
      throw error
    }
  }

  // Update task
  async function updateTask(id: number, updates: Partial<Task>) {
    try {
      const { data, error } = await supabase
        .from('tasks')
        .update(updates)
        .eq('id', id)
        .select()
        .single()

      if (error) throw error
      setTasks(prev => prev.map(task =>
        task.id === id ? data : task
      ))
      return data
    } catch (error) {
      console.error('Error updating task:', error)
      throw error
    }
  }

  // Delete task
  async function deleteTask(id: number) {
    try {
      const { error } = await supabase
        .from('tasks')
        .delete()
        .eq('id', id)

      if (error) throw error
      setTasks(prev => prev.filter(task => task.id !== id))
    } catch (error) {
      console.error('Error deleting task:', error)
      throw error
    }
  }

  return {
    tasks,
    loading,
    addTask,
    updateTask,
    deleteTask,
    refetch: fetchTasks
  }
}
```

### Step 6: Create User Interface

```tsx
// src/components/TaskList.tsx
import React, { useState } from 'react'
import { useTasks } from '../hooks/useTasks'
import { supabase } from '../lib/supabase'

export function TaskList() {
  const { tasks, loading, addTask, updateTask, deleteTask } = useTasks()
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [user, setUser] = useState(null)

  // Get current user
  React.useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
    }
    getUser()
  }, [])

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTaskTitle.trim() || !user) return

    try {
      await addTask({
        title: newTaskTitle,
        user_id: user.id
      })
      setNewTaskTitle('')
    } catch (error) {
      console.error('Error adding task:', error)
    }
  }

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    try {
      await updateTask(taskId, { completed: !completed })
    } catch (error) {
      console.error('Error updating task:', error)
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId)
    } catch (error) {
      console.error('Error deleting task:', error)
    }
  }

  if (loading) return <div>Loading tasks...</div>

  return (
    <div className="task-list">
      <h1>My Tasks</h1>

      {/* Add new task form */}
      <form onSubmit={handleAddTask}>
        <input
          type="text"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
          placeholder="Add a new task..."
          required
        />
        <button type="submit">Add Task</button>
      </form>

      {/* Task list */}
      <div className="tasks">
        {tasks.map(task => (
          <div key={task.id} className={`task ${task.completed ? 'completed' : ''}`}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => handleToggleComplete(task.id, task.completed)}
            />
            <span className="task-title">{task.title}</span>
            <button
              onClick={() => handleDeleteTask(task.id)}
              className="delete-btn"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
```

### Step 7: Add Authentication

```tsx
// src/components/Auth.tsx
import React, { useState } from 'react'
import { supabase } from '../lib/supabase'

export function Auth() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const { error } = await supabase.auth.signUp({
        email,
        password
      })

      if (error) throw error
      alert('Check your email for the confirmation link!')
    } catch (error) {
      alert(error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password
      })

      if (error) throw error
    } catch (error) {
      alert(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <form onSubmit={handleSignIn}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Sign In'}
        </button>
        <button
          type="button"
          onClick={handleSignUp}
          disabled={loading}
        >
          Sign Up
        </button>
      </form>
    </div>
  )
}
```

## Understanding Supabase Architecture

### Core Components

```
Supabase Platform
├── Database (PostgreSQL)
│   ├── Tables & Schemas
│   ├── Row Level Security (RLS)
│   ├── Triggers & Functions
│   └── Real-time Subscriptions
├── Authentication
│   ├── User Management
│   ├── OAuth Providers
│   ├── JWT Tokens
│   └── Custom Auth Flows
├── Storage
│   ├── File Uploads
│   ├── CDN Integration
│   ├── Access Policies
│   └── Image Transformations
├── Edge Functions
│   ├── Serverless Functions
│   ├── API Routes
│   ├── Webhooks
│   └── Background Jobs
└── Dashboard & APIs
    ├── Admin Interface
    ├── REST API
    ├── GraphQL API
    └── Realtime API
```

### API Layer

Supabase automatically generates APIs for your database:

```typescript
// REST API endpoints are automatically created
// GET /rest/v1/tasks - Get all tasks
// POST /rest/v1/tasks - Create new task
// GET /rest/v1/tasks?id=eq.1 - Get specific task
// PATCH /rest/v1/tasks?id=eq.1 - Update task
// DELETE /rest/v1/tasks?id=eq.1 - Delete task

// Client-side usage
const { data, error } = await supabase
  .from('tasks')
  .select('*')
  .eq('completed', false)
  .order('created_at', { ascending: false })
```

### Real-time Capabilities

```typescript
// Subscribe to real-time changes
const subscription = supabase
  .channel('tasks')
  .on('postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'tasks'
    },
    (payload) => {
      console.log('Change received!', payload)
      // Update UI with new data
    }
  )
  .subscribe()

// Clean up subscription
subscription.unsubscribe()
```

## Security Best Practices

### Row Level Security (RLS)

```sql
-- Enable RLS on tables
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Create policies for data access
CREATE POLICY "Users can view own tasks"
  ON tasks FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks"
  ON tasks FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Development Workflow

### Local Development

```bash
# Start local Supabase
supabase start

# Reset database
supabase db reset

# Generate types
supabase gen types typescript --local > types/supabase.ts

# View logs
supabase logs
```

### Database Migrations

```bash
# Create migration
supabase migration new create_tasks_table

# Apply migrations
supabase db push

# View migration status
supabase db diff
```

## Testing Your Setup

### Basic Connection Test

```typescript
// Test database connection
const testConnection = async () => {
  try {
    const { data, error } = await supabase
      .from('tasks')
      .select('count')
      .single()

    if (error) throw error
    console.log('✅ Database connection successful!')
  } catch (error) {
    console.error('❌ Database connection failed:', error)
  }
}
```

### Authentication Test

```typescript
// Test authentication
const testAuth = async () => {
  try {
    const { data, error } = await supabase.auth.getUser()

    if (error) throw error
    console.log('✅ Authentication working!')
    console.log('User:', data.user?.email)
  } catch (error) {
    console.error('❌ Authentication failed:', error)
  }
}
```

## What We've Accomplished

Congratulations! 🎉 You've successfully:

1. **Set up a Supabase project** with database and authentication
2. **Created a complete task management application** with full CRUD operations
3. **Implemented user authentication** with secure access controls
4. **Built real-time features** for live data synchronization
5. **Configured Row Level Security** for data protection
6. **Used automatic API generation** for seamless data access
7. **Set up development workflow** with local environment
8. **Implemented security best practices** for production readiness

## Next Steps

Now that you have a working Supabase application, let's dive deeper into database design and management. In [Chapter 2: Database Design & Management](02-database-design.md), we'll explore advanced PostgreSQL features, migrations, and data modeling strategies.

---

**Practice what you've learned:**
1. Add more features to your task app (due dates, categories, priorities)
2. Implement real-time updates for multiple users
3. Add file attachments using Supabase Storage
4. Create a mobile version using React Native

*What kind of application are you most excited to build with Supabase's powerful features?* 🚀

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `error`, `tasks`, `supabase` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with Supabase` as an operating subsystem inside **Supabase Tutorial: Building Modern Backend Applications**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `task`, `auth`, `console` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with Supabase` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `error`.
2. **Input normalization**: shape incoming data so `tasks` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `supabase`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [View Repo](https://github.com/supabase/supabase)
  Why it matters: authoritative reference on `View Repo` (github.com).

Suggested trace strategy:
- search upstream code for `error` and `tasks` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Database Design & Management](02-database-design.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
