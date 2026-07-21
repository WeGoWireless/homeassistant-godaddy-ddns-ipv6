"""Binary sensors for GoDaddy DDNS IPv6."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up GoDaddy DDNS IPv6 binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        [
            GoDaddyPublicIPv6AvailableBinarySensor(
                coordinator,
                entry,
            )
        ]
    )


class GoDaddyPublicIPv6AvailableBinarySensor(
    CoordinatorEntity,
    BinarySensorEntity,
):
    """Report whether Home Assistant has a public IPv6 address."""

    _attr_has_entity_name = True
    _attr_name = "Public IPv6 Available"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_icon = "mdi:ip-network"

    def __init__(self, coordinator, entry):
        """Initialize the binary sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = (
            f"{entry.entry_id}_public_ipv6_available"
        )

    @property
    def is_on(self) -> bool:
        """Return true when a public IPv6 address is available."""
        if not isinstance(self.coordinator.data, dict):
            return False

        return bool(self.coordinator.data.get("ipv6"))

    @property
    def extra_state_attributes(self):
        """Return diagnostic information."""
        if not isinstance(self.coordinator.data, dict):
            return {
                "ipv6_address": None,
                "message": "Coordinator data unavailable",
            }

        return {
            "ipv6_address": self.coordinator.data.get("ipv6"),
            "last_updated": self.coordinator.data.get("last_updated"),
            "api_success": self.coordinator.data.get("success"),
            "http_code": self.coordinator.data.get("http_code"),
            "http_status": self.coordinator.data.get("http_text"),
            "message": self.coordinator.data.get("message"),
        }
