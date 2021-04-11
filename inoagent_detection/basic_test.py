""" Test module of check_inoagent module"""
import os
import sys
import csv
from tqdm import tqdm
import pickle
from pprint import pprint # pprint(dict)
sys.path.insert(0, os.getcwd())
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"

RESULTS_ALL_PTNS = "autotest_db/results_all_patterns_db.pkl"
RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db.pkl"

FBK = {0: {'date': '09.10.2019',
     'excluded': 'FALSE',
     'inoagent_type': 'НКО',
     'name': 'Некоммерческая организация "Фонд борьбы с коррупцией"',
     'org_type': 'Юридической лицо',
     'span': [0, 24],
     'text_found': 'Фонд борьбы с коррупцией'}}

with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))

with open(RESULTS_ALL_PTNS, "rb") as pkl_file:
    old_results_all = pickle.load(pkl_file, encoding="utf-8")

with open(RESULTS_SEP_PTNS, "rb") as pkl_file:
    old_results_sep = pickle.load(pkl_file, encoding="utf-8")


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

def test_inoagent_list() -> None:
    """Test if checking inoagent list works."""
    assert check_all_patterns(inoagent_list) == old_results_all["inoagent_list_all"]
