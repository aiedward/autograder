from score import NormalizedCutoffs, Score
from pattern.en import parsetree, wordnet as wn, quantify

import nltk as nl
import spelling
import subjectVerbAgreement as sva
import sentence
import verb
import categories


class Essay:
	def __init__(self, filename, text, real_score = 0):
		self.text                   = text
		self.text_list              = self.text.replace('\n'," ").split()
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
			
	
	# Replaces VBZ tags with VBZis or VBZhas
	def disambiguate_vbz(self):
		tags = map(lambda x : (x[0], 'VBZis') if x[1] == 'VBZ' and x[0] == 'is' else x, self.tags)

		self.tags_vbz = map(lambda x : (x[0], 'VBZhas') if x[1] == 'VBZ' and x[0] == 'has' else x, tags)


	# Returns a string formatted for the competition
	def output(self):
		t = self.classification 
		
		if t == 1:
			grade = "low"
		elif t == 2:
			grade = "medium"
		else:
			grade = "high"
			
		string = self.filename + "\t" + str(self.normalized_score.spelling) + "\t" + str(self.normalized_score.sbj_vrb) + "\t" + str(self.normalized_score.vrb_tense) + "\t" + "0\t0\t0\t" + str(self.normalized_score.length) + "\t" + grade + "\n"
		
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
		
		# Now predict
		self.predict()


	# Takes an essay and scores it according to the trained cutoff points   
	def predict(self):
		for cat in categories.ALL:
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


	# Prints a summary of the essay
	def summary(self):
		print self.filename
		print "Real Score: "       + str(self.real_score)
		print "Classification: "   + str(self.classification)
		print "Grader Score: "     + str(self.grader_score)
		self.normalized_score._print()