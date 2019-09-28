import configparser
import time

from grubber import vk_grubber


class Storage:
    def __init__(self, timestamp: int):
        config = configparser.ConfigParser()
        config.read('../../resources/config.ini')
        self.celeb_list = config['DEFAULT']['celeb_list']
        self.vk_token = config['DEFAULT']['vk_token']
        self.last_timestamp = timestamp
        self.vk_grubber = vk_grubber.Grubber(self.vk_token)
        self.post_list = []
        self.refresh()

    def refresh(self):
        ids = open(self.celeb_list, "r")
        upd = []
        _ids = set()
        for celeb_id in ids:
            _ids.add(int(celeb_id))

        for _id in _ids:
            upd.extend(self.vk_grubber.posts(int(_id), self.last_timestamp))
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
