#!/usr/bin/env python
import re
import json
import config

from flask import request, redirect, url_for, abort, jsonify, render_template
from flask import make_response, Response
from flask import g

from db import DB

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from tweetbot.streaming import TweetReply

""" Directory for static files """
STATIC_DIR = "assets/"

""" Mime type dictionary """
MIME_DICT = {
    "js": "text/javascript",
    "css": "text/css",
    "imgs": "image/png",
    "libraries": "text/javascript",
    "data": "text/csv"
}

streamer_list = list()

@config.app.route("/<filename>", methods = ["GET"])
def serve_html_page(filename):
    if filename == "favicon.ico":
        with open(STATIC_DIR + "imgs/favicon.ico") as f:
            return Response(f.read(), mimetype = "image/x-icon")

    return render_template(filename)


@config.app.route("/streamer/<stream_id>")
def get_streamer(stream_id):
    return render_template("streamer.html", stream_id=stream_id)


@config.app.route("/streamee/<stream_id>")
def get_streamee(stream_id):
    return render_template("streamee.html", stream_id=stream_id)


@config.app.route("/<filetype>/<filename>", methods = ["GET"])
def serve_script(filetype, filename):
    with open(STATIC_DIR + filetype + "/" + filename) as f:
        return Response(f.read(), mimetype = MIME_DICT[filetype])


@config.app.route("/twitter/<username>")
def twitter_username(username):
    global streamer_list
    if not username in streamer_list:
        tr = TweetReply()
        tr.tweet_to_person(username)
        streamer_list.append(username)

    return jsonify(error="No error")


@config.app.route("/streamer_list")
def get_streamer_list():
    return render_template("streamerlist.html", streamer_list=streamer_list)


@config.app.route("/make_anon/<s_id>")
def get_make_anon(s_id):
    global streamer_list
    if not s_id in streamer_list:
        streamer_list.append(s_id)

    return jsonify(error="No error")


@config.app.route("/")
def get_index():
    return render_template("landing.html")


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


@config.app.route('/map', methods=["GET"])
def map():
    return render_template(
        'map.html',
        search_term="",
        rss=list()
    )


@config.app.route('/map', methods=["POST"])
def query():
    db = get_db()
    collections = db.return_collections()
    rss = collections["rss"]

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

    return render_template(
        'map.html',
        search_term=search_term,
        rss=rss_results
    )


@config.app.route('/tweets', methods=["POST"])
def tweets():
    db = get_db()
    collections = db.return_collections()
    tweets = collections["tweets"]
    tweet_results = []

    if request.data is not None:
        search_term = json.loads(request.data)["search_term"]

        # find relevant tweets
        if search_term != "":
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
            for tweet in tweet_results:
                tweet.pop("_id")
                print tweet["text"]

        return jsonify({"tweets": tweet_results})

if __name__ == "__main__":
    app.run(debug=True)
