import vk_api as vk


class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.VkApi(token=self.token)
        self.session.auth(token_only="true")
        self.api = self.session.get_api()

    def print_info(self, vk_id: str):
        print(self.api.wall.get(domain=vk_id, cout=5))
        return
