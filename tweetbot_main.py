#!/usr/bin/env python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from streamy.db import DB
from streamy.tweetbot.streaming import TwitterStream
from streamy.tweetbot.streaming import TweetReply
from streamy.tweetbot.streaming import TwitterTrends
from geopy import geocoders

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="vePyS3FmZCV4pwUCE9gWpg"
consumer_secret="SbeMeY8c0o7Cg3D8UqNMqIApl1ldQX0kz1nuz0ghh8"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="26055337-Bs5RZJYHQRZ5dbGIOZk4SYV1lw8nHQG5YEUodowFT"
access_token_secret="J0AhNitT95NiVkOwJAFUHqKLDAUmZrSAzhI0VQfoOqHlo"

def get_boundary(address):
	g = geocoders.GoogleV3()
	place, (lat, lng) = g.geocode(address)
	return [lng-0.005, lat-0.005, lng+0.005, lat+0.005]


if __name__ == '__main__':
    db = DB()
    db.connect()

    #[-0.0299759,51.5019442,-0.0122416,51.5087498]
    query = "Keiv, Ukrain"
    print get_boundary(query)
    s = TwitterStream(locations=get_boundary(query), db=db)


    # reply = TweetReply()

    # for tweet in s.queue:
    #     screen_name = tweet["user"]["screen_name"]
    #     tweet_id = tweet["id_str"]
    #     url = ""

    #     reply.tweet_with_request(screen_name, tweet_id, url)

    # trends = TwitterTrends()
    # import pprint
    # pprint.pprint(trends.get_trends())
