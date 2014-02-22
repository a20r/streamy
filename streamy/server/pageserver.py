

from flask import request, redirect, url_for, abort, jsonify, render_template
from flask import make_response, Response
import config

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
        with open(STATIC_DIR + "img/favicon.ico") as f:
            return Response(f.read(), mimetype = "image/x-icon")

    return render_template(filename)

@config.app.route("/<filetype>/<filename>", methods = ["GET"])
def serve_script(filetype, filename):
    with open(STATIC_DIR + filetype + "/" + filename) as f:
        return Response(f.read(), mimetype = MIME_DICT[filetype])

