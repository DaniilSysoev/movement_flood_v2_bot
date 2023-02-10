import requests
from bs4 import BeautifulSoup


class Events:
    def __init__(self):
        self.list_of_events = []

        req = requests.get('https://my-calend.ru/holidays')
        soup = BeautifulSoup(req.content, 'html.parser')

        ul = soup.find('ul', attrs={
            'class': 'holidays-items'
        })
        li = ul.findAll('li')
        for i in li:
            if i.find('a') is not None:
                self.list_of_events.append(i.find('a').text)
            else:
                self.list_of_events.append(i.find('span').text)