from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from .const import DOMAIN

class AeroducConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_zeroconf(self, discovery_info):
        host = discovery_info.host
        unique_id = discovery_info.properties.get("device_id", host)
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_HOST: host})
        return self.async_create_entry(title=discovery_info.name, data={CONF_HOST: host})
