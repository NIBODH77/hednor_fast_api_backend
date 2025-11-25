# # # from fastapi import APIRouter, Depends, HTTPException
# # # from sqlalchemy.orm import Session
# # # from typing import List

# # # from .. import models, schemas
# # # from ..database import get_db

# # # router = APIRouter(prefix="/brands", tags=["brands"])



# # # @router.post("/", response_model=schemas.Brand)
# # # def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
# # #     # Check if slug exists
# # #     existing_brand = db.query(models.Brand).filter(
# # #         models.Brand.slug == brand.slug
# # #     ).first()
# # #     if existing_brand:
# # #         raise HTTPException(status_code=400, detail="Brand with this slug already exists")
    
# # #     db_brand = models.Brand(
# # #         name=brand.name,
# # #         slug=brand.slug,
# # #         description=brand.description,
# # #         is_active=brand.is_active
# # #     )
# # #     db.add(db_brand)
    
# # #     # Add category associations
# # #     for category_id in brand.category_ids:
# # #         category = db.query(models.Category).get(category_id)
# # #         if category:
# # #             db_brand.categories.append(category)
    
# # #     db.commit()
# # #     db.refresh(db_brand)
# # #     return db_brand




# # # @router.post("/bulk", response_model=List[schemas.Brand])
# # # def create_bulk_brands(brands: List[schemas.BrandCreate], db: Session = Depends(get_db)):
# # #     created_brands = []
# # #     for brand in brands:
# # #         existing_brand = db.query(models.Brand).filter(
# # #             models.Brand.slug == brand.slug
# # #         ).first()
# # #         if existing_brand:
# # #             continue
        
# # #         db_brand = models.Brand(
# # #             name=brand.name,
# # #             slug=brand.slug,
# # #             description=brand.description,
# # #             is_active=brand.is_active
# # #         )
# # #         db.add(db_brand)
        
# # #         for category_id in brand.category_ids:
# # #             category = db.query(models.Category).get(category_id)
# # #             if category:
# # #                 db_brand.categories.append(category)
        
# # #         db.commit()
# # #         db.refresh(db_brand)
# # #         created_brands.append(db_brand)
    
# # #     return created_brands



# # # @router.get("/", response_model=List[schemas.Brand])
# # # def get_all_brands(db: Session = Depends(get_db)):
# # #     return db.query(models.Brand).all()

# # # @router.get("/{brand_id}", response_model=schemas.BrandWithCategories)
# # # def get_brand(brand_id: int, db: Session = Depends(get_db)):
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")
    
# # #     categories = brand.categories
# # #     return {
# # #         **brand.__dict__,
# # #         "categories": categories
# # #     }



# # # @router.put("/{brand_id}", response_model=schemas.Brand)
# # # def update_brand(
# # #     brand_id: int,
# # #     brand_update: schemas.BrandUpdate,
# # #     db: Session = Depends(get_db)
# # # ):
# # #     db_brand = db.query(models.Brand).get(brand_id)
# # #     if not db_brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")
    
# # #     # Update simple fields
# # #     for field, value in brand_update.dict(exclude_unset=True, exclude={"category_ids"}).items():
# # #         setattr(db_brand, field, value)
    
# # #     # Update categories if provided
# # #     if brand_update.category_ids is not None:
# # #         # Clear existing categories
# # #         db_brand.categories = []
# # #         # Add new categories
# # #         for category_id in brand_update.category_ids:
# # #             category = db.query(models.Category).get(category_id)
# # #             if category:
# # #                 db_brand.categories.append(category)
    
# # #     db.add(db_brand)
# # #     db.commit()
# # #     db.refresh(db_brand)
# # #     return db_brand



# # # @router.delete("/{brand_id}")
# # # def delete_brand(brand_id: int, db: Session = Depends(get_db)):
# # #     brand = db.query(models.Brand).get(brand_id)
# # #     if not brand:
# # #         raise HTTPException(status_code=404, detail="Brand not found")
    
# # #     # Check if brand has products
# # #     product_count = db.query(models.Product).filter(
# # #         models.Product.brand_id == brand_id
# # #     ).count()
# # #     if product_count > 0:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail="Cannot delete brand with associated products"
# # #         )
    
# # #     # Remove all category associations (handled automatically by SQLAlchemy)
# # #     db.delete(brand)
# # #     db.commit()
# # #     return {"message": "Brand deleted successfully"}



# # # @router.get("/by-category/{category_id}", response_model=List[schemas.Brand])
# # # def get_brands_by_category(category_id: int, db: Session = Depends(get_db)):
# # #     # Verify category exists
# # #     category = db.query(models.Category).get(category_id)
# # #     if not category:
# # #         raise HTTPException(status_code=404, detail="Category not found")
    
# # #     # Get all ancestor category IDs (including self) using closure table
# # #     ancestor_rels = db.query(models.CategoryRelationship).filter(
# # #         models.CategoryRelationship.descendant_id == category_id
# # #     ).all()
# # #     ancestor_ids = [rel.ancestor_id for rel in ancestor_rels]
    
# # #     # Get brands associated with any of these categories
# # #     brands = db.query(models.Brand).join(
# # #         models.Brand.categories
# # #     ).filter(
# # #         models.Category.id.in_(ancestor_ids)
# # #     ).distinct().all()
    
# # #     return brands

    









# # # =========================================================================================================================================================


# # # =========================================================================================================================================================







# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from app import schemas, models
# from ..database import get_db




# router = APIRouter(prefix="/brands", tags=["brands"])

# # CREATE
# @router.post("/", response_model=schemas.Brand, status_code=status.HTTP_201_CREATED)
# def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
#     db_brand = models.Brand(
#         name=brand.name,
#         slug=brand.slug,
#         description=brand.description,
#         is_active=brand.is_active
#     )
#     db.add(db_brand)
#     db.commit()
#     db.refresh(db_brand)
    
#     # Add category associations if provided
#     if brand.category_ids:
#         categories = db.query(models.Category).filter(
#             models.Category.id.in_(brand.category_ids)
#         ).all()
#         db_brand.categories = categories
#         db.commit()
#         db.refresh(db_brand)
    
#     return db_brand




# # READ
# @router.get("/", response_model=List[schemas.BrandWithCategories])
# def list_brands(
#     skip: int = 0,
#     limit: int = 100,
#     is_active: bool = None,
#     db: Session = Depends(get_db)
# ):
#     query = db.query(models.Brand)
#     if is_active is not None:
#         query = query.filter(models.Brand.is_active == is_active)
#     return query.offset(skip).limit(limit).all()

# @router.get("/{brand_id}", response_model=schemas.BrandWithCategories)
# def get_brand(brand_id: int, db: Session = Depends(get_db)):
#     brand = db.query(models.Brand).get(brand_id)
#     if not brand:
#         raise HTTPException(status_code=404, detail="Brand not found")
#     return brand

# # UPDATE
# @router.put("/{brand_id}", response_model=schemas.BrandWithCategories)
# def update_brand(
#     brand_id: int,
#     brand: schemas.BrandUpdate,
#     db: Session = Depends(get_db)
# ):
#     db_brand = db.query(models.Brand).get(brand_id)
#     if not db_brand:
#         raise HTTPException(status_code=404, detail="Brand not found")
    
#     update_data = brand.model_dump(exclude_unset=True)
    
#     for field, value in update_data.items():
#         if field != 'category_ids':
#             setattr(db_brand, field, value)
    
#     if 'category_ids' in update_data:
#         categories = db.query(models.Category).filter(
#             models.Category.id.in_(brand.category_ids or [])
#         ).all()
#         db_brand.categories = categories
    
#     db.commit()
#     db.refresh(db_brand)
#     return db_brand

# # DELETE
# @router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_brand(brand_id: int, db: Session = Depends(get_db)):
#     brand = db.query(models.Brand).get(brand_id)
#     if not brand:
#         raise HTTPException(status_code=404, detail="Brand not found")
    
#     # Check for associated products
#     if db.query(models.Product).filter(
#         models.Product.brand_id == brand_id
#     ).count() > 0:
#         raise HTTPException(
#             status_code=400,
#             detail="Cannot delete brand with associated products"
#         )
    
#     db.delete(brand)
#     db.commit()






from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/brands", tags=["brands"])

# CREATE
@router.post("/", response_model=schemas.Brand, status_code=status.HTTP_201_CREATED)
async def create_brand(brand: schemas.BrandCreate, db: AsyncSession = Depends(get_db)):
    db_brand = models.Brand(
        name=brand.name,
        slug=brand.slug,
        description=brand.description,
        is_active=brand.is_active
    )
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)
    
    # Add category associations if provided
    if brand.category_ids:
        result = await db.execute(
            select(models.Category).filter(
                models.Category.id.in_(brand.category_ids)
            )
        )
        categories = result.scalars().all()
        db_brand.categories = list(categories)
        await db.commit()
        await db.refresh(db_brand)
    
    return db_brand

# READ
@router.get("/", response_model=List[schemas.Brand])
async def list_brands(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Brand)
    if is_active is not None:
        query = query.filter(models.Brand.is_active == is_active)
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{brand_id}", response_model=schemas.Brand)
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Brand).filter(models.Brand.id == brand_id)
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

# UPDATE
@router.put("/{brand_id}", response_model=schemas.Brand)
async def update_brand(
    brand_id: int,
    brand: schemas.BrandUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Brand).filter(models.Brand.id == brand_id)
    )
    db_brand = result.scalar_one_or_none()
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    update_data = brand.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field != 'category_ids':
            setattr(db_brand, field, value)
    
    if 'category_ids' in update_data:
        result = await db.execute(
            select(models.Category).filter(
                models.Category.id.in_(brand.category_ids or [])
            )
        )
        categories = result.scalars().all()
        db_brand.categories = list(categories)
    
    await db.commit()
    await db.refresh(db_brand)
    return db_brand

# DELETE
@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Brand).filter(models.Brand.id == brand_id)
    )
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Check for associated products
    product_result = await db.execute(
        select(models.Product).filter(
            models.Product.brand_id == brand_id
        )
    )
    if product_result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Cannot delete brand with associated products"
        )
    
    await db.delete(brand)
    await db.commit()
