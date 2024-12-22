import pytest

from python_package_template.template import template_function


@pytest.mark.parametrize("value,expected", [(0, "The value is less then 1"),
                                            (3, "The value is less then 4")])
def test_template_function(value: int, expected: str):
    assert template_function(value) == expected


def test_template_function_invalid_input():
    with pytest.raises(ValueError):
        template_function(-1)
