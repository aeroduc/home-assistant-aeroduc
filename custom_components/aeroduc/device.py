import asyncio
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)


class AeroducDevice:
    """Handles all communication with the AeroDuc HTTP API."""

    def __init__(self, host: str):
        self.host = host
        self.base_url = f"http://{host}"
        self.device_id: str = None
        self.name: str = None
        self.manufacturer: str = None
        self.model: str = None
        self._status_endpoint: str = None
        self._info_endpoint: str = None
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Fetch /api/info once at startup."""
        async with self._lock:
            if self.device_id is not None:
                return  # already done

            url = f"{self.base_url}/api/info"
            _LOGGER.debug("Fetching AeroDuc info from %s", url)
            async with aiohttp.ClientSession() as session:
                resp = await session.get(url)
                resp.raise_for_status()
                info = await resp.json()

            self.device_id = info["device_id"]
            self.name = info["name"]
            self.manufacturer = info["manufacturer"]
            self.model = info["model"]
            self._info_endpoint = info["endpoints"]["info"]
            self._status_endpoint = info["endpoints"]["status"]
            _LOGGER.info("AeroDuc %s initialized", self.device_id)

    async def _fetch_status(self) -> dict:
        """Fetch /api/status."""
        url = f"{self.base_url}{self._status_endpoint}"
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            resp.raise_for_status()
            return await resp.json()

    @property
    async def read_temperature(self) -> float:
        data = await self._fetch_status()
        return data["sensors"]["temperature"]

    @property
    async def read_humidity(self) -> float:
        data = await self._fetch_status()
        return data["sensors"]["humidity"]
