import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

""" 
recursive algo, breaking list to sublists until only one elem in each then
merging back up into original list
O (n * log n) - so quite efficient
"""
def merge_sort(data):
    if len(data) <= 1:
        return
    mid = len(data) // 2
    left, right = data[:mid], data[mid:]
    log.debug(f'recurse left: {left}')    
    log.debug(f'recurse right: {right}')    
    merge_sort(left)
    merge_sort(right)

    left_idx = right_idx = idx = 0 # idx is main data list
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            data[idx] = left[left_idx]
            left_idx += 1
        else:
            data[idx] = right[right_idx]
            right_idx += 1
        idx += 1
    log.debug(f'sorted: {data}')
    # check for any leftovers
    while left_idx < len(left):
        data[idx] = left[left_idx]
        left_idx += 1
        idx += 1
    while right_idx < len(right):
        data[idx] = right[right_idx]
        right_idx += 1
        idx += 1

    
a = [4, 11, 9, -1, 89, 113, 77, 32, 56, 2, 6]

merge_sort(a)
print('-'*15)
print(a)