def render_use_of_total(in_use: float, *, total: int) -> str:
    return f"{in_use:.0f} of {total}"


def render_days(days: int) -> str:
    return f"{days} days"
