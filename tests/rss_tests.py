#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from streamy.db import DB
from streamy.rss import RSSReader


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.db.connect()

        self.rss = RSSReader(self.db)

    def test_parse_feed(self):
        result = self.rss.parse_feed("bbc_news")

        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0]["title"] is not None)
        self.assertTrue(result[0]["summary"] is not None)
        self.assertTrue(result[0]["date"] is not None)

    def test_record_feed(self):
        self.rss.record_feed("bbc_news")

        bbc_news = self.rss.collections["bbc_news"]
        self.assertTrue(bbc_news.count() > 0)

        bbc_news.remove()
        self.assertTrue(bbc_news.count() == 0)


if __name__ == "__main__":
    unittest.main()
