import csv
from tqdm import tqdm
import pickle
from pprint import pprint
from get_new_results import get_all_patterns_results
from get_new_results import get_sep_patterns_results

RESULTS_SEP_PTNS = "autotest_db/results_separate_patterns_db.pkl"
RESULTS_SEP_PTNS_NEW = "autotest_db/results_separate_patterns_db_new.pkl"

with open(RESULTS_SEP_PTNS, "rb") as pkl_file:
    old_results_sep = pickle.load(pkl_file, encoding="utf-8")

for key, value in old_results_sep.items():
    print(f"Pattern: {key} Quantity: {len(value)}")

new_results_sep = get_sep_patterns_results(RESULTS_SEP_PTNS_NEW, load_old=False)
