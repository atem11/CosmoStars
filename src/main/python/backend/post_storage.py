import configparser
import time

from backend import main
from grubber import vk_grubber


class Storage:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('src/main/resources/config.ini')
        self.vk_token = config['DEFAULT']['vk_token']
        self.celeb_list = config['DEFAULT']['celeb_list']
        self.last_timestamp = int(time.time()) - 5500000
        self.vk_grubber = vk_grubber.Grubber(self.vk_token)
        self.post_list = []
        self.liked_post = []
        self.refresh()

    def refresh(self):
        ids = open(self.celeb_list, "r")
        upd = []
        _ids = set()
        for celeb_id in ids:
            _ids.add(int(celeb_id))

        for _id in _ids:
            upd.extend(self.vk_grubber.posts(int(_id), self.last_timestamp, 0))
        upd = sorted(upd, key=lambda post: post['date'])

        self.post_list.extend(upd)
        self.last_timestamp = int(time.time())
        return

    def celeb_list(self):
        ids = open(self.celeb_list, "r")
        res = []
        _ids = set()
        for celeb_id in ids:
            _ids.add(int(celeb_id))

        for celeb_id in _ids:
            user = self.vk_grubber.user_info(celeb_id)
            res.append(user['first_name'] + " " + user['last_name'])

        return res

    def post(self, post_id: int):
        post = ''
        for post in self.post_list:
            if post['id'] == post_id:
                post = main.Post(
                    post['id'],
                    post['author'],
                    post['avatar_source'],
                    post['owner_id'],
                    post['text'],
                    post['date'],
                    post['likes'],
                    post['reposts']
                )
                break
        return post

    def like(self, post_id: int):
        post = self.post(post_id)
        self.liked_post.append(post)

    def dislike(self, post_id: int):
        for post in self.liked_post:
            if post.post_id == post_id:
                self.liked_post.remove(post)
                break

    def posts(self, timestamp_start: int, timestamp_end: int):
        res = []
        for post in self.post_list:
            if timestamp_start <= post['data'] <= timestamp_end:
                res.append(main.Post(
                    post['id'],
                    post['author'],
                    post['avatar_source'],
                    post['owner_id'],
                    post['text'],
                    post['date'],
                    post['likes'],
                    post['reposts']
                ))
        return res
