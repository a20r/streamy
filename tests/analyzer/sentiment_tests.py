#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from streamy.db import DB
# from streamy.analyzer.sentiment import SentimentAnalyzer
from streamy.analyzer.sentiment import SentimentAnalyzer


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.db.connect()

        self.sentiment = SentimentAnalyzer(self.db)

    def test_analyze_text(self):
        result_1 = self.sentiment.analyze_text("great")
        result_2 = self.sentiment.analyze_text("bad")

        self.assertTrue(result_1["polarity"] > 0)
        self.assertTrue(result_2["polarity"] < 0)


if __name__ == "__main__":
    unittest.main()
