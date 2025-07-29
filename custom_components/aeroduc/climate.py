from homeassistant.const import UnitOfTemperature
from homeassistant.components.climate import ClimateEntity
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    hass.data.setdefault(DOMAIN, {})
    host = entry.data["host"]
    device = AeroducDevice(host)
    hass.data[DOMAIN][entry.entry_id] = device
    return True


class AeroducDevice:
    def __init__(self, host):
        self.host = host


class AeroducClimate(ClimateEntity):
    def __init__(self, device: AeroducDevice):
        self._device = device
        self._attr_name = "Aeroduc Climate"
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self._device.read_temperature()

    @property
    def hvac_mode(self):
        return "cool"

    async def async_set_hvac_mode(self, hvac_mode):
        await self._device.set_mode(hvac_mode)

    @property
    def supported_features(self):
        return 0
