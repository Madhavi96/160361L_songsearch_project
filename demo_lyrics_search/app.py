# app.py
from flask import Flask, request, jsonify, render_template
from query_test import get_lyrics

app = Flask(__name__)

app.debug = True


#...
@app.route('/lyrics/', methods=['post', 'get'])
def login():
    lyrics = ''
    view_range = ''
    num = ""
    if request.method == 'POST':
        words = request.form.get('username').strip()  # access the data inside 
        r1 = request.form.get('r1')
        
        
        if r1!=None:
            view_range = r1
        
     


        lyrics = get_lyrics(words,view_range)
        num = len(lyrics)
 
        
 
    return render_template('front.html', message=lyrics,num=num)
#...

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Search Sinhala Lyrics</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000,debug=True)