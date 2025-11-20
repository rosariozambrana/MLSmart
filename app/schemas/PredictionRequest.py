# -*- coding: utf-8 -*-
"""
Pydantic Schemas - Similar a Laravel Requests
Validacin de datos de entrada
"""
from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Schema para request de prediccin"""

    metros: float = Field(
        ...,
        gt=0,
        le=1000,
        description="Metros cuadrados del inmueble",
        example=80.0
    )
    cuartos: int = Field(
        ...,
        ge=1,
        le=20,
        description="Nmero de habitaciones",
        example=2
    )
    banos: int = Field(
        ...,
        ge=1,
        le=10,
        description="Nmero de baos",
        example=1
    )
    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitud GPS",
        example=-17.783889
    )
    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitud GPS",
        example=-63.182222
    )
    parking: int = Field(
        default=0,
        ge=0,
        le=1,
        description="Tiene parking (0=no, 1=si)",
        example=1
    )
    piscina: int = Field(
        default=0,
        ge=0,
        le=1,
        description="Tiene piscina (0=no, 1=si)",
        example=0
    )

    @field_validator('lat')
    @classmethod
    def validate_latitude_scz(cls, v):
        """Validar que la latitud est en rango de Santa Cruz"""
        if not (-18.0 <= v <= -17.5):
            raise ValueError('Latitud fuera del rango de Santa Cruz de la Sierra')
        return v

    @field_validator('lon')
    @classmethod
    def validate_longitude_scz(cls, v):
        """Validar que la longitud est en rango de Santa Cruz"""
        if not (-63.5 <= v <= -62.5):
            raise ValueError('Longitud fuera del rango de Santa Cruz de la Sierra')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "metros": 80.0,
                "cuartos": 2,
                "banos": 1,
                "lat": -17.783889,
                "lon": -63.182222,
                "parking": 1,
                "piscina": 0
            }
        }


class PredictionResponse(BaseModel):
    """Schema para response de prediccin"""

    precio_sugerido: float = Field(..., description="Precio sugerido en ETH", example=0.0015)
    precio_min: float = Field(..., description="Precio mnimo en ETH", example=0.0012)
    precio_max: float = Field(..., description="Precio mximo en ETH", example=0.0018)
    confianza: float = Field(..., ge=0, le=1, description="Confianza del modelo (0-1)", example=0.92)
    anillo: float = Field(..., description="Anillo detectado (1-10, puede ser 3.5 para 3er Externo)", example=2)
    zona_especial: str | None = Field(None, description="Zona especial si aplica", example="Equipetrol")

    class Config:
        json_schema_extra = {
            "example": {
                "precio_sugerido": 0.0015,
                "precio_min": 0.0012,
                "precio_max": 0.0018,
                "confianza": 0.92,
                "anillo": 2,
                "zona_especial": None
            }
        }
