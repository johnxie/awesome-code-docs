---
layout: default
title: "Chapter 7: Backup & Migration"
parent: "PhotoPrism Tutorial"
nav_order: 7
---

# Chapter 7: Backup & Migration

Welcome to **Chapter 7: Backup & Migration**. In this part of **PhotoPrism Tutorial: AI-Powered Photos App**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter covers backup strategies, data migration, and disaster recovery for PhotoPrism installations.

## 💾 Backup Strategies

### Database Backup

```bash
# Backup PhotoPrism database
docker exec photoprism_db pg_dump -U photoprism photoprism > backup_$(date +%Y%m%d_%H%M%S).sql

# For SQLite (default)
docker cp photoprism:/photoprism/storage/photoprism.db ./backup/
```

### File System Backup

```bash
# Backup photos and storage
docker run --rm -v photoprism_photos:/source -v $(pwd)/backup:/backup alpine tar czf /backup/photos_$(date +%Y%m%d).tar.gz -C /source .

# Backup storage directory
docker run --rm -v photoprism_storage:/source -v $(pwd)/backup:/backup alpine tar czf /backup/storage_$(date +%Y%m%d).tar.gz -C /source .
```

### Automated Backup Script

```bash
#!/bin/bash
# photoprism_backup.sh

BACKUP_DIR="/opt/backups/photoprism"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Stop PhotoPrism for consistent backup
docker-compose stop photoprism

# Database backup
docker exec photoprism_db pg_dump -U photoprism photoprism > $BACKUP_DIR/db_$DATE.sql

# File backup
docker run --rm -v photoprism_photos:/photos -v $BACKUP_DIR:/backup alpine tar czf /backup/photos_$DATE.tar.gz -C /photos .
docker run --rm -v photoprism_storage:/storage -v $BACKUP_DIR:/backup alpine tar czf /backup/storage_$DATE.tar.gz -C /storage .

# Restart PhotoPrism
docker-compose start photoprism

# Clean old backups
find $BACKUP_DIR -name "*.sql" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: $DATE"
```

## 🔄 Data Migration

### Migrate Between Servers

```bash
# Export data from source server
ssh source-server "docker exec photoprism_db pg_dump -U photoprism photoprism" > source_backup.sql

# Copy photos
rsync -avz source-server:/path/to/photos/ /new/server/photos/

# Import on destination
docker cp source_backup.sql photoprism_db:/tmp/
docker exec photoprism_db psql -U photoprism photoprism < /tmp/source_backup.sql
```

### Migrate from Other Services

#### From Google Photos

```typescript
// Google Photos export processing
const processGooglePhotosExport = async (exportPath) => {
  const fs = require('fs')
  const path = require('path')

  const files = fs.readdirSync(exportPath)
  
  for (const file of files) {
    if (path.extname(file).toLowerCase() === '.json') {
      const metadata = JSON.parse(fs.readFileSync(path.join(exportPath, file), 'utf8'))
      
      // Process metadata and move files to PhotoPrism import
      await processGoogleMetadata(metadata)
    }
  }
}
```

#### From Apple Photos

```bash
# Export from Apple Photos
# File > Export > Export Unmodified Originals

# Move to PhotoPrism import
mv ~/Desktop/ApplePhotosExport/* ~/photoprism/photos/import/

# Trigger import
docker exec photoprism photoprism import
```

## ☁️ Cloud Backup Solutions

### AWS S3 Backup

```typescript
// AWS S3 backup integration
const AWS = require('aws-sdk')

const s3Backup = {
  s3: new AWS.S3({
    accessKeyId: process.env.AWS_ACCESS_KEY,
    secretAccessKey: process.env.AWS_SECRET_KEY,
    region: process.env.AWS_REGION
  }),

  async uploadBackup(localPath, bucket, key) {
    const fileStream = fs.createReadStream(localPath)
    
    const uploadParams = {
      Bucket: bucket,
      Key: key,
      Body: fileStream
    }

    return this.s3.upload(uploadParams).promise()
  },

  async downloadBackup(bucket, key, localPath) {
    const downloadParams = {
      Bucket: bucket,
      Key: key
    }

    const fileStream = fs.createWriteStream(localPath)
    const s3Stream = this.s3.getObject(downloadParams).createReadStream()
    
    return new Promise((resolve, reject) => {
      s3Stream.pipe(fileStream)
        .on('finish', resolve)
        .on('error', reject)
    })
  }
}
```

### Google Cloud Storage

```typescript
// Google Cloud Storage backup
const { Storage } = require('@google-cloud/storage')

const gcsBackup = {
  storage: new Storage({
    keyFilename: '/path/to/service-account-key.json'
  }),

  bucket: 'photoprism-backups',

  async uploadBackup(localPath, remotePath) {
    await this.storage.bucket(this.bucket).upload(localPath, {
      destination: remotePath,
      metadata: {
        metadata: {
          backupDate: new Date().toISOString()
        }
      }
    })
  }
}
```

## 🔄 Version Upgrades

### Database Migration

```bash
# Backup before upgrade
docker exec photoprism_db pg_dump -U photoprism photoprism > pre_upgrade_backup.sql

# Stop services
docker-compose down

# Pull new version
docker-compose pull

# Run database migrations
docker-compose run --rm photoprism photoprism migrate

# Start services
docker-compose up -d
```

### Rolling Back

```bash
# Rollback procedure
docker-compose down
docker tag photoprism/photoprism:latest photoprism/photoprism:previous
docker pull photoprism/photoprism:previous_version

# Restore database
docker exec photoprism_db psql -U photoprism photoprism < pre_upgrade_backup.sql

# Start with previous version
docker-compose up -d
```

## 📊 Backup Verification

### Integrity Checks

```typescript
// Verify backup integrity
const verifyBackup = async (backupPath) => {
  const checks = {
    database: await verifyDatabaseBackup(backupPath),
    files: await verifyFileBackup(backupPath),
    metadata: await verifyMetadataBackup(backupPath)
  }

  return {
    valid: Object.values(checks).every(check => check.valid),
    details: checks
  }
}

const verifyDatabaseBackup = async (path) => {
  try {
    // Test database restore
    const testDb = new sqlite3.Database(':memory:')
    const backupData = fs.readFileSync(path, 'utf8')
    
    // Parse and validate SQL
    const statements = backupData.split(';').filter(stmt => stmt.trim())
    
    return { valid: true, statementCount: statements.length }
  } catch (error) {
    return { valid: false, error: error.message }
  }
}
```

### Automated Testing

```typescript
// Automated backup testing
const testBackupRestore = async () => {
  // Create test data
  await createTestPhotos()
  
  // Perform backup
  await performBackup()
  
  // Test restore
  const restoreResult = await testRestore()
  
  // Verify data integrity
  const integrityCheck = await verifyRestoredData()
  
  return {
    backupSuccessful: true,
    restoreSuccessful: restoreResult.success,
    dataIntegrity: integrityCheck.valid
  }
}
```

## 🚨 Disaster Recovery

### Recovery Plan

```typescript
// Disaster recovery procedures
const disasterRecovery = {
  priorities: [
    'Restore database',
    'Restore photo files',
    'Verify AI models',
    'Test functionality',
    'Update DNS if needed'
  ],

  procedures: {
    database: {
      steps: [
        'Stop PhotoPrism',
        'Create new database',
        'Restore from backup',
        'Run migrations',
        'Start PhotoPrism'
      ]
    },
    
    files: {
      steps: [
        'Verify backup integrity',
        'Restore to correct paths',
        'Set proper permissions',
        'Trigger re-indexing'
      ]
    }
  },

  async executeRecovery(scenario) {
    for (const step of this.procedures[scenario].steps) {
      console.log(`Executing: ${step}`)
      await executeStep(step)
    }
  }
}
```

## 📈 Monitoring Backup Health

### Backup Metrics

```typescript
// Backup monitoring and alerting
const backupMonitoring = {
  metrics: {
    lastBackupTime: null,
    backupSize: 0,
    backupDuration: 0,
    successRate: 1.0
  },

  thresholds: {
    maxAge: 24 * 60 * 60 * 1000, // 24 hours
    minSuccessRate: 0.95
  },

  checkHealth() {
    const issues = []

    const age = Date.now() - this.metrics.lastBackupTime
    if (age > this.thresholds.maxAge) {
      issues.push('Backup is too old')
    }

    if (this.metrics.successRate < this.thresholds.minSuccessRate) {
      issues.push('Backup success rate too low')
    }

    return {
      healthy: issues.length === 0,
      issues
    }
  },

  async sendAlert(message) {
    // Send alert to monitoring system
    await monitoringSystem.alert('PhotoPrism Backup', message)
  }
}
```

## 🔧 Maintenance Tasks

### Regular Maintenance

```bash
# Clean up old thumbnails
docker exec photoprism photoprism thumbs clean

# Optimize database
docker exec photoprism_db vacuumdb -U photoprism --analyze photoprism

# Check disk usage
docker system df
docker volume ls
```

### Health Checks

```typescript
// Automated health checks
const healthChecks = {
  async checkDatabase() {
    try {
      await db.query('SELECT COUNT(*) FROM photos')
      return { status: 'healthy' }
    } catch (error) {
      return { status: 'unhealthy', error: error.message }
    }
  },

  async checkStorage() {
    const stats = fs.statSync('/photoprism/photos')
    const freeSpace = stats.available / (1024 * 1024 * 1024) // GB
    
    if (freeSpace < 10) {
      return { status: 'warning', message: 'Low disk space' }
    }
    
    return { status: 'healthy' }
  },

  async runAllChecks() {
    const results = await Promise.all([
      this.checkDatabase(),
      this.checkStorage(),
      // Add more checks
    ])

    return {
      overall: results.every(r => r.status === 'healthy') ? 'healthy' : 'unhealthy',
      checks: results
    }
  }
}
```

## 📝 Chapter Summary

- ✅ Implemented automated backup scripts
- ✅ Created migration procedures
- ✅ Set up cloud backup solutions
- ✅ Planned version upgrade processes
- ✅ Built backup verification systems
- ✅ Developed disaster recovery plans
- ✅ Established monitoring and maintenance

**Key Takeaways:**
- Regular backups are critical for data safety
- Test backups regularly to ensure they work
- Plan for different disaster scenarios
- Automate as much as possible
- Monitor backup health continuously
- Document all procedures thoroughly
- Consider both cloud and local backup options

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `photoprism`, `docker`, `backup` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 7: Backup & Migration` as an operating subsystem inside **PhotoPrism Tutorial: AI-Powered Photos App**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `Backup`, `database`, `exec` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 7: Backup & Migration` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `photoprism`.
2. **Input normalization**: shape incoming data so `docker` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `backup`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [github.com/photoprism/photoprism](https://github.com/photoprism/photoprism)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism` (github.com).
- [github.com/photoprism/photoprism/discussions](https://github.com/photoprism/photoprism/discussions)
  Why it matters: authoritative reference on `github.com/photoprism/photoprism/discussions` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `photoprism` and `docker` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Previous Chapter: Chapter 6: API Integration](06-api-integration.md)
- [Next Chapter: Chapter 8: Production Deployment](08-production-deployment.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
