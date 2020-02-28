"""dikk."""
from pathlib import Path
# import subprocess

a = Path('/Volumes/X3/SWTEMP/').glob('*.nsp')

a = list(a)
a.sort(key=lambda _: _.stat().st_size)

for x in a:
  print(x)
