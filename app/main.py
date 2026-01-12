"""
Main FastAPI Application
=========================
Entry point for the Data Normalization Application.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.config import settings
from app.utils.logger import app_logger

# Import routers
from app.routes import upload, database, analysis, normalization, export


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Web-based application for data normalization from various sources",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(upload.router)
app.include_router(database.router)
app.include_router(analysis.router)
app.include_router(normalization.router)
app.include_router(export.router)
from app.routes import pendampingan
app.include_router(pendampingan.router)


# ============================================================================
# WEB PAGES (Frontend Routes)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Homepage"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    """Upload page"""
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@app.get("/analysis/{file_id}", response_class=HTMLResponse)
async def analysis_page(request: Request, file_id: str):
    """Analysis page"""
    return templates.TemplateResponse(
        "analysis.html",
        {"request": request, "file_id": file_id}
    )


@app.get("/normalize/{file_id}", response_class=HTMLResponse)
async def normalize_page(request: Request, file_id: str):
    """Normalization configuration page"""
    return templates.TemplateResponse(
        "normalization.html",
        {"request": request, "file_id": file_id}
    )


@app.get("/preview/{original_file_id}/{normalized_file_id}", response_class=HTMLResponse)
async def preview_page(request: Request, original_file_id: str, normalized_file_id: str):
    """Preview page (before vs after)"""
    return templates.TemplateResponse(
        "preview.html",
        {
            "request": request,
            "original_file_id": original_file_id,
            "normalized_file_id": normalized_file_id
        }
    )


@app.get("/export/{file_id}", response_class=HTMLResponse)
async def export_page(request: Request, file_id: str):
    """Export page"""
    return templates.TemplateResponse(
        "export.html",
        {"request": request, "file_id": file_id}
    )


# ============================================================================
# HEALTH CHECK & INFO
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


@app.get("/info")
async def app_info():
    """Application information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "allowed_extensions": settings.allowed_extensions_list,
        "max_upload_size_mb": round(settings.MAX_UPLOAD_SIZE / 1024 / 1024, 2)
    }


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    app_logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    app_logger.info(f"Debug mode: {settings.DEBUG}")
    app_logger.info(f"Allowed file extensions: {settings.allowed_extensions_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    app_logger.info(f"Shutting down {settings.APP_NAME}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "error_title": "404 - Page Not Found",
            "error_message": "The page you are looking for does not exist."
        },
        status_code=404
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Custom 500 handler"""
    app_logger.error(f"Server error: {str(exc)}")
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "error_title": "500 - Server Error",
            "error_message": "An internal server error occurred. Please try again later."
        },
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
