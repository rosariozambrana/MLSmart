# -*- coding: utf-8 -*-
"""
Main entry point for ML Service
"""
import uvicorn
from server import app
from app.config.settings import settings

if __name__ == "__main__":
    print("=" * 60)
    print(f"{settings.APP_NAME}")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Port: {settings.PORT}")
    print("Server: http://localhost:{settings.PORT}")
    print("Docs: http://localhost:{settings.PORT}/docs")
    print("=" * 60)

    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=False  # Desactivar reload para evitar conflictos
    )
