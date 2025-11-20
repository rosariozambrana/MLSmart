# -*- coding: utf-8 -*-
"""
Dataset Service - Genera datos sintticos para entrenamiento
Basado en precios reales de Santa Cruz en ETH
"""
import pandas as pd
import numpy as np
from pathlib import Path
from app.config.settings import settings


class DatasetService:
    """Servicio para generacin y manejo de datasets"""

    # Precios base en ETH por anillo (1 ETH = 18,057.68 BOB)
    # Basado en alquileres reales Santa Cruz (800-5000 BOB/mes)
    PRECIOS_BASE_ETH = {
        0: 0.1385,   # Centro (< 500m): ~2500 BOB (zona comercial)
        1: 0.1108,   # 1er anillo: ~2000 BOB
        2: 0.0886,   # 2do anillo: ~1600 BOB
        3: 0.0775,   # 3er anillo: ~1400 BOB
        4: 0.0664,   # 4to anillo: ~1200 BOB
        5: 0.0554,   # 5to anillo: ~1000 BOB
        6: 0.0499,   # 6to anillo: ~900 BOB
        7: 0.0470,   # 7mo anillo: ~850 BOB
        8: 0.0455,   # 8vo anillo: ~820 BOB
        9: 0.0450,   # 9no anillo: ~812 BOB
        10: 0.0443,  # 10mo anillo: ~800 BOB (más barato)
        101: 0.2215, # Equipetrol: PREMIUM (~4000 BOB)
        102: 0.1660, # Urubo: RESIDENCIAL (~3000 BOB)
        103: 0.1385, # Norte: MEDIO-ALTO (~2500 BOB)
    }

    @staticmethod
    def generar_dataset_sintetico(n_samples: int = 500) -> pd.DataFrame:
        """
        Genera dataset sinttico basado en datos reales de Santa Cruz

        Args:
            n_samples: Nmero de muestras a generar

        Returns:
            DataFrame con datos sintticos
        """
        np.random.seed(settings.RANDOM_STATE)

        data = []

        for _ in range(n_samples):
            # Caractersticas del inmueble
            metros = np.random.randint(30, 250)  # 30m a 250m
            cuartos = np.random.randint(1, 6)    # 1 a 5 habitaciones
            banos = max(1, cuartos - np.random.randint(0, 2))  # Baos proporcionales
            parking = np.random.choice([0, 1], p=[0.4, 0.6])  # 60% tiene parking
            piscina = np.random.choice([0, 1], p=[0.85, 0.15])  # 15% tiene piscina

            # Zona (centro 0, anillos 1-10 y zonas especiales 101-103)
            # Distribucin realista: ms inmuebles en anillos intermedios
            zona_id = np.random.choice(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 101, 102, 103],
                p=[0.02, 0.05, 0.08, 0.12, 0.15, 0.15, 0.15, 0.11, 0.07, 0.05, 0.03, 0.01, 0.005, 0.005]
            )

            # Precio base segn zona
            precio_base = DatasetService.PRECIOS_BASE_ETH[zona_id]

            # Ajustes por caractersticas (escalados a precios reales)
            # Metros cuadrados: +0.0001 ETH por m (~1.8 BOB/m)
            precio_metros = metros * 0.0001

            # Habitaciones: +0.003 ETH por habitacin (~54 BOB)
            precio_cuartos = cuartos * 0.003

            # Baos: +0.002 ETH por bao (~36 BOB)
            precio_banos = banos * 0.002

            # Parking: +0.008 ETH (~144 BOB)
            precio_parking = 0.008 if parking == 1 else 0

            # Piscina: +0.015 ETH (~270 BOB)
            precio_piscina = 0.015 if piscina == 1 else 0

            # Precio total
            precio_total = (
                precio_base +
                precio_metros +
                precio_cuartos +
                precio_banos +
                precio_parking +
                precio_piscina
            )

            # Agregar ruido realista (10%)
            ruido = np.random.uniform(0.90, 1.10)
            precio_final = round(precio_total * ruido, 6)

            # Agregar a dataset
            data.append({
                'metros_cuadrados': metros,
                'num_habitacion': cuartos,
                'num_banos': banos,
                'zona_id': zona_id,
                'parking': parking,
                'piscina': piscina,
                'precio_eth': precio_final
            })

        df = pd.DataFrame(data)

        # Estadsticas
        print(f"[Dataset] Dataset generado: {len(df)} inmuebles")
        print(f"[Precio] Precio ETH - Min: {df['precio_eth'].min():.6f}, Max: {df['precio_eth'].max():.6f}, Media: {df['precio_eth'].mean():.6f}")
        print(f"[Metros] Metros - Min: {df['metros_cuadrados'].min()}, Max: {df['metros_cuadrados'].max()}")
        print(f"[Habitaciones]  Habitaciones - Min: {df['num_habitacion'].min()}, Max: {df['num_habitacion'].max()}")

        return df

    @staticmethod
    def guardar_dataset(df: pd.DataFrame, filename: str = None) -> Path:
        """
        Guarda dataset en CSV

        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo (opcional)

        Returns:
            Path del archivo guardado
        """
        if filename is None:
            filename = settings.DATASET_PATH

        filepath = settings.get_full_path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(filepath, index=False)
        print(f"[OK] Dataset guardado en: {filepath}")

        return filepath

    @staticmethod
    def cargar_dataset(filename: str = None) -> pd.DataFrame:
        """
        Carga dataset desde CSV

        Args:
            filename: Nombre del archivo (opcional)

        Returns:
            DataFrame cargado
        """
        if filename is None:
            filename = settings.DATASET_PATH

        filepath = settings.get_full_path(filename)

        if not filepath.exists():
            raise FileNotFoundError(f"Dataset no encontrado: {filepath}")

        df = pd.DataFrame(pd.read_csv(filepath))
        print(f"[Cargado] Dataset cargado: {len(df)} registros desde {filepath}")

        return df

    @staticmethod
    def generar_y_guardar(n_samples: int = 500) -> Path:
        """
        Genera y guarda dataset en un solo paso

        Args:
            n_samples: Nmero de muestras

        Returns:
            Path del archivo guardado
        """
        df = DatasetService.generar_dataset_sintetico(n_samples)
        filepath = DatasetService.guardar_dataset(df)
        return filepath
