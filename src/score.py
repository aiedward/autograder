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