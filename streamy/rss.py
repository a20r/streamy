#!/usr/bin/env python
import feedparser

from streamy.analyzer.sentiment import SentimentAnalyzer


class RSSReader(object):
    def __init__(self, db):
        self.db = db
        self.targets = {
            "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
            "cnn": "http://rss.cnn.com/rss/edition.rss",
            "fox": "http://feeds.foxnews.com/foxnews/latest",
            "nytimes": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "google": "https://news.google.com/?output=rss",
            "guardian": "http://feeds.theguardian.com/theguardian/world/rss",
            "wall_street_journal": "http://online.wsj.com/xml/rss/3_7085.xml",
            "usa_today": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories"
        }

        if self.db.state != "CONNECTED":
            raise RuntimeError("Not connected to database!")

        self.collections = self.db.return_collections()
        self.sentiment = SentimentAnalyzer()

    def strip_html(self, data):
        tag = False
        quote = False
        out = ""

        for c in data:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

        return out

    def parse_feed(self, target):
        url = self.targets[target]
        feed = feedparser.parse(url)

        entries = []
        for entry in feed["entries"]:
            tags = set((
                self.strip_html(entry["title"])
                + " "
                + self.strip_html(entry["summary"])
            ).split())

            entries.append({
                "source": target,
                "source_link": entry["link"],
                "title": self.strip_html(entry["title"]),
                "summary": self.strip_html(entry["summary"]),
                "date": entry["published"],
                "tags": list(tags)
            })

        return entries

    def record_feed(self):
        for target in self.targets:
            for entry in self.parse_feed(target):
                if not self.collections["rss"].find_one(entry):
                    sentiment = self.sentiment.analyze_text(entry["title"])
                    entry["sentiment"] = sentiment
                    self.collections["rss"].insert(entry)
