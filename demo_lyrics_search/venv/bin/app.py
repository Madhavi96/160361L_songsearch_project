# app.py
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

app.debug = True


#...
@app.route('/lyrics/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside 
        password = request.form.get('password')
 
        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"
 
    return render_template('login.html', message=message)
#...

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Hoolaaa</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000,debug=True)
