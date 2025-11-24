# Hednor E-Commerce API

## Overview

A fully asynchronous e-commerce API built with FastAPI and PostgreSQL for managing products, categories, and brands. The API supports both single and bulk product creation with proper validation and error handling. All database operations use async/await patterns for high performance.

## User Preferences

Preferred communication style: Simple, everyday language. Hinglish support appreciated.

## Recent Changes (Nov 24, 2025)

- **Converted entire project to async**: All routes now use AsyncSession for database operations
- **Added bulk product creation endpoint**: POST `/api/v1/products/bulk` accepts JSON array of products
- **Fixed greenlet issues**: Removed lazy-loaded relationship access in responses
- **All endpoints working**: Single product, bulk product, list, get, update, delete endpoints all functional
- **Database recreated**: Tables now have proper schema including parent_id for category hierarchy

## System Architecture

### Backend Framework
- **FastAPI**: Modern async web framework with auto-generated API documentation
- **Uvicorn**: ASGI server bound to 0.0.0.0:5000
- **Python 3.12**: Runtime environment

### Database Layer
- **SQLAlchemy 2.0**: Async ORM using AsyncSession
- **AsyncPG**: PostgreSQL async driver for non-blocking operations
- **PostgreSQL**: Primary database with connection pooling and SSL support
- **Models**: Category (with parent_id hierarchy), Brand, Product

### Project Structure
```
app/
├── main.py              # FastAPI app setup and startup
├── database.py          # AsyncSession configuration
├── models.py            # SQLAlchemy models (Category, Brand, Product)
├── schemas.py           # Pydantic schemas for validation and responses
└── routes/
    ├── categories.py    # Category endpoints (list, hierarchy, search)
    ├── brand.py         # Brand CRUD endpoints
    └── product.py       # Product CRUD + bulk create endpoints
start.py                 # Application entry point with async init
```

### API Endpoints

#### Products
- `POST /api/v1/products/` - Create single product (Form data)
- `POST /api/v1/products/bulk` - Create multiple products (JSON array)
- `GET /api/v1/products/` - List all products with filters
- `GET /api/v1/products/{id}` - Get single product
- `PUT /api/v1/products/{id}` - Update product (Form data)
- `DELETE /api/v1/products/{id}` - Delete product

#### Categories
- `GET /api/v1/categories/top-level` - Get top-level categories
- `GET /api/v1/categories/{id}/children` - Get category children
- `GET /api/v1/categories/{id}/hierarchy` - Get category hierarchy (recursive)
- `GET /api/v1/categories/search` - Search categories by name

#### Brands
- `POST /api/v1/brands/` - Create brand
- `GET /api/v1/brands/` - List brands
- `GET /api/v1/brands/{id}` - Get single brand
- `PUT /api/v1/brands/{id}` - Update brand
- `DELETE /api/v1/brands/{id}` - Delete brand

### Key Features

**Bulk Product Creation**:
- Accepts JSON array of up to 100 products
- Validates all categories and brands exist
- Checks for duplicate slugs
- Returns detailed success/failure status for each product
- Atomic transaction: all succeed or appropriate failures reported

**Async Operations**:
- All database queries use `await` and AsyncSession
- No blocking I/O operations
- Connection pooling enabled
- SSL support for cloud databases

**Error Handling**:
- Proper HTTP status codes
- Detailed error messages
- Validation for relationships (category, brand)
- Duplicate slug detection

## Database Schema

### Categories Table
- `id` (int, PK)
- `name` (varchar)
- `slug` (varchar, unique)
- `description` (varchar)
- `is_active` (boolean)
- `is_leaf` (boolean)
- `parent_id` (int, FK to categories.id)

### Brands Table
- `id` (int, PK)
- `name` (varchar)
- `slug` (varchar, unique)
- `description` (varchar)
- `is_active` (boolean)

### Products Table
- `id` (int, PK)
- `name` (varchar)
- `slug` (varchar, unique)
- `description` (varchar)
- `price` (float)
- `selling_price` (float)
- `discount` (float)
- `quantity` (int)
- `category_id` (int, FK)
- `brand_id` (int, FK)
- `is_active` (boolean)
- `image_path` (varchar)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## Testing Commands

```bash
# Bulk product creation (3 products)
curl -X POST http://localhost:5000/api/v1/products/bulk \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Nike Pro", "slug": "nike-pro", "price": 120, "quantity": 50, "category_id": 1, "brand_id": 1},
    {"name": "Nike Elite", "slug": "nike-elite", "price": 140, "quantity": 75, "category_id": 1, "brand_id": 1}
  ]'

# Single product (Form data)
curl -X POST http://localhost:5000/api/v1/products/ \
  -F "name=Adidas Running" \
  -F "slug=adidas-running" \
  -F "price=130" \
  -F "quantity=60" \
  -F "category_id=1" \
  -F "brand_id=1"

# List products
curl http://localhost:5000/api/v1/products/

# Get API docs
curl http://localhost:5000/docs
```

## Dependencies

- fastapi
- uvicorn
- sqlalchemy
- asyncpg
- psycopg2-binary
- pydantic
- python-multipart

## Known Issues & Notes

- Single product endpoint uses Form data (multipart) for image support
- Bulk product endpoint uses JSON (no image support in bulk)
- Relationships (category, brand) not included in product responses to avoid greenlet issues
- Product responses include only basic fields and relationship IDs
