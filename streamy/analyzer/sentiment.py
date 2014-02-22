#!/usr/bin/env python
# import json

# import requests
from pattern.en import sentiment


class SentimentAnalyzer(object):
    def __init__(self, db=None):
        self.db = db

    def analyze_text(self, text):
        # USING NLTK WEB
        # sentiment_url = "http://text-processing.com/api/sentiment/"
        # data = {"text": text}

        # # analyze text
        # result = requests.post(sentiment_url, data=data)
        # result = json.loads(result.text)

        # USING PATTERN
        analysis = sentiment(text)
        result = {
            "polarity": analysis[0],
            "subjectivity": analysis[1]
        }

        return result
