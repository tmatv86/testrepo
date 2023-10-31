import geopy
import telebot
import os
import certifi
import ssl
from whether import get_whether, f_g_link
from telebot import types
import geopy.geocoders.yandex
from geopy import Nominatim
from checklocation import NService, search_closest_location
from ratess import get_wanted_currency

# global variables
amount = 0
lat = ''
lon = ''

def set_lat(latitude):
    global lat
    lat = latitude

def set_lon(longitude):
    global lon
    lon = longitude

def get_latitude():
    return lat

def get_longitude():
    return lon

def convert_currency(from_currency, to_currency, val):
    res = get_wanted_currency(from_currency.upper(), to_currency.upper(), val)
    return res

def get_api_key():
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv('API_KEY')

def get_my_token():
    from dotenv import load_dotenv
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    return BOT_TOKEN

def get_cert():
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

# create telebot object
bot = telebot.TeleBot(token=get_my_token())

# decorators to manage bot
# ----------------pre-settings-------------------- #
# pip install python-dotenv
# configure .env
# pip install geopy
# ------------------------------------------------ #
# test message bot
@bot.message_handler(commands=['start', 'help', 'info'])
def say_hello(message):
    bot.send_message(message.chat.id, 'Hello, how are you?')
    bot.send_message(message.chat.id, 'Please, use one of the following commands: \n '
                                      '/search - to perform search between locations'
                                      '/currency - to set a currency for change\n'          
                                      '/currencyrate - to see basic currency rates\n'
                                      '/whether - to see whether in your location\n')

@bot.message_handler(commands=['currencyrate'])
def currencyrate(message):
    bot.send_message(message.chat.id, 'This will print you basic rates')

@bot.message_handler(commands=['currency'])
def currency_convertor(message):
    bot.send_message(message.chat.id, "Input sum: ")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Unknown format. Input sum: ")
        bot.register_next_step_handler(message, summa)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    if amount > 0:
        btn1 = types.InlineKeyboardButton('MYR/USD', callback_data='myr/usd')
        btn2 = types.InlineKeyboardButton('USD/MYR', callback_data='usd/myr')
        btn3 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        btn4 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn5 = types.InlineKeyboardButton('MYR/RUB', callback_data='myr/rub')
        btn6 = types.InlineKeyboardButton('RUB/MYR', callback_data='rub/myr')
        btn7 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn8 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')

        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

        bot.send_message(message.chat.id, "Please, select currencies to proceed: ", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Number should be > 0. Input amount: ")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(lambda m: True)
def answer(callback):
    from_curr, to_curr = callback.data.split('/')
    res = convert_currency(from_curr, to_curr, amount)
    responsestr = f"Convertion result {from_curr.upper()} to {to_curr.upper()} " + str(res)
    bot.send_message(callback.message.chat.id, responsestr, parse_mode='html')


@bot.message_handler(commands=["search"])
def geo_search(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send coordinates", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Confirm your coordinates?", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):

    if message.location is not None:

        set_lat(message.location.latitude)
        set_lon(message.location.longitude)
        bot.send_message(message.chat.id, "What do you looking for? ")
        bot.register_next_step_handler(message, general_search)

@bot.message_handler(commands=['whether'])
def get_whether_in_my_city(message):
    city = 'Kuala Lumpur'
    res_message = get_whether(city)
    bot.send_message(message.chat.id, res_message)

def get_my_city(lat, lon):
    get_cert()
    geolocator = Nominatim(scheme='http', user_agent="python-requests/2.31.0")
    location = geolocator.reverse('{}, {}'.format(lat, lon), language='en', exactly_one=True)
    return location.raw['address'].get('city', '')
def general_search(message):

    geo_object = NService()
    addr, min_distance = search_closest_location(str(get_latitude()), str(get_longitude()),
            message.text + ', ' + get_my_city(str(get_latitude()), str(get_longitude())), geo_object)

    if not min_distance:
        result_message = "Not found! Please, change your request details."
    else:
        result_message = f'The closest {message.text} to you: {addr}, ~{min_distance} km'

    req = f_g_link(addr)
    bot.send_message(message.chat.id, result_message)
    bot.send_message(message.chat.id, req)

bot.infinity_polling(none_stop=True)