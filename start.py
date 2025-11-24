import uvicorn
import sys

if __name__ == "__main__":
    print("=" * 50)
    print("Hednor E-Commerce API - Starting...")
    print("=" * 50)
    
    # Start FastAPI server with uvicorn
    # Database initialization will happen in app startup event
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="info"
    )
