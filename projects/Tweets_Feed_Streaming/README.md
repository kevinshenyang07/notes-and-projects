## Tweets Streaming with Word Cloud


use brew to install rabbitmq  
use pip to install flask, tweepy, pika
use pip to install nltk and its corpus of stop words 

1. start rabbit message queue service ```$ rabbitmq-server```
2. start tweets feed ```$ python feed_producer.py```
3. start flask service ```$ python app.py```
4. in the browser, enter ```localhost:5000/word_cloud``` to see word cloud, if the messages are not enough for the get_tweets() function, it will hold.

