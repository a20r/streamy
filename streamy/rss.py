#!/usr/bin/env python
import feedparser


class RSSReader(object):
    def __init__(self, db):
        self.db = db
        self.rss_targets = {
            "bbc_news": "http://feeds.bbci.co.uk/news/rss.xml",
            "cnn": "http://rss.cnn.com/rss/edition.rss",
            "fox": "http://feeds.foxnews.com/foxnews/latest",
            "nytimes": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        }

        if self.db.state != "CONNECTED":
            raise RuntimeError("Not connected to database!")

        self.collections = self.db.return_collections()

    def parse_feed(self, target):
        url = self.rss_targets[target]
        feed = feedparser.parse(url)

        entries = []
        for entry in feed["entries"]:
            entries.append({
                "title": entry["title"],
                "summary": entry["summary"],
                "date": entry["published"]
            })

        return entries

    def record_feed(self, target):
        entries = self.parse_feed(target)
        self.collections[target].insert(entries)
