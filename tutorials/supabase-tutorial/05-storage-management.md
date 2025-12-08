---
layout: default
title: "Chapter 5: Storage & File Management"
parent: "Supabase Tutorial"
nav_order: 5
---

# Chapter 5: Storage & File Management

Handle uploads, access controls, and CDN delivery with Supabase Storage.

## Objectives
- Upload/download files securely
- Configure bucket policies
- Serve media via CDN with signed URLs
- Organize files with predictable paths

## Bucket Setup
```bash
supabase storage create-bucket avatars --public=false
```

## Upload (JS)
```javascript
const file = document.querySelector('input[type=file]').files[0]
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`users/${user.id}/avatar.png`, file, { upsert: true })
```

## Signed URLs
```javascript
const { data } = await supabase.storage
  .from('avatars')
  .createSignedUrl(`users/${user.id}/avatar.png`, 60 * 60) // 1 hour
console.log(data.signedUrl)
```

## Access Policies (RLS-like)
- Make bucket private by default
- Use signed URLs for time-bound access
- For public assets, create a dedicated public bucket

## Image Optimization
- Store original; generate variants via Edge Functions or client-side transforms
- Cache-control headers for static assets

## Troubleshooting
- 401 on download: ensure signed URL not expired; check bucket privacy
- Upload failures: verify file size limits and MIME type
- Slow delivery: enable CDN in dashboard; use caching headers

## Performance Notes
- Prefer smaller optimized variants for UI
- Parallelize uploads cautiously; respect rate limits

## Security Notes
- Keep PII in private buckets
- Use short-lived signed URLs; avoid sharing raw paths

## Next Steps
Chapter 6 adds Edge Functions for custom APIs and storage-backed workflows.
