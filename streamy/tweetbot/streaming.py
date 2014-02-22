#!/usr/bin/env python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from ..db import DB

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="vePyS3FmZCV4pwUCE9gWpg"
consumer_secret="SbeMeY8c0o7Cg3D8UqNMqIApl1ldQX0kz1nuz0ghh8"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="26055337-Bs5RZJYHQRZ5dbGIOZk4SYV1lw8nHQG5YEUodowFT"
access_token_secret="J0AhNitT95NiVkOwJAFUHqKLDAUmZrSAzhI0VQfoOqHlo"

class TwitterStream(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    tweets = None 
    
    def on_data(self, data):
        #print json.loads(data)['text']
        self.insert_tweet(data)
        return True

    def on_error(self, status):
        print status

    def __init__(self, **kwargs):
        #l = TwitterStream()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, self)
        stream.filter(locations=kwargs["locations"])

        self.db = kwargs["db"] # assumes db is already connected
        if self.db.state == "IDLE" or self.db.state == "DISCONNECTED":
            self.db.connect()

        collections = db.return_collections()
        self.tweets = collections["tweets"]
        
    def insert_tweet(self, tweet):
        self.tweets.insert(tweet)