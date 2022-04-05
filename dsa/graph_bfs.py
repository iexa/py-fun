import logging as log
from collections import deque

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

""" 
simple graph breadth-first-search
"""
def search(graph, start='you', predicate=None):
    if predicate is None:
        raise ValueError('Must supply a valid predicate function.')
    search_queue: deque = deque()
    search_queue += graph[start]
    visited = []
    while search_queue:
        item = search_queue.popleft()
        log.info(f'{item=}')
        if item in visited:
            continue
        if predicate(item):
            log.info(f'Found: {item=}')
            return True
        else:
            search_queue += graph[item]
            log.debug(f'{search_queue=}')
            visited.append(item)
    return False




g = dict()
g['you'] = ('alice', 'bob', 'claire')
g['bob'] = ('ankita', 'peggy')
g['alice'] = ('peggy',)
g['claire'] = ('thom', 'penny')
g['ankita'] = ()
g['peggy'] = ()
g['thom'] = ()
g['penny'] = ()

print('-'*15)
search(g, predicate=lambda x: x.endswith('m'))
