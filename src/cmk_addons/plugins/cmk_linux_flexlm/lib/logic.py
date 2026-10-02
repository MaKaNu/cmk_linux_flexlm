import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime


@dataclass(frozen=True)
class LicenseFeature:
    feature: str
    in_use: int
    total: int
    expires: date | None


def parse_string_table(rows: Sequence[Sequence[str]]) -> list[LicenseFeature]:
    features = []

    for row in rows:
        if not row:
            continue

        data = json.loads(" ".join(row))
        features.append(
            LicenseFeature(
                feature=data["feature"],
                in_use=int(data["in_use"]),
                total=int(data["total"]),
                expires=(
                    date.fromisoformat(data["expires"])
                    if data["expires"] is not None
                    else None
                ),
            )
        )
    return features


LEGACY_DATE_FORMAT = "%d-%b-%Y"


def parse_legacy_string_table(rows: Sequence[Sequence[str]]) -> list[LicenseFeature]:
    """Parse rows of the form: <feature> <in_use> <total> <dd-Mon-YYYY|None>."""
    features = []

    for row in rows:
        if not row:
            continue

        feature, in_use, total, expires = row
        features.append(
            LicenseFeature(
                feature=feature,
                in_use=int(in_use),
                total=int(total),
                expires=(
                    None
                    if expires == "None"
                    else datetime.strptime(expires, LEGACY_DATE_FORMAT)
                    .replace(tzinfo=UTC)
                    .date()
                ),
            )
        )
    return features
