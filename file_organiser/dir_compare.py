import os
import ntpath
from pathlib import Path
from shutil import copyfile


def main():
    SOURCE_FOLDER = r'C:/Users/59850/Desktop/yt_bot/'
    DESTINATION_FOLDER = r'C:/Users/59850/Desktop/from fenix6/'
    SECOND_BATCH = r'C:/Users/59850/Desktop/2nd_batch/'

    # Detect files that already been copied to device:
    counter = 0
    music_on_device = set()
    paths = Path(DESTINATION_FOLDER).glob('**/*')
    for path in paths:
        music_on_device.add(ntpath.basename(path))
        counter+=1
    print(f"Device contains {counter} songs!")

    # Copy files that are not on device to separate folder
    counter = 0
    paths = Path(SOURCE_FOLDER).glob('**/*')
    for path in paths:
        if ntpath.basename(path) not in music_on_device:
            copyfile(path, SECOND_BATCH + ntpath.basename(path))
            print(ntpath.basename(path))
            counter+=1

    print(f"{counter} songs needs to be copied to device!")






if __name__ == "__main__":
    main()


## Docs: http://www.pygame.org/docs/ref/music.html