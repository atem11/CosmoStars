from flask import Flask, request
from itertools import islice
from backend import post_storage

import time
import json

app = Flask(__name__)


class Post:
    def __init__(self,
                 post_id: str,
                 author: str,
                 avatar_source: str,
                 author_id: str,
                 content: str,
                 timestamp: int,
                 likes: int,
                 reposts: int):
        self.post_id = post_id
        self.author = author
        self.avatar_source = avatar_source
        self.author_id = author_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.reposts = reposts


class Celeb:
    def __init__(self, first_name: str, last_name: str):
        self.name = first_name + ' ' + last_name


storage = post_storage.Storage(1564617500)


@app.route('/celeb_list')
def celeb_list():
    return storage.celeb_list()


@app.route('/refresh')
def refresh():
    storage.refresh()


@app.route('/liked_posts')
def liked_posts():
    start_timestamp = int(request.args.get("timestamp", time.time() * 1000))
    count = int(request.args.get("count", 5))

    posts = islice(filter(lambda post: post.timestamp <= start_timestamp, liked_posts), 0, count)
    return json.dumps(list(map(lambda post: post.__dict__, posts)))


@app.route('/like', methods=['POST'])
def like():
    post_id = request.form['post_id']
    liked_posts.extend(filter(lambda post: post.post_id == post_id))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
