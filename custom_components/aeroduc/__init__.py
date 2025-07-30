from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .device import AeroducDevice
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # create & initialize your device
    device = AeroducDevice(entry.data["host"])
    await device.initialize()
    # stash it so your platforms can pick it up
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = device

    # forward to sensor only
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
