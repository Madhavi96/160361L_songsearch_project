import sys
import os
from googletrans import Translator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet as wn
'''
import nltk
nltk.download()
'''
#get average vector for sentence 1
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
#print(nouns)
'''
translator =  Translator()

word1 = "හොඳම"
word2 = "ටොප"


en_term1 = translator.translate(word1,src='si',dest='en').text.lower()
en_term2 = translator.translate(word2,src='si',dest='en').text.lower()
'''
print('clarence' in nouns)
'''
print(en_term1,en_term2)

print(en_term1 in nouns)
en_term1=en_term1+".n.01"
en_term2=en_term2+".n.01"

w1 = wn.synset(en_term1)
w2 = wn.synset(en_term2)

s = w1.path_similarity(w2)  
print(s)
'''
