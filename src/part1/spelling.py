""" Maintained by Jason Duetsch """

import enchant #for spell check, nltk wordnet says words like "how" are misspelled

def mistakes(essay_obj):
    
    essay = essay_obj.text_list
    
    #load dictionary using enchant library
    dictionary = enchant.Dict("en_US")
    misspelled_words = 0.0 
    
    #take only unique words of essay
    #essay = list(set(essay))    
   # print(len(essay))
    ##join contractions
    
    cntrc_list = []    
    
    for i in range(0,len(essay)):
       # print i
        string = essay[i]
        if(string.count("'") !=0): #if contraction
            #print('string')
            #print(string)
            #print(essay[i-1])
            #print(essay[i])
            essay[i-1] = essay[i-1]+string #add contraction             
            cntrc_list.append(string)
            
    #remove -> right contraction part
    for i in range(0,len(cntrc_list)):
        if cntrc_list[i] in essay:
            essay.remove(cntrc_list[i])
     
    #take only unique words of essay
    essay = list(set(essay))          
            
           
    ###delete punctuation so that the spell checker doesn't count them as errors
     
    punctuation_list = [",","?","(",")","-","...", ".''", ",''", ">", "<", ":", "..", ";"]
    removal_list = []

    
    # find all punctuation in essay and add to removal list
    for word in range(0,len(essay)):
        for i in range(0,len(punctuation_list)):
            if essay[word] == punctuation_list[i]:
                removal_list.append(punctuation_list[i]) # add punctuation list to removal list
        
   
    
    ## Finally remove puncuation from grammer
    for i in range(0,len(removal_list)):
        essay.remove(removal_list[i])
    # print('removal list' ,removal_list)
  
    #if it can't find the word, count it as a misspelled word
    for i in range(0,len(essay)):
        if dictionary.check(essay[i]) == False:
            #print(essay[i])
            misspelled_words += 1
    #print('misspelled_words')
    #print(misspelled_words)
   #return percentage of misspeled words
    return(misspelled_words/len(essay))