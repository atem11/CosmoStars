import configparser
import json
import pickle
import time
from datetime import date, datetime
import pandas as pd
import numpy as np

from flask import Flask, request

from backend import post_storage
from backend.stories_grabber import StoriesGrabber
from backend import whoosh_search

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

config = configparser.ConfigParser()
config.read('src/main/resources/config.ini')
create = False
if config['DEFAULT']['create_index'] == "True":
    create = True
search = whoosh_search.Searcher(config['DEFAULT']['index_root'], create)
if create:
    search.create(storage.post_list)
#
# res = search.search("Полный список Умного голосования на выборах в Мосгордуму 2019")
# for _id in res:
#     print(json.dumps(storage.post_by_id(_id), ensure_ascii=False))

sgd = pickle.load(open("src/main/storage/model.ml", 'rb'))


@app.route('/celeb_list')
def celeb_list():
    return json.dumps(storage.celeb_lst(), ensure_ascii=False)


@app.route('/refresh')
def refresh():
    upd = storage.refresh()
    search.update(upd)


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
    ans = []
    for p in storage.liked_post:
        ans.append(storage.construct(p))
    return json.dumps(ans, ensure_ascii=False)


@app.route('/posts', methods=['GET'])
def posts():
    timestamp_start = int(request.args.get('time_start', 0))
    timestamp_finish = int(request.args.get('time_end', int(time.time() * 1000)))
    query = request.args.get('query', None)

    texts = []
    result_posts = []
    if query is None:
        result_posts.extend(storage.posts(timestamp_start, timestamp_finish))
    else:
        ids = search.search(query)
        for post_id in ids:
            find = storage.post(post_id)
            result_posts.append(find)

    for p in result_posts:
        texts.append(p.content)

    df = pd.Series(texts)
    all_probs = sgd.predict_proba(df)
    tags = sgd.classes_[np.argsort(-all_probs)]

    json_list = []
    for i in range(len(result_posts)):
        probs = all_probs[i]
        high_probable = sum(i > 0.1 for i in probs)
        post[i].tags = list(tags[i][:high_probable])
        json_list.append(result_posts[i].__dict__)
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
