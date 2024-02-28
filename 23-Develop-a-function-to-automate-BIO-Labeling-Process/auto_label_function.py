import pandas as pd 

#Master entity dictionary. 
master_dict = {"ORG": 
            {"provider", "providers", "distributor", "deployer", "operator", "notifying authority", "conformity assessment body", "notified body", "market surveillance authority", "digital innovation hubs", "testing experimentation facilities", "researchers", "importer", "the commission", "businesses", "government"},
            "PER": {"authorised representative", "competent authorities"}, "DAT": {"training data", "validation data", "testing data", "input data", "biometric data", "special categories of personal data", "sensitive operational data", "high quality datasets", "high quality data", "health data", "datasets"},
            "SYS": {"post-market monitoring system", "emotion recognition system", "biometric categorisation system", "remote biometric identification system", "real-time remote biometric identification", "post remote biometric identification system", "high-risk AI systems", "AI systems", "risk management system", "quality management system"},
            "ACT": {"placing on the market", "making available on the market", "putting into service", "substantial modification", "development", "data sharing", "training", "validation", "testing", "access to data", "provision of high-quality data", "bias detection", "bias correction", "post market monitoring", "automatic recording", "placed on the market", "put it into service", "evaluate", "interpretation of the outputs", "technical and scientific support"},
            "SPA": {"publicly accessible space", "European common data spaces", "European health data space"},
            "STA": {"harmonised standard", "state of the art"},
            "ALG": {"biometric identification", "biometric verification", "profiling", "artificial intelligence algorithms", "system behaviour"},
            "PRO": {"conformity assessment", "assessment", "evaluate", "human oversight measures", "governance framework"},
            "HAR": {"reasonably foreseeable misuse"},
            "MAR": {"CE marking of conformity", "CE marking"},
            "DOC": {"instructions for use", "common specification", "documentation", "Union harmonisation legislation"},
            "ETH": {"human oversight", "transparency", "public interest", "non-discriminatory", "trustful", "accountable", "privacy-preserving", "secure", "transparent", "trustworthy", "institutional governance", "fundamental rights and freedoms of natural persons", "public interest", "traceability", "compliance", "safety", "health", "Cybersecurity", "data poisoning"}


            }
#I opted to go with a dictionary of sets rather than lists as they have a lookup time of O(1)


'''
This function searches every key in the dictionary and
then checks if the lower case version of the current string is in the set of that master entity
if it finds a matching entity it will return it to the autolabel program, if not it will return false
'''
def dict_search (ner_tags, curr_string, curr_index, prefix):
    for entity in master_dict:
        if curr_string.lower() in master_dict[entity]:
            tag = prefix + str(entity)
            ner_tags[curr_index] = tag
            return str(entity)
    return "false"
 
 #Takes in token, list of tokens, and index of token to be split 
 #splits tokens with brackets/punctuation/whatever else and makes those seperate tokens,    
def punc_split(token, tokens, index, startpunc,endpunc):
    
    last_element = token[len(token)-1]
    first_element = token[0]
    #Checks if this is the root of the word
    root = True
    
    if first_element in ('(', '[', '{') and token not in ('(', '[', '{'):
        root = False
        startpunc +=1
        punc_split(token[1:len(token)], tokens, index, startpunc, endpunc)
        tokens.insert (index, first_element)
    if last_element in (',', ';', ':', ')', ']', '}') and token not in (',', ';', ':', ')', ']', '}') and root == True:
        root = False
        tokens.insert(index+1, last_element)
        punc_split(token[0:len(token)-1], tokens, index,startpunc, endpunc)
        
    if root == True:
        tokens[index] = token 
        
    return tokens
    
#This function works on the scale of a sentence it splits the sentence into tokens using space as the delimeter then assigns NER tags to each token
def auto_label(sentence):
    tokens = sentence.split()
    ner_tags = []
    
    #Splitting punctuation into seperate words for the sake of cleaner training data
    for token in tokens:
        ner_tags.append(0)
        #Filling Ner_tag array, since labelling function relies on tokens having a default ner_tag value 
        tokens = punc_split(token, tokens, tokens.index(token), 0, 0)
        
        ''' last_element = token[len(token)-1]
        secondlast_element = token[len(token)-2]
        index = tokens.index(token)
        first_element = token[0]
        filler_num = 0 #Keeps track of the amount of punctuation/brackers etc to know where to insert tokens
        if first_element in ('(', '[', '{') and token not in ('(', '[', '{'):
            if last_element in (')', ']', '}', ',', ';', ':') and token not in (')', ']', '}', ',', ';', ':'):
                token = token[1:len(token)-1]
                tokens.insert(index+1, token)
                tokens.insert(index+2, last_element)
                #If word doesnt end in bracket we just split it from the first bracket and let the last element detection handle the second
                #updating last element since previous last element was taken
                last_element = secondlast_element
            else:
                token = token[1:len(token)]
                tokens.insert(index+1, token) 
                
            tokens[index] = first_element
            filler_num +=1
            
        elif secondlast_element in (')', ']', '}', ',', ';', ':'):
            token = token[1:len(token)-2]
            tokens.insert(index+1, secondlast_element)
            filler_num+=1
            
        #if the tokens last element of the token is punctuation and if the entire token isnt just punctuation
        if  last_element in (',', ';', ':', ')', ']', '}') and token not in (',', ';', ':', ')', ']', '}'):
             #The punctuation mark is added in front of the token  
             tokens.insert(index+1+filler_num, last_element)
             #The punctuation mark is removed from the token and the altered token replaces the old one
             token = token[0:len(token)-1]
             tokens[index+filler_num] = token '''
             
    
    #Labelling loop
    for index in range (len(tokens)):
        #Loop that checks if ner_tag at the current token index == 0, if it is then run label, if not then skip
        if ner_tags[index] == 0:
            match = label(tokens, ner_tags, index, index, "" )
    return_list = []
    return_list.append(tokens)
    return_list.append(ner_tags)
    
    return return_list
        
'''
Recursive labelling function, 
it takes in the list of tokens, ner tags, current index and starting index along with the current string
It passes up the current string + the string stored in the current index of the tokens list 
then recursively calls itself on the next index of the tokens list until it reaches the end
by that point current string + string will be the start index + the rest of the sentence following it
the search_dict function is then called and attempts to match the current_string, if it cannot do so "false"
is returned which is recieved by the iteration of the function that called it, 
that function then itself attempts to match it's current string 
which would be from the start index to the current_index (rest of the sentence - 1 token)
if the match is found dict_search returns the entity name and the function recursively adds "I-" to it
returning to the start index which will add "B-" and finally return
if the match is not found even after solely the token in the start index is searched it will label itself as "O"
'''

def label(tokens, ner_tags, curr_index, start_index, curr_string):
    #Adding new word onto old one
    string = tokens[curr_index]
    if curr_index >= 511:
        return "false"
    #If starting word then the full string is equal to the word
    if curr_index == start_index:
        curr_string = string
        #Prefixes based on whether its the beginning of an entity
        prefix = "B-"
         
    else:
        curr_string += " " + string
        prefix ="I-"
        
    next_index = curr_index +1
    
    if next_index < len(tokens):
        found_match = label(tokens, ner_tags, next_index, start_index, curr_string)
    else:
        found_match = dict_search (ner_tags, curr_string, curr_index, prefix)
        if curr_index == start_index:
            if found_match == "false":
                tag = "O"
            else:
                tag = prefix + found_match          
            ner_tags[curr_index] = tag
        return found_match
    
    if found_match != "false":
        tag = prefix + found_match          
        ner_tags[curr_index] = tag
        return found_match      
    else:
        tag = dict_search (ner_tags, curr_string, curr_index, prefix)
        if curr_index != start_index:
            return tag
        else: 
            if tag == "false":
                ner_tags[curr_index] = "O"
            
            
def paragraph_to_labeled_sentences(paragraph):
    sentences = paragraph.split(".")
    tokens_list = []
    tags_list = []
     
    for sentence in sentences:
        #for the sake of context length and not hitting the recursion limit because the punctuation in the AI act draft is unique to say the least.
        if len(sentence) >= 511:
            
            long_sentence = ' '.join([str(word) for word in sentence])
            split_sentences = str(long_sentence.split(','))
            sentences += split_sentences
            
        return_list = auto_label(sentence)
        tokens_list.append(return_list[0])
        tags_list.append(return_list[1])
    
    return tokens_list, tags_list

#Reads from the ai act parsed by Dylans parsing function.              
with open ("C:/Users/Administrator.ADMINTR-S0JT5RL/Downloads/parsed-ai-act.txt", "r", encoding='utf-8') as ai_act:
    
    
    token_list, tags_list = paragraph_to_labeled_sentences(ai_act.read())
    #Creates column for tokens and column for tags, 
    df = pd.DataFrame(list(zip(token_list, tags_list)), columns = ['tokens', 'ner_tags'])
    #Outputs the tokens and ner tags, into training data jsonl
    with open('training-data.jsonl', mode ='w') as writer:
        writer.write(df.to_json(orient='records', lines=True, force_ascii=False))