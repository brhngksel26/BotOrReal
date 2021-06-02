from re import template
from flask import Flask
from flask import request,jsonify,render_template
from app.tweet_data_utils import result
from app.tweepy_utils import bot_or_not
from threading import Thread

app = Flask(__name__)




@app.route('/')
def index():
	return render_template('hashtag.html')

@app.route('/username')
def username():
    return render_template('username.html')

@app.route('/tweet_result', methods=['POST'])
def tweet_result():
    hashtag = request.form.get('hashtag')
    tweet_count = request.form.get('tweet_count')
    email = request.form.get('email')
    thread = Thread(target=result, args=(email,hashtag,tweet_count))
    thread.daemon = True
    thread.start()
    messages = "İşlem Başlatıldı"
    return render_template('hashtag.html', template_data = messages)


@app.route('/account_result', methods=['POST'])
def account_result():
    hashtag = request.form.get('username')
    data_result = bot_or_not(hashtag)
    return render_template('username.html',template_data = data_result)

@app.route('/hashtag',methods=['POST'])
def tweet_result_api():
    data = request.get_json()
    email = {'email' :data['email']}
    tweet_count = {'tweet_count': data['tweet_count']}
    hashtag = {'hashtag' : data['hashtag']}
    
    email = str(email).replace("{'email': '","")
    email = str(email).replace("'}","")

    tweet_count = str(tweet_count).replace("{'tweet_count': '","")
    tweet_count = str(tweet_count).replace("'}","")

    
    thread = Thread(target=result, args=(email,hashtag,tweet_count))
    thread.daemon = True
    thread.start()
    
    return jsonify({'messages':'işlem başlatıldı'})


@app.route('/username',methods=['POST'])
def bot_or_real_result_api():
    data = request.get_json()
    username = {'username' : data['username']}

    username = str(username).replace("{'username': '","")
    username = username.replace("'}","")

    result = bot_or_not(username)

    return jsonify({'sonuc':result})