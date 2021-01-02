import hashlib
import ntpath
from pathlib import Path
from tqdm import tqdm
import csv
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
    # Find another way to calculate
    # print(f"New Onedrive contains {counter} files!")


def main():
    SOURCE_FOLDER = r'D:/OneDriv/'
    DESTINATION_FOLDER = r'D:/OneDrive/'
    # SECOND_BATCH = r'D:/not_copied/'

    make_files_db(DESTINATION_FOLDER, 'new_onedrive.csv')
    make_files_db(SOURCE_FOLDER, 'old_onedrive.csv')

    # # Detect files that are not in new OneDrive
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
