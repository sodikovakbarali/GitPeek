# 🐳 Docker Quick Start

Get GitPeek running in **under 2 minutes** with Docker!

## Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/engine/install/))
- Docker Compose v2.0+ (included with Docker Desktop)

## 🚀 Start GitPeek (Production Mode)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# 2. Start the application
docker-compose up -d
```

**That's it!** 🎉 GitPeek is now running:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 🛠️ Development Mode (with Hot-Reload)

```bash
# Start with hot-reload for both frontend and backend
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Now you can:
- ✅ Edit code locally - changes reflect immediately
- ✅ Frontend available at: http://localhost:5173 (Vite dev server)
- ✅ Backend available at: http://localhost:8000 (with auto-reload)

## 🎯 Common Commands

```bash
# Stop GitPeek
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild images
docker-compose build --no-cache

# Run tests
docker-compose exec backend poetry run pytest
docker-compose exec frontend npm test

# Access shell
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh
```

## ⚙️ Configuration (Optional)

To enable GitHub OAuth login:

```bash
# 1. Create .env file
cp .env.docker.example .env

# 2. Edit .env and add your GitHub OAuth credentials
nano .env

# 3. Restart
docker-compose down && docker-compose up -d
```

## 🔧 Using Make Commands (Even Easier!)

```bash
# Start production
make docker-up

# Start development
make docker-dev

# Stop
make docker-down

# View logs
make docker-logs

# Run tests
make docker-test

# Clean everything
make docker-clean
```

## 🐛 Troubleshooting

### Port Already in Use?

Edit `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

### Services Won't Start?

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Reset Everything?

```bash
# Remove containers, volumes, and images
docker-compose down -v --rmi all
docker-compose up -d
```

## 📚 Full Documentation

- [Complete Docker Guide](DOCKER.md) - Detailed Docker documentation
- [Main README](README.md) - Full project documentation
- [Poetry Guide](POETRY.md) - Python dependency management

## 💡 Why Docker?

✅ **Works on every machine** - No "works on my machine" issues
✅ **Consistent environments** - Same setup for dev, test, and production
✅ **Easy setup** - One command to start everything
✅ **Isolated** - Doesn't affect your system
✅ **Production-ready** - Same containers for development and deployment

---

**Need help?** Check [DOCKER.md](DOCKER.md) or open an issue on GitHub!

