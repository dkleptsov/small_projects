""" This script creates databese for auto testing of check_inoagent """
import csv
import time
import pickle
from tqdm import tqdm
import concurrent.futures
from pprint import pprint
from check_inoagent import check_single_pattern


def check_line(args) -> dict:
    """Function check whole lenta with single pattern. """
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


def get_results(results_path: str, load_old=False) -> dict:
    """Function to check whole lenta with each pattern. Needed for testing. """
    if load_old:
        with open(results_path, "rb") as pkl_file:
            new_results = pickle.load(pkl_file, encoding="utf-8")
        return new_results    

    INOAGENT_LIST = "autotest_db/text_to_search.txt"
    LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
    PATTERNS_DB = "patterns_db.csv"

    with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
        inoagent_list_str = text_file.read()    
    with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
        lenta = list(csv.reader(lnt_file, delimiter=','))
    with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
        pattern_lines = list(csv.reader(patterns_file, delimiter=';'))[1:]

    inoagent_line = [INOAGENT_LIST, "Список иностранных агентов", 
                     inoagent_list_str, "", "", ""]
    lenta.append(inoagent_line)

    args = [(i, line, lenta) for i, line in enumerate(pattern_lines)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(check_line, args)
    
    new_results: dict = {}
    for result in results:
        new_results.update(result)

    with open(results_path,'wb') as pkl_file:
        pickle.dump(new_results, pkl_file)
    return new_results


def main():
    start = time.perf_counter()
    get_results("autotest_db/results_db.pkl")
    print(f"It took {time.perf_counter() - start:.2f} seconds!")


if __name__ == "__main__":
    main()
