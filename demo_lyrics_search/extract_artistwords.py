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

			artist = line['artist_list']
			musicby = line['musics_by_list']
			lyricsby = line['lyrics_by_list']

			li.extend(artist)
			li.extend(musicby)
			li.extend(lyricsby)		

			for ele in li:
				ele=ele.replace('.','\n')
				newli = ele.split(' ')
				for item in newli:
					if item not in all_words:
						all_words.append(item)

with open('artists.txt', 'a') as art_f:   
	for ele in all_words: 
    
		art_f.write(ele+'\n') 

