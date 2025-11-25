from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


# =====================================================================
# CATEGORY SCHEMAS
# =====================================================================

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True
    parent_id: Optional[int] = None
    is_leaf: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None
    is_leaf: Optional[bool] = None


class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryWithChildren(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    parent_id: Optional[int] = None
    has_children: bool = False
    model_config = ConfigDict(from_attributes=True)


class CategorySearchResult(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool
    parent_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class CategoryPath(BaseModel):
    id: int
    name: str
    slug: str
    level: int = 0
    model_config = ConfigDict(from_attributes=True)


class CategoryWithRelationships(Category):
    ancestors: List[Category] = []
    descendants: List[Category] = []
    brands: List['Brand'] = []


# =====================================================================
# BRAND SCHEMAS
# =====================================================================

class BrandBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True


class BrandCreate(BrandBase):
    category_ids: List[int] = []


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    category_ids: Optional[List[int]] = None


class Brand(BrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class BrandWithCategories(Brand):
    categories: List[Category] = []


# =====================================================================
# PRODUCT SCHEMAS
# =====================================================================

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    selling_price: Optional[float] = None
    discount: Optional[float] = None
    quantity: int
    category_id: int
    brand_id: int
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductBulkCreate(BaseModel):
    """Schema for bulk product creation via JSON"""
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    selling_price: Optional[float] = None
    discount: Optional[float] = None
    quantity: int = 0
    category_id: int
    brand_id: int
    is_active: bool = True


class BulkProductResult(BaseModel):
    """Result for each product in bulk operation"""
    success: bool
    product_id: Optional[int] = None
    slug: str
    error: Optional[str] = None


class BulkProductResponse(BaseModel):
    """Response for bulk product creation"""
    total: int
    created: int
    failed: int
    results: List[BulkProductResult]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    selling_price: Optional[float] = None
    discount: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None


class ProductOut(ProductBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    model_config = ConfigDict(from_attributes=True)


class Product(ProductBase):
    id: int
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    model_config = ConfigDict(from_attributes=True)


# Update forward references
CategoryWithRelationships.model_rebuild()
BrandWithCategories.model_rebuild()


# Category Search Result Schema
class CategorySearchResult(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int
    path: Optional[str] = None
    
    class Config:
        from_attributes = True
