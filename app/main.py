from re import template
from flask import Flask
from flask import request,jsonify,render_template
from app.tweet_data_utils import result
from app.tweepy_utils import bot_or_not

application = Flask(__name__)

@application.route('/')
def index():
	return render_template('hashtag.html')

@application.route('/username')
def username():
    return render_template('username.html')

@application.route('/tweet_result', methods=['POST'])
def tweet_result():
    hashtag = request.form.get('hashtag')
    tweet_count = request.form.get('tweet_count')
    email = request.form.get('email')

    data = result(email,hashtag,tweet_count)
    return render_template('hashtag.html', template_data = data)


@application.route('/account_result', methods=['POST'])
def account_result():
    hashtag = request.form.get('username')
    data_result = bot_or_not(hashtag)
    return render_template('username.html',template_data = data_result)

@application.route('/hashtag',methods=['POST'])
def tweet_result_api():
    data = request.get_json()
    email = {'email' :data['email']}
    tweet_count = {'tweet_count': data['tweet_count']}
    hashtag = {'hashtag' : data['hashtag']}
    
    email = str(email).replace("{'email': '","")
    email = str(email).replace("'}","")

    tweet_count = str(tweet_count).replace("{'tweet_count': '","")
    tweet_count = str(tweet_count).replace("'}","")

    hashtag = str(hashtag).replace("{'hashtag': '","")
    hashtag = str(hashtag).replace("'}","")
    result(email,hashtag,tweet_count)
    
    return jsonify({'messages':'işlem başlatıldı'})


@application.route('/username',methods=['POST'])
def bot_or_real_result_api():
    data = request.get_json()
    username = {'username' : data['username']}

    username = str(username).replace("{'username': '","")
    username = username.replace("'}","")

    result = bot_or_not(username)

    return jsonify({'sonuc':result})