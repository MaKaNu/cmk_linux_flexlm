# CheckMK Linux FlexLM Plugin

Monitors FlexLM license feature usage and reports the number of licenses in use
and their total, along with license expiry dates.

## Prerequisites on the license server

- A Linux FlexLM license server with `lmutil` installed.
- The path to lmutil will either be determined by systemd service or via PATH variable.
- The Checkmk Linux agent must be able to run `lmutil lmstat -a` and
  `lmutil lmstat -i`.
- Checkmk 2.5.0p6 or newer.


## Installation of the MKP

MKP installation and packaging instructions are not available yet; the
installation logic has not been implemented.
