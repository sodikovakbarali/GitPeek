# Docker Setup Guide

This guide covers running GitPeek with Docker for consistent, reproducible environments.

## 🐳 Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/engine/install/))
- Docker Compose v2.0+ (included with Docker Desktop)

## 🚀 Quick Start (Production Mode)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek
```

### 2. Configure Environment (Optional)

Create a `.env` file in the project root:

```bash
# .env
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:3000/auth/callback
SECRET_KEY=your-secret-key-here
```

### 3. Start the Application

```bash
docker-compose up -d
```

That's it! 🎉

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### 4. Stop the Application

```bash
docker-compose down
```

To also remove volumes (database):

```bash
docker-compose down -v
```

## 🛠️ Development Mode

For development with hot-reload:

### 1. Start Development Environment

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This will:
- ✅ Mount source code as volumes for live editing
- ✅ Enable hot-reload for both frontend and backend
- ✅ Expose frontend on http://localhost:5173 (Vite dev server)
- ✅ Expose backend on http://localhost:8000 with auto-reload

### 2. Make Changes

Edit files locally - changes will be reflected immediately!

### 3. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📦 Building Images

### Build All Images

```bash
docker-compose build
```

### Build Specific Service

```bash
docker-compose build backend
docker-compose build frontend
```

### Build with No Cache

```bash
docker-compose build --no-cache
```

## 🔍 Useful Commands

### Check Service Status

```bash
docker-compose ps
```

### Execute Commands in Container

```bash
# Backend shell
docker-compose exec backend /bin/bash

# Frontend shell
docker-compose exec frontend /bin/sh

# Run backend tests
docker-compose exec backend pytest

# Install new backend dependency
docker-compose exec backend poetry add <package-name>

# Install new frontend dependency
docker-compose exec frontend npm install <package-name>
```

### View Real-time Logs

```bash
docker-compose logs -f
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

## 🧪 Running Tests in Docker

### Backend Tests

```bash
# Run tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Run specific test file
docker-compose exec backend pytest app/tests/test_routes.py
```

### Frontend Tests

```bash
# Run tests
docker-compose exec frontend npm test

# Run with coverage
docker-compose exec frontend npm run test:coverage
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Docker Compose                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐   ┌──────────────┐   │
│  │   Frontend   │   │   Backend    │   │
│  │  (Node 20)   │   │ (Python 3.11)│   │
│  │   Port: 80   │   │  Port: 8000  │   │
│  │    Nginx     │   │   FastAPI    │   │
│  └──────────────┘   └──────────────┘   │
│         │                   │           │
│         └───────┬───────────┘           │
│                 │                       │
│          gitpeek-network                │
│                 │                       │
│         ┌───────▼───────┐               │
│         │  backend-data │               │
│         │    (Volume)   │               │
│         └───────────────┘               │
└─────────────────────────────────────────┘
```

## 🔐 Security Best Practices

### For Production Deployment:

1. **Use secrets management:**
   ```bash
   # Use Docker secrets or external secret managers
   docker secret create github_client_id ./secrets/client_id.txt
   ```

2. **Don't commit `.env` files:**
   ```bash
   # Already in .gitignore
   echo ".env" >> .gitignore
   ```

3. **Use secure SECRET_KEY:**
   ```bash
   # Generate secure key
   python -c 'import secrets; print(secrets.token_urlsafe(32))'
   ```

4. **Update base images regularly:**
   ```bash
   docker-compose pull
   docker-compose up -d --build
   ```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change ports in docker-compose.yml:
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

### Permission Errors

```bash
# Fix volume permissions
docker-compose down -v
sudo chown -R $USER:$USER .
docker-compose up -d
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

## 📊 Resource Usage

### Check Resource Usage

```bash
docker stats
```

### Limit Resources

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          memory: 256M
```

## 🌐 Production Deployment

### 1. Using Docker on VPS

```bash
# On your server
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Set environment variables
nano .env

# Start in production mode
docker-compose up -d

# Set up reverse proxy (nginx/traefik)
# Configure SSL certificates (Let's Encrypt)
```

### 2. Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml gitpeek

# Check services
docker service ls
```

### 3. Using Kubernetes

Convert docker-compose to Kubernetes:

```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-linux-amd64 -o kompose
chmod +x kompose

# Convert
./kompose convert

# Deploy
kubectl apply -f .
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```

### Backup Data

```bash
# Backup volume
docker run --rm -v gitpeek_backend-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/gitpeek-backup-$(date +%Y%m%d).tar.gz /data

# Restore backup
docker run --rm -v gitpeek_backend-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/gitpeek-backup-20240101.tar.gz -C /
```

## 🎯 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build images
        run: docker-compose build

      - name: Run tests
        run: |
          docker-compose up -d
          docker-compose exec -T backend pytest
          docker-compose exec -T frontend npm test
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Dockerizing Python Apps](https://docs.docker.com/language/python/containerize/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

## 💡 Tips

1. **Use `.dockerignore`** to exclude unnecessary files from builds
2. **Multi-stage builds** reduce final image size significantly
3. **Layer caching** speeds up builds - order Dockerfile commands wisely
4. **Health checks** ensure services are actually ready before accepting traffic
5. **Named volumes** persist data between container restarts

---

**Need help?** Open an issue on GitHub or check the [main README](README.md).

