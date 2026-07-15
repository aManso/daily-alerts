from dataclasses import dataclass


@dataclass(slots=True)
class FuelStation:
    id: int
    name: str
    address: str
    city: str
    latitude: float
    longitude: float
    price: float
    distance: float = 0