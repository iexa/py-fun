""" 
  unpacks rar files that are double-packed
  ]usually scene-release files are packed this way[
"""
__author__ = 'iexa'

from pathlib import Path
import rarfile as rf
from time import time
# import zipfile as zf


def unpack(file, todir):
  """unpacks a double-packed file; needs unrar on syspath; returns Path of it or False"""
  def testpath(z):
    """test file exts for rar multipart start -input: Path.suffixes list"""
    if   len(z) == 1 and z[0] == '.rar': return True
    elif len(z) >= 2 and z[-2] in ('.part1', '.part01'): return True
    elif len(z) >= 2 and z[-1] == '.rar' and '.part' not in z[-2]: return True
    return False
  

  z = rf.RarFile(file, crc_check=False)
  extraction_dir = Path(z.namelist()[0]).parent
  print(' '*7, f"| {file.stat().st_size>>20}mb unpacking...", end='', flush=True)
  t0 = time()
  try:
    z.extractall(path=todir)
  except rf.Error:
    print(' '*7, f'\nINFO: ==> CHECK <== ARCHIVE FILE ERROR ?CRC or PASSWORD?')
    z.close()
    return False
  z.close()

  inside = [x for x in (todir/extraction_dir).iterdir() if testpath(x.suffixes)]
  if len(inside) != 1:
    print(' '*7, f'\nINFO: ==> CHECK <== CANNOT UNPACK INSIDE FILE(s)')
    return False
  print(f'{round(time()-t0,1)}s, now the inner one...', end='', flush=True)
  t0 = time()
  inside = inside[0]
  z = rf.RarFile(inside, crc_check=False)
  final_file = z.namelist()[0]

  if len(z.namelist()) > 1:
    print(' '*7, f'\nINFO: ==> CHECK <== MORE THAN 1 INSIDE FILES')
    return False
  try:
    z.extractall(path=(todir/extraction_dir))
  except rf.Error:
    print(' '*7, f'\nINFO: ==> CHECK <== INSIDE ARCHIVE FILE ERROR ?CRC or PASSWORD?')
    z.close()
    return False
  z.close()  
  print(f'{round(time()-t0,1)}s done.', flush=True)
  return todir / extraction_dir / final_file


""" MAIN """
startpath = Path('/Volumes/X3/SWTEMP')

t0 = time()
allfiles = tuple(startpath.glob('*.rar'))
allfiles_cnt = len(allfiles)
print(f'>>> Unpacking from {startpath}')
for nr, p1 in enumerate(allfiles, start=1):
  print(f'{str(nr).zfill(3)}/{str(allfiles_cnt).zfill(3)}: {p1.name}', flush=True)
  gotit = unpack(p1, startpath)
  if not gotit:
    print('-'*7, '==> CHECK <== something went wrong with this one')
    continue
  # some filename massaging
  rename_to = str(gotit.parent.relative_to(startpath))
  rename_to = rename_to.translate(rename_to.maketrans('_.', '  '))
  rename_to = rename_to.partition(' eShop')[0] + '.nsp'
  gotit.rename(startpath / Path(rename_to))  
  # cleanup files
  for x in gotit.parent.iterdir():
    x.unlink()
  gotit.parent.rmdir()
  p1.unlink()
  # if nr > 77:
    # break
t1 = int(time()-t0)
print(f'>>> DONE in {t1//60}m {t1%60}s - [phew!]')
