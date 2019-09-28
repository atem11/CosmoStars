import json
import pickle
import time
from datetime import date, datetime
import pandas as pd
import numpy as np

from flask import Flask, request

from backend import post_storage
from backend.stories_grabber import StoriesGrabber

app = Flask(__name__)


class Post:
    # status = 'liked', 'disliked' or 'unknown'
    def __init__(self,
                 post_id: str,
                 status: str,
                 author: str,
                 avatar_source: str,
                 author_id: str,
                 content: str,
                 timestamp: int,
                 likes: int,
                 reposts: int):
        self.post_id = post_id
        self.status = status
        self.author = author
        self.avatar_source = avatar_source
        self.author_id = author_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.reposts = reposts


storage = post_storage.Storage()
stories_grabber = StoriesGrabber()
stories_grabber.grab(date(2019, 7, 1), date.today())

sgd = pickle.load(open("src/main/storage/model.ml", 'rb'))


@app.route('/celeb_list')
def celeb_list():
    return json.dumps(storage.celeb_lst(), ensure_ascii=False)


@app.route('/refresh')
def refresh():
    storage.refresh()


@app.route('/post', methods=['GET'])
def post():
    post_id = request.form['post_id']
    return json.dumps(storage.post(post_id), ensure_ascii=False)


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
    res = []
    for p in storage.liked_post:
        res.append(storage.construct(p))
    return json.dumps(res, ensure_ascii=False)


@app.route('/posts', methods=['GET'])
def posts():
    timestamp_start = int(request.args.get('time_start', 0))
    timestamp_finish = int(request.args.get('time_end', int(time.time() * 1000)))

    texts = []
    posts = storage.posts(timestamp_start, timestamp_finish)
    for p in posts:
        texts.append(p.content)
    df = pd.Series(texts)
    all_probs = sgd.predict_proba(df)
    tags = sgd.classes_[np.argsort(-all_probs)]

    json_list = []
    for i in range(len(posts)):
        probs = all_probs[i]
        high_probable = sum(i > 0.1 for i in probs)
        json_list.append({
            'post': posts[i].__dict__,
            'tags': list(tags[i][:high_probable])
        })
    return json.dumps(json_list, ensure_ascii=False)


@app.route('/stories', methods=['GET'])
def stories():
    from_ts = int(request.args['from'])
    to_ts = int(request.args['to'])
    grabbed = stories_grabber.grab(datetime.fromtimestamp(from_ts).date(), datetime.fromtimestamp(to_ts).date())
    dict_list = list(map(lambda x: {
        'title': x.title,
        'date': time.mktime(x.story_date.timetuple())
    }, grabbed))
    return json.dumps(dict_list, ensure_ascii=False)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
