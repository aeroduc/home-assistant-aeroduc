import requests
from homeassistant.components.climate import ClimateEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.climate.const import HVAC_MODE_COOL, HVAC_MODE_OFF

async def async_setup_entry(hass, entry):
    host = entry.data["host"]
    device = AeroducClimate(host)
    hass.data.setdefault("aeroduc", []).append(device)
    hass.helpers.entity_platform.async_add_entities([device], update_before_add=True)

class AeroducClimate(ClimateEntity):
    def __init__(self, host):
        self._host = host
        self._temp = None
        self._humid = None
        self._mode = HVAC_MODE_OFF

    @property
    def name(self):
        return "Aeroduc Climate"

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def hvac_mode(self):
        return self._mode

    async def async_update(self):
        resp = await self.hass.async_add_executor_job(requests.get, f"http://{self._host}/api/status")
        data = resp.json()
        self._temp = data.get("temperature")
        self._humid = data.get("humidity")
        self._mode = HVAC_MODE_COOL if data.get("on") else HVAC_MODE_OFF
