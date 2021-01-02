import os
from pathlib import Path
import ntpath
from pygame import mixer
from shutil import copyfile


def main():
    SOURCE_FOLDER = r'C:/Users/59850/Desktop/Music'
    DESTINATION_FOLDER = r'C:/Users/59850/Desktop/Selected/'
    mixer.init()

    # Itterate through subfolders and files in folder
    paths = Path(SOURCE_FOLDER).glob('**/*')
    for path in paths:
        if path.is_file():
            try:
                mixer.music.load(path)
                mixer.music.play()
                while mixer.music.get_busy():
                    print(path)
                    print('Copy this music to selected? :')
                    action = input()
                    if action == 'y':
                        copyfile(path, DESTINATION_FOLDER + ntpath.basename(path))
                    mixer.music.stop()
                
            except Exception as e:
                print(f'\n ERROR: {e}')


if __name__ == "__main__":
    main()


## Docs: http://www.pygame.org/docs/ref/music.html