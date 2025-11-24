from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, and_
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/categories", tags=["categories"])

# Helper function
async def verify_category_exists(category_id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Category).filter(
            models.Category.id == category_id,
            models.Category.is_active == True
        )
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found or inactive"
        )
    return category

@router.get("/top-level", response_model=List[schemas.CategoryWithChildren])
async def get_top_level_categories(db: AsyncSession = Depends(get_db)):
    try:
        # Get all top-level categories (where parent_id is NULL)
        result = await db.execute(
            select(models.Category).filter(
                models.Category.parent_id == None,
                models.Category.is_active == True
            ).order_by(models.Category.name)
        )
        categories = result.scalars().all()
        
        if not categories:
            return []
        
        # Check which categories have children
        category_ids = [c.id for c in categories]
        parents_result = await db.execute(
            text("SELECT DISTINCT parent_id FROM categories WHERE parent_id = ANY(:ids) AND is_active = TRUE"),
            {'ids': category_ids}
        )
        parents_with_children_set = {row[0] for row in parents_result.fetchall()}
        
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
async def get_category_children(
    category_id: int, 
    db: AsyncSession = Depends(get_db)
):
    try:
        # Verify parent exists
        await verify_category_exists(category_id, db)
        
        # Get children
        result = await db.execute(
            select(models.Category).filter(
                models.Category.parent_id == category_id,
                models.Category.is_active == True
            ).order_by(models.Category.name)
        )
        children = result.scalars().all()
        
        if not children:
            return []
        
        # Check which children have their own children
        child_ids = [c.id for c in children]
        if child_ids:
            parents_result = await db.execute(
                text("SELECT DISTINCT parent_id FROM categories WHERE parent_id = ANY(:ids) AND is_active = TRUE"),
                {'ids': child_ids}
            )
            parents_with_children_set = {row[0] for row in parents_result.fetchall()}
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
async def get_category_hierarchy(
    category_id: int,
    max_level: int = Query(9, ge=1, le=9),
    db: AsyncSession = Depends(get_db)
):
    try:
        await verify_category_exists(category_id, db)
        
        query = text("""
            WITH RECURSIVE category_hierarchy AS (
                SELECT 
                    id,
                    name,
                    slug,
                    1 AS level
                FROM categories
                WHERE id = :category_id AND is_active = TRUE
                
                UNION ALL
                
                SELECT
                    c.id,
                    c.name,
                    c.slug,
                    h.level + 1
                FROM categories c
                JOIN category_hierarchy h ON c.parent_id = h.id
                WHERE c.is_active = TRUE
                AND h.level < :max_level
            )
            SELECT 
                id,
                name,
                slug,
                level
            FROM category_hierarchy
            ORDER BY level, name
        """)
        
        result = await db.execute(query, {'category_id': category_id, 'max_level': max_level})
        rows = result.fetchall()
        
        return [
            schemas.CategoryPath(id=row[0], name=row[1], slug=row[2], level=row[3])
            for row in rows
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching hierarchy: {str(e)}"
        )

@router.get("/search", response_model=List[schemas.CategorySearchResult])
async def search_categories(
    query: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    try:
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(models.Category).filter(
                and_(
                    models.Category.is_active == True,
                    models.Category.name.ilike(search_pattern)
                )
            ).order_by(models.Category.name).limit(20)
        )
        categories = result.scalars().all()
        
        return [
            schemas.CategorySearchResult(
                id=cat.id,
                name=cat.name,
                slug=cat.slug,
                description=cat.description,
                is_active=cat.is_active,
                parent_id=cat.parent_id
            )
            for cat in categories
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching categories: {str(e)}"
        )
