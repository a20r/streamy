

from flask import request, redirect, url_for, abort, jsonify, render_template
from flask import make_response, Response
import config

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


@config.app.route("/")
def get_index():
    return render_template("landing.html")

