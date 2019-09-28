from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import List

import feedparser
import requests


@dataclass
class Story:
    story_date: date
    title: str


class StoriesGrabber:
    MONTH_MAPPER = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }

    def __init__(self):
        self._cache = {}

    def grab(self, from_date: date, to_date: date) -> List[Story]:
        result = []
        for single_date in self._daterange(from_date, to_date):
            if single_date in self._cache:
                result.append(self._cache[single_date])
            else:
                cache_line = []
                month = StoriesGrabber.MONTH_MAPPER[single_date.month]
                url = u"https://ru.wikinews.org/w/index.php?title=Служебная:NewsFeed&feed=atom&categories=" + str(
                    single_date.day) + "_" + month + "_" + str(
                    single_date.year) + "%7CОпубликовано&notcategories=Не%20публиковать&namespace=0&count=15&ordermethod=categoryadd&stablepages=only"

                cache_file = Path("src/main/storage/stories/" + single_date.strftime("%d_%m_%Y"))
                if cache_file.is_file():
                    with open(cache_file, "r") as file:
                        content = file.read()
                else:
                    req = requests.get(url)
                    with open(cache_file, "w") as file:
                        file.write(req.text)
                    content = req.text

                feed = feedparser.parse(content)
                for post in feed.entries:
                    cache_line.append(Story(single_date, post['title']))
                self._cache[single_date] = cache_line
                result.append(cache_line)
        return result

    @staticmethod
    def _daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


def main():
    stories_grabber = StoriesGrabber()
    stories_grabber.grab(date(2019, 7, 1), date.today())


if __name__ == "__main__":
    main()
