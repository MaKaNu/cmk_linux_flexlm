from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_cmk_linux_flexlm():
    return Dictionary(
        elements={
            "levels_upper": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper levels for licenses in use"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                ),
            ),
            "levels_expiry": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Lower levels for license expiry (days remaining)"),
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=InputHint(value=(30, 5)),
                ),
            ),
        }
    )


rule_spec_cmk_linux_flexlm = CheckParameters(
    name="cmk_linux_flexlm",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_form_cmk_linux_flexlm,
    title=Title("Linux FlexLM License Status"),
)
