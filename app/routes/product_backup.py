from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional, Any
from datetime import datetime
from pathlib import Path
import os
import uuid

from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])

# Image upload configuration
IMAGE_UPLOAD_DIR = Path("uploads/products")
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Ensure upload directory exists
IMAGE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_uploaded_image(file: UploadFile) -> Optional[str]:
    if not file:
        return None
    
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image too large. Max size: {MAX_IMAGE_SIZE//(1024*1024)}MB"
        )
    
    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = IMAGE_UPLOAD_DIR / filename
    
    # Save file
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    
    return str(filename)

def get_image_url(image_path: Optional[str]) -> Optional[str]:
    if image_path:
        return f"/uploads/products/{image_path}"
    return None

# BULK CREATE - Create multiple products via JSON
@router.post("/bulk", response_model=schemas.BulkProductResponse, status_code=status.HTTP_201_CREATED)
async def create_bulk_products(
    products: List[schemas.ProductBulkCreate],
    db: AsyncSession = Depends(get_db)
):
    """
    Create multiple products at once.
    Returns success/failure status for each product.
    """
    if not products:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product list cannot be empty"
        )
    
    if len(products) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 products per bulk request"
        )
    
    results = []
    created_count = 0
    failed_count = 0
    
    # Collect all unique category and brand IDs for batch validation
    category_ids = set(p.category_id for p in products)
    brand_ids = set(p.brand_id for p in products)
    slug_set = set(p.slug for p in products)
    
    # Validate all categories exist
    category_result = await db.execute(
        select(models.Category).filter(models.Category.id.in_(category_ids))
    )
    valid_categories = {c.id for c in category_result.scalars().all()}
    
    # Validate all brands exist
    brand_result = await db.execute(
        select(models.Brand).filter(models.Brand.id.in_(brand_ids))
    )
    valid_brands = {b.id for b in brand_result.scalars().all()}
    
    # Check for existing slugs
    existing_slugs_result = await db.execute(
        select(models.Product.slug).filter(models.Product.slug.in_(slug_set))
    )
    existing_slugs = {row[0] for row in existing_slugs_result.fetchall()}
    
    # Process each product
    for product_data in products:
        try:
            # Validate category
            if product_data.category_id not in valid_categories:
                results.append(schemas.BulkProductResult(
                    success=False,
                    slug=product_data.slug,
                    error=f"Category {product_data.category_id} not found"
                ))
                failed_count += 1
                continue
            
            # Validate brand
            if product_data.brand_id not in valid_brands:
                results.append(schemas.BulkProductResult(
                    success=False,
                    slug=product_data.slug,
                    error=f"Brand {product_data.brand_id} not found"
                ))
                failed_count += 1
                continue
            
            # Check slug uniqueness
            if product_data.slug in existing_slugs:
                results.append(schemas.BulkProductResult(
                    success=False,
                    slug=product_data.slug,
                    error="Product with this slug already exists"
                ))
                failed_count += 1
                continue
            
            # Create product
            db_product = models.Product(
                name=product_data.name,
                slug=product_data.slug,
                description=product_data.description,
                price=product_data.price,
                selling_price=product_data.selling_price,
                discount=product_data.discount,
                quantity=product_data.quantity,
                category_id=product_data.category_id,
                brand_id=product_data.brand_id,
                is_active=product_data.is_active
            )
            
            db.add(db_product)
            await db.flush()  # Get the ID without committing
            
            results.append(schemas.BulkProductResult(
                success=True,
                product_id=db_product.id,
                slug=product_data.slug
            ))
            created_count += 1
            existing_slugs.add(product_data.slug)  # Add to existing to prevent duplicates in same batch
            
        except Exception as e:
            results.append(schemas.BulkProductResult(
                success=False,
                slug=product_data.slug,
                error=str(e)
            ))
            failed_count += 1
    
    # Commit all successful products
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    
    return schemas.BulkProductResponse(
        total=len(products),
        created=created_count,
        failed=failed_count,
        results=results
    )

# CREATE - Single product via Form
@router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    slug: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    selling_price: Optional[float] = Form(None),
    discount: Optional[float] = Form(None),
    quantity: int = Form(0),
    category_id: int = Form(...),
    brand_id: int = Form(...),
    is_active: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    # Check if slug exists
    result = await db.execute(
        select(models.Product).filter(models.Product.slug == slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this slug already exists"
        )
    
    # Validate category
    category_result = await db.execute(
        select(models.Category).filter(models.Category.id == category_id)
    )
    if not category_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Validate brand
    brand_result = await db.execute(
        select(models.Brand).filter(models.Brand.id == brand_id)
    )
    if not brand_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )
    
    # Handle image upload
    image_path = None
    if image:
        image_path = save_uploaded_image(image)
    
    # Create product
    db_product = models.Product(
        name=name,
        slug=slug,
        description=description,
        price=price,
        selling_price=selling_price,
        discount=discount,
        quantity=quantity,
        category_id=category_id,
        brand_id=brand_id,
        is_active=is_active,
        image_path=image_path
    )
    
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    
    # Eagerly load relationships to avoid greenlet issues
    result = await db.execute(
        select(models.Product)
        .where(models.Product.id == db_product.id)
        .options(selectinload(models.Product.category), selectinload(models.Product.brand))
    )
    product = result.scalar_one_or_none()
    
    return schemas.ProductOut(
        **product.__dict__,
        image_url=get_image_url(product.image_path),
        category=product.category,
        brand=product.brand
    )

# READ - List all products
@router.get("/", response_model=List[schemas.ProductOut])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    category_id: int = None,
    brand_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Product)
    
    if is_active is not None:
        query = query.filter(models.Product.is_active == is_active)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if brand_id:
        query = query.filter(models.Product.brand_id == brand_id)
    
    query = query.options(
        selectinload(models.Product.category),
        selectinload(models.Product.brand)
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    return [
        schemas.ProductOut(
            **product.__dict__,
            image_url=get_image_url(product.image_path),
            category=product.category,
            brand=product.brand
        )
        for product in products
    ]

# READ - Get single product
@router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.id == product_id)
        .options(selectinload(models.Product.category), selectinload(models.Product.brand))
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return schemas.ProductOut(
        **product.__dict__,
        image_url=get_image_url(product.image_path),
        category=product.category,
        brand=product.brand
    )

# UPDATE
@router.put("/{product_id}", response_model=schemas.ProductOut)
async def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    selling_price: Optional[float] = Form(None),
    discount: Optional[float] = Form(None),
    quantity: Optional[int] = Form(None),
    is_active: Optional[bool] = Form(None),
    category_id: Optional[int] = Form(None),
    brand_id: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Product)
        .where(models.Product.id == product_id)
        .options(selectinload(models.Product.category), selectinload(models.Product.brand))
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update fields
    if name is not None:
        product.name = name
    if slug is not None:
        if slug != product.slug:
            slug_check = await db.execute(
                select(models.Product).filter(models.Product.slug == slug)
            )
            if slug_check.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product with this slug already exists"
                )
        product.slug = slug
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if selling_price is not None:
        product.selling_price = selling_price
    if discount is not None:
        product.discount = discount
    if quantity is not None:
        product.quantity = quantity
    if is_active is not None:
        product.is_active = is_active
    if category_id is not None:
        product.category_id = category_id
    if brand_id is not None:
        product.brand_id = brand_id
    
    # Handle image
    if image:
        # Delete old image
        if product.image_path:
            old_path = IMAGE_UPLOAD_DIR / product.image_path
            if old_path.exists():
                os.remove(old_path)
        # Save new image
        product.image_path = save_uploaded_image(image)
    
    product.updated_at = datetime.utcnow()
    await db.commit()
    
    # Re-fetch with eager loading to avoid greenlet issues
    result = await db.execute(
        select(models.Product)
        .where(models.Product.id == product_id)
        .options(selectinload(models.Product.category), selectinload(models.Product.brand))
    )
    updated_product = result.scalar_one_or_none()
    
    return schemas.ProductOut(
        **updated_product.__dict__,
        image_url=get_image_url(updated_product.image_path),
        category=updated_product.category,
        brand=updated_product.brand
    )

# DELETE
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Product).filter(models.Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Delete image file
    if product.image_path:
        image_file = IMAGE_UPLOAD_DIR / product.image_path
        if image_file.exists():
            os.remove(image_file)
    
    await db.delete(product)
    await db.commit()
