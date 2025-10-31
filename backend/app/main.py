from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes import public, auth
from app.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    logger.info("Starting GitPeek API...")
    await init_db()
    yield
    logger.info("Shutting down GitPeek API...")


app = FastAPI(
    title="GitPeek API",
    description="API for viewing GitHub user activity",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public.router, prefix="/api/public", tags=["public"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to GitPeek API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

