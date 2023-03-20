from config import open_weather_token
import datetime
from aiogram.dispatcher import Dispatcher
import requests
import telebot
from telebot import types
import os
import random

bot = telebot.TeleBot('5848071699:AAHtKvGwVkzpbmeaNVXs1cQEtRwHzOJ96rA')
dp = Dispatcher(bot)

@bot.message_handler(commands= ['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web = types.KeyboardButton("Сайт")
    start = types.KeyboardButton("Привет")
    photo = types.KeyboardButton("Пикча")
    weather = types.KeyboardButton("Прогноз погоды")
    markup.add(web, start, photo, weather)

    mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u> </b>, я Кипарис.'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == "Пикча":
            # photo = open('jihead 2.0.jpg', 'rb')
            DIR = 'arts'
            photo = open(os.path.join(DIR, random.choice(os.listdir(DIR))), 'rb')
            bot.send_photo(message.chat.id, photo)

    if message.chat.type == 'private':
        if message.text == "Сайт":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Заскамиться",url="https://www.youtube.com/watch?v=n5Xwn01sE4Q&ab_channel=TimurGazizulin"))
            bot.send_message(message.chat.id, f'На, держи', reply_markup=markup)

    if message.chat.type == 'private':
        if message.text == "Привет":
            mess = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u> </b>, я Кипарис.'
            bot.send_message(message.chat.id, mess, parse_mode='html')

    if message.text == 'private':
        if message.text == "Прогноз погоды":
            code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
            }

            try:
                r = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
                )
                data = r.json()

                city = data["name"]
                cur_weather = data["main"]["temp"]

                weather_description = data["weather"][0]["main"]
                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    wd = "Посмотри в окно, не пойму что там за погода!"

                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]
                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                length_of_the_day = datetime.datetime.fromtimestamp(
                    data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"])

                bot.send_message(message.chat.id, f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                      f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                      f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                      f"Хорошего дня!", parse_mode='html')

            except:
                bot.send_message(message.chat.id, f"Проверьте название города")


    if message.text != "Привет":
        if message.text != "Сайт":
            if message.text != "Пикча":
                bot.send_message(message.chat.id, f'Не понял. Там же внизу команды есть, напиши их')


# @bot.message_handler(content_types= ['text'])
# def get_user_text(message):
#     if message.text == 'Ку':
#         bot.send_message(message.chat.id, 'Ку', parse_mode='html')
#     elif message.text =='id':
#         bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}', parse_mode='html')
#     elif message.text == 'photo':
#         photo = open('', 'rb')
#         bot.send_photo(message.chat.id, photo)
#     else:
#         bot.send_message(message.chat.id, 'Не понял', parse_mode='html')

@bot.message_handler(content_types= ['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, f'Зачем ты мне отправил фото?', parse_mode='html')

@bot.message_handler(content_types=['sticker'])
def get_user_sticker(message):
    bot.send_message(message.chat.id, f'Найс стикер.', parse_mode='html')

# @bot.message_handler(commands= ['photo'])
# def photo(message):
#     photo = open('', 'rb')
#     bot.send_photo(message.chat.id, photo)

# @bot.message_handler(commands= ['web'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Заскамиться", url="https://www.youtube.com/watch?v=n5Xwn01sE4Q&ab_channel=TimurGazizulin"))
#     bot.send_message(message.chat.id, f'На, держи', reply_markup=markup)

# @bot.message_handler(commands= ['help'])
# def help(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     web = types.KeyboardButton("/web")
#     start = types.KeyboardButton("/start")
#     markup.add(web, start)
#     bot.send_message(message.chat.id, f'Хелп:', reply_markup=markup)




bot.polling(none_stop=True, interval=0)