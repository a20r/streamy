#!/usr/bin/env python
import pymongo

# GLOBAL VARS
host = "localhost"
port = "27017"


class DB(object):
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "localhost")
        self.port = kwargs.get("port", "27017")

    def connect(self):
        self.client = pymongo.MongoClient(
            'mongodb://{0}:{1}/'.format(host, port)
        )

    def disconnect(self):
        self.client.disconnect()

    def return_collections(self):
        collections = {}

        db = self.client.streamy
        collections = {
            "tweets": db.tweets
        }

        return collections


if __name__ == "__main__":
    db = DB()
    db.connect()
    collections = db.return_collections()

    tweets = collections["tweets"]
    tweet.add()

