#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from flask import Flask
# from flask import request
# from flask import jsonify
from flask import render_template

# GLOBAL VARS
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="home")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
