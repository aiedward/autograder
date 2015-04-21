""" Maintained by Jordan Williams"""

from score import NormalizedCutoffs, Score
from essay import Essay

import categories
import quantiles
import rank
import glob

# Find cutoffs for classification
def find_cutoffs(essays):
    scores = map(lambda x : x.grader_score, essays)
    scores.sort()
    
    NormalizedCutoffs.total = quantiles.find(scores, [0.33, 0.66])
    
    return None
    
    
def print_cutoffs():
    NormalizedCutoffs._print(NormalizedCutoffs)
    
    return None
    

# Saves the learned cutoff values in "cutoffs.txt"
def save_cutoffs():
    file = open("cutoffs.txt", "w+")
    
    for cat in categories.ALL + ["total"]:
        cutoffs_list = getattr(NormalizedCutoffs, cat)
        
        file.write(str(cutoffs_list) + "\n")
        
    file.close()
    
    return None
    

# Restores the cutoffs learned for our model in "cutoffs.txt"
def restore_cutoffs():
    file = open("cutoffs.txt", "r")
    
    for cat in categories.ALL + ["total"]:
        cutoffs_str  = file.readline().strip("[]\n").split(",")
        cutoffs_list = map(lambda x : float(x), cutoffs_str)
        
        setattr(NormalizedCutoffs, cat, cutoffs_list)
        
    file.close()
    
    return None
    

    
# Learns the cutoff weights for each category and calculates each essays score
def train(save = True):
    # Read all essays training essays into memory
    essays = read_in_essays(training = True)
    
    # Send each essay through the pipeline to prepare for grading
    for essay in essays:
        essay.pipeline()
    
    # Normalize scores and learn cutoffs for each category
    for cat in categories.ALL:
        setattr(NormalizedCutoffs, cat, rank.normalize(essays, cat))
    
    # Calculate the total score for each essay
    for essay in essays:
        essay.calculate_score()
        
    find_cutoffs(essays)
    save_cutoffs() if save else None
    
    return essays


# Given a single filepath to an essay, prints the score according to a trained model
def test():
	essays = read_in_essays(training = False)
	
	restore_cutoffs()
	
	output = []
	
	for essay in essays:
		essay.pipeline()
		output.append(essay.output())
	
	new_output	= ""
	for string in output:
		new_output += string

	file = open("output/results.txt", "w+")
	file.write(str(new_output))
	file.close
	
	print "See output/results.txt for classification predictions"
	
	return None


# Converts a file to a string
def file_to_string(filename):
	with open(filename, "r") as f:
		return f.read()


# Reads in essays for high, medium, and low classes
def read_in_essays(training=True, cwd="", debug=False):
	type = "training" if training else "test"
	
	essays = []
	
	if type == "training":
		for i, score in enumerate(["low", "medium", "high"]):
			filenames = glob.glob(cwd + "input/" + type + "/" + score + "/*.txt")
			essays.extend( map(lambda x : Essay(x, file_to_string(x), i+1), filenames) )
		
	else:
		filenames  = glob.glob("input/" + type + "/tokenized/*.txt")
		essays = map(lambda x : Essay(x, file_to_string(x), 1), filenames)
		
	print "Read in " + str(len(essays)) + " essays from " + type + " data"
	
	return essays[0] if debug else essays