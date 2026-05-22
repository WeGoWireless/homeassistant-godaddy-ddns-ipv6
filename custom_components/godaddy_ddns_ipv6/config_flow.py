import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import network

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_API_SECRET,
    CONF_DOMAIN,
    CONF_RECORD_NAME,
    CONF_INTERFACE,
    CONF_TTL,
    CONF_UPDATE_INTERVAL,
    DEFAULT_INTERFACE,
    DEFAULT_TTL,
    DEFAULT_RECORD_NAME,
    DEFAULT_UPDATE_INTERVAL,
)


class GoDaddyDDNSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry):
        return GoDaddyDDNSOptionsFlow()

    async def _async_get_interfaces(self):
        interfaces = []

        adapters = await network.async_get_adapters(self.hass)

        for adapter in adapters:
            name = adapter.get("name")

            if name and name not in interfaces:
                interfaces.append(name)

        fallback = [
            "end0",
            "wlan0",
            "eth0",
            "wlan1",
        ]

        for iface in fallback:
            if iface not in interfaces:
                interfaces.append(iface)

        return interfaces

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=f"{user_input[CONF_RECORD_NAME]}.{user_input[CONF_DOMAIN]}",
                data=user_input,
                options={
                    CONF_INTERFACE: user_input[CONF_INTERFACE],
                    CONF_TTL: user_input[CONF_TTL],
                    CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                },
            )

        interfaces = await self._async_get_interfaces()

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_API_SECRET): str,
            vol.Required(CONF_DOMAIN): str,
            vol.Required(
                CONF_RECORD_NAME,
                default=DEFAULT_RECORD_NAME,
            ): str,
            vol.Required(
                CONF_INTERFACE,
                default=DEFAULT_INTERFACE,
            ): vol.In(interfaces),
            vol.Required(
                CONF_TTL,
                default=DEFAULT_TTL,
            ): int,
            vol.Required(
                CONF_UPDATE_INTERVAL,
                default=DEFAULT_UPDATE_INTERVAL,
            ): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )


class GoDaddyDDNSOptionsFlow(config_entries.OptionsFlow):
    async def _async_get_interfaces(self):
        interfaces = []

        adapters = await network.async_get_adapters(self.hass)

        allowed_prefixes = (
            "end",
            "eno",
            "ens",
            "enp",
            "eth",
            "wlan",
            "wl",
        )

        blocked_prefixes = (
            "veth",
            "docker",
            "br-",
            "hassio",
            "lo",
            "zt",
            "tailscale",
        )

        for adapter in adapters:
            name = adapter.get("name")

            if not name:
                continue

            if name.startswith(blocked_prefixes):
                continue

            if not name.startswith(allowed_prefixes):
                continue

            if name not in interfaces:
                interfaces.append(name)

        fallback = ["end0", "wlan0", "eth0"]

        for iface in fallback:
            if iface not in interfaces:
                interfaces.append(iface)

        return interfaces

    async def async_step_init(self, user_input=None):
        config_entry = self.hass.config_entries.async_get_entry(self.handler)

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interface = config_entry.options.get(
            CONF_INTERFACE,
            config_entry.data.get(CONF_INTERFACE, DEFAULT_INTERFACE),
        )

        current_ttl = config_entry.options.get(
            CONF_TTL,
            config_entry.data.get(CONF_TTL, DEFAULT_TTL),
        )

        current_update_interval = config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            config_entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
        )

        interfaces = await self._async_get_interfaces()

        schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=config_entry.options.get(CONF_API_KEY, config_entry.data.get(CONF_API_KEY)),): str,
            vol.Required(CONF_API_SECRET, default=config_entry.options.get(CONF_API_SECRET, config_entry.data.get(CONF_API_SECRET)),): str,
            vol.Required(CONF_DOMAIN, default=config_entry.options.get(CONF_DOMAIN, config_entry.data.get(CONF_DOMAIN)),): str,
            vol.Required(CONF_RECORD_NAME, default=config_entry.options.get(CONF_RECORD_NAME, config_entry.data.get(CONF_RECORD_NAME, DEFAULT_RECORD_NAME)),): str,
            vol.Required(CONF_INTERFACE, default=current_interface): vol.In(interfaces),
            vol.Required(CONF_TTL, default=current_ttl): int,
            vol.Required(CONF_UPDATE_INTERVAL, default=current_update_interval): int,
        })

        return self.async_show_form(step_id="init", data_schema=schema)
