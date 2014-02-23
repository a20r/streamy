#!/usr/bin/env python
import os
import sys

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

# GLOBAL VARS
app = Flask(__name__)


@app.route('/')
def index():
    geo_points = [
        (56.341304, -2.791441),  # Gannochy Hall
        (55.953252, -3.188267)  # Edinburgh
    ]
    return render_template('index.html', geo_points=geo_points)


if __name__ == '__main__':
    app.run()
