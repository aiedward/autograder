from pattern.en import Sentence, pluralize, lemma
from rules import PRONOUN_TAGS, PRONOUN_GENDER, PRONOUN_IGNORE, PRONOUN_PLURAL, PRONOUN_SINGULAR
import genderPredictor as gp

CONTINUE = 1,
RETAIN = 2
SMOOTH = 3
ROUGH = 4

SUBJECT = 1
NOMINAL = 2
OBJECT = 3
INDIRECT = 4

gender_predictor = gp.genderPredictor()
gender_predictor.trainAndTest()


class Sentence:
    def __init__(self, sentence):
        self.tree = sentence
        self.backward_center = None
        self.forward_centers = []
        self.previous = None
        self.pronouns = []
        self.resolutions = []
    
class Pronoun:
    def __init__(self, word):
        self.word = word
        self.resolution = None
        
class ForwardCenter:
    
    def __init__(self, word, rank):
        self.word = word
        self.rank = rank


def mistakes(essay):
    return compute_ambiguity(essay)


# Returns a metric that determines whether pronouns can be resolved via centering
def compute_ambiguity(essay):
    sentences = map(lambda x : Sentence(x), essay.parsetree.sentences)

    for prev, curr in zip(sentences, sentences[1:]):
        curr.previous = prev
    
    unresolved = 0.0
    
    for sentence in sentences:
        sentence.pronouns = find_pronouns(sentence.tree)
        
        # No pronouns to resolve
        if not sentence.pronouns:
            continue
        
        find_forward_centers(sentence)
        
        # Double check that no pronouns got added
        if sentence.forward_centers:
            filter(lambda x : x and not is_pronoun(x), map(lambda y : y.word, sentence.forward_centers))
        
        find_backward_center(sentence)
        
        for pronoun in sentence.pronouns:
            if not resolve(sentence, pronoun):
                unresolved += 1
        
    return unresolved / reduce(lambda x,y : x + y, map(lambda z : len(z.pronouns), sentences))
    

# Find transition for a given pronoun
def resolve(sentence, pronoun):
    # Find transition states
    transitions = map(lambda x : (pronoun, x, get_transition(sentence, pronoun, x)), sentence.forward_centers)
    transitions = filter(lambda x : x[2] is not None, transitions)
    
    # Primary sort on transition, secondary sort on proximity
    transitions = sorted(transitions, key = lambda x : (x[2], get_distance(pronoun.word, x[1].word)))
    
    if transitions:
        for transition in transitions:
            sentence.resolutions.append(transition[1])
            pronoun.resolution = transition[1]
            
            if sentence.backward_center is None:
                sentence.backward_center = transition[1]
            
            return True
        
    return False
    
    

def get_transition(sentence, pronoun, center):
    if not is_compatable(pronoun, center):
        return None
    
    if is_previous_backward_center(sentence, center):
        if is_preferred_center(sentence, center):
            return CONTINUE
        return RETAIN
        
    else:
        if is_preferred_center(sentence, center):
            return SMOOTH
        return ROUGH
    
    
# Returns True if backward center of U_n == backward center of U_n+1
def is_previous_backward_center(sentence, center):
    if sentence.previous is None or sentence.previous.backward_center is None:
        return True
        
    return True if sentence.previous.backward_center == center else False
    
    
# Returns True if backward center of U_n+1 == preferred center of U_n+1
def is_preferred_center(sentence, center):
    if sentence.forward_centers:
        return True if sentence.forward_centers[0].word == center else False
        
    return False
    

# Finds the backward center for an utterance
def find_backward_center(sentence):
    if sentence.previous and sentence.previous.forward_centers:
        sentence.backward_center = sentence.previous.forward_centers[0].word
        
    return None
    

# Finds the forward centes for an utterance
def find_forward_centers(sentence):
    for func in [find_subjects, find_existential_predicate_nominals, find_objects, find_indirect_objects, find_prepositions]:
        sentence.forward_centers.extend(func(sentence))
    

# Finds all of the pronouns in a sentence
def find_pronouns(sentence):
    return map(lambda y : Pronoun(y), filter(lambda x : x.tag in PRONOUN_TAGS and x.string.lower() not in PRONOUN_IGNORE, sentence.words))


# Finds the subject of a sentence
def find_subjects(sentence):
    subjects = map(lambda x : ForwardCenter(x.head, SUBJECT) if x else None, sentence.tree.subjects)
    subjects = filter(lambda x : x and not is_pronoun(x.word) and not is_in_pnp(sentence, x.word.phrase), subjects)
    
    return subjects if subjects else []
    

# Finds the existential nominals in a sentence
def find_existential_predicate_nominals(sentence):
    centers = map(lambda y : ForwardCenter(y.head, NOMINAL), filter(lambda x : x.tag == "NP" and contains_existential(x), sentence.tree.phrases))
    
    return filter(lambda x : not is_in_pnp(sentence, x.word.phrase) and x.word.string not in map(lambda y : y.word.string, sentence.forward_centers), centers)
    

# Finds the objects in a sentence
def find_objects(sentence):
    centers =  map(lambda x : ForwardCenter(x.head, OBJECT), sentence.tree.objects)
    
    return filter(lambda x : x.word.string not in map(lambda y : y.word.string, sentence.forward_centers), centers)
    

# Finds the indirect objects in a sentence
def find_indirect_objects(sentence):
    return []
    

# Finds the prepositions in a sentence
# Might not use this, not necessary
def find_prepositions(sentence):
    return []
    
    
# Checks contraints on a pronoun and its proposed resolution
def is_compatable(pronoun, resolution):
    if not pronoun.word or not resolution.word:
        return False
    
    # Resolution must come before pronoun and not be too far away
    if pronoun.word.sentence.id - resolution.word.sentence.id > 2 or pronoun.word.sentence.id - resolution.word.sentence.id < 0:
        return False
        
    if resolution.word.index > pronoun.word.index:
        return False
    
    # Check gender agreement
    if pronoun.word.string.lower() in PRONOUN_GENDER:
        if gender_predictor.classify(pronoun.word.string) != gender_predictor.classify(resolution.word.string):
            return False
            
    # Check number agrrement
    if is_plural(pronoun.word.string) != is_plural(resolution.word.string):
        return False
        
    # Check it isn;t resolving to another pronoun
    if resolution.word.tag in PRONOUN_TAGS:
        return False
    
    return True
    

# Retruns True if a word is in its plural form
def is_plural(word):
    if word.lower() in PRONOUN_PLURAL:
        return True
        
    if word.lower() in PRONOUN_SINGULAR:
        return False
    
    return True if pluralize(lemma(word.lower())) == word.lower() else False
    

# Returns the distance between 2 pattern.en Words
def get_distance(word1, word2):
    return abs(word2.index - word1.index)
    

def is_in_pnp(sentence, pronoun):
    pronoun_bounds = (pronoun.start, pronoun.stop)
    pnp_bounds = map(lambda x : (x.start, x.stop), sentence.tree.pnp)
    
    if not pnp_bounds:
        return False
    
    if pronoun_bounds[0] >= pnp_bounds[0] and pronoun_bounds[1] <= pnp_bounds[1]:
        return True
        
    return False
    

def is_pronoun(word):
    return True if word.tag in PRONOUN_TAGS or word.string.lower() in PRONOUN_IGNORE or word.string.lower() in PRONOUN_GENDER else False
    

# Retruns True if a phrase contains an existential
# Only pass NP to this function
def contains_existential(phrase):
    return True if filter(lambda x : x.tag == "DT", phrase.words) else False
    