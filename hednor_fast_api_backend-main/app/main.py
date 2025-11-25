# # # # from fastapi import FastAPI
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from app import models
# # # # from app.database import engine
# # # # from app.routes import product,category
# # # # from fastapi.staticfiles import StaticFiles
# # # # from fastapi.responses import FileResponse

# # # # # Create database tables (if not using Alembic)
# # # # models.Base.metadata.create_all(bind=engine)

# # # # # Initialize FastAPI app
# # # # app = FastAPI(
# # # #     title="E-Commerce Product API",
# # # #     description="API to manage products, images, and variants.",
# # # #     version="1.0.0"
# # # # )

# # # # # CORS Configuration (allow frontend access)

# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=["http://localhost:3000"],
# # # #     allow_credentials=True,
# # # #     allow_methods=["*"],
# # # #     allow_headers=["*"],
# # # # )


# # # # # Include product-related routes
# # # # app.include_router(product.router)
# # # # app.include_router(category.router)  # ← register it



# # # # @app.get("/")
# # # # def read_root():
# # # #     return {"message": "Hello, FastAPI!"}


# # # # @app.get("/favicon.ico", include_in_schema=False)
# # # # async def favicon():
# # # #     return FileResponse("static/favicon.ico")



# # # # from fastapi import FastAPI
# # # # from fastapi.middleware.cors import CORSMiddleware
# # # # from fastapi.staticfiles import StaticFiles
# # # # from fastapi.responses import FileResponse, JSONResponse
# # # # import os

# # # # from app import models
# # # # from app.database import engine
# # # # from app.config import settings  # Updated import
# # # # from fastapi import FastAPI
# # # # from fastapi.staticfiles import StaticFiles
# # # # from pathlib import Path
# # # # import os


# # # # from fastapi import FastAPI
# # # # from .database import engine
# # # # from . import models
# # # # from .routes import category, brand, product

# # # # # Create database tables
# # # # models.Base.metadata.create_all(bind=engine)

# # # # app = FastAPI(
# # # #     title="E-Commerce API",
# # # #     description="API for managing e-commerce categories, brands, and products",
# # # #     version="1.0.0"
# # # # )


# # # # # Configure CORS middleware
# # # # app.add_middleware(
# # # #     CORSMiddleware,
# # # #     allow_origins=settings.CORS_ORIGINS,  # Now comes from settings
# # # #     allow_credentials=True,
# # # #     allow_methods=["GET", "POST", "PUT", "DELETE"],
# # # #     allow_headers=["*"],
# # # # )

# # # # @app.get("/")
# # # # def root():
# # # #     return {"message": "E-Commerce API is running"}


# # # #  # Configure static files
# # # # def setup_static_files():
# # # #     static_dir = Path(__file__).parent / "static"
# # # #     try:
# # # #         static_dir.mkdir(exist_ok=True)
# # # #         app.mount("/static", StaticFiles(directory=static_dir), name="static")
# # # #     except Exception as e:
# # # #         print(f"Static files setup error: {e}")

# # # # setup_static_files()


# # # # # # Include API routes
# # # # # app.include_router(
# # # # #     product.router,
# # # # #     prefix="/api/v1",
# # # # #     tags=["Products"]
# # # # # )

# # # # # # app.include_router(
# # # # # #     category.router,
# # # # # #     prefix="/api/v1",  # Optional prefix
# # # # # #     tags=["Categories"]
# # # # # # )


# # # # # Include routers
# # # # app.include_router(category.router)
# # # # app.include_router(brand.router)
# # # # app.include_router(product.router)



# # # # # Health check endpoint
# # # # @app.get("/", include_in_schema=False)
# # # # def health_check():
# # # #     return {"status": "healthy", "version": app.version}



# # # # # Favicon endpoint
# # # # @app.get("/favicon.ico", include_in_schema=False)
# # # # async def favicon():
# # # #     favicon_path = os.path.join("static", "favicon.ico")
# # # #     if os.path.exists(favicon_path):
# # # #         return FileResponse(favicon_path)
# # # #     return {"message": "No favicon found"}



# # # # # Custom exception handler (example)
# # # # @app.exception_handler(404)
# # # # async def not_found_exception_handler(request, exc):
# # # #     return JSONResponse(
# # # #         status_code=404,
# # # #         content={"message": "The requested resource was not found"},
# # # #     )



# # # from fastapi import FastAPI, Request
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.staticfiles import StaticFiles
# # # from fastapi.responses import FileResponse, JSONResponse
# # # from pathlib import Path
# # # import os

# # # from app import models
# # # from app.database import engine
# # # from app.config import settings
# # # from app.routes import category, brand, product

# # # # Create database tables

# # # from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
# # # from sqlalchemy.orm import Session
# # # import shutil
# # # import os
# # # from datetime import datetime
# # # from typing import Optional
# # # from . import models, schemas
# # # from .database import get_db
# # # import logging
# # # from fastapi.staticfiles import StaticFiles





# # # # Create database tables
# # # models.Base.metadata.create_all(bind=engine)

# # # app = FastAPI(
# # #     title="E-Commerce API",
# # #     description="API for managing e-commerce categories, brands, and products",
# # #     version="1.0.0"
# # # )


# # # app.mount("/uploads",StaticFiles(directory="uploads"), name="uploads")

# # # # CORS Middleware
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=settings.CORS_ORIGINS,
# # #     allow_credentials=True,
# # #     allow_methods=["GET", "POST", "PUT", "DELETE"],
# # #     allow_headers=["*"],
# # # )



# # # # API Routes
# # # app.include_router(category.router )
# # # app.include_router(brand.router)
# # # app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# # # app.include_router(product.router)

# # # # Static Files Setup
# # # def setup_static_files():
# # #     static_dir = Path(__file__).parent / "static"
# # #     try:
# # #         static_dir.mkdir(exist_ok=True)
# # #         app.mount("/static", StaticFiles(directory=static_dir), name="static")
# # #     except Exception as e:
# # #         print(f"Static files setup error: {e}")

# # # setup_static_files()

# # # # Root and Health Check
# # # @app.get("/", include_in_schema=False)
# # # def health_check():
# # #     return {"status": "healthy", "version": app.version}

# # # # Favicon Endpoint
# # # @app.get("/favicon.ico", include_in_schema=False)
# # # async def favicon():
# # #     favicon_path = os.path.join("static", "favicon.ico")
# # #     if os.path.exists(favicon_path):
# # #         return FileResponse(favicon_path)
# # #     return JSONResponse(content={"message": "No favicon found"}, status_code=404)

# # # # Exception Handler
# # # @app.exception_handler(404)
# # # async def not_found_exception_handler(request: Request, exc):
# # #     return JSONResponse(
# # #         status_code=404,
# # #         content={"message": "The requested resource was not found"},
# # #     )










# # from fastapi import FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.responses import FileResponse, JSONResponse
# # from pathlib import Path
# # import os
# # import logging

# # from app import models
# # from app.database import engine
# # from app.config import settings
# # from app.routes import category, brand, product


# # # Initialize logger
# # logger = logging.getLogger(__name__)
# # logging.basicConfig(level=logging.INFO)

# # def create_app():
# #     # Create database tables
# #     models.Base.metadata.create_all(bind=engine)

# #     app = FastAPI(
# #         title="E-Commerce API",
# #         description="API for managing e-commerce categories, brands, and products",
# #         version="1.0.0",
# #         docs_url="/docs",
# #         redoc_url="/redoc"
# #     )

# #     # Setup middleware
# #     app.add_middleware(
# #         CORSMiddleware,
# #         allow_origins=settings.CORS_ORIGINS,
# #         allow_credentials=True,
# #         allow_methods=["*"],
# #         allow_headers=["*"],
# #     )

# #     # Create uploads directory if it doesn't exist
# #     settings.IMAGE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# #     # Mount static files
# #     # app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# #     # Include routers
# #     app.include_router(category.router, prefix="/api/v1")
# #     # app.include_router(brand.router, prefix="/api/v1")
# #     # app.include_router(product.router, prefix="/api/v1")

# #     # Health check endpoint
# #     @app.get("/", include_in_schema=False)
# #     async def health_check():
# #         return {
# #             "status": "healthy",
# #             "version": app.version,
# #             "environment": settings.ENVIRONMENT if hasattr(settings, 'ENVIRONMENT') else "development"
# #         }

# #     # Favicon endpoint
# #     @app.get("/favicon.ico", include_in_schema=False)
# #     async def favicon():
# #         favicon_path = Path("static") / "favicon.ico"
# #         if favicon_path.exists():
# #             return FileResponse(favicon_path)
# #         return JSONResponse(
# #             content={"message": "No favicon found"}, 
# #             status_code=404
# #         )

# #     # Exception handler
# #     @app.exception_handler(404)
# #     async def not_found_handler(request: Request, exc):
# #         return JSONResponse(
# #             status_code=404,
# #             content={"message": "Resource not found"},
# #         )

# #     @app.exception_handler(500)
# #     async def server_error_handler(request: Request, exc):
# #         logger.error(f"Server error: {exc}")
# #         return JSONResponse(
# #             status_code=500,
# #             content={"message": "Internal server error"},
# #         )

# #     return app
# # app = create_app()




# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
# from . import models,schemas
# from .routes import categories  # This imports from routers/categories.py

# app = FastAPI()

# # Setup CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create database tables
# models.Base.metadata.create_all(bind=engine)

# # Include routers
# app.include_router(
#     categories.router,
#     prefix="/api/v1",
#     tags=["categories"]
# )

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Category API"}






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
