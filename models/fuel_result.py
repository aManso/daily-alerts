from dataclasses import dataclass
from .fuel_station import FuelStation

@dataclass(slots=True)
class FuelResult:
    reference_station: FuelStation
    cheapest_station: FuelStation
    nearby_stations: list[FuelStation]