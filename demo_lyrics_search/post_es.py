#insert lyrics to elasticsearch
import os
import sys
import json

import requests

headers = {
    'Content-Type': 'application/json',
}

params = (
    ('pretty', 'true'),
)

lyrics_file = '/home/madhavi/Documents/demo_lyrics_search/demo_lyrics_search/spiders/sin_oldies.json'
#file = json.loads(open().read(), strict=False)



i = 1
all_lines=[]

with open(lyrics_file) as f:
	for line in f:

		line = json.loads(line,strict=False)

		lyric_text = line['lyric-text']
		title = line['title']
		key = line['key']
		beat = line['beat']
		artist_list = line['artist_list']
		genre_list =  line['genre_list']
		lyrics_by_list = line['lyrics_by_list']
		musics_by_list = line['musics_by_list']
		visits =  int(line['visits'])

		if len(artist_list) >0 :

			data = {
				"lyric-text":lyric_text,
				"title":title,
				"key":key,
				"beat":beat,
				"artist_list":artist_list,
				"genre_list":genre_list,
				"lyrics_by_list":lyrics_by_list,
				"musics_by_list":musics_by_list,
				"visits":visits
			}

			if line not in all_lines:
				first_cmd = 'http://localhost:9200/lyrics/_doc/{}?pretty=true'.format(str(i))
				res = requests.post(first_cmd, headers=headers, data=json.dumps(data))
				print('res = ',res)
				all_lines.append(line)
				i = i+1



print("Posted {} songs".format(str(i-1)))