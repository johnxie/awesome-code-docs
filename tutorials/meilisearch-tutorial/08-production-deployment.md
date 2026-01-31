---
layout: default
title: "Chapter 8: Production Deployment"
parent: "MeiliSearch Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

This final chapter covers deploying Meilisearch in production environments, including scaling, monitoring, security, and maintenance strategies.

## 🚀 Production Setup

### Server Requirements

```bash
# Recommended server specifications
MINIMUM_SPECS="
CPU: 2 cores
RAM: 4GB
Storage: 20GB SSD
Network: 100Mbps
"

RECOMMENDED_SPECS="
CPU: 4+ cores
RAM: 8GB+
Storage: 100GB+ SSD
Network: 1Gbps
"
```

### Docker Production Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  meilisearch:
    image: getmeili/meilisearch:v1.8.0
    container_name: meilisearch_prod
    restart: unless-stopped
    ports:
      - "127.0.0.1:7700:7700"
    environment:
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
      - MEILI_DB_PATH=./meili_data
      - MEILI_HTTP_ADDR=0.0.0.0:7700
      - MEILI_ENV=production
      - MEILI_LOG_LEVEL=INFO
      - MEILI_MAX_INDEX_SIZE=5GiB
    volumes:
      - ./meili_data:/meili_data
      - ./snapshots:/snapshots
    networks:
      - meilisearch_network

networks:
  meilisearch_network:
    driver: bridge
```

### Systemd Service

```bash
# Create systemd service file
sudo tee /etc/systemd/system/meilisearch.service > /dev/null <<EOF
[Unit]
Description=Meilisearch Search Engine
After=network.target

[Service]
Type=simple
User=meilisearch
Group=meilisearch
WorkingDirectory=/var/lib/meilisearch
ExecStart=/usr/local/bin/meilisearch --db-path /var/lib/meilisearch/data --master-key ${MEILI_MASTER_KEY}
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=meilisearch

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable meilisearch
sudo systemctl start meilisearch
```

## 🔒 Security Configuration

### Master Key Management

```bash
# Generate strong master key
MASTER_KEY=$(openssl rand -hex 32)
echo "MEILI_MASTER_KEY=$MASTER_KEY" > .env

# Use environment variables
export MEILI_MASTER_KEY=$MASTER_KEY
```

### Network Security

```bash
# Configure firewall
sudo ufw allow from 127.0.0.1 to any port 7700
sudo ufw deny from 0.0.0.0/0 to any port 7700

# Or using iptables
sudo iptables -A INPUT -p tcp -s 127.0.0.1 --dport 7700 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 7700 -j DROP
```

### SSL/TLS Configuration

```bash
# Using Nginx as reverse proxy with SSL
sudo tee /etc/nginx/sites-available/meilisearch > /dev/null <<EOF
server {
    listen 443 ssl http2;
    server_name search.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:7700;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

### API Key Management

```bash
# Create tenant-specific API keys
curl -X POST 'http://localhost:7700/keys' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_master_key' \
  --data '{
    "description": "Search-only key for web app",
    "actions": ["search"],
    "indexes": ["products", "articles"],
    "expiresAt": "2025-12-31T23:59:59Z"
  }'
```

## 📊 Monitoring and Logging

### Health Checks

```bash
# Health check endpoint
curl http://localhost:7700/health

# Detailed stats
curl 'http://localhost:7700/indexes/products/stats'
```

### Log Configuration

```bash
# Configure logging
export MEILI_LOG_LEVEL=INFO
export MEILI_MAX_LOG_SIZE=100MiB
export MEILI_MAX_LOG_FILES=5
```

### Monitoring Dashboard

```javascript
// Simple monitoring dashboard
class MeiliMonitor {
  constructor(client) {
    this.client = client;
  }

  async getHealthStatus() {
    try {
      const health = await this.client.health();
      return { status: 'healthy', ...health };
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  }

  async getIndexStats() {
    const indexes = await this.client.getIndexes();
    const stats = {};

    for (const index of indexes) {
      stats[index.uid] = await this.client.index(index.uid).getStats();
    }

    return stats;
  }

  async getPerformanceMetrics() {
    // Monitor response times, throughput, etc.
    return {
      uptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
      // Add custom metrics
    };
  }
}
```

## 🚀 Scaling Strategies

### Horizontal Scaling

```yaml
# Multiple Meilisearch instances
version: '3.8'
services:
  meilisearch-1:
    image: getmeili/meilisearch:v1.8.0
    environment:
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
    volumes:
      - ./data-1:/meili_data
    networks:
      - meilisearch-cluster

  meilisearch-2:
    image: getmeili/meilisearch:v1.8.0
    environment:
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
    volumes:
      - ./data-2:/meili_data
    networks:
      - meilisearch-cluster

  load-balancer:
    image: nginx:alpine
    ports:
      - "7700:7700"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - meilisearch-1
      - meilisearch-2
    networks:
      - meilisearch-cluster
```

### Load Balancing

```nginx
# nginx.conf for load balancing
events {
    worker_connections 1024;
}

http {
    upstream meilisearch_backend {
        server meilisearch-1:7700;
        server meilisearch-2:7700;
    }

    server {
        listen 7700;
        location / {
            proxy_pass http://meilisearch_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```

## 💾 Backup and Recovery

### Snapshot Creation

```bash
# Create snapshot
curl -X POST 'http://localhost:7700/snapshots' \
  -H 'Authorization: Bearer your_master_key'

# List snapshots
curl 'http://localhost:7700/snapshots' \
  -H 'Authorization: Bearer your_master_key'
```

### Automated Backups

```bash
#!/bin/bash
# backup_meilisearch.sh

BACKUP_DIR="/var/backups/meilisearch"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_NAME="meilisearch_$TIMESTAMP"

# Create snapshot
curl -X POST 'http://localhost:7700/snapshots' \
  -H 'Authorization: Bearer your_master_key' \
  -d "{\"snapshotName\": \"$SNAPSHOT_NAME\"}"

# Download snapshot
curl "http://localhost:7700/snapshots/$SNAPSHOT_NAME/download" \
  -H 'Authorization: Bearer your_master_key' \
  -o "$BACKUP_DIR/$SNAPSHOT_NAME.tar.gz"

# Clean old backups (keep last 7 days)
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

### Recovery Process

```bash
# Stop Meilisearch
sudo systemctl stop meilisearch

# Restore from snapshot
tar -xzf /path/to/snapshot.tar.gz -C /var/lib/meilisearch/

# Start Meilisearch
sudo systemctl start meilisearch
```

## 🔧 Performance Optimization

### Index Optimization

```bash
# Optimize index
curl -X POST 'http://localhost:7700/indexes/products/optimize' \
  -H 'Authorization: Bearer your_master_key'
```

### Memory Configuration

```bash
# Configure memory usage
export MEILI_MAX_INDEX_SIZE=10GiB
export MEILI_MAX_TASK_DB_SIZE=1GiB
```

### Query Optimization

```javascript
// Optimize search queries
const optimizedSearch = async (query, filters) => {
  // Use specific attributes to reduce payload
  const params = {
    q: query,
    filter: filters,
    attributesToRetrieve: ['id', 'title', 'price'], // Only needed fields
    limit: 50 // Reasonable limit
  };

  return await client.search(query, params);
};
```

## 📈 Analytics and Metrics

### Search Analytics

```javascript
class SearchAnalytics {
  constructor() {
    this.metrics = {
      totalSearches: 0,
      averageResponseTime: 0,
      popularQueries: new Map(),
      failedSearches: 0
    };
  }

  trackSearch(query, results, responseTime) {
    this.metrics.totalSearches++;
    this.metrics.averageResponseTime =
      (this.metrics.averageResponseTime + responseTime) / 2;

    // Track popular queries
    const count = this.metrics.popularQueries.get(query) || 0;
    this.metrics.popularQueries.set(query, count + 1);
  }

  getMetrics() {
    return {
      ...this.metrics,
      popularQueries: Array.from(this.metrics.popularQueries.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
    };
  }
}
```

### Performance Monitoring

```javascript
// Monitor Meilisearch performance
const monitor = async () => {
  const stats = await client.getStats();

  console.log('Index Stats:', {
    numberOfDocuments: stats.numberOfDocuments,
    size: stats.size,
    lastUpdate: stats.lastUpdate
  });

  // Check task queue
  const tasks = await client.getTasks();
  const pendingTasks = tasks.filter(task => task.status === 'processing');

  if (pendingTasks.length > 10) {
    console.warn('High task queue:', pendingTasks.length);
  }
};
```

## 🚨 Maintenance Tasks

### Regular Maintenance

```bash
#!/bin/bash
# maintenance.sh

# Update Meilisearch
docker pull getmeili/meilisearch:latest

# Backup before maintenance
./backup_meilisearch.sh

# Health check
curl http://localhost:7700/health

# Clean old logs
find /var/log/meilisearch -name "*.log" -mtime +30 -delete

# Optimize indexes
curl -X POST 'http://localhost:7700/indexes/*/optimize' \
  -H 'Authorization: Bearer your_master_key'
```

### Log Rotation

```bash
# Configure logrotate
sudo tee /etc/logrotate.d/meilisearch > /dev/null <<EOF
/var/log/meilisearch/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 meilisearch meilisearch
    postrotate
        systemctl reload meilisearch
    endscript
}
EOF
```

## 🌍 CDN Integration

### Static Asset Caching

```javascript
// Cache search results in CDN
const cachedSearch = async (query, ttl = 300) => {
  const cacheKey = `search:${query}`;

  // Check CDN cache first
  const cached = await cdn.get(cacheKey);
  if (cached) return cached;

  // Perform search
  const results = await client.search(query);

  // Cache in CDN
  await cdn.set(cacheKey, results, ttl);

  return results;
};
```

## 📝 Deployment Checklist

```bash
# Pre-deployment checklist
DEPLOYMENT_CHECKLIST="
☐ Server requirements met
☐ Master key generated and secured
☐ SSL/TLS configured
☐ Firewall rules applied
☐ Backup strategy implemented
☐ Monitoring setup
☐ Load balancer configured
☐ Health checks working
☐ Documentation updated
☐ Team notified of deployment
"
```

## 🚨 Troubleshooting Production

### Common Issues

1. **High Memory Usage**
   ```bash
   # Check memory usage
   ps aux | grep meilisearch

   # Configure memory limits
   export MEILI_MAX_INDEX_SIZE=5GiB
   ```

2. **Slow Search Performance**
   ```bash
   # Check index stats
   curl 'http://localhost:7700/indexes/products/stats'

   # Optimize index
   curl -X POST 'http://localhost:7700/indexes/products/optimize'
   ```

3. **Task Queue Backlog**
   ```bash
   # Monitor tasks
   curl 'http://localhost:7700/tasks?statuses=processing'

   # Check server resources
   top -p $(pgrep meilisearch)
   ```

## 📝 Chapter Summary

- ✅ Configured production-ready Meilisearch deployment
- ✅ Implemented security measures (SSL, API keys, firewall)
- ✅ Set up monitoring and logging
- ✅ Configured scaling and load balancing
- ✅ Implemented backup and recovery strategies
- ✅ Optimized performance and maintenance

**Key Takeaways:**
- Always use strong master keys and secure API endpoints
- Implement proper monitoring and health checks
- Set up automated backups and recovery procedures
- Configure load balancing for high availability
- Monitor performance and optimize regularly
- Implement proper logging and log rotation
- Use SSL/TLS in production environments
- Plan for scaling as your application grows
