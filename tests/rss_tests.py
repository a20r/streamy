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
        result = self.rss.parse_feed("bbc")

        self.assertTrue(len(result) > 0)
        self.assertTrue(result[0]["title"] is not None)
        self.assertTrue(result[0]["summary"] is not None)
        self.assertTrue(result[0]["date"] is not None)

    def test_record_feed(self):
        self.rss.record_feed()

        # test simple insert
        rss = self.rss.collections["rss"]
        count = rss.count()
        self.assertTrue(rss.count() > 0)

        # test no duplicates
        self.rss.record_feed()
        self.assertEquals(count, rss.count())

        # test remove all documents
        # rss.remove()
        # self.assertTrue(rss.count() == 0)


if __name__ == "__main__":
    unittest.main()
