from typing import Any, TypeVar

T = TypeVar("T")


def is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def get(dict: dict[str, Any], keys: list[str], defaultValue: Any = None) -> Any:
    """
    Retrieves a nested value from a dictionary using a list of keys.

    :param dict: The dictionary to retrieve the value from.
    :param keys: A list of keys representing the path to the desired value.
    :param defaultValue: The value to return if the specified path does not
                         exist in the dictionary. Defaults to None.
    :return: The value found at the specified path or the defaultValue if
             the path does not exist.
    """
    result = dict
    for key in keys:
        result = result.get(key) if result else None
    return result or defaultValue


def gets(dict: dict[str, T], keys: list[str]) -> dict[str, T]:
    result = {}
    for key in keys:
        result[key] = dict.get(key)
    return result


# def get(dict: dict[str, Any], keys: list[str], defaultValue: Any = None) -> Any:
#     result = dict
#     for key in keys:
#         result = result.get(key) if result else None
#     return result or defaultValue
