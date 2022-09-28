# Работа с меню
import re
import time
from datetime import date, timedelta, datetime

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey
from aiogram.exceptions import TelegramForbiddenError

from bot_app.bot_create import bot
from bot_app.data_exchanger import (list_menus, list_dishes,
                                    add_new_menu,
                                    get_menu, remove_menu, list_users)
from bot_app.handlers.admin.admin_handlers import admin_main_menu
from bot_app.handlers.admin.dishes_handlers import (admin_list_dishes,
                                                    admin_get_formalized_dish,
                                                    client_get_formalized_dish)
from bot_app.handlers.utils import validate_date
from bot_app.keyboards.admin_kb import (admin_work_with_menus_kb,
                                        admin_add_menus_confirm_kb,
                                        admin_remove_menu_choose_kb,
                                        admin_confirm_send_kb)
from bot_app.keyboards.common_kb import remove_kb
from bot_app.keyboards.user_kb import client_yes_no_kb
from bot_app.phrases.admin_phrases import (MENU_MAIN, MENU_CREATE_START,
                                           MENU_ALREADY_EXIST, MENU_TITLE,
                                           ALL_MENUS, ENTER_MENU_ID,
                                           CHECK_MENU_DATA,
                                           CHECK_MENU_DATA_2,
                                           CHECK_MENU_DATA_3, MENU_SAVE_TO_DB,
                                           MENU_SAVE_TO_DB_ERR,
                                           MENU_SAVE_AGAIN, MENU_IN_DB,
                                           CHECK_INT, ID_NOT_FOUND,
                                           CHECK_MENU_ID_ERR,
                                           MENU_RM_LIST, MENU_RM_LIST_2,
                                           MENU_RM, MENU_RM_NOT_EXIST,
                                           MENU_RM_ERR,
                                           MENU_RM_CANCEL, MENU_SEND_LIST,
                                           CONFIRM_SEND_MENU, MSG_DELAY,
                                           MENU_CLIENT_TEXT,
                                           MENU_CLIENT_TEXT_2)
from bot_app.states import AdminState, UserState


async def admin_work_with_menus(message: types.Message, state: FSMContext):
    """Раздел работы с меню. Ожидания выбора действия."""
    await bot.send_message(text=MENU_MAIN,
                           chat_id=message.from_user.id,
                           reply_markup=admin_work_with_menus_kb())
    await state.set_state(AdminState.wait_admin_work_with_menus_choose)


async def admin_work_with_menus_choose(message: types.Message,
                                       state: FSMContext):
    """Распределение после выбора действия над меню."""
    if message.text == 'Новое меню':
        await state.set_state(AdminState.wait_admin_create_menus_start)
        return await admin_create_menus_start(message, state)
    elif message.text == 'Удалить меню':
        await state.set_state(AdminState.wait_admin_remove_menus)
        return await admin_remove_menus(message, state)
    elif message.text == 'Созданные меню':
        text = await admin_list_menus()
        await bot.send_message(text=text,
                               chat_id=message.from_user.id)
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)
    elif message.text == 'Разослать меню':
        await state.set_state(AdminState.wait_admin_send_menu)
        return await admin_send_menu(message, state)
    elif message.text == 'Главное меню':
        await state.set_state(AdminState.wait_admin_main_menu)
        return await admin_main_menu(message, state)


async def admin_create_menus_start(message: types.Message, state: FSMContext):
    """Создание нового меню. Ожидание ввода даты, на которое создается меню."""
    await bot.send_message(text=MENU_CREATE_START,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_create_menus_validate_date)


async def admin_create_menus_validate_date(message: types.Message,
                                           state: FSMContext):
    """Проверка введенной даты на валидность, проверка наличия меню на 
    указанную дату в базе данных. Запрос название нового меню."""
    my_date = message.text
    formalized_date = await validate_date(message, my_date)
    if not formalized_date:
        await state.set_state(AdminState.wait_admin_create_menus_start)
        return await admin_create_menus_start(message, state)
    available_menus = await list_menus()
    for menu in available_menus:
        if str(formalized_date) == str(menu['date_of_menu']):
            await bot.send_message(text=MENU_ALREADY_EXIST,
                                   chat_id=message.from_user.id)
            await state.set_state(AdminState.wait_admin_work_with_menus)
            return await admin_work_with_menus(message, state)
    await state.update_data(menu_date=str(formalized_date))
    await bot.send_message(text=MENU_TITLE,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_create_menus_title)


async def admin_create_menus_title(message: types.Message, state: FSMContext):
    """Обработка названия меню."""
    menu_title = message.text
    await state.update_data(menu_title=menu_title)
    await state.set_state(AdminState.wait_admin_create_menus_dishes)
    return await admin_create_menus_dishes(message, state)


async def admin_create_menus_dishes(message: types.Message, state: FSMContext):
    """Вывод таблицы уже созданных блюд, предложение выбрать из них те,
    которые нужно добавлять в создаваемое меню. Ввод валидируется
    соответствием регулярному выражению. Формат ввода, например: 3, 12, 8, 4,
    9."""
    dishes = await admin_list_dishes()
    await bot.send_message(text=ALL_MENUS.format(dishes),
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await bot.send_message(text=ENTER_MENU_ID,
                           chat_id=message.from_user.id)
    await state.set_state(AdminState.wait_admin_create_menus_dishes_check)


async def admin_create_menus_dishes_check(message: types.Message,
                                          state: FSMContext):
    """Валидация введенных данных. Проверка соответствия шаблону. Проверка
    на наличие введенных ID блюд в базе данных"""
    added_dishes = message.text.replace(" ", "")
    r = r'^((([1-9](\d?)+)([,])([\s]?))+([1-9](\d?)+))$|^(([1-9](\d?)+))$'
    pattern = re.compile(r)
    if re.match(pattern, added_dishes):
        add_dishes_list = added_dishes.split(',')
    else:
        await bot.send_message(text=CHECK_MENU_DATA,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(AdminState.wait_admin_create_menus_dishes)
        return await admin_create_menus_dishes(message, state)

    add_dishes_list = [int(item) for item in add_dishes_list]
    available_dishes = await list_dishes()
    dishes_list = []
    for added_dish_id in add_dishes_list:
        try:
            dishes_list.append(
                next(dish for dish in available_dishes['json'] if dish['id'] ==
                     added_dish_id))
        except StopIteration:

            await bot.send_message(
                text=CHECK_MENU_DATA_2.format(added_dish_id),
                chat_id=message.from_user.id,
                reply_markup=remove_kb()
            )
            await state.set_state(AdminState.wait_admin_create_menus_dishes)
            return await admin_create_menus_dishes(message, state)
    added_dishes_ids = []
    [added_dishes_ids.append(dish['id']) for dish in dishes_list]
    data = await state.get_data()
    await state.update_data(menu_dishes_id=added_dishes_ids,
                            dishes_list=dishes_list)
    await bot.send_message(text=CHECK_MENU_DATA_3.format(data["menu_date"],
                                                         data["menu_title"]),
                           chat_id=message.from_user.id,
                           reply_markup=admin_add_menus_confirm_kb())
    for dish_instance in dishes_list:
        await admin_get_formalized_dish(message, dish_instance)
    await state.set_state(AdminState.wait_admin_create_menus_confirm)


async def admin_create_menus_confirm(message: types.Message,
                                     state: FSMContext):
    """Сохранение нового меню в базу, либо возврат в начало в случае
    необходимости исправления."""
    if message.text == 'Да, все верно':
        data = await state.get_data()
        current_date = datetime.strptime(data['menu_date'],
                                         "%Y-%m-%d").date().isoformat()
        menu_data = {'title': data['menu_title'],
                     'date_of_menu': current_date,
                     'dishes': data['menu_dishes_id']}

        response = await add_new_menu(menu_data)
        text = ''
        if response['status'] == 201:
            text = MENU_SAVE_TO_DB
        else:
            text = MENU_SAVE_TO_DB_ERR
        await bot.send_message(text=text,
                               chat_id=message.from_user.id)
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)

    elif message.text == 'Нужно исправить':
        await bot.send_message(text=MENU_SAVE_AGAIN,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(AdminState.wait_admin_create_menus_start)
        return await admin_create_menus_start(message, state)


# Удаление меню
async def admin_list_menus():
    """Выводит список доступных меню из базы."""
    response = await list_menus()
    text = MENU_IN_DB
    for item in response:
        text += (f'{item["date_of_menu"]} | <b>{item["id"]}</b> | '
                 f'{item["title"]}\n')
    return text


async def admin_formalized_list_dishes(message: types.Message, dishes_list):
    """Цикл, выводящий стилизованный вид блюда для списка блюд в меню"""
    if isinstance(dishes_list, list):
        for dish in dishes_list:
            await admin_get_formalized_dish(message, dish)


async def admin_get_formalized_menu(message: types.Message, menu_instance):
    """Выводит меню в оформленном виде."""
    menu = menu_instance
    menu_id = menu['id']
    menu_date = menu['date_of_menu']
    menu_title = menu['title']
    formalized_menu = (f'<b>Id меню: </b>\n{menu_id}\n'
                       f'<b>Дата меню: </b>\n{menu_date}\n'
                       f'<b>Название: </b>\n{menu_title}\n'
                       f'<b>Блюда в меню:</b>')
    await bot.send_message(text=formalized_menu,
                           chat_id=message.from_user.id)
    await admin_formalized_list_dishes(message, menu['dishes'])


async def admin_check_id_menu_value(message: types.Message):
    """Проверка правильности введенного id меню."""
    menu_id = message.text
    response = await get_menu(menu_id)
    try:
        int(menu_id)
    except ValueError:
        await bot.send_message(text=CHECK_INT,
                               chat_id=message.from_user.id)
        return response['json'], False
    if response['status'] == 404:
        await bot.send_message(text=ID_NOT_FOUND,
                               chat_id=message.from_user.id)
        return response['json'], False
    elif response['status'] == 200:
        return response['json'], True
    else:
        await bot.send_message(text=CHECK_MENU_ID_ERR,
                               chat_id=message.from_user.id)
        return response['json'], False


async def admin_remove_menus(message: types.Message, state: FSMContext):
    """Список меню и введение id меню для удаления из базы."""
    menus = await admin_list_menus()
    await bot.send_message(text=MENU_RM_LIST.format(menus),
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await bot.send_message(text=MENU_RM_LIST_2,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_remove_menu_choose)


async def admin_remove_menu_choose(message: types.Message, state: FSMContext):
    """Просмотр удаляемого меню."""
    menu_instance, is_correct_digit = await admin_check_id_menu_value(
        message)
    if not is_correct_digit:
        await state.set_state(AdminState.wait_admin_remove_menus)
        return await admin_remove_menus(message, state)
    await state.update_data(menu_id=message.text)
    text = 'Вы хотите удалить вот это меню?'
    await admin_get_formalized_menu(message, menu_instance)
    await bot.send_message(text=text,
                           chat_id=message.from_user.id,
                           reply_markup=admin_remove_menu_choose_kb())
    await state.set_state(AdminState.wait_admin_remove_menu_confirm)


async def admin_remove_menu_confirm(message: types.Message, state: FSMContext):
    """Удаление меню из базы данных."""
    if message.text == 'Да, уверен':
        data = await state.get_data()
        menu_id = data['menu_id']
        response = await remove_menu(menu_id)
        if response['status'] == 204:
            text = MENU_RM
        elif response['status'] == 404:
            text = MENU_RM_NOT_EXIST.format(response)
        else:
            text = MENU_RM_ERR.format(response)
        await bot.send_message(text=text,
                               chat_id=message.from_user.id,
                               reply_markup=admin_work_with_menus_kb())
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)
    elif message.text == 'Отмена!!':
        await bot.send_message(text=MENU_RM_CANCEL,
                               chat_id=message.from_user.id,
                               reply_markup=admin_work_with_menus_kb())
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)


async def admin_send_menu(message: types.Message, state: FSMContext):
    """Список меню с их ID, запрос id на рассылку меню на завтра."""
    menus = await admin_list_menus()
    await bot.send_message(text=MENU_SEND_LIST.format(menus),
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_confirm_choose_send_menu)


async def admin_confirm_choose_send_menu(message: types.Message,
                                         state: FSMContext):
    """Валидация id меню, ознакомление с рассылаемыми данными, предложение
    рассылки меню пользователям."""
    menu, is_correct_digit = await admin_check_id_menu_value(message)
    if not is_correct_digit:
        await state.set_state(AdminState.wait_admin_send_menu)
        return await admin_send_menu(message, state)
    await state.update_data(menu=menu)
    tomorrow = date.today() + timedelta(days=1)
    formalized_menu = (f'<b>Id меню: </b>\n{menu["id"]}\n'
                       f'<b>Дата меню: </b>\n{menu["date_of_menu"]}\n'
                       f'<b>Название: </b>\n{menu["title"]}\n')
    await bot.send_message(
        text=CONFIRM_SEND_MENU.format(tomorrow, formalized_menu),
        chat_id=message.from_user.id,
        reply_markup=admin_confirm_send_kb())
    await state.set_state(AdminState.wait_admin_send_menu_run)


async def admin_send_menu_run(message: types.Message, state: FSMContext):
    """Обработка ответа. Если да - производится рассылка, если нет - возврат
     в раздел работы с меню"""
    if message.text == 'Да':
        data = await state.get_data()
        menu = data['menu']
        await bot.send_message(text=MSG_DELAY,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        cnt = await admin_send_menu_to_client(state, menu)
        text = (f'Меню разослал всем.\n'
                f'Успешных отправок: {cnt["delivered"]}\n'
                f'Бот заблокирован у: {cnt["blocked"]}')
        await bot.send_message(text=text,
                               chat_id=message.from_user.id)
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)
    elif message.text == 'Нет, отмена!':
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)


async def admin_send_menu_to_client(state: FSMContext, menu):
    """Непосредственно рассылка меню пользователям."""
    all_users = await list_users()
    cnt = {
        'delivered': 0,
        'blocked': 0,
    }
    for user in all_users:
        if (not user['is_admin'] and user['is_register']
                and user['is_allow_mail']):
            try:
                await bot.send_message(
                    text=MENU_CLIENT_TEXT.format(menu["date_of_menu"]),
                    chat_id=user['user_id'])
                await client_formalized_list_dishes(menu['dishes'],
                                                    user['user_id'])
                await bot.send_message(text=MENU_CLIENT_TEXT_2,
                                       chat_id=user['user_id'],
                                       reply_markup=client_yes_no_kb())
                key = StorageKey(bot_id=bot.id,
                                 chat_id=user['user_id'],
                                 user_id=user['user_id'])
                await state.storage.set_state(
                    bot=bot,
                    key=key,
                    state=UserState.wait_client_if_order
                )
                await state.storage.update_data(bot=bot,
                                                key=key,
                                                data={'menu': menu})
                cnt['delivered'] += 1
                time.sleep(1)
            except TelegramForbiddenError:
                cnt['blocked'] += 1
    return cnt


async def client_formalized_list_dishes(dishes_list, client_id):
    """Красивое представление блюд для списка блюд в меню."""
    if isinstance(dishes_list, list):
        for dish in dishes_list:
            await client_get_formalized_dish(dish, client_id)
