import vk


class Grubber:

    def __init__(self, vk_token: str):
        self.token = vk_token
        self.session = vk.Session(access_token=self.token)
        self.api = vk.API(self.session)
        pass

    def print_info(self, addr: str):
        print(self.api.users.get(user_ids=1))
        return
