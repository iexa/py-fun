import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

""" 
get a pivot element and then partition elems lower than that and larger than that
call recursively quicksort again with these best case O(n log n) worst O ( n^2 )
picking a random pivot element results in avg case == best case
"""
def quick_sort(data, pivot_idx=0):
    if len(data) < 2:
        log.debug(f'returning {data=}')
        return data
    pivot = data[pivot_idx] # try diff ones. decides how fast it goes
    less = [val for idx, val in enumerate(data) if idx != pivot_idx and val < pivot]
    more = [val for idx, val in enumerate(data) if idx != pivot_idx and val > pivot]
    log.debug(f'{pivot_idx=} {pivot=}')
    log.debug(f'{less=}, {more=}')
    return quick_sort(less) + [pivot] + quick_sort(more)


a = [4, 11, 9, -1, 89, 113, 77, 32, 56, 2, 6]

print(a)
b = quick_sort(a)
print('-'*15)
print(b)
