import vk_api as vk
import json

class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.VkApi(token=self.token)
        self.api = self.session.get_api()

    def print_info(self, vk_id: str):
        user_id = self.api.users.get(user_ids=[vk_id])[0]['id']
        print(json.dumps(self.api.wall.get(owner_id=-user_id, offset=148273753, extended=1), indent=2))
        return
