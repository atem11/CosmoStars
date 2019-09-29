import configparser
import json
import pickle
import time
from datetime import date, datetime

import emoji
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
                 domain: str,
                 author: str,
                 avatar_source: str,
                 author_id: str,
                 content: str,
                 timestamp: int,
                 likes: int,
                 reposts: int):
        self.post_id = post_id
        self.status = status
        self.domain = domain
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

# TEST
# q1 = "Нотр-Дам"
# q2 = "Богоматери"
#
# for post in storage.post_list:
#     if q1 in post['text'] or q2 in post['text']:
#         print(json.dumps(post, ensure_ascii=False))


# res = search.search("собор Богоматери Нотр-Дам сгорел")
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


@app.route('/add_celeb')
def add_celeb():
    domain = request.form['domain']
    storage.add_celeb(domain)


@app.route('/post', methods=['GET'])
def post():
    post_id = request.form['post_id']
    return json.dumps(storage.post(post_id), ensure_ascii=False)


@app.route('/post_like', methods=['POST'])
def like():
    post_id = request.form['post_id']
    storage.like(post_id)
    return ""


@app.route('/post_dislike', methods=['POST'])
def dis():
    post_id = request.form['post_id']
    storage.dislike(post_id)
    return ""


@app.route('/liked_posts')
def liked_post():
    ans = []
    for p in storage.liked_post:
        ans.append(storage.construct(p))
    # print(ans)
    ans.sort(key=lambda x: x.timestamp)
    ans = [x.__dict__ for x in ans]
    return json.dumps(ans, ensure_ascii=False)


@app.route('/tags', methods=['GET'])
def tags():
    return json.dumps(list(sgd.classes_), ensure_ascii=False)


@app.route('/posts', methods=['GET'])
def posts():
    timestamp_start = int(int(request.args.get('time_start', 0)) / 1000)
    timestamp_finish = int(int(request.args.get('time_end', int(time.time() * 1000))) / 1000)
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

    tags = []
    all_probs = []
    if len(texts) == 0:
        pass
    else:
        df = pd.Series(texts)
        all_probs = sgd.predict_proba(df)
        tags = sgd.classes_[np.argsort(-all_probs)]

    json_list = []
    if len(all_probs) != 0:
        for i in range(len(result_posts)):
            normalized = result_posts[i].content
            normalized = emoji.get_emoji_regexp().sub(r'', normalized)
            if len(normalized) > 100:
                probs = all_probs[i]
                high_probable = sum(i > 0.1 for i in probs)
                result_posts[i].tags = list(tags[i][:high_probable])
                json_list.append(result_posts[i].__dict__)

    grabbed = stories_grabber.grab(datetime.fromtimestamp(timestamp_start).date(),
                                   datetime.fromtimestamp(timestamp_finish).date())
    grabbed = list(filter(lambda x: search.test(x.title), grabbed))
    stories_list = list(map(lambda x: {
        'title': x.title,
        'date': time.mktime(x.story_date.timetuple())
    }, grabbed))
    return json.dumps({
        'posts': json_list,
        'stories': stories_list
    }, ensure_ascii=False)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
