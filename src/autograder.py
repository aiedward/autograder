from pattern.en import parsetree, wordnet as wn, quantify

import nltk as nl
import re
import glob
import spelling
import subjectVerbAgreement as sva
import sentence
import rank
import quantiles
import verb

CATEGORIES = ["spelling", "sbj_vrb", "vrb_tense", "length"]


##
###########################################
# Classes
###########################################
##
    
class NormalizedCutoffs:
    spelling  = [0,0,0,0]
    sbj_vrb   = [0,0,0,0]
    vrb_tense = [0,0,0,0]
    length    = [0,0,0,0]
    total     = [0,0]
    
    def _print(self):
        print "Spelling: "               + str(self.spelling)
        print "Subject-Verb Agreement: " + str(self.sbj_vrb)
        print "Verb Tense: "             + str(self.vrb_tense)
        print "Length: "                 + str(self.length)
        print "Total: "                  + str(self.total)

class Score:
    spelling  = 0.0
    sbj_vrb   = 0.0
    vrb_tense = 0.0
    sent_form = 0.0
    coherence = 0.0
    topic     = 0.0
    length    = 0.0
    
    # Prints the scores 
    def _print(self):
        print "Spelling: "               + str(self.spelling)
        print "Subject-Verb Agreement: " + str(self.sbj_vrb)
        print "Verb Tense: "             + str(self.vrb_tense)
        # print "Sentence Formation: "     + str(self.sent_form)
        # print "Coherence: "              + str(self.coherence)
        # print "Topic: "                  + str(self.topic)
        print "Length: "                 + str(self.length)
    
    
class Essay:
	def __init__(self, filename, text, real_score = 0):
		self.text                   = text
		self.text_list              = read_data(self.text)
		self.tags                   = nl.pos_tag(self.text_list)
		self.raw_score              = Score()
		self.normalized_score       = Score()
		self.real_score             = real_score
		self.filename               = filename
		self.grader_score           = 0.0
		self.classification         = 1
		self.classification_penalty = 0


	# Calculates the weighted score for an essay
	def calculate_score(self):
		s = self.normalized_score
		self.grader_score = s.spelling + s.sbj_vrb + s.vrb_tense + 2*s.sent_form + 2*s.coherence + 3*s.topic + 2*s.length


	# Selects the class of the essay based on the learned cutoffs
	def classify(self):
		if self.grader_score > NormalizedCutoffs.total[0]:
			self.classification += 1
		if self.grader_score > NormalizedCutoffs.total[1]:
			self.classification += 1


	def output(self):
		t = self.classification 
		
		if t == 1:
			grade = "low"
		elif t == 2:
			grade = "medium"
		else:
			grade = "high"
			
		string = self.filename + "\t" + str(self.normalized_score.spelling) + "\t" + str(self.normalized_score.sbj_vrb) + "\t" + str(self.normalized_score.vrb_tense) + "\t" + "0\t0\t0\t" + str(self.normalized_score.length) + "\tunknown\n"
		
		return string


	# Builds a parse tree using Pattern.en
	def parse(self):
		self.parsetree = parsetree(self.text, relations=True)


	# Sends the essay down the pipeline to calculate it's raw scores for each category
	def pipeline(self):
		self.raw_score.spelling  = spelling.mistakes(self)
		self.raw_score.sbj_vrb   = sva.mistakes(self)
		self.raw_score.length    = sentence.length(self) + verb.unique_verbs(self)
		self.raw_score.vrb_tense = verb.mistakes(self)
		
		return self


	# Takes an essay and scores it according to the trained cutoff points   
	def predict(self):
		for cat in CATEGORIES:
			raw = getattr(self.raw_score, cat)
			score = 1

		# Score the essay according to its cutoff level
		if cat == "length":
			for i, cutoff in enumerate(getattr(NormalizedCutoffs, cat)):
				if raw > cutoff:
					score += 1

		else:
			for i, cutoff in enumerate(getattr(NormalizedCutoffs, cat)):
				if raw < cutoff:
					score += 1

		# Store the normalized score
		setattr(self.normalized_score, cat, score)

		# Calculate the essay's total score and classify
		self.calculate_score()
		self.classify()

		# Calculate mis-classification penalty
		if self.real_score != 0 and self.real_score != self.classification:
			self.classification_penalty = abs(self.real_score - self.classification)


	# Replaces VBZ tags with VBZis or VBZhas
	def disambiguate_vbz(self):
		tags = map(lambda x : (x[0], 'VBZis') if x[1] == 'VBZ' and x[0] == 'is' else x, self.tags)

		self.tags_vbz = map(lambda x : (x[0], 'VBZhas') if x[1] == 'VBZ' and x[0] == 'has' else x, tags)


	# Prints a summary of the essay
	def summary(self):
		print self.filename
		print "Real Score: "       + str(self.real_score)
		print "Classification: "   + str(self.classification)
		print "Grader Score: "     + str(self.grader_score)
		self.normalized_score._print()


##
###########################################
# Module Functions
###########################################
##

# Find cutoffs for classification
def find_cutoffs(essays):
    scores = map(lambda x : x.grader_score, essays)
    scores.sort()
    
    NormalizedCutoffs.total = quantiles.find(scores, [0.33, 0.66])
    
    
def print_cutoffs():
    NormalizedCutoffs._print(NormalizedCutoffs)
    

# Saves the learned cutoff values in "cutoffs.txt"
def save_cutoffs():
    file = open("cutoffs.txt", "w+")
    
    for cat in CATEGORIES + ["total"]:
        cutoffs_list = getattr(NormalizedCutoffs, cat)
        
        file.write(str(cutoffs_list) + "\n")
        
    file.close()
    

# Restores the cutoffs learned for our model in "cutoffs.txt"
def restore_cutoffs():
    file = open("cutoffs.txt", "r")
    
    for cat in CATEGORIES + ["total"]:
        cutoffs_str  = file.readline().strip("[]\n").split(",")
        cutoffs_list = map(lambda x : float(x), cutoffs_str)
        
        setattr(NormalizedCutoffs, cat, cutoffs_list)
        
    file.close()
    

    
# Learns the cutoff weights for each category and calculates each essays score
def train(save = True):
    # Read all essays training essays into memory
    essays = read_in_essays(training = True)
    
    # Send each essay through the pipeline to prepare for grading
    for essay in essays:
        essay.pipeline()
    
    # Normalize scores and learn cutoffs for each category
    for cat in CATEGORIES:
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
		essay.pipeline().predict()
		output.append(essay.output())
	
	new_output	= ""
	for string in output:
		new_output += string

	file = open("output/results.txt", "w+")
	file.write(str(new_output))
	file.close


# Reads in a tokenized string and converts it into a list of tokens
def read_data(textfile):
	return textfile.replace('\n'," ").split()


# Converts a file to a string
def file_to_string(filename):
	with open(filename, "r") as f:
		return f.read()


# Reads in essays for high, medium, and low classes
def read_in_essays(training = True, cwd = ""):
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
	
	return essays