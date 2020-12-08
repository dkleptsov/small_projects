import os
import ntpath
import hashlib
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
from tqdm import tqdm
 

def getinfo(image_path: str):
    image_info = {}
    image_info['path'] = image_path
    image_info['file_name'] = ntpath.basename(image_path)
    image_info['type'] = image_info['file_name'].split('.')[-1]
    # Calculate hash
    hasher = hashlib.md5()
    with open(image_path, 'rb') as file:
        data = file.read()
        hasher.update(data)
    image_info['hash'] = hasher.hexdigest()
    # Get year of the image
    try:
        image = Image.open(image_path)
        image_info['date'] = image.getexif()[36867]
    except Exception:
        image_info['date'] = None

    return image_info


def main():
    SOURCE_FOLDER = r'G:/PHOTO_SORTING/'

    # Itterate through subfolders and files in folder
    paths = Path(SOURCE_FOLDER).glob('**/*')
    for path in tqdm(paths):
        if path.is_file():
            getinfo(path)

        # Store information in database

    # Organise and delete dublicates


if __name__ == "__main__":
    main()
