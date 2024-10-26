from geopy.geocoders import Nominatim
from app.services.geocoding_service import GeocodingService

class NominatimGeocodingService(GeocodingService):
    def __init__(self):
        self.geolocator = Nominatim(user_agent="astro_api")

    def get_coordinates(self, location_name: str):
        location = self.geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(f"Ubicación '{location_name}' no encontrada")
