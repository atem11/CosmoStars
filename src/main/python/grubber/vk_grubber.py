import vk


class Grubber:

    def __init__(self):
        self.token = "78e2215a78e2215a78e2215a91788f3d73778e278e2215a256c671320107ea57d007f2a"
        self.session = vk.Session(access_token=self.token)
        self.api = vk.API(self.session)
        pass

    def print_info(self, addr: str):
        print(self.api.users.get(user_ids=1))
        return
