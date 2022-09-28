from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.bot_create import bot
from bot_app.data_exchanger import list_orders
from bot_app.handlers.admin.admin_handlers import admin_main_menu
from bot_app.handlers.utils import validate_date, create_csv_file
from bot_app.keyboards.admin_kb import (admin_work_with_orders_kb,
                                        admin_choose_orders_kb)
from bot_app.keyboards.common_kb import remove_kb
from bot_app.phrases.admin_phrases import (ORDER_MENU_TEXT,
                                           ORDER_CHOOSE_DATE,
                                           ENTER_DATE, NO_ORDERS)
from bot_app.states import AdminState


async def admin_work_with_orders(message: types.Message, state: FSMContext):
    """Меню работы с заказами."""
    await bot.send_message(text=ORDER_MENU_TEXT,
                           chat_id=message.from_user.id,
                           reply_markup=admin_work_with_orders_kb())
    await state.set_state(AdminState.wait_admin_choose_orders)


async def admin_choose_orders(message: types.Message, state: FSMContext):
    """Обработка кнопок меню работы с заказами."""
    if message.text == 'Список заказов':
        await bot.send_message(text=ORDER_CHOOSE_DATE,
                               chat_id=message.from_user.id,
                               reply_markup=admin_choose_orders_kb())
        await state.set_state(AdminState.wait_admin_list_orders)
    elif message.text == 'Главное меню':
        await state.set_state(AdminState.wait_admin_main_menu)
        return await admin_main_menu(message, state)


async def admin_list_orders(message: types.Message, state: FSMContext):
    """Просмотр совершенных заказов по дням."""
    if message.text == 'На сегодня' or message.text == 'На завтра':
        await state.set_state(
            AdminState.wait_admin_list_orders_by_date_execute)
        return await admin_list_orders_by_date_execute(message, state)
    elif message.text == 'На дату':
        await state.set_state(AdminState.wait_admin_list_orders_by_date)
        return await admin_list_orders_by_date(message, state)
    elif message.text == 'Главное меню':
        await state.set_state(AdminState.wait_admin_main_menu)
        return await admin_main_menu(message, state)


async def admin_list_orders_by_date(message: types.Message, state: FSMContext):
    """Указание даты, на которую нужно посмотреть заказы. Дата в формате
    ДД.ММ.ГГГГ ."""
    await bot.send_message(text=ENTER_DATE,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_list_orders_by_date_execute)


async def admin_list_orders_by_date_execute(message: types.Message,
                                            state: FSMContext):
    """Просмотр заказов на определенную дату."""
    if message.text == 'На сегодня':
        today = datetime.today().strftime('%d.%m.%Y')
        search_date = today
    elif message.text == 'На завтра':
        today = datetime.today()
        delta = timedelta(days=1)
        tomorrow = today + delta
        search_date = tomorrow.strftime('%d.%m.%Y')
    else:
        search_date = message.text
    formalized_date = await validate_date(message, search_date)
    if not formalized_date:
        await state.set_state(AdminState.wait_admin_list_orders_by_date)
        return await admin_list_orders_by_date(message, state)
    orders = await list_orders(formalized_date)
    if not orders['json']:
        text = NO_ORDERS
        await bot.send_message(text=text.format(formalized_date),
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        return await admin_work_with_orders(message, state)
    else:
        file, caption = create_csv_file(orders)
        await bot.send_document(message.from_user.id, file, caption=caption)
    await state.set_state(AdminState.wait_admin_main_menu)
    return await admin_main_menu(message, state)
