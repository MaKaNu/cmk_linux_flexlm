# /usr/bin/env python3

import json
import os
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path

FEATURE_PATTERN = re.compile(
    (
        r"^Users of (?P<feature>\S+):\s+\(Total of (?P<total>\d+) licenses? issued;"
        r"\s+Total of (?P<in_use>\d+) licenses? in use"
        r"(?:;\s+.*EXPIRES\s+(?P<expires>\S+))?"
    ),
    re.IGNORECASE,
)

TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class LicenseFeature:
    feature: str
    in_use: int
    total: int
    expires: date | None

    def as_json(self) -> str:
        """Return the instance as a single JSON line string."""
        return json.dumps(asdict(self))


def exec_get_running_units() -> list[str]:
    """Finds lmutil path by discovering running systemd services that executes lmgrd."""
    res = subprocess.run(
        [
            "systemctl",
            "list-units",
            "--type=service",
            "--state=running",
            "--no-legend",
            "--no-pager",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return res.stdout.splitlines()


def exec_get_execstart_units(unit_name: str) -> str:
    res = subprocess.run(
        ["systemctl", "show", unit_name, "--property=ExecStart"],
        capture_output=True,
        text=True,
        check=True,
    )

    return res.stdout


def find_lmutil_via_systemd() -> str | None:
    for line in exec_get_running_units():
        parts = line.split()
        if not parts:
            continue

        unit_name = parts[0]

        unit_with_exec_start = exec_get_execstart_units(unit_name)

        if not "lmgrd" in unit_with_exec_start:
            continue

        match = re.search(r"path=([\S;]+)", unit_with_exec_start)
        if not match:
            continue
        lmgrd_path = Path(match.group(1))
        lmgrd_dir = lmgrd_path.parent
        candidate = lmgrd_dir / "lmutil"

        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)


def create_feature_from_match(match: re.Match) -> LicenseFeature:
    groups = match.groupdict(default="")
    expires = groups["expires"]

    feature = LicenseFeature(
        feature=groups["feature"],
        in_use=int(groups["in_use"]),
        total=int(groups["total"]),
        expires=(
            datetime.strptime(expires, "%s-%b-%Y").replace(tzinfo=UTC).date()
            if expires
            else None
        ),
    )
    return feature


def extract_features(stdout_lines: list[str]) -> str:
    json_lines = []
    for line in stdout_lines:
        match = re.match(FEATURE_PATTERN, line)

        if match:
            json_lines.append(create_feature_from_match(match).as_json())

    return "\n".join(json_lines)


def read_all_license_features(lmutil_bin: str) -> str:
    res = subprocess.run(
        [lmutil_bin, "lmstat", "-a"], capture_output=True, text=True, check=True
    )

    jsonl = extract_features(res.stdout.splitlines())

    return jsonl


def main() -> None:
    print("<<<cmk_linux_flexlm>>>")
    lmutil = find_lmutil_via_systemd()
    if not lmutil:
        raise RuntimeError("lmutil not found!")
    print(read_all_license_features(lmutil))


if __name__ == "__main__":
    main()
