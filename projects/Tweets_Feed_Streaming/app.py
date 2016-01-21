from flask import Flask, Response, render_template
import pika
import json
import pandas
from nltk.corpus import stopwords
import re

 #setup queue
connection = pika.BlockingConnection()
channel = connection.channel()


#function to get data from queue
def get_tweets(size=10):
    tweets = []
    # Get ten messages and break out
    count = 0
    for method_frame, properties, body in channel.consume('twitter_topic_feed'):

        tweets.append(json.loads(body))

        count += 1

        # Acknowledge the message
        channel.basic_ack(method_frame.delivery_tag)

        # Escape out of the loop after 10 messages
        if count == size:
            break

    # Cancel the consumer and return any pending messages
    requeued_messages = channel.cancel()
    print 'Requeued %i messages' % requeued_messages

    return tweets

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    PROPAGATE_EXCEPTIONS=True
)


@app.route('/feed/raw_feed', methods=['GET'])
def get_raw_tweets():
    tweets = get_tweets(size=5)
    text = ""
    for tweet in tweets:
        tt = tweet.get('text', "")
        text = text + tt + "<br>"

    return text


@app.route('/feed/word_count', methods=['GET'])
def get_word_count():
    tweets = get_tweets(size=200)
    stop = stopwords.words('english')
    twt_hndls = ['retweeted', 'basic', 'bad', 'fuck', 'shit', 'note', '&amp;',
    'fart', '#python']

    tokens = []
    for tweet in tweets:
        tt = tweet.get('text', "").lower()
        for word in tt.split():
            # get rid of the urls
            if re.search(r'http', word) or len(word) < 4:
                continue
            if word not in stop and word not in twt_hndls:
                tokens.append(word)

    p = pandas.Series(tokens)
    #get the counts per word
    freq = p.value_counts()
    #how many max words do we want to give back
    freq = freq.ix[0:300]

    response = Response(freq.to_json())
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response


@app.route('/word_cloud', methods=['GET'])
def index():
    return render_template('word_cloud.html')


if __name__ == "__main__":
    app.run()
