from pattern.en import tenses as tn, PRESENT, PAST, FUTURE

import rules

# Returns True if ngram is in violation of the supplied rule set
def is_rule_violation(ngram, rule_set):
	return True if ",".join(map(lambda x : x[1], ngram)) in rule_set else False


# Returns the error for tense similarity between sentences
def compute_tense_similarity(essay):
	sentences 		   = essay.parsetree
	sentence_vp_chunks = map(lambda x : x.verbs, sentences)
	tense_counts	   = map(lambda x : tense_counts(x), sentence_vp_chunks)
	
	for c in tense_counts: 
		print c
		
	return 0

#
# Returns true if a tag is a verb
def is_verb(tag):
	return True if tag in rules.VERBS else False
	
#
# Returns a list of all Verb bigrams given an essay
def find_bigrams(essay):
	tags = filter(lambda x : True if "'" not in x[0] and "," not in x[0] else False, essay.tags_vbz)
	
	bigrams = []
	advance = 0
	
	for i in range(0, len(tags)):
		# Do we need to skip this iteration?
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
	
	for i in range(0, len(tags)):
		# Skip over trigrams so we do not overcount
		if( is_verb(tags[i][1]) ):
			if( is_verb(tags[i+1][1]) ):
				if( is_verb(tags[i+2][1]) ):
					trigrams.append([tags[i], tags[i+1], tags[i+2]])
					
	return trigrams
	
	

# Returns a list of a list of verbs for each sentence
def find_verbs(essay):
	essay.parse()
	verb_chunks = map(lambda x : x.verbs, essay.parsetree)
	verb_tags	= map(lambda x : map(lambda y : y.words, x), verb_chunks)
	verbs		= map(lambda x : map(lambda y : y.tag, [v for verbs in x for v in verbs]), verb_tags)
	
	# Grab head word of each chunk then filter out onlt verbs
	chunks = map(lambda x : x.chunks, essay.parsetree)
	
	vp_chunks = []
	for chunk in chunks:
		vp_chunks.append(filter(lambda x : x.type == "VP", chunk))
	
	# vp_heads = map(lambda x : x.head, vp_chunks)
	
	return vp_chunks
	

# Returns the tense of a word if it is unambiguous
def tense(word):
	tense = None
	
	# Check defined rules first
	tense = FUTURE if word in rules.FUTURE_INDICATORS else tense
	tense = PAST   if word in rules.PAST_INDICATORS else tense
	
	if tense is not None:
		return tense
		
	# Now check pattern.en tense
	tense = PAST    if tense_h(word, PAST) and not tense_h(word, PRESENT) and not tense_h(word, FUTURE) else tense
	tense = PRESENT if not tense_h(word, PAST) and tense_h(word, PRESENT) and not tense_h(word, FUTURE) else tense
	tense = FUTURE  if not tense_h(word, PAST) and not tense_h(word, PRESENT) and tense_h(word, FUTURE) else tense
	
	return tense
	

# Checks if a tense is possible for a given word using pattern.en
def tense_h(word, tense):
	return True if tense in tn(word) else False
	
	
# Examines the words in a VP and checks if there are any definite indicators of tense
def tense_indicator(words):
	for word in words:
		indicator = tense(word)
		if indicator is not None:
			return indicator
			
	return None


# Takes a list of VP chunks for a sentence and returns the counts of each tense in a tuple (past, present, future)
def tense_counts(vp_chunks):
	# If any word in VP chunk is in an Indicator, the entire phrase gets counted as that tense
	past, present, future = 0.0,0.0,0.0
	
	past 	= reduce(lambda x,y : x + (1 if tense_indicator(y) is PAST else 0), vp_chunks)
	present = reduce(lambda x,y : x + (1 if tense_indicator(y) is PRESENT else 0), vp_chunks)
	future  = reduce(lambda x,y : x + (1 if tense_indicator(y) is FUTURE else 0), vp_chunks)
	
	word_obj_list  = map(lambda x : x.words, chunk)
	word_list_flat = map(lambda x : map(lambda y : y.string, x), word_obj_list)
	
	return (past, present, future)
	

#
# Returns the number of verb agreement mistakes found
def mistakes(essay):
	essay.disambiguate_vbz()
	
	bigrams  = find_bigrams(essay)
	trigrams = find_trigrams(essay)
	errors   = 0.0
	
	for bigram in bigrams:
		errors += (1 if is_rule_violation(bigram, rules.VERB_BIGRAM_RULES) else 0)
		
	for trigram in trigrams:
		errors += (1 if is_rule_violation(trigram, rules.VERB_TRIGRAM_RULES) else 0)
	
	return errors / (len(bigrams) + len(trigrams))


#
# Returns the number of unique verbs in an essay
def unique_verbs(essay):
	unique_verbs = filter(lambda x : True if x[1] in rules.VERBS else False, essay.tags)
	
	return len(set(map(lambda x : x[0], unique_verbs)))


#
# #
# def plural(word):
# 	return True if pluralize(word) == word else False
	
	