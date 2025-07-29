from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .climate import async_setup_entry as climate_setup


async def async_setup(hass: HomeAssistant, config: dict):
    # Required to allow config flow setup
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_setups(entry, ["climate", "sensor"])
    return True
