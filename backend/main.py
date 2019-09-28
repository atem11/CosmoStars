from flask import Flask, request
from itertools import islice
import time
import json

app = Flask(__name__)


class Post:
    def __init__(self,
                 post_id: str,
                 author: str,
                 avatar_source: str,
                 author_id: str,
                 content: str,
                 timestamp: int,
                 likes: int,
                 reposts: int):
        self.post_id = post_id
        self.author = author
        self.avatar_source = avatar_source
        self.author_id = author_id
        self.content = content
        self.timestamp = timestamp
        self.likes = likes
        self.reposts = reposts


POSTS = [
    Post("123", "Ольга Бузова", "https://sun9-69.userapi.com/c850324/v850324431/1dffa7/7hexV-7y-P8.jpg?ava=1", "olgabuzova",
         "Владивосток 🙏🏻 Родина моей мамочки.... Здесь мой дедушка ходил в океан🚢 познакомился с "
         "бабушкой, и здесь же родилась моя мамуля❤️ Жили на Косом переулке😙и мама пешком сама в 7 "
         "лет шла до 13 школы, где и училась, пока не переехали в Клайпеду ...Я жду вас всех сегодня "
         "в Палладе на моем шоу «Принимай меня» 🙌🏻 Новые песни, новая программа...Мы на месте 🚀 "
         "Вот она я👸🏻 Кто сегодня с нами? Пишите 🥰", int(time.time() * 1000), 10, 5),

    Post("4567", "Ольга Бузова", "https://sun9-69.userapi.com/c850324/v850324431/1dffa7/7hexV-7y-P8.jpg?ava=1", "olgabuzova",
         "Мои дорогие, поздравляю вас с великим и светлым праздником Рождества Пресвятой "
         "Богородицы🌹🌹🌹Хочу пожелать вам счастья и веры в чудеса☀🤲🏻 Я верю в то, "
         "что добро всегда побеждает, что искренняя молитва творит чудеса и что нет ничего "
         "невозможного для тех, кто верит... Пусть в вашем сердце царит мир и любовь, и Богородица "
         "хранит вас от всего плохого. Она всех слышит и всем помогает! Я благодарна Небесам за всё, "
         "что происходит в моей жизни и верю, что самое главное чудо ещё впереди 🙏🏻♾... А у вас "
         "случались чудеса? Поделитесь своей историей🙏🏼 Что считаете главным чудом в своей жизни?",
         int(time.time()) - 1000, 100, 90),
    Post("kek", "Всеволод Степанов", "https://sun9-15.userapi.com/c853520/v853520142/d3c45/XxvJnu46ke0.jpg?ava=1",
         "id186108519", "КУКАРЕКУ ОЛОЛО ПЫЩЬПЫЩЬ", int(time.time() * 1000) - 20000, 1, 0),

    Post("kok", "Павел Дуров", "https://sun9-53.userapi.com/c836333/v836333001/31192/y1Cm4JfplhQ.jpg?ava=1", "durov",
         "Иногда говорят, что Telegram был заблокирован в России, так как “закон есть закон”. Однако "
         "Telegram заблокирован в России как раз вопреки главному закону страны – Конституции. Решения "
         "судов и законы, противоречащие Конституции, не имеют силы. А это значит, что и сама "
         "блокировка Telegram незаконна. Если бы ФСБ ограничилась запросом информации о нескольких "
         "террористах, то ее требование вписывалось бы в рамки Конституции. Однако речь идет о "
         "передаче универсальных ключей шифрования с целью последующего бесконтрольного доступа к "
         "переписке неограниченного круга лиц. A это – прямое нарушение 23-й статьи Конституции о "
         "праве каждого на тайну переписки. По этой причине юристы из “Агоры” сегодня обжаловали "
         "решение Верховного суда России о законности приказа ФСБ. Надеюсь, власти России откажутся от "
         "языка неисполнимых ультиматумов, на котором сегодня ведется диалог с технологическими "
         "компаниями. Независимо от этого, мы продолжим борьбу за Telegram в России. История наших "
         "предков учит биться до победного конца. С Днем Победы!", int(time.time() * 1000) - 40000,
         1000000, 20000),
]

liked_posts = []


@app.route('/feed')
def feed():
    start_timestamp = int(request.args.get("timestamp", time.time() * 1000))
    count = int(request.args.get("count", 5))

    posts = islice(filter(lambda post: post.timestamp <= start_timestamp, POSTS), 0, count)
    return json.dumps(list(map(lambda post: post.__dict__, posts)))


@app.route('/liked_posts')
def liked_posts():
    start_timestamp = int(request.args.get("timestamp", time.time() * 1000))
    count = int(request.args.get("count", 5))

    posts = islice(filter(lambda post: post.timestamp <= start_timestamp, liked_posts), 0, count)
    return json.dumps(list(map(lambda post: post.__dict__, posts)))


@app.route('/like', methods=['POST'])
def like():
    post_id = request.form['post_id']
    liked_posts.extend(filter(lambda post: post.post_id == post_id, POSTS))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
