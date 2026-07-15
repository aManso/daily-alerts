from math import asin, cos, radians, sin, sqrt

from pathlib import Path
import json
import requests

from models.fuel_result import FuelResult
from models.fuel_station import FuelStation

URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
CACHE_FILE = Path("cache/fuel_stations.json")
FUEL_FIELDS = {
    "gasoleo_a": "Precio Gasoleo A",
    "gasoleo_a_premium": "Precio Gasoleo Premium",
    "gasolina_95": "Precio Gasolina 95 E5",
    "gasolina_98": "Precio Gasolina 98 E5",
}


def _to_float(value: str) -> float | None:
    if not value:
        return None

    return float(value.replace(",", "."))


def _download(use_cache=False):

    print(f"Downloading fuel stations data... {use_cache}")

    if use_cache:

        if not CACHE_FILE.exists():
            raise FileNotFoundError(
                "cache/fuel_stations.json not found. Download it first."
            )

        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)["ListaEESSPrecio"]

    response = requests.get(URL, timeout=60)

    response.raise_for_status()

    return response.json()["ListaEESSPrecio"]


def _normalize(station: dict, fuel_field: str) -> FuelStation | None:

    price = _to_float(station[fuel_field])

    if price is None:
        return None

    return FuelStation(
        id=int(station["IDEESS"]),
        name=station["Rótulo"],
        address=station["Dirección"],
        city=station["Localidad"],
        latitude=_to_float(station["Latitud"]),
        longitude=_to_float(station["Longitud (WGS84)"]),
        price=price,
    )


def _distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    return R * 2 * asin(sqrt(a))


def search(
    reference_station_id: int,
    radius_km: float,
    fuel_type: str,
    use_cache: bool = False,
) -> FuelResult:

    fuel_field = FUEL_FIELDS[fuel_type]

    stations = []

    for raw in _download(use_cache=use_cache):

        station = _normalize(raw, fuel_field)

        if station:
            stations.append(station)

    reference = next(
        s for s in stations
        if s.id == reference_station_id
    )

    nearby = []

    for station in stations:

        station.distance = _distance(
            reference.latitude,
            reference.longitude,
            station.latitude,
            station.longitude,
        )

        if station.distance <= radius_km:
            nearby.append(station)

    nearby.sort(key=lambda s: s.price)

    return FuelResult(
        reference_station=reference,
        cheapest_station=nearby[0],
        nearby_stations=nearby,
    )


def find(text: str, fuel_type: str = "gasoleo_a") -> list[FuelStation]:

    fuel_field = FUEL_FIELDS[fuel_type]

    tokens = text.lower().strip().split()

    results = []

    print(f"Searching for '{text}'...")

    for raw in _download(use_cache=True):

        station = _normalize(raw, fuel_field)

        if station is None:
            continue

        name = station.name.lower()
        address = station.address.lower()
        city = station.city.lower()

        haystack = f"{name} {address} {city}"

        # Todas las palabras deben aparecer
        if not all(token in haystack for token in tokens):
            continue

        score = 0

        for token in tokens:

            if token in name:
                score += 100

            if token in address:
                score += 50

            if token in city:
                score += 20

        results.append((score, station))

    results.sort(
        key=lambda item: (
            -item[0],              # Mayor puntuación primero
            item[1].city,
            item[1].name
        )
    )

    return [station for _, station in results]
