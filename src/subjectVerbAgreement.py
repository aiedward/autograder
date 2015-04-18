def mistakes(essay_obj):
	tags = [] 
	whole_tags = essay_obj.tags

	#just store tags as one list for simplicity
	for i in range(0,len(whole_tags)):
		tags.append(whole_tags[i][1])
	
	#convert to string 
	tags2=str(tags)

	##re tag the PRP to include specific PRP as plural vs singular
	#PRPsi = I, you, they, we
	#PRPpl = He she it

	PRPsi_list = ['i','you','they','we','I','You','They','We'] 
	PRPpl_list = ['he','she','it','He','She','It']

	pronoun_errors = 0.0


	#calculate pronoun errors for PRPsi singular list
	for i in range(0,len(whole_tags)-1):
		for j in range(0,len(PRPsi_list)):
			if whole_tags[i][0] == PRPsi_list[j] and whole_tags[i+1][1] == 'VBZ':
				# if in PRPPsi list and VBZ is the following tag
				pronoun_errors+=1
  
  
	# calculate pronoun errors for PRPpl plural list
	for i in range(0,len(tags)-1):
		for j in range(0,len(PRPpl_list)):
			if whole_tags[i][0] == PRPpl_list[j] and whole_tags[i+1][1] == 'VBP':
				# if in PRPPpl list and VBP is the following tag
				pronoun_errors+=1
			
			if whole_tags[i][0] == PRPpl_list[j] and whole_tags[i+1][1] == 'VB':
				# if in PRPPpl list and VB is the following tag
				pronoun_errors+=1
				
	# check verb tense
	vb_count = 0.0
	vb_count+=tags2.count("'NNP', 'VBP'") #good rule
	vb_count+=tags2.count("'NNPS', 'VBZ'") #good rule
	vb_count+=tags2.count("'NN', 'VBP'")    # good rule
	vb_count+=tags2.count("'NN', 'VB'")     # good rule
	#vb_count+=tags2.count("'NN', 'VBG'")    tense rule missing llama is eating -> missing is

	#vb_count+=tags2.count("'NN', 'VBN'")  # tense rule the llama has easten -> missing has
	vb_count+=tags2.count("'NNS', 'VBZ'") # good rule
	#vb_count+=tags2.count("'NNS', 'VBG'") tense rule the llamas are eating -> misssing are
	#vb_count+=tags2.count("'NNS', 'VBN'") tense rule the llamas have eaten 

	# new rules
	vb_count+=tags2.count("'NNP', 'VB'")
	vb_count+=tags2.count("'NNS', 'WDT', 'VBZ'")
	vb_count+=tags2.count("'NN', 'WDT', 'VB'")
	vb_count+=tags2.count("'NN', 'WDT', 'VBP'")

	return(vb_count+pronoun_errors) / len(tags)