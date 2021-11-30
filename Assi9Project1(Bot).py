import telebot

import segno
from telebot import types
import math
from datetime import datetime
from persiantools.jdatetime import JalaliDate ,JalaliDateTime
from gtts import gTTS
import random

bot = telebot.TeleBot("2132705025:AAHEkyiqIyPu9QtVS56gqp07WfWSEZ069zc")

count = 1


def Click():
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Restart the game', )
    markup.add(button)


@bot.message_handler(commands=['start'])
def hi(message):
    bot.reply_to(message, f'Welcome {message.from_user.first_name}')


@bot.message_handler(commands=['game'])
def game(message):
    bot.reply_to(message, "Welcome to the game of the Number")
    Click()
    msg = bot.send_message(message.chat.id,
                           'Please Pick a number between 1 and 15? you only got 6 tries so choose wisely',
                           reply_markup=markup)
    attempt = 1
    number = random.randint(1, 15)
    bot.register_next_step_handler(msg, lambda message: Random_number(message, attempt, number))


def Random_number(message, attempt, number):
    text = message.text
    if text.isdigit() == True:
        n = int(text)

        if attempt < 6:
            attempt += 1
            if n < number:
                msg = bot.send_message(message.chat.id, 'Bozorg tar ast')
                bot.register_next_step_handler(msg, lambda message: Random_number(message, attempt, number))


            elif n > number:
                msg = bot.send_message(message.chat.id, 'Kochek tar ast')
                bot.register_next_step_handler(msg, lambda message: Random_number(message, attempt, number))

            else:
                bot.send_message(message.chat.id,
                                 'You won the game , game is over Restart the game if you wanna play more '.format(
                                     attempt - 1))
        else:
            bot.send_message(message.chat.id, 'You lost >:) game terminated'.format(number))

    elif text == 'Restart the game':
        bot.send_message(message.chat.id, "You restart the game")
        game(message)

    elif text == 'Exit' or text == 'exit':
        bot.send_message(message.chat.id, "We are out use /help for other commands to proceed ")


    elif text[0] == "/":
        msg = bot.send_message(message.chat.id, 'Please enter either a number or Exit')
        bot.register_next_step_handler(msg, lambda message: Random_number(message, attempt, number))
    else:
        msg = bot.send_message(message.chat.id, 'Please enter either a number or Exit')
        bot.register_next_step_handler(msg, lambda message: Random_number(message, attempt, number))


try_age_count = 0


@bot.message_handler(commands=['age'])
def age_jalili(message):
    global try_age_count
    if try_age_count < 1:
        bot.reply_to(message, "Welcome to age calculator")
    else:
        pass
    msg = bot.send_message(message.chat.id, "please enter your birthday date like this Year/Month/Day")
    bot.register_next_step_handler(msg, lambda message: age_calculator(message))


def age_calculator(message):
    global try_age_count
    text = message.text
    format = "%Y/%m/%d"

    try:
        datetime.strptime(text, format)
        if len(text) == 10:
            day_difference = JalaliDate.today() - JalaliDateTime(int(text[0:4]), int(text[5:7]), int(text[8:10]))
            day_difference = day_difference.days
            age_result = day_difference / 365
            bot.send_message(message.chat.id, f'You are {math.trunc(age_result)} years old')
            bot.send_message(message.chat.id, f'command is over use /help for more commands')


        elif len(text) == 9 and text[6] == '/':
            day_difference = JalaliDate.today() - JalaliDateTime(int(text[0:4]), int(text[5:6]), int(text[7:9]))
            day_difference = day_difference.days
            age_result = day_difference / 365
            bot.send_message(message.chat.id, f'You are {math.trunc(age_result)} years old')
            bot.send_message(message.chat.id, f'command is over use /help for more commands')


        elif len(text) == 9 and text[6] != '/':
            day_difference = JalaliDate.today() - JalaliDateTime(int(text[0:4]), int(text[5:7]), int(text[8:9]))
            day_difference = day_difference.days
            age_result = day_difference / 365
            bot.send_message(message.chat.id, f'You are {math.trunc(age_result)} years old')
            bot.send_message(message.chat.id, f'command is over use /help for more commands')


        elif len(text) == 8:
            day_difference = JalaliDate.today() - JalaliDateTime(int(text[0:4]), int(text[5:6]), int(text[7:8]))
            day_difference = day_difference.days
            age_result = day_difference / 365
            bot.send_message(message.chat.id, f'You are {math.trunc(age_result)} years old')
            bot.send_message(message.chat.id, f'command is over use /help for more commands')

    except:
        bot.send_message(message.chat.id, f'Invalid input try again')
        try_age_count += 1
        bot.register_next_step_handler(message, age_jalili(message))


@bot.message_handler(commands=['voice'])
def tts_bot(message):
    bot.reply_to(message, "Welcome to text to speech ")
    msg = bot.send_message(message.chat.id, "please enter a sentence you want to be convereted to audio")
    bot.register_next_step_handler(msg, lambda message: tts_action(message))


def tts_action(message):
    text_tts = message.text
    language = 'en'
    my_tts_obj = gTTS(text=text_tts, lang=language, slow=False)
    my_tts_obj.save("voice.mp3")
    voice = open('voice.mp3', 'rb')
    bot.send_voice(message.chat.id, voice)
    bot.send_message(message.chat.id, f'command is over use /help for more commands')


max_counter = 0


@bot.message_handler(commands=['max'])
def max(message):
    global max_counter
    if max_counter < 1:
        bot.reply_to(message, "Welcome to Maximum finder")
    else:
        pass
    msg = bot.send_message(message.chat.id, "Please enter array of numbers like this 1,2,3,4 or 1 2 3 4")
    bot.register_next_step_handler(msg, lambda message: max_finder(message))


def max_finder(message):
    global max_counter
    text = message.text
    try:
        if text.find(',') == True:
            array = (text).split(",")
        elif text.find(' ') == True:
            array = (text).split(" ")

        array_int_map = map(int, array)
        array_int = list(array_int_map)
        max_value = None
        for num in array_int:
            if (max_value is None or num > max_value):
                max_value = num
        bot.send_message(message.chat.id, f'Your max is = {max_value}')
        bot.send_message(message.chat.id, "command is over use /help for more commands")

    except:
        bot.send_message(message.chat.id, f'invalid input pleaase try again')
        max_counter += 1
        bot.register_next_step_handler(message, max(message))


max_index_counter = 0


@bot.message_handler(commands=['argmax'])
def max_index(message):
    global max_index_counter
    if max_index_counter < 1:
        bot.reply_to(message, "Welcome to Find the index of maximum ")
    else:
        pass
    msg = bot.send_message(message.chat.id, "Please enter array of numbers like this 1,2,3,4 or 1 2 3 4")
    bot.register_next_step_handler(msg, lambda message: max_index_action(message))


def max_index_action(message):
    global max_index_counter
    text = message.text
    try:
        if text.find(',') == True:
            array = (text).split(",")
        elif text.find(' ') == True:
            array = (text).split(" ")

        array_int_map = map(int, array)
        array_int = list(array_int_map)
        max_value = None
        for num in array_int:
            if (max_value is None or num > max_value):
                max_value = num

        max_value_index = array_int.index(max_value)
        bot.send_message(message.chat.id, f'index of the maximum number of array is {max_value_index}')
        bot.send_message(message.chat.id, "command is over use /help for more commands")

    except:
        bot.send_message(message.chat.id, f'invalid input pleaase try again')
        max_index_counter += 1
        bot.register_next_step_handler(message, max_index(message))


@bot.message_handler(commands=['qrcode'])
def qrcode(message):
    bot.reply_to(message, "Welcome to qrcode generator")
    msg = bot.send_message(message.chat.id, "Please enter sentence or anything for qrcode generation")
    bot.register_next_step_handler(msg, lambda message: qrcode_generator(message))


def qrcode_generator(message):
    text = message.text
    qrcode = segno.make(text)
    qrcode.save('text.png', scale=15)
    photo = open('text.png', 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['best_username_for_github'])
def meme(message):
    bot.send_photo(message.chat.id, "https://ibb.co/zmjTXjc")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, '''   

    /start is for warm welcome to my bot

/game  is a random guessing number game

/age   is for calculating the your age according to jalili date

/voice is for converting a text to audio

/max is for finding the maximum in array of numbers

/argmax for finding the index of maximum of that array

/qrcode is for generating a sentence to qrcode

/best_username_for_github its just a silly meme dont give me a zero

    '''
                 )


@bot.message_handler(content_types=['text'])
def MessageChecker(message):
    text = message.text
    if text == 'Restart the game':
        bot.send_message(message.chat.id, "You restart the game")
        game(message)


bot.infinity_polling()