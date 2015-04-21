""" Maintained by Jordan Williams """

from math import floor
import quantiles

def normalize_h(error, length, i):
	score = (5 * (i + 1.0) / length)
	
	#if the score is less than 1 assign it as a 1
	if(score < 1.0):
		score = 1
		
	return score

#converts score to a number 1-5
def normalize(essays, attribute):
	# Sort the essays by the given attribute in ASC order unless we are ranking length
	essays.sort(key = lambda a : getattr(a.raw_score, attribute), reverse = True)
	
	if attribute == "length":
		essays.reverse()
		
	for i, essay in enumerate(essays):
		raw_score = getattr(essay.raw_score, attribute)
		setattr(essay.normalized_score, attribute, normalize_h(raw_score, len(essays), i))
		
	
	# print attribute.capitalize()
	# print ", ".join(set(map(lambda x : str(getattr(x.raw_score, attribute)), essays)))
	
	# Remember to print to excel
	# print ", ".join(set(map(lambda x : str(getattr(x.raw_score, decimals = 2), attribute), essays)))
	
	return quantiles.find(map(lambda x : getattr(x.raw_score, attribute), essays), [0.2, 0.4, 0.6, 0.8])