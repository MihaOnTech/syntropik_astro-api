from fastapi import APIRouter, HTTPException
from app.models.schemas import BirthData, AstrologyData
from app.services.geocoding_service import get_coordinates
from app.services.timezone_service import get_timezone
from app.services.astrology_service import AstrologyCalculator
from datetime import datetime

router = APIRouter()

@router.post("/calculate", response_model=AstrologyData)
async def calculate_astrology(data: BirthData):
    try:
        # Obtener coordenadas
        if data.latitude is not None and data.longitude is not None:
            lat, lon = data.latitude, data.longitude
        else:
            lat, lon = get_coordinates(data.location)

        # Obtener zona horaria
        timezone = get_timezone(lat, lon)

        # Procesar fecha y hora
        birth_datetime = datetime.strptime(f"{data.date} {data.time}", "%d/%m/%Y %H:%M")
        birth_datetime = timezone.localize(birth_datetime)

        # Cálculos astrológicos
        calculator = AstrologyCalculator()
        planets = calculator.calculate_planets(birth_datetime, lat, lon)
        houses = calculator.calculate_houses(birth_datetime, lat, lon)
        aspects = calculator.calculate_aspects(planets)

        result = AstrologyData(
            name=data.name,
            date=data.date,
            time=data.time,
            location=data.location or f"{lat}, {lon}",
            planets=planets,
            houses=houses,
            aspects=aspects
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
