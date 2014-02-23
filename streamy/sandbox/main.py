#!/usr/bin/env python
import re
import json

from flask import Flask
from flask import g
from flask import request
from flask import render_template
from flask_sockets import Sockets

from db import DB


# GLOBAL VARS
app = Flask(__name__)
sockets = Sockets(app)


def get_db():
    if not hasattr(g, "db"):
        g.db = DB()
        g.db.connect()

    return g.db


def modify_source_names(feeds):
    # modify source labels - bit hacky but it will do for now
    for feed in feeds:
        feed["source"] = feed["source"].replace("_", " ")

        if feed["source"] == "bbc":
            feed["source"] = "BBC"
        elif feed["source"] == "cnn":
            feed["source"] = "CNN"
        elif feed["source"] == "fox":
            feed["source"] = "FOX"
        elif feed["source"] == "google":
            feed["source"] = "Google"
        elif feed["source"] == "guardian":
            feed["source"] = "Guardian"
        elif feed["source"] == "wall street journal":
            feed["source"] = "Wall Street Journal"
        elif feed["source"] == "usa today":
            feed["source"] = "USA Today"
        elif feed["source"] == "nytimes":
            feed["source"] = "NY Times"

    return feeds


def jsonify_tweets(tweets):
    result = []
    for tweet in tweets:
        tweet.pop("_id")
        result.append(json.dumps(tweet))
    return result


@app.route('/', methods=["GET"])
def index():
    return render_template(
        'index.html',
        tweets=list(),
        rss=list()
    )


@app.route('/', methods=["POST"])
def query():
    db = get_db()
    collections = db.return_collections()
    rss = collections["rss"]
    tweets = collections["tweets"]

    # get search term
    search_term = None
    if request.form["search_term"] is not None:
        search_term = request.form["search_term"]

    # find relevant rss feeds
    rss_results = list(
        rss.find(
            {
                "$or": [
                    {"title": re.compile(search_term, re.IGNORECASE)},
                    {"summary": re.compile(search_term, re.IGNORECASE)},
                ]
            }
        ).sort("date", -1)
    )
    rss_results = modify_source_names(rss_results)

    # find relevant tweets
    tweet_results = list(
        tweets.find(
            {
                "$or": [
                    {"text": re.compile(search_term, re.IGNORECASE)},
                    {"summary": re.compile(search_term, re.IGNORECASE)},
                    {
                        "entities": {
                            "$elemMatch": {
                                "text": re.compile(search_term, re.IGNORECASE)
                            }
                        }
                    }
                ]
            }
        ).sort("created_at", -1)
    )
    tweet_results = jsonify_tweets(tweet_results)

    return render_template(
        'index.html',
        tweets=tweet_results,
        rss=rss_results
    )


if __name__ == "__main__":
    app.run(debug=True)
