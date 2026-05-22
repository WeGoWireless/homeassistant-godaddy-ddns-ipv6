from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN

SENSORS = [
    ("ipv6", "GoDaddy DDNS IPv6 Address"),
    ("last_updated", "GoDaddy DDNS Last Updated"),
    ("success", "GoDaddy DDNS API Success"),
    ("http_code", "GoDaddy DDNS HTTP Code"),
    ("http_text", "GoDaddy DDNS HTTP Status"),
    ("message", "GoDaddy DDNS Last Message"),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([
        GoDaddyDDNSSensor(coordinator, entry, key, name)
        for key, name in SENSORS
    ])

class GoDaddyDDNSSensor(SensorEntity):
    def __init__(self, coordinator, entry, key, name):
        self.coordinator = coordinator
        self.entry = entry
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.key)

    @property
    def extra_state_attributes(self):
        return {
            "integration": "GoDaddy DDNS IPv6",
        }

    async def async_update(self):
        await self.coordinator.async_request_refresh()
