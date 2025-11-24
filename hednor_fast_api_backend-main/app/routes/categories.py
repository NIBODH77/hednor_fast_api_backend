# # # from fastapi import APIRouter, Depends, HTTPException
# # # from sqlalchemy.orm import Session
# # # from typing import List

# # # from .. import models, schemas
# # # from ..database import get_db

# # # router = APIRouter(prefix="/categories", tags=["categories"])


# # # from fastapi import APIRouter, Depends, HTTPException, Query
# # # from sqlalchemy.orm import Session
# # # from typing import List, Optional

# # # from .. import models, schemas
# # # from ..database import get_db

# # # import os
# # # from datetime import datetime
# # # from uuid import uuid4


# # # router = APIRouter(prefix="/products", tags=["products"])


# # # # Configuration
# # # IMAGE_UPLOAD_DIR = "uploads/products"
# # # ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
# # # MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# # # # Ensure upload directory exists
# # # os.makedirs(IMAGE_UPLOAD_DIR, exist_ok=True)

# # # def save_uploaded_image(file: UploadFile) -> Optional[str]:
# # #     if not file:
# # #         return None
        
# # #     # Validate file type
# # #     if file.content_type not in ALLOWED_IMAGE_TYPES:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Invalid image type. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
# # #         )
    
# # #     # Validate file size
# # #     file.file.seek(0, 2)  # Seek to end
# # #     file_size = file.file.tell()
# # #     file.file.seek(0)  # Reset pointer
    
# # #     if file_size > MAX_IMAGE_SIZE:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail=f"Image too large. Max size: {MAX_IMAGE_SIZE//(1024*1024)}MB"
# # #         )
    
# # #     # Generate unique filename
# # #     ext = os.path.splitext(file.filename)[1]
# # #     filename = f"{uuid4().hex}{ext}"
# # #     filepath = os.path.join(IMAGE_UPLOAD_DIR, filename)
    
# # #     # Save file
# # #     with open(filepath, "wb") as buffer:
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
# # #     # Check if slug exists
# # #     existing_product = db.query(models.Product).filter(
# # #         models.Product.slug == slug
# # #     ).first()
# # #     if existing_product:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Product with this slug already exists"
# # #         )
    
# # #     # Validate category exists
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_404_NOT_FOUND,
# # #             detail="Category not found"
# # #         )
    
# # #     # Validate brand exists
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(
# # #             status_code=status.HTTP_404_NOT_FOUND,
# # #             detail="Brand not found"
# # #         )
    
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
# # #             status_code=status.HTTP_400_BAD_REQUEST,
# # #             detail="Brand is not associated with the selected category or its ancestors"
# # #         )
    
# # #     # Handle image upload
# # #     image_filename = None
# # #     if image:
# # #         try:
# # #             image_filename = save_uploaded_image(image)
# # #         except HTTPException as e:
# # #             raise e
# # #         except Exception as e:
# # #             raise HTTPException(
# # #                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# # #                 detail=f"Failed to upload image: {str(e)}"
# # #             )
    
# # #     # Create product
# # #     db_product = models.Product(
# # #         name=name,
# # #         slug=slug,
# # #         description=description,
# # #         price=price,
# # #         quantity=quantity,
# # #         is_active=is_active,
# # #         category_id=category_id,
# # #         brand_id=brand_id,
# # #         image_url=f"/{IMAGE_UPLOAD_DIR}/{image_filename}" if image_filename else None
# # #     )
    
# # #     db.add(db_product)
# # #     db.commit()
# # #     db.refresh(db_product)
# # #     return db_product

# # # @router.get("/", response_model=List[schemas.Product])
# # # def get_all_products(
# # #     db: Session = Depends(get_db),
# # #     category_id: Optional[int] = Query(None, description="Filter by category and its descendants"),
# # #     brand_id: Optional[int] = Query(None, description="Filter by brand"),
# # #     min_price: Optional[float] = Query(None, description="Minimum price"),
# # #     max_price: Optional[float] = Query(None, description="Maximum price"),
# # #     is_active: Optional[bool] = Query(None, description="Filter by active status")
# # # ):
# # #     query = db.query(models.Product)
    
# # #     # Apply category filter (include all descendants)
# # #     if category_id:
# # #         # Verify category exists
# # #         category = db.query(models.Category).get(category_id)
# # #         if not category:
# # #             raise HTTPException(status_code=404, detail="Category not found")
        
# #       # Get all descendant category IDs
# # #         descendant_rels = db.query(models.CategoryRelationship).filter(
# # #             models.CategoryRelationship.ancestor_id == category_id
# # #         ).all()
# # #         descendant_ids = [rel.descendant_id for rel in descendant_rels]
        
# # #         query = query.filter(models.Product.category_id.in_(descendant_ids))
    
# # #     # Apply brand filter
# # #     if brand_id:
# # #         query = query.filter(models.Product.brand_id == brand_id)
    
# # #     # Apply price filters
# # #     if min_price is not None:
# # #         query = query.filter(models.Product.price >= min_price)
# # #     if max_price is not None:
# # #         query = query.filter(models.Product.price <= max_price)
    
# # #     # Apply active status filter
# # #     if is_active is not None:
# # #         query = query.filter(models.Product.is_active == is_active)
    
# # #     return query.all()

# # # @router.get("/{product_id}", response_model=schemas.Product)
# # # def get_product(product_id: int, db: Session = Depends(get_db)):
# # #     product = db.query(models.Product).get(product_id)
# # #     if not product:
# # #         raise HTTPException(status_code=404, detail="Product not found")
# # #     return product

# # # @router.put("/{product_id}", response_model=schemas.Product)
# # # def update_product(
# # #     product_id: int,
# # #     product_update: schemas.ProductUpdate,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     db_product = db.query(models.Product).get(product_id)
# # #     if not db_product:
# # #         raise HTTPException(status_code=404, detail="Product not found")
    
# # #     # Check if slug is being updated and if new slug exists
# # #     if product_update.slug and product_update.slug != db_product.slug:
# # #         existing_product = db.query(models.Product).filter(
# # #             models.Product.slug == product_update.slug
# # #         ).first()
# # #         if existing_product:
# # #             raise HTTPException(status_code=400, detail="Product with this slug already exists")
    
# # #     # Verify category if being updated
# # #     if product_update.category_id is not None:
# # #         category = db.query(models.Category).get(product_update.category_id)
# # #         if not category:
# # #             raise HTTPException(status_code=404, detail="Category not found")
    
# # #     # Verify brand if being updated
# # #     if product_update.brand_id is not None:
# # #         brand = db.query(models.Brand).get(product_update.brand_id)
# # #         if not brand:
# # #             raise HTTPException(status_code=404, detail="Brand not found")
        
# # #         # If both category and brand are being updated, validate association
# # #         if product_update.category_id is not None:
# # #             new_category_id = product_update.category_id
# # #         else:
# # #             new_category_id = db_product.category_id
        
# # #         # Check brand-category association
# # #         ancestor_rels = db.query(models.CategoryRelationship).filter(
# # #             models.CategoryRelationship.descendant_id == new_category_id,
# # #             models.CategoryRelationship.depth > 0
# # #         ).all()
# # #         ancestor_ids = [rel.ancestor_id for rel in ancestor_rels] + [new_category_id]
        
# # #         brand_categories = db.query(models.category_brand_association).filter(
# # #             models.category_brand_association.c.brand_id == product_update.brand_id,
# # #             models.category_brand_association.c.category_id.in_(ancestor_ids)
# # #         ).first()
        
# # #         if not brand_categories:
# # #             raise HTTPException(
# # #                 status_code=400,
# # #                 detail="Brand is not associated with the selected category or its ancestors"
# # #             )
    
# # #     # Update fields
# # #     for field, value in product_update.dict(exclude_unset=True).items():
# # #         setattr(db_product, field, value)
    
# # #     db.add(db_product)
# # #     db.commit()
# # #     db.refresh(db_product)
# # #     return db_product

# # # @router.delete("/{product_id}")
# # # def delete_product(product_id: int, db: Session = Depends(get_db)):
# # #     product = db.query(models.Product).get(product_id)
# # #     if not product:
# # #         raise HTTPException(status_code=404, detail="Product not found")
    
# # #     db.delete(product)
# # #     db.commit()
# # #     return {"message": "Product deleted successfully"}
    



    
# # # @router.post("/bulk", response_model=List[schemas.Category])
# # # def create_bulk_categories(categories: List[schemas.CategoryCreate], db: Session = Depends(get_db)):
# # #     created_categories = []
# # #     for category in categories:
# # #         # Similar logic as single create, but optimized for bulk
# # #         existing_category = db.query(models.Category).filter(
# # #             models.Category.slug == category.slug
# # #         ).first()
# # #         if existing_category:
# # #             continue  # Skip duplicates
        
# # #         db_category = models.Category(
# # #             name=category.name,
# # #             slug=category.slug,
# # #             description=category.description,
# # #             is_active=category.is_active,
# # #             is_leaf=True
# # #         )
# # #         db.add(db_category)
# # #         db.commit()
# # #         db.refresh(db_category)
        
# # #         self_relationship = models.CategoryRelationship(
# # #             ancestor_id=db_category.id,
# # #             descendant_id=db_category.id,
# # #             depth=0
# # #         )
# # #         db.add(self_relationship)
        
# # #         if category.parent_id:
# # #             parent = db.query(models.Category).get(category.parent_id)
# # #             if parent:
# # #                 parent_relationships = db.query(models.CategoryRelationship).filter(
# # #                     models.CategoryRelationship.descendant_id == parent.id
# # #                 ).all()
                
# # #                 for rel in parent_relationships:
# # #                     new_rel = models.CategoryRelationship(
# # #                         ancestor_id=rel.ancestor_id,
# # #                         descendant_id=db_category.id,
# # #                         depth=rel.depth + 1
# # #                     )
# # #                     db.add(new_rel)
                
# # #                 parent.is_leaf = False
# # #                 db.add(parent)
        
# # #         db.commit()
# # #         created_categories.append(db_category)
    
# # #     return created_categories

# # # @router.get("/", response_model=List[schemas.Category])
# # # def get_all_categories(db: Session = Depends(get_db)):
# # #     return db.query(models.Category).all()

# # # @router.get("/{category_id}", response_model=schemas.CategoryWithRelationships)
# # # def get_category(category_id: int, db: Session = Depends(get_db)):
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")
    
# # #     # Get ancestors and descendants through relationships
# # #     ancestor_rels = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id,
# # #         models.CategoryRelationship.depth > 0
# # #     ).all()
    
# # #     descendant_rels = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.ancestor_id == category_id,
# # #         models.CategoryRelationship.depth > 0
# # #     ).all()
    
# # #     ancestors = [db.query(models.Category).get(rel.ancestor_id) for rel in ancestor_rels]
# # #     descendants = [db.query(models.Category).get(rel.descendant_id) for rel in descendant_rels]
    
# # #     # Get associated brands
# # #     brands = category.brands
    
# # #     return {
# # #         **category.__dict__,
# # #         "ancestors": ancestors,
# # #         "descendants": descendants,
# # #         "brands": brands
# # #     }

# # # @router.put("/{category_id}", response_model=schemas.Category)
# # # def update_category(
# # #     category_id: int, 
# # #     category_update: schemas.CategoryUpdate, 
# # #     db: Session = Depends(get_db)
# # # ):
# # #     db_category = db.query(models.Category).get(category_id)
# # #     if not db_category:
# # #         raise HTTPException(status_code=404, detail="Category not found")
    
# # #     for field, value in category_update.dict(exclude_unset=True).items():
# # #         setattr(db_category, field, value)
    
# # #     db.add(db_category)
# # #     db.commit()
# # #     db.refresh(db_category)
# # #     return db_category

# # # @router.delete("/{category_id}")
# # # def delete_category(category_id: int, db: Session = Depends(get_db)):
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")
    
# # #     # Check if category has products
# # #     product_count = db.query(models.Product).filter(
# # #         models.Product.category_id == category_id
# # #     ).count()
# # #     if product_count > 0:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Cannot delete category with associated products"
# # #         )
    
# # #     # Check if category has children
# # #     child_count = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.ancestor_id == category_id,
# # #         models.CategoryRelationship.depth == 1
# # #     ).count()
# # #     if child_count > 0:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Cannot delete category with child categories"
# # #         )
    
# # #     # Delete all relationships involving this category
# # #     db.query(models.CategoryRelationship).filter(
# # #         (models.CategoryRelationship.ancestor_id == category_id) |
# # #         (models.CategoryRelationship.descendant_id == category_id)
# # #     ).delete()
    
# # #     # If this was a child category, check if parent is now a leaf
# # #     parent_rels = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id,
# # #         models.CategoryRelationship.depth == 1
# # #     ).all()
    
# # #     for rel in parent_rels:
# # #         parent = db.query(models.Category).get(rel.ancestor_id)
# # #         if parent:
# # #             # Check if parent has any other children
# # #             other_children = db.query(models.CategoryRelationship).filter(
# # #                 models.CategoryRelationship.ancestor_id == parent.id,
# # #                 models.CategoryRelationship.depth == 1
# # #             ).count()
# # #             if other_children == 0:
# # #                 parent.is_leaf = True
# # #                 db.add(parent)
    
# # #     db.delete(category)
# # #     db.commit()
# # #     return {"message": "Category deleted successfully"}







# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session
# # from typing import List, Optional

# # from .. import models, schemas
# # from ..database import get_db
# # from ..models import fast_add_relationships  # ✅ import optimized relationship function
# # from sqlalchemy.orm import Session
# # from typing import List
# # import logging
# # from sqlalchemy import update
# # from pydantic import ValidationError





# # router = APIRouter(prefix="/categories", tags=["categories"])
# # logger = logging.getLogger(__name__)


# # @router.post("/", response_model=schemas.Category)
# # def create_category(
# #     category: schemas.CategoryCreate, 
# #     db: Session = Depends(get_db)
# # ):
# #     # Check if category with this slug already exists
# #     existing_category = db.query(models.Category).filter(
# #         models.Category.slug == category.slug
# #     ).first()
# #     if existing_category:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="Category with this slug already exists"
# #         )

# #     # Create new category
# #     db_category = models.Category(
# #         name=category.name,
# #         slug=category.slug,
# #         description=category.description,
# #         is_active=category.is_active,
# #         is_leaf=True  # Default to true, will be updated if children added
# #     )
# #     db.add(db_category)
# #     db.commit()
# #     db.refresh(db_category)

# #     # # Create self-relationship
# #     # self_relationship = models.CategoryRelationship(
# #     #     ancestor_id=db_category.id,
# #     #     descendant_id=db_category.id,
# #     #     depth=0
# #     # )
# #     # db.add(self_relationship)

# #     # # If parent_id is provided, create relationships
# #     # if category.parent_id:
# #     #     parent = db.query(models.Category).get(category.parent_id)
# #     #     if not parent:
# #     #         raise HTTPException(
# #     #             status_code=status.HTTP_404_NOT_FOUND,
# #     #             detail="Parent category not found"
# #     #         )

# #     #     # Get all parent's ancestor relationships
# #     #     parent_relationships = db.query(models.CategoryRelationship).filter(
# #     #         models.CategoryRelationship.descendant_id == parent.id
# #     #     ).all()

# #     #     # Create new relationships for each ancestor
# #     #     for rel in parent_relationships:
# #     #         new_rel = models.CategoryRelationship(
# #     #             ancestor_id=rel.ancestor_id,
# #     #             descendant_id=db_category.id,
# #     #             depth=rel.depth + 1
# #     #         )
# #     #         db.add(new_rel)

# #     #     # Update parent's is_leaf status
# #     #     parent.is_leaf = False
# #     #     db.add(parent)

# #     # db.commit()
# #     # return db_category





# # # ====================================================================================================================


# # # @router.post("/bulk", response_model=List[schemas.Category])
# # # def create_bulk_categories(
# # #     categories: List[schemas.CategoryCreate], 
# # #     db: Session = Depends(get_db)
# # # ):
# # #     created_categories = []
# # #     for category in categories:
# # #         # Check for existing category
# # #         existing_category = db.query(models.Category).filter(
# # #             models.Category.slug == category.slug
# # #         ).first()
# # #         if existing_category:
# # #             continue  # Skip duplicates

# # #         # Create new category
# # #         db_category = models.Category(
# # #             name=category.name,
# # #             slug=category.slug,
# # #             description=category.description,
# # #             is_active=category.is_active,
# # #             is_leaf=True
# # #         )
# # #         db.add(db_category)
# # #         db.commit()
# # #         db.refresh(db_category)

# # #         # Create self-relationship
# # #         self_relationship = models.CategoryRelationship(
# # #             ancestor_id=db_category.id,
# # #             descendant_id=db_category.id,
# # #             depth=0
# # #         )
# # #         db.add(self_relationship)

# # #         # Handle parent relationship if exists
# # #         if category.parent_id:
# # #             parent = db.query(models.Category).get(category.parent_id)
# # #             if parent:
# # #                 parent_relationships = db.query(models.CategoryRelationship).filter(
# # #                     models.CategoryRelationship.descendant_id == parent.id
# # #                 ).all()

# # #                 for rel in parent_relationships:
# # #                     new_rel = models.CategoryRelationship(
# # #                         ancestor_id=rel.ancestor_id,
# # #                         descendant_id=db_category.id,
# # #                         depth=rel.depth + 1
# # #                     )
# # #                     db.add(new_rel)

# # #                 parent.is_leaf = False
# # #                 db.add(parent)

# # #         db.commit()
# # #         created_categories.append(db_category)

# # #     return created_categories




# # router = APIRouter(prefix="/categories", tags=["categories"])

# # @router.post("/bulk", 
# #              response_model=List[schemas.Category], 
# #              status_code=status.HTTP_201_CREATED,
# #              summary="Create categories in bulk with hierarchy",
# #              responses={
# #                  422: {"description": "Validation Error"},
# #                  500: {"description": "Internal Server Error"}
# #              })
# # async def create_bulk_categories(
# #     categories_data: List[dict],
# #     db: Session = Depends(get_db)
# # ):
# #     """
# #     Insert multiple categories with hierarchy in bulk, maintaining parent-child relationships
# #     and closure table for efficient querying.

# #     Example Input:
# #     [
# #         {
# #             "name": "Electronics",
# #             "slug": "electronics",
# #             "description": "All electronic devices",
# #             "is_active": true,
# #             "is_leaf": false,
# #             "children": [
# #                 {
# #                     "name": "Computers",
# #                     "slug": "computers",
# #                     "is_leaf": false,
# #                     "children": [...]
# #                 }
# #             ]
# #         }
# #     ]
# #     """
# #     try:
# #         # Start a new transaction explicitly
# #         with db.begin():
# #             created_categories = []
            
# #             def process_category(data: dict, parent_id: int = None) -> models.Category:
# #                 # Validate input against our schema
# #                 try:
# #                     category_schema = schemas.CategoryCreate(**data)
# #                 except ValidationError as e:
# #                     raise ValueError(f"Invalid category data: {e.errors()}")

# #                 # Create and save the category
# #                 category = models.Category(
# #                     name=category_schema.name,
# #                     slug=category_schema.slug,
# #                     description=category_schema.description,
# #                     is_active=category_schema.is_active,
# #                     is_leaf=category_schema.is_leaf,
# #                     parent_id=parent_id
# #                 )
# #                 db.add(category)
# #                 db.flush()  # Get the ID immediately

# #                 # Create self-relationship (required for closure table)
# #                 db.add(models.CategoryRelationship(
# #                     ancestor_id=category.id,
# #                     descendant_id=category.id,
# #                     depth=0
# #                 ))

# #                 # If this isn't a root category, inherit parent relationships
# #                 if parent_id:
# #                     parent_rels = db.query(models.CategoryRelationship).filter(
# #                         models.CategoryRelationship.descendant_id == parent_id
# #                     ).all()
                    
# #                     for rel in parent_rels:
# #                         db.add(models.CategoryRelationship(
# #                             ancestor_id=rel.ancestor_id,
# #                             descendant_id=category.id,
# #                             depth=rel.depth + 1
# #                         ))

# #                 # Process children recursively if they exist
# #                 if 'children' in data and data['children']:
# #                     for child_data in data['children']:
# #                         process_category(child_data, category.id)

# #                 created_categories.append(category)
# #                 return category

# #             # Process all root categories
# #             for category_data in categories_data:
# #                 process_category(category_data)

# #             # Refresh all created categories to ensure we return complete data
# #             for cat in created_categories:
# #                 db.refresh(cat)

# #             return created_categories

# #     except ValueError as e:
# #         # This handles our custom validation errors
# #         raise HTTPException(
# #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# #             detail=str(e)
# #         )
# #     except Exception as e:
# #         # This catches any other unexpected errors
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=f"Failed to create categories: {str(e)}"
# #         )



# # # def fast_add_relationships(db: Session, category_obj: Category):
# # #     # Add self relationship
# # #     db.add(CategoryRelationship(
# # #         ancestor_id=category_obj.id,
# # #         descendant_id=category_obj.id,
# # #         depth=0
# # #     ))

# # #     # Add relationships from ancestors (if parent exists)
# # #     parent = category_obj.parent
# # #     while parent:
# # #         db.add(CategoryRelationship(
# # #             ancestor_id=parent.id,
# # #             descendant_id=category_obj.id,
# # #             depth=1  # Will auto-increment deeper if while-loop continues
# # #         ))
# # #         # Now go up the tree
# # #         rel = db.query(Category).filter(Category.id == parent.parent_id).first()
# # #         parent = rel if rel else None

# # #     db.commit()




# # # ===========================================================================





# # @router.get("/", response_model=List[schemas.Category])
# # def get_all_categories(db: Session = Depends(get_db)):
# #     return db.query(models.Category).all()

# # @router.get("/{category_id}", response_model=schemas.CategoryWithRelationships)
# # def get_category(category_id: int, db: Session = Depends(get_db)):
# #     category = db.query(models.Category).get(category_id)
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )

# #     # Get ancestors and descendants through relationships
# #     ancestor_rels = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.descendant_id == category_id,
# #         models.CategoryRelationship.depth > 0
# #     ).all()

# #     descendant_rels = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.ancestor_id == category_id,
# #         models.CategoryRelationship.depth > 0
# #     ).all()

# #     ancestors = [db.query(models.Category).get(rel.ancestor_id) for rel in ancestor_rels]
# #     descendants = [db.query(models.Category).get(rel.descendant_id) for rel in descendant_rels]

# #     # Get associated brands
# #     brands = category.brands

# #     return {
# #         **category.__dict__,
# #         "ancestors": ancestors,
# #         "descendants": descendants,
# #         "brands": brands
# #     }

# # @router.put("/{category_id}", response_model=schemas.Category)
# # def update_category(
# #     category_id: int, 
# #     category_update: schemas.CategoryUpdate, 
# #     db: Session = Depends(get_db)
# # ):
# #     db_category = db.query(models.Category).get(category_id)
# #     if not db_category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )

# #     # Check if slug is being updated and already exists
# #     if category_update.slug and category_update.slug != db_category.slug:
# #         existing_category = db.query(models.Category).filter(
# #             models.Category.slug == category_update.slug
# #         ).first()
# #         if existing_category:
# #             raise HTTPException(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 detail="Category with this slug already exists"
# #             )

# #     # Update fields
# #     for field, value in category_update.dict(exclude_unset=True).items():
# #         setattr(db_category, field, value)

# #     db.add(db_category)
# #     db.commit()
# #     db.refresh(db_category)
# #     return db_category

# # @router.delete("/{category_id}")
# # def delete_category(category_id: int, db: Session = Depends(get_db)):
# #     category = db.query(models.Category).get(category_id)
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )

# #     # Check if category has products
# #     product_count = db.query(models.Product).filter(
# #         models.Product.category_id == category_id
# #     ).count()
# #     if product_count > 0:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="Cannot delete category with associated products"
# #         )

# #     # Check if category has children
# #     child_count = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.ancestor_id == category_id,
# #         models.CategoryRelationship.depth == 1
# #     ).count()
# #     if child_count > 0:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="Cannot delete category with child categories"
# #         )

# #     # Delete all relationships involving this category
# #     db.query(models.CategoryRelationship).filter(
# #         (models.CategoryRelationship.ancestor_id == category_id) |
# #         (models.CategoryRelationship.descendant_id == category_id)
# #     ).delete()

# #     # If this was a child category, check if parent is now a leaf
# #     parent_rels = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.descendant_id == category_id,
# #         models.CategoryRelationship.depth == 1
# #     ).all()

# #     for rel in parent_rels:
# #         parent = db.query(models.Category).get(rel.ancestor_id)
# #         if parent:
# #             # Check if parent has any other children
# #             other_children = db.query(models.CategoryRelationship).filter(
# #                 models.CategoryRelationship.ancestor_id == parent.id,
# #                 models.CategoryRelationship.depth == 1
# #             ).count()
# #             if other_children == 0:
# #                 parent.is_leaf = True
# #                 db.add(parent)

# #     db.delete(category)
# #     db.commit()
# #     return {"message": "Category deleted successfully"}




# # =========================================================================================================================================================


# # =========================================================================================================================================================






# # from fastapi import APIRouter, Depends, HTTPException, status, Query
# # from sqlalchemy.orm import Session
# # from typing import List, Optional
# # from ..schemas import category 
# # from app import models
# # from ..database import get_db



# # router = APIRouter(prefix="/categories", tags=["categories"])

# # # -------------------------------
# # # CREATE Operations
# # # -------------------------------
# # # (Your existing bulk create endpoint would go here)

# # @router.post("/", 
# #             response_model=schemas.Category,
# #             status_code=status.HTTP_201_CREATED)
# # def create_category(
# #     category: schemas.CategoryCreate, 
# #     db: Session = Depends(get_db)
# # ):
# #     """Create a single category"""
# #     try:
# #         # Check if slug already exists
# #         existing = db.query(models.Category).filter(
# #             models.Category.slug == category.slug
# #         ).first()
# #         if existing:
# #             raise HTTPException(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 detail="Category with this slug already exists"
# #             )

# #         db_category = models.Category(
# #             name=category.name,
# #             slug=category.slug,
# #             description=category.description,
# #             is_active=category.is_active,
# #             is_leaf=category.is_leaf,
# #             parent_id=category.parent_id
# #         )
# #         db.add(db_category)
# #         db.commit()
# #         db.refresh(db_category)
        
# #         # Add closure table relationships
# #         fast_add_relationships(db, db_category)
        
# #         return db_category
        
# #     except Exception as e:
# #         db.rollback()
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=f"Error creating category: {str(e)}"
# #         )

# # # -------------------------------
# # # READ Operations
# # # -------------------------------

# # @router.get("/", response_model=List[schemas.CategoryWithRelationships])
# # def list_categories(
# #     skip: int = 0,
# #     limit: int = 100,
# #     is_active: Optional[bool] = None,
# #     is_leaf: Optional[bool] = None,
# #     db: Session = Depends(get_db)
# # ):
# #     """List all categories with optional filters"""
# #     query = db.query(models.Category)
    
# #     if is_active is not None:
# #         query = query.filter(models.Category.is_active == is_active)
# #     if is_leaf is not None:
# #         query = query.filter(models.Category.is_leaf == is_leaf)
        
# #     return query.offset(skip).limit(limit).all()

# # @router.get("/{category_id}", response_model=schemas.CategoryWithRelationships)
# # def get_category(
# #     category_id: int, 
# #     db: Session = Depends(get_db)
# # ):
# #     """Get a single category by ID with all relationships"""
# #     category = db.query(models.Category).get(category_id)
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )
# #     return category

# # @router.get("/slug/{slug}", response_model=schemas.CategoryWithRelationships)
# # def get_category_by_slug(
# #     slug: str, 
# #     db: Session = Depends(get_db)
# # ):
# #     """Get a category by slug"""
# #     category = db.query(models.Category).filter(
# #         models.Category.slug == slug
# #     ).first()
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )
# #     return category

# # @router.get("/{category_id}/children", response_model=List[schemas.Category])
# # def get_category_children(
# #     category_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     """Get direct children of a category"""
# #     return db.query(models.Category).filter(
# #         models.Category.parent_id == category_id
# #     ).all()

# # @router.get("/{category_id}/tree", response_model=List[schemas.Category])
# # def get_category_tree(
# #     category_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     """Get entire subtree of a category using closure table"""
# #     category = db.query(models.Category).get(category_id)
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )
    
# #     # Get all descendants (excluding self)
# #     relationships = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.ancestor_id == category_id,
# #         models.CategoryRelationship.depth > 0
# #     ).all()
    
# #     descendant_ids = [rel.descendant_id for rel in relationships]
# #     if not descendant_ids:
# #         return []
        
# #     return db.query(models.Category).filter(
# #         models.Category.id.in_(descendant_ids)
# #     ).all()

# # # -------------------------------
# # # UPDATE Operations
# # # -------------------------------

# # @router.put("/{category_id}", response_model=schemas.Category)
# # def update_category(
# #     category_id: int,
# #     category: schemas.CategoryUpdate,
# #     db: Session = Depends(get_db)
# # ):
# #     """Update a category"""
# #     db_category = db.query(models.Category).get(category_id)
# #     if not db_category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )
    
# #     try:
# #         update_data = category.model_dump(exclude_unset=True)
        
# #         # Prevent changing parent if it would create cycles
# #         if 'parent_id' in update_data and update_data['parent_id']:
# #             # Check if new parent is a descendant (would create cycle)
# #             is_descendant = db.query(models.CategoryRelationship).filter(
# #                 models.CategoryRelationship.ancestor_id == category_id,
# #                 models.CategoryRelationship.descendant_id == update_data['parent_id'],
# #                 models.CategoryRelationship.depth > 0
# #             ).first()
            
# #             if is_descendant:
# #                 raise HTTPException(
# #                     status_code=status.HTTP_400_BAD_REQUEST,
# #                     detail="Cannot set parent to a descendant category"
# #                 )
        
# #         for field, value in update_data.items():
# #             setattr(db_category, field, value)
            
# #         db.commit()
# #         db.refresh(db_category)
        
# #         # If parent changed, rebuild relationships
# #         if 'parent_id' in update_data:
# #             rebuild_closure_table(db, db_category)
            
# #         return db_category
        
# #     except Exception as e:
# #         db.rollback()
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail=str(e)
# #         )

# # # -------------------------------
# # # DELETE Operations
# # # -------------------------------

# # @router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# # def delete_category(
# #     category_id: int,
# #     db: Session = Depends(get_db)
# # ):
# #     """Delete a category"""
# #     category = db.query(models.Category).get(category_id)
# #     if not category:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="Category not found"
# #         )
    
# #     try:
# #         # Check if category has products
# #         product_count = db.query(models.Product).filter(
# #             models.Product.category_id == category_id
# #         ).count()
        
# #         if product_count > 0:
# #             raise HTTPException(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 detail="Cannot delete category with associated products"
# #             )
        
# #         # Check if category has children
# #         child_count = db.query(models.Category).filter(
# #             models.Category.parent_id == category_id
# #         ).count()
        
# #         if child_count > 0:
# #             raise HTTPException(
# #                 status_code=status.HTTP_400_BAD_REQUEST,
# #                 detail="Cannot delete category with child categories"
# #             )
        
# #         # Delete from closure table first
# #         db.query(models.CategoryRelationship).filter(
# #             (models.CategoryRelationship.ancestor_id == category_id) |
# #             (models.CategoryRelationship.descendant_id == category_id)
# #         ).delete()
        
# #         # Then delete the category
# #         db.delete(category)
# #         db.commit()
        
# #     except Exception as e:
# #         db.rollback()
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail=f"Error deleting category: {str(e)}"
# #         )

# # # -------------------------------
# # # Helper Functions
# # # -------------------------------

# # def fast_add_relationships(db: Session, category_obj: models.Category):
# #     """Add closure table relationships for a new category"""
# #     # Self relationship
# #     self_rel = models.CategoryRelationship(
# #         ancestor_id=category_obj.id,
# #         descendant_id=category_obj.id,
# #         depth=0
# #     )
# #     db.add(self_rel)

# #     # Inherit ancestors from parent
# #     if category_obj.parent_id:
# #         parent_relationships = db.query(models.CategoryRelationship).filter(
# #             models.CategoryRelationship.descendant_id == category_obj.parent_id
# #         ).all()

# #         for parent_rel in parent_relationships:
# #             db.add(models.CategoryRelationship(
# #                 ancestor_id=parent_rel.ancestor_id,
# #                 descendant_id=category_obj.id,
# #                 depth=parent_rel.depth + 1
# #             ))

# #     db.commit()

# # def rebuild_closure_table(db: Session, category: models.Category):
# #     """Rebuild closure table relationships for a category after parent change"""
# #     # Delete all existing relationships for this category
# #     db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.descendant_id == category.id
# #     ).delete()
    
# #     # Add new relationships
# #     fast_add_relationships(db, category)
    
# #     # Update relationships for all descendants
# #     descendants = db.query(models.CategoryRelationship).filter(
# #         models.CategoryRelationship.ancestor_id == category.id,
# #         models.CategoryRelationship.depth > 0
# #     ).all()
    
# #     for rel in descendants:
# #         descendant = db.query(models.Category).get(rel.descendant_id)
# #         if descendant:
# #             rebuild_closure_table(db, descendant)




# from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.orm import Session
# from typing import List, Optional
# from app import schemas, models
# from ..database import get_db

# router = APIRouter(prefix="/categories", tags=["categories"])

# # -------------------------------
# # CREATE Operations
# # -------------------------------
# # (Your existing bulk create endpoint would go here)

# @router.post("/", 
#             response_model=schemas.Category,
#             status_code=status.HTTP_201_CREATED)
# def create_category(
#     category: schemas.CategoryCreate, 
#     db: Session = Depends(get_db)
# ):
#     """Create a single category"""
#     try:
#         # Check if slug already exists
#         existing = db.query(models.Category).filter(
#             models.Category.slug == category.slug
#         ).first()
#         if existing:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Category with this slug already exists"
#             )

#         db_category = models.Category(
#             name=category.name,
#             slug=category.slug,
#             description=category.description,
#             is_active=category.is_active,
#             is_leaf=category.is_leaf,
#             parent_id=category.parent_id
#         )
#         db.add(db_category)
#         db.commit()
#         db.refresh(db_category)
        
#         # Add closure table relationships
#         fast_add_relationships(db, db_category)
        
#         return db_category
        
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creating category: {str(e)}"
#         )

# # -------------------------------
# # READ Operations
# # -------------------------------

# @router.get("/", response_model=List[schemas.CategoryWithRelationships])
# def list_categories(
#     skip: int = 0,
#     limit: int = 100,
#     is_active: Optional[bool] = None,
#     is_leaf: Optional[bool] = None,
#     db: Session = Depends(get_db)
# ):
#     """List all categories with optional filters"""
#     query = db.query(models.Category)
    
#     if is_active is not None:
#         query = query.filter(models.Category.is_active == is_active)
#     if is_leaf is not None:
#         query = query.filter(models.Category.is_leaf == is_leaf)
        
#     return query.offset(skip).limit(limit).all()




# @router.get("/{category_id}", response_model=schemas.CategoryWithRelationships)
# def get_category(
#     category_id: int, 
#     db: Session = Depends(get_db)
# ):
#     """Get a single category by ID with all relationships"""
#     category = db.query(models.Category).get(category_id)
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
#     return category

    

# @router.get("/slug/{slug}", response_model=schemas.CategoryWithRelationships)
# def get_category_by_slug(
#     slug: str, 
#     db: Session = Depends(get_db)
# ):
#     """Get a category by slug"""
#     category = db.query(models.Category).filter(
#         models.Category.slug == slug
#     ).first()
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
#     return category

# @router.get("/{category_id}/children", response_model=List[schemas.Category])
# def get_category_children(
#     category_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Get direct children of a category"""
#     return db.query(models.Category).filter(
#         models.Category.parent_id == category_id
#     ).all()

# @router.get("/{category_id}/tree", response_model=List[schemas.Category])
# def get_category_tree(
#     category_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Get entire subtree of a category using closure table"""
#     category = db.query(models.Category).get(category_id)
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
    
#     # Get all descendants (excluding self)
#     relationships = db.query(models.CategoryRelationship).filter(
#         models.CategoryRelationship.ancestor_id == category_id,
#         models.CategoryRelationship.depth > 0
#     ).all()
    
#     descendant_ids = [rel.descendant_id for rel in relationships]
#     if not descendant_ids:
#         return []
        
#     return db.query(models.Category).filter(
#         models.Category.id.in_(descendant_ids)
#     ).all()

# # -------------------------------
# # UPDATE Operations
# # -------------------------------

# @router.put("/{category_id}", response_model=schemas.Category)
# def update_category(
#     category_id: int,
#     category: schemas.CategoryUpdate,
#     db: Session = Depends(get_db)
# ):
#     """Update a category"""
#     db_category = db.query(models.Category).get(category_id)
#     if not db_category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
    
#     try:
#         update_data = category.model_dump(exclude_unset=True)
        
#         # Prevent changing parent if it would create cycles
#         if 'parent_id' in update_data and update_data['parent_id']:
#             # Check if new parent is a descendant (would create cycle)
#             is_descendant = db.query(models.CategoryRelationship).filter(
#                 models.CategoryRelationship.ancestor_id == category_id,
#                 models.CategoryRelationship.descendant_id == update_data['parent_id'],
#                 models.CategoryRelationship.depth > 0
#             ).first()
            
#             if is_descendant:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail="Cannot set parent to a descendant category"
#                 )
        
#         for field, value in update_data.items():
#             setattr(db_category, field, value)
            
#         db.commit()
#         db.refresh(db_category)
        
#         # If parent changed, rebuild relationships
#         if 'parent_id' in update_data:
#             rebuild_closure_table(db, db_category)
            
#         return db_category
        
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )

# # -------------------------------
# # DELETE Operations
# # -------------------------------

# @router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(
#     category_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Delete a category"""
#     category = db.query(models.Category).get(category_id)
#     if not category:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Category not found"
#         )
    
#     try:
#         # Check if category has products
#         product_count = db.query(models.Product).filter(
#             models.Product.category_id == category_id
#         ).count()
        
#         if product_count > 0:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Cannot delete category with associated products"
#             )
        
#         # Check if category has children
#         child_count = db.query(models.Category).filter(
#             models.Category.parent_id == category_id
#         ).count()
        
#         if child_count > 0:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Cannot delete category with child categories"
#             )
        
#         # Delete from closure table first
#         db.query(models.CategoryRelationship).filter(
#             (models.CategoryRelationship.ancestor_id == category_id) |
#             (models.CategoryRelationship.descendant_id == category_id)
#         ).delete()
        
#         # Then delete the category
#         db.delete(category)
#         db.commit()
        
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error deleting category: {str(e)}"
#         )

# # -------------------------------
# # Helper Functions
# # -------------------------------

# def fast_add_relationships(db: Session, category_obj: models.Category):
#     """Add closure table relationships for a new category"""
#     # Self relationship
#     self_rel = models.CategoryRelationship(
#         ancestor_id=category_obj.id,
#         descendant_id=category_obj.id,
#         depth=0
#     )
#     db.add(self_rel)

#     # Inherit ancestors from parent
#     if category_obj.parent_id:
#         parent_relationships = db.query(models.CategoryRelationship).filter(
#             models.CategoryRelationship.descendant_id == category_obj.parent_id
#         ).all()

#         for parent_rel in parent_relationships:
#             db.add(models.CategoryRelationship(
#                 ancestor_id=parent_rel.ancestor_id,
#                 descendant_id=category_obj.id,
#                 depth=parent_rel.depth + 1
#             ))

#     db.commit()

# def rebuild_closure_table(db: Session, category: models.Category):
#     """Rebuild closure table relationships for a category after parent change"""
#     # Delete all existing relationships for this category
#     db.query(models.CategoryRelationship).filter(
#         models.CategoryRelationship.descendant_id == category.id
#     ).delete()
    
#     # Add new relationships
#     fast_add_relationships(db, category)
    
#     # Update relationships for all descendants
#     descendants = db.query(models.CategoryRelationship).filter(
#         models.CategoryRelationship.ancestor_id == category.id,
#         models.CategoryRelationship.depth > 0
#     ).all()
    
#     for rel in descendants:
#         descendant = db.query(models.Category).get(rel.descendant_id)
#         if descendant:
#             rebuild_closure_table(db, descendant)



# ====================================================================================================================
#                                  Categories Display-Hierarchy
# ====================================================================================================================




from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.schemas import CategorySearchResult


router = APIRouter()

# Helper function
def verify_category_exists(category_id: int, db: Session):
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.is_active == True
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found or inactive"
        )
    return category

@router.get("/top-level", response_model=List[schemas.CategoryWithChildren])
def get_top_level_categories(db: Session = Depends(get_db)):
    try:
        # Get all top-level categories
        categories = db.query(models.Category).filter(
            models.Category.parent_id == None,
            models.Category.is_active == True
        ).order_by(models.Category.name).all()
        
        if not categories:
            return []
        
        # Check which categories have children
        category_ids = [c.id for c in categories]
        parents_with_children = db.execute(
            text("SELECT DISTINCT parent_id FROM categories WHERE parent_id IN :ids AND is_active = TRUE"),
            {'ids': tuple(category_ids)}
        ).fetchall()
        
        parents_with_children_set = {row[0] for row in parents_with_children}
        
        # Build response
        response = []
        for category in categories:
            response.append(schemas.CategoryWithChildren(
                id=category.id,
                name=category.name,
                slug=category.slug,
                is_active=category.is_active,
                parent_id=category.parent_id,
                has_children=category.id in parents_with_children_set
            ))
            
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching top-level categories: {str(e)}"
        )

@router.get("/{category_id}/children", response_model=List[schemas.CategoryWithChildren])
def get_category_children(
    category_id: int, 
    db: Session = Depends(get_db)
):
    try:
        # Verify parent exists
        verify_category_exists(category_id, db)
        
        # Get children
        children = db.query(models.Category).filter(
            models.Category.parent_id == category_id,
            models.Category.is_active == True
        ).order_by(models.Category.name).all()
        
        if not children:
            return []
        
        # Check which children have their own children
        child_ids = [c.id for c in children]
        if child_ids:
            parents_with_children = db.execute(
                text("SELECT DISTINCT parent_id FROM categories WHERE parent_id IN :ids AND is_active = TRUE"),
                {'ids': tuple(child_ids)}
            ).fetchall()
            parents_with_children_set = {row[0] for row in parents_with_children}
        else:
            parents_with_children_set = set()
        
        # Build response
        response = []
        for child in children:
            response.append(schemas.CategoryWithChildren(
                id=child.id,
                name=child.name,
                slug=child.slug,
                is_active=child.is_active,
                parent_id=child.parent_id,
                has_children=child.id in parents_with_children_set
            ))
            
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching child categories: {str(e)}"
        )
    


 


@router.get("/{category_id}/hierarchy", response_model=List[schemas.CategoryPath])
def get_category_hierarchy(
    category_id: int,
    max_level: int = Query(9, ge=1, le=9),
    db: Session = Depends(get_db)
):
    """
    Get the hierarchical path of a category and its children up to the specified level.
    
    - **category_id**: ID of the category to start from
    - **max_level**: Maximum depth of hierarchy to return (1-9, default: 9)
    """
    try:
        verify_category_exists(category_id, db)
        
        query = """
            WITH RECURSIVE category_hierarchy AS (
                SELECT 
                    id,
                    name,
                    slug,
                    1 AS level,
                    name::TEXT AS path
                FROM categories
                WHERE id = :category_id AND is_active = TRUE
                
                UNION ALL
                
                SELECT
                    c.id,
                    c.name,
                    c.slug,
                    h.level + 1,
                    (h.path || ' > ' || c.name)::TEXT AS path
                FROM categories c
                JOIN category_hierarchy h ON c.parent_id = h.id
                WHERE c.is_active = TRUE
                AND h.level < :max_level
            )
            SELECT 
                id,
                name,
                slug,
                level,
                path
            FROM category_hierarchy
            ORDER BY path
        """
        result = db.execute(text(query), {'category_id': category_id, 'max_level': max_level})
        
        # Properly convert rows to dictionaries
        rows = result.mappings().all()
        return [schemas.CategoryPath.model_validate(row) for row in rows]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching category hierarchy: {str(e)}"
        )
    



@router.get("/search", response_model=List[CategorySearchResult])
def search_categories(
    query: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("SELECT * FROM search_categories_v2(:keyword, :max_limit)"),
            {"keyword": query, "max_limit": limit}
        )
        rows = result.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "slug": row[2],
                "level": row[3],
                "path": row[4]
            } for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching categories: {e}")