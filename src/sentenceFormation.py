import os
from nltk.parse import stanford
os.environ['JAVAHOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['JAVA_HOME'] = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
os.environ['STANFORD_PARSER'] = 'lib'
os.environ['STANFORD_MODELS'] = 'lib'

"""
Returns the percentage of incomplete sentences.
Fragments, clauses...

ROOT -> 
    SBAR
    S
    S (must have 2 or more S following SBAR)

FRAG

ROOT ->
    NP
    SBAR (needs a preceding VP)

"""
def mistakes(essay):
    number_of_fragments(essay)
    return 0

def number_of_fragments(essay):
    parser = stanford.StanfordParser(model_path="lib/englishPCFG.ser.gz")
    sentence_list = essay.text.split(".\n")
    
    # Split most likely makes the last element an empty string
    try:
        sentence_list.remove("")
    except:
        pass
    
    sentences = list(parser.raw_parse_sents(sentence_list))
    trees = map(lambda x : x.next(), sentences)

    for tree in trees:
        print tree
        print ""