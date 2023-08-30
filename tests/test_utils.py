import logging

import pytest

from tbt.utils import camel_to_snake


@pytest.mark.parametrize(
    "value,expected",
    [
        ("Camel", "camel"),
        ("CamelCase", "camel_case"),
        ("CamelCaseTest", "camel_case_test"),
        ("CamelCaseTest123", "camel_case_test123"),
    ]
)
def test_camel_to_snake(value, expected):
    got = camel_to_snake(value)
    assert got == expected, f"Expected {expected}, got {got}"

