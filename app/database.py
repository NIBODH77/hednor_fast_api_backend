from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get DATABASE_URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:123456789@localhost:5432/hednor_db"
)

# Clean up URL for asyncpg
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://").replace("postgres://", "postgresql+asyncpg://")

# Remove any sslmode parameters from URL
if "?" in DATABASE_URL:
    base_url = DATABASE_URL.split("?")[0]
    DATABASE_URL = base_url

# Configure SSL for cloud database connections (Neon, AWS RDS, etc.)
connect_args = {
    "server_settings": {
        "application_name": "hednor_ecommerce",
        "jit": "off"
    }
}
if "neon.tech" in DATABASE_URL or "rds.amazonaws.com" in DATABASE_URL:
    connect_args["ssl"] = True

# Create async engine with proper configuration
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Base class for models
Base = declarative_base()

# Async database dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Initialize database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
