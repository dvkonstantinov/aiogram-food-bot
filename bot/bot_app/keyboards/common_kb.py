from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


def start_kb():
    button = KeyboardButton(text='Начать')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def reg_kb():
    button = KeyboardButton(text='Зарегистрироваться')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def confirm_reg_kb():
    button = KeyboardButton(text='Да, все верно')
    button2 = KeyboardButton(text='Есть ошибки')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def start_using():
    button = KeyboardButton(text='Что за правила?')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def ready_repair_reg_kb():
    button = KeyboardButton(text='Давай исправим')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def remove_kb():
    kb = ReplyKeyboardRemove()
    return kb
