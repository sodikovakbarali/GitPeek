# 🚀 Getting Started with GitPeek

Choose the method that works best for you!

## 🐳 Method 1: Docker (Easiest & Most Reliable)

**Perfect for: Everyone! Especially if you want zero configuration headaches.**

```bash
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek
docker-compose up -d
```

✅ **Pros:**
- Works identically on every machine (Windows, Mac, Linux)
- No dependency conflicts
- No "works on my machine" issues
- One command to start everything
- Production-ready

❌ **Cons:**
- Requires Docker installation
- Slightly slower initial build
- Uses more disk space

**When to use:** This is the RECOMMENDED method for most users!

---

## 💻 Method 2: Local Development with Poetry

**Perfect for: Python developers who want fine control and faster iteration.**

```bash
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Backend
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

✅ **Pros:**
- Fastest iteration cycle
- Full control over dependencies
- Easier debugging
- Better IDE integration

❌ **Cons:**
- Requires Python 3.11+ and Node.js 20+
- Manual setup required
- Potential dependency conflicts
- Different behavior across machines

**When to use:** When actively developing and need hot-reload speed.

---

## 📦 Method 3: Local Development with pip

**Perfect for: Quick testing or when you don't want to install Poetry.**

```bash
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

✅ **Pros:**
- Simple and familiar
- No extra tools needed
- Quick setup

❌ **Cons:**
- Dependency resolution issues
- Less reproducible
- Harder to manage updates

**When to use:** Quick local testing or learning the codebase.

---

## 🎯 Which Method Should You Choose?

### Use Docker if:
- ✅ You want it to "just work"
- ✅ You're sharing with others
- ✅ You're deploying to production
- ✅ You don't want to install Python/Node locally
- ✅ You want consistent environments

### Use Poetry if:
- ✅ You're actively developing the backend
- ✅ You need fast iteration
- ✅ You're familiar with Python tooling
- ✅ You want better dependency management

### Use pip if:
- ✅ You just want to try it quickly
- ✅ You don't want to learn new tools
- ✅ You're already comfortable with venv

---

## 📊 Quick Comparison

| Feature | Docker | Poetry | pip |
|---------|--------|--------|-----|
| Setup time | ⭐⭐⭐ Fast | ⭐⭐ Medium | ⭐⭐⭐ Fast |
| Reliability | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good | ⭐⭐ Fair |
| Reproducibility | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐⭐ Very Good | ⭐⭐ Fair |
| Dev speed | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Very Good |
| Learning curve | ⭐⭐⭐⭐ Easy | ⭐⭐ Moderate | ⭐⭐⭐⭐⭐ Easiest |
| Disk space | ⭐⭐ Heavy | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Light |

---

## 🎓 Step-by-Step: Docker (Recommended)

### 1. Install Docker

- **Windows/Mac:** [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux:** [Docker Engine](https://docs.docker.com/engine/install/)

### 2. Clone and Start

```bash
# Clone the repository
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Access GitPeek

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000/docs

### 4. Optional: Enable GitHub OAuth

```bash
# Create .env file
cp .env.docker.example .env

# Edit with your GitHub OAuth credentials
nano .env

# Restart
docker-compose restart
```

### 5. Development Mode (Hot Reload)

```bash
# Stop production mode
docker-compose down

# Start development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Now:
- Frontend: http://localhost:5173 (with Vite hot-reload)
- Backend: http://localhost:8000 (with auto-reload)
- Edit code locally - see changes instantly!

---

## 🎓 Step-by-Step: Poetry (Local Development)

### 1. Install Prerequisites

```bash
# Install Python 3.11 or 3.12
python3 --version  # Check version

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install Node.js 20+
node --version  # Check version
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies
poetry install

# Create environment file
cp .env.example .env
# Edit .env if needed

# Run backend
poetry run uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

### 3. Setup Frontend (New Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Run frontend
npm run dev
```

Frontend runs at http://localhost:5173

### 4. Test It

- Open http://localhost:5173
- Search for a GitHub user (e.g., "torvalds")
- See the magic! ✨

---

## 🆘 Troubleshooting

### Docker Issues

```bash
# Ports in use?
# Edit docker-compose.yml and change ports

# Services won't start?
docker-compose logs

# Start fresh
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Local Development Issues

```bash
# Backend won't start?
cd backend
poetry install --no-root
poetry run uvicorn app.main:app --reload

# Frontend won't start?
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev

# Python version issues?
# Install Python 3.11 or 3.12 (NOT 3.13!)
```

---

## 📚 Next Steps

After getting it running:

1. **Read the docs:**
   - [DOCKER.md](DOCKER.md) - Complete Docker guide
   - [POETRY.md](POETRY.md) - Poetry documentation
   - [README.md](README.md) - Full project documentation

2. **Set up GitHub OAuth** (optional):
   - Go to https://github.com/settings/developers
   - Create OAuth App
   - Add credentials to `.env`

3. **Run tests:**
   ```bash
   # Docker
   docker-compose exec backend poetry run pytest
   docker-compose exec frontend npm test

   # Local
   cd backend && poetry run pytest
   cd frontend && npm test
   ```

4. **Start developing:**
   - Check out [CONTRIBUTING.md](CONTRIBUTING.md)
   - Look at the code structure
   - Make your first contribution!

---

## 💬 Need Help?

- 📖 Read the [Documentation](README.md)
- 🐛 [Open an issue](https://github.com/yourusername/GitPeek/issues)
- 💡 Check [Discussions](https://github.com/yourusername/GitPeek/discussions)

---

**Happy coding!** 🎉

