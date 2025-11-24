# # # from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, status, Query
# # # from fastapi.responses import JSONResponse

# # # from sqlalchemy.orm import Session
# # # from sqlalchemy import func

# # # from typing import List, Optional
# # # from uuid import uuid4
# # # from datetime import datetime
# # # import os
# # # import io 
# # # import csv
# # # import logging

# # # from .. import models, schemas
# # # from ..database import get_db
# # # import uuid




# # # router = APIRouter(prefix="/products", tags=["products"])
# # # logger = logging.getLogger(__name__)


# # # # # Configuration
# # # # IMAGE_UPLOAD_DIR = "uploads/products"
# # # # ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
# # # # MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# # # # # Ensure upload directory exists
# # # # os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

# # # # def save_uploaded_image(file: UploadFile) -> Optional[str]:
# # # #     if not file:
# # # #         return None
    
    
        
# # # #     # Validate file type
# # # #     if file.content_type not in ALLOWED_IMAGE_TYPES:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST,
# # # #             detail=f"Invalid image type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
# # # #         )
    
# # # #     # Validate file size
# # # #     file.file.seek(0, 2)  # Seek to end
# # # #     file_size = file.file.tell()
# # # #     file.file.seek(0)  # Reset pointer
    
# # # #     if file_size > MAX_IMAGE_SIZE:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST,
# # # #             detail=f"Image too large. Max size: {MAX_IMAGE_SIZE//(1024*1024)}MB"
# # # #         )
    
# # # #     # Generate unique filename
# # # #     ext = os.path.splitext(file.filename)[1]
# # # #     filename = f"{uuid4().hex}{ext}"
# # # #     filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)
    
# # # #     # Save file
# # # #     with open(filepath, "wb") as buffer:
# # # #         file.file.seek(0)  # reset before saving        
# # # #         buffer.write(file.file.read())  # save
   
    
# # # #     return filename



# # # # @router.post("/", response_model=schemas.Product)
# # # # async def create_product(
# # # #     name: str = Form(...),
# # # #     slug: str = Form(...),
# # # #     description: Optional[str] = Form(None),
# # # #     price: float = Form(...),
# # # #     quantity: int = Form(...),
# # # #     category_id: int = Form(...),
# # # #     brand_id: int = Form(...),
# # # #     is_active: bool = Form(True),
# # # #     image: Optional[UploadFile] = File(None),
# # # #     db: Session = Depends(get_db)
# # # # ):
    

# # # #     print("Creating product with slug:", image)
# # # #     # Check if slug exists
# # # #     existing_product = db.query(models.Product).filter(
# # # #         models.Product.slug == slug
# # # #     ).first()
# # # #     if existing_product:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST,
# # # #             detail="Product with this slug already exists"
# # # #         )
    
# # # #     # Validate category exists
# # # #     category = db.query(models.Category).get(category_id)
# # # #     if not category:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_404_NOT_FOUND,
# # # #             detail="Category not found"
# # # #         )
    
# # # #     # Validate brand exists
# # # #     brand = db.query(models.Brand).get(brand_id)
# # # #     if not brand:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_404_NOT_FOUND,
# # # #             detail="Brand not found"
# # # #         )
    
# # # #     # Validate brand-category association
# # # #     ancestor_rels = db.query(models.CategoryRelationship).filter(
# # # #         models.CategoryRelationship.descendant_id == category_id,
# # # #         models.CategoryRelationship.depth > 0
# # # #     ).all()
# # # #     ancestor_ids = [rel.ancestor_id for rel in ancestor_rels] + [category_id]
    
# # # #     brand_categories = db.query(models.category_brand_association).filter(
# # # #         models.category_brand_association.c.brand_id == brand_id,
# # # #         models.category_brand_association.c.category_id.in_(ancestor_ids)
# # # #     ).first()
    
# # # #     if not brand_categories:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST,
# # # #             detail="Brand is not associated with the selected category or its ancestors"
# # # #         )
    
# # # #     # Handle image upload
# # # #     image_filename = None
# # # #     if image:
# # # #         try:
# # # #             image_filename = save_uploaded_image(image)
# # # #         except HTTPException as e:
# # # #             raise e
# # # #         except Exception as e:
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # # #                 detail=f"Failed to upload image: {str(e)}"
# # # #             )


# # # #     # print("path is",f"/{os.path.join(IMAGE_UPLOAD_DIR, image_filename).replace("\\", "/")}")
    
# # # #     # Create product
# # # #     db_product = models.Product(
# # # #         name=name,
# # # #         slug=slug,
# # # #         description=description,
# # # #         price=price,
# # # #         quantity=quantity,
# # # #         is_active=is_active,
# # # #         category_id=category_id,
# # # #         brand_id=brand_id,
# # # #         # image_url=f"/{IMAGE_UPLOAD_DIR}/{image_filename}" if image_filename else None
# # # #         # image_url=f"/{os.path.join(IMAGE_UPLOAD_DIR, image_filename).replace("\\", "/")}" if image_filename else None
# # # #         image_path=image_filename if image_filename else None
        


# # # #     )
    
# # # #     db.add(db_product)
# # # #     db.commit()
# # # #     db.refresh(db_product)
# # # #     return db_product




# # # from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException, status
# # # from sqlalchemy.orm import Session
# # # from typing import Optional
# # # from uuid import uuid4
# # # import os

# # # from app import models, schemas
# # # from app.database import get_db

# # # # Image config
# # # IMAGE_UPLOAD_DIR = "uploads/products"
# # # ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
# # # MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# # # # Ensure upload directory exists
# # # os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

# # # router = APIRouter(prefix="/products", tags=["Products"])

# # # def save_uploaded_image(file: UploadFile) -> Optional[str]:
# # #     if not file:
# # #         return None

# # #     if file.content_type not in ALLOWED_IMAGE_TYPES:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Invalid image type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
# # #         )

# # #     file.file.seek(0, 2)  # move to end
# # #     file_size = file.file.tell()
# # #     file.file.seek(0)  # reset pointer

# # #     if file_size > MAX_IMAGE_SIZE:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Image too large. Max size: {MAX_IMAGE_SIZE // (1024 * 1024)}MB"
# # #         )

# # #     ext = os.path.splitext(file.filename)[1]
# # #     filename = f"{uuid4().hex}{ext}"
# # #     filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

# # #     with open(filepath, "wb") as buffer:
# # #         file.file.seek(0)
# # #         buffer.write(file.file.read())

# # #     return filename


# # # @router.post("/", response_model=schemas.Product)
# # # async def create_product(
# # #     name: str = Form(...),
# # #     slug: str = Form(...),
# # #     description: Optional[str] = Form(None),
# # #     price: float = Form(...),
# # #     quantity: int = Form(...),
# # #     category_id: int = Form(...),
# # #     brand_id: int = Form(...),
# # #     is_active: bool = Form(True),
# # #     image: Optional[UploadFile] = File(None),
# # #     db: Session = Depends(get_db)
# # # ):
# # #     # Check for slug uniqueness
# # #     if db.query(models.Product).filter_by(slug=slug).first():
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Product with this slug already exists"
# # #         )

# # #     # Validate category
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")

# # #     # Validate brand
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")

# # #     # Validate brand-category association (including ancestors)
# # #     ancestors = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id,
# # #         models.CategoryRelationship.depth > 0
# # #     ).all()
# # #     ancestor_ids = [rel.ancestor_id for rel in ancestors] + [category_id]

# # #     brand_assoc = db.query(models.category_brand_association).filter(
# # #         models.category_brand_association.c.brand_id == brand_id,
# # #         models.category_brand_association.c.category_id.in_(ancestor_ids)
# # #     ).first()

# # #     if not brand_assoc:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Brand is not associated with this category or its ancestors"
# # #         )

# # #     # Save image
# # #     image_filename = None
# # #     if image:
# # #         try:
# # #             image_filename = save_uploaded_image(image)
# # #         except HTTPException as e:
# # #             raise e
# # #         except Exception as e:
# # #             raise HTTPException(
# # #                 status_code=500,
# # #                 detail=f"Image upload failed: {str(e)}"
# # #             )

# # #     # Create product entry
# # #     product = models.Product(
# # #         name=name,
# # #         slug=slug,
# # #         description=description,
# # #         price=price,
# # #         quantity=quantity,
# # #         is_active=is_active,
# # #         category_id=category_id,
# # #         brand_id=brand_id,
# # #         image_path=image_filename  # stored filename (can be used to create a URL)
# # #     )

# # #     db.add(product)
# # #     db.commit()
# # #     db.refresh(product)

# # #     return product













# # # # ======================================================================================





# # # # @router.post("/bulk")
# # # # async def bulk_create_products(file: UploadFile = File(...)):
# # # #     try:
# # # #         # Read the uploaded file
# # # #         contents = await file.read()
# # # #         text_contents = contents.decode('utf-8')
        
# # # #         # Parse CSV
# # # #         csv_reader = csv.DictReader(io.StringIO(text_contents))
# # # #         products = []
# # # #         errors = []
# # # #         created_count = 0
        
# # # #         for row_num, row in enumerate(csv_reader, start=2):  # row_num starts at 2 (header is 1)
# # # #             try:
# # # #                 # Validate required fields
# # # #                 if not all(key in row for key in ['Image', 'Name', 'Price', 'Stock', 'Category', 'Brand', 'Status']):
# # # #                     raise ValueError("Missing required fields")
                
# # # #                 # Convert and validate data types
# # # #                 price = float(row['Price'])
# # # #                 quantity = int(row['Stock'])
# # # #                 is_active = row['Status'].lower() in ['active', 'true', 'yes', '1']
                
# # # #                 # Create product data
# # # #                 product_data = {
# # # #                     'image': row['Image'],
# # # #                     'name': row['Name'],
# # # #                     'price': price,
# # # #                     'quantity': quantity,
# # # #                     'category': row['Category'],
# # # #                     'brand': row['Brand'],
# # # #                     'is_active': is_active
# # # #                 }
                
# # # #                 # Here you would typically save to database
# # # #                 # For example: await save_product_to_db(product_data)
# # # #                 products.append(product_data)
# # # #                 created_count += 1
                
# # # #             except ValueError as ve:
# # # #                 errors.append(f"Row {row_num}: Invalid data - {str(ve)}")
# # # #             except Exception as e:
# # # #                 errors.append(f"Row {row_num}: {str(e)}")
        
# # # #         if errors and not products:
# # # #             raise HTTPException(
# # # #                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# # # #                 detail=errors
# # # #             )
        
# # # #         return JSONResponse(
# # # #             status_code=status.HTTP_201_CREATED,
# # # #             content={
# # # #                 "message": "Bulk upload processed",
# # # #                 "created_count": created_count,
# # # #                 "error_count": len(errors),
# # # #                 "errors": errors if errors else None
# # # #             }
# # # #         )
        
# # # #     except Exception as e:
# # # #         raise HTTPException(
# # # #             status_code=status.HTTP_400_BAD_REQUEST,
# # # #             detail=f"Error processing file: {str(e)}"
# # # #         )

# # # # # Helper function to save product to database (example)
# # # # async def save_product_to_db(product_data: dict):
# # # #     # This would be your actual database insertion logic
# # # #     # For example using SQLAlchemy, MongoDB, etc.
# # # #     pass






# # # IMAGE_UPLOAD_DIR = "uploads/products"


# # # def validate_and_set_image_path(filename: str) -> Optional[str]:
# # #     """Validate if image exists and return the path (filename only)"""
# # #     if not filename:
# # #         return None

# # #     filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

# # #     if not os.path.isfile(filepath):
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Image file '{filename}' not found in {IMAGE_UPLOAD_DIR}"
# # #         )

# # #     return filename  # only store filename in DB (not full path)


# # # @router.post("/productsbulk")
# # # async def bulk_upload_products(
# # #     file: UploadFile = File(...),
# # #     db: Session = Depends(get_db)
# # # ):
# # #     if not file.filename.endswith(".csv"):
# # #         raise HTTPException(status_code=400, detail="Only CSV files are supported")

# # #     contents = await file.read()
# # #     decoded = contents.decode("utf-8").splitlines()
# # #     reader = csv.DictReader(decoded)

# # #     created_products = []
# # #     errors = []

# # #     for i, row in enumerate(reader, start=1):
# # #         try:
# # #             image_path = validate_and_set_image_path(row.get("image_filename", "").strip())

# # #             # Validate required fields
# # #             if not row.get("name") or not row.get("slug"):
# # #                 errors.append(f"Row {i}: Missing required fields: name or slug")
# # #                 continue

# # #             # Optional: Check for slug conflicts
# # #             existing = db.query(models.Product).filter(models.Product.slug == row["slug"]).first()
# # #             if existing:
# # #                 errors.append(f"Row {i}: Slug '{row['slug']}' already exists")
# # #                 continue

# # #             # Create product
# # #             product = models.Product(
# # #                 name=row["name"],
# # #                 slug=row["slug"],
# # #                 description=row.get("description", ""),
# # #                 price=float(row["price"]) if row.get("price") else 0.0,
# # #                 quantity=int(row["quantity"]) if row.get("quantity") else 0,
# # #                 category_id=int(row["category_id"]),
# # #                 brand_id=int(row["brand_id"]),
# # #                 is_active=row.get("is_active", "true").lower() == "true",
# # #                 image_path=image_path
# # #             )

# # #             db.add(product)
# # #             created_products.append(product)

# # #         except Exception as e:
# # #             errors.append(f"Row {i}: {str(e)}")

# # #     db.commit()

# # #     return {
# # #         "created": len(created_products),
# # #         "errors": errors
# # #     }





# # # @router.post("bulk", status_code=status.HTTP_201_CREATED)
# # # async def bulk_create_products(
# # #     file: UploadFile = File(...),
# # #     db: Session = Depends(get_db),
# # #     auto_associate: bool = True
# # # ):
# # #     """
# # #     Bulk create products from CSV with:
# # #     - Automatic category/brand creation with unique slugs
# # #     - Automatic brand-category associations
# # #     - Comprehensive validation and error handling
# # #     """
# # #     try:
# # #         # Validate file type
# # #         if not file.filename.lower().endswith('.csv'):
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_400_BAD_REQUEST,
# # #                 detail="Only CSV files are allowed"
# # #             )

# # #         # Read and parse CSV
# # #         contents = await file.read()
# # #         csv_data = io.StringIO(contents.decode('utf-8'))
# # #         csv_reader = csv.DictReader(csv_data)
        
# # #         if not csv_reader.fieldnames:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# # #                 detail="CSV file is empty or missing headers"
# # #             )

# # #         stats = {
# # #             'created': 0,
# # #             'updated_associations': 0,
# # #             'created_categories': 0,
# # #             'created_brands': 0,
# # #             'errors': []
# # #         }

# # #         # Cache for existing categories/brands to reduce DB queries
# # #         category_cache = {}
# # #         brand_cache = {}

# # #         for row_num, row in enumerate(csv_reader, start=2):
# # #             try:
# # #                 # Clean and validate row
# # #                 cleaned_row = {
# # #                     'image_path': str(row.get('image_path', '')).strip(),
# # #                     'name': str(row.get('name', '')).strip(),
# # #                     'price': str(row.get('price', '')).strip(),
# # #                     'quantity': str(row.get('quantity', '')).strip(),
# # #                     'category': str(row.get('category', '')).strip(),
# # #                     'brand': str(row.get('brand', '')).strip(),
# # #                     'is_active': str(row.get('is_active', '')).strip().lower()
# # #                 }

# # #                 # Validate required fields
# # #                 for field, value in cleaned_row.items():
# # #                     if not value and field != 'image_path':  # image_path can be empty
# # #                         raise ValueError(f"Missing required field: {field}")

# # #                 # Convert and validate numeric fields
# # #                 try:
# # #                     price = float(cleaned_row['price'])
# # #                     quantity = int(cleaned_row['quantity'])
# # #                     if price <= 0 or quantity < 0:
# # #                         raise ValueError("Price must be > 0 and quantity >= 0")
# # #                 except ValueError:
# # #                     raise ValueError("Invalid numeric value for price/quantity")

# # #                 # --- Handle Category ---
# # #                 category_name = cleaned_row['category']
# # #                 category = category_cache.get(category_name.lower())
                
# # #                 if not category:
# # #                     category = db.query(models.Category).filter(
# # #                         func.lower(models.Category.name) == category_name.lower()
# # #                     ).first()
                    
# # #                     if not category and auto_associate:
# # #                         base_slug = category_name.lower().replace(" ", "-")
# # #                         slug = base_slug
# # #                         counter = 1
                        
# # #                         # Ensure slug is unique
# # #                         while True:
# # #                             existing = db.query(models.Category).filter(
# # #                                 models.Category.slug == slug
# # #                             ).first()
# # #                             if not existing:
# # #                                 break
# # #                             slug = f"{base_slug}-{counter}"
# # #                             counter += 1
                        
# # #                         category = models.Category(
# # #                             name=category_name,
# # #                             slug=slug,
# # #                             is_active=True,
# # #                             is_leaf=True
# # #                         )
# # #                         db.add(category)
# # #                         db.flush()
# # #                         stats['created_categories'] += 1
                    
# # #                     if category:  # Cache found or created category
# # #                         category_cache[category_name.lower()] = category

# # #                 # --- Handle Brand ---
# # #                 brand_name = cleaned_row['brand']
# # #                 brand = brand_cache.get(brand_name.lower())
                
# # #                 if not brand:
# # #                     brand = db.query(models.Brand).filter(
# # #                         func.lower(models.Brand.name) == brand_name.lower()
# # #                     ).first()
                    
# # #                     if not brand and auto_associate:
# # #                         base_slug = brand_name.lower().replace(" ", "-")
# # #                         slug = base_slug
# # #                         counter = 1
                        
# # #                         # Ensure slug is unique
# # #                         while True:
# # #                             existing = db.query(models.Brand).filter(
# # #                                 models.Brand.slug == slug
# # #                             ).first()
# # #                             if not existing:
# # #                                 break
# # #                             slug = f"{base_slug}-{counter}"
# # #                             counter += 1
                        
# # #                         brand = models.Brand(
# # #                             name=brand_name,
# # #                             slug=slug,
# # #                             is_active=True
# # #                         )
# # #                         db.add(brand)
# # #                         db.flush()
# # #                         stats['created_brands'] += 1
                    
# # #                     if brand:  # Cache found or created brand
# # #                         brand_cache[brand_name.lower()] = brand

# # #                 if not category or not brand:
# # #                     raise ValueError("Category/Brand not found and auto-associate is disabled")

# # #                 # Handle association
# # #                 if brand not in category.brands:
# # #                     if auto_associate:
# # #                         category.brands.append(brand)
# # #                         stats['updated_associations'] += 1
# # #                     else:
# # #                         raise ValueError("Brand not associated with category")

# # #                 # Create product with unique slug
# # #                 base_product_slug = cleaned_row['name'].lower().replace(" ", "-")
# # #                 product_slug = f"{base_product_slug}-{uuid.uuid4().hex[:4]}"

      
# # #                 product = models.Product(
# # #                     image_path=cleaned_row['image_path'],
# # #                     name=cleaned_row['name'],
# # #                     price=price,
# # #                     quantity=quantity,
# # #                     category_id=category.id,
# # #                     brand_id=brand.id,
# # #                     is_active=cleaned_row['is_active'] in ['true', 'yes', '1', 'active'],
# # #                     slug=product_slug,
# # #                     created_at=datetime.utcnow(),
# # #                     updated_at=datetime.utcnow()
# # #                 )
# # #                 db.add(product)
# # #                 stats['created'] += 1

# # #             except Exception as e:
# # #                 stats['errors'].append(f"Row {row_num}: {str(e)}")

# # #         db.commit()
        
# # #         response = {
# # #             "message": "Bulk upload processed",
# # #             "stats": stats
# # #         }
        
# # #         if stats['errors']:
# # #             response["error_count"] = len(stats['errors'])
# # #             response["sample_errors"] = stats['errors'][:5]  # Show first 5 errors
        
# # #         return response

# # #     except csv.Error as e:
# # #         db.rollback()
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Invalid CSV format: {str(e)}"
# # #         )
# # #     except Exception as e:
# # #         db.rollback()
# # #         raise HTTPException(
# # #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #             detail=f"Processing error: {str(e)}"
# # #         )

# # # # ==============================================================================
 



# # # # @router.get("/", response_model=List[schemas.Product])
# # # # def get_all_products(
# # # #     db: Session = Depends(get_db),
# # # #     category_id: Optional[int] = Query(None, description="Filter by category and its descendants"),
# # # #     brand_id: Optional[int] = Query(None, description="Filter by brand"),
# # # #     min_price: Optional[float] = Query(None, description="Minimum price"),
# # # #     max_price: Optional[float] = Query(None, description="Maximum price"),
# # # #     is_active: Optional[bool] = Query(None, description="Filter by active status")
# # # # ):
# # # #     query = db.query(models.Product)
    
# # # #     # Apply category filter (include all descendants)
# # # #     if category_id:
# # # #         # Verify category exists
# # # #         category = db.query(models.Category).get(category_id)
# # # #         if not category:
# # # #             raise HTTPException(status_code=404, detail="Category not found")
        
# # # #         # Get all descendant category IDs
# # # #         descendant_rels = db.query(models.CategoryRelationship).filter(
# # # #             models.CategoryRelationship.ancestor_id == category_id
# # # #         ).all()
# # # #         descendant_ids = [rel.descendant_id for rel in descendant_rels]
        
# # # #         query = query.filter(models.Product.category_id.in_(descendant_ids))
    
# # # #     # Apply brand filter
# # # #     if brand_id:
# # # #         query = query.filter(models.Product.brand_id == brand_id)
# # # #     # Apply price filters
# # # #     if min_price is not None:
# # # #         query = query.filter(models.Product.price >= min_price)
# # # #     if max_price is not None:
# # # #         query = query.filter(models.Product.price <= max_price)
    
# # # #     # Apply active status filter
# # # #     if is_active is not None:
# # # #         query = query.filter(models.Product.is_active == is_active)
    
# # # #     return query.all()



# # # @router.get("/products/", response_model=List[schemas.ProductOut])
# # # async def get_products(
# # #     page: int = 1,
# # #     limit: int = 10,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     products = db.query(models.Product).offset((page-1)*limit).limit(limit).all()
    
# # #     # Ensure None descriptions are converted to empty strings
# # #     for product in products:
# # #         if product.description is None:
# # #             product.description = ""
    
# # #     return products


# # # # ==========================================================================

# # # @router.put("/{product_id}", response_model=schemas.Product)
# # # async def update_product(
# # #     product_id: int,
# # #     request: Request,  # <- Add this temporarily

# # #     name: str = Form(...),
# # #     slug: str = Form(...),
# # #     description: str = Form(...),
# # #     price: float = Form(...),
# # #     quantity: int = Form(...),
# # #     category_id: int = Form(...),
# # #     brand_id: int = Form(...),
# # #     is_active: bool = Form(...),
# # #     image: Optional[UploadFile] = File(None),
# # #     db: Session = Depends(get_db)
# # # ):
# # #     db_product = db.query(models.Product).get(product_id)
# # #     if not db_product:
# # #         raise HTTPException(status_code=404, detail="Product not found")

# # #     # Check slug conflict
# # #     if slug != db_product.slug:
# # #         existing_product = db.query(models.Product).filter(models.Product.slug == slug).first()
# # #         if existing_product:
# # #             raise HTTPException(status_code=400, detail="Slug already exists")

# # #     # Validate category
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")

# # #     # Validate brand
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")

# # #     # Validate brand-category association
# # #     ancestor_rels = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id,
# # #         models.CategoryRelationship.depth > 0
# # #     ).all()
# # #     ancestor_ids = [rel.ancestor_id for rel in ancestor_rels] + [category_id]

# # #     brand_categories = db.query(models.category_brand_association).filter(
# # #         models.category_brand_association.c.brand_id == brand_id,
# # #         models.category_brand_association.c.category_id.in_(ancestor_ids)
# # #     ).first()

# # #     if not brand_categories:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Brand is not associated with the selected category or its ancestors"
# # #         )

# # #     # Save new image if uploaded
# # #     if image:
# # #         image_filename = save_uploaded_image(image)
# # #         db_product.image_path = image_filename

# # #     # Update fields
# # #     db_product.name = name
# # #     db_product.slug = slug
# # #     db_product.description = description
# # #     db_product.price = price
# # #     db_product.quantity = quantity
# # #     db_product.category_id = category_id
# # #     db_product.brand_id = brand_id
# # #     db_product.is_active = is_active
    

# # #     db.commit()
# # #     db.refresh(db_product)
# # #     return db_product


# # # # =============================================================================


# # # @router.delete("/{product_id}")
# # # def delete_product(product_id: int, db: Session = Depends(get_db)):
# # #     product = db.query(models.Product).get(product_id)
# # #     if not product:
# # #         raise HTTPException(status_code=404, detail="Product not found")
    
# # #     db.delete(product)
# # #     db.commit()
# # #     return {"message": "Product deleted successfully"}
    



    



# # # =========================================================================================================================================================


# # # =========================================================================================================================================================


# # from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, status, Query
# # from fastapi.responses import JSONResponse

# # from sqlalchemy.orm import Session
# # from sqlalchemy import func

# # from typing import List, Optional
# # from uuid import uuid4
# # from datetime import datetime
# # import csv
# # import io
# # import os
# # import logging
# # import uuid


# # from app import schemas, models
# # from ..database import get_db
# # import shutil







# # router = APIRouter(prefix="/products", tags=["products"])
# # logger = logging.getLogger(__name__)


# # # # CREATE
# # # @router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
# # # def create_product(
# # #     product: schemas.ProductCreate, 
# # #     db: Session = Depends(get_db),
# # #     image: UploadFile = File(None)
# # # ):
# # #     # Check category exists
# # #     if not db.query(models.Category).get(product.category_id):
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Invalid category ID"
# # #         )
    
# # #     # Check brand exists
# # #     if not db.query(models.Brand).get(product.brand_id):
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Invalid brand ID"
# # #         )
    
# # #     db_product = models.Product(**product.model_dump())
    
# # #     # Handle image upload
# # #     if image:
# # #         try:
# # #             upload_dir = "uploads/products"
# # #             os.makedirs(upload_dir, exist_ok=True)
# # #             file_path = f"{upload_dir}/{image.filename}"
# # #             with open(file_path, "wb") as buffer:
# # #                 shutil.copyfileobj(image.file, buffer)
# # #             db_product.image_path = file_path
# # #         except Exception as e:
# # #             raise HTTPException(
# # #                 status_code=500,
# # #                 detail=f"Error uploading image: {str(e)}"
# # #             )
    
# # #     db.add(db_product)
# # #     db.commit()
# # #     db.refresh(db_product)
# # #     return db_product




# # # # Image config
# # # IMAGE_UPLOAD_DIR = "uploads/products"
# # # ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
# # # MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# # # # Ensure upload directory exists
# # # os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

# # # router = APIRouter(prefix="/products", tags=["Products"])

# # # def save_uploaded_image(file: UploadFile) -> Optional[str]:
# # #     if not file:
# # #         return None

# # #     if file.content_type not in ALLOWED_IMAGE_TYPES:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Invalid image type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
# # #         )

# # #     file.file.seek(0, 2)  # move to end
# # #     file_size = file.file.tell()
# # #     file.file.seek(0)  # reset pointer

# # #     if file_size > MAX_IMAGE_SIZE:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Image too large. Max size: {MAX_IMAGE_SIZE // (1024 * 1024)}MB"
# # #         )

# # #     ext = os.path.splitext(file.filename)[1]
# # #     filename = f"{uuid4().hex}{ext}"
# # #     filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

# # #     with open(filepath, "wb") as buffer:
# # #         file.file.seek(0)
# # #         buffer.write(file.file.read())

# # #     return filename


# # # @router.post("/", response_model=schemas.Product)
# # # async def create_product(
# # #     name: str = Form(...),
# # #     slug: str = Form(...),
# # #     description: Optional[str] = Form(None),
# # #     price: float = Form(...),
# # #     quantity: int = Form(...),
# # #     category_id: int = Form(...),
# # #     brand_id: int = Form(...),
# # #     is_active: bool = Form(True),
# # #     image: Optional[UploadFile] = File(None),
# # #     db: Session = Depends(get_db)
# # # ):
# # #     # Check for slug uniqueness
# # #     if db.query(models.Product).filter_by(slug=slug).first():
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Product with this slug already exists"
# # #         )

# # #     # Validate category
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")

# # #     # Validate brand
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")

# # #     # Validate brand-category association (including ancestors)
# # #     ancestors = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id,
# # #         models.CategoryRelationship.depth > 0
# # #     ).all()
# # #     ancestor_ids = [rel.ancestor_id for rel in ancestors] + [category_id]

# # #     brand_assoc = db.query(models.category_brand_association).filter(
# # #         models.category_brand_association.c.brand_id == brand_id,
# # #         models.category_brand_association.c.category_id.in_(ancestor_ids)
# # #     ).first()

# # #     if not brand_assoc:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Brand is not associated with this category or its ancestors"
# # #         )

# # #     # Save image
# # #     image_filename = None
# # #     if image:
# # #         try:
# # #             image_filename = save_uploaded_image(image)
# # #         except HTTPException as e:
# # #             raise e
# # #         except Exception as e:
# # #             raise HTTPException(
# # #                 status_code=500,
# # #                 detail=f"Image upload failed: {str(e)}"
# # #             )

# # #     # Create product entry
# # #     product = models.Product(
# # #         name=name,
# # #         slug=slug,
# # #         description=description,
# # #         price=price,
# # #         quantity=quantity,
# # #         is_active=is_active,
# # #         category_id=category_id,
# # #         brand_id=brand_id,
# # #         image_path=image_filename  # stored filename (can be used to create a URL)
# # #     )

# # #     db.add(product)
# # #     db.commit()
# # #     db.refresh(product)

# # #     return product



# # # Configuration
# # # 👇 Add this line here
# # BASE_URL = "http://localhost:8000"
# # IMAGE_UPLOAD_DIR = "uploads/products"
# # ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
# # MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# # # Ensure folder exists
# # os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

# # def save_uploaded_image(file: UploadFile) -> Optional[str]:
# #     if not file:
# #         return None
# #     if file.content_type not in ALLOWED_IMAGE_TYPES:
# #         raise HTTPException(status_code=400, detail="Unsupported image type")

# #     ext = file.filename.split(".")[-1]
# #     filename = f"{uuid.uuid4().hex}.{ext}"
# #     file_path = os.path.join(IMAGE_UPLOAD_DIR, filename)

# #     content = file.file.read()
# #     if len(content) > MAX_IMAGE_SIZE:
# #         raise HTTPException(status_code=400, detail="Image file too large")

# #     with open(file_path, "wb") as f:
# #         f.write(content)

# #         return file_path.replace("\\", "/")  # ✅ Ensure web-compatible path




# # @router.post("/products", response_model=schemas.ProductOut)
# # def create_product(
# #     name: str = Form(...),
# #     slug: str = Form(...),
# #     description: Optional[str] = Form(None),
# #     price: float = Form(...),
# #     quantity: int = Form(...),
# #     is_active: bool = Form(True),
# #     category_id: int = Form(...),
# #     brand_id: int = Form(...),
# #     image: Optional[UploadFile] = File(None),
# #     db: Session = Depends(get_db)
# # ):
# #     image_path = None

# #     if image:
# #         if image.content_type not in ALLOWED_IMAGE_TYPES:
# #             raise HTTPException(status_code=400, detail="Unsupported image type")

# #         content = image.file.read()
# #         if len(content) > MAX_IMAGE_SIZE:
# #             raise HTTPException(status_code=400, detail="Image file too large")

# #         file_ext = os.path.splitext(image.filename)[-1]
# #         file_name = f"{uuid.uuid4().hex}{file_ext}"
# #         full_path = os.path.join(IMAGE_UPLOAD_DIR, file_name)

# #         with open(full_path, "wb") as buffer:
# #             buffer.write(content)

# #         image_path = full_path.replace(os.sep, "/")

# #     db_product = models.Product(
# #         name=name,
# #         slug=slug,
# #         description=description,
# #         price=price,
# #         quantity=quantity,
# #         is_active=is_active,
# #         category_id=category_id,
# #         brand_id=brand_id,
# #         image_path=image_path
# #     )
# #     db.add(db_product)
# #     db.commit()
# #     db.refresh(db_product)

# #     product_out = schemas.ProductOut.model_validate(db_product)
# #     if image_path:
# #         product_out.image_url = f"{BASE_URL}/{image_path}"
# #     return product_out

# # # -----------for bulk-------------------------


# # @router.post("/bulk-upload", 
# #              response_model=List[schemas.ProductOut],
# #              status_code=status.HTTP_201_CREATED,
# #              summary="Bulk upload products from CSV")
# # async def bulk_upload_products(
# #     file: UploadFile = File(..., description="CSV file with product data"),
# #     db: Session = Depends(get_db)
# # ):
# #     """
# #     Bulk upload products from CSV file.
    
# #     CSV Format (header row required):
# #     name,slug,description,price,quantity,is_active,category_id,brand_id,image_path
    
# #     Example row:
# #     "Premium Laptop","premium-laptop","High-end laptop",1299.99,50,true,5,2,"laptops/premium.jpg"
# #     """
# #     try:
# #         # Read and parse the CSV file
# #         contents = await file.read()
# #         text_contents = contents.decode('utf-8')
# #         csv_reader = csv.DictReader(io.StringIO(text_contents))
        
# #         products = []
# #         errors = []
        
# #         with db.begin():
# #             for row_num, row in enumerate(csv_reader, 1):
# #                 try:
# #                     # Validate required fields
# #                     if not all(k in row for k in ['name', 'slug', 'price', 'category_id', 'brand_id']):
# #                         raise ValueError("Missing required fields")
                    
# #                     # Convert types
# #                     row['price'] = float(row['price'])
# #                     row['quantity'] = int(row.get('quantity', 0))
# #                     row['is_active'] = row.get('is_active', 'true').lower() == 'true'
# #                     row['category_id'] = int(row['category_id'])
# #                     row['brand_id'] = int(row['brand_id'])
                    
# #                     # Check category exists
# #                     if not db.query(models.Category).get(row['category_id']):
# #                         raise ValueError(f"Category ID {row['category_id']} not found")
                    
# #                     # Check brand exists
# #                     if not db.query(models.Brand).get(row['brand_id']):
# #                         raise ValueError(f"Brand ID {row['brand_id']} not found")
                    
# #                     # Create product
# #                     product = models.Product(
# #                         name=row['name'],
# #                         slug=row['slug'],
# #                         description=row.get('description'),
# #                         price=row['price'],
# #                         quantity=row['quantity'],
# #                         is_active=row['is_active'],
# #                         category_id=row['category_id'],
# #                         brand_id=row['brand_id'],
# #                         image_path=row.get('image_path'),
# #                         created_at=datetime.utcnow(),
# #                         updated_at=datetime.utcnow()
# #                     )
                    
# #                     db.add(product)
# #                     db.flush()  # Get the ID
# #                     products.append(product)
                    
# #                 except Exception as e:
# #                     errors.append({
# #                         'row': row_num,
# #                         'error': str(e),
# #                         'data': row
# #                     })
            
# #             if errors:
# #                 db.rollback()
# #                 return {
# #                     "message": "Some products failed validation",
# #                     "success_count": len(products),
# #                     "error_count": len(errors),
# #                     "errors": errors
# #                 }
            
# #             # Commit if no errors
# #             db.commit()
            
# #             # Refresh all products to get complete data
# #             for product in products:
# #                 db.refresh(product)
            
# #             return products
            
# #     except csv.Error as e:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail=f"Invalid CSV file: {str(e)}"
# #         )
# #     except Exception as e:
# #         db.rollback()
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=f"Error processing bulk upload: {str(e)}"
# #         )



# # # ------------------------------------------------------------------------------


# # # READ
# # @router.get("/", response_model=List[schemas.ProductOut])
# # def list_products(
# #     skip: int = 0,
# #     limit: int = 100,
# #     category_id: int = None,
# #     brand_id: int = None,
# #     is_active: bool = None,
# #     min_price: float = None,
# #     max_price: float = None,
# #     db: Session = Depends(get_db)
# # ):
# #     query = db.query(models.Product)
    
# #     if category_id is not None:
# #         query = query.filter(models.Product.category_id == category_id)
# #     if brand_id is not None:
# #         query = query.filter(models.Product.brand_id == brand_id)
# #     if is_active is not None:
# #         query = query.filter(models.Product.is_active == is_active)
# #     if min_price is not None:
# #         query = query.filter(models.Product.price >= min_price)
# #     if max_price is not None:
# #         query = query.filter(models.Product.price <= max_price)
        
# #     return query.offset(skip).limit(limit).all()



# # @router.get("/{product_id}", response_model=schemas.ProductOut)
# # def get_product(product_id: int, db: Session = Depends(get_db)):
# #     product = db.query(models.Product).get(product_id)
# #     if not product:
# #         raise HTTPException(status_code=404, detail="Product not found")
# #     return product

# # # UPDATE
# # @router.put("/{product_id}", response_model=schemas.ProductOut)
# # def update_product(
# #     product_id: int,
# #     product: schemas.ProductUpdate,
# #     db: Session = Depends(get_db),
# #     image: UploadFile = File(None)
# # ):
# #     db_product = db.query(models.Product).get(product_id)
# #     if not db_product:
# #         raise HTTPException(status_code=404, detail="Product not found")
    
# #     update_data = product.model_dump(exclude_unset=True)
    
# #     # Handle image upload
# #     if image:
# #         try:
# #             # Delete old image if exists
# #             if db_product.image_path and os.path.exists(db_product.image_path):
# #                 os.remove(db_product.image_path)
                
# #             upload_dir = "uploads/products"
# #             os.makedirs(upload_dir, exist_ok=True)
# #             file_path = f"{upload_dir}/{image.filename}"
# #             with open(file_path, "wb") as buffer:
# #                 shutil.copyfileobj(image.file, buffer)
# #             update_data['image_path'] = file_path
# #         except Exception as e:
# #             raise HTTPException(
# #                 status_code=500,
# #                 detail=f"Error updating image: {str(e)}"
# #             )
    
# #     for field, value in update_data.items():
# #         setattr(db_product, field, value)
    
# #     db.commit()
# #     db.refresh(db_product)
# #     return db_product



# # # DELETE
# # @router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_product(product_id: int, db: Session = Depends(get_db)):
# #     product = db.query(models.Product).get(product_id)
# #     if not product:
# #         raise HTTPException(status_code=404, detail="Product not found")
    
# #     # Delete associated image
# #     if product.image_path and os.path.exists(product.image_path):
# #         try:
# #             os.remove(product.image_path)
# #         except Exception as e:
# #             pass  # Don't fail if image deletion fails
    
# #     db.delete(product)
# #     db.commit()













from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError, OperationalError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io
import os
import uuid
import shutil



from app.database import get_db


from app import schemas, models
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])

# Configuration
IMAGE_UPLOAD_DIR = "uploads/products"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload directory exists
os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

def save_uploaded_image(file: UploadFile) -> Optional[str]:
    """Save uploaded image and return the relative path"""
    if not file or file.content_type not in ALLOWED_IMAGE_TYPES:
        return None

    # Check file size
    file.file.seek(0, 2)  # Move to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset pointer
    
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image too large. Max size: {MAX_IMAGE_SIZE//1024//1024}MB"
        )

    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)

    # Save file
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving image: {str(e)}"
        )

    return filepath.replace("\\", "/")  # Ensure forward slashes for web

def get_image_url(image_path: Optional[str]) -> Optional[str]:
    """Convert filesystem path to URL path"""
    if not image_path:
        return None
    return f"/{image_path}"



@router.post("/products/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    slug: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    selling_price: Optional[float] = Form(None),  # NEW FIELD
    discount: Optional[float] = Form(None),         # NEW FIELD
    quantity: int = Form(None),
    is_active: bool = Form(True),
    category_id: int = Form(...),
    brand_id: int = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):


       # NEW: Calculate selling_price if discount is provided
    if discount and discount > 0:
        calculated_selling_price = price * (1 - discount/100)
        if selling_price is None:
            selling_price = calculated_selling_price
        else:
            # Ensure provided selling_price isn't lower than calculated
            selling_price = max(selling_price, calculated_selling_price)


    # Check if slug already exists
    if db.query(models.Product).filter(models.Product.slug == slug).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this slug already exists"
        )

    # Validate category exists
    category = db.query(models.Category).get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Validate brand exists and is associated with category
    brand = db.query(models.Brand).get(brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    # Check brand-category association (including ancestors)
    ancestor_ids = [category_id]
    ancestors = db.query(models.CategoryRelationship).filter(
        models.CategoryRelationship.descendant_id == category_id,
        models.CategoryRelationship.depth > 0
    ).all()
    ancestor_ids.extend([rel.ancestor_id for rel in ancestors])

    brand_assoc = db.query(models.category_brand_association).filter(
        models.category_brand_association.c.brand_id == brand_id,
        models.category_brand_association.c.category_id.in_(ancestor_ids)
    ).first()

    if not brand_assoc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Brand is not associated with this category or its ancestors"
        )

    # Handle image upload
    image_path = None
    if image:
        try:
            image_path = save_uploaded_image(image)
        except HTTPException as e:
            raise e

    # Create product
    product = models.Product(
        name=name,
        slug=slug,
        description=description,
        price=price,
        selling_price=selling_price,  # NEW FIELD
        discount=discount,            # NEW FIELD
        quantity=quantity,
        is_active=is_active,
        category_id=category_id,
        brand_id=brand_id,
        image_path=image_path,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    # Prepare response with image URL
    product_out = schemas.ProductOut(
        **product.__dict__,
        image_url=get_image_url(product.image_path),
        category=category,
        brand=brand
    )

    return product_out





# router = APIRouter()
@router.post("/bulk-upload")
async def bulk_upload_products(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="Only CSV files are allowed"
        )

    try:
        content = await file.read()
        content = content.decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(content))
        
        if not reader.fieldnames:
            raise HTTPException(
                status_code=400,
                detail="Empty CSV file or invalid format"
            )

        errors = []
        success_count = 0
        batch_size = 100  # Process in batches
        batch = []

        for i, row in enumerate(reader, start=2):
            try:
                # Validate required fields
                required = ["name", "slug", "price", "category_id", "brand_id"]
                missing = [field for field in required if not row.get(field)]
                if missing:
                    raise ValueError(f"Missing required fields: {missing}")

                # Handle image if provided
                image_path = None
                if row.get("image_path"):
                    # Validate image exists
                    if not os.path.exists(row["image_path"]):
                        raise ValueError(f"Image not found at path: {row['image_path']}")

                    # Copy image to uploads directory
                    ext = os.path.splitext(row["image_path"])[1]
                    new_filename = f"{uuid.uuid4().hex}{ext}"
                    new_path = os.path.join(IMAGE_UPLOAD_DIR, new_filename)
                    shutil.copy2(row["image_path"], new_path)
                    image_path = new_path.replace("\\", "/")

                product = models.Product(
                    name=row["name"],
                    slug=row["slug"],
                    price=float(row["price"]),
                    selling_price=float(row["selling_price"]) if row.get("selling_price") else None,  # NEW FIELD
                    discount=float(row.get("discount")),                                          # NEW FIELD
                    quantity=int(row.get("quantity")),
                    is_active=row.get("is_active", "True").lower() == "true",
                    category_id=int(row["category_id"]),
                    brand_id=int(row["brand_id"]),
                    image_path=image_path,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                batch.append(product)

                # Commit in batches
                if len(batch) >= batch_size:
                    db.bulk_save_objects(batch)
                    db.commit()
                    success_count += len(batch)
                    batch = []

            except Exception as e:
                errors.append({
                    "row": i,
                    "error": str(e),
                    "data": row
                })

        # Commit remaining items
        if batch:
            db.bulk_save_objects(batch)
            db.commit()
            success_count += len(batch)

        if errors:
            return {
                "message": "Partial success",
                "success_count": success_count,
                "error_count": len(errors),
                "errors": errors
            }

        return {
            "message": "All products uploaded successfully",
            "success_count": success_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
        

@router.get("/", response_model=List[schemas.ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_discount: Optional[float] = None,  # NEW FILTER
    max_discount: Optional[float] = None,  # NEW FILTER
    db: Session = Depends(get_db)
):
    """List products with optional filters"""
    query = db.query(models.Product)
    
    # Apply filters
    if min_discount is not None:                                             # NEW FILTER
        query = query.filter(models.Product.discount >= min_discount)
    if max_discount is not None:                                            # NEW FILTER
        query = query.filter(models.Product.discount <= max_discount)
    
    if category_id is not None:
        query = query.filter(models.Product.category_id == category_id)
    if brand_id is not None:
        query = query.filter(models.Product.brand_id == brand_id)
    if is_active is not None:
        query = query.filter(models.Product.is_active == is_active)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    
    # Convert to ProductOut with image URLs
    return [
        schemas.ProductOut(
            **product.__dict__,
            image_url=get_image_url(product.image_path),
            category=product.category,
            brand=product.brand
        )
        for product in products
    ]



@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID"""
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


    # NEW: Calculate final price if not set
    if product.selling_price is None and product.discount > 0:
        product.selling_price = product.price * (1 - product.discount/100)
    
    
    return schemas.ProductOut(
        **product.__dict__,
        image_url=get_image_url(product.image_path),
        category=product.category,
        brand=product.brand
    )
@router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    selling_price: Optional[float] = Form(None),  # NEW FIELD
    discount: Optional[float] = Form(None),       # NEW FIELD
    quantity: Optional[int] = Form(None),
    is_active: Optional[bool] = Form(None),
    category_id: Optional[int] = Form(None),
    brand_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        product = db.query(models.Product).get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

                # NEW: Price/discount calculation logic
        if discount is not None and discount > 0:
            current_price = price if price is not None else product.price
            calculated_selling_price = current_price * (1 - discount/100)
        
        if selling_price is None:
            selling_price = calculated_selling_price
        else:
            selling_price = max(selling_price, calculated_selling_price)


        # Create update dictionary with only provided fields
        update_data = {}
        if name is not None: 
            update_data["name"] = name
        if slug is not None:
            if slug != product.slug:
                if db.query(models.Product).filter(models.Product.slug == slug).first():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Product with this slug already exists"
                    )
            update_data["slug"] = slug
        if description is not None: 
            update_data["description"] = description
        if price is not None: 
            update_data["price"] = price

        if selling_price is not None:  # NEW FIELD
            update_data["selling_price"] = selling_price
        if discount is not None:       # NEW FIELD
            update_data["discount"] = discount

        if quantity is not None: 
            update_data["quantity"] = quantity
        if is_active is not None: 
            update_data["is_active"] = is_active
        
        # Handle relationships
        if category_id is not None:
            category = db.query(models.Category).get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
            update_data["category_id"] = category_id
        
        if brand_id is not None:
            brand = db.query(models.Brand).get(brand_id)
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not found"
                )
            update_data["brand_id"] = brand_id

        # Handle image update
        if image:
            try:
                # Delete old image if exists
                if product.image_path and os.path.exists(product.image_path):
                    os.remove(product.image_path)
                
                # Save new image
                image_path = save_uploaded_image(image)
                update_data["image_path"] = image_path
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error updating image: {str(e)}"
                )

        # Only update if there are changes
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            db.query(models.Product).filter(
                models.Product.id == product_id
            ).update(update_data)
            db.commit()
            db.refresh(product)

        return schemas.ProductOut(
            **product.__dict__,
            image_url=get_image_url(product.image_path),
            category=product.category,
            brand=product.brand
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )@router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    quantity: Optional[int] = Form(None),
    is_active: Optional[bool] = Form(None),
    category_id: Optional[int] = Form(None),
    brand_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        product = db.query(models.Product).get(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Create update dictionary with only provided fields
        update_data = {}
        if name is not None: 
            update_data["name"] = name
        if slug is not None:
            if slug != product.slug:
                if db.query(models.Product).filter(models.Product.slug == slug).first():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Product with this slug already exists"
                    )
            update_data["slug"] = slug
        if description is not None: 
            update_data["description"] = description
        if price is not None: 
            update_data["price"] = price
        if quantity is not None: 
            update_data["quantity"] = quantity
        if is_active is not None: 
            update_data["is_active"] = is_active
        
        # Handle relationships
        if category_id is not None:
            category = db.query(models.Category).get(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found"
                )
            update_data["category_id"] = category_id
        
        if brand_id is not None:
            brand = db.query(models.Brand).get(brand_id)
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not found"
                )
            update_data["brand_id"] = brand_id

        # Handle image update
        if image:
            try:
                # Delete old image if exists
                if product.image_path and os.path.exists(product.image_path):
                    os.remove(product.image_path)
                
                # Save new image
                image_path = save_uploaded_image(image)
                update_data["image_path"] = image_path
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error updating image: {str(e)}"
                )

        # Only update if there are changes
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            db.query(models.Product).filter(
                models.Product.id == product_id
            ).update(update_data)
            db.commit()
            db.refresh(product)

        return schemas.ProductOut(
            **product.__dict__,
            image_url=get_image_url(product.image_path),
            category=product.category,
            brand=product.brand
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Delete associated image if exists
    if product.image_path and os.path.exists(product.image_path):
        try:
            os.remove(product.image_path)
        except Exception:
            pass  # Don't fail if image deletion fails

    db.delete(product)
    db.commit()