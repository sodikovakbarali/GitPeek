# GitPeek 🔍

> Peek into any GitHub user's activity — repositories and commits over time

[![Build Status](https://github.com/yourusername/GitPeek/workflows/Build%20and%20Test/badge.svg)](https://github.com/yourusername/GitPeek/actions)
[![codecov](https://codecov.io/gh/yourusername/GitPeek/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/GitPeek)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

GitPeek is a full-stack web application that lets you explore any GitHub user's activity, including their repositories and commits over customizable time periods (day, week, month, or year). Optionally authenticate via GitHub OAuth to view private repositories.

## ✨ Features

- 🔍 **Search any GitHub user** by username
- 📊 **Interactive activity charts** showing commit history
- 📦 **Repository overview** with stars, forks, and languages
- 💾 **Recent commits** across all repositories
- 🔐 **GitHub OAuth authentication** for private repo access
- 🌓 **Dark/Light mode** toggle
- 📱 **Fully responsive** design
- ⚡ **Fast API caching** for optimal performance
- 🧪 **Comprehensive test coverage** (90%+)

## 🏗️ Architecture

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Database:** SQLite with SQLAlchemy ORM
- **Caching:** In-database caching with 10-minute expiration
- **Authentication:** GitHub OAuth via Authlib
- **Testing:** Pytest with 90%+ coverage
- **API:** RESTful endpoints + GitHub REST/GraphQL API integration

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS + Custom UI components
- **Routing:** React Router v6
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Testing:** Vitest + React Testing Library

### DevOps
- **CI/CD:** GitHub Actions
- **Backend Deployment:** Render
- **Frontend Deployment:** Vercel
- **Containerization:** Docker

## 🚀 Quick Start

### 🐳 Option 1: Docker (Recommended - Works Everywhere!)

**Prerequisites:** Docker & Docker Compose

```bash
# Clone the repository
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Start everything with one command!
docker-compose up -d

# Or use Make
make docker-up
```

**That's it!** 🎉
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

**This works immediately for all public repositories!** 🚀

**For development with hot-reload:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
# Or: make docker-dev
```

See [DOCKER.md](DOCKER.md) for complete Docker documentation.

---

### 🔐 Optional: GitHub OAuth (For Private Repositories)

**You can skip this!** GitPeek works perfectly without OAuth for viewing public repositories.

**Only follow these steps if you want to view private repositories:**

See [OAUTH_SETUP.md](OAUTH_SETUP.md) for complete step-by-step instructions.

**Quick version:**
1. Create GitHub OAuth app at https://github.com/settings/developers
2. Add credentials to `.env` file
3. Restart backend

Most users don't need this!

---

### 💻 Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 20+
- Git
- GitHub account (for OAuth, optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek
```

2. **Backend Setup**

**Option A: Using Poetry (Recommended)**
```bash
cd backend

# Install dependencies with Poetry
poetry install

# Create .env file
cp .env.example .env
# Edit .env with your GitHub OAuth credentials (optional)

# Run the server
poetry run uvicorn app.main:app --reload
```

**Option B: Using pip**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your GitHub OAuth credentials (optional)

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

See [POETRY.md](POETRY.md) for complete Poetry documentation.

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env if needed

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## ⚙️ Configuration

### Basic Configuration (Optional)

GitPeek works out of the box with no configuration needed!

All configuration is optional and only needed for:
- 🔐 GitHub OAuth (to view private repositories)
- 🔧 Custom API URLs
- 🎛️ Advanced features

### GitHub OAuth Setup (Optional)

**⚡ Skip this if you only want to view public repositories!**

To enable private repository viewing, see the complete guide:
- 📖 **[OAUTH_SETUP.md](OAUTH_SETUP.md)** - Step-by-step OAuth setup guide

Quick summary:
1. Create GitHub OAuth app at https://github.com/settings/developers
2. Create `.env` file in project root with your credentials
3. Restart backend: `docker-compose restart backend`

**Most users can skip this!** The app works great without OAuth.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest --cov=app --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Frontend Tests

```bash
cd frontend
npm run test:coverage
```

View coverage report: `open coverage/index.html`

## 🐳 Docker

### Build and Run with Docker

**Backend:**
```bash
cd backend
docker build -t gitpeek-backend .
docker run -p 8000:8000 --env-file .env gitpeek-backend
```

**Frontend:**
```bash
cd frontend
docker build -t gitpeek-frontend .
docker run -p 80:80 gitpeek-frontend
```

### Docker Compose (Coming Soon)

```bash
docker-compose up -d
```

## 📦 Deployment

### Backend Deployment (Render)

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy!

Alternatively, use the included `render.yaml`:
```bash
render deploy
```

### Frontend Deployment (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Deploy:
```bash
cd frontend
vercel --prod
```

Or connect your repository directly on [Vercel](https://vercel.com) for automatic deployments.

### CI/CD Setup

The project includes GitHub Actions workflows:

- **Build & Test** (`.github/workflows/build.yml`): Runs on every push/PR
- **Deploy** (`.github/workflows/deploy.yml`): Deploys to production on push to `main`

**Required GitHub Secrets:**
- `RENDER_API_KEY` - Your Render API key
- `RENDER_SERVICE_ID` - Your Render service ID
- `VERCEL_TOKEN` - Your Vercel token
- `VERCEL_ORG_ID` - Your Vercel organization ID
- `VERCEL_PROJECT_ID` - Your Vercel project ID

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Main Endpoints

**Public Routes:**
- `POST /api/public/activity` - Get user activity (public repos only)
- `GET /api/public/user/{username}` - Get user information
- `GET /api/public/search/{username}` - Quick search

**Authenticated Routes:**
- `GET /api/auth/login` - Get GitHub OAuth URL
- `GET /api/auth/callback` - OAuth callback handler
- `POST /api/auth/activity` - Get activity (includes private repos)
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

## 🛠️ Development

### Project Structure

```
GitPeek/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database setup
│   │   ├── models/              # Pydantic models
│   │   ├── routes/              # API routes
│   │   ├── services/            # Business logic
│   │   └── tests/               # Backend tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── render.yaml
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── context/             # Context providers
│   │   ├── lib/                 # Utilities & API
│   │   ├── pages/               # Page components
│   │   └── tests/               # Frontend tests
│   ├── Dockerfile
│   ├── vercel.json
│   └── package.json
├── .github/
│   └── workflows/               # CI/CD workflows
├── README.md
└── LICENSE
```

### Code Style

**Backend:**
- Follow PEP 8
- Use type hints
- Run: `ruff check app/`

**Frontend:**
- ESLint configuration included
- Run: `npm run lint`

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Tests pass (`pytest` for backend, `npm test` for frontend)
- Code is linted
- Coverage remains above 90%

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [GitHub API](https://docs.github.com/en/rest) for providing public data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python framework
- [React](https://react.dev/) and [Vite](https://vitejs.dev/) for the frontend tooling
- [TailwindCSS](https://tailwindcss.com/) for beautiful styling
- [Recharts](https://recharts.org/) for data visualization

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, React, and TypeScript**

