import uvicorn
import asyncio
from app.database import init_db

async def startup():
    """Initialize database on startup"""
    print("=" * 50)
    print("Hednor E-Commerce API - Starting...")
    print("=" * 50)
    await init_db()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    # Run initialization
    asyncio.run(startup())
    
    # Start FastAPI server
    print("\nStarting FastAPI server on 0.0.0.0:5000...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
