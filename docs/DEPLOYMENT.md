# 🚀 Deployment Guide

## Overview

This guide covers deploying the Network Infrastructure Knowledge Graph system in various environments, from development to production scale.

---

## 📋 Prerequisites

### System Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- Python: 3.8+
- Neo4j: 4.0+

**Recommended for Production:**
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 100GB+ SSD
- Python: 3.11+
- Neo4j: 5.0+

### Dependencies

```bash
# Core dependencies
pip install neo4j>=5.0.0
pip install pydantic>=2.0.0
pip install streamlit>=1.28.0
pip install plotly>=5.0.0
pip install pyvis>=0.3.0
pip install networkx>=3.0.0

# Optional dependencies
pip install uvicorn>=0.23.0  # For FastAPI deployment
pip install gunicorn>=21.0.0  # For production WSGI server
pip install redis>=4.0.0  # For caching
```

---

## 🐳 Docker Deployment

### Basic Docker Setup

Create a `Dockerfile`:

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.0
    container_name: neo4j-kg
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_dbms_memory_heap_initial__size: 512m
      NEO4J_dbms_memory_heap_max__size: 2G
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    restart: unless-stopped

  kg-app:
    build: .
    container_name: kg-app
    ports:
      - "8501:8501"
    depends_on:
      - neo4j
    environment:
      NEO4J_URI: bolt://neo4j:7687
      NEO4J_USERNAME: neo4j
      NEO4J_PASSWORD: password
    volumes:
      - ./visualizations:/app/visualizations
    restart: unless-stopped

volumes:
  neo4j_data:
  neo4j_logs:
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f kg-app

# Stop services
docker-compose down
```

---

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Deployment

**1. Launch EC2 Instance**

```bash
# Launch Ubuntu 20.04 LTS instance
# Recommended: t3.large or larger
# Security group: Allow ports 22, 7474, 7687, 8501
```

**2. Install Dependencies**

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Install Git
sudo apt install git -y

# Clone repository
git clone https://github.com/your-username/KGs.git
cd KGs
```

**3. Configure Security**

```bash
# Create environment file
cat > .env << EOF
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-secure-password
EOF

# Set secure permissions
chmod 600 .env
```

**4. Deploy**

```bash
# Deploy with Docker Compose
docker-compose up -d

# Generate initial data
docker-compose exec kg-app python main.py
```

#### ECS Deployment

Create `task-definition.json`:

```json
{
  "family": "kg-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "kg-app",
      "image": "your-account.dkr.ecr.region.amazonaws.com/kg-app:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NEO4J_URI",
          "value": "bolt://your-neo4j-endpoint:7687"
        }
      ],
      "secrets": [
        {
          "name": "NEO4J_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:neo4j-password"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/kg-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Cloud Run Deployment

**1. Build and Push Image**

```bash
# Build image
docker build -t gcr.io/your-project/kg-app .

# Push to Container Registry
docker push gcr.io/your-project/kg-app
```

**2. Deploy to Cloud Run**

```bash
# Deploy service
gcloud run deploy kg-app \
    --image gcr.io/your-project/kg-app \
    --platform managed \
    --region us-central1 \
    --set-env-vars NEO4J_URI=bolt://your-neo4j-ip:7687 \
    --set-env-vars NEO4J_USERNAME=neo4j \
    --set-env-vars NEO4J_PASSWORD=your-password \
    --port 8501 \
    --memory 2Gi \
    --cpu 1 \
    --allow-unauthenticated
```

#### GKE Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kg-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kg-app
  template:
    metadata:
      labels:
        app: kg-app
    spec:
      containers:
      - name: kg-app
        image: gcr.io/your-project/kg-app:latest
        ports:
        - containerPort: 8501
        env:
        - name: NEO4J_URI
          value: "bolt://neo4j-service:7687"
        - name: NEO4J_USERNAME
          value: "neo4j"
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: neo4j-secret
              key: password
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: kg-app-service
spec:
  selector:
    app: kg-app
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

### Azure Deployment

#### Container Instances

```bash
# Create resource group
az group create --name kg-rg --location eastus

# Create container instance
az container create \
    --resource-group kg-rg \
    --name kg-app \
    --image your-registry.azurecr.io/kg-app:latest \
    --ports 8501 \
    --dns-name-label kg-app-unique \
    --environment-variables \
        NEO4J_URI=bolt://your-neo4j-ip:7687 \
        NEO4J_USERNAME=neo4j \
    --secure-environment-variables \
        NEO4J_PASSWORD=your-password \
    --cpu 2 \
    --memory 4
```

---

## 🔧 Production Configuration

### Environment Variables

Create a comprehensive `.env` file:

```bash
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-secure-password
NEO4J_DATABASE=neo4j

# Application Configuration
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Data Generation (for initial setup)
SWITCH_COUNT=10
SERVER_COUNT=20
VMS_PER_SERVER=15
PODS_PER_VM=50
CONTAINERS_PER_POD=3

# Caching Configuration
REDIS_URI=redis://localhost:6379
CACHE_TTL=3600

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-domain.com

# Performance
MAX_WORKERS=4
QUERY_TIMEOUT=30
CONNECTION_POOL_SIZE=50
```

### Neo4j Production Configuration

Create `neo4j.conf`:

```conf
# Memory settings
dbms.memory.heap.initial_size=2g
dbms.memory.heap.max_size=4g
dbms.memory.pagecache.size=2g

# Network settings
dbms.default_listen_address=0.0.0.0
dbms.connector.bolt.listen_address=:7687
dbms.connector.http.listen_address=:7474

# Security
dbms.security.auth_enabled=true
dbms.security.procedures.unrestricted=apoc.*,algo.*

# Performance
dbms.query_cache_size=100
dbms.query_cache.skip_warmup=true
dbms.transaction.timeout=60s

# Logging
dbms.logs.query.enabled=true
dbms.logs.query.threshold=1000ms
```

### Application Configuration

Create `config/production.py`:

```python
import os
from typing import Optional

class ProductionConfig:
    # Database
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DATABASE: str = os.getenv("NEO4J_DATABASE", "neo4j")
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Performance
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    QUERY_TIMEOUT: int = int(os.getenv("QUERY_TIMEOUT", "30"))
    CONNECTION_POOL_SIZE: int = int(os.getenv("CONNECTION_POOL_SIZE", "50"))
    
    # Caching
    REDIS_URI: Optional[str] = os.getenv("REDIS_URI")
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "").split(",")
```

---

## 📊 Monitoring and Observability

### Health Checks

Create `health_check.py`:

```python
from kg.database import Neo4jKnowledgeGraph
import json
import time

def health_check():
    """Comprehensive health check"""
    start_time = time.time()
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {}
    }
    
    try:
        # Database connectivity
        kg = Neo4jKnowledgeGraph()
        result = kg.execute_query("RETURN 1 as test")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time": f"{time.time() - start_time:.3f}s"
        }
        
        # Data availability
        stats = kg.get_statistics()
        health_status["checks"]["data"] = {
            "status": "healthy" if stats["total_entities"] > 0 else "unhealthy",
            "entities": stats["total_entities"],
            "relationships": stats["total_relationships"]
        }
        
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    return health_status

if __name__ == "__main__":
    print(json.dumps(health_check(), indent=2))
```

### Logging Configuration

Create `logging.conf`:

```ini
[loggers]
keys=root,kg

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_kg]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=kg
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('kg.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

### Prometheus Metrics

Create `metrics.py`:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import functools

# Metrics
query_counter = Counter('kg_queries_total', 'Total number of queries')
query_duration = Histogram('kg_query_duration_seconds', 'Query duration')
entity_count = Gauge('kg_entities_total', 'Total number of entities')
relationship_count = Gauge('kg_relationships_total', 'Total number of relationships')

def track_query_metrics(func):
    """Decorator to track query metrics"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        query_counter.inc()
        try:
            result = func(*args, **kwargs)
            query_duration.observe(time.time() - start_time)
            return result
        except Exception as e:
            query_duration.observe(time.time() - start_time)
            raise
    return wrapper

def update_entity_metrics(kg):
    """Update entity count metrics"""
    stats = kg.get_statistics()
    entity_count.set(stats['total_entities'])
    relationship_count.set(stats['total_relationships'])

# Start metrics server
start_http_server(8000)
```

---

## 🔒 Security Considerations

### Authentication and Authorization

```python
# config/auth.py
from functools import wraps
import jwt
import os

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'No token provided'}, 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            current_user = payload['user']
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token'}, 401
        
        return f(current_user, *args, **kwargs)
    return decorated
```

### Network Security

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.0
    networks:
      - kg-internal
    environment:
      NEO4J_AUTH: neo4j/password
    volumes:
      - neo4j_data:/data
    # Don't expose ports externally in production

  kg-app:
    build: .
    networks:
      - kg-internal
      - kg-external
    environment:
      NEO4J_URI: bolt://neo4j:7687

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - kg-external
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl

networks:
  kg-internal:
    driver: bridge
    internal: true
  kg-external:
    driver: bridge
```

### SSL/TLS Configuration

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://kg-app:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 🔄 Backup and Recovery

### Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/neo4j"
NEO4J_HOME="/var/lib/neo4j"

# Create backup directory
mkdir -p $BACKUP_DIR

# Stop Neo4j
systemctl stop neo4j

# Create backup
tar -czf $BACKUP_DIR/neo4j_backup_$DATE.tar.gz $NEO4J_HOME/data

# Start Neo4j
systemctl start neo4j

# Keep only last 7 days of backups
find $BACKUP_DIR -name "neo4j_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: neo4j_backup_$DATE.tar.gz"
```

### Application Backup

```bash
#!/bin/bash
# app_backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/kg-app"
APP_DIR="/opt/kg-app"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application data
tar -czf $BACKUP_DIR/kg_app_backup_$DATE.tar.gz \
    $APP_DIR/visualizations \
    $APP_DIR/config \
    $APP_DIR/.env

echo "Application backup completed: kg_app_backup_$DATE.tar.gz"
```

### Automated Backup with Cron

```bash
# Add to crontab
crontab -e

# Backup database daily at 2 AM
0 2 * * * /opt/scripts/backup.sh

# Backup application weekly on Sundays at 3 AM
0 3 * * 0 /opt/scripts/app_backup.sh
```

---

## 📈 Performance Optimization

### Neo4j Tuning

```conf
# Memory optimization
dbms.memory.heap.initial_size=8g
dbms.memory.heap.max_size=8g
dbms.memory.pagecache.size=4g

# Query optimization
dbms.query_cache_size=1000
cypher.default_index_provider=range-1.0

# Connection pooling
dbms.connector.bolt.thread_pool_min_size=5
dbms.connector.bolt.thread_pool_max_size=400
```

### Application Caching

```python
# cache.py
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

---

## 🔍 Troubleshooting Production Issues

### Common Issues

1. **High Memory Usage**
   ```bash
   # Check Neo4j memory usage
   docker exec neo4j-kg neo4j-admin memrec
   
   # Adjust heap size
   NEO4J_dbms_memory_heap_max__size=4G
   ```

2. **Slow Queries**
   ```cypher
   -- Enable query logging
   CALL dbms.setConfigValue('dbms.logs.query.enabled', 'true');
   
   -- Check slow queries
   CALL dbms.listQueries() YIELD queryId, query, elapsedTimeMillis 
   WHERE elapsedTimeMillis > 1000 
   RETURN queryId, query, elapsedTimeMillis;
   ```

3. **Connection Pool Exhaustion**
   ```python
   # Increase connection pool size
   from neo4j import GraphDatabase
   
   driver = GraphDatabase.driver(
       uri, 
       auth=(username, password),
       max_connection_pool_size=50
   )
   ```

### Monitoring Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f --tail=100 kg-app

# Check resource usage
docker stats

# Neo4j metrics
curl -H "Accept: application/json" http://localhost:7474/db/manage/server/jmx/domain/org.neo4j/

# Health check
curl http://localhost:8501/health
```

---

This deployment guide provides comprehensive instructions for deploying the Knowledge Graph system in various environments. Choose the deployment method that best fits your infrastructure and requirements. 