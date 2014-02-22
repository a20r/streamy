#!/usr/bin/env python
import json

import requests


class SentimentAnalyzer(object):
    def __init__(self, db):
        self.db = db

    def analyze_text(self, text):
        sentiment_url = "http://text-processing.com/api/sentiment/"
        data = {"text": text}

        # analyze text
        result = requests.post(sentiment_url, data=data)
        result = json.loads(result.text)

        return result
