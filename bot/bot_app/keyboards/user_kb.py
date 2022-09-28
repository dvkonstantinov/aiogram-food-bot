# =======клаиватуры клиентского раздела===========
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def enter_client_section_kb():
    button = KeyboardButton(text='Согласен')
    button2 = KeyboardButton(text='Отказаться')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


# Клиентский раздел
def client_yes_no_kb():
    button = KeyboardButton(text='Да')
    button2 = KeyboardButton(text='Нет')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def client_sel_payment_kb():
    button = KeyboardButton(text='Оплата по карте')
    button2 = KeyboardButton(text='Оплата наличными')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def client_sel_delivery_kb():
    button = KeyboardButton(text='Самовывоз')
    button2 = KeyboardButton(text='Доставка')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def client_comment_kb():
    button = KeyboardButton(text='Пропустить')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def client_check_order_kb():
    button = KeyboardButton(text='Да, все верно')
    button2 = KeyboardButton(text='Нет, исправить')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def client_try_again():
    button = KeyboardButton(text='Попробовать снова')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard
