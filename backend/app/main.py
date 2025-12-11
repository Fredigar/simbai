"""
SIMBA Backend - FastAPI Application

Main FastAPI application with:
- REST API routes
- WebSocket support
- CORS configuration
- Middleware setup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.logger import logger

# Import routers (will create these next)
# from app.api.routes import chat, assistants, conversations, tools, documents, config

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Sistema Inteligente de Mensajería con Backend Avanzado",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return JSONResponse(
        content={
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/api/docs",
            "health": "/health",
        }
    )


# Include routers (will uncomment as we create them)
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(assistants.router, prefix="/api/assistants", tags=["assistants"])
# app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
# app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
# app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
# app.include_router(config.router, prefix="/api/config", tags=["config"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database: {settings.DATABASE_URL}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
