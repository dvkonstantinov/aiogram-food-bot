# =======клаиватуры админского раздела===========
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_check_accept_kb():
    button = KeyboardButton(text='')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def admin_main_menu_kb():
    button = KeyboardButton(text='Работа с меню')
    button2 = KeyboardButton(text='Работа с блюдами')
    button3 = KeyboardButton(text='Работа с заказами')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2], [button3]],
                                   resize_keyboard=True)
    return keyboard


# Работа с заказами
def admin_work_with_orders_kb():
    button = KeyboardButton(text='Список заказов')
    button2 = KeyboardButton(text='Главное меню')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def admin_choose_orders_kb():
    button = KeyboardButton(text='На сегодня')
    button2 = KeyboardButton(text='На завтра')
    button3 = KeyboardButton(text='На дату')
    button4 = KeyboardButton(text='Главное меню')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2],
                                             [button3, button4]],
                                   resize_keyboard=True)
    return keyboard


# работа с блюдами
def admin_work_with_dishes_kb():
    button = KeyboardButton(text='Список блюд')
    button2 = KeyboardButton(text='Добавить блюдо')
    button3 = KeyboardButton(text='Изменить блюдо')
    button4 = KeyboardButton(text='Удалить блюдо')
    button5 = KeyboardButton(text='Главное меню')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2],
                                             [button3, button4],
                                             [button5]],
                                   resize_keyboard=True)
    return keyboard


def admin_add_dish_noimage_kb():
    button = KeyboardButton(text='Без фото')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def admin_add_dish_check_kb():
    button = KeyboardButton(text='Да, все верно')
    button2 = KeyboardButton(text='Нужно исправить')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def admin_start_repair_dish_kb():
    button = KeyboardButton(text='Название')
    button2 = KeyboardButton(text='Краткое название')
    button3 = KeyboardButton(text='Описание')
    button4 = KeyboardButton(text='Фотография')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2],
                                             [button3, button4]],
                                   resize_keyboard=True)
    return keyboard


def admin_remove_dish_choose_kb():
    button = KeyboardButton(text='Да, уверен')
    button2 = KeyboardButton(text='Отмена!!')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


# работа с меню
def admin_work_with_menus_kb():
    button = KeyboardButton(text='Новое меню')
    button2 = KeyboardButton(text='Удалить меню')
    button3 = KeyboardButton(text='Созданные меню')
    button4 = KeyboardButton(text='Разослать меню')
    button5 = KeyboardButton(text='Главное меню')

    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2],
                                             [button3, button4],
                                             [button5]],
                                   resize_keyboard=True)
    return keyboard


def admin_add_menus_confirm_kb():
    button = KeyboardButton(text='Да, все верно')
    button2 = KeyboardButton(text='Нужно исправить')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def admin_remove_menu_choose_kb():
    button = KeyboardButton(text='Да, уверен')
    button2 = KeyboardButton(text='Отмена!!')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard


def admin_confirm_send_kb():
    button = KeyboardButton(text='Да')
    button2 = KeyboardButton(text='Нет, отмена!')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button, button2]],
                                   resize_keyboard=True)
    return keyboard
