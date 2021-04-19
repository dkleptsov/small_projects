""" Test module of check_inoagent module"""
import os
import sys
import csv
import pickle
import pytest
sys.path.insert(0, os.getcwd())
import settings
from check_lenta import get_results
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern


with open(settings.INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(settings.LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(settings.PATTERNS_DB, "r", encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))

with open(settings.RESULTS, "rb") as pkl_file:
    old_results = pickle.load(pkl_file, encoding="utf-8")

new_results = get_results(settings.RESULTS_NEW, load_old=True)


def test_empty_string() -> None:
    """Result of empty string should be empty dictionary."""
    assert check_all_patterns("") == {}


def test_random_string() -> None:
    """Result of random string should be empty dictionary."""
    assert check_all_patterns("выаолвыр адавордлоавр") == {}


def test_fbk() -> None:
    """This text should be detected as inoagent."""
    assert check_all_patterns("Фонд борьбы с коррупцией") == settings.FBK


def test_single_pattern() -> None:
    """Checking if regex even work."""
    for result in check_single_pattern("Лев Пономарев", 
    r"пономар\w{2,5}\s*\bл\w{2,4}\b|\bл\w{2,4}\s*пономар\w{2,5}"):
        assert result == {'span': [0, 13], 'text_found': 'Лев Пономарев'}


def test_results_keys() -> None:
    """Check if old and new results have the same keys."""
    assert old_results.keys() == new_results.keys()


value_tuples = []
for key in old_results:
    value_tuples.append((old_results.get(key), new_results.get(key)))


@pytest.mark.parametrize("old_result, new_result", value_tuples)
def test_zero_results_values(old_result, new_result):
    if len(new_result) == 0: print(new_result)
    assert len(new_result) > 0


@pytest.mark.parametrize("old_result, new_result", value_tuples)
def test_results_values(old_result, new_result):
    assert old_result == new_result


# def test_inoagent_list() -> None:
#     """Test if checking inoagent list works."""
#     assert check_all_patterns(inoagent_list) == old_results["inoagent_list_all"]

