import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    device = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            AeroducTemperature(device),
            AeroducHumidity(device),
        ],
        update_before_add=True,
    )


class AeroducSensorBase(SensorEntity):
    def __init__(self, device, sensor_type):
        self._device = device
        self._sensor_type = sensor_type  # "temperature" or "humidity"

        # friendly name from the API info
        self._attr_name = f"{device.name} {sensor_type.title()}"

        # unique_id: device_id + sensor type
        self._attr_unique_id = f"{device.device_id}_{sensor_type}"

        # tie to the hardware device in HA
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device.device_id)},
            "name": device.name,
            "manufacturer": device.manufacturer,
            "model": device.model,
        }


class AeroducTemperature(AeroducSensorBase):
    def __init__(self, device):
        super().__init__(device, "temperature")
        self._attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT

    async def async_update(self):
        # HA calls this to refresh the value
        self._attr_native_value = await self._device.read_temperature


class AeroducHumidity(AeroducSensorBase):
    def __init__(self, device):
        super().__init__(device, "humidity")
        self._attr_native_unit_of_measurement = PERCENTAGE

    async def async_update(self):
        self._attr_native_value = await self._device.read_humidity
