# GoDaddy DDNS IPv6 for Home Assistant

Automatically updates a GoDaddy AAAA DNS record using the current IPv6 address from a selected Home Assistant network interface.

Supports:
- IPv6 dynamic DNS updates
- Ethernet or Wi-Fi interfaces
- Home Assistant UI configuration
- HACS installation
- Manual force update button
- Status sensors
- Configurable update interval
- Runtime reconfiguration without removing the integration

---

# Features

## Automatic IPv6 Detection

Uses Home Assistant network adapters directly instead of shell scripts or container network commands.

Works correctly with:
- Home Assistant OS
- Home Assistant Supervised
- Home Assistant Container

---

## Configurable Interface Selection

Choose the interface used for IPv6 updates:
- `end0`
- `eth0`
- `wlan0`
- etc.

Interfaces are selectable from the Home Assistant UI.

---

## Automatic DDNS Updates

Checks for IPv6 changes automatically.

Only updates GoDaddy when the IPv6 address changes.

Default update interval:
- 60 minutes

Configurable from the integration settings.

---

## Runtime Reconfiguration

Without removing the integration, you can change:
- API Key
- API Secret
- Domain
- Record Name
- Interface
- TTL
- Update Interval

From:

`Settings → Devices & Services → GoDaddy DDNS IPv6 → Configure`

---

# Entities Created

## Sensors

| Entity | Description |
|---|---|
| `sensor.godaddy_ddns_ipv6_address` | Current detected IPv6 |
| `sensor.godaddy_ddns_last_updated` | Last successful update time |
| `sensor.godaddy_ddns_api_success` | API success/failure |
| `sensor.godaddy_ddns_http_code` | HTTP response code |
| `sensor.godaddy_ddns_http_status` | Human-readable HTTP status |
| `sensor.godaddy_ddns_last_message` | Last API/update message |

---

## Button

| Entity | Description |
|---|---|
| `button.godaddy_ddns_force_update` | Force immediate update |

---

# Installation

## HACS Installation

### Add Custom Repository

In HACS:

1. Open HACS
2. Integrations
3. Click the three dots in the upper-right
4. Select:
   - Custom repositories

Add:

```text
https://github.com/YOUR_GITHUB_USERNAME/homeassistant-godaddy-ddns-ipv6
