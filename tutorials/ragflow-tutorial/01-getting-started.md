---
layout: default
title: "Chapter 1: Getting Started with RAGFlow"
parent: "RAGFlow Tutorial"
nav_order: 1
---

# Chapter 1: Getting Started with RAGFlow

Welcome to your journey with RAGFlow! This chapter will guide you through installing and setting up RAGFlow, understanding its core components, and creating your first RAG application.

## 🎯 What You'll Learn

- RAGFlow architecture and components
- Installation methods (Docker, source, cloud)
- Basic configuration and setup
- First RAG application walkthrough
- Core concepts and terminology

## 🏗️ RAGFlow Architecture

RAGFlow consists of several key components working together:

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Web Interface]
        B[API Gateway]
    end

    subgraph "Application Layer"
        C[RAGFlow Server]
        D[Task Scheduler]
        E[Document Parser]
    end

    subgraph "Data Layer"
        F[Vector Database]
        G[Graph Database]
        H[Document Store]
    end

    subgraph "AI Layer"
        I[Embedding Models]
        J[LLM Services]
        K[Inference Engine]
    end

    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    D --> G
    E --> H
    C --> I
    C --> J
    J --> K
```

### Core Components

1. **Web Interface**: User-friendly management console
2. **RAGFlow Server**: Main application server handling requests
3. **Document Parser**: Processes various document formats
4. **Vector Database**: Stores document embeddings for similarity search
5. **Graph Database**: Maintains knowledge relationships
6. **Task Scheduler**: Manages background processing tasks

## 🚀 Installation Methods

### Method 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/infiniflow/ragflow.git
cd ragflow

# Start all services
docker-compose -f docker-compose.yml up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f ragflow-server
```

**Expected output:**
```
Starting ragflow-server ... done
Starting ragflow-web ... done
Starting ragflow-redis ... done
Starting ragflow-mysql ... done
Starting ragflow-minio ... done
```

### Method 2: Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install python3.10 python3.10-venv redis-server mysql-server

# Clone and setup
git clone https://github.com/infiniflow/ragflow.git
cd ragflow

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for web interface)
cd web
npm install
npm run build

# Start services
cd ..
python api/ragflow_server.py &
python web/ragflow_web.py &
```

### Method 3: Cloud Deployment

#### AWS EC2 Deployment

```bash
# Launch EC2 instance (t3.large or better)
# Ubuntu 20.04 LTS, 8GB RAM minimum

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Clone and deploy
git clone https://github.com/infiniflow/ragflow.git
cd ragflow

# Modify docker-compose.yml for production
vim docker-compose.yml

# Start services
docker-compose up -d
```

#### Google Cloud Run

```yaml
# cloud-run-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: ragflow-service
spec:
  template:
    spec:
      containers:
      - image: infiniflow/ragflow:latest
        ports:
        - containerPort: 80
        env:
        - name: DATABASE_URL
          value: "mysql://user:pass@db-host:3306/ragflow"
        resources:
          limits:
            cpu: "2000m"
            memory: "4Gi"
```

## ⚙️ Configuration

### Environment Variables

```bash
# Create .env file
cat > .env << EOF
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=ragflow
MYSQL_PASSWORD=ragflow123
MYSQL_DATABASE=ragflow

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=ragflow
MINIO_SECRET_KEY=ragflow123
MINIO_BUCKET=ragflow

# LLM Configuration
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
OLLAMA_BASE_URL=http://localhost:11434

# Application Settings
RAGFLOW_PORT=80
RAGFLOW_HOST=0.0.0.0
LOG_LEVEL=INFO
EOF
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  ragflow-server:
    image: infiniflow/ragflow:latest
    ports:
      - "80:80"
    environment:
      - MYSQL_HOST=mysql
      - REDIS_HOST=redis
      - MINIO_ENDPOINT=minio:9000
    depends_on:
      - mysql
      - redis
      - minio
    volumes:
      - ./logs:/app/logs

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ragflow
      MYSQL_DATABASE: ragflow
      MYSQL_USER: ragflow
      MYSQL_PASSWORD: ragflow
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio
    environment:
      MINIO_ACCESS_KEY: ragflow
      MINIO_SECRET_KEY: ragflow123
    volumes:
      - minio_data:/data
    command: server /data

volumes:
  mysql_data:
  redis_data:
  minio_data:
```

## 🌐 Accessing RAGFlow

Once installed, access RAGFlow through your web browser:

```bash
# Local installation
open http://localhost:80

# Or with specific host
open http://your-server-ip:80
```

### Default Credentials
- **Username**: `admin`
- **Password**: `admin`

## 🏃‍♂️ Your First RAG Application

### Step 1: Create Knowledge Base

```python
import requests

# RAGFlow API base URL
BASE_URL = "http://localhost:80/api/v1"

# Authentication
headers = {
    "Authorization": "Bearer your_api_token"
}

# Create knowledge base
kb_data = {
    "name": "My First Knowledge Base",
    "description": "A sample knowledge base for testing",
    "embedding_model": "text-embedding-ada-002",
    "chunk_size": 512,
    "chunk_overlap": 50
}

response = requests.post(
    f"{BASE_URL}/knowledge-bases",
    json=kb_data,
    headers=headers
)

kb_id = response.json()["data"]["id"]
print(f"Created knowledge base: {kb_id}")
```

### Step 2: Upload Documents

```python
# Upload document
files = {
    'file': open('sample_document.pdf', 'rb')
}

upload_data = {
    'knowledge_base_id': kb_id,
    'parser_config': {
        'chunk_size': 512,
        'chunk_overlap': 50,
        'parsing_method': 'auto'
    }
}

response = requests.post(
    f"{BASE_URL}/documents/upload",
    files=files,
    data={'data': json.dumps(upload_data)},
    headers=headers
)

document_id = response.json()["data"]["id"]
```

### Step 3: Query the Knowledge Base

```python
# Ask a question
query_data = {
    "knowledge_base_id": kb_id,
    "question": "What is RAGFlow?",
    "top_k": 5,
    "similarity_threshold": 0.7
}

response = requests.post(
    f"{BASE_URL}/chat/completions",
    json=query_data,
    headers=headers
)

answer = response.json()["data"]["answer"]
print(f"Answer: {answer}")
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 80
sudo lsof -i :80

# Kill the process
sudo kill -9 <PID>

# Or use different port
docker-compose up -d --scale ragflow-server=1 -p 8080:80
```

#### Database Connection Issues
```bash
# Check MySQL container
docker-compose logs mysql

# Reset database
docker-compose down -v
docker-compose up -d mysql
```

#### Memory Issues
```bash
# Check system resources
free -h
df -h

# Increase Docker memory limit
# Docker Desktop: Preferences > Resources > Memory
```

### Health Checks

```bash
# Check service health
curl http://localhost:80/health

# Check database connectivity
docker-compose exec mysql mysql -u ragflow -p ragflow -e "SELECT 1"

# Check Redis connectivity
docker-compose exec redis redis-cli ping
```

## 📊 Monitoring Setup

### Basic Monitoring

```python
import requests
import time
from datetime import datetime

class RAGFlowMonitor:
    def __init__(self, base_url="http://localhost:80"):
        self.base_url = base_url

    def check_health(self):
        """Check RAGFlow health status"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_system_info(self):
        """Get system information"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/system/info")
            return response.json()
        except:
            return None

    def monitor_loop(self):
        """Continuous monitoring loop"""
        while True:
            health = self.check_health()
            timestamp = datetime.now().isoformat()

            status = "HEALTHY" if health else "UNHEALTHY"
            print(f"[{timestamp}] RAGFlow Status: {status}")

            time.sleep(30)  # Check every 30 seconds

# Usage
monitor = RAGFlowMonitor()
monitor.monitor_loop()
```

## 🎯 Key Concepts

### Knowledge Base
A container for documents and their processed content. Each knowledge base can have:
- Multiple documents
- Custom parsing configurations
- Different embedding models
- Specific retrieval settings

### Document Processing
RAGFlow supports various document formats:
- **Text files**: .txt, .md, .json
- **Office documents**: .docx, .xlsx, .pptx
- **PDF files**: .pdf with text extraction
- **Web content**: URLs and HTML
- **Code files**: .py, .js, .java, etc.

### Chunking Strategies
- **Fixed size**: Equal-sized chunks
- **Sentence-based**: Natural language boundaries
- **Semantic**: Meaning-based segmentation
- **Hierarchical**: Multi-level chunking

## 🏆 Achievement Unlocked!

Congratulations! 🎉 You've successfully:

- ✅ Installed RAGFlow using Docker
- ✅ Configured the system components
- ✅ Created your first knowledge base
- ✅ Uploaded and processed documents
- ✅ Performed your first Q&A query
- ✅ Set up basic monitoring

## 🚀 What's Next?

Now that you have RAGFlow up and running, let's dive deeper into document processing techniques in [Chapter 2: Document Processing](02-document-processing.md).

---

**Practice what you've learned:**
1. Experiment with different installation methods
2. Create multiple knowledge bases with different configurations
3. Upload various document types and observe processing
4. Test different query types and parameters
5. Set up monitoring for your RAGFlow instance

*What document type are you most excited to process with RAGFlow?* 📄

## What Problem Does This Solve?

Most teams struggle here because the hard part is not writing more code, but deciding clear boundaries for `ragflow`, `docker`, `compose` so behavior stays predictable as complexity grows.

In practical terms, this chapter helps you avoid three common failures:

- coupling core logic too tightly to one implementation path
- missing the handoff boundaries between setup, execution, and validation
- shipping changes without clear rollback or observability strategy

After working through this chapter, you should be able to reason about `Chapter 1: Getting Started with RAGFlow` as an operating subsystem inside **RAGFlow Tutorial: Complete Guide to Open-Source RAG Engine**, with explicit contracts for inputs, state transitions, and outputs.

Use the implementation notes around `mysql`, `response`, `Check` as your checklist when adapting these patterns to your own repository.

## How it Works Under the Hood

Under the hood, `Chapter 1: Getting Started with RAGFlow` usually follows a repeatable control path:

1. **Context bootstrap**: initialize runtime config and prerequisites for `ragflow`.
2. **Input normalization**: shape incoming data so `docker` receives stable contracts.
3. **Core execution**: run the main logic branch and propagate intermediate state through `compose`.
4. **Policy and safety checks**: enforce limits, auth scopes, and failure boundaries.
5. **Output composition**: return canonical result payloads for downstream consumers.
6. **Operational telemetry**: emit logs/metrics needed for debugging and performance tuning.

When debugging, walk this sequence in order and confirm each stage has explicit success/failure conditions.

## Source Walkthrough

Use the following upstream sources to verify implementation details while reading this chapter:

- [GitHub Repository](https://github.com/infiniflow/ragflow)
  Why it matters: authoritative reference on `GitHub Repository` (github.com).
- [AI Codebase Knowledge Builder](https://github.com/johnxie/awesome-code-docs)
  Why it matters: authoritative reference on `AI Codebase Knowledge Builder` (github.com).

Suggested trace strategy:
- search upstream code for `ragflow` and `docker` to map concrete implementation paths
- compare docs claims against actual runtime/config code before reusing patterns in production

## Chapter Connections

- [Tutorial Index](index.md)
- [Next Chapter: Chapter 2: Document Processing](02-document-processing.md)
- [Main Catalog](../../README.md#-tutorial-catalog)
- [A-Z Tutorial Directory](../../discoverability/tutorial-directory.md)
