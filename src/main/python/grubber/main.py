import configparser
import json

from grubber.vk_grubber import Grubber


def main():
    config = configparser.ConfigParser()
    config.read('../../resources/config.ini')
    vk_token = config['DEFAULT']['vk_token']

    test = Grubber(vk_token)
    ids = open("../../resources/celebrities_id.txt", "r")
    result = []
    cnt = 0
    _ids = set()
    for celeb_id in ids:
        _ids.add(int(celeb_id))

    for celeb_id in _ids:
        cnt += 1
        print("grub celeb num=" + str(cnt) + " id=" + str(celeb_id))
        res = test.posts(celeb_id, 0, 0)  # 2019/august/01 00:00:00 1564617500
        result.extend(res)
        res = test.posts(celeb_id, 0, 100)
        result.extend(res)

    result = sorted(result, key=lambda post: post['date'])
    out = open("../../resources/celeb_posts.json", "w")
    out.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
