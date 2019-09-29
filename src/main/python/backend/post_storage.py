import configparser
import time
import os
import json

from backend import main
from grubber import vk_grubber


class Storage:
    def __init__(self):
        self.time_window = 5500000
        config = configparser.ConfigParser()
        config.read('src/main/resources/config.ini')
        self.vk_token = config['DEFAULT']['vk_token']
        self.celeb_list = config['DEFAULT']['celeb_list']
        self.storage_path = config['DEFAULT']['storage']
        self.storage_celeb = config['DEFAULT']['celebs']
        self.last_timestamp = int(time.time()) - self.time_window
        self.vk_grubber = vk_grubber.Grubber(self.vk_token)

        self.celeb_ids = set()
        self.celeb_names = []

        self.post_list = []
        self.liked_post = []

        if os.path.exists(self.storage_celeb):
            with open(self.storage_celeb, "r") as f:
                self.celeb_names = json.load(f)
            for celeb in self.celeb_names:
                self.celeb_ids.add(int(celeb['id']))
        else:
            with open(self.celeb_list, "r") as f:
                for _id in f:
                    self.celeb_ids.add(int(_id))
            self.refresh_celeb()

        for post in self.post_list:
            if post['status'] == "liked":
                self.liked_post.append(post)

        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                self.post_list = json.load(f)
        else:
            self.refresh()

    def save_celeb(self):
        (dirs, file) = os.path.split(self.storage_celeb)
        os.makedirs(dirs, exist_ok=True)
        with open(self.storage_celeb, "w") as f:
            f.write(json.dumps(self.celeb_names, ensure_ascii=False))

    def refresh_celeb(self):
        upd = []
        for _id in self.celeb_ids:
            usr = self.vk_grubber.user_info(_id)
            upd.append({'id': _id,
                        'domain': usr['domain'],
                        'name': usr['first_name'] + " " + usr['last_name']
                        })
        self.celeb_names = upd
        self.save_celeb()

    def save_data(self):
        (dirs, file) = os.path.split(self.storage_path)
        os.makedirs(dirs, exist_ok=True)
        with open(self.storage_path, "w") as f:
            f.write(json.dumps(self.post_list, ensure_ascii=False))

    def refresh(self):
        upd = []
        for _id in self.celeb_ids:
            upd.extend(self.vk_grubber.posts(int(_id), self.last_timestamp, 0))
        upd = sorted(upd, key=lambda post: post['date'])
        self.post_list.extend(upd)
        self.last_timestamp = self.post_list[-1]['date']
        self.save_data()
        return upd

    def celeb_lst(self):
        return self.celeb_names

    def add_celeb(self, domain):
        user = self.vk_grubber.user_info(domain)
        if user['id'] in self.celeb_ids:
            return
        else:
            usr = {'id': user['id'],
                   'domain': user['domain'],
                   'name': user['first_name'] + " " + user['last_name']
                   }
            self.celeb_ids.add(usr['id'])
            self.celeb_names.append(usr)
            self.save_celeb()
            upd = self.vk_grubber.posts(usr['id'], self.last_timestamp - self.time_window, 0)
            self.post_list.extend(upd)
            self.post_list = sorted(self.post_list, key=lambda post: post['date'])
            self.save_data()

    def post_by_id(self, post_id: int):
        for post in self.post_list:
            if post['id'] == int(post_id):
                return post

    @staticmethod
    def construct(post):
        return main.Post(
            post['id'],
            post['status'],
            post['domain'],
            post['author'],
            post['avatar_source'],
            post['owner_id'],
            post['text'],
            post['date'],
            post['likes'],
            post['reposts']
        )

    def post(self, post_id: int):
        return self.construct(self.post_by_id(post_id))

    def like(self, post_id: int):
        post = self.post_by_id(post_id)
        post['status'] = "liked"
        if not (post in self.liked_post):
            self.liked_post.append(post)

    def dislike(self, post_id: int):
        post = self.post_by_id(post_id)
        post['status'] = "disliked"
        if post in self.liked_post:
            self.liked_post.remove(post)

    def posts(self, timestamp_start: int, timestamp_end: int):
        res = []
        for post in self.post_list:
            if timestamp_start <= post['date'] <= timestamp_end:
                res.append(self.construct(post))
        return res
