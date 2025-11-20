# -*- coding: utf-8 -*-
"""
Prediction Controller - Similar a Laravel Controller
Maneja requests de prediccin
"""
from fastapi import HTTPException
from app.services.MLPredictionService import MLPredictionService
from app.schemas.PredictionRequest import PredictionRequest, PredictionResponse


class PredictionController:
    """Controller para endpoints de prediccin"""

    def __init__(self):
        """Inicializa el controller con el servicio ML"""
        self.ml_service = MLPredictionService()

    async def predict(self, request: PredictionRequest) -> dict:
        """
        Endpoint: POST /predict
        Predice el precio de un inmueble

        Args:
            request: Datos del inmueble

        Returns:
            Prediccin de precio
        """
        try:
            # Delegar lgica al Service
            response = self.ml_service.predecir_precio(request)

            return {
                "success": True,
                "data": response.model_dump()
            }

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en prediccin: {str(e)}")

    async def status(self) -> dict:
        """
        Endpoint: GET /status
        Obtiene el estado del servicio ML

        Returns:
            Estado del servicio
        """
        try:
            status_info = self.ml_service.get_model_status()

            return {
                "success": True,
                "data": status_info
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error obteniendo status: {str(e)}")

    async def train(self, n_samples: int = 500) -> dict:
        """
        Endpoint: POST /train
        Entrena o re-entrena el modelo

        Args:
            n_samples: Nmero de muestras a generar

        Returns:
            Resultado del entrenamiento
        """
        try:
            if not (100 <= n_samples <= 10000):
                raise HTTPException(
                    status_code=400,
                    detail="n_samples debe estar entre 100 y 10000"
                )

            result = self.ml_service.entrenar_modelo(n_samples)

            return {
                "success": True,
                "data": result
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error entrenando modelo: {str(e)}")
