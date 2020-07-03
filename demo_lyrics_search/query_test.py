import sys
import os

import os
import sys
import json
import requests

from googletrans import Translator

adjective_list = ['best','popular','top','good','better']
song_synonym_list = ['song','songs']
genre_list = ['old','byla','classic','duet','pair','movie','film','inspirational','exemplary','group','new']
genre_list.extend(['පැරණි','බයිලා','ක්ලැසික්','යුගල','චිත්‍රපට','පොප්','නව','ආදර්ශමත්','කණ්ඩායම්','අලුත්'])

counts = ['one','two','three','four','five','six','seven','eight','nine','ten','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred']
count_dict = {
	'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'twenty':20,'thirty':30,'fourty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90,'hundred':100

}


artistwords = []
titlewords=[]

with open('artists.txt') as art_f:   
	lines = art_f.readlines()
	for ele in lines:
		if ele.strip() != '\n':     
			artistwords.append(ele.strip()) 


with open('titles.txt') as t:   
	lines = t.readlines()
	for ele in lines:
		titlewords.append(ele.strip()) 

def check_genre(word):
	for ele in genre_list:
		w = [w for w in set(word) if w != ' ']

	
		g =  [w for w in set(ele)]

		sim = len(set(w) & set(g)) / float(len(set(w) | set(g))) * 100
		if sim>60:
			return True
		
	return False

def get_lyrics(words,view_range):
	headers = {
    'Content-Type': 'application/json',
	}

	params = (
	    ('pretty', 'true'),
	)



	translator =  Translator()

	



	#words = "ක්ලැරන්ස් පැරණි හොඳම ගීත දහය"
	words = words.replace(',',' ')
	word_li = words.split(' ')

	en_word_li = [ translator.translate(word,src='si',dest='en').text.lower() for word in word_li]


	search_in_genre = []
	search_in_visits = False
	remaining_words = [] #search in lyrics,artists,musis,lyricsby
	search_in_all_artists=[]
	search_in_titles = []

	count = None

	for i in range(len(en_word_li)):
		word = en_word_li[i]
		si_word=word_li[i]
		if si_word in artistwords:
			search_in_all_artists.append(si_word)

		elif check_genre(word) or check_genre(si_word):
			#check the keyword in genres
			search_in_genre.append(si_word)

		elif word in adjective_list:
			#sort by views(filter)
			search_in_visits= True

		elif word in song_synonym_list:
			#do nothing
			pass
		elif word in counts:
			count = count_dict[word]

		else:
			#artist/lyrics_by/music_by/ lyrics
			remaining_words.append(si_word)

	remaining = " ".join(remaining_words)

	rem_count = 0

	if len(remaining_words)>0:
		for ele in titlewords:
			if remaining in "**"+ele+"**":
				rem_count += 1
		if rem_count>0:
			search_in_titles.append(remaining)
			remaining_words = []

		


	print(rem_count)




	first_cmd = 'http://localhost:9200/lyrics/_search?size=1000&pretty=true'
	query = {}



	must_list=[]
	if len(search_in_genre) >0:

		ele = " ".join(search_in_genre)
		wild_ele="*"
		for i in ele:
			wild_ele+=i+"*"
		wild_ele+="*"

		

		append_gen = {"query_string": {"query":wild_ele,"fields":["genre_list"]}}

		must_list.append(append_gen)

	if len(search_in_all_artists) >0:
		ele = " ".join(search_in_all_artists)
		ele="*"+ele+"*"

		remain_li = []
		
		append_art =  {"query_string": {"query": ele,"fields":["artist_list","musics_by_list","lyrics_by_list"]}}

		must_list.append(append_art)

	if len(search_in_titles) >0:

		ele = " ".join(search_in_titles)
		#make this a term query
		append_gen = {"query_string": {"query":ele,"fields":["title"]}}

		must_list.append(append_gen)

	if len(search_in_titles) ==0 and len(remaining_words)>0:
		ele = " ".join(remaining_words)
		ele="*"+ele+"*"

		append_rem = {"query_string": {"query":ele,"fields":["lyric-text"]}}

		must_list.append(append_rem)

	if view_range != '':

		if view_range == "1":
			range_val = [{"range":{"visits" : {"gte" : 0 }}},{"range":{"visits" : {"lte" : 2000 }}}]
		if view_range == "2":
			range_val = [{"range":{"visits" : {"gte" : 2000 }}},{"range":{"visits" : {"lte" : 4000 }}}]
		if view_range == "3":
			range_val = [{"range":{"visits" : {"gte" : 4000 }}},{"range":{"visits" : {"lte" : 6000 }}}]
		if view_range == "4":
			range_val = {"range":{"visits" : {"gte" : 6000 }}}

		range_q = {"bool":{"filter":range_val}}
		must_list.append(range_q)






	s_query = {"query" : {"bool": {"must": must_list}},"sort": { "_score": { "order": "desc" }}}
	print(s_query)

	#tst ={"query":{"bool":{"should":[{"term":{"genre_list":"පැරණි"}}]}}}

	res = requests.get(first_cmd, headers=headers, data=json.dumps(s_query))

	response = json.loads(res.text)
	if response['hits']['total']['value'] == 0:
		return ["No Results"]
	yields = response['hits']['hits']
	yield_li = []

	for item in yields:
		yield_li.append(item['_source'])

	



	if search_in_visits:
		yield_li = sorted(yield_li, key=lambda k: k['visits'], reverse=True)
	
	if count != None and len(yield_li)>=count:
		yield_li = yield_li[0:count]

	if rem_count>0:
		yield_li = yield_li[0:rem_count]

	lyric_li = []
	for item in yield_li:
		other = "ගීත මාතෘකාව : {}\nපිවිසිම් වාර: {}\nවර්ගය : {}\nගායනය : {}\nගීත රචකයා : {}\nසංගීතය : {}\n\n{}\n".format(item['title'],item['visits'],",".join(item['genre_list']),",".join(item['artist_list']), ",".join(item['lyrics_by_list']),",".join(item['musics_by_list']),item['lyric-text'])
		
		lyric_li.append(other)


	
	return lyric_li


