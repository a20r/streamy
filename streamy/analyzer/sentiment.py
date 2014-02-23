#!/usr/bin/env python
# import json

# import requests
from pattern.en import sentiment


class SentimentAnalyzer(object):
    def __init__(self, db=None):
        self.db = db

    def analyze_text(self, text):
        analysis = sentiment(text)
        result = {
            "polarity": analysis[0],
            "subjectivity": analysis[1]
        }

        return result
