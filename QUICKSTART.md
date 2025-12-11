# GitPeek Quick Start Guide

Get GitPeek up and running in under 5 minutes! 🚀

**⚡ Note:** GitPeek works immediately for viewing **all public repositories**. OAuth setup is **optional** and only needed if you want to view private repositories. See [OAUTH_SETUP.md](OAUTH_SETUP.md) for OAuth instructions.

## 📋 Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ and Node.js 20+ (for local development)
- Git

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/GitPeek.git
cd GitPeek

# Run the setup script
./setup.sh

# Follow the on-screen instructions
```

### Option 2: Manual Setup

**1. Backend Setup**
```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:5173/auth/callback
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
DATABASE_URL=sqlite+aiosqlite:///./gitpeek.db
CACHE_EXPIRE_MINUTES=10
EOL

# Start the backend server
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000

**2. Frontend Setup (in a new terminal)**
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start the development server
npm run dev
```

Frontend will run at: http://localhost:5173

## 🎯 Using GitPeek

1. **Open your browser** to http://localhost:5173

2. **Search for any GitHub user:**
   - Enter a username (e.g., `torvalds`, `gvanrossum`)
   - Select a time range (day, week, month, year)
   - Click Search

3. **View Results:**
   - User statistics
   - Commit activity chart
   - Repository list
   - Recent commits

4. **Optional: GitHub OAuth Login**
   - Click "Login with GitHub" to view private repositories
   - You'll need to set up GitHub OAuth first (see below)

## 🔑 Setting Up GitHub OAuth (Optional)

To enable authentication and view private repos:

1. **Create a GitHub OAuth App:**
   - Go to https://github.com/settings/developers
   - Click "New OAuth App"
   - Fill in:
     - **Application name:** GitPeek
     - **Homepage URL:** http://localhost:5173
     - **Authorization callback URL:** http://localhost:5173/auth/callback
   - Click "Register application"

2. **Get Credentials:**
   - Copy the **Client ID**
   - Generate a **Client Secret**

3. **Update Backend .env:**
   ```bash
   GITHUB_CLIENT_ID=your_actual_client_id
   GITHUB_CLIENT_SECRET=your_actual_client_secret
   ```

4. **Restart the backend server**

5. **Try logging in!**

## 🐳 Using Docker (Alternative)

```bash
# Build and start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:80
# Backend: http://localhost:8000
```

## 🧪 Running Tests

**Backend Tests:**
```bash
cd backend
source venv/bin/activate
pytest --cov=app
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## 📚 Next Steps

- Read the [full README](README.md) for detailed documentation
- Check out [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## 🆘 Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (should be 3.11+)
- Ensure virtual environment is activated
- Check if port 8000 is already in use

### Frontend won't start
- Check Node version: `node --version` (should be 20+)
- Delete `node_modules` and run `npm install` again
- Check if port 5173 is already in use

### Can't find GitHub user
- Ensure the username is correct (case-sensitive)
- Check if the user has public repositories
- Verify backend is running at http://localhost:8000

### OAuth login not working
- Verify GitHub OAuth app callback URL matches exactly
- Check backend .env has correct CLIENT_ID and CLIENT_SECRET
- Ensure backend is restarted after updating .env

## 📧 Need Help?

- Check the [README](README.md) for more details
- Open an issue on GitHub
- Read the API docs at http://localhost:8000/docs

---

**Happy coding!** 🎉

