from typing import Any
from babel.numbers import format_currency, format_decimal


def to_float(input_value: Any) -> float:
    try:
        return float(input_value)  # type: ignore
    except ValueError:
        return False


def is_int(value: Any) -> bool:
    """
    use `isinstance(value, int)` not work for case value is `False`
    """
    return type(value) is int


def is_float(value: Any) -> bool:
    return type(value) is float


def formatNumber(
    value: int | float | str, format: str | None = None, locale: str = "vi_VN"
) -> str:
    return format_decimal(value, format, locale)


def formatCurrency(
    value: int | float | str, currency: str = "VND", locale: str = "vi_VN"
) -> str:
    return format_currency(value, currency=currency, locale=locale)
