# 🤖 ML Prediction Service

Servicio de Machine Learning para predicción de precios de alquiler usando Random Forest.

## 📋 Requisitos

- Python 3.11+
- pip

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
# Ejecutar servidor de desarrollo
python app.py

# O con uvicorn directamente
uvicorn app:app --reload --host 0.0.0.0 --port 5000
```

## 📡 Endpoints

### `GET /`
Health check del servicio

### `POST /predict`
Predice el precio de un inmueble

**Body:**
```json
{
  "metros": 80,
  "cuartos": 2,
  "banos": 1,
  "lat": -17.783889,
  "lon": -63.182222,
  "parking": 1,
  "piscina": 0
}
```

**Response:**
```json
{
  "precio_sugerido": 0.0015,
  "precio_min": 0.0012,
  "precio_max": 0.0018,
  "confianza": 0.92
}
```

### `GET /status`
Estado del modelo ML

## 🏗️ Arquitectura

```
ml_service/
├── app/
│   ├── api/              # Endpoints
│   ├── services/         # Lógica de negocio
│   ├── models/           # Modelos ML
│   └── config/           # Configuración
├── storage/              # Datos y modelos
└── tests/                # Tests
```

## 🔧 Tecnologías

- **FastAPI** - Framework web
- **scikit-learn** - Machine Learning
- **pandas** - Procesamiento de datos
- **geopy** - Cálculos geográficos

php artisan reverb:start --host=192.168.100.9 --port=8080
php artisan serve --host=192.168.100.9 --port=8000
py main.py
