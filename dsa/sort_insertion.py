import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

""" 
sorting like a deck of cards. left part (1st elem) is already sorted, right part is not
going through right upwards while comparing pieces to the left, if left lower, exchange 
O(n ** 2) but ideally if nearly sorted already closer to O (n)
"""
def insertion_sort(data):
    for i in range(1, len(data)):
        val = data[i]
        log.info(f'{i=}')
        log.info(f'before: {data}')
        while i > 0 and data[i-1] > val:
            data[i] = data[i-1]
            i -= 1
        data[i] = val
        log.info(f'after: {data}')
    return data

    
a = [4, 11, 9, -1, 89, 113, 77, 32, 56, 2, 6]

insertion_sort(a)
print('-'*15)
print(a)