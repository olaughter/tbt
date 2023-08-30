import logging

import pytest

from tbt.utils import camel_to_snake, log_details


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


def test_log_details_info(caplog):
    @log_details
    def test_func(arg):
        return arg

    arg = "values should pass through decorator"
    with caplog.at_level(logging.INFO):
        returned_value = test_func(arg=arg)
    assert returned_value == arg
    assert caplog.text != ""


def test_log_details_warning(caplog):
    @log_details
    def test_func():
        pass

    with caplog.at_level(logging.WARNING):
        test_func()
    assert caplog.text == ""
