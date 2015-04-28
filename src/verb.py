""" Maintained by Jordan Williams """

from pattern.en import tenses as tn, suggest, PRESENT, PAST, FUTURE

import rules

# Returns True if ngram is in violation of the supplied rule set
def is_rule_violation(ngram, rule_set):
	return True if ",".join(map(lambda x : x[1], ngram)) in rule_set else False


# Returns the error for tense similarity between sentences
def compute_tense_similarity_errors(essay):
	sentences 	= essay.parsetree
	sentence_vp_chunks = map(lambda x : x.verbs, sentences)
	tense_tuples = map(lambda x : tense_of_sentence(x), sentence_vp_chunks)
	
	# If any sentence contains PAST, PRESENT, and FUTURE tenses, it is an error
	errors = reduce(lambda x,y : x+y, map(lambda z : 1.0 if z[0] > 0 and z[1] > 0 and z[2] > 0 else 0.0, tense_tuples))
		
	return errors


# Returns true if a tag is a verb
def is_verb(tag):
	return True if tag in rules.VERBS else False
	

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
	verb_tags = map(lambda x : map(lambda y : y.words, x), verb_chunks)
	verbs = map(lambda x : map(lambda y : y.tag, [v for verbs in x for v in verbs]), verb_tags)
	
	# Grab head word of each chunk then filter out onlt verbs
	chunks = map(lambda x : x.chunks, essay.parsetree)
	
	vp_chunks = []
	for chunk in chunks:
		vp_chunks.append(filter(lambda x : x.type == "VP", chunk))

	return vp_chunks
	

# Returns the tense of a word if it is unambiguous
def tense_of_word(word):
	tense = None
	tag   = word.tag
	word  = word.string
		
	# Use wordnet suggestion if word is mispelled
	word = word if suggest(word)[0][1] == 1.0 else suggest(word)[0][0]
	
	# Check defined rules first
	tense = FUTURE if word in rules.FUTURE_INDICATORS else tense
	tense = PAST if word in rules.PAST_INDICATORS else tense
	
	if tense is not None:
		return tense
		
	# check pre-defined rules
	tense = PAST if tag in rules.PAST else tense
	tense = PRESENT if tag in rules.PRESENT else tense
	tense = FUTURE if tag in rules.FUTURE else tense
	
	if tense is not None:
		return tense
		
	# Now check pattern.en tense
	tense = PAST if tense_of_word_h(word, PAST) and not tense_of_word_h(word, PRESENT) and not tense_of_word_h(word, FUTURE) else tense
	tense = PRESENT if not tense_of_word_h(word, PAST) and tense_of_word_h(word, PRESENT) and not tense_of_word_h(word, FUTURE) else tense
	tense = FUTURE if not tense_of_word_h(word, PAST) and not tense_of_word_h(word, PRESENT) and tense_of_word_h(word, FUTURE) else tense
	
	return tense


# Checks if a tense is possible for a given word using pattern.en
def tense_of_word_h(word, tense):
	return True if tense in tn(word) else False


# Examines the words in a VP and checks if there are any definite indicators of tense
def tense_of_vp(words):	
	# Check modals
	modal_words = filter(lambda x : x.tag == "MD", words)
	
	if PAST in map(lambda x : tense_of_word(x), modal_words): return PAST
	if FUTURE in map(lambda x : tense_of_word(x), modal_words): return FUTURE
	if PRESENT in map(lambda x : tense_of_word(x), modal_words): return PRESENT
	
	# Check head of VP
	return tense_of_word(words[0].chunk.head)


# Takes a list of VP chunks for a sentence and returns the counts of each tense in a tuple (past, present, future)
def tense_of_sentence(vp_chunks):
	# If any word in VP chunk is in an Indicator, the entire phrase gets counted as that tense
	past, present, future = 0.0,0.0,0.0
	
	tense_counts = map(lambda x : tense_of_vp(x), vp_chunks)
	
	if tense_counts:
		past = reduce(lambda x,y : x + y, map(lambda z : 1 if z == PAST else 0, tense_counts))
		present = reduce(lambda x,y : x + y, map(lambda z : 1 if z == PRESENT else 0, tense_counts))
		future = reduce(lambda x,y : x + y, map(lambda z : 1 if z == FUTURE else 0, tense_counts))
	
		return (past, present, future)
	
	return (0, 0, 0)


# Returns the number of verb agreement mistakes found
def mistakes(essay):
	essay.disambiguate_vbz()
	essay.parse()
	
	bigrams = find_bigrams(essay)
	trigrams = find_trigrams(essay)
	ngram_errors = 0.0
	
	for bigram in bigrams:
		ngram_errors += (1.0 if is_rule_violation(bigram, rules.VERB_BIGRAM_RULES) else 0.0)
		
	for trigram in trigrams:
		ngram_errors += (1.0 if is_rule_violation(trigram, rules.VERB_TRIGRAM_RULES) else 0.0)
	
	return (ngram_errors / (len(bigrams) + len(trigrams))) + compute_tense_similarity_errors(essay)


# Returns the number of unique verbs in an essay
def unique_verbs(essay):
	unique_verbs = filter(lambda x : True if x[1] in rules.VERBS else False, essay.tags)
	
	return len(set(map(lambda x : x[0], unique_verbs)))
