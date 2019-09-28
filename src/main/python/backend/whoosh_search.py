import os
import emoji
from whoosh import qparser
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser


class Searcher:
    def __init__(self, root):
        self.root = root
        if not os.path.exists(root):
            os.mkdir(root)
        schema = Schema(id=ID(stored=True), content=TEXT)
        self.ix = create_in(root, schema)
        self.parser = QueryParser("content", self.ix.schema, group=qparser.OrGroup)

    def create(self, posts: list):
        writer = self.ix.writer()

        for post in posts:
            text = post['text']
            text = emoji.get_emoji_regexp().sub(r'.', text)
            if text != "":
                writer.add_document(id=str(post['id']),
                                    content=text)
        writer.commit()

    def search(self, query):
        q = self.parser.parse(query)
        res = self.ix.searcher().search(q, limit=50)
        ans = []
        for item in res:
            ans.append(item['id'])
        return ans
