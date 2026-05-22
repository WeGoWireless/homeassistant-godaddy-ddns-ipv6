from homeassistant.components.button import ButtonEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        GoDaddyDDNSUpdateButton(data["coordinator"], data["updater"], entry),
    ])

class GoDaddyDDNSUpdateButton(ButtonEntity):
    def __init__(self, coordinator, updater, entry):
        self.coordinator = coordinator
        self.updater = updater
        self.entry = entry
        self._attr_name = "GoDaddy DDNS Force Update"
        self._attr_unique_id = f"{entry.entry_id}_force_update"

    async def async_press(self):
        await self.updater.async_update(force=True)
        await self.coordinator.async_request_refresh()
