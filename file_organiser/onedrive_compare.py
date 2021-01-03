import hashlib
import ntpath
from pathlib import Path
from tqdm import tqdm
import csv
import pandas as pd
import filecmp
import os
# from shutil import copyfile


def get_hash(file_path):
    # Calculate hash
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        data = file.read()
        hasher.update(data)
    return hasher.hexdigest()


def make_files_db(folder: str, db_name: str):
    # Create database of files in folder
    paths = Path(folder).glob('**/*')
    f = open(db_name, 'w', encoding='utf-8')
    with f:
        writer = csv.DictWriter(f, fieldnames=['fname', 'hash', 'path'])
        writer.writeheader()
        for path in tqdm(paths):
            try:
                if path.is_file():
                    writer.writerow({'fname': ntpath.basename(path),
                                     'hash': get_hash(path),
                                     'path': path})
            except Exception as e:
                print(e)
                print(path)
    f.close()


def print_paths_with_identical_hashes(df):
    hash_count = df['hash'].value_counts()
    hash_count = hash_count[hash_count > 2]

    filecmp.clear_cache()
    duplicates = open("data/duplicates_old.txt", "w+", encoding='utf-8')
    for h, count in tqdm(hash_count.items()):
        duplicates.write(f"\n\nHash: {h} count: {count}\n")
        for f in df['path'][df['hash'] == h]:
            duplicates.write(f + '\n')
            # if filecmp.cmp(df['path'][df['hash'] == h].iloc[0], f, shallow=False) is not True:
            #     print(f)
    duplicates.close()
    return None


def delete_duplicates(df):
    hash_count = df['hash'].value_counts()
    hash_count = hash_count[hash_count > 2]

    for h, count in tqdm(hash_count.items()):
        for f in df['path'][df['hash'] == h]:
            if f != df['path'][df['hash'] == h].iloc[0]:
                try:
                    os.remove(f)
                except Exception as e:
                    print(e)
                    print(f)
    return None


def delete_copied(df_old, df_new):
    copied_hashes = set(df_new['hash'])

    for index, row in df_old.iterrows():
        if row['hash'] in copied_hashes:
            try:
                os.remove(row['path'])
            except Exception as e:
                print(e)
                print(row['path'])

    return None


# def compare_df(df1, df2):
#     col_list = ['A', 'B', 'C', 'D']
#     idx = (df1.loc[:,  col_list] == df2.loc[:,  col_list]).all(axis=1)
#     df1['new_row'] = idx.astype(int)
#     return None


def main():
    # Define our constants
    # SOURCE_FOLDER = r'D:/OneDriv/'
    # DESTINATION_FOLDER = r'D:/OneDrive/'
    # SECOND_BATCH = r'D:/not_copied/'

    # Step 1. Create data bases of available files:
    # make_files_db(DESTINATION_FOLDER, 'new_onedrive.csv')
    # make_files_db(SOURCE_FOLDER, 'data/old_onedrive.csv')

    # Step 2. Load data
    old_onedrive = pd.read_csv('data/old_onedrive.csv', encoding='cp1251')
    new_onedrive = pd.read_csv('data/new_onedrive.csv', encoding='cp1251')
    print(old_onedrive.head())
    print(old_onedrive.describe())

    # Step 3. Delete duplicates
    # delete_duplicates(old_onedrive)

    # Step 4. Delete already copied files
    delete_copied(old_onedrive, new_onedrive)

    # counter = 0
    # f = open("file_list.txt", "a")
    # paths = Path(SOURCE_FOLDER).glob('**/*')
    # for path in tqdm(paths):
    #     if path.is_file():
    #         if get_hash(path) not in hashes_in_onedrive:
    #             f.write(path)
    #             counter += 1
    #             if ntpath.basename(path) in paths_in_onedrive:
    #                 print(path)
    #             # copyfile(path, SECOND_BATCH + ntpath.basename(path))
    # f.close()
    # print(f"{counter} files needs to be copied to OneDrive!")


if __name__ == "__main__":
    main()
