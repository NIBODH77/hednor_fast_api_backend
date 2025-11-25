
# # # # schema_models.py
# # # from app.database import Base

# # # from sqlalchemy import Column, String, Integer, Text, Boolean, Date, DateTime, DECIMAL, ForeignKey
# # # from sqlalchemy.dialects.postgresql import UUID
# # # from sqlalchemy.orm import relationship
# # # from sqlalchemy.ext.declarative import declarative_base
# # # import uuid

# # # # Base = declarative_base()

# # # def default_uuid():
# # #     return str(uuid.uuid4())

# # # class User(Base):
# # #     __tablename__ = "users"
# # #     user_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     name = Column(String(100))
# # #     email = Column(String(100), unique=True, nullable=False)
# # #     phone = Column(String(15))
# # #     password_hash = Column(Text, nullable=False)
# # #     user_type = Column(String(20), default='customer')
# # #     created_at = Column(DateTime)
# # #     updated_at = Column(DateTime)

# # # class Address(Base):
# # #     __tablename__ = "addresses"
# # #     address_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
# # #     full_name = Column(String(100))
# # #     phone = Column(String(15))
# # #     address_line1 = Column(Text)
# # #     address_line2 = Column(Text)
# # #     city = Column(String(100))
# # #     state = Column(String(100))
# # #     postal_code = Column(String(20))
# # #     country = Column(String(50))
# # #     is_default = Column(Boolean, default=False)

# # # class Category(Base):
# # #     __tablename__ = "categories"
# # #     category_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     name = Column(String(100), nullable=False)
# # #     parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"))
# # #     description = Column(Text)



# # # class Product(Base):
# # #     __tablename__ = "products"
# # #     product_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     title = Column(String(200))
# # #     description = Column(Text)
# # #     brand = Column(String(100))
# # #     price = Column(DECIMAL(10, 2))
# # #     discount_price = Column(DECIMAL(10, 2))
# # #     stock_quantity = Column(Integer)
# # #     category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"))
# # #     is_active = Column(Boolean, default=True)
# # #     created_at = Column(DateTime)

# # #     # ✅ Add relationships
# # #     images = relationship("ProductImage", backref="product", cascade="all, delete-orphan")
# # #     variants = relationship("ProductVariant", backref="product", cascade="all, delete-orphan")

# # # class ProductImage(Base):
# # #     __tablename__ = "productimages"
# # #     image_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
# # #     image_url = Column(Text)
# # #     is_primary = Column(Boolean, default=False)

# # # class ProductVariant(Base):
# # #     __tablename__ = "productvariants"
# # #     variant_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
# # #     variant_type = Column(String(50))
# # #     variant_value = Column(String(50))
# # #     price_modifier = Column(DECIMAL(10,2))
# # #     stock_quantity = Column(Integer)

# # # class Order(Base):
# # #     __tablename__ = "orders"
# # #     order_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
# # #     address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.address_id"))
# # #     status = Column(String(20))
# # #     total_amount = Column(DECIMAL(10,2))
# # #     shipping_cost = Column(DECIMAL(10,2))
# # #     placed_at = Column(DateTime)
# # #     payment_status = Column(String(20))

# # # class OrderItem(Base):
# # #     __tablename__ = "orderitems"
# # #     order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id"))
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
# # #     variant_id = Column(UUID(as_uuid=True), ForeignKey("productvariants.variant_id"))
# # #     quantity = Column(Integer)
# # #     price = Column(DECIMAL(10,2))

# # # class Payment(Base):
# # #     __tablename__ = "payments"
# # #     payment_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id")) 
# # #     payment_method = Column(String(50))
# # #     amount = Column(DECIMAL(10,2))
# # #     payment_date = Column(DateTime)
# # #     status = Column(String(20))
# # #     transaction_id = Column(Text)

# # # class Shipment(Base):
# # #     __tablename__ = "shipments"
# # #     shipment_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id"))
# # #     courier_service = Column(String(100))
# # #     tracking_number = Column(String(100))
# # #     shipped_at = Column(DateTime)
# # #     delivered_at = Column(DateTime)
# # #     status = Column(String(20))

# # # class Review(Base):
# # #     __tablename__ = "reviews"
# # #     review_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
# # #     rating = Column(Integer)
# # #     comment = Column(Text)
# # #     created_at = Column(DateTime)

# # # class Cart(Base):
# # #     __tablename__ = "carts"
# # #     cart_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
# # #     created_at = Column(DateTime)

# # # class CartItem(Base):
# # #     __tablename__ = "cartitems"
# # #     cart_item_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.cart_id"))
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
# # #     variant_id = Column(UUID(as_uuid=True), ForeignKey("productvariants.variant_id"))
# # #     quantity = Column(Integer)

# # # class Wishlist(Base):
# # #     __tablename__ = "wishlists"
# # #     wishlist_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

# # # class WishlistItem(Base):
# # #     __tablename__ = "wishlistitems"
# # #     id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     wishlist_id = Column(UUID(as_uuid=True), ForeignKey("wishlists.wishlist_id"))
# # #     product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))

# # # class Coupon(Base):
# # #     __tablename__ = "coupons"
# # #     coupon_code = Column(String(50), primary_key=True)
# # #     discount_percent = Column(Integer)
# # #     valid_from = Column(Date)
# # #     valid_to = Column(Date)
# # #     usage_limit = Column(Integer)
# # #     used_count = Column(Integer, default=0)

# # # class ActivityLog(Base):
# # #     __tablename__ = "activitylogs"
# # #     log_id = Column(UUID(as_uuid=True), primary_key=True, default=default_uuid)
# # #     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
# # #     activity = Column(Text)
# # #     created_at = Column(DateTime)

# # from pydantic import BaseModel, Field
# # from typing import Optional, List
# # from datetime import datetime
# # from app.database import Base




# # class CategoryBase(BaseModel):
# #     name: str
# #     level: int
# #     is_leaf: Optional[bool] = False
# #     parent_id: Optional[int] = None


# # class CategoryCreate(CategoryBase):
# #     pass


# # class Category(CategoryBase):
# #     id: int

# #     class Config:
# #         from_attributes = True


# # class CategoryRelationshipBase(BaseModel):
# #     ancestor_id: int
# #     descendant_id: int
# #     depth: int


# # class CategoryRelationshipCreate(CategoryRelationshipBase):
# #     pass


# # class CategoryRelationship(CategoryRelationshipBase):
# #     class Config:
# #         from_attributes = True


# # class ProductBase(BaseModel):
# #     product_id: str = Field(..., description="Unique product identifier")
# #     name: str
# #     title: str
# #     description: Optional[str] = None
# #     brand: Optional[str] = None
# #     price: float
# #     discount_price: Optional[float] = None
# #     stock_quantity: Optional[int] = None
# #     category_id: int
# #     rating: Optional[float] = 0.0
# #     reviews: Optional[int] = 0
# #     in_stock: Optional[bool] = True
# #     is_active: Optional[bool] = True
# #     seller: Optional[str] = "Amazon"
# #     specs: Optional[str] = None  # Assuming JSON string
# #     image_url: Optional[str] = None


# # class ProductCreate(ProductBase):
# #     pass


# # class Product(Base):
# #     id: int
# #     created_at: Optional[datetime]

# #     class Config:
# #         from_attributes = True








# # from sqlalchemy import  Text
# # from sqlalchemy.orm import relationship, declarative_base
# # from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime
# # from sqlalchemy.orm import relationship
# # from uuid import uuid4  
# # from datetime import datetime

# # from app.database import Base

# # Base = declarative_base()

# # class Category(Base):
# #     __tablename__ = "categories"

# #     id = Column(Integer, primary_key=True, index=True)
# #     name = Column(String(255), nullable=False)
# #     level = Column(Integer, nullable=False)
# #     is_leaf = Column(Boolean, default=False)
# #     parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

# #     parent = relationship("Category", remote_side=[id])
# #     products = relationship("Product", back_populates="category")

# #     # Relationship with brands
# #     brands = relationship(
# #         "ProductBrand",
# #         secondary="brand_categories",
# #         back_populates="categories"
# #     )



# # class CategoryRelationship(Base):
# #     __tablename__ = "category_relationships"

# #     id = Column(Integer, primary_key=True, index=True)
# #     ancestor_id = Column(Integer, ForeignKey("categories.id"))
# #     descendant_id = Column(Integer, ForeignKey("categories.id"))
# #     depth = Column(Integer, nullable=False)

# # class Product(Base):
# #     __tablename__ = "products"

# #     id = Column(Integer, primary_key=True, index=True)
# #     product_id = Column(String(50), unique=True, index=True)
# #     name = Column(String(255), nullable=False)
# #     title = Column(String(255), nullable=False)
# #     description = Column(Text, nullable=True)
# #     brand = Column(String(255), nullable=True)
# #     price = Column(Float, nullable=False)
# #     discount_price = Column(Float, nullable=True)
# #     stock_quantity = Column(Integer, nullable=False)
# #     category_id = Column(Integer, ForeignKey("categories.id"))
# #     rating = Column(Float, default=0.0)
# #     reviews = Column(Integer, default=0)
# #     in_stock = Column(Boolean, default=True)
# #     is_active = Column(Boolean, default=True)
# #     seller = Column(String(255), default="Amazon")
# #     specs = Column(Text, nullable=True)
# #     image_url = Column(String(500), nullable=True)
# #     created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Required
# #     category = relationship("Category", back_populates="products")


from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, func
from datetime import datetime
import os
from pathlib import Path
import uuid

from app.database import Base  # Import Base from database.py instead of creating new one

# Association table for many-to-many relationship between Category and Brand
category_brand_association = Table(
    'category_brand_association',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('brand_id', Integer, ForeignKey('brands.id'))
)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_leaf = Column(Boolean, default=False)  # Indicates if category has no children
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)  # Simple hierarchy
    
    # Self-referential relationships for hierarchy
    parent_relationships = relationship(
        "CategoryRelationship",
        foreign_keys="[CategoryRelationship.descendant_id]",
        back_populates="descendant"
    )
    child_relationships = relationship(
        "CategoryRelationship",
        foreign_keys="[CategoryRelationship.ancestor_id]",
        back_populates="ancestor"
    )
    
    # Direct parent-child relationship
    children = relationship("Category", backref="parent", remote_side=[id])
    
    # Many-to-many with Brand
    brands = relationship(
        "Brand",
        secondary=category_brand_association,
        back_populates="categories"
    )
    
    # Products in this category
    products = relationship("Product", back_populates="category")

class CategoryRelationship(Base):
    __tablename__ = 'category_relationships'
    
    ancestor_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    descendant_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    depth = Column(Integer, nullable=False)
    
    ancestor = relationship(
        "Category",
        foreign_keys=[ancestor_id],
        back_populates="child_relationships"
    )
    descendant = relationship(
        "Category",
        foreign_keys=[descendant_id],
        back_populates="parent_relationships"
    )

class Brand(Base):
    __tablename__ = 'brands'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Many-to-many with Category
    categories = relationship(
        "Category",
        secondary=category_brand_association,
        back_populates="brands"
    )
    
    # Products for this brand
    products = relationship("Product", back_populates="brand")


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image_path = Column(String(500), nullable=True)  # Store file path instead of URL
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    
    # Relationships
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")
    
    brand_id = Column(Integer, ForeignKey('brands.id'))
    brand = relationship("Brand", back_populates="products")
    
    @property
    def image_url(self):
        if self.image_path:
            
            # return f"/uploads/products/{Path(self.image_path).name}"
            return f"/uploads/products/{self.image_path}"

        return None
    
    # Convenience properties
    @property
    def category_name(self):
        return self.category.name if self.category else None
    
    @property
    def brand_name(self):
        return self.brand.name if self.brand else None





