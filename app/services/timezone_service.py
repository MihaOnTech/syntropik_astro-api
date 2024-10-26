from timezonefinder import TimezoneFinder
import pytz

def get_timezone(lat: float, lon: float):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    if timezone_str:
        return pytz.timezone(timezone_str)
    else:
        raise ValueError("Zona horaria no encontrada para las coordenadas proporcionadas")
