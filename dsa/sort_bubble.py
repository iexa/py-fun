""" basic bubble sort with minimal optimization """

import logging as log

log.basicConfig(level=log.DEBUG, format='%(levelname)s: %(message)s')

def bubble_sort(lst):
	if len(lst) < 2:
		return lst
	unsorted_idx = len(lst) - 1
	sort_finished = False

	while not sort_finished:
		sort_finished = True
		for i in range(unsorted_idx):
			if lst[i] > lst[i+1]:
				lst[i], lst[i+1] = lst[i+1], lst[i]
				sort_finished = False
		log.info(f"{unsorted_idx=} {lst=}")
		unsorted_idx -= 1 # decrease each iter so each "bubbling" goes only till needed
	return lst
	

a = [67, 13, 21, 9, -4, 55, 11, 74, 32, 22]
b = [9,8,7,6,5,4,3,2]
print(a)
bubble_sort(a)

print(f"\n{b}")
bubble_sort(b)
