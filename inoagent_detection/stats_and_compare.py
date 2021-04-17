import csv
from tqdm import tqdm
import pickle
import seaborn as sns
# import pandas as pd
# import numpy as np
from pprint import pprint
from time import time
from get_new_results import get_all_patterns_results
from get_new_results import get_sep_patterns_results

RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db_new.pkl"
RESULTS_SEP_PTNS_NEW = "autotest_db/results_separate_patterns_db_new.pkl"


def sort_dict(dict2sort) -> dict:
    sorted_list = []
    for key, value in dict2sort.items():
        sorted_list.append((key, len(value)))
    sorted_list.sort(key=lambda x:x[1], reverse=True)
    sorted_dict = {}
    for k, _ in sorted_list:
        sorted_dict[k] = dict2sort[k]
    return sorted_dict


def print_stats(path=RESULTS_SEP_PTNS_NEW) -> None:
    """Function to print basic stats about results."""
    with open(path, "rb") as pkl_file:
        results_sep = pickle.load(pkl_file, encoding="utf-8")
    results_sep = sort_dict(results_sep)
    for key, value in results_sep.items():
        if len(value) > 0:
            print(f"Pattern: {key} Quantity: {len(value)}")

    keys = [k for k in results_sep.keys() if len(results_sep[k]) > 0]
    vals = [len(results_sep[k]) for k in keys]
    sns.set_style("darkgrid")
    sns_plot = sns.barplot(x=keys, y=vals)
    sns_plot.set_xticklabels(sns_plot.get_xticklabels(),rotation=90,ha='right')
    sns_plot.figure.set_figwidth(18)
    sns_plot.figure.set_figheight(10)
    sns_plot.figure.savefig("autotest_db/results_chart.png")


def dict_compare(dict_1: dict, dict_2:dict) -> list:
    """Fuction to compare two dictionaries"""
    only_in_1, only_in_2 = [], []
    if dict_1 == dict_2:
        return only_in_1, only_in_2
    
    if dict_1 == None:
        return [], dict_2
    elif dict_2 == None:
        return dict_1, []

    for item in dict_1.items():
        if item not in dict_2.items():
            only_in_1.append(item)

    for item in dict_2.items():
        if item not in dict_1.items():
            only_in_2.append(item)
    return only_in_1, only_in_2

def normal_vs_extended(path=RESULTS_SEP_PTNS_NEW) -> None:
    """Function to compare results of normal and extended mode"""
    with open(path, "rb") as pkl_file:
        results = pickle.load(pkl_file, encoding="utf-8")
    
    for i in range(len(results.keys())//2):
        only_in_normal, only_in_extended = dict_compare(
            results.get(f"normal_{i}"), results.get(f"extended_{i}"))
        if only_in_normal != []:
            print(f"\n********* Only in normal_{i}: *********")
            print_result(only_in_normal)
        if only_in_extended != []:
            print(f"\n********* Only in extended_{i}: *********")
            print_result(only_in_extended)


def print_result(list2print:list) -> None:
    for _, value in list2print:
        print(f"Text: {value['text_found']}            url: {value['url']}")
        name = value['name']
    print(f"Name: {name}")

def old_vs_new(old_path = "autotest_db/results_separate_patterns_db.pkl",
               new_path = "autotest_db/results_separate_patterns_db_new.pkl"):
    with open(old_path, "rb") as pkl_file:
        old = pickle.load(pkl_file, encoding="utf-8")
    with open(new_path, "rb") as pkl_file:
        new = pickle.load(pkl_file, encoding="utf-8")
    
    for key in set(list(old.keys()) + list(new.keys())):           
        only_in_old, only_in_new = dict_compare(old.get(key), new.get(key))
        if only_in_old != []:
            print(f"\n********* Deleted in {key}: *********")
            print_result(only_in_old)
        if only_in_new != []:
            print(f"\n********* Added in {key}: *********")
            print_result(only_in_new)    


def test_regex() -> None:
    pass


def main():
    start = time()
    get_sep_patterns_results(RESULTS_SEP_PTNS_NEW, load_old=False)
    # print_stats(RESULTS_SEP_PTNS)
    # normal_vs_extended()
    # old_vs_new()
    print(f"It took {time()-start} seconds!")

if __name__ == "__main__":
    main()
