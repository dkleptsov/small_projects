""" Test module of check_inoagent module"""
import os
import sys
import pickle
import pytest
sys.path.insert(0, os.getcwd())
from get_new_results import get_all_patterns_results
from get_new_results import get_sep_patterns_results

RESULTS_ALL_PTNS = "autotest_db/results_all_patterns_db.pkl"
RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db.pkl"

with open(RESULTS_ALL_PTNS, "rb") as pkl_file:
    old_results_all = pickle.load(pkl_file, encoding="utf-8")

with open(RESULTS_SEP_PTNS, "rb") as pkl_file:
    old_results_sep = pickle.load(pkl_file, encoding="utf-8")

new_results_all = get_all_patterns_results(load_old=False)
new_results_sep = get_sep_patterns_results(load_old=False)

# Testing all patterns results
def test_results_all_keys() -> None:
    """Check if old and new results have the same keys."""
    assert old_results_all.keys() == new_results_all.keys()

value_tuples = []
for key in old_results_all:
    value_tuples.append((old_results_all.get(key), new_results_all.get(key)))

@pytest.mark.parametrize("old_result, new_result", value_tuples)
def test_results_all_values(old_result, new_result):
    assert old_result == new_result

# Testing each pattern separately
def test_results_sep_keys() -> None:
    """Check if old and new results have the same keys."""
    assert old_results_sep.keys() == new_results_sep.keys()

value_tuples = []
for key in old_results_sep:
    value_tuples.append((old_results_sep.get(key), new_results_sep.get(key)))

@pytest.mark.parametrize("old_result, new_result", value_tuples)
def test_results_sep_values(old_result, new_result):
    assert old_result == new_result
