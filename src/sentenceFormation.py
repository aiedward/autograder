"""Maintained by Jason Deutsch"""

import stanfordParser
import numpy as np
import re
from nltk.parse import stanford

"""
Returns the percentage of incomplete sentences.
Fragments, clauses...

ROOT -> 
    SBAR

FRAG

ROOT ->
    NP
    SBAR (needs a preceding VP)

"""
def mistakes(essay):
    return fix(essay)
    
    
def fix(essay):
    parser = stanford.StanfordParser(model_path="lib/englishPCFG.ser.gz")
    sentence_list = essay.text.split("\n")

    # Split most likely makes the last element an empty string
    try:
        sentence_list.remove("")
    except:
        pass
        
    sentences = list(parser.raw_parse_sents(sentence_list))
    trees = map(lambda x : x.next(), sentences)
    
    frag_errors = 0.0
    sbar_errors = 0.0
    
    for tree in trees:
        for t in tree.subtrees():
            frag_errors += 1 if t.label().encode('utf8') == "FRAG" else 0
            sbar_errors += 1 if t.label().encode('utf8') == "SBAR" else 0
            
    return frag_errors / len(trees)
