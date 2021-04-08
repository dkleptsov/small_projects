""" An example of a test module in pytest. """

from pytest_dojo.code import total, join

def test_total_empty() -> None:
    """Total of empty list should be zero."""
    assert total([]) == 0.0

def test_total_single_item() -> None:
    """Total of single item list should be value of this single item. """
    assert total([110.0]) == 110.0

def test_total_many_items() -> None:
    """Total of a list with many items should be sum of items values. """
    assert total([-1.0, 6, 0.003]) == 5.003

def test_join_many_items() -> None:
    """Join of many items should be string of concatenated items"""
    assert join([-1, 2, 0], ", ") == "-1, 2, 0"

def test_join_one_item() -> None:
    """Join of one item should string of this one item"""
    assert join([16], "t") == "16"

def test_join_empty() -> None:
    """Join of empty list should empty string """
    assert join([], "") == ""

