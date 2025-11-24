from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from pathlib import Path

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
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)  # Simple parent-child hierarchy
    
    # Self-referential relationships for hierarchy
    parent = relationship("Category", remote_side="Category.id", backref="children")
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
    selling_price = Column(Float, nullable=True)  # Discounted price
    discount = Column(Float, nullable=True)  # Discount percentage
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    image_path = Column(String(500), nullable=True)  # Store file path
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
            return f"/uploads/products/{self.image_path}"
        return None
    
    # Convenience properties
    @property
    def category_name(self):
        return self.category.name if self.category else None
    
    @property
    def brand_name(self):
        return self.brand.name if self.brand else None
