""" This script creates databese for auto testing of check_inoagent """
from check_inoagent_test import LENTA_FILE
import csv
import time
import pickle
from tqdm import tqdm
from check_inoagent import check_all_patterns
from check_inoagent import check_single_pattern

INOAGENT_LIST = "autotest_db/text_to_search.txt"
LENTA_FILE = "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv"
PATTERNS_DB = "patterns_db.csv"
RESULTS_ALL_PTNS = "autotest_db/results_all_patterns_db.pkl"
RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db.pkl"

with open(INOAGENT_LIST, "r", encoding="utf-8") as text_file:
    inoagent_list = text_file.read()

with open(LENTA_FILE, "r", encoding="utf-8") as lnt_file:
    lenta = list(csv.reader(lnt_file, delimiter=','))

results_db = {}

## Create results for all patterns together
# results_db["inoagent_list_all"] = check_all_patterns(inoagent_list)

# start = time.time()
# for news in tqdm(lenta):
#     results = check_all_patterns(news[2], verbose=True)
#     if len(results) > 0:
#         results_db[f"{news[0]}"] = results
# print(f"Checking all lenta took:{time.time() - start} seconds.")

# with open(RESULTS_ALL_PTNS,'wb') as pkl_file:
#     pickle.dump(results_db, pkl_file)

# Create results for lenta for each pattern separately
with open(PATTERNS_DB, encoding="utf-8") as patterns_file:
    patterns = list(csv.reader(patterns_file, delimiter=';'))

for i, pattern in enumerate(patterns):
    for news in tqdm(lenta):
        results_db[f"normal_{i}"] = [x for x in check_single_pattern(news[2], 
                    pattern[1], name=news[0])]
    
#         results_db[f"extended_{i}"] = [x for x in check_single_pattern(news[2], 
#                     pattern[0], name=news[0])]


# print("\nНазвание иноагента: {}".format(pattern[2]))
# if extended:
#         pattern_to_test = pattern[0]
#         print("Тестирование расширенного режима")
# else:
#         pattern_to_test = pattern[1]
#         print("Тестирование обычного режима")

# print("\n1. Поиск по списку иноагентов:")
# results = [x for x in check_single_pattern(nko_list, pattern_to_test, name=pattern[2])]

# print("\n2. Поиск по новостям lenta.ru:")
# with open(lenta_path, encoding="utf-8") as csv_file:
#         lenta = csv.reader(csv_file, delimiter=',')
#         for news in lenta:
#         results = [x for x in check_single_pattern(news[2], pattern_to_test, name=news[0])]


with open(RESULTS_SEP_PTNS,'wb') as pkl_file:
    pickle.dump(results_db, pkl_file)
