""" This script creates databese for auto testing of check_inoagent """
import os
import sys
import csv
import pickle
from tqdm import tqdm
# sys.path.insert(0, os.getcwd())
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"
RESULTS_ALL_PTNS_NEW = "autotest_db/results_all_patterns_db_new_2.pkl"
RESULTS_SEP_PTNS_NEW = "autotest_db/results_separate_patterns_db_new_2.pkl"
VERBOSITY = False

with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))


def get_all_patterns_results(load_old=False) -> dict:
    if load_old:
        with open(RESULTS_ALL_PTNS_NEW, "rb") as pkl_file:
            new_results_all = pickle.load(pkl_file, encoding="utf-8")
        return new_results_all
    
    new_results_all: dict = {}
    new_results_all["inoagent_list_all"] = check_all_patterns(inoagent_list)
    for news in tqdm(lenta):
        news_text, news_url = news[2], news[0]
        results = check_all_patterns(news_text, verbose=VERBOSITY)
        if len(results) > 0:
            new_results_all[f"{news_url}"] = results
    with open(RESULTS_ALL_PTNS_NEW,'wb') as pkl_file:
        pickle.dump(new_results_all, pkl_file)
    return new_results_all


def get_sep_patterns_results(load_old=False) -> dict:
    if load_old:
        with open(RESULTS_SEP_PTNS_NEW, "rb") as pkl_file:
            new_results_all = pickle.load(pkl_file, encoding="utf-8")
        return new_results_all
    new_results_sep: dict = {}
    for i, pattern in tqdm(enumerate(patterns)):
        normal_pattern, extended_pattern = pattern[1], pattern[0]
        for news in lenta:
            news_text, news_url = news[2], news[0]
            new_results_sep[f"normal_{i}"] = [x for x in check_single_pattern(
                news_text, normal_pattern, name=news_url, verbose=VERBOSITY)]    
            new_results_sep[f"extended_{i}"]=[x for x in check_single_pattern(
                news_text, extended_pattern, name=news_url, verbose=VERBOSITY)]
    with open(RESULTS_SEP_PTNS_NEW,'wb') as pkl_file:
        pickle.dump(new_results_sep, pkl_file)
    return new_results_sep
