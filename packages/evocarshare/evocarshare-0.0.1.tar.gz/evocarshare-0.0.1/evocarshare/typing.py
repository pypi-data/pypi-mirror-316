from typing import TypedDict


class ApiVehicleStatus(TypedDict):
    energyLevel: int
    isCharging: bool


class ApiVehicleDesc(TypedDict):
    id: str
    model: str
    plate: str
    name: str
    modelId: str
    optionIds: list[str]
    cityId: str
    serviceId: str
    iconUrl: str


class ApiVehiclePosition(TypedDict):
    lat: float
    lon: float


class ApiVehicleLocation(TypedDict):
    address: dict[str, str]  # TODO
    position: ApiVehiclePosition


class ApiVehicleData(TypedDict):
    status: ApiVehicleStatus
    description: ApiVehicleDesc
    location: ApiVehicleLocation


# class ApiError(TypedDict):
#     code: str
