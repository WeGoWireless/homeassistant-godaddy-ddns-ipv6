GoDaddy DDNS IPv6 for Home Assistant

Automatically updates a GoDaddy AAAA DNS record using the current IPv6 address from a selected Home Assistant network interface.

Supports:

IPv6 dynamic DNS updates
Ethernet or Wi-Fi interfaces
Home Assistant UI configuration
HACS installation
Manual force update button
Status sensors
Configurable update interval
Runtime reconfiguration without removing the integration
Features
Automatic IPv6 Detection

Uses Home Assistant network adapters directly instead of shell scripts or container network commands.

Works correctly with:

Home Assistant OS
Home Assistant Supervised
Home Assistant Container
Configurable Interface Selection

Choose the interface used for IPv6 updates:

end0
eth0
wlan0
etc.

Interfaces are selectable from the Home Assistant UI.

Automatic DDNS Updates

Checks for IPv6 changes automatically.

Only updates GoDaddy when the IPv6 address changes.

Default update interval:

60 minutes

Configurable from the integration settings.

Runtime Reconfiguration

Without removing the integration, you can change:

API Key
API Secret
Domain
Record Name
Interface
TTL
Update Interval

From:

Settings
Devices & Services
GoDaddy DDNS IPv6
Configure
Entities Created
Sensors
Entity	Description
sensor.godaddy_ddns_ipv6_address	Current detected IPv6
sensor.godaddy_ddns_last_updated	Last successful update time
sensor.godaddy_ddns_api_success	API success/failure
sensor.godaddy_ddns_http_code	HTTP response code
sensor.godaddy_ddns_http_status	Human-readable HTTP status
sensor.godaddy_ddns_last_message	Last API/update message
Button
Entity	Description
button.godaddy_ddns_force_update	Force immediate update
Installation
HACS Installation
Add Custom Repository

In HACS:

Open HACS
Integrations
Click the three dots in the upper-right
Select:
Custom repositories

Add:

https://github.com/YOUR_GITHUB_USERNAME/homeassistant-godaddy-ddns-ipv6

Category:

Integration

Install the integration.

Restart Home Assistant.

Manual Installation

Copy:

custom_components/godaddy_ddns_ipv6

to:

/config/custom_components/godaddy_ddns_ipv6

Restart Home Assistant.

Setup

Go to:

Settings → Devices & Services → Add Integration

Search:

GoDaddy DDNS IPv6

Enter:

GoDaddy API Key
GoDaddy API Secret
Domain
Record Name
Interface
TTL
Update Interval
GoDaddy API Key

Create API credentials here:

GoDaddy Developer Portal

Production API endpoint used:

https://api.godaddy.com
Record Name Examples
Root Domain

Use:

@

Example:

example.com
Subdomain

Use:

home

Example:

home.example.com
Example Configuration
Setting	Example
Domain	example.com
Record Name	home
Interface	end0
TTL	600
Update Interval	60
HTTP Status Examples
Code	Meaning
200	OK
400	Bad Request
401	Unauthorized
403	Forbidden
404	Not Found
422	Invalid Record
429	Rate Limited
500	Server Error
Notes
IPv6 Change Detection

The integration only updates GoDaddy when the IPv6 address changes.

This minimizes unnecessary API calls.

Home Assistant Restart

Configuration changes generally apply immediately.

Some update interval changes may require a Home Assistant restart.

Troubleshooting
No Global IPv6 Found

Verify:

IPv6 is enabled
Selected interface is correct
Interface has a global IPv6 address

Check:

Settings
System
Network
Unauthorized / 401

Verify:

API Key
API Secret
Wrong IPv6 Address

Verify the correct interface is selected:

end0
wlan0
etc.
Force Update

Use:

button.godaddy_ddns_force_update

to manually trigger an update.

Future Improvements

Planned ideas:

IPv4 support
Multiple record support
Multiple domains
Diagnostics download
Device info page
Immediate option reload without restart
Auto-select preferred interface
Update history tracking
Notification support
License

MIT License

Disclaimer

This project is not affiliated with or endorsed by GoDaddy.
