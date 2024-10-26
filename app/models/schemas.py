"""
Este módulo define los modelos de datos utilizados 
para las entradas y salidas de la API astrológica.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class RetrogradeStatus(str, Enum):
    DIRECT = "Directo"
    RETROGRADE = "Retrógrado"


class BirthData(BaseModel):
    name: str = Field(..., description="Nombre de la persona")
    date: str = Field(
        ...,
        description="Fecha de nacimiento en formato 'dd/mm/yyyy'",
        example="05/02/1993",
    )
    time: str = Field(
        ...,
        description="Hora de nacimiento en formato 'HH:MM' (24 horas)",
        example="15:30",
    )
    location: Optional[str] = Field(
        None,
        description="Lugar de nacimiento (ciudad, país)",
        example="Zaragoza, España",
    )
    latitude: Optional[float] = Field(
        None, description="Latitud de la ubicación", example=41.6561
    )
    longitude: Optional[float] = Field(
        None, description="Longitud de la ubicación", example=-0.8773
    )

    @field_validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%Y")
        except ValueError:
            raise ValueError("La fecha debe estar en formato 'dd/mm/yyyy'")
        return v

    @field_validator("time")
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError("La hora debe estar en formato 'HH:MM'")
        return v

    @model_validator(mode="after")
    def check_location_or_coordinates(cls, values):
        if not values.location and (
            values.latitude is None or values.longitude is None
        ):
            raise ValueError("Debe proporcionar 'location' o 'latitude' y 'longitude'")
        return values


class Planet(BaseModel):
    planet: str = Field(..., description="Nombre del planeta", example="Sol")
    sign: str = Field(
        ...,
        description="Signo zodiacal en el que se encuentra el planeta",
        example="Acuario",
    )
    sign_degrees: float = Field(
        ..., description="Grados dentro del signo zodiacal", example=16.30
    )
    retrograde: RetrogradeStatus = Field(
        ..., description="Movimiento retrógrado o directo", example="Directo"
    )
    position: float = Field(
        ..., description="Posición eclíptica en grados (0° a 360°)", example=316.30
    )
    house: int = Field(..., description="Número de la casa (1-12)", example=3)

    @field_validator("sign_degrees")
    def validate_sign_degrees(cls, v):
        if not 0 <= v < 30:
            raise ValueError("sign_degrees debe estar entre 0 y 30")
        return v

    @field_validator("position")
    def validate_position(cls, v):
        if not 0 <= v < 360:
            raise ValueError("position debe estar entre 0 y 360")
        return v


class House(BaseModel):
    house: int = Field(..., description="Número de la casa (1-12)", example=1)
    sign: str = Field(
        ..., description="Signo zodiacal en la cúspide de la casa", example="Sagitario"
    )
    degrees: float = Field(
        ..., description="Grados de la cúspide de la casa", example=3.97
    )
    position: float = Field(
        ..., description="Posición en grados eclípticos", example=243.97
    )


class Aspect(BaseModel):
    planet_1: str = Field(..., description="Primer planeta", example="Sol")
    planet_2: str = Field(..., description="Segundo planeta", example="Luna")
    aspect: str = Field(
        ...,
        description="Tipo de aspecto (Conjunción, Oposición, etc.)",
        example="Conjunción",
    )
    degree: float = Field(
        ..., description="Ángulo exacto del aspecto en grados", example=0.0
    )

    @field_validator("degree")
    def validate_degree(cls, v):
        if not 0 <= v <= 360:
            raise ValueError("degree debe estar entre 0 y 360")
        return v


class AstrologyData(BaseModel):
    name: str
    date: str
    time: str
    location: str
    planets: List[Planet]
    houses: List[House]
    aspects: List[Aspect]
