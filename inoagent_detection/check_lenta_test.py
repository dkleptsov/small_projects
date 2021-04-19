""" Test module of check_inoagent module"""
import os
import sys
import csv
import pickle
import pytest
sys.path.insert(0, os.getcwd())
from check_lenta import get_results
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"

FBK = {0: {'date': '09.10.2019',
     'excluded': 'FALSE',
     'inoagent_type': 'НКО',
     'name': 'Некоммерческая организация "Фонд борьбы с коррупцией"',
     'org_type': 'Юридической лицо',
     'span': [0, 24],
     'text_found': 'Фонд борьбы с коррупцией'}}

RESULTS = "autotest_db/results_db.pkl"
RESULTS_NEW = "autotest_db/results_db.pkl"

with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))

with open(RESULTS, "rb") as pkl_file:
    old_results = pickle.load(pkl_file, encoding="utf-8")

new_results = get_results(RESULTS_NEW, load_old=True)


def test_empty_string() -> None:
    """Result of empty string should be empty dictionary."""
    assert check_all_patterns("") == {}


def test_random_string() -> None:
    """Result of random string should be empty dictionary."""
    assert check_all_patterns("выаолвыр адавордлоавр") == {}


def test_fbk() -> None:
    """This text should be detected as inoagent."""
    assert check_all_patterns("Фонд борьбы с коррупцией") == FBK


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
def test_results_values(old_result, new_result):
    assert old_result == new_result


# def test_inoagent_list() -> None:
#     """Test if checking inoagent list works."""
#     assert check_all_patterns(inoagent_list) == old_results["inoagent_list_all"]