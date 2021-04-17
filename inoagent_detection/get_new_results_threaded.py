""" This script creates databese for auto testing of check_inoagent """
import os
import sys
import csv
import pickle
from tqdm import tqdm
import concurrent.futures
# from pprint import pprint
# sys.path.insert(0, os.getcwd())
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern


def check_line(args) -> dict:
    normal_pattern, extended_pattern = args[1][1], args[1][0]
    inoagent_name = args[1][2]   
    results_line, i = {}, args[0]
    results_line[f"normal_{i}"], results_line[f"extended_{i}"] = {}, {}
    num_results_normal = 0
    num_results_extended = 0

    for news in args[2]:
        news_text, news_url = news[2], news[0]
        for result in check_single_pattern(news_text, normal_pattern):
            result["url"] = news_url
            result["name"] = inoagent_name
            results_line[f"normal_{i}"][num_results_normal] = result
            num_results_normal += 1
        for result in check_single_pattern(news_text, extended_pattern):
            result["url"] = news_url
            result["name"] = inoagent_name
            results_line[f"extended_{i}"][num_results_extended] = result
            num_results_extended += 1
    return results_line


def get_sep_patterns_results(results_path: str, load_old=False) -> dict:
    INOAGENT_LIST = "autotest_db/text_to_search.txt"
    LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
    PATTERNS_DB = "patterns_db.csv"

    if load_old:
        with open(results_path, "rb") as pkl_file:
            new_results = pickle.load(pkl_file, encoding="utf-8")
        return new_results

    with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
        lenta = list(csv.reader(lnt_file, delimiter=','))
    with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
        pattern_lines = list(csv.reader(patterns_file, delimiter=';'))

    new_results: dict = {}
    args = [(i+1, line, lenta) for i, line in enumerate(pattern_lines)]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(check_line, args)

    for result in results:
        new_results.update(result)
    print(new_results)

    # for i, line in tqdm(enumerate(pattern_lines[1:])):
    #     normal_pattern, extended_pattern = line[1], line[0]
    #     inoagent_name = line[2]
    #     new_results_sep[f"normal_{i}"] = {}
    #     new_results_sep[f"extended_{i}"] = {}
 
    #     num_results_normal = 0
    #     num_results_extended = 0
    #     for news in lenta:
    #         news_text, news_url = news[2], news[0]
    #         for result in check_single_pattern(news_text, normal_pattern):
    #             result["url"] = news_url
    #             result["name"] = inoagent_name
    #             new_results_sep[f"normal_{i}"][num_results_normal] = result
    #             num_results_normal += 1
    #         for result in check_single_pattern(news_text, extended_pattern):
    #             result["url"] = news_url
    #             result["name"] = inoagent_name
    #             new_results_sep[f"extended_{i}"][num_results_extended] = result
    #             num_results_extended += 1



    with open(results_path,'wb') as pkl_file:
        pickle.dump(new_results, pkl_file)
    return new_results


def main():
    get_sep_patterns_results("autotest_db/results_db_new.pkl")

    # with open("autotest_db/results_separate_patterns_db.pkl", "rb") as pkl_file:
    #     new_results_all = pickle.load(pkl_file, encoding="utf-8")
    # pprint(new_results_all)


if __name__ == "__main__":
    main()
