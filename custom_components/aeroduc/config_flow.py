import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.warning(">>> Aeroduc config_flow.py loaded")


class AeroducConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_zeroconf(self, discovery_info):
        _LOGGER.warning("🧠 Zeroconf triggered: %s", discovery_info)

        self.discovery_info = discovery_info
        host = getattr(discovery_info, "host", discovery_info.ip_address)
        unique_id = discovery_info.properties.get("device_id", host)
        _LOGGER.warning("🌍 Using unique_id: %s", unique_id)

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})

        self.discovery_info.host = discovery_info.ip_address
        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        """Confirm discovery before setting up."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.discovery_info.name,
                data={CONF_HOST: self.discovery_info.host},
            )

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={"name": self.discovery_info.name},
        )

    async def async_step_user(self, user_input=None):
        """Manual config fallback."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_HOST],
                data={CONF_HOST: user_input[CONF_HOST]},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
        )
