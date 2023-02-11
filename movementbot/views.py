from django.shortcuts import HttpResponse
import telebot
from django.conf import settings
from .models import Profile
from datetime import date
from .congrats_text import CongratsText
import random
from .horo import Horo
from .events import Events
import json


bot = telebot.TeleBot(settings.BOT_TOKEN)
# https://api.telegram.org/bot6061400466:AAHJnAjiriDTu98rPyt7tF0_kIXsEEPKjBM/setWebhook?url=https://02ea-95-64-192-254.eu.ngrok.io
# https://api.telegram.org/bot6061400466:AAHJnAjiriDTu98rPyt7tF0_kIXsEEPKjBM/deleteWebhook?url=https://9e93-83-242-179-137.eu.ngrok.io/


def index(request):
    # bot.set_webhook('https://9e93-83-242-179-137.eu.ngrok.io/')
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    name = ''
    if message.from_user.last_name is None:
        name = f'{message.from_user.first_name}'
    else:
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f'Привет! {name}\n'
                                      f'Я бот, который будет спамить вам беседу :)\n\n'
                                      f'Чтобы узнать больше команд, напишите /help')


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = list(message.text.split())
    if len(text) == 1:
        bot.send_message(
            message.chat.id,
            '''/start
/register
/birthday
/astro
/events

Напишите /help <Нужная команда без слэша> чтобы узнать о команде подробнее'''
        )
    elif text[1] == 'start':
        bot.send_message(
            message.chat.id,
            '/start - Приветственное сообщение'
        )

    elif text[1] == 'register':
        bot.send_message(
            message.chat.id,
            '/register <Имя> <Тэг> <День рождения (дд.мм.гггг)> - регистрация профиля или его обновление'
        )
    elif text[1] == 'birthday':
        bot.send_message(
            message.chat.id,
            '/birthday - узнать, у кого из зарегестрированных пользователей сегодня день рождения'
        )
    elif text[1] == 'astro':
        bot.send_message(
            message.chat.id,
            '/astro - узнать гороскоп всех знаков\n/astro <Знак> - узнать гороскоп у конкретного знака'
        )
    elif text[1] == 'events':
        bot.send_message(
            message.chat.id,
            '/events - узнать, какие праздники отмечают сегодня'
        )


@bot.message_handler(commands=['register'])
def register(message: telebot.types.Message):
    text = list(message.text.split())
    if len(text) == 4:
        if text[2][0] != '@':
            bot.send_message(message.chat.id, 'Не могу распознать ваш тэг')
        elif '.' not in text[3]:
            bot.send_message(message.chat.id, 'Не могу распознать дату')
        else:
            bot.send_message(message.chat.id, 'Принято...')
            clean_date = list(text[3].split('.'))
            clean_date = date(int(clean_date[2]), int(clean_date[1]), int(clean_date[0]))
            p, _ = Profile.objects.get_or_create(
                foreign_id=message.from_user.id,
                defaults={
                    'id_channel': message.chat.id,
                    'name': text[1],
                    'tg_tag': text[2],
                    'birthday': clean_date
                }
            )
            if _:
                bot.send_message(message.chat.id, 'Профиль создан!')
            else:
                bot.send_message(message.chat.id, 'Такой профиль уже существует, обновляю данные...')
                Profile.objects.filter(foreign_id=message.from_user.id).update(id_channel=message.chat.id,
                                                                               name=text[1], tg_tag=text[2],
                                                                               birthday=clean_date)
                bot.send_message(message.chat.id, 'Профиль обновлен!')
    else:
        bot.send_message(message.chat.id, 'Не хватает данных')


@bot.message_handler(commands=['birthday'])
def birthday(message: telebot.types.Message):
    profiles = Profile.objects.filter(id_channel=message.chat.id).values()
    congrats = []
    for i in profiles:
        if date.today().day == i['birthday'].day and date.today().month == i['birthday'].month:
            congrats.append([i['name'], i['tg_tag'], date.today().year-i['birthday'].year])
    text = ''
    if len(congrats) == 0:
        bot.send_message(message.chat.id, 'Сегодня ни у кого нет дня рождения ((')
    elif len(congrats) == 1:
        text = text + f"Сегодня день рождения празднует {congrats[0][0]} {congrats[0][1]} и ему/ей исполняется" \
                      f" {congrats[0][2]}\n\n{CongratsText.text[random.randint(0, len(CongratsText.text)-1)]}"
    else:
        people = []
        ages = []
        for i in congrats:
            people.append(' '.join((i[0], i[1])))
            ages.append(str(i[2]))
        people = ', '.join(people)
        ages = ', '.join(ages)
        text = text + f"Сегодня день рождения празднует {people} и ему/ей исполняется" \
                      f" {ages}\n\n{CongratsText.text[random.randint(0, len(CongratsText.text) - 1)]}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['all_birthdays'])
def all_birthdays(message):
    if str(message.from_user.id) == settings.ADMIN_ID:
        profiles = Profile.objects.all().values()
        dict_of_congrats = {}
        for i in profiles:
            if date.today().day == i['birthday'].day and date.today().month == i['birthday'].month:
                if i['id_channel'] in list(dict_of_congrats.keys()):
                    dict_of_congrats[i['id_channel']].append([i['name'], i['tg_tag'], date.today().year-i['birthday'].year])
                else:
                    dict_of_congrats[i['id_channel']] = [[i['name'], i['tg_tag'], date.today().year-i['birthday'].year]]
        else:
            for i in dict_of_congrats:
                text = ''
                congrats = dict_of_congrats[i]
                if len(congrats) == 1:
                    text = text + f"Сегодня день рождения празднует {congrats[0][0]} {congrats[0][1]} и ему/ей исполняется"\
                                  f" {congrats[0][2]}\n\n{CongratsText.text[random.randint(0, len(CongratsText.text) - 1)]}"
                else:
                    people = []
                    ages = []
                    for j in congrats:
                        people.append(' '.join((j[0], j[1])))
                        ages.append(str(j[2]))
                    people = ', '.join(people)
                    ages = ', '.join(ages)
                    text = text + f"Сегодня день рождения празднует {people} и ему/ей исполняется" \
                                  f" {ages}\n\n{CongratsText.text[random.randint(0, len(CongratsText.text) - 1)]}"
                bot.send_message(i, text)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к этой команде')


@bot.message_handler(commands=['astro'])
def astro(message: telebot.types.Message):
    horo = Horo()
    message_text = list(message.text.split())
    text = ''
    if len(message_text) == 1:
        text = f'{horo.zodiac_signs["овен"][0]}\n{horo.zodiac_signs["овен"][2]}\n\n' \
               f'{horo.zodiac_signs["телец"][0]}\n{horo.zodiac_signs["телец"][2]}\n\n' \
               f'{horo.zodiac_signs["близнецы"][0]}\n{horo.zodiac_signs["близнецы"][2]}\n\n' \
               f'{horo.zodiac_signs["рак"][0]}\n{horo.zodiac_signs["рак"][2]}\n\n' \
               f'{horo.zodiac_signs["лев"][0]}\n{horo.zodiac_signs["лев"][2]}\n\n' \
               f'{horo.zodiac_signs["дева"][0]}\n{horo.zodiac_signs["дева"][2]}\n\n' \
               f'{horo.zodiac_signs["весы"][0]}\n{horo.zodiac_signs["весы"][2]}\n\n' \
               f'{horo.zodiac_signs["скорпион"][0]}\n{horo.zodiac_signs["скорпион"][2]}\n\n' \
               f'{horo.zodiac_signs["стрелец"][0]}\n{horo.zodiac_signs["стрелец"][2]}\n\n' \
               f'{horo.zodiac_signs["козерог"][0]}\n{horo.zodiac_signs["козерог"][2]}\n\n' \
               f'{horo.zodiac_signs["водолей"][0]}\n{horo.zodiac_signs["водолей"][2]}\n\n' \
               f'{horo.zodiac_signs["рыбы"][0]}\n{horo.zodiac_signs["рыбы"][2]}'
    elif message_text[1].lower() in list(horo.zodiac_signs.keys()):
        text = f'{horo.zodiac_signs[message_text[1].lower()][0]}\n{horo.zodiac_signs[message_text[1].lower()][2]}'
    else:
        text = 'Не удалось распознать команду'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['events'])
def events(message):
    events = Events()
    bot.send_message(message.chat.id, f'Сегодня {str(date.today())} отмечаются праздники:\n\n'+"\n".join(events.list_of_events))