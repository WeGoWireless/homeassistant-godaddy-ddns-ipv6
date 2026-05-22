import logging
import requests

from homeassistant.components import network
from homeassistant.util import dt as dt_util

from .const import (
    CONF_API_KEY,
    CONF_API_SECRET,
    CONF_DOMAIN,
    CONF_RECORD_NAME,
    CONF_INTERFACE,
    CONF_TTL,
)

_LOGGER = logging.getLogger(__name__)


class GoDaddyDDNSUpdater:
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self.last_ipv6 = None
        self.last_updated = None
        self.last_success = False
        self.last_http_code = None
        self.last_message = None

    def _get_config(self, key):
        return self.entry.options.get(key, self.entry.data.get(key))

    async def async_update(self, force=False):
        ipv6 = await self._async_get_ipv6()

        if not ipv6:
            self.last_success = False
            self.last_http_code = None
            self.last_message = "No global IPv6 found"
            return self._data(None)

        if not force and ipv6 == self.last_ipv6:
            self.last_success = True
            self.last_message = "IPv6 unchanged"
            return self._data(ipv6)

        try:
            status_code, message = await self.hass.async_add_executor_job(
                self._update_godaddy,
                ipv6,
            )

            self.last_ipv6 = ipv6
            self.last_updated = dt_util.now().strftime("%m/%d/%Y %I:%M %p")
            self.last_success = status_code == 200
            self.last_http_code = status_code
            self.last_message = message

        except Exception as err:
            self.last_success = False
            self.last_http_code = None
            self.last_message = str(err)
            _LOGGER.exception("GoDaddy DDNS update failed")

        return self._data(ipv6)

    def _data(self, ipv6):
        return {
            "ipv6": ipv6,
            "last_updated": self.last_updated,
            "success": self.last_success,
            "http_code": self.last_http_code,
            "http_text": self._http_text(self.last_http_code)
            if self.last_http_code
            else None,
            "message": self.last_message,
        }

    def _http_text(self, code):
        mapping = {
            200: "OK",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            422: "Invalid Record",
            429: "Rate Limited",
            500: "Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }

        return mapping.get(code, f"HTTP {code}")

    async def _async_get_ipv6(self):
        adapters = await network.async_get_adapters(self.hass)
        interface = self._get_config(CONF_INTERFACE)

        for adapter in adapters:
            if adapter.get("name") != interface:
                continue

            for ipv6 in adapter.get("ipv6", []):
                addr = ipv6.get("address")

                if not addr:
                    continue

                addr = addr.split("/", 1)[0].lower()

                if addr.startswith("fe80"):
                    continue
                if addr.startswith("fd"):
                    continue
                if addr.startswith("::1"):
                    continue

                _LOGGER.info(
                    "GoDaddy DDNS found global IPv6 on %s: %s",
                    interface,
                    addr,
                )
                return addr

        _LOGGER.warning("GoDaddy DDNS no global IPv6 found on %s", interface)
        return None

    def _update_godaddy(self, ipv6):
        api_key = self._get_config(CONF_API_KEY)
        api_secret = self._get_config(CONF_API_SECRET)
        domain = self._get_config(CONF_DOMAIN)
        record = self._get_config(CONF_RECORD_NAME)
        ttl = self._get_config(CONF_TTL)

        url = f"https://api.godaddy.com/v1/domains/{domain}/records/AAAA/{record}"

        headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json",
        }

        payload = [
            {
                "data": ipv6,
                "ttl": ttl,
            }
        ]

        response = requests.put(url, headers=headers, json=payload, timeout=20)

        if response.status_code == 200:
            return response.status_code, "GoDaddy AAAA record updated"

        return response.status_code, f"GoDaddy failed: {response.text}"
