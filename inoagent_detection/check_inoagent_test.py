""" Test module of check_inoagent module"""
import csv
import pickle
import pytest
from tqdm import tqdm
# import pprint # pprint.pprint(dict)
from .check_inoagent import check_all_patterns
from .check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"
RESULTS_ALL_PTNS = "autotest_db/results_all_patterns_db.pkl"
RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db.pkl"
RESULTS_ALL_PTNS_NEW = "autotest_db/results_all_patterns_db_new_2.pkl"
RESULTS_SEP_PTNS_NEW = "autotest_db/results_separate_patterns_db_new_2.pkl"
VERBOSITY = False
RECALCULATE = False # Переделать расчеты в функции и звать их

with open(RESULTS_ALL_PTNS, "rb") as pkl_file:
    old_results_all = pickle.load(pkl_file, encoding="utf-8")

with open(RESULTS_SEP_PTNS, "rb") as pkl_file:
    old_results_sep = pickle.load(pkl_file, encoding="utf-8")

# with open(RESULTS_ALL_PTNS_NEW, "rb") as pkl_file:
#     new_results_all = pickle.load(pkl_file, encoding="utf-8")

# with open(RESULTS_SEP_PTNS_NEW, "rb") as pkl_file:
#     new_results_sep = pickle.load(pkl_file, encoding="utf-8")

# Getting new results from scratch
with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))

new_results_all: dict = {}
new_results_all["inoagent_list_all"] = check_all_patterns(inoagent_list)
for news in tqdm(lenta):
    results = check_all_patterns(news[2], verbose=VERBOSITY)
    if len(results) > 0:
        new_results_all[f"{news[0]}"] = results
with open(RESULTS_ALL_PTNS_NEW,'wb') as pkl_file:
    pickle.dump(new_results_all, pkl_file)

new_results_sep: dict = {}
for i, pattern in tqdm(enumerate(patterns)):
    normal_pattern, extended_pattern = pattern[1], pattern[0]
    for news in lenta:
        news_text, news_url = news[2], news[0]
        new_results_sep[f"normal_{i}"] = [x for x in check_single_pattern(news_text, 
                    normal_pattern, name=news_url, verbose=VERBOSITY)]    
        new_results_sep[f"extended_{i}"]=[x for x in check_single_pattern(news_text, 
                    extended_pattern, name=news_url, verbose=VERBOSITY)]
with open(RESULTS_SEP_PTNS_NEW,'wb') as pkl_file:
    pickle.dump(new_results_sep, pkl_file)


# Добавить сюда простые тесты, чтобы видеть прогресс?


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

# Testing of edge cases
def test_empty_string() -> None:
    """Result of empty string should be empty dictionary."""
    assert check_all_patterns("") == {}

def test_random_string() -> None:
    """Result of random string should be empty dictionary."""
    assert check_all_patterns("выаолвыр адавордлоавр") == {}

# # # Call regex on other texts
# # def test_single_pattern() -> None:
# #     """Result of random string should be empty dictionary."""
# #     assert 1 == 0

# # # Test telegram bot