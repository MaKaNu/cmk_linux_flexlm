import datetime
from functools import partial
from typing import Any

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
    check_levels,
)

from cmk_addons.plugins.cmk_linux_flexlm.lib.logic import (
    LicenseFeature,
    parse_legacy_string_table,
    parse_string_table,
)
from cmk_addons.plugins.cmk_linux_flexlm.lib.render import (
    render_days,
    render_use_of_total,
)

# ------------------------------------------------------------------------------
# Section Parser
# ------------------------------------------------------------------------------


def parse_cmk_linux_flexlm(string_table: StringTable) -> list[LicenseFeature]:
    return parse_string_table(string_table)


# Legacy Parser
def parse_lnx_flexlm(string_table: StringTable) -> list[LicenseFeature]:
    return parse_legacy_string_table(string_table)


# Both sections publish the same parsed section, so one check handles either agent.
agent_section_cmk_linux_flexlm = AgentSection(
    name="cmk_linux_flexlm",
    parse_function=parse_cmk_linux_flexlm,
)

# Legacy agent output: whitespace separated rows
agent_section_lnx_flexlm = AgentSection(
    name="lnx_flexlm",
    parsed_section_name="cmk_linux_flexlm",
    parse_function=parse_lnx_flexlm,
)


def discover_cmk_linux_flexlm(section: list[LicenseFeature]) -> DiscoveryResult:
    if not section:
        return
    yield Service()


def check_cmk_linux_flexlm(
    params: dict[str, Any], section: list[LicenseFeature]
) -> CheckResult:
    if not section:
        yield Result(state=State.UNKNOWN, summary="No license features detected")
        return

    for feature in section:
        if feature.expires is not None:
            days_left = (
                feature.expires - datetime.datetime.now(tz=datetime.UTC).date()
            ).days
            yield from check_levels(
                days_left,
                levels_lower=params["levels_expiry"],
                label=f"{feature.feature} expires in (days)",
                render_func=render_days,
            )

        yield from check_levels(
            feature.in_use,
            levels_upper=params["levels_upper"],
            metric_name=f"{feature.feature}_licenses",
            label=f"{feature.feature} in use",
            boundaries=(0, feature.total),
            render_func=partial(render_use_of_total, total=feature.total),
        )


check_plugin_cmk_linux_flexlm = CheckPlugin(
    name="cmk_linux_flexlm",
    sections=["cmk_linux_flexlm"],
    service_name="FlexLM License Status",
    discovery_function=discover_cmk_linux_flexlm,
    check_function=check_cmk_linux_flexlm,
    check_ruleset_name="cmk_linux_flexlm",
    check_default_parameters={
        "levels_upper": ("no_levels", None),
        "levels_expiry": ("fixed", (30, 5)),
    },
)
