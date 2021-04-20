import csv
import time
import pickle
import seaborn as sns
from pprint import pprint
import settings
from check_lenta import get_results
from check_lenta import check_line


def sort_dict(dict2sort) -> dict:
    sorted_list = []
    for key, value in dict2sort.items():
        sorted_list.append((key, len(value)))
    sorted_list.sort(key=lambda x:x[1], reverse=True)
    sorted_dict = {}
    for k, _ in sorted_list:
        sorted_dict[k] = dict2sort[k]
    return sorted_dict


def print_stats(path=settings.RESULTS_NEW) -> None:
    """Function to print basic stats about results."""
    with open(path, "rb") as pkl_file:
        results = pickle.load(pkl_file, encoding="utf-8")
    results = sort_dict(results)
    for key, value in results.items():
        if len(value) > 0:
            print(f"Pattern: {key} Quantity: {len(value)}")

    keys = [k for k in results.keys() if len(results[k]) > 0]
    vals = [len(results[k]) for k in keys]
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


def normal_vs_extended(path=settings.RESULTS_NEW) -> dict:
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
    return only_in_normal, only_in_extended


def print_result(list2print:list) -> None:
    for _, value in list2print:
        print(f"Text: {value['text_found']}            url: {value['url']}")
        name = value['name']
    print(f"Name: {name}")


def old_vs_new(old_path = settings.RESULTS,
               new_path = settings.RESULTS_NEW) -> None:
    with open(old_path, "rb") as pkl_file:
        old = pickle.load(pkl_file)
    with open(new_path, "rb") as pkl_file:
        new = pickle.load(pkl_file)
    
    if old == new:
        print("Old and new results are identical!")
    
    for key in set(list(old.keys()) + list(new.keys())):           
        only_in_old, only_in_new = dict_compare(old.get(key), new.get(key))
        if only_in_old != []:
            print(f"\n********* Deleted in {key}: *********")
            print_result(only_in_old)
        if only_in_new != []:
            print(f"\n********* Added in {key}: *********")
            print_result(only_in_new)
    return only_in_old, only_in_new


def check_one_new(num, old_path = settings.RESULTS) -> None:
    with open(settings.INOAGENT_LIST, "r", encoding="utf-8") as text_file:
        inoagent_list_str = text_file.read()    
    with open(settings.LENTA_FILE, "r", encoding="utf-8") as lnt_file:
        lenta = list(csv.reader(lnt_file, delimiter=','))
    with open(settings.PATTERNS_DB, encoding="utf-8") as patterns_file:
        pattern_lines = list(csv.reader(patterns_file, delimiter=';'))[1:]
    with open(old_path, "rb") as pkl_file:
        old = pickle.load(pkl_file)

    inoagent_line = [settings.INOAGENT_LIST, "Список иностранных агентов", 
                     inoagent_list_str, "", "", ""]
    lenta.append(inoagent_line)
    print(f"Name of inoagent       {pattern_lines[num][2]}")
    print(f"Normal pattern         {pattern_lines[num][1]}")
    print(f"Extended pattern       {pattern_lines[num][0]}")
    print(f"Row in CSV file        {num+2}")
    print("New results:")
    args = [num, pattern_lines[num], lenta]
    new_results = check_line(args)
    pprint(new_results)

    old_results ={}
    old_results[f"normal_{num}"] = old.get(f"normal_{num}")
    old_results[f"extended_{num}"] = old.get(f"extended_{num}")
    pprint(old_results)

def compare_url(dict_1, dict_2) -> None:
    pprint(dict_1)


def main():
    start = time.perf_counter()
    # get_results(settings.RESULTS_NEW)
    # print_stats(settings.RESULTS)
    # normal_vs_extended()
    # old_vs_new()
    check_one_new(45)
    print(f"It took {time.perf_counter()-start:.2f} seconds!")


if __name__ == "__main__":
    main()

