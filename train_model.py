# -*- coding: utf-8 -*-
"""
Script para entrenar el modelo ML
Ejecutar antes de iniciar el servicio por primera vez
"""
import sys
import io
from app.services.DatasetService import DatasetService
from app.models.RandomForestModel import RandomForestModel

# Fix encoding para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Entrena y guarda el modelo"""
    print("=" * 60)
    print("ENTRENAMIENTO DEL MODELO ML")
    print("=" * 60)

    # 1. Generar dataset sintético
    print("\nPaso 1: Generando dataset sintetico...")
    df = DatasetService.generar_dataset_sintetico(n_samples=5000)

    # 2. Guardar dataset
    print("\nPaso 2: Guardando dataset...")
    DatasetService.guardar_dataset(df)

    # 3. Entrenar modelo
    print("\nPaso 3: Entrenando modelo Random Forest...")
    model = RandomForestModel()
    metrics = model.entrenar(df)

    # 4. Guardar modelo
    print("\nPaso 4: Guardando modelo entrenado...")
    model.guardar()

    # 5. Resumen
    print("\n" + "=" * 60)
    print("ENTRENAMIENTO COMPLETADO")
    print("=" * 60)
    print(f"R2 Score (Test): {metrics['test']['r2']:.4f}")
    print(f"RMSE (Test): {metrics['test']['rmse']:.6f} ETH")
    print(f"MAE (Test): {metrics['test']['mae']:.6f} ETH")
    print("\nEl servicio esta listo para usarse!")
    print("   Ejecuta: python app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
