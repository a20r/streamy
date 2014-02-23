

from flask import request, redirect, url_for, abort, jsonify, render_template
from flask import make_response, Response
import config

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from streaming.tweetbot import TweetReply

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
    tr = TweetReply()
    tr.tweet_to_person(username)

    return jsonify(error="No error")

