from .common import (is_last_index)

# test case for is_last_index function
def test_is_last_index() -> None:
    assert is_last_index([1], 2) is True
    print("Test passed!")
