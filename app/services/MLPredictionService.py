# -*- coding: utf-8 -*-
"""
ML Prediction Service - Similar a Laravel Service
Orquesta geolocalizacin y prediccin ML
"""
from app.models.RandomForestModel import RandomForestModel
from app.services.GeolocationService import GeolocationService
from app.schemas.PredictionRequest import PredictionRequest, PredictionResponse


class MLPredictionService:
    """Servicio principal de prediccin ML"""

    def __init__(self):
        """Inicializa el servicio con modelo cargado"""
        self.model = RandomForestModel()
        self.geo_service = GeolocationService()

        # Intentar cargar modelo existente
        if not self.model.cargar():
            print("[Advertencia] Modelo no encontrado. Se entrenar automticamente en la primera prediccin.")

    def predecir_precio(self, request: PredictionRequest) -> PredictionResponse:
        """
        Predice el precio de un inmueble

        Args:
            request: Request con datos del inmueble

        Returns:
            Response con prediccin
        """
        # 1. Anlisis de geolocalizacin
        ubicacion = self.geo_service.analizar_ubicacion(request.lat, request.lon)

        # 2. Preparar features para el modelo
        features = {
            'metros': request.metros,
            'cuartos': request.cuartos,
            'banos': request.banos,
            'zona_id': ubicacion['zona_id'],
            'parking': request.parking,
            'piscina': request.piscina
        }

        # 3. Entrenar modelo si no est entrenado
        if not self.model.is_trained:
            print("[Info] Modelo no entrenado. Entrenando automticamente...")
            self.model.entrenar()
            self.model.guardar()

        # 4. Predecir precio
        prediccion = self.model.predecir(features)

        # 5. Aplicar multiplicador de zona especial si aplica
        if ubicacion['multiplicador_precio'] != 1.0:
            mult = ubicacion['multiplicador_precio']
            prediccion['precio_sugerido'] *= mult
            prediccion['precio_min'] *= mult
            prediccion['precio_max'] *= mult
            prediccion['precio_sugerido'] = round(prediccion['precio_sugerido'], 6)
            prediccion['precio_min'] = round(prediccion['precio_min'], 6)
            prediccion['precio_max'] = round(prediccion['precio_max'], 6)

        # 6. Construir response
        response = PredictionResponse(
            precio_sugerido=prediccion['precio_sugerido'],
            precio_min=prediccion['precio_min'],
            precio_max=prediccion['precio_max'],
            confianza=prediccion['confianza'],
            anillo=ubicacion['anillo'],
            zona_especial=ubicacion['zona_especial']
        )

        return response

    def get_model_status(self) -> dict:
        """
        Obtiene el estado del modelo ML

        Returns:
            Diccionario con informacin del modelo
        """
        model_info = self.model.get_info()

        return {
            'service': 'ML Prediction Service',
            'status': 'operational' if self.model.is_trained else 'requires_training',
            'model': model_info,
            'geolocation': {
                'centro_scz': {
                    'lat': self.geo_service.CENTRO_SCZ[0],
                    'lon': self.geo_service.CENTRO_SCZ[1]
                },
                'anillos_por_sector': {sector: len(radios) for sector, radios in self.geo_service.ANILLOS_RADIOS_POR_SECTOR.items()},
                'zonas_especiales': list(self.geo_service.ZONAS_ESPECIALES.keys())
            }
        }

    def entrenar_modelo(self, n_samples: int = 500) -> dict:
        """
        Entrena (o re-entrena) el modelo

        Args:
            n_samples: Nmero de muestras sintticas a generar

        Returns:
            Mtricas de entrenamiento
        """
        from app.services.DatasetService import DatasetService

        # Generar dataset
        df = DatasetService.generar_dataset_sintetico(n_samples)

        # Entrenar
        metrics = self.model.entrenar(df)

        # Guardar
        self.model.guardar()

        # Guardar dataset tambin
        DatasetService.guardar_dataset(df)

        return {
            'status': 'success',
            'samples_trained': n_samples,
            'metrics': metrics
        }
