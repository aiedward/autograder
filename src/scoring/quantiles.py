""" Maintained by Jordan Williams """

from math import floor

def unique_list(sequence):
    seen = set()
    seen_add = seen.add
    return [ x for x in sequence if not (x in seen or seen_add(x))]

def find(scores, percentages):	
	values = []
	scores_set = unique_list(scores)
	length = len(scores_set)
	
	percentages = [0.33, 0.66] if length < 9 else percentages
	
	for i in percentages:
		values.append(scores_set[int(floor(length * i))])
		
	return values