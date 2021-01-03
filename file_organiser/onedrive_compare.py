import hashlib
import ntpath
from pathlib import Path
from tqdm import tqdm
import csv
import pandas as pd
# import os
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
    f = open(db_name, 'w')
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


def main():
    # Define our constants
    SOURCE_FOLDER = r'D:/OneDriv/'
    DESTINATION_FOLDER = r'D:/OneDrive/'
    # SECOND_BATCH = r'D:/not_copied/'

    # Step 1. Create data bases of available files:
    # make_files_db(DESTINATION_FOLDER, 'new_onedrive.csv')
    # make_files_db(SOURCE_FOLDER, 'old_onedrive.csv')

    # Step 2. Delete dublicate files
    new_onedrive = pd.read_csv('new_onedrive.csv', encoding='cp1251')
    old_onedrive = pd.read_csv('old_onedrive.csv', encoding='cp1251')

    print(new_onedrive)
    print(old_onedrive)

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
