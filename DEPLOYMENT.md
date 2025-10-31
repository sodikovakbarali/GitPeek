# Deployment Guide

This guide covers deploying GitPeek to production environments.

## 🌐 Backend Deployment (Render)

### Option 1: Using Render Dashboard

1. **Create a Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name:** `gitpeek-backend`
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   Add these in the "Environment" section:
   ```
   GITHUB_CLIENT_ID=<your-client-id>
   GITHUB_CLIENT_SECRET=<your-client-secret>
   GITHUB_REDIRECT_URI=https://your-frontend-url.vercel.app/auth/callback
   SECRET_KEY=<generate-secure-random-key>
   DATABASE_URL=sqlite+aiosqlite:///./gitpeek.db
   CACHE_EXPIRE_MINUTES=10
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note your backend URL (e.g., `https://gitpeek-backend.onrender.com`)

### Option 2: Using render.yaml

1. Install Render CLI:
   ```bash
   npm install -g render-cli
   ```

2. Login:
   ```bash
   render login
   ```

3. Deploy:
   ```bash
   render deploy
   ```

### Option 3: Using GitHub Actions

The project includes a deployment workflow. To use it:

1. Get your Render API key from [Account Settings](https://dashboard.render.com/account/settings)
2. Add secrets to your GitHub repository:
   - `RENDER_API_KEY`: Your Render API key
   - `RENDER_SERVICE_ID`: Your service ID (from Render dashboard URL)
3. Push to `main` branch to trigger deployment

## 🚀 Frontend Deployment (Vercel)

### Option 1: Using Vercel Dashboard

1. **Import Project**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository

2. **Configure Project**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

3. **Environment Variables**
   Add in project settings:
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment
   - Your frontend will be live at `https://your-project.vercel.app`

### Option 2: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login:
   ```bash
   vercel login
   ```

3. Deploy from frontend directory:
   ```bash
   cd frontend
   vercel --prod
   ```

4. Set environment variables:
   ```bash
   vercel env add VITE_API_BASE_URL
   ```
   Enter your backend URL when prompted.

### Option 3: Using GitHub Actions

The deployment workflow is included. To use it:

1. Get your Vercel token from [Account Settings](https://vercel.com/account/tokens)
2. Add secrets to your GitHub repository:
   - `VERCEL_TOKEN`: Your Vercel token
   - `VERCEL_ORG_ID`: Your organization ID
   - `VERCEL_PROJECT_ID`: Your project ID
3. Push to `main` to trigger deployment

## 🔧 Post-Deployment Configuration

### Update GitHub OAuth

After deployment, update your GitHub OAuth app:

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Select your OAuth app
3. Update **Authorization callback URL** to:
   ```
   https://your-frontend.vercel.app/auth/callback
   ```

### Update Backend Environment

Update the backend `GITHUB_REDIRECT_URI` to match:
```
GITHUB_REDIRECT_URI=https://your-frontend.vercel.app/auth/callback
```

## 🐳 Docker Deployment

### Using Docker Compose

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Build and run**
   ```bash
   docker-compose up -d
   ```

3. **Access**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:80

### Individual Docker Containers

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

## 🔒 Security Checklist

Before deploying to production:

- [ ] Generate a strong `SECRET_KEY`
- [ ] Set up HTTPS (handled by Render/Vercel)
- [ ] Configure CORS origins to your frontend domain
- [ ] Set secure OAuth redirect URIs
- [ ] Enable rate limiting (if needed)
- [ ] Review and secure all environment variables
- [ ] Set up monitoring and error tracking
- [ ] Configure database backups (if using persistent DB)

## 📊 Monitoring

### Backend (Render)

Render provides built-in monitoring:
- View logs in the Render dashboard
- Set up health check endpoint (`/health`)
- Configure alerts for downtime

### Frontend (Vercel)

Vercel provides analytics:
- View deployment logs
- Monitor build times
- Check Web Vitals

### Additional Tools

Consider adding:
- **Sentry** for error tracking
- **LogRocket** for session replay
- **Google Analytics** for user analytics

## 🔄 Continuous Deployment

The project is set up for automatic deployment:

1. **On push to `main`:**
   - Tests run automatically
   - If tests pass, deploys to production

2. **On pull requests:**
   - Tests run automatically
   - Preview deployments on Vercel

## 🆘 Troubleshooting

### Backend not starting

1. Check logs in Render dashboard
2. Verify all environment variables are set
3. Check database connection
4. Ensure Python version matches (3.11+)

### Frontend build fails

1. Check Node.js version (20+)
2. Verify environment variables
3. Check build logs in Vercel
4. Ensure API URL is correct

### OAuth not working

1. Verify callback URL matches in GitHub OAuth app
2. Check `GITHUB_REDIRECT_URI` in backend
3. Ensure CORS is configured correctly
4. Verify client ID and secret are correct

## 📝 Deployment Checklist

- [ ] Backend deployed and healthy
- [ ] Frontend deployed and accessible
- [ ] Environment variables set correctly
- [ ] GitHub OAuth configured
- [ ] CORS configured for frontend domain
- [ ] Database initialized
- [ ] Health checks passing
- [ ] CI/CD pipeline working
- [ ] Monitoring set up
- [ ] Documentation updated

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

**Need help?** Open an issue on GitHub!

