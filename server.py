"""
FastAPI Application - Entry Point
Similar a index.php de Laravel
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.routes import prediction

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Servicio de Machine Learning para predicción de precios de alquiler",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (permitir requests desde Laravel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominio de Laravel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(prediction.router, prefix="", tags=["ML"])


@app.get("/", tags=["Health"])
async def root():
    """
    Health check del servicio
    """
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "ML Prediction Service is running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint de health check
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print(f"{settings.APP_NAME}")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Port: {settings.PORT}")
    print("=" * 60)

    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
