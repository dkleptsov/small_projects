""" Test module of check_inoagent module"""
import pickle
import csv
from .check_inoagent import check_all_patterns
from .check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"
RESULTS_FILE = "autotest_db/results_all_patterns_db.pkl"

with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(RESULTS_FILE, "rb") as pkl_file:
    old_results = pickle.load(pkl_file, encoding="utf-8")

new_results = {}

# Testing check_all_patterns function
def test_inoagent_list() -> None:
    """Results of check_all_patterns on list of inoagents should be the same."""
    assert check_all_patterns(inoagent_list) == old_results["inoagent_list_all"]

# def test_inoagent_list_timing() -> None:
#     assert 1 == 0

def test_lenta_full() -> None:
    """Results of check_all_patterns on whole lenta should be the same."""
    new_results["inoagent_list_all"] = check_all_patterns(inoagent_list)
    for news in lenta:
        result = check_all_patterns(news[2], verbose=True)
        if len(new_results) > 0:
            new_results[f"{news[0]}"] = result
    assert new_results == old_results

def test_empty_string() -> None:
    """Result of empty string should be empty dictionary."""
    assert check_all_patterns("") == {}

def test_random_string() -> None:
    """Result of random string should be empty dictionary."""
    assert check_all_patterns("выаолвыр адавордлоавр") == {}

# # Call regex on other texts
# def test_single_pattern() -> None:
#     """Result of random string should be empty dictionary."""
#     assert 1 == 0

# # Test telegram bot