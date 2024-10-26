import googlemaps
from app.services.geocoding_service import GeocodingService

class GoogleMapsGeocodingService(GeocodingService):
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def get_coordinates(self, location_name: str):
        geocode_result = self.client.geocode(location_name)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            raise ValueError(f"Ubicación '{location_name}' no encontrada")
