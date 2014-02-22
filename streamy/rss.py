#!/usr/bin/env python
import feedparser

rss_targets = [
    "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "http://feeds.bbci.co.uk/news/rss.xml",
]


class RSS(object):
    def __init__(self):
        self.state = "IDLE"

    def parse_feed(self, feed_url):
        return feedparser.parse(feed_url)
