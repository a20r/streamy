
from flask import Flask
from flask import render_template

import config


@config.app.route('/')
def index():
    return render_template('index.html', title="home")

