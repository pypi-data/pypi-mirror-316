"""Implementation of an API for accessing the EvoCarShare service."""

import logging
import time
from collections.abc import Iterable
from typing import Any

from aiohttp import ClientResponse, ClientSession

from .exceptions import EvoApiCallError, EvoProgramError
from .types import CredentialBundle, GpsCoord, RangedVehicle, Token, Vehicle

_LOGGER = logging.getLogger(__name__)

# DictKeys
ACCESS_TOKEN = "access_token"  # noqa: S105
LOCATION = "location"


class EvoApi:
    URL_OAUTH: str = "https://java-us01.vulog.com/auth/realms/BCAA-CAYVR/protocol/openid-connect/token/"
    URL_VEHCILES: str = "https://java-us01.vulog.com/apiv5/availableVehicles/fc256982-77d1-455c-8ab0-7862c170db6a"

    def __init__(self, client_session: ClientSession, credentials: CredentialBundle, request_timeout: int = 10) -> None:
        self._token = None
        self._client_session = client_session
        self.credentials = credentials

        self._request_timeout = request_timeout

    async def _async_get_token(self) -> tuple[str, float]:
        data = {
            "grant_type": "client_credentials",
            "scope": "",
            "client_id": self.credentials.client_id,
            "client_secret": self.credentials.client_secret,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
        }

        async with self._client_session.post(self.URL_OAUTH, headers=headers, data=data) as resp:
            data = await self._parse_response(resp)
            if ACCESS_TOKEN not in data:
                raise EvoApiCallError(resp.status, self.URL_OAUTH, data)

            return (data[ACCESS_TOKEN], data["expires_in"])

    async def get_token(self) -> Token:
        if not self._validate_token(self._token):
            token = None
            _LOGGER.debug("No valid token - fetching")
            token, valid_for = await self._async_get_token()
            self._token = Token(token, time.time() + valid_for - 1)

        if not self._token:
            raise EvoProgramError("expectNotNull", self._token)  # TODO Add retry logic
        return self._token

    @staticmethod
    def _validate_token(token: Token | None, now: float | None = None) -> bool:
        if not token:
            return False
        return (now or time.time()) > token.valid_to

    def build_headers(self, token: Token) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Connection": "close",
            "Authorization": "bearer " + str(token.token),  # TODO remove str?
            "X-API-Key": self.credentials.api_key,
            "Host": "java-us01.vulog.com",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.8",
        }

    async def _parse_response(self, resp: ClientResponse, ref_coord: GpsCoord | None = None) -> Any:
        data = await resp.json()
        if resp.status != 200:
            raise EvoApiCallError(status=resp.status, url=str(resp.url), payload=await resp.json())

        _LOGGER.debug("ApiCallData(%s):%s", resp.url, data)
        return data

    async def get_vehicles(self) -> "Iterable[Vehicle]":
        token = await self.get_token()
        headers = self.build_headers(token)
        async with self._client_session.get(self.URL_VEHCILES, headers=headers) as resp:
            data = await self._parse_response(resp)
            return [Vehicle.from_dict(d) for d in data]

    async def get_vehicles_within(self, meters: int, of: GpsCoord) -> "Iterable[Vehicle]":
        return self._filter_vehicles_within(meters, of, await self.get_vehicles())

    @staticmethod
    def _filter_vehicles_within(meters: int, of: GpsCoord, vehicles: Iterable[Vehicle]) -> Iterable[Vehicle]:
        def close(v: RangedVehicle) -> bool:
            return v.distance <= meters

        return filter(close, [v.to_ranged(of) for v in vehicles])
