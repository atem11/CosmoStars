import vk_api as vk


class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.VkApi(token=self.token)
        self.api = self.session.get_api()

    def print_info(self, vk_id: str):
        print(self.api.wall.get(owner_id=-1, domain=vk_id, cout=1))
        return
