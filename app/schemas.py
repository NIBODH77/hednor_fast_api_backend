# # # # schemas.py
# # # from pydantic import BaseModel, Field
# # # from typing import Optional
# # # from uuid import UUID
# # # from datetime import datetime
# # # from pydantic import BaseModel



# # # class CategoryBase(BaseModel):
# # #     name: str
# # #     level: int
# # #     is_leaf: bool = False

# # # class CategoryCreate(CategoryBase):
# # #     pass

# # # class Category(CategoryBase):
# # #     id: int

# # #     class Config:
# # #         orm_mode = True



# # # class ProductBase(BaseModel):
# # #     title: str = Field(..., min_length=2, max_length=100)
# # #     description: Optional[str] = Field(None, max_length=500)
# # #     brand: str = Field(..., min_length=2, max_length=50)
# # #     price: float = Field(..., gt=0)
# # #     discount_price: Optional[float] = Field(None, gt=0)
# # #     stock_quantity: int = Field(0, ge=0)
# # #     category_id: UUID
# # #     is_active: bool = True
# # #     image_url: Optional[str] = None

# # # class ProductCreate(ProductBase):
# # #     pass

# # # class Product(ProductBase):
# # #     product_id: UUID
# # #     created_at: datetime
    
# # #     class Config:
# # #         orm_mode = True


# from datetime import datetime
# from typing import List, Optional
# from pydantic import BaseModel, Field, validator
# from typing import Optional
# from uuid import UUID
# from datetime import datetime
# from pydantic import BaseModel
# from datetime import timezone


# # ----------------------
# # Category Schemas
# # ----------------------

# class CategoryBase(BaseModel):
#     name: str = Field(..., max_length=255)
#     level: int
#     is_leaf: bool = False

# class CategoryCreate(CategoryBase):
#     parent_id: Optional[int] = None

# class CategoryUpdate(BaseModel):
#     name: Optional[str] = Field(None, max_length=255)
#     level: Optional[int]
#     is_leaf: Optional[bool]
#     parent_id: Optional[int]

# class Category(CategoryBase):
#     id: int
#     parent_id: Optional[int]
#     products: List['Product'] = []

#     class Config:
#         orm_mode = True

# # ----------------------
# # Category Relationship Schemas
# # ----------------------

# class CategoryRelationshipBase(BaseModel):
#     ancestor_id: int
#     descendant_id: int
#     depth: int

# class CategoryRelationshipCreate(CategoryRelationshipBase):
#     pass

# class CategoryRelationship(CategoryRelationshipBase):
#     class Config:
#         orm_mode = True

# # ----------------------
# # Product Schemas
# # ----------------------

# class ProductBase(BaseModel):
#     name: str = Field(..., max_length=255)
#     title: str = Field(..., max_length=255)
#     description: Optional[str]
#     brand: Optional[str]
#     price: float
#     discount_price: Optional[float]
#     stock_quantity: int
#     category_id: int
#     rating: float = 0.0
#     reviews: int = 0
#     in_stock: bool = True
#     is_active: bool = True
#     seller: str = "Amazon"
#     specs: Optional[str]  # JSON string
#     image_url: Optional[str] = Field(None, max_length=500)

# class ProductCreate(ProductBase):
#     product_id: Optional[str] = Field(None, max_length=50)

# class ProductUpdate(BaseModel):
#     name: Optional[str] = Field(None, max_length=255)
#     title: Optional[str] = Field(None, max_length=255)
#     description: Optional[str]
#     brand: Optional[str]
#     price: Optional[float]
#     discount_price: Optional[float]
#     stock_quantity: Optional[int]
#     category_id: Optional[int]
#     rating: Optional[float]
#     reviews: Optional[int]
#     in_stock: Optional[bool]
#     is_active: Optional[bool]
#     seller: Optional[str]
#     specs: Optional[str]
#     image_url: Optional[str] = Field(None, max_length=500)

# class Product(ProductBase):
#     id: int
#     product_id: str
#     created_at: datetime
#     category: Optional[Category]

#     class Config:
#          from_attributes = True

# # ----------------------
# # Search & Filter Schemas
# # ----------------------

# class ProductFilters(BaseModel):
#     query: Optional[str]
#     min_price: Optional[float]
#     max_price: Optional[float]
#     in_stock: Optional[bool]
#     category_id: Optional[int]
#     skip: int = 0
#     limit: int = 100

# # ----------------------
# # Response Schemas
# # ----------------------

# class PaginatedResponse(BaseModel):
#     total: int
#     skip: int
#     limit: int
#     items: List[Product]

# # Update forward references
# Category.update_forward_refs()


from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# -------------------------
# Category Schemas
# -------------------------

# class CategoryBase(BaseModel):
#     name: str = Field(..., max_length=255)
#     level: int
#     is_leaf: bool = False

# class CategoryCreate(CategoryBase):
#     parent_id: Optional[int] = None

# class CategoryUpdate(BaseModel):
#     name: Optional[str] = Field(None, max_length=255)
#     level: Optional[int]
#     is_leaf: Optional[bool]
#     parent_id: Optional[int]

# class Category(CategoryBase):
#     id: int
#     parent_id: Optional[int]

#     class Config:
#         from_attributes = True


# class CategoryBase(BaseModel):
#     name: str
#     level: int
#     is_leaf: bool
#     parent_id: Optional[int] = None

# class CategoryCreate(CategoryBase):
#     pass

# class CategoryUpdate(BaseModel):
#     name: Optional[str]
#     level: Optional[int]
#     is_leaf: Optional[bool]
#     parent_id: Optional[int]

# class Category(CategoryBase):
#     id: int

# class Category(CategoryBase):
#     category_id: int  # <- alias for id

#     class Config:
#         orm_mode = True
#         # from_attributes = True
#         fields = {'category_id': 'id'}

# # -------------------------
# # Category Relationship Schemas
# # -------------------------

# class CategoryRelationshipBase(BaseModel):
#     ancestor_id: int
#     descendant_id: int
#     depth: int

# class CategoryRelationshipCreate(CategoryRelationshipBase):
#     pass

# class CategoryRelationship(CategoryRelationshipBase):
#     id: int

#     class Config:
#         from_attributes = True


# # -------------------------
# # Product Schemas
# # -------------------------

# class ProductBase(BaseModel):
#     name: str = Field(..., max_length=255)
#     title: str = Field(..., max_length=255)
#     description: Optional[str] = None
#     brand: Optional[str] = None
#     price: float
#     discount_price: Optional[float] = None
#     stock_quantity: int
#     category_id: int
#     rating: float = 0.0
#     reviews: int = 0
#     in_stock: bool = True
#     is_active: bool = True
#     seller: str = "Amazon"
#     specs: Optional[str] = None  # JSON as string
#     image_url: Optional[str] = Field(None, max_length=500)

# class ProductCreate(ProductBase):
#     product_id: Optional[str] = Field(None, max_length=50)

# class ProductUpdate(BaseModel):
#     name: Optional[str] = Field(None, max_length=255)
#     title: Optional[str] = Field(None, max_length=255)
#     description: Optional[str]
#     brand: Optional[str]
#     price: Optional[float]
#     discount_price: Optional[float]
#     stock_quantity: Optional[int]
#     category_id: Optional[int]
#     rating: Optional[float]
#     reviews: Optional[int]
#     in_stock: Optional[bool]
#     is_active: Optional[bool]
#     seller: Optional[str]
#     specs: Optional[str]
#     image_url: Optional[str]

# class Product(ProductBase):
#     id: int
#     product_id: str

#     class Config:
#         orm_mode = True




from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# ----------------------
# Base Schemas
# ----------------------

class CategoryBase(BaseModel):
    id: Optional[int] = None  # Add this line
    name: str
    level: int
    is_leaf: bool = False
    parent_id: Optional[int] = None

class ProductBrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class ProductBase(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    category_id: int

# ----------------------
# Create Schemas
# ----------------------

class CategoryCreate(CategoryBase):
    pass

class ProductBrandCreate(ProductBrandBase):
    pass

class ProductCreate(ProductBase):
    description: Optional[str] = None
    discount_price: Optional[float] = None
    stock_quantity: int = Field(..., ge=0)
    brand_id: Optional[int] = None
    specs: Optional[str] = None
    image_url: Optional[str] = None

# ----------------------
# Response Schemas
# ----------------------

class ProductBrand(ProductBrandBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryRelationship(BaseModel):
    ancestor_id: int
    descendant_id: int
    depth: int
    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
    children: List["Category"] = []
    brands: List[ProductBrand] = []
    model_config = ConfigDict(from_attributes=True)

class Product(ProductBase):
    id: int
    description: Optional[str] = None
    discount_price: Optional[float] = None
    stock_quantity: int
    brand: Optional[ProductBrand] = None
    rating: float = 0.0
    reviews: int = 0
    in_stock: bool = True
    is_active: bool = True
    seller: str = "Amazon"
    specs: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    category: Category
    model_config = ConfigDict(from_attributes=True)

# ----------------------
# Relationship Schemas
# ----------------------

class BrandCategoryLink(BaseModel):
    brand_id: int
    category_id: int
    model_config = ConfigDict(from_attributes=True)

# ----------------------
# Update Schemas
# ----------------------

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    is_leaf: Optional[bool] = None
    parent_id: Optional[int] = None

class ProductBrandUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    specs: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

# ----------------------
# Special Purpose Schemas
# ----------------------

class CategoryWithProducts(Category):
    products: List[Product] = []

class ProductBrandWithProducts(ProductBrand):
    products: List[Product] = []
    categories: List[Category] = []

class ProductWithRelationships(Product):
    category: Category
    brand: Optional[ProductBrand] = None



from typing import List, Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Category(CategoryBase):
    id: int
    is_leaf: bool
    
    class Config:
        from_attributes = True

class CategoryWithRelationships(Category):
    ancestors: List['Category'] = []
    descendants: List['Category'] = []
    brands: List['Brand'] = []

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
    
    class Config:
        from_attributes = True

class BrandWithCategories(Brand):
    categories: List[Category] = []




class ProductBase(BaseModel):
    name: str
    slug: str
    description: str
    price: float
    quantity: int
    category_id: int
    brand_id: int
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True




class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    
    class Config:
        from_attributes = True

# Update forward references
CategoryWithRelationships.update_forward_refs()
BrandWithCategories.update_forward_refs()



from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True
    parent_id: Optional[int] = None
    is_leaf: Optional[bool] = True



class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    is_leaf: Optional[bool] = True
    parent_id: Optional[int] = None
    parent_slug: Optional[str] = None  # 🔧 Add this line



class CategoryUpdate(BaseModel):
    pass



class Category(CategoryBase):
    id: int
    is_leaf: bool
    
    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes for Pydantic v2

class CategoryWithRelationships(Category):
    ancestors: List['Category'] = []
    descendants: List['Category'] = []
    brands: List['Brand'] = []

class CategoryWithChildren(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    parent_id: Optional[int] = None
    has_children: bool = False
    
    class Config:
        from_attributes = True

class CategorySearchResult(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool
    parent_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class CategoryPath(BaseModel):
    id: int
    name: str
    slug: str
    level: int = 0
    
    class Config:
        from_attributes = True

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
    
    class Config:
        from_attributes = True

class BrandWithCategories(Brand):
    categories: List[Category] = []

class ProductBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None  # Changed from required to optional
    price: float
    quantity: int
    category_id: int
    brand_id: int
    is_active: bool = True

class ProductCreate(ProductBase):
    selling_price: Optional[float] = None
    discount: Optional[float] = None

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

class ProductOut(ProductBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    category: Optional[Category] = None  # Added
    brand: Optional[Brand] = None       # Added

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    

class Product(ProductBase):
    id: int
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    image_path: Optional[str] = None  # Added for image handling
    image_url: Optional[str]  # ✅ ADD THIS
    created_at: datetime
    updated_at: datetime


    # class Config:
    #     orm_mode = True

    class Config:
        from_attributes = True

# Update forward references after all classes are defined
CategoryWithRelationships.update_forward_refs()
BrandWithCategories.update_forward_refs()





