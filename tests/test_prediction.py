"""
Tests para el servicio de predicción
"""
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "service" in data


def test_health_check():
    """Test del health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_status_endpoint():
    """Test del endpoint de status"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data


def test_predict_endpoint():
    """Test de predicción"""
    payload = {
        "metros": 80.0,
        "cuartos": 2,
        "banos": 1,
        "lat": -17.783889,
        "lon": -63.182222,
        "parking": 1,
        "piscina": 0
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "data" in data

    prediction = data["data"]
    assert "precio_sugerido" in prediction
    assert "precio_min" in prediction
    assert "precio_max" in prediction
    assert "confianza" in prediction
    assert "anillo" in prediction

    # Validar rangos
    assert prediction["precio_sugerido"] > 0
    assert prediction["precio_min"] <= prediction["precio_sugerido"]
    assert prediction["precio_max"] >= prediction["precio_sugerido"]
    assert 0 <= prediction["confianza"] <= 1
    assert 1 <= prediction["anillo"] <= 10


def test_predict_validation_error():
    """Test de validación de datos incorrectos"""
    payload = {
        "metros": -10,  # Inválido: metros negativos
        "cuartos": 2,
        "banos": 1,
        "lat": -17.783889,
        "lon": -63.182222
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_zona_especial_equipetrol():
    """Test de predicción en zona especial (Equipetrol)"""
    payload = {
        "metros": 100.0,
        "cuartos": 3,
        "banos": 2,
        "lat": -17.765,  # Equipetrol
        "lon": -63.155,
        "parking": 1,
        "piscina": 1
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    prediction = data["data"]

    # Equipetrol debería tener precio más alto
    assert prediction["zona_especial"] == "Equipetrol"
    assert prediction["precio_sugerido"] > 0.002  # Premium price
