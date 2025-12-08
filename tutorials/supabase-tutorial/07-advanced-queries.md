---
layout: default
title: "Chapter 7: Advanced Queries & RLS"
parent: "Supabase Tutorial"
nav_order: 7
---

# Chapter 7: Advanced Queries & RLS

Write efficient queries, add search, and harden Row Level Security.

## Objectives
- Implement complex filters and pagination
- Add full-text search
- Optimize queries and indexes
- Harden RLS for multi-tenant data

## Complex Query (JS)
```javascript
const { data, error } = await supabase
  .from('messages')
  .select('id, content, created_at')
  .eq('room_id', roomId)
  .lt('created_at', cursor)
  .order('created_at', { ascending: false })
  .limit(50)
```

## Full-Text Search (SQL)
```sql
alter table public.articles add column search tsvector
  generated always as (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'B')
  ) stored;
create index on public.articles using gin (search);
```

Query:
```sql
select id, title, ts_rank(search, plainto_tsquery('english', 'vector database')) as rank
from public.articles
where search @@ plainto_tsquery('english', 'vector database')
order by rank desc
limit 20;
```

## RLS for Multi-Tenant Apps
```sql
create policy "Tenant can read own data" on public.items
for select using (auth.uid() = tenant_id);

create policy "Tenant can write own data" on public.items
for insert with check (auth.uid() = tenant_id)
for update using (auth.uid() = tenant_id);
```

## Performance Tips
- Use `explain analyze` to spot slow plans
- Add covering indexes for common filters/sorts
- Avoid N+1 in clients; fetch related data with RPC or view

## Troubleshooting
- Slow queries: add indexes; reduce payload; cache results
- RLS blocks: ensure `auth.uid()` is available; test with `set local role authenticated` in SQL editor
- Search returns few results: try `websearch_to_tsquery` or synonyms

## Security Notes
- Default deny; only allow needed verbs
- Separate policies for select/insert/update/delete
- Audit access on sensitive tables

## Next Steps
Finish with Chapter 8 to prepare production deployments with monitoring and scaling.
