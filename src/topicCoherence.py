""" Maintained by Jason Duetsch """

def score(essay):
    whole_tags = essay.tags
    
    tags = list()
    
    #just store tags as one list for simplicity
    for i in range(0,len(whole_tags)):
        tags.append(whole_tags[i][0])
    
    #convert to string 
    tags2=str(tags)
    
    
    pollution = 0.0
    pollution+=tags2.count('pollution')
    pollution+=tags2.count('Pollution')
    pollution+=tags2.count('polluting')
    pollution+=tags2.count('Polluting')
    pollution+=tags2.count('pollutes')
    pollution+=tags2.count('Pollutes')
    pollution+=tags2.count('Polluted')
    pollution+=tags2.count('polluted')
    
    score1 = pollution/len(whole_tags)
    
    more_less = 0.0
    more_less+=tags2.count('more')
    more_less+=tags2.count('More')
    more_less+=tags2.count('less')
    more_less+=tags2.count('Less')
    
    score2 = more_less/len(whole_tags)
    
    return(score1+score2)