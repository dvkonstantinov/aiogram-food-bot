import csv
import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import FSInputFile

from bot_app.bot_create import bot
from bot_app.keyboards.common_kb import remove_kb
from bot_app.phrases.common_phrases import VALIDATE_DATE_TEXT


async def get_data_to_validate(state: FSMContext):
    """Запрос данных для валидации"""


def validate_phone(message: types.Message):
    """Проверка введенного номера телефона"""
    phone = message.text
    pattern = re.compile(
        r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    if not re.match(pattern, phone):
        return False
    else:
        return phone


def validate_name(message: types.Message):
    """Проверка введенного имени или фамилии"""
    name = message.text
    pattern = re.compile(
        r'^[-a-zA-Zа-яА-Яё]+$')
    if not re.match(pattern, name):
        return False
    else:
        return name


async def validate_date(message: types.Message, my_date):
    """Проверка на валидность введенной даты.  Принимается дата в формате
    ДД.ММ.ГГГГ ."""
    pattern = re.compile('(^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.]('
                         '19|20)[0-9]{2}$)')
    if not re.match(pattern, my_date):
        await bot.send_message(text=VALIDATE_DATE_TEXT,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        formalized_date = None
        return formalized_date
    else:
        formalized_date = datetime.strptime(my_date, "%d.%m.%Y").date()
        return formalized_date


def create_csv_file(orders):
    """Функция возвращает csv файл orders.csv и его название. Через
    stringIO создать не получилось, не смог решить проблему с кодировкой
    файла на выходе."""
    fieldnames = ['Имя', 'Фамилия', 'Телефон', 'Дата меню',
                  'Название меню', 'Порций', 'Оплата', 'Сдача с',
                  'Способ получения', 'Адрес доставки', 'Комментарий']
    cnt_users = 0
    cnt_servings = 0
    with open('orders.csv', mode='w', encoding='windows-1251',
              newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(fieldnames)
        for order in orders['json']:
            csvdata = [
                order['user']['input_firstname'],
                order['user']['input_lastname'],
                order['user']['input_phone'],
                order['menu']['date_of_menu'],
                order['menu']['title'],
                order['num_of_servings'],
                order['payment_type'],
                order['cash_change'],
                order['delivery'],
                order['delivery_address'],
                order['comment']
            ]
            writer.writerow(csvdata)
            cnt_users += 1
            cnt_servings += int(order['num_of_servings'])
    caption = (f'Всего заказало человек: {cnt_users} \n'
               f'Общее количество порций: {cnt_servings}\n'
               f'Подробности в документе')
    f.close()
    file = FSInputFile("orders.csv",
                       filename=f"Заказы на"
                                f" {order['menu']['date_of_menu']}.csv")
    return file, caption


def check_case_serving(count):
    """Подбор правильного окончания для слово "порция"."""
    mes1 = 'порция'
    mes2 = 'порции'
    mes3 = 'порций'
    mes_count = ''
    try:
        count = int(count)
        if count % 10 == 1:
            mes_count = mes1
        elif 1 <= count % 10 <= 4:
            mes_count = mes2
        elif 5 <= count % 10 <= 9 or count % 10 == 0:
            mes_count = mes3
        return mes_count
    except TypeError:
        pass
