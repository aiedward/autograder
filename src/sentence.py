""" Maintained by Jason Duetsch """

import verb

def length(essay_obj):
    #number of unique tags    
    tags = essay_obj.tags
    num_unique_tags = len( set(tags) )
    
    #number of sentences
    total_sentences = 0.0
    for i in range(0, len(tags)):
        if tags[i][1] == '.':
            total_sentences += 1
              
    return (total_sentences + 0.1 * num_unique_tags) + verb.unique_verbs(essay_obj)