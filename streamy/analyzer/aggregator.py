#!/usr/bin/env python
from bson.code import Code
from pattern.en import parse


class Aggregator(object):
    def __init__(self, db):
        self.db = db

        if self.db.state != "CONNECTED":
            raise RuntimeError("Not connected to database!")

        self.collections = self.db.return_collections()

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

        tags = []
        result = self.collections["result"].find().sort("value", -1)
        for res in result:
            parse_result = parse(res["_id"])

            if "NNP" in parse_result:
                tags.append({"tag": res["_id"], "count": res["value"]})

        return tags
