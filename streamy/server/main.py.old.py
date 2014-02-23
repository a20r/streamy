#!/usr/bin/env python
import re

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


@app.route('/', methods=["GET"])
def index():
    geo_points = [
        (56.341304, -2.791441),  # Gannochy Hall
        (55.953252, -3.188267)  # Edinburgh
    ]
    return render_template(
        'index.html',
        geo_points=geo_points,
        rss=list()
    )


@app.route('/', methods=["POST"])
def query():
    db = get_db()
    collections = db.return_collections()
    rss = collections["rss"]

    search_term = None
    if request.form["search_term"] is not None:
        search_term = request.form["search_term"]

    results = list(
        rss.find(
            {
                "$or": [
                    {"title": re.compile(search_term, re.IGNORECASE)},
                    {"summary": re.compile(search_term, re.IGNORECASE)},
                ]
            }
        ).sort("date")
    )
    results = modify_source_names(results)

    return render_template(
        'index.html',
        geo_points=[],
        rss=results
    )


if __name__ == "__main__":
    app.run(debug=True)
