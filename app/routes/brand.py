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
