from geopy.distance import geodesic
from haversine import haversine

class DistanceStrategy:
    def calculate(self, coord1, coord2):
        raise NotImplementedError

class GeopyStrategy(DistanceStrategy):
    def calculate(self, coord1, coord2):
        return geodesic(coord1, coord2).km

class HaversineStrategy(DistanceStrategy):
    def calculate(self, coord1, coord2):
        return haversine(coord1, coord2)

class GeoDistanceContext:
    def __init__(self, strategy: DistanceStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DistanceStrategy):
        self._strategy = strategy

    def calculate_distance(self, coord1, coord2):
        return self._strategy.calculate(coord1, coord2)
