from geopy.geocoders import Nominatim

def get_coordinates(location_name: str):
    geolocator = Nominatim(user_agent="astro_api")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        raise ValueError(f"Ubicación '{location_name}' no encontrada")