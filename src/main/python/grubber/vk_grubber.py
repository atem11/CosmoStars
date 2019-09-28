import vk_api as vk


class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.VkApi(token=self.token)
        self.api = self.session.get_api()

    def posts(self, vk_id: int, timestamp: int):
        user_id = self.api.users.get(user_ids=[vk_id])[0]['id']
        try:
            post_list = self.api.wall.get(owner_id=user_id, count=100, filter="owner")
            ans_list = []
            for post in post_list['items']:
                if int(post['date']) > timestamp:
                    item = {'id': post['id'],
                            'owner_id': post['owner_id'],
                            'date': post['date'],
                            'text': post['text'],
                            'attachments': []
                            }
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
            print("wall closed " + str(vk_id))
            return []
