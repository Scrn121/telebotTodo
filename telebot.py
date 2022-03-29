import telebot
from telebot import types
import random
from random import choice

token = "#"

bot = telebot.TeleBot(token)

RANDOM_TASKS = ["Поесть", "Поспать", "Погулять", "Поиграть"]

HELP = """
Всем привет! Данный бот поможет вам запоминать важные дела на конкретные даты!
written by @kmi121"""

todos = dict()

def add_todo (date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]

def random_add(message):
    task = random.choice(RANDOM_TASKS)
    add_todo ('сегодня', task)
    bot.send_message(message.chat.id, f' Задача {task} добавлена на сегодня' )

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton('help')
    btn2 = types.KeyboardButton('add')
    btn3 = types.KeyboardButton('show')
    btn4 = types.KeyboardButton('random')

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, text="Привет, {0.first_name}! что ты хочешь сделать?".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['add'])
def get_date(message):
    bot.reply_to(message, 'Введите дату');
    bot.register_next_step_handler(message, get_task);

def get_task(message):
    global date
    date=message.text
    bot.reply_to(message, 'введите задачу');
    bot.register_next_step_handler(message, add);

def add(message):
global task
    task = message.text
    if date in todos and task in todos[date]:
        bot.send_message(message.chat.id, f'задача {task} уже есть на {date}')
    else:
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача {task} добавлена на {date}')

@bot.message_handler(commands=['show'])

def show_date(message):
    bot.reply_to(message, 'Введите дату');
    bot.register_next_step_handler(message, show)

def show(message):
    global date
    date = message.text.lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "help"):
        bot.send_message(message.chat.id, HELP)
    elif (message.text == "random"):
        random_add(message)
    elif (message.text == "add"):
        get_date(message)
    elif (message.text == "show"):
        show_date(message)



#Обращение к серверам TG (while run)
bot.polling(none_stop=True)

