from datetime import date

from cmk_addons.plugins.cmk_linux_flexlm.lib.logic import (
    LicenseFeature,
    parse_legacy_string_table,
    parse_string_table,
)


def test_parse_json_string_table_rows():
    rows = [
        ['{"feature":', '"MATLAB","in_use":3,"total":10,"expires":"2026-12-31"}'],
        ['{"feature":"Other","in_use":0,"total":5,"expires":null}'],
    ]

    assert parse_string_table(rows) == [
        LicenseFeature("MATLAB", 3, 10, date(2026, 12, 31)),
        LicenseFeature("Other", 0, 5, None),
    ]


def test_parse_legacy_string_table_rows():
    rows = [
        ["MATLAB", "3", "10", "31-Dec-2026"],
        ["Other", "0", "5", "None"],
    ]

    assert parse_legacy_string_table(rows) == [
        LicenseFeature("MATLAB", 3, 10, date(2026, 12, 31)),
        LicenseFeature("Other", 0, 5, None),
    ]
