import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
import json

#pip install googletrans-temp

from googletrans import Translator

class ToScrapeSpiderXPath(CrawlSpider):
	
	
	name = 'spi'
	next_urls = ['https://sinhalasongbook.com/tag/group-songs/page/{}'.format(page) for page in range(2,9)]

	start_urls = [
		'https://sinhalasongbook.com/tag/group-songs/'
		
	]
	start_urls.extend(next_urls)


	rules = (
		Rule(LinkExtractor(restrict_xpaths="//a[@class='entry-title-link']"), callback="parse_meta_data", follow= True),
		
	)
	
	
	
	
	def translate_to_sinhala(self,word):
		translator =  Translator()
		li = word.split(' ')

		new_words = ['Begh' if word == 'Beg' else word for word in li]
		new_words = ['Dhevi' if word == 'Devi' else word for word in new_words]
		new_words = ['Abeysekaraa' if word == 'Abeysekara' else word for word in new_words]
		new_words = ['Lathaa' if word == 'Latha' else word for word in new_words]
		new_words = ['Abhishekhaa' if word == 'Abhisheka' else word for word in new_words]
		new_words = ['Raajah' if word == 'Rajah' else word for word in new_words]	
		new_words = ['Wedisingha' if word == 'Wedisinghe' else word for word in new_words]	
		new_words = ['Adikaari' if word == 'Adikari' else word for word in new_words]
		new_words = ['Athaawuda' if word == 'Athauda' else word for word in new_words]
		new_words = ['Wijeywardhana' if word == 'Wijewardhana' else word for word in new_words]
		new_words = ['Nakhalanda' if word == 'Nakalanda' else word for word in new_words]
		new_words = ['Karunaanayake' if word == 'Karunanayake' else word for word in new_words]
		new_words = ['Naamal' if word == 'Namal' else word for word in new_words]
		new_words = ['Neelaa' if word == 'Neela' else word for word in new_words]
		new_words = ['Punyaa' if word == 'Punya' else word for word in new_words]	
		new_words = ['Punsirii' if word == 'Punsiri' else word for word in new_words]
		new_words = ['Udhupitiya' if word == 'Udupitiya' else word for word in new_words]	
		new_words = ['Sreemathi' if word == 'Shreemathi' else word for word in new_words]
		new_words = ['Umaariya' if word == 'Umariya' else word for word in new_words]
		new_words = ['Kumaarathunga' if word == 'Kumarathunga' else word for word in new_words]
		new_words = ['Seykara' if word == 'Sekara' else word for word in new_words]

		sin_terms = [translator.translate(word,dest='si').text for word in new_words]
		sin_terms = ['ද' if word == 'වල' else word for word in sin_terms]
		sin_terms = ['සමන්' if word == 'එක්ව' else word for word in sin_terms]
		sin_terms = ['බන්ඩාර' if word == 'ගුවන්තොටුපල' else word for word in sin_terms]
		sin_terms = ['ආත්මා' if word == 'ආත්මය' else word for word in sin_terms]
		sin_terms = ['ලියනාරච්චි' if word == 'ලියාන්රාචි' else word for word in sin_terms]
		sin_terms = ['කන්දනාරච්චි' if word == 'කන්දනරාචි' else word for word in sin_terms]
		sin_terms = ['ඩැඩී' if word == 'තාත්තේ' else word for word in sin_terms]
		sin_terms = ['දමිත්' if word == 'මර්දනය කරන ලදි' else word for word in sin_terms]
		sin_terms = ['දයාන්' if word == 'රැඳී සිටින්න' else word for word in sin_terms]
		sin_terms = ['වයිධ්‍යාසේකර' if word == 'ඔවුන් එය කෑවා' else word for word in sin_terms]
		sin_terms = ['උඩවත්ත' if word == 'ගැලවීම' else word for word in sin_terms]
		sin_terms = ['අද්දරාරච්චි' if word == 'අඩඩාර්චි' else word for word in sin_terms]
		sin_terms = ['කල්පනා' if word == 'පරිකල්පනය' else word for word in sin_terms]
		sin_terms = ['චිත්‍රසේන' if word == 'චීන' else word for word in sin_terms]
		sin_terms = ['දිවුල්ගනේ' if word == 'ඩිවුල්ගාන්' else word for word in sin_terms]
		sin_terms = ['කොරින්' if word == 'සිරුර' else word for word in sin_terms]
		sin_terms = ['මර්සි' if word == 'දයාව' else word for word in sin_terms]
		sin_terms = ['දිසාසේකර' if word == 'දිසේකර' else word for word in sin_terms]
		sin_terms = ['බද්දගේ' if word == 'බැජ්ගේ' else word for word in sin_terms]
		sin_terms = ['සංඛ' if word == 'සහභාගීත්වය' else word for word in sin_terms]
		sin_terms = ['ශ්‍යාමන්' if word == 'අඳුරේ' else word for word in sin_terms]
		sin_terms = ['දංගමුව' if word == 'ආශ්‍රිත' else word for word in sin_terms]
		sin_terms = ['ශ්‍යාමි' if word == 'ලැජ්ජයි' else word for word in sin_terms]
		sin_terms = ['සිසිර' if word == 'ඉතිරිය' else word for word in sin_terms]


		sin_term = ' '.join(sin_terms)
		return sin_term

   
	def parse_meta_data(self, response):
		
		# Sinhala Lyrics
		space_set = set([' '])
		
		content = response.xpath("//pre[1]").extract()
		regex = r"([A-z])+|[0-9]|\||-|\"|\*|\'|\—|\∆|\		|\ – |\            |\t|\      |\        |\       |\      |\               |\        |\           |\        |([.!?\\\/\(\)\+#&<>;:=__-])+"

		sinhala_lyrics = ''
		x = content[0].split('\n')
		for line in x:
			new=re.sub(regex,'',line)
			chars = set(new)
			if not (len(chars)==0 or (chars == space_set)):
				sinhala_lyrics += new+'\n'
		
			
		
		#Sinhala title
		title = response.xpath("//h1[@class='entry-title']/text()").extract()[0]
		sin_title = re.sub(regex,'',title).strip()	
		
		
		#key (F major/C)
		try:
			key_beat = response.xpath("//div[@class='entry-content']/h3/text()").extract()[0].split('|')
			key = key_beat[0].split(':')[1].strip()
		except IndexError:
			key = None

		#Beat (4/4 Beat)
		try:
			beat = key_beat[1].split(':')[1].strip()
		except IndexError:
			beat = None

		#Artist Name
		try:

			artists = response.xpath("//div[@class='su-column su-column-size-3-6']//span[@class='entry-categories']/a/text()").extract()

			artist_list = [self.translate_to_sinhala(str(person)) for person in artists]
			
		except Exception:
			artist_list = []

		

		#Genre 
		try:
			genre_dict = {
				'Golden Oldies': ['පැරණි'],
				'Calypso': ['බයිලා'],
				'Classics': ['ක්ලැසික්'],
				'duet':['යුගල'],
				'Duets':['යුගල'],
				'Movie Songs':['චිත්‍රපට'],
				'Old Pop':['පැරණි පොප්'],
				'Old Pops':['පැරණි පොප්'],
				'New Pop':['නව පොප්'],
				'Inspirational':['ආදර්ශමත්'],
				'Group Songs':['කණ්ඩායම්'],
				'Current Songs':['අලුත්',],
				'Golden Pop':[],
				'Request':[],
				'reques':[]


			}
			genre_list=[]
			genres = response.xpath("//div[@class='su-column su-column-size-3-6']//span[@class='entry-tags']/a/text()").extract()
			
			for genre in genres:
				genre_list.extend(genre_dict[str(genre)])

		except IndexError:
			genre_list = None


		#Lyrics By
		try:

			lyrics_by = response.xpath("//div[@class='su-column su-column-size-2-6']//span[@class='lyrics']/a/text()").extract()
			lyrics_by_list = [self.translate_to_sinhala(str(lyric_by)) for lyric_by in lyrics_by]

		except Exception:
			lyrics_by_list = []

		#Music By
		try:

			musics_by = response.xpath("//div[@class='su-column su-column-size-2-6']//span[@class='music']/a/text()").extract()
			musics_by_list = [self.translate_to_sinhala(str(music_by)) for music_by in musics_by]

		except Exception:
			musics_by_list = []



		#Number of visits of the song
		try:
			regex_num = r"([A-z])+|\||-|\"|\*|\'|\s|([.,!?\\\/\(\)\+#&<>;:=__-])+"
			
			visits = response.xpath("//div[@class='tptn_counter']/text()").extract()[0]
			visits = re.sub(regex_num,'',visits)

		except Exception:
			visits = 0

	    

		#Assembling data 
		data = {
			'lyric-text': sinhala_lyrics,
			'title':sin_title,
			'key':key,
			'beat':beat,
			'artist_list':artist_list,
			'genre_list':genre_list,
			'lyrics_by_list':lyrics_by_list,
			'musics_by_list':musics_by_list,
			'visits':visits
		}

		#Write data to a json file
		with open('../sin_oldies.json', 'a') as fp:
		    json_string = json.dumps(data, ensure_ascii=False)
		    fp.write(json_string+'\n')   





		'''	
		command = 'scrapy crawl spi'
		os.system(command)
		'''
