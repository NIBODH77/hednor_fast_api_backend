from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import logging

from app.database import engine, init_db, Base
from app.routes import categories, brand, product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Hednor E-Commerce API",
    description="API for managing e-commerce products, categories, and brands",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
Path("uploads/products").mkdir(parents=True, exist_ok=True)

# Mount static files for product images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routers
app.include_router(
    categories.router,
    prefix="/api/v1",
    tags=["Categories"]
)

app.include_router(
    brand.router,
    prefix="/api/v1", 
    tags=["Brands"]
)

app.include_router(
    product.router,
    prefix="/api/v1",
    tags=["Products"]
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Hednor E-Commerce API is running",
        "version": app.version
    }

# Favicon endpoint
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return JSONResponse(
        content={"message": "No favicon configured"},
        status_code=404
    )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found"},
    )

@app.exception_handler(500)
async def server_error_handler(request, exc):
    logger.error(f"Server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully!")
