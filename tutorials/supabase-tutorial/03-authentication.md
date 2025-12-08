---
layout: default
title: "Chapter 3: Authentication & Authorization"
parent: "Supabase Tutorial"
nav_order: 3
---

# Chapter 3: Authentication & Authorization

Add secure auth flows, OAuth providers, and enforce Row Level Security (RLS).

## Objectives
- Implement email/password and OAuth login
- Manage user profiles and metadata
- Enforce RLS for per-user data access
- Protect service-role operations

## Email/Password Sign Up (JS)
```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY)

const { data, error } = await supabase.auth.signUp({
  email: 'alice@example.com',
  password: 'StrongP@ssw0rd',
})
if (error) console.error(error)
```

## OAuth Example (GitHub)
```javascript
const { data, error } = await supabase.auth.signInWithOAuth({ provider: 'github' })
```

## Persist Profile on Signup (SQL trigger)
```sql
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, username)
  values (new.id, split_part(new.email, '@', 1));
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
```

## RLS Policies
```sql
alter table public.profiles enable row level security;

create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);
```

## Server-Side Service Role
- Use `SUPABASE_SERVICE_ROLE_KEY` only on trusted servers
- Avoid exposing service keys to clients

## Troubleshooting
- 401 errors: check anon vs service role key usage
- RLS blocks queries: verify `auth.uid()` is available (only via authenticated client)
- OAuth redirect issues: confirm callback URLs in Supabase dashboard

## Performance Notes
- Cache session in memory for SSR frameworks
- Use `select('*')` judiciously; fetch only needed fields

## Security Notes
- Enable email confirmations for signup
- Enforce strong password policy via dashboard
- Rotate service keys periodically

## Next Steps
Continue to Chapter 4 to add real-time subscriptions and live data updates.
