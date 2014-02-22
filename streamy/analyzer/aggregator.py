#!/usr/bin/env python
import nltk

from bson.code import Code


class Aggregator(object):
    def __init__(self, db):
        self.db = db

        if self.db.state != "CONNECTED":
            raise RuntimeError("Not connected to database!")

        self.collections = self.db.return_collections()

    def find_tags(self, tag_prefix, tagged_text):
        """
        Find tokens matching the specified tag_prefix
        """
        cfd = nltk.ConditionalFreqDist(
            (tag, word) for (word, tag) in tagged_text
            if tag.startswith(tag_prefix)
        )
        return dict((tag, cfd[tag].keys()[:5]) for tag in cfd.conditions())

    def word_cloud(self):
        map_code = Code("""
function() {
    if (!this.tags) {
        return;
    }

    this.tags.forEach(function(tag) {
        emit(tag, 1);
    });
}
        """)

        reduce_code = Code("""
function(key, values) {
    var count = 0;

    for (var i = 0; i < values.length; i++) {
        count += values[i];
    }

    return count;
}
        """)

        self.collections["rss"].map_reduce(
            map_code,
            reduce_code,
            "result"
        )

        words = []
        result = self.collections["result"].find()
        for res in result:
            words.append(res["_id"])

        # Tokenize the raw text
        tokens = nltk.word_tokenize(" ".join(words))

        # Tag the tokens with their type - ie are they nouns or not
        tokens = nltk.pos_tag(tokens)

        # find all the proper nouns and print them out
        tags = []
        tag_dict = self.find_tags('NNP', tokens)
        for tag in sorted(tag_dict):
            tags.extend(tag_dict[tag])

        return tags
