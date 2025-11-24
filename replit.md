# ODH Receptionist Panel

## Overview

The ODH Receptionist Panel is a visitor and employee management system built with FastAPI. It provides role-based access control with separate interfaces for administrators and receptionists to manage visitor check-ins, scheduled appointments, and employee records. The system features session-based authentication and a PostgreSQL database backend.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI**: Modern async web framework chosen for its high performance, automatic API documentation, and native async/await support
- **Uvicorn**: ASGI server for running the FastAPI application
- **Python 3.12**: Runtime environment

### Database Layer
- **SQLAlchemy 2.0**: ORM for database interactions with async support via `AsyncSession`
- **Alembic**: Database migration management tool for schema versioning
- **PostgreSQL**: Primary relational database with asyncpg driver for async operations
- **Connection Strategy**: Async engine with connection pooling, SSL support for cloud databases (Neon, AWS RDS)

### Authentication & Security
- **Session-based Authentication**: Cookie-based sessions instead of JWT tokens for web interface
- **Passlib + Bcrypt**: Password hashing with bcrypt algorithm (72-byte limit enforced)
- **Role-based Access Control**: Two user roles - "admin" and "receptionist" with different permission levels
- **Default Credentials**: Auto-created admin user on first startup (username: admin, password: admin123) - must be changed immediately after first login

### Frontend Architecture
- **Jinja2 Templates**: Server-side HTML rendering with three template directories:
  - `frontend/`: Login pages
  - `frontend/admin/templates/`: Admin dashboard and management interfaces
  - `frontend/reception/templates/`: Receptionist-specific views
- **Tailwind CSS**: Utility-first CSS framework via CDN
- **Font Awesome**: Icon library for UI elements

### Application Structure
- **Models** (`app/models.py`): SQLAlchemy ORM models for User, Visitor, and Employee entities
- **CRUD Operations** (`app/crud.py`): Database query functions and business logic
- **Schemas** (`app/schemas.py`): Pydantic models for data validation
- **Security** (`app/security.py`): Authentication helpers, password hashing, token creation
- **Routes**: Modular routing (currently consolidated in `app/main.py`)
  - Authentication endpoints (login, logout)
  - Admin routes (user management, employee management, visitor oversight)
  - Receptionist routes (visitor check-in/out, appointments)

### Data Models
- **User**: Authentication and role management (admin/receptionist)
- **Visitor**: Guest tracking with check-in/out times, contact details, purpose of visit
- **Employee**: Staff directory with personal details, emergency contacts, documents (Aadhaar, PAN)

### Database Initialization
- **Startup Process**: `start.py` initializes database tables and creates default admin user
- **Migration Support**: Alembic configured for schema versioning (migrations present in `alembic/versions/`)

## External Dependencies

### Core Services
- **PostgreSQL Database**: Async PostgreSQL connection via asyncpg
  - Default local: `postgresql+asyncpg://postgres:nibodh%40123@localhost/odhreceptiondb`
  - Supports cloud providers: Neon, AWS RDS with SSL
  - Environment variable: `DATABASE_URL`

### SMS Gateway Integration
- **SMS Gateway Center**: Third-party SMS service for notifications
  - Base URL: `https://unify.smsgateway.center/SMSApi/send`
  - Credentials stored in `app/settings.py`
  - DLT (Distributed Ledger Technology) template IDs for OTP messages
  - Used for visitor notifications and OTP verification

### Python Package Dependencies
- **fastapi**: Web framework (v0.104.1+)
- **uvicorn**: ASGI server with standard extras
- **sqlalchemy**: ORM (v2.0.23+)
- **asyncpg**: PostgreSQL async driver
- **psycopg2-binary**: PostgreSQL adapter (sync fallback)
- **alembic**: Database migrations
- **pydantic-settings**: Configuration management
- **python-jose**: JWT operations (legacy, may be unused)
- **passlib**: Password hashing
- **bcrypt**: Bcrypt hashing implementation
- **python-multipart**: Form data handling
- **jinja2**: Template engine
- **email-validator**: Email validation
- **httpx**: HTTP client for external API calls
- **python-dateutil**: Date manipulation
- **pytz**: Timezone support

### Configuration Management
- **Pydantic Settings**: Environment-based configuration via `.env` file
- **Settings Class** (`app/settings.py`): Centralized configuration with defaults
  - Database URL
  - SMS gateway credentials
  - Secret keys (⚠️ default "logan" - should be changed in production)
  - Debug mode flags

### Static Assets
- **Tailwind CSS**: Loaded via CDN (cdn.tailwindcss.com)
- **Font Awesome**: Icon library via CDN (v6.4.0)
- Custom color scheme defined in template headers (primary, secondary, accent colors)