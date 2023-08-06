#!/usr/bin/env python3
""" Small tool that grabs a specific user's github stars, caches it and
    then allows you to run searches on it from the shell.
    
    It comes handy if you also use this feature of github as a sort of dev 
    bookmark. It uses the free github api (which is rate limited hence the 
    cache too). And searches in description, full_name and topics.
    
    Oh, important: no dependencies, besides python stdlib.
    
    TODO: add token use as if you have more than 6k stars you'll be rate limited
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from pathlib import Path
from time import time
import json
import re
import argparse

# TODO: arguments: -u user  -f force cache rebuild
# TODO: .status = 429 rate limited, header Retry-After secs how long to wait

__version__ = "v0.1.1, 2023/jun by iexa"
DEFAULT_GITHUB_USER = "iexa"
GITHUB_URL = "https://api.github.com/users/[user]/starred?per_page=100&page="
CACHE_STALE_TIME_SECS = 7*24*3600
CACHE_FILE = Path.home() / ".githubstarsearch"
CACHE_FILE_HEADER = f"HELLOOO from githubstarsearch cache {__version__}\n"

# file format: pickled + zipped, data + searches stored
# description, topics array, stargazers_count, homepage
# full_name (https://github.com/+), created_at, pushed_at, stargazers_count, language

def go_ahead():
  # check cache, download if none/stale/forced, do search, print results with links and desc 

  print(f"Github Star Search ({__version__})")
  data = grab_and_parse_stars()


def is_cached_data_stale():
  """ returns True if no cache file or stale, otherwise False """
  if not Path(CACHE_FILE).exists():
    return True
  try:
    is_stale = (time() - Path(CACHE_FILE).stat().st_mtime) > CACHE_STALE_TIME_SECS
  except IOError:
    return True # some error with the cache file so no cache for now
  return is_stale
  

def get_cached_data():
  """ returns None if no cache file or decoded data """
  try:
    with open(CACHE_FILE) as f:
      a = f.readline()
      print(a)
  except IOError as e:
     print(e)


def save_cached_data(data):
  """ yup. that. """
  pass
  

def grab_and_parse_stars():
  github_user = DEFAULT_GITHUB_USER
  base_url = GITHUB_URL.replace('[user]', github_user)
  
  def get_last_page_from_link_header(link) -> int:
    if not link:
      return None
    p = re.compile(r"&page=(\d+)>;\s+rel=\"last", re.IGNORECASE)
    if m := p.search(link): # .search not .match, - match only at beginning
      return int(m.group(1))
    
  data = []
  page = 1
  while True:
    try:
      with urlopen(f"{base_url}{page}") as f:
        if f.status != 200:
          print(f.status, f.reason)
          break      
        d = f.read().decode('utf8')
        if not len(d):
          break
        d = json.loads(d)
        # TODO: parse data
        last_page = get_last_page_from_link_header(f.headers['Link'])
        if not last_page: # no last page exists anymore, which means we are on it
          break
        print(f"\r > grabbing {page*100}/{(last_page-1)*100}+ 🌟's & refreshing cache.", end='')   
        page += 1
    except HTTPError as e:
      print(e)
      exit()
  return data



if __name__ == "__main__":
  go_ahead()
  