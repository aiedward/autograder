from pattern.en import parsetree

import rules

#
# Returns true if a tag is a verb
def is_verb(tag):
	return True if tag in rules.VERBS else False
	
	
#
# Returns the number of unique verbs in an essay
def unique_verbs(essay):
	unique_verbs = filter(lambda x : True if x[1] in rules.VERBS else False, essay.tags)
	
	return len(set(map(lambda x : x[0], unique_verbs)))


#
# Returns a list of all Verb bigrams given an essay
def find_bigrams(essay):
	tags = filter(lambda x : True if "'" not in x[0] and "," not in x[0] else False, essay.tags_vbz)
	
	bigrams = []
	advance = 0
	
	for i in range(0, len(tags)):
		# Do we need to skip iterations?
		if advance > 0:
			advance -= 1
			continue
		
		# Skip over trigrams so we do not overcount
		if( is_verb(tags[i][1]) ):
			if( is_verb(tags[i+1][1]) ):
				if( is_verb(tags[i+2][1]) ):
					advance = 3
					continue
				else:
					bigrams.append([tags[i], tags[i+1]])
					
	return bigrams


#
# Returns a list of all Verb trigrams given an essay
def find_trigrams(essay):
	tags = filter(lambda x : True if "'" not in x[0] and "," not in x[0] else False, essay.tags_vbz)
	
	trigrams = []
	advance = 0
	
	for i in range(0, len(tags)):
		# Skip over trigrams so we do not overcount
		if( is_verb(tags[i][1]) ):
			if( is_verb(tags[i+1][1]) ):
				if( is_verb(tags[i+2][1]) ):
					trigrams.append([tags[i], tags[i+1], tags[i+2]])
					
	return trigrams
	
	
def find_verbs(essay):
	essay.parse()

#
# Returns the number of verb agreement mistakes found
def mistakes(essay):
	essay.disambiguate_vbz()
	
	bigrams  = find_bigrams(essay)
	trigrams = find_trigrams(essay)
	errors   = 0.0
	
	for bigram in bigrams:
		if ",".join(map(lambda x : x[1], bigram)) in rules.VERB_BIGRAM_RULES: 
			errors += 1
		
	for trigram in trigrams:
		if ",".join(map(lambda x : x[1], trigram)) in rules.VERB_TRIGRAM_RULES:
			errors += 1
	
	return errors / (len(bigrams) + len(trigrams))


#
# #
# def plural(word):
# 	return True if pluralize(word) == word else False
	
	