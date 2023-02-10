from bs4 import BeautifulSoup
import requests


class Horo():
    def __init__(self):
        self.zodiac_signs = {
            "овен": ['♈️  Овен', 'aries'],
            "телец": ['♉️  Телец', 'taurus'],
            "близнецы": ['♊️  Близнецы', 'gemini'],
            "рак": ['♋️  Рак', 'cancer'],
            "лев": ['♌️  Лев', "leo"],
            "дева": ['♍️  Дева', 'virgo'],
            "весы": ['♎️  Весы', 'libra'],
            "скорпион": ['♏️  Скорпион', 'scorpio'],
            "стрелец": ['♐️  Стрелец', 'sagittarius'],
            "козерог": ['♑️  Козерог', 'capricorn'],
            "водолей": ['♒️  Водолей', 'aquarius'],
            "рыбы": ['♓️  Рыбы', 'pisces']
        }
        for i in self.zodiac_signs:
            req = requests.get(f'https://horo.mail.ru/prediction/{self.zodiac_signs[i][1]}/today/')
            soup = BeautifulSoup(req.content, 'html.parser')
            data = soup.find('div', attrs={
                'class': 'article__item article__item_alignment_left article__item_html'
            })
            self.zodiac_signs[i].append(data.p.text)