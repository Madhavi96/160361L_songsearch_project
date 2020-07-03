import os
import sys
import json
import joblib

lyrics_file = '/home/madhavi/Documents/demo_lyrics_search/demo_lyrics_search/spiders/sin_oldies.json'
#file = json.loads(open().read(), strict=False)



i = 1
all_words=[]

with open(lyrics_file) as f:
		for line in f:
			li = []
			line = json.loads(line,strict=False)

			title = line['title']

			if title not in all_words:
				all_words.append(title)
				
			

with open('titles.txt', 'a') as t:   
	for ele in all_words:     
		t.write(ele+'\n') 

