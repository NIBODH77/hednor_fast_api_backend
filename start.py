import asyncio
import os
import sys
from sqlalchemy import select
from app.database import Base, AsyncSessionLocal, engine
from app.models import User
from app.crud import hash_password
import uvicorn


async def init_database():
    """Initialize database and create tables"""
    print("Initializing database...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created successfully!")
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.username == "admin"))
        admin_user = result.scalars().first()
        
        if not admin_user:
            print("Creating default admin user...")
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin"
            )
            db.add(admin)
            await db.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
        else:
            print("✅ Admin user already exists")


if __name__ == "__main__":
    print("=" * 50)
    print("ODH Receptionist Panel - Starting...")
    print("=" * 50)
    
    asyncio.run(init_database())
    
    print("\nStarting FastAPI server on 0.0.0.0:5000...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
