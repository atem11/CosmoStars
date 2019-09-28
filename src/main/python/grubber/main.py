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
    for celeb_id in ids:
        cnt += 1
        print("grub celeb num=" + str(cnt) + " id=" + celeb_id)
        res = test.posts(int(celeb_id), 1564617600)  # 2019/august/01 00:00:00
        result.extend(res)

    result = sorted(result, key=lambda post: post['date'], reverse=True)
    out = open("../../resources/celeb_posts.json", "w")
    out.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
