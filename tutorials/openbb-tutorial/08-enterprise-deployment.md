---
layout: default
title: "Chapter 8: Production Deployment"
parent: "OpenBB Tutorial"
nav_order: 8
---

# Chapter 8: Production Deployment

This chapter covers deploying OpenBB-based applications to production, including API service deployment, task scheduling, workflow automation, monitoring, and enterprise architecture patterns. You'll learn how to build reliable, scalable financial data services.

## 🎯 What You'll Learn

- FastAPI service deployment for OpenBB
- Scheduled data collection and analysis pipelines
- Workflow automation and alerting
- Docker and Kubernetes deployment patterns
- Monitoring, logging, and enterprise security

## 📊 Production Architecture

```mermaid
graph TB
    subgraph "API Layer"
        A[FastAPI Service]
        B[Authentication]
        C[Rate Limiting]
    end

    subgraph "Processing Layer"
        D[Task Scheduler]
        E[Analysis Pipelines]
        F[Alert Engine]
    end

    subgraph "Data Layer"
        G[PostgreSQL]
        H[Redis Cache]
        I[Object Storage]
    end

    subgraph "Infrastructure"
        J[Docker / K8s]
        K[Load Balancer]
        L[Monitoring]
        M[Log Aggregation]
    end

    K --> A
    A --> B
    B --> C
    C --> D
    C --> E
    D --> F
    E --> G
    E --> H
    F --> I
    J --> A
    J --> D
    L --> A
    L --> D
    M --> A
    M --> D
```

## 🚀 API Service Deployment

### FastAPI Application

```python
"""
OpenBB API Service - main.py
Production-ready financial data API
"""
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
import logging
import time
import os

from openbb import obb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("openbb-api")

# Initialize FastAPI
app = FastAPI(
    title="OpenBB Financial Data API",
    description="Production API for financial data and analysis",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
API_KEYS = set(os.getenv("API_KEYS", "").split(","))


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    """Verify API token"""
    if credentials.credentials not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return credentials.credentials


# Request/Response models
class StockQuoteRequest(BaseModel):
    symbol: str = Field(description="Stock ticker symbol")
    provider: Optional[str] = Field(default="fmp", description="Data provider")


class HistoricalRequest(BaseModel):
    symbol: str
    start_date: date
    end_date: Optional[date] = None
    interval: Optional[str] = "1d"


class AnalysisRequest(BaseModel):
    symbol: str
    start_date: date
    end_date: Optional[date] = None
    indicators: List[str] = ["sma_20", "rsi", "macd"]


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    uptime_seconds: float


# Startup time tracking
START_TIME = time.time()


# Middleware for request logging and timing
@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={duration:.3f}s"
    )
    response.headers["X-Response-Time"] = f"{duration:.3f}"
    return response


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Service health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


# Data endpoints
@app.post("/api/v1/quote")
async def get_quote(
    request: StockQuoteRequest,
    token: str = Depends(verify_token),
):
    """Get real-time stock quote"""
    try:
        data = obb.equity.price.quote(
            request.symbol, provider=request.provider
        )
        return {"data": data.to_dataframe().to_dict("records")}
    except Exception as e:
        logger.error(f"Quote error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/historical")
async def get_historical(
    request: HistoricalRequest,
    token: str = Depends(verify_token),
):
    """Get historical price data"""
    try:
        data = obb.equity.price.historical(
            request.symbol,
            start_date=str(request.start_date),
            end_date=str(request.end_date) if request.end_date else None,
            interval=request.interval,
        )
        df = data.to_dataframe()
        df.index = df.index.astype(str)
        return {"data": df.to_dict("records"), "count": len(df)}
    except Exception as e:
        logger.error(f"Historical error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analysis")
async def run_analysis(
    request: AnalysisRequest,
    token: str = Depends(verify_token),
):
    """Run technical analysis"""
    try:
        data = obb.equity.price.historical(
            request.symbol,
            start_date=str(request.start_date),
            end_date=str(request.end_date) if request.end_date else None,
        )
        df = data.to_dataframe()

        results = {"symbol": request.symbol}

        if "sma_20" in request.indicators:
            df['sma_20'] = df['close'].rolling(20).mean()
            results['sma_20'] = round(df['sma_20'].iloc[-1], 2)

        if "rsi" in request.indicators:
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            results['rsi'] = round(rsi.iloc[-1], 2)

        if "macd" in request.indicators:
            ema12 = df['close'].ewm(span=12).mean()
            ema26 = df['close'].ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            results['macd'] = round(macd.iloc[-1], 4)
            results['macd_signal'] = round(signal.iloc[-1], 4)

        return results
    except Exception as e:
        logger.error(f"Analysis error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info",
    )
```

### Rate Limiting Middleware

```python
"""Rate limiting for the API service"""
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Token bucket rate limiting"""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Extract client identifier
        client_id = request.headers.get(
            "Authorization", request.client.host
        )

        # Check rate limit
        now = time.time()
        self.requests[client_id] = [
            t for t in self.requests[client_id] if now - t < 60
        ]

        if len(self.requests[client_id]) >= self.rpm:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.rpm),
                    "X-RateLimit-Remaining": "0",
                },
            )

        self.requests[client_id].append(now)
        remaining = self.rpm - len(self.requests[client_id])

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.rpm)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

# Add to the FastAPI app
# app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
```

## ⏰ Task Scheduling

### Scheduled Data Collection

```python
"""
Scheduled data pipeline - scheduler.py
"""
import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Callable, List
from openbb import obb
import pandas as pd

logger = logging.getLogger("openbb-scheduler")


class DataPipeline:
    """Scheduled financial data collection pipeline"""

    def __init__(self, db_connection_string: str = None):
        self.watchlist = []
        self.jobs = []
        self.db = db_connection_string

    def add_watchlist(self, symbols: list):
        """Add symbols to monitoring watchlist"""
        self.watchlist.extend(symbols)
        self.watchlist = list(set(self.watchlist))

    def collect_daily_prices(self):
        """Collect end-of-day prices for all watchlist symbols"""
        logger.info(f"Collecting daily prices for {len(self.watchlist)} symbols")
        results = []

        for symbol in self.watchlist:
            try:
                data = obb.equity.price.historical(
                    symbol,
                    start_date=str(
                        (datetime.now() - timedelta(days=5)).date()
                    ),
                )
                df = data.to_dataframe()
                latest = df.iloc[-1]
                results.append({
                    "symbol": symbol,
                    "date": str(df.index[-1]),
                    "open": latest['open'],
                    "high": latest['high'],
                    "low": latest['low'],
                    "close": latest['close'],
                    "volume": latest['volume'],
                })
                logger.info(f"  {symbol}: ${latest['close']:.2f}")
            except Exception as e:
                logger.error(f"  Error fetching {symbol}: {e}")

        self._store_results("daily_prices", results)
        return results

    def collect_fundamentals(self):
        """Collect fundamental data quarterly"""
        logger.info("Collecting fundamental data")

        for symbol in self.watchlist:
            try:
                income = obb.equity.fundamental.income(
                    symbol, period="quarterly", limit=1
                ).to_dataframe()
                balance = obb.equity.fundamental.balance(
                    symbol, period="quarterly", limit=1
                ).to_dataframe()

                logger.info(
                    f"  {symbol}: Revenue=${income.iloc[0].get('revenue', 0) / 1e9:.2f}B"
                )
            except Exception as e:
                logger.error(f"  Error fetching fundamentals for {symbol}: {e}")

    def run_technical_scan(self):
        """Run technical analysis scan across watchlist"""
        logger.info("Running technical scan")
        alerts = []

        for symbol in self.watchlist:
            try:
                data = obb.equity.price.historical(
                    symbol,
                    start_date=str(
                        (datetime.now() - timedelta(days=100)).date()
                    ),
                ).to_dataframe()

                # RSI check
                delta = data['close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                current_rsi = rsi.iloc[-1]

                # Moving average crossover check
                sma_20 = data['close'].rolling(20).mean().iloc[-1]
                sma_50 = data['close'].rolling(50).mean().iloc[-1]

                if current_rsi < 30:
                    alerts.append({
                        "symbol": symbol,
                        "alert": "RSI Oversold",
                        "value": round(current_rsi, 2),
                    })
                elif current_rsi > 70:
                    alerts.append({
                        "symbol": symbol,
                        "alert": "RSI Overbought",
                        "value": round(current_rsi, 2),
                    })

                if sma_20 > sma_50:
                    prev_sma_20 = data['close'].rolling(20).mean().iloc[-2]
                    prev_sma_50 = data['close'].rolling(50).mean().iloc[-2]
                    if prev_sma_20 <= prev_sma_50:
                        alerts.append({
                            "symbol": symbol,
                            "alert": "Golden Cross",
                            "value": f"SMA20={sma_20:.2f} > SMA50={sma_50:.2f}",
                        })

            except Exception as e:
                logger.error(f"  Scan error for {symbol}: {e}")

        if alerts:
            self._send_alerts(alerts)
        return alerts

    def _store_results(self, table: str, results: list):
        """Store results to database or file"""
        df = pd.DataFrame(results)
        filename = f"{table}_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        logger.info(f"Stored {len(results)} records to {filename}")

    def _send_alerts(self, alerts: list):
        """Send alert notifications"""
        for alert in alerts:
            logger.warning(
                f"ALERT: {alert['symbol']} - {alert['alert']} ({alert['value']})"
            )
        # In production, integrate with email, Slack, or PagerDuty

    def setup_schedule(self):
        """Configure the schedule"""
        # Daily price collection at market close
        schedule.every().monday.at("16:30").do(self.collect_daily_prices)
        schedule.every().tuesday.at("16:30").do(self.collect_daily_prices)
        schedule.every().wednesday.at("16:30").do(self.collect_daily_prices)
        schedule.every().thursday.at("16:30").do(self.collect_daily_prices)
        schedule.every().friday.at("16:30").do(self.collect_daily_prices)

        # Technical scan every hour during market hours
        schedule.every().hour.do(self.run_technical_scan)

        # Fundamental data quarterly
        schedule.every(90).days.do(self.collect_fundamentals)

        logger.info("Schedule configured")

    def run(self):
        """Run the scheduler loop"""
        self.setup_schedule()
        logger.info("Scheduler started")

        while True:
            schedule.run_pending()
            time.sleep(60)


# Usage
pipeline = DataPipeline()
pipeline.add_watchlist([
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "META", "TSLA", "JPM", "JNJ", "PG",
])
# pipeline.run()  # Run in production
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -r appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEYS=${API_KEYS}
      - OPENBB_API_KEY_FMP=${OPENBB_API_KEY_FMP}
      - OPENBB_API_KEY_POLYGON=${OPENBB_API_KEY_POLYGON}
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://user:pass@postgres:5432/openbb
      - LOG_LEVEL=info
    depends_on:
      - redis
      - postgres
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "2.0"

  scheduler:
    build: .
    command: python scheduler.py
    environment:
      - OPENBB_API_KEY_FMP=${OPENBB_API_KEY_FMP}
      - OPENBB_API_KEY_POLYGON=${OPENBB_API_KEY_POLYGON}
      - DATABASE_URL=postgresql://user:pass@postgres:5432/openbb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  dashboard:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: openbb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
      - dashboard
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

### Requirements File

```text
# requirements.txt
openbb>=4.0.0
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
redis>=4.5.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
schedule>=1.2.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
requests>=2.31.0
python-dotenv>=1.0.0
```

## 📊 Monitoring and Observability

### Application Monitoring

```python
"""
Monitoring and metrics collection - monitoring.py
"""
import time
import psutil
import logging
from datetime import datetime
from typing import Dict
from dataclasses import dataclass, field

logger = logging.getLogger("openbb-monitor")


@dataclass
class MetricsCollector:
    """Collect and report application metrics"""

    request_count: int = 0
    error_count: int = 0
    total_response_time: float = 0.0
    endpoint_metrics: Dict[str, dict] = field(default_factory=dict)

    def record_request(self, endpoint: str, duration: float, success: bool):
        """Record a request metric"""
        self.request_count += 1
        self.total_response_time += duration

        if not success:
            self.error_count += 1

        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                "count": 0, "errors": 0, "total_time": 0.0,
                "max_time": 0.0, "min_time": float('inf'),
            }

        metrics = self.endpoint_metrics[endpoint]
        metrics["count"] += 1
        metrics["total_time"] += duration
        metrics["max_time"] = max(metrics["max_time"], duration)
        metrics["min_time"] = min(metrics["min_time"], duration)
        if not success:
            metrics["errors"] += 1

    def get_summary(self) -> dict:
        """Get metrics summary"""
        avg_response = (
            self.total_response_time / self.request_count
            if self.request_count > 0 else 0
        )
        error_rate = (
            self.error_count / self.request_count * 100
            if self.request_count > 0 else 0
        )

        return {
            "timestamp": datetime.now().isoformat(),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate_pct": round(error_rate, 2),
            "avg_response_time_ms": round(avg_response * 1000, 2),
            "endpoints": {
                ep: {
                    "count": m["count"],
                    "errors": m["errors"],
                    "avg_time_ms": round(m["total_time"] / m["count"] * 1000, 2),
                    "max_time_ms": round(m["max_time"] * 1000, 2),
                }
                for ep, m in self.endpoint_metrics.items()
            },
        }


class SystemMonitor:
    """Monitor system resource usage"""

    @staticmethod
    def get_system_metrics() -> dict:
        """Collect system-level metrics"""
        cpu_pct = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "cpu_percent": cpu_pct,
            "memory_percent": memory.percent,
            "memory_used_gb": round(memory.used / (1024 ** 3), 2),
            "memory_total_gb": round(memory.total / (1024 ** 3), 2),
            "disk_percent": disk.percent,
            "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        }

    @staticmethod
    def check_health() -> dict:
        """Run health checks"""
        checks = {}

        # Check OpenBB connectivity
        try:
            from openbb import obb
            obb.equity.price.quote("AAPL")
            checks["openbb"] = "healthy"
        except Exception as e:
            checks["openbb"] = f"unhealthy: {e}"

        # Check system resources
        memory = psutil.virtual_memory()
        checks["memory"] = (
            "healthy" if memory.percent < 85
            else "warning" if memory.percent < 95
            else "critical"
        )

        cpu_pct = psutil.cpu_percent(interval=1)
        checks["cpu"] = (
            "healthy" if cpu_pct < 80
            else "warning" if cpu_pct < 95
            else "critical"
        )

        checks["overall"] = (
            "healthy" if all(
                v == "healthy" for v in checks.values()
            ) else "degraded"
        )

        return checks


# Integration with FastAPI
metrics = MetricsCollector()
system_monitor = SystemMonitor()

# Add metrics endpoint to the API
# @app.get("/metrics")
# async def get_metrics():
#     return {
#         "application": metrics.get_summary(),
#         "system": system_monitor.get_system_metrics(),
#         "health": system_monitor.check_health(),
#     }
```

### Alerting System

```python
"""Alert management for production monitoring"""
import smtplib
from email.mime.text import MIMEText
from typing import List, Optional
import json
import requests


class AlertManager:
    """Manage and dispatch alerts"""

    def __init__(self):
        self.channels = {}
        self.alert_history = []

    def add_channel(self, name: str, handler):
        """Register an alert channel"""
        self.channels[name] = handler

    def send_alert(self, severity: str, title: str, message: str,
                   channels: Optional[List[str]] = None):
        """Send alert to specified channels"""
        alert = {
            "severity": severity,
            "title": title,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        self.alert_history.append(alert)

        target_channels = channels or list(self.channels.keys())
        for channel_name in target_channels:
            if channel_name in self.channels:
                try:
                    self.channels[channel_name](alert)
                except Exception as e:
                    logger.error(f"Alert dispatch failed for {channel_name}: {e}")


def slack_handler(alert: dict):
    """Send alert to Slack"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return

    color_map = {
        "critical": "#f44336",
        "warning": "#ff9800",
        "info": "#2196f3",
    }

    payload = {
        "attachments": [{
            "color": color_map.get(alert["severity"], "#666"),
            "title": alert["title"],
            "text": alert["message"],
            "footer": f"OpenBB Alert | {alert['timestamp']}",
        }]
    }
    requests.post(webhook_url, json=payload, timeout=10)


def email_handler(alert: dict):
    """Send alert via email"""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    recipients = os.getenv("ALERT_EMAILS", "").split(",")

    if not smtp_user or not recipients:
        return

    msg = MIMEText(
        f"Severity: {alert['severity']}\n\n{alert['message']}\n\n"
        f"Time: {alert['timestamp']}"
    )
    msg["Subject"] = f"[{alert['severity'].upper()}] {alert['title']}"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


# Usage
alert_manager = AlertManager()
alert_manager.add_channel("slack", slack_handler)
alert_manager.add_channel("email", email_handler)

# Trigger alerts based on conditions
# alert_manager.send_alert(
#     severity="warning",
#     title="High API Error Rate",
#     message="Error rate exceeded 5% in the last 10 minutes",
# )
```

## ☸️ Kubernetes Deployment

### Kubernetes Manifests

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openbb-api
  labels:
    app: openbb-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: openbb-api
  template:
    metadata:
      labels:
        app: openbb-api
    spec:
      containers:
        - name: openbb-api
          image: openbb-api:latest
          ports:
            - containerPort: 8000
          env:
            - name: API_KEYS
              valueFrom:
                secretKeyRef:
                  name: openbb-secrets
                  key: api-keys
            - name: OPENBB_API_KEY_FMP
              valueFrom:
                secretKeyRef:
                  name: openbb-secrets
                  key: fmp-key
            - name: REDIS_URL
              value: "redis://redis-service:6379"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: openbb-secrets
                  key: database-url
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "2Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: openbb-api-service
spec:
  selector:
    app: openbb-api
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: openbb-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: openbb-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

## 🔒 Security Best Practices

### Enterprise Security Patterns

```mermaid
graph LR
    A[Client] --> B[TLS Termination]
    B --> C[Authentication]
    C --> D[Authorization]
    D --> E[Rate Limiting]
    E --> F[API Service]
    F --> G[Encrypted Storage]
```

```python
"""Security utilities for production deployment"""
import hashlib
import secrets
from cryptography.fernet import Fernet
import os


class SecretManager:
    """Manage sensitive credentials securely"""

    def __init__(self):
        self._key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self._cipher = Fernet(self._key)

    def encrypt(self, value: str) -> str:
        """Encrypt a sensitive value"""
        return self._cipher.encrypt(value.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        """Decrypt an encrypted value"""
        return self._cipher.decrypt(encrypted.encode()).decode()

    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_key(key: str) -> str:
        """Hash an API key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()


class AuditLogger:
    """Log all API access for compliance"""

    def __init__(self, log_file: str = "audit.log"):
        self.logger = logging.getLogger("audit")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(message)s"
            )
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_access(self, user: str, endpoint: str,
                   action: str, result: str):
        """Log an API access event"""
        self.logger.info(
            f"user={user} | endpoint={endpoint} | "
            f"action={action} | result={result}"
        )

    def log_data_access(self, user: str, data_type: str,
                        symbols: list):
        """Log data access for compliance"""
        self.logger.info(
            f"user={user} | data_access={data_type} | "
            f"symbols={','.join(symbols)}"
        )
```

### Production Deployment Checklist

| Category | Item | Priority |
|:---------|:-----|:---------|
| **Security** | TLS/SSL certificates | Critical |
| **Security** | API key rotation policy | Critical |
| **Security** | Secrets management (Vault, AWS Secrets) | Critical |
| **Security** | Audit logging enabled | High |
| **Reliability** | Health check endpoints | Critical |
| **Reliability** | Automated failover | High |
| **Reliability** | Database backups | Critical |
| **Performance** | Redis caching layer | High |
| **Performance** | Connection pooling | High |
| **Performance** | Horizontal auto-scaling | Medium |
| **Monitoring** | Application metrics | High |
| **Monitoring** | Alerting (Slack, email) | High |
| **Monitoring** | Log aggregation | Medium |
| **Operations** | CI/CD pipeline | High |
| **Operations** | Rollback procedures | Critical |
| **Operations** | Runbook documentation | Medium |

## 🎯 Best Practices

### Production Deployment Guidelines

1. **Infrastructure as Code**
   - Version control all deployment configurations
   - Use Terraform or Pulumi for cloud infrastructure
   - Maintain separate configs for staging and production

2. **Zero-Downtime Deployments**
   - Use rolling updates or blue-green deployment
   - Always run health checks before routing traffic
   - Maintain backward-compatible API versions

3. **Data Management**
   - Cache market data with appropriate TTLs
   - Implement circuit breakers for external API calls
   - Maintain a local fallback data store

4. **Observability**
   - Instrument all critical paths with metrics
   - Set up alerts for error rate and latency thresholds
   - Retain logs for at least 90 days for compliance

5. **Disaster Recovery**
   - Document and test recovery procedures regularly
   - Maintain database replicas in separate availability zones
   - Keep encrypted backups of all configuration and secrets

## 🏆 Achievement Unlocked!

Congratulations! You've mastered:

- ✅ FastAPI service deployment with authentication and rate limiting
- ✅ Scheduled data collection and analysis pipelines
- ✅ Docker and Docker Compose deployment
- ✅ Kubernetes manifests with auto-scaling
- ✅ Monitoring, metrics, and alerting systems
- ✅ Enterprise security patterns and compliance logging

## 🎓 Tutorial Complete!

You've completed the entire OpenBB tutorial series! Here's a recap of everything covered:

| Chapter | Topic | Skills Gained |
|:--------|:------|:-------------|
| 1 | Getting Started | Installation, configuration, first analysis |
| 2 | Data Access | API keys, data providers, caching |
| 3 | Technical Analysis | Indicators, patterns, charting |
| 4 | Fundamental Analysis | Financial statements, DCF, ratios |
| 5 | Portfolio Management | Optimization, risk, backtesting |
| 6 | Custom Data Sources | Providers, pipelines, aggregation |
| 7 | Visualization | Dashboards, charts, reports |
| 8 | Production Deployment | APIs, scheduling, enterprise patterns |

---

**Practice what you've learned:**
1. Deploy the FastAPI service locally with Docker Compose
2. Set up scheduled data collection for your watchlist
3. Configure monitoring with health checks and alerts
4. Implement rate limiting and API key authentication
5. Build a CI/CD pipeline for automated deployments

*Built with insights from the [OpenBB](https://github.com/OpenBB-finance/OpenBB) project.*
