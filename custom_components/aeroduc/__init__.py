from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .climate import async_setup_entry as climate_setup

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(climate_setup(hass, entry))
    return True
