import pandas as pd
from deep_translator import GoogleTranslator
from textblob import TextBlob
from app.tweepy_utils import bot_or_not
import twint 
import datetime
import csv
import os
import smtplib
import app.auth_info 
from flask import Flask

app = Flask(__name__)



def sendMail(send_email,message):
    message = message.encode("ascii", errors="ignore")
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(app.auth_info.mail,app.auth_info.password)
    server.sendmail(app.auth_info.mail,send_email,message)



def twint_run(serch_key,limit):
    filename = datetime.datetime.now()
    filename = str(filename).replace(" ","-")
    filename = filename + ".csv"
    c = twint.Config()
    c.Search = serch_key
    c.Limit = limit
    c.Store_csv = True
    c.Output = filename

    app.logger.info(os.path.abspath(filename))
    
    
    #Run
    twint.run.Search(c)

    return filename

def csv_edit(filename):
    inputFileName = filename
    outputFileName = os.path.splitext(inputFileName)[0] + "_modified1.csv"

    with open(inputFileName, newline='') as inFile:
        with open(outputFileName, 'w', newline='') as outfile:
            r = csv.reader(inFile)
            w = csv.writer(outfile)

            next(r, None)  # skip the first row from the reader, the old header
            # write new header
            w.writerow(["id", "conversation_id", "created_at", "date", "time", "timezone", "user_id", "username", "name", "place", "tweet"
        , "language", "mentions", "urls", "photos", "replies_count", "retweets_count", "likes_count", "hashtags", "cashtags", "link"
        , "retweet", "quote_url", "video", "thumbnail", "near" , "geo" , "source", "user_rt_id", "user_rt", "retweet_id", "reply_to", "retweet_date", "translate",
        "trans_src", "trans_dest"])
            for row in r:
                w.writerow(row)

        os.remove(filename)
        return outputFileName

def result(email,serch_key,tweet_count):
    csv_file = twint_run(serch_key,tweet_count)
    output_file_name = csv_edit(csv_file)

    data = pd.read_csv(output_file_name,encoding='utf-8')
    data.drop("video",axis = 1,inplace = True )
    data.drop("thumbnail",axis = 1,inplace = True )
    data.drop("near",axis = 1,inplace = True )
    data.drop("geo",axis = 1,inplace = True )
    data.drop("source", axis = 1, inplace = True)
    data.drop("user_rt_id", axis = 1, inplace = True)
    data.drop("user_rt", axis = 1, inplace = True)
    data.drop("retweet_id", axis = 1, inplace = True)
    data.drop("reply_to", axis = 1, inplace = True)
    data.drop("retweet_date", axis = 1, inplace = True)
    data.drop("translate", axis = 1, inplace = True)
    data.drop("trans_src",axis = 1,inplace = True )
    data.drop("trans_dest",axis = 1,inplace = True )
    data.drop("id",axis = 1,inplace = True )
    data.drop("conversation_id",axis = 1,inplace = True )
    data.drop("created_at",axis = 1,inplace = True )
    data.drop("date",axis = 1,inplace = True )
    data.drop("time", axis = 1, inplace = True)
    data.drop("timezone", axis = 1, inplace = True)
    data.drop("user_id", axis = 1, inplace = True)
    data.drop("name", axis = 1, inplace = True)
    data.drop("place", axis = 1, inplace = True)
    data.drop("language", axis = 1, inplace = True)
    data.drop("mentions", axis = 1, inplace = True)
    data.drop("urls",axis = 1,inplace = True )
    data.drop("photos",axis = 1,inplace = True )
    data.drop("replies_count",axis = 1,inplace = True )
    data.drop("retweets_count", axis = 1, inplace = True)
    data.drop("likes_count", axis = 1, inplace = True)
    data.drop("hashtags", axis = 1, inplace = True)
    data.drop("cashtags", axis = 1, inplace = True)
    data.drop("link", axis = 1, inplace = True)
    data.drop("retweet", axis = 1, inplace = True)
    data.drop("quote_url", axis = 1, inplace = True)

    bot_account = 0
    human_account = 0
    bot_counter = 0
    for column in data.values:
        account = bot_or_not(column[0])
        if account == "Bot":
            bot_account = bot_account + 1
        if account == "insan":
            human_account = human_account + 1
        bot_counter = bot_counter + 1
        if bot_counter == tweet_count:
            break
    

    likely_count = 0
    likely_point = 0
    unlikely_count = 0
    unlikely_point = 0
    neutral_count = 0
    blob_counter = 0
    for column in data.values:
        if column[1] != "nan" and column[1] != None and len(str(column[1])) > 10:
            translated = GoogleTranslator(source='auto', target='en').translate(str(column[1]))
            blob = TextBlob(str(translated))
            polarity = blob.polarity
            if polarity > 0 :
                likely_count = likely_count + 1
                likely_point = likely_point + polarity
            if polarity < 0 :
                unlikely_count = unlikely_count + 1
                unlikely_point = unlikely_point + polarity
            if polarity == 0:
                neutral_count = neutral_count + 1
            
            blob_counter = blob_counter + 1

            if blob_counter == tweet_count:
                break
    

    likely_result_point = (abs(likely_point) / likely_count) * 100
    unlikely_result_point = (abs(unlikely_point) / unlikely_count) * 100
    polarity_result = 'Olumlu Tweet Sayısı = ' + str(likely_count) +"\n" + "Olumluluk Oranı = " + str(round(likely_result_point))+"%"+ "\n" + "Olumsuz Tweet Sayısı = " + str(unlikely_count) + "\n" + "Olumsuzluk Oranı = "  + str(round(unlikely_result_point))+"%"+"\n" + "Nötr Tweet Sayısı = " + str(neutral_count) + "\n"
    bot_or_not_result = 'Bot Hesap Sayısı = ' + str(bot_account) + "\n" + "İnsan Hesab Sayısı = " + str(human_account)
    message = polarity_result + bot_or_not_result

    sendMail(email,message)
    os.remove(output_file_name)
    return message


