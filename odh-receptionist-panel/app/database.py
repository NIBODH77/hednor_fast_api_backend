from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from urllib.parse import urlparse, parse_qs

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:nibodh%40123@localhost/odhreceptiondb"
)

# Clean up URL for asyncpg
if DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://").replace("postgres://", "postgresql+asyncpg://")

# Remove any sslmode parameters from URL
if "?" in DATABASE_URL:
    base_url = DATABASE_URL.split("?")[0]
    DATABASE_URL = base_url

# Configure SSL for cloud database connections (Neon, AWS RDS, etc.)
# Use proper SSL verification for production security
connect_args = {}
if "neon.tech" in DATABASE_URL or "rds.amazonaws.com" in DATABASE_URL:
    # For asyncpg, simply use ssl=True to enable SSL with proper certificate validation
    connect_args = {"ssl": True}

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_target_metadata():
    return Base.metadata
