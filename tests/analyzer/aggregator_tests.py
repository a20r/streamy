#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from streamy.db import DB
from streamy.rss import RSSReader
from streamy.analyzer.aggregator import Aggregator


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.db.connect()

        self.rss = RSSReader(self.db)
        self.rss.record_feed()

        self.aggregator = Aggregator(self.db)

    def tearDown(self):
        collections = self.db.return_collections()
        collections["rss"].remove()
        collections["result"].remove()

    def test_word_cloud(self):
        tags = self.aggregator.word_cloud()

        print "TAGS:"

        for tag in tags[0:20]:
            print tag["tag"], tag["count"]





        print "LEN:", len(tags)

        self.assertTrue(tags is not None)
        self.assertTrue(len(tags) > 0)


if __name__ == "__main__":
    unittest.main()
