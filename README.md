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

Login into your site and provide the mkp file (for example via scp).

```bash
mkp add cmk_linux_flexlm-1.0.1.mkp
mkp activate cmk_linux_flexlm
```

Copy the agent based plugin to the monitored flexlm server.

- Location on site:
  - `local/share/check_mk/agents/plugins/cmk_linux_flexlm.py`
- Target location on flexlm server:
  - `/usr/lib/check_mk_agent/plugins/cmk_linux_flexlm.py`

Run service discovery and accept the deteced services, one for each feature.

Create Service rules and apply them via service label to different amounts of feature licesnes.
