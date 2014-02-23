#!/usr/bin/env python
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API

from streamy.analyzer.sentiment import SentimentAnalyzer



# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="bqyKjzTjaQpKEDZ7blcuIg"
consumer_secret="f3NFp8ZucXMibQvq9j24VTmXVtQlyhIoqt3z6Uw4ms"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="14113807-VrdngSdnYVhVx9ja1GvROt2Dd3FEWqnWRR6Y3XxBf"
access_token_secret="jHR0rd8tCvSjpx4hdlj69cdYiY1HWHVpoktqZcsKf2WZw"

class TwitterStream(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    locations = ""

    def __init__(self, **kwargs):

        #reply = TweetReply()
        #reply.tweet_with_request("Alehins")

        # database
        self.db = kwargs["db"] # assumes db is already connected
        if self.db.state == "IDLE" or self.db.state == "DISCONNECTED":
            self.db.connect()
        collections = self.db.return_collections()
        self.tweets = collections["tweets"]

        # misc
        self.counter = 0
        self.queue = []
        self.locations=kwargs["locations"]
        self.sentiment = SentimentAnalyzer()

        # twitter
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, self)
        stream.filter(locations=kwargs["locations"])

    def on_data(self, data):
        tweet_data = json.loads(data)
        tweet_data["requested_for_locations"] = self.locations
        #tweet_data["requested_for_locations"]

        if self.counter < 100:
            print self.counter
            self.insert_tweet(tweet_data)
            self.queue.append(tweet_data)
            self.counter += 1
            return True
        else:
            return False

    def on_error(self, status):
        # print status
        print

    def insert_tweet(self, tweet):
        self.tweets.insert(tweet)


class TweetReply():
    def __init__(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)

    def tweet_in_response(self, screen_name, tweet_id, url):
        # self.api.update_status("@" + screen_name + " Hi! Could you please click the link to stream your surroundings? " + url, tweet_id)
        self.api.update_status("@" + screen_name + " We support you!", tweet_id)

    def tweet_to_person(self, screen_name):
        # self.api.update_status("@" + screen_name + " Hi! Could you please click the link to stream your surroundings? " + url, tweet_id)
        self.api.update_status("@" + screen_name + " Somebody requested a live stream from you: http://streamy.co/streamer/" + screen_name)


class TwitterTrends(object):
    def __init__(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth)

    def get_trends(self):
        return self.api.trends_available()
