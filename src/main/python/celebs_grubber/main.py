import configparser
import vk_api
from russian_names import RussianNames


def main():
    config = configparser.ConfigParser()
    config.read('../../resources/config.ini')
    login = config['DEFAULT']['personal_login']
    password = config['DEFAULT']['personal_password']

    vk_session = vk_api.VkApi(login, password)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()

    rn = RussianNames(count=10000, patronymic=False, surname=False)
    names_with_repeats = rn.get_batch()
    unique_names = sorted(set(names_with_repeats))

    with open("../../resources/celebrities_id.txt", "w") as file:
        for name in unique_names:
            result = vk.users.search(q=name, sort=0, fields=['verified', 'followers_count'], count=1000)
            for person in result['items']:
                if 'verified' in person and 'followers_count' in person:
                    if person['verified'] == 1 and person['followers_count'] > 100000:
                        file.write(str(person['id']))
                        file.write("\n")
                        print(person['first_name'] + " " + person['last_name'] + " " + str(person['id']))
            print("###########")


if __name__ == "__main__":
    main()
