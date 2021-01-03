# pip install charset-normalizer

# Print decoded text
# from charset_normalizer import CharsetNormalizerMatches as CnM
# print(CnM.from_path('new_onedrive.csv').best().first())

from charset_normalizer.cli.normalizer import cli_detect
from glob import glob


cli_detect(glob('./data/*'))