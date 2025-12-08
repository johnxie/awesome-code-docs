---
layout: default
title: "Chapter 2: Database Design & Management"
parent: "Supabase Tutorial"
nav_order: 2
---

# Chapter 2: Database Design & Management

Model your schema, manage migrations, and prepare Postgres for secure, real-time apps.

## Objectives
- Create tables, relationships, and constraints
- Set up migrations and seed data
- Configure Row Level Security (RLS) foundations
- Index for performance

## Create Schema (SQL)
```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  full_name text,
  created_at timestamptz default now()
);

create index on public.profiles (username);
```

## Migrations with Supabase CLI
```bash
supabase db diff --file initial_schema.sql
supabase db push  # apply to remote project
```

## Seeding Data
```bash
supabase db seed --file seeds/seed.sql
```

Example `seeds/seed.sql`:
```sql
insert into public.profiles (id, username, full_name)
values
  (gen_random_uuid(), 'alice', 'Alice Doe'),
  (gen_random_uuid(), 'bob', 'Bob Smith');
```

## Relationships
- Use `references ... on delete cascade` for dependent tables
- Prefer UUID primary keys for distributed clients
- Add unique constraints for natural keys (e.g., username)

## Indexing Basics
- Index high-cardinality lookup columns (email, username)
- Add composite indexes for frequent filters (e.g., `(user_id, created_at desc)`)
- Avoid over-indexing write-heavy tables

## RLS Foundations
- Enable RLS on tables that hold user data
```sql
alter table public.profiles enable row level security;
```

- Default deny policy
```sql
create policy "Profiles are viewable by owners" on public.profiles
for select using (auth.uid() = id);
```

## Troubleshooting
- Migration conflicts: rebase or regenerate diff; ensure clean schema state
- Missing extensions: enable `pgcrypto` for UUID, `pg_trgm` for search
- Performance issues: examine `explain analyze` before adding indexes

## Performance Notes
- Use `created_at timestamptz default now()` for ordering and pagination
- Prefer `text` + constraints over `varchar(n)` unless needed
- Partition only when datasets are very large; start simple

## Security Notes
- Always enable RLS on user-owned data
- Restrict `supabase_admin` usage; use service roles server-side only

## Next Steps
Proceed to Chapter 3 to implement authentication and authorization using Supabase Auth and RLS.
