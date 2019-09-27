import configparser

from grubber.vk_grubber import Grubber


def main():
    config = configparser.ConfigParser()
    config.read('../../resources/config.ini')
    vk_token = config['DEFAULT']['vk_token']

    test = Grubber(vk_token)
    test.print_info("olgabuzova")


if __name__ == "__main__":
    main()
