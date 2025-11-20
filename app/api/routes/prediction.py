# -*- coding: utf-8 -*-
"""
Prediction Routes - Similar a routes/api.php de Laravel
Define las rutas de la API
"""
from fastapi import APIRouter
from app.api.controllers.PredictionController import PredictionController
from app.schemas.PredictionRequest import PredictionRequest

# Crear router
router = APIRouter()

# Instanciar controller (singleton)
prediction_controller = PredictionController()


@router.post("/predict", tags=["Prediction"])
async def predict_price(request: PredictionRequest):
    """
    Predice el precio de un inmueble basado en sus caractersticas

    - **metros**: Metros cuadrados del inmueble
    - **cuartos**: Nmero de habitaciones
    - **banos**: Nmero de baos
    - **lat**: Latitud GPS
    - **lon**: Longitud GPS
    - **parking**: Tiene parking (0=no, 1=si)
    - **piscina**: Tiene piscina (0=no, 1=si)
    """
    return await prediction_controller.predict(request)


@router.get("/status", tags=["Health"])
async def get_status():
    """
    Obtiene el estado del servicio ML y el modelo entrenado
    """
    return await prediction_controller.status()


@router.post("/train", tags=["Admin"])
async def train_model(n_samples: int = 500):
    """
    Entrena o re-entrena el modelo ML

    - **n_samples**: Nmero de muestras sintticas a generar (100-10000)
    """
    return await prediction_controller.train(n_samples)
