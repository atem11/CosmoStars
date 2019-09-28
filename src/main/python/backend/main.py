from flask import Flask, request
from backend import post_storage
import time

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


storage = post_storage.Storage()


@app.route('/celeb_list')
def celeb_list():
    return storage.celeb_lst()


@app.route('/refresh')
def refresh():
    storage.refresh()


@app.route('/post', methods=['POST'])
def post():
    post_id = request.form['post_id']
    return storage.post(post_id)


@app.route('/post_like', methods=['POST'])
def like():
    post_id = request.form['post_id']
    return storage.like(post_id)


@app.route('/post_dislike', methods=['POST'])
def dis():
    post_id = request.form['post_id']
    return storage.dislike(post_id)


@app.route('/liked_posts')
def liked_post():
    return storage.liked_post


@app.route('/posts', methods=['GET'])
def posts():
    timestamp_start = int(request.args.get('time_start', 0))
    timestamp_finish = int(request.args.get('time_end', int(time.time() * 1000)))
    return storage.posts(timestamp_start, timestamp_finish)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
