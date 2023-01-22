#!/usr/bin/env python3
from os import rename
import re
from pathlib import Path

"""
Rename files in a folder by using a text file with the new names
in the same order as listed in the file.
"""
# dry_run - do not do it, just list the files
def rename_files(list_of_new_names_file, existing_files_glob, add_prefix_nrs: bool,
                  dry_run=True, root=Path('./')):
  DIGITS = 1  # const that show how many digits are in the prefix of the new name
  with open(root / Path(list_of_new_names_file), encoding='utf8') as file:
    names = file.readlines()
    len_name = len(names)
    DIGITS = 4 if len_name // 1000 else 3 if len_name // 100 else 2

  new_names = []
  for nr, name in enumerate(names, start=1):
    def prettifyname(x):
      """ Remove stupid characters from filename, condense spaces to 1. """
      x = ''.join(map(lambda x: '' if x in "\"“”?':/;,!-_&^%$#@*><)(][" else x, x))
      return (re.sub(r'\s+', ' ', x)).strip()
    new_names.append(
      f"{str(nr).zfill(DIGITS)+' ' if add_prefix_nrs else ''}{prettifyname(name.lower())}")

  # get list of files and order them
  files = [x for x in root.glob(existing_files_glob)]
  files = sorted(files, key=lambda s:
    # natural sort as in 1..9,10,11, and not 1,10,11..19,2,20,..
    [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', str(s))]
  )

  for new_name, old_name in zip(new_names, files):
    new_name += old_name.suffix
    # old_sub = Path(old_name).with_suffix('.srt')
    # new_sub = root.joinpath(new_name).with_suffix('.srt')
    # print(f'{old_sub} -> {new_sub}')
    print(f'{old_name} -> {root.joinpath(new_name)}')
    if not dry_run:
      rename(old_name, root.joinpath(new_name))



LIST_OF_NEW_NAMES_FILE      = "new filenames one per line.txt"
EXISTING_FILES_GLOB_PATTERN = "lesson*.mp4"

add_prefix_nrs = True
print(f"---\nRenaming files using '{LIST_OF_NEW_NAMES_FILE} in current folder.'\n")
if input("Use prefix numbers? 'y' - yes or no - <anything + Enter> ") != 'y':
  add_prefix_nrs = False

while(input("\nDry run only <press any+Enter> or do for real 'r'? ") != 'r'):
  rename_files(LIST_OF_NEW_NAMES_FILE, EXISTING_FILES_GLOB_PATTERN, add_prefix_nrs)

rename_files(LIST_OF_NEW_NAMES_FILE, EXISTING_FILES_GLOB_PATTERN, add_prefix_nrs, dry_run=False)
print("\n DONE.")

