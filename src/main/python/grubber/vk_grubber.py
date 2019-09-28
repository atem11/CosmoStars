import vk_api as vk


class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.VkApi(token=self.token)
        self.api = self.session.get_api()

    def user_info(self, vk_id: int):
        user = self.api.users.get(user_ids=[vk_id])[0]
        return user

    def posts(self, vk_id: int, timestamp: int):
        user = self.api.users.get(user_ids=[vk_id], fields='photo_200')[0]
        try:
            post_list = self.api.wall.get(owner_id=user['id'], count=100, filter="owner")
            ans_list = []
            for post in post_list['items']:
                if int(post['date']) > timestamp:
                    if post['owner_id'] == user['id']:
                        item = {'id': post['id'],
                                'owner_id': post['owner_id'],
                                'date': post['date'],
                                'text': post['text'],
                                'attachments': [],
                                'author': user['first_name'] + " " + user['last_name'],
                                'avatar_source': "",
                                'likes': post['likes']['count'],
                                'reposts': post['reposts']['count']
                                }
                        if 'photo_200' in user:
                            item['avatar_source'] = user['photo_200']
                        if 'attachments' in post:
                            item['attachments'] = post['attachments']
                        elif 'copy_history' in post:
                            item['attachments'].append({'type': 'repost',
                                                        'repost': {
                                                            'id': post['copy_history'][0]['id'],
                                                            'owner_id': post['copy_history'][0]['owner_id']
                                                        }
                                                        })
                        ans_list.append(item)
            return ans_list
        except vk.exceptions.ApiError:
            print("wall closed " + user['first_name'] + " " + user['last_name'])
            return []
