import os


def main():
    # Itterate through subfolders and files in folder
    directory = r'D:\OutlookDB\Foto2020'
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(os.path.join(directory, filename))
        else:
            continue
    # Get information from each file

    # Store information in database

    # Organise and delete dublicates


if __name__ == "__main__":
    main()