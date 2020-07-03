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

		line = json.loads(line,strict=False)

		lyric_text = line['lyric-text']
		linelist = lyric_text.split('\n')

		for ele in linelist:
			all_words.extend(ele.split(' '))


filename = 'lyricswords'
joblib.dump(all_words, filename)
