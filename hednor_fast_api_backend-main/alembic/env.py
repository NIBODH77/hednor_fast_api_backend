# from logging.config import fileConfig
# from sqlalchemy import engine_from_config, pool
# from alembic import context
# from urllib.parse import quote_plus
# import os
# import sys

# # Add your app to Python path
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# # ✅ Import Base and models
# # Import your models
# from app import models
# from app.database import Base

# # DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/hednor_db"
# DATABASE_URL = "postgresql+psycopg2://postgres:123456789@localhost:5432/hednor_db"


# # # ✅ PostgreSQL connection
# # username = "hednoruser"
# # password = quote_plus("Hednor@H123456852")  # Use quote_plus to escape special characters
# # host = "172.105.123.229"
# # port = 5451
# # database = "hednordb"

# # DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# # ✅ Alembic config
# config = context.config
# config.set_main_option("sqlalchemy.url", DATABASE_URL.replace('%', '%%'))

# # ✅ Logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # ✅ SQLAlchemy metadata
# target_metadata = Base.metadata

# # ✅ Migration functions
# def run_migrations_offline() -> None:
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )
#     with context.begin_transaction():
#         context.run_migrations()

# def run_migrations_online() -> None:
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section, {}),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#         )
#         with context.begin_transaction():
#             context.run_migrations()

# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()






from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from urllib.parse import quote_plus
import os
import sys
from dotenv import load_dotenv
from app import models




# Load environment variables
load_dotenv()

# Add your app to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your models and Base
from app.models import *  # noqa: F401,F403 (import all models for Alembic)
from app.database import Base
from app import models

# Database configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "123456789"))
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hednor_db")

# Construct database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Alembic config
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL.replace('%', '%%'))

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata
target_metadata = models.Base.metadata
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Enable type comparison
        compare_server_default=True,  # Compare server defaults
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,  # Include all schemas
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()