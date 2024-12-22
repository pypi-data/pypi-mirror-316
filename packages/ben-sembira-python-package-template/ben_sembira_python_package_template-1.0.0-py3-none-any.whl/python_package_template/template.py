def template_function(value: int) -> str:
    if value < 0:
        raise ValueError(
            f"value can only be a non-negative integer. Got {value=}")
    return f"The value is less then {value + 1}"
