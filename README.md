The repository contains code for scraping a website containing Sinhala Songs and their meta data. The website used for scraping song data is https://sinhalasongbook.com/. Extracted meta data includes

	1.Sinhala Lyrics
	2.Name of the Artist/s
	3.Name of the Lyricist/s
	4.Name of the musician/s
	5.Genre/s of the song
	6.Number of visits(website) to the song
	7.Title of the song
	8.Key of the song(F major/C)
	9.Beat of the song(4/4 beat)

The Data folder contains the scrapped data written to a json file, after preprocessing. This contains 950 songs and relavant meta data. The IR system is designed using elasticsearch.

* Folder Struture

All the required files are inside the demo_lyrics_search sub folder. Inside the demo_lyrics_search sub folder, following files exist.

	venv,templates,app.py : Related to the flask app front-end rendering
	
	spiders : Related to the files useful for crawling the website. test.py file is the file created to scrape song website in this project
	
	sin_oldies.json : contains scraped and processed song metadata
	
	post_es.py : A python script used to post metadata to elasticsearch from sin_oldies.json file. 
	
	query_test.py : A python script to analyze user entered keywords, construct queries and fetch/assemble the results to be rendered to the user
	
	extract_lyrics_words.py : extract_artistwords.py,extract_titlewords.py : Python scripts to extrat all different lyrics words, artist(/musician/lyricist) 				words, title words respectively in the song corpus(sin_oldies.json)


1. About the scraping process

* The spiders/test.py file contains the code used to scrape the webpages of the site. 
* In order to diretly scrape from the site, open a terminal inside spiders folder and execute : scrapy crawl spi
* This will scrape from specified urls and save processed meta data inside sin_oldies.json file.
* Below is a simple explanation to important code blocks of test.py

'spi' is the name of the spider

	name = 'spi'

Change next_urls by specifying a list of urls ('https://sinhalasongbook.com/tag/group-songs/page/2,'https://sinhalasongbook.com/tag/group-songs/page/3,etc) you need to scrape. Change this by the required next urls you need to scrape.

	next_urls = ['https://sinhalasongbook.com/tag/group-songs/page/{}'.format(page) for page in range(2,9)]

start_urls contain the seed/start url ('https://sinhalasongbook.com/tag/group-songs/) the spider needs to scrape. Change this by the required start url you need to scrape.

	start_urls = [	'https://sinhalasongbook.com/tag/group-songs/']

extending the urls to provide all urls to spider

	start_urls.extend(next_urls)

translate_to_sinhala : this function translates given english words to sinhala. As the website contains artist/lyrcist/musician names in English, translation to Sinhala is required. Google translate service is used for this. 

	def translate_to_sinhala(self,word):
		translator =  Translator()

Some translations are misleading. Thus required to go through each translation and apply hacks for the misleading ones.

	new_words = ['Begh' if word == 'Beg' else word for word in li]

This function takes into account the scraped data at hand and process/parse the data as required by the application

	def parse_meta_data(self, response):


2. Indexing Techniques

For indexing the song documents, the standard client - curl is used to sent http requests as Elasticsearch uses a REST API. The meta data are indexed and fetched from the index insted of _source by making the store=True in indexing.


	curl -XPUT http://localhost:9200/lyrics/_mapping/?pretty=true -H 'Content-Type: application/json' -d '
	{
	    "properties" : {
		    "lyric-text" : { "type" : "text" , "store" : true },
		    "title" : { "type" : "text", "store" : true  },
		    "key" : { "type" : "text", "store" : true  },
		    "beat" : { "type" : "text", "store" : true  },
		    "artist_list" : { "type" : "text", "store" : true  },
		    "genre_list" : { "type" : "text", "store" : true },
		    "lyrics_by_list" : { "type" : "text", "store" : true },
		    "musics_by_list" : { "type" : "text", "store" : true  },
		    "visits" : { "type" : "long", "store" : true }
		}
	}
	'


3. Querying techniques/Advanced features

When finding given words in lyrics/artists, etc character level similarity percentage is considered. e.x if we search by the Genre:  කණ්ඩායම් but with typos (e.x කණ්ඩයම්) the character level similarity percentage still increases 90%. Thus taken as a match with the intended Genre. 
Text classification is used to identify the focus of a user keyword. First the user entered keywords are broken into word-level and analyzed the suggested content. A word can suggest an artist/musician/lyricist name (අමරදේව) or a number (දහය) or a genre (කණ්ඩායම්) or else simply the user's intention to retrieve the best songs by using words such as best (හොඳම). Analyzing/finding these different focus areas is done by keeping word-collections (one collection contains all artist/musician/lyricist names, another contains all genre names,etc) related to the corpus and matching each keyword with the best word-collection. ex. If one keyword is අමරදේව, by comparing the word with the word-collection having all names(artist/musician/lyricist) we can find that the user needs to fetch songs by artist/musician/lyricist name field.

After finding all different query fields hidden in the user entered keywords, we can construct a simple/complex query in a rule based manner. e.x. If the user needs to filter by both artist name and genre, we can build a complex query using Boolean operators like and/or (must/should).

Facets are used when filtering by number of visits and any given keyword(genre, name, etc)
Range queries are used when the user needs to filter song data by the number of visits to the song. Compound queries are used when the user needs to filter song data by multiple fields/metadata. Text mining is used for organizing unstructured scraped data.











