
from flask import Flask

app = Flask(__name__)
app.debug = True

WS_HEADER = "ws://"


# Imports needed for routes to run
import pageserver


