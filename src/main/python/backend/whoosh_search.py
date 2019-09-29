import os
import emoji
from whoosh import qparser
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser


class Searcher:
    def __init__(self, root, create=False):
        self.root = root
        if not os.path.exists(root):
            os.makedirs(root, exist_ok=True)
        self.schema = Schema(id=ID(stored=True), content=TEXT)
        if not create:
            self.ix = open_dir(root)
            self.parser = QueryParser("content", self.ix.schema, group=qparser.OrGroup)

    def create(self, posts: list):
        self.ix = create_in(self.root, self.schema)
        self.parser = QueryParser("content", self.ix.schema, group=qparser.OrGroup)
        self.update(posts)

    def update(self, upd: list):
        writer = self.ix.writer()
        for post in upd:
            text = post['text']
            text = emoji.get_emoji_regexp().sub(r'.', text)
            if text != "":
                writer.add_document(id=str(post['id']),
                                    content=text)
        writer.commit()

    def test(self, query):
        rank = 10
        q = self.parser.parse(query)
        res = self.ix.searcher().search(q, limit=5)
        valid = True
        for item in res:
            if item.score < rank:
                valid = False
        return valid

    def search(self, query):
        q = self.parser.parse(query)
        res = self.ix.searcher().search(q, limit=5)
        ans = []
        for item in res:
            ans.append(item['id'])
        return ans
