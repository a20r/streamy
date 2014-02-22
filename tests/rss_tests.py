#!/usr/bin/env python
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from streamy.rss_scraper import RSS


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.rss = RSS()

    def test_parse_feed(self):
        feed = self.rss.parse_feed("http://feeds.bbci.co.uk/news/rss.xml")
        print feed


if __name__ == "__main__":
    unittest.main()
