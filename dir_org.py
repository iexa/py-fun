import os
import logging as log
from pathlib import Path

BASE_DIR = 'dir_org'
SUBDIRS = {
    "docs": 'pdf rtf txt docx pptx xlsx',
    "audio": 'm4a m4b mp3 ogg wav',
    "video": 'avi mpg mp4 m4v',
    "image": 'jpg jpeg png gif',
    "code": 'py js ts jsx tsx'
}

# config logger, only succeeds if never called before
# log.basicConfig(level=log.DEBUG)
log.basicConfig(level=log.DEBUG, filename='dir_org.log', filemode='w')

def chooseDir(val):
    for category, suffixes in SUBDIRS.items():
        if val in suffixes.split(): return category
    return 'misc'

def organizeDir():
    for item in os.scandir():
        origPath = Path(item)
        if origPath.is_dir(): continue
        suffix = origPath.suffix[1:].lower() # remove '.'
        dir = chooseDir(suffix)
        log.info(f'{dir}, {origPath}')
        dirPath = BASE_DIR / Path(dir)
        if not dirPath.is_dir():
            dirPath.mkdir(parents=True)
        # origPath.rename(dirPath / origPath)

if __name__ == '__main__':
    organizeDir()
