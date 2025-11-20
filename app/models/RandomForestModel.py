# -*- coding: utf-8 -*-
"""
Random Forest Model - Modelo de Machine Learning
Entrenamiento y prediccin de precios
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from app.config.settings import settings
from app.services.DatasetService import DatasetService


class RandomForestModel:
    """Modelo Random Forest para prediccin de precios"""

    def __init__(self):
        """Inicializa el modelo"""
        self.model = None
        self.feature_names = [
            'metros_cuadrados',
            'num_habitacion',
            'num_banos',
            'zona_id',
            'parking',
            'piscina'
        ]
        self.is_trained = False
        self.metrics = {}

    def entrenar(self, df: pd.DataFrame = None) -> dict:
        """
        Entrena el modelo Random Forest

        Args:
            df: DataFrame con datos de entrenamiento (opcional)

        Returns:
            Diccionario con mtricas de entrenamiento
        """
        # Si no se proporciona dataset, generar uno sinttico
        if df is None:
            print("[Dataset] Generando dataset sinttico...")
            df = DatasetService.generar_dataset_sintetico(n_samples=500)

        # Preparar features (X) y target (y)
        X = df[self.feature_names]
        y = df['precio_eth']

        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=settings.TEST_SIZE,
            random_state=settings.RANDOM_STATE
        )

        print(f"[Info] Entrenando Random Forest...")
        print(f"   - Samples entrenamiento: {len(X_train)}")
        print(f"   - Samples prueba: {len(X_test)}")
        print(f"   - Features: {self.feature_names}")

        # Crear y entrenar modelo
        self.model = RandomForestRegressor(
            n_estimators=settings.N_ESTIMATORS,
            max_depth=settings.MAX_DEPTH,
            min_samples_split=settings.MIN_SAMPLES_SPLIT,
            random_state=settings.RANDOM_STATE,
            n_jobs=-1  # Usar todos los cores
        )

        self.model.fit(X_train, y_train)

        # Evaluar modelo
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)

        # Mtricas
        self.metrics = {
            'train': {
                'r2': r2_score(y_train, y_pred_train),
                'rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                'mae': mean_absolute_error(y_train, y_pred_train)
            },
            'test': {
                'r2': r2_score(y_test, y_pred_test),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                'mae': mean_absolute_error(y_test, y_pred_test)
            },
            'feature_importance': dict(zip(
                self.feature_names,
                self.model.feature_importances_.tolist()
            ))
        }

        self.is_trained = True

        # Mostrar resultados
        print(f"\n[OK] Entrenamiento completado!")
        print(f"[Metricas] Mtricas Test Set:")
        print(f"   - R Score: {self.metrics['test']['r2']:.4f}")
        print(f"   - RMSE: {self.metrics['test']['rmse']:.6f} ETH")
        print(f"   - MAE: {self.metrics['test']['mae']:.6f} ETH")
        print(f"\n[Feature] Feature Importance:")
        for feature, importance in self.metrics['feature_importance'].items():
            print(f"   - {feature}: {importance:.4f}")

        return self.metrics

    def predecir(self, features: dict) -> dict:
        """
        Realiza prediccin de precio

        Args:
            features: Diccionario con caractersticas del inmueble

        Returns:
            Diccionario con prediccin
        """
        if not self.is_trained or self.model is None:
            raise ValueError("El modelo no ha sido entrenado. Llama a entrenar() primero.")

        # Preparar features en el orden correcto
        X = pd.DataFrame([{
            'metros_cuadrados': features['metros'],
            'num_habitacion': features['cuartos'],
            'num_banos': features['banos'],
            'zona_id': features['zona_id'],
            'parking': features['parking'],
            'piscina': features['piscina']
        }])

        # Prediccin
        precio_sugerido = self.model.predict(X)[0]

        # Intervalo de confianza (basado en desviacin de rboles individuales)
        predicciones_arboles = np.array([tree.predict(X)[0] for tree in self.model.estimators_])
        std = np.std(predicciones_arboles)

        precio_min = max(0.0001, precio_sugerido - (1.5 * std))  # Mnimo 0.0001 ETH
        precio_max = precio_sugerido + (1.5 * std)

        # Confianza basada en R score
        confianza = self.metrics.get('test', {}).get('r2', 0.85)

        resultado = {
            'precio_sugerido': round(precio_sugerido, 6),
            'precio_min': round(precio_min, 6),
            'precio_max': round(precio_max, 6),
            'confianza': round(confianza, 2)
        }

        return resultado

    def guardar(self, filepath: str = None) -> Path:
        """
        Guarda el modelo entrenado

        Args:
            filepath: Ruta donde guardar (opcional)

        Returns:
            Path del archivo guardado
        """
        if not self.is_trained:
            raise ValueError("No hay modelo entrenado para guardar")

        if filepath is None:
            filepath = settings.MODEL_PATH

        full_path = settings.get_full_path(filepath)
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Guardar modelo y metadatos
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'version': settings.APP_VERSION
        }

        joblib.dump(model_data, full_path)
        print(f"[Guardado] Modelo guardado en: {full_path}")

        return full_path

    def cargar(self, filepath: str = None) -> bool:
        """
        Carga un modelo entrenado

        Args:
            filepath: Ruta del modelo (opcional)

        Returns:
            True si se carg exitosamente
        """
        if filepath is None:
            filepath = settings.MODEL_PATH

        full_path = settings.get_full_path(filepath)

        if not full_path.exists():
            print(f"[Advertencia] Modelo no encontrado en: {full_path}")
            return False

        # Cargar modelo y metadatos
        model_data = joblib.load(full_path)

        self.model = model_data['model']
        self.feature_names = model_data['feature_names']
        self.metrics = model_data.get('metrics', {})
        self.is_trained = True

        print(f"[OK] Modelo cargado desde: {full_path}")
        print(f"[Dataset] R Score: {self.metrics.get('test', {}).get('r2', 'N/A')}")

        return True

    def get_info(self) -> dict:
        """
        Obtiene informacin del modelo

        Returns:
            Diccionario con informacin del modelo
        """
        if not self.is_trained:
            return {
                'status': 'not_trained',
                'message': 'Modelo no entrenado'
            }

        return {
            'status': 'trained',
            'features': self.feature_names,
            'metrics': self.metrics,
            'n_estimators': self.model.n_estimators if self.model else 0,
            'max_depth': self.model.max_depth if self.model else 0
        }
