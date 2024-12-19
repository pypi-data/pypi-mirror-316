from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, Self

from haversine.haversine import Unit, haversine

from .typing import ApiVehicleData


@dataclass
class CredentialBundle:
    api_key: str
    client_id: str
    client_secret: str


class Token(NamedTuple):
    token: str
    valid_to: float


@dataclass
class GpsCoord:
    """GPS Coordinate."""

    latitude: float
    longitude: float

    def distanceTo(self, other: GpsCoord) -> int:
        """Return the distance between two GpsCoords measured in meters."""

        dist: float = haversine(self.to_tuple(), other.to_tuple(), unit=Unit.METERS)
        return int(dist)

    def __iter__(self):
        yield self.latitude
        yield self.longitude

    def to_tuple(self) -> tuple[float, float]:
        return self.latitude, self.longitude


DESC = "description"
LOCATION = "location"
STATUS = "status"


class Vehicle:
    vid: str
    model: str
    plate: str
    location: GpsCoord
    energy_level: int
    is_charging: bool

    def __init__(
        self,
        vid: str,
        model: str,
        plate: str,
        location: GpsCoord,
        energy_level: int,
        is_charging: bool,
    ):
        self.vid = vid
        self.model = model
        self.plate = plate
        self.location = location
        self.energy_level = energy_level
        self.is_charging = is_charging

    def __repr__(self) -> str:
        return f"Evo( {self._repr__guts()} )"

    def _repr__guts(self) -> str:
        return f'vid="{self.vid}" plate="{self.plate}"  model="{self.model}" location={self.location} is_charging={self.is_charging}'

    @classmethod
    def from_dict(cls, d: ApiVehicleData) -> Self:
        return cls(
            vid=d[DESC]["id"],
            model=d[DESC]["model"],
            plate=d[DESC]["plate"],
            location=GpsCoord(d[LOCATION]["position"]["lat"], d[LOCATION]["position"]["lon"]),
            energy_level=d[STATUS]["energyLevel"],
            is_charging=d[STATUS]["isCharging"],
        )

    def distanceFrom(self, gps: GpsCoord) -> int:
        return self.location.distanceTo(gps)

    def to_ranged(self, gps: GpsCoord) -> RangedVehicle:
        return RangedVehicle(self, gps)


class RangedVehicle(Vehicle):
    """A Vehicle which contains a distance to a given GpsCoord"""

    _instance: Vehicle
    distance: int

    def __init__(self, vehicle: Vehicle, ref_coord: GpsCoord) -> None:
        # This class uses both inheritance and composition.
        # Composition is used to allow initializing this class without having to duplicate __init__
        # Inheritance is used to provide code completion and typing, __getattr__ calls out to _instance
        self._instance = vehicle
        dd = vehicle.distanceFrom(ref_coord)
        self.distance = dd
        pass

    def __getattr__(self, name: str):
        return getattr(self._instance, name)

    def __repr__(self) -> str:
        return f'RangedEvo( {self._repr__guts()} distance="{self.distance}" )'
