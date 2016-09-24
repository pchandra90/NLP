
# coding: utf-8

# In[ ]:

import sys
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from colorama import Fore, Back
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
person = wn.synset('person.n.01')
place = wn.synset('place.n.01')
time = wn.synset('time.n.01')
month = wn.synset('month.n.01')
year = wn.synset('year.n.01')
day = wn.synset('day.n.01')
date = wn.synset('date.n.01')

from nltk.corpus import stopwords
stopwords = stopwords.words('english')
stopwords.append("'s")



# In[ ]:

AV = ['is', 'am', 'are', 'can', 'cannot', 'could', "couldn't", 'dare', 'may', 'might', 'must', 
      'need', 'ought', 'shall', 'should', "shouldn't", 'will', 'would', "won't", "wouldn't", 
      "don't", "doesn't", "hasn't", "haven't"]

AVE = ['do', 'does']
AVH = ['has', 'have']

WHAT = ['what', 'which']
WHEN = ['when']
WHO = ['who', 'whom', 'whose']


# In[ ]:

def time_similarity(word):
    return max(time.lin_similarity(word, semcor_ic), 
              month.lin_similarity(word, semcor_ic),
              year.lin_similarity(word, semcor_ic), 
              day.lin_similarity(word, semcor_ic), 
              date.lin_similarity(word, semcor_ic))
    


# In[ ]:

def my_tag_pos(list):
    tagged_list = []   
    for i in range(len(list)):
        word = list[i]
        if word.lower() in WHAT:
            tagged_list.append((word, 'WHAT'))
        elif word.lower() in WHEN:
            tagged_list.append((word, 'WHEN'))
        elif word.lower() in WHO:
            tagged_list.append((word, 'WHO'))
        elif word.lower() in AV:
            tagged_list.append((word, 'AV'))
        elif word.lower() in AVE and (i == 0 or list[i-1] == ',' 
                                      or nltk.pos_tag([list[i-1]])[0][1][0] == 'W'):
            tagged_list.append((word, 'AV'))
        elif word.lower() in AVH and (i == 0 or list[i-1] == ',' 
                                      or nltk.pos_tag([list[i-1]])[0][1][0] == 'W'):
            tagged_list.append((word, 'AV'))
        else:
            tagged_list.append((word, 'NULL'))
    
    return tagged_list
            
    


# In[ ]:

def tag_pos(sent_qus):
    words = word_tokenize(sent_qus)
    tag_pos_my_tag = my_tag_pos(words)
    tag_pos_nltk_tag = nltk.pos_tag(words)
    tagged = []
    for i in range(len(tag_pos_my_tag)):
        word, tag = tag_pos_my_tag[i]
        if tag == 'NULL':
            tag = tag_pos_nltk_tag[i][1]
        tagged.append((word, tag))
            
    return tagged


# In[ ]:

def find_type(ques_sent):
    tagged_list = tag_pos(ques_sent)
    word_token = word_tokenize(ques_sent)
    dict_type = {'Affirmation': False, 'What': False, 'When': False, 'Who': False}
    i = 0
    while i < len(word_token):
        if tagged_list[i][1] is 'AV':
            if 'or' not in word_token:
                dict_type['Affirmation'] = True
                break
            elif 'any' in word_token or 'either' in word_token:
                dict_type['Affirmation'] = True
                break
            else:
                dict_type['What'] = True
                break
        
        elif tagged_list[i][1] is 'WHO':
            dict_type['Who'] = True
            break
        
        elif tagged_list[i][1] is 'WHEN':
            dict_type['When'] = True
            break
        
        elif tagged_list[i][1] is 'WHAT':
            if 'location' in ques_sent.lower() or 'place' in ques_sent.lower():
                break
            elif 'time' in ques_sent.lower() or 'date' in ques_sent.lower():
                dict_type['When'] = True
                break
            elif 'the name of' in ques_sent.lower() or 'the names of' in ques_sent.lower():
                words_without_stopwords = [w for w in word_token if w.lower() not in stopwords]
                tagged_without_stopwords = nltk.pos_tag(words_without_stopwords)
                try:
                    j = words_without_stopwords.index('name')+1
                except:
                    #print(Fore.GREEN + str(tagged_without_stopwords) + Fore.RESET)
                    j = words_without_stopwords.index('names')+1 
                while j < len(words_without_stopwords):
                    if tagged_without_stopwords[j][1][:2] == 'NN':
                        word_noun = tagged_without_stopwords[j][0]
                        break
                    j+=1
                
                try:
                    ti = word_token.index(word_noun)
                    if((ti+1) < len(word_token) and word_token[ti+1] in WHO):
                        dict_type['Who'] = True
                        break
                        
                    word_noun = wn.synsets(word_noun)[0]
                    person_s = person.lin_similarity(word_noun, semcor_ic)
                    place_s = place.lin_similarity(word_noun, semcor_ic)
                    if (person_s > place_s) and person_s > 0.2:
                        dict_type['Who'] = True
                        break
                    else:
                        dict_type['What'] = True
                        break
                        
                except:
                    #print(Fore.YELLOW + str(word_noun) + Fore.RESET)
                    dict_type['What'] = True
                    break
                    
            elif ((i+2) < len(tagged_list)) and tagged_list[i+1][1][:2] == 'NN'and tagged_list[i+2][1][:2] == 'VB':
                word_noun = tagged_list[i+1][0]
                try:
                    word_noun = wn.synsets(word_noun)[0]
                    person_s = person.lin_similarity(word_noun, semcor_ic)
                    time_s = time_similarity(word_noun)
                    if person_s >= 0.2:
                        dict_type['Who'] = True
                        break
                    elif time_s >= 0.2:
                        dict_type['When'] = True
                        break
                    else:
                        dict_type['What'] = True
                        break 
                        
                except:
                    #print(Fore.RED + str(word_noun) + Fore.RESET)
                    dict_type['What'] = True
                    break
                    
            else:
                dict_type['What'] = True
                break
                
        elif i >= (len(word_token) -1):
            break
        
        else:
            for k in range(i+1,len(word_token)):
                if tagged_list[k][1] == 'WHAT':
                    i = k
                    break
                elif tagged_list[k][1] == 'WHO':
                    i = k
                    break
                elif tagged_list[k][1] == 'WHEN':
                    i = k
                    break
                elif tagged_list[k][1] == ',':
                    i = k+1
                    break
                elif k+1 >= len(word_token):
                    i = k+1
                
            
    return dict_type
                    


# In[ ]:

file = input("Enter the name of questions file (.txt format): ")
index = file.find('.txt', -4)
if index == -1:
    file = file + '.txt'
try:
    questions = open(file, 'r').read()
except:
    print(file + ' not found. exittng...')
    sys.exit()

ques_list = sent_tokenize(questions)
print('Nos. of questions: {0}'.format(len(ques_list)) )
total_printed = 0
FROM = 0
TO = len(ques_list)
for q in range(FROM, TO):
    dict_type = find_type(ques_list[q])
    if dict_type['Affirmation'] is True:
        print(Fore.GREEN + ques_list[q] + ' Type: ' + 'Affirmation' + Fore.RESET )
        total_printed+=1
    elif dict_type['What'] is True:
        print(Fore.CYAN + ques_list[q] + ' Type: ' + 'What' + Fore.RESET )
        total_printed+=1
    elif dict_type['When'] is True:
        print(Fore.BLUE + ques_list[q] + ' Type: ' + 'When' + Fore.RESET )
        total_printed+=1
    elif dict_type['Who'] is True:
        print(Fore.MAGENTA + ques_list[q] + ' Type: ' + 'Who' + Fore.RESET )
        total_printed+=1
    else:
        print(Fore.RED + ques_list[q] + ' Type: ' + 'Unknown' + Fore.RESET )
        total_printed+=1
        
    
    
print('Total printed: {0}'.format(total_printed))

           

