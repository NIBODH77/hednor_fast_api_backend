# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker

# # # Replace credentials as needed
# # # DATABASE_URL = "postgresql://postgres:Nibodh@0012345@localhost:5432/hednor_db"

# # # DATABASE_URL = "postgresql://postgres:Nibodh%400012345@localhost:5432/hednor_db"

# # DATABASE_URL = "postgresql://postgres:Nibodh%400012345@localhost:5432/hednor_db"

# # engine = create_engine(DATABASE_URL)
# # SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# # Base = declarative_base()
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, declarative_base

# # # Local PostgreSQL example:
# # # DATABASE_URL = "postgresql://postgres:Hednor@H123456852:5451/hednordb"
# # # DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/hednor_db"
# # DATABASE_URL = "postgresql+psycopg2://postgres:123456789@localhost:5432/hednor_db"


# # engine = create_engine(DATABASE_URL)
# # SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# # # ✅ This must exist!
# # Base = declarative_base()

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()


# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker
# # from app.config import settings
# # import os
# # from dotenv import load_dotenv



# # load_dotenv()  # Load .env file if present

# # # Correct PostgreSQL connection URL format
# # SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:123456789@localhost:5432/hednor_db")

# # # Create the engine
# # engine = create_engine(
# #     SQLALCHEMY_DATABASE_URL,
# #     pool_pre_ping=True,  # Optional: checks connection health before use
# #     echo=False  # Enable SQL query logging
# # )

# # # Create session factory
# # SessionLocal = sessionmaker(
# #     autocommit=False,
# #     autoflush=False,
# #     bind=engine
# # )

# # # Base class for models
# # Base = declarative_base()

# # # Dependency to get DB session
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()










# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.config import settings
# from contextlib import contextmanager
# import logging

# # Configure logging
# logger = logging.getLogger(__name__)

# # Create the engine with improved configuration
# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,  # Checks connection health before use
#     pool_size=10,        # Number of connections to keep open
#     max_overflow=20,     # Number of connections beyond pool_size to allow
#     pool_recycle=3600,   # Recycle connections after 1 hour
#     pool_timeout=30,     # Seconds to wait before giving up on getting a connection
#     echo=False,          # Set to True for SQL query logging in development
#     connect_args={
#         "connect_timeout": 5,  # 5 second timeout for initial connection
#         "keepalives": 1,       # Enable TCP keepalive
#         "keepalives_idle": 30, # TCP keepalive idle time
#         "keepalives_interval": 10, # TCP keepalive interval
#         "keepalives_count": 5  # TCP keepalive count
#     }
# )

# # Session factory with improved configuration
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     expire_on_commit=False  # Gives more control over when instances expire
# )

# # Base class for models
# Base = declarative_base()

# # Dependency to get DB session
# def get_db():
#     """
#     Generator function that yields database sessions.
#     Ensures the session is properly closed after use.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         logger.error(f"Database error occurred: {e}")
#         db.rollback()
#         raise
#     finally:
#         db.close()

# # Context manager for sessions
# @contextmanager
# def session_scope():
#     """
#     Provide a transactional scope around a series of operations.
#     Usage:
#     with session_scope() as session:
#         # do database operations
#     """
#     session = SessionLocal()
#     try:
#         yield session
#         session.commit()
#     except Exception:
#         session.rollback()
#         raise
#     finally:
#         session.close()

# def init_db():
#     """
#     Initialize the database by creating all tables.
#     Should be called at application startup.
#     """
#     try:
#         Base.metadata.create_all(bind=engine)
#         logger.info("Database tables created successfully")
#     except Exception as e:
#         logger.error(f"Error creating database tables: {e}")
#         raise

# def ping_db():
#     """
#     Test the database connection.
#     Returns True if successful, False otherwise.
#     """
#     try:
#         with engine.connect() as conn:
#             conn.execute("SELECT 1")
#         return True
#     except Exception as e:
#         logger.error(f"Database ping failed: {e}")
#         return False








# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"
# # SQLALCHEMY_DATABASE_URL =  "postgresql+psycopg2://postgres:123456789@localhost:5432/hednor_db"
# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:nibodh%40123@localhost/odhreceptiondb"




# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get DATABASE_URL from environment or use SQLite by default
# Force SQLite if system database (helium) is set
database_url_env = os.getenv("DATABASE_URL", "")
if "helium" in database_url_env or not database_url_env:
    DATABASE_URL = "sqlite+aiosqlite:///./ecommerce.db"
else:
    DATABASE_URL = database_url_env

# Create async engine with proper configuration for SQLite
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
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
