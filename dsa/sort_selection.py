import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

""" 
- similar to insertion sort, but it looks ahead not backwards, and it also does not need to create
room for the newly found item in the already sorted stack at the bottom like insertion
- each iter needs to check one less item as it gets sorted from the bottom up
"""
def selection_sort(data):
    if len(data) < 2:
        return data
    for i in range(len(data)-1): # check only til' top-1 as inner loop will do the rest
        lowest_idx = i
        log.info(f"{lowest_idx=}, {data=}")
        for j in range(i+1, len(data)):
            if data[j] < data[lowest_idx]:
                lowest_idx = j
        if lowest_idx != i:
            log.info(f"lowest_idx changed swapping {lowest_idx=} <> {i=}")
            data[i], data[lowest_idx] = data[lowest_idx], data[i]
    return data
    
    

a = [4, 5, 8, 11, -9, 124, 12, 75, 0]
selection_sort(a)
