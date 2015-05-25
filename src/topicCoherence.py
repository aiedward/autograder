""" Maintained by Jason Duetsch """

def score(essay):
    whole_tags = essay.tags
    
    tags = list()
    
    #just store tags as one list for simplicity
    for i in range(0,len(whole_tags)):
        tags.append(whole_tags[i][0])
    
    #convert to string 
    tags2=str(tags)
    
    
    num_sentences = tags2.count('.')

    relevent_word_count = 0.0
    
    #country category    
    relevent_word_count+=tags2.count('Country')
    relevent_word_count+=tags2.count('Countries')
    relevent_word_count+=tags2.count('Developed')
    relevent_word_count+=tags2.count('Developing')
    
    relevent_word_count+=tags2.count('country')
    relevent_word_count+=tags2.count('countries')
    relevent_word_count+=tags2.count('developed')
    relevent_word_count+=tags2.count('developing')
    
    #more/less category
    relevent_word_count+=tags2.count('more')
    relevent_word_count+=tags2.count('More')
    relevent_word_count+=tags2.count('less')
    relevent_word_count+=tags2.count('Less')
    
    #road category
    relevent_word_count+=tags2.count('road')
    relevent_word_count+=tags2.count('Road')
    relevent_word_count+=tags2.count('Roads')
    relevent_word_count+=tags2.count('roads')
    relevent_word_count+=tags2.count('highway')
    relevent_word_count+=tags2.count('Highways')
    relevent_word_count+=tags2.count('Highway')
    relevent_word_count+=tags2.count('highways')
    
    #pollution category
    relevent_word_count+=tags2.count('pollution')
    relevent_word_count+=tags2.count('Pollution')
    relevent_word_count+=tags2.count('polluting')
    relevent_word_count+=tags2.count('Polluting')
    relevent_word_count+=tags2.count('pollutes')
    relevent_word_count+=tags2.count('Pollutes')
    relevent_word_count+=tags2.count('Polluted')
    relevent_word_count+=tags2.count('polluted')
    
    #future category
    relevent_word_count+=tags2.count('future')
    relevent_word_count+=tags2.count('Future')
    
    #oil category
    relevent_word_count+=tags2.count('oil')
    relevent_word_count+=tags2.count('Oil')
    relevent_word_count+=tags2.count('petroleum')
    relevent_word_count+=tags2.count('Petroleum')
    relevent_word_count+=tags2.count('petrol')
    relevent_word_count+=tags2.count('Petrol')
    relevent_word_count+=tags2.count('gasoline')
    relevent_word_count+=tags2.count('Gasoline')
    relevent_word_count+=tags2.count('gas')
    relevent_word_count+=tags2.count('Gas')
    
    #cars category
    
    relevent_word_count+=tags2.count('cars')
    relevent_word_count+=tags2.count('Cars')
    relevent_word_count+=tags2.count('car')
    relevent_word_count+=tags2.count('car')
    relevent_word_count+=tags2.count('vehicle')
    relevent_word_count+=tags2.count('Vehicle')
    relevent_word_count+=tags2.count('vehicles')
    relevent_word_count+=tags2.count('Vehicles')
    relevent_word_count+=tags2.count('auto')
    relevent_word_count+=tags2.count('Auto')
    relevent_word_count+=tags2.count('automobile')
    relevent_word_count+=tags2.count('Automobile')
    relevent_word_count+=tags2.count('Automobiles')
    relevent_word_count+=tags2.count('automobiles')
    
    if num_sentences == 0:
        return relevent_word_count/(len(whole_tags))
    
    return(relevent_word_count/num_sentences)