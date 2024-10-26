from abc import ABC, abstractmethod

class GeocodingService(ABC):
    @abstractmethod
    def get_coordinates(self, location_name: str):
        pass