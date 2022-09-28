# ==================работа с блюдами==================
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from bot_app.bot_create import BASE_URL
from bot_app.bot_create import bot
from bot_app.data_exchanger import (list_dishes, add_dish, get_dish,
                                    edit_dish, remove_dish)
from bot_app.handlers.admin.admin_handlers import admin_main_menu
from bot_app.keyboards.admin_kb import (admin_work_with_dishes_kb,
                                        admin_add_dish_noimage_kb,
                                        admin_add_dish_check_kb,
                                        admin_start_repair_dish_kb,
                                        admin_remove_dish_choose_kb)
from bot_app.keyboards.common_kb import remove_kb
from bot_app.phrases.admin_phrases import (DISH_MENU_TEXT, ADM_CHOOSE_DISH,
                                           ADM_CHOOSE_DISH_2, LIST_DISH,
                                           ADM_ADD_TITLE, ADM_ADD_DESCR,
                                           ADM_ADD_PHOTO, ADD_TO_DB,
                                           DISH_REPAIR, DISH_REPAIR_2,
                                           DISHES_TO_REPAIR,
                                           CHECK_ID_ERR, ID_DISH_404,
                                           ID_DISH_OTHER_ERR,
                                           START_REPAIR_DISH,
                                           START_REPAIR_DISH_2, DISH_EDIT_DATA,
                                           DISH_EDIT_DATA_2, DISH_EDIT_DATA_3,
                                           DISH_EDIT_DATA_4, DISH_EDIT_SUCCESS,
                                           DISH_EDIT_ERR, DISH_RM_ENTER_ID,
                                           DISH_RM_ACCEPT, DISH_RM_CONFIRM,
                                           DISH_RM_CONFIRM_2,
                                           DISH_RM_CONFIRM_3,
                                           DISH_RM_CANCEL)
from bot_app.states import AdminState


async def admin_work_with_dishes(message: types.Message, state: FSMContext):
    """Меню работы с блюдами."""
    await bot.send_message(text=DISH_MENU_TEXT,
                           chat_id=message.from_user.id,
                           reply_markup=admin_work_with_dishes_kb())
    await state.set_state(AdminState.wait_admin_choose_dishes)


async def admin_choose_dishes(message: types.Message, state: FSMContext):
    """Обработка кнопок из меню работы с блюдами."""
    if message.text == 'Список блюд':
        text = await admin_list_dishes()
        await bot.send_message(text=text,
                               chat_id=message.from_user.id)
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)
    elif message.text == 'Добавить блюдо':
        await bot.send_message(text=ADM_CHOOSE_DISH,
                               chat_id=message.from_user.id)
        await bot.send_message(text=ADM_CHOOSE_DISH_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(AdminState.wait_admin_add_dish_title)
    elif message.text == 'Изменить блюдо':
        await state.set_state(AdminState.wait_admin_repair_dish)
        return await admin_repair_dish(message, state)
    elif message.text == 'Удалить блюдо':
        await state.set_state(AdminState.wait_admin_remove_dish)
        return await admin_remove_dish(message, state)
    elif message.text == 'Главное меню':
        await state.set_state(AdminState.wait_admin_main_menu)
        return await admin_main_menu(message, state)


# Список доступных блюд
async def admin_list_dishes():
    """Представление списка доступных блюд в базе данных"""
    response = await list_dishes()
    text = LIST_DISH
    for item in response['json']:
        text += f'{item["id"]}: {item["shortname"]}\n'
    return text


# Добавление блюда
async def admin_add_dish_title(message: types.Message, state: FSMContext):
    """Добавление нового блюда. Краткое название блюда."""
    await state.update_data(title=message.text)
    await bot.send_message(text=ADM_ADD_TITLE,
                           chat_id=message.from_user.id)
    await state.set_state(AdminState.wait_admin_add_dish_shortname)


async def admin_add_dish_shortname(message: types.Message, state: FSMContext):
    """Добавление нового блюда. Описание блюда."""
    await state.update_data(shortname=message.text)
    await bot.send_message(text=ADM_ADD_DESCR,
                           chat_id=message.from_user.id)
    await state.set_state(AdminState.wait_admin_add_dish_descr)


async def admin_add_dish_descr(message: types.Message, state: FSMContext):
    """Добавление нового блюда. Фотография блюда, либо без фотографии."""
    await state.update_data(descr=message.text)
    await bot.send_message(text=ADM_ADD_PHOTO,
                           chat_id=message.from_user.id,
                           reply_markup=admin_add_dish_noimage_kb())
    await state.set_state(AdminState.wait_admin_add_dish_photo)


async def admin_add_dish_photo(message: types.Message, state: FSMContext):
    """Добавление нового блюда. Обработка информации, фотографии и вывод
    пользователю на подтверждение."""
    data = await state.get_data()
    text = ''
    if message.photo:
        mes_img = message.photo[-1]
        file_id = mes_img.file_id
        file = await bot.get_file(file_id)
        filename = mes_img.file_id
        await state.update_data(image=file.file_path,
                                filename=filename,
                                image_id=file_id)
        text = (f'Теперь проверим как это выглядит:\n'
                f'Название: {data["title"]}\n'
                f'Короткое название: {data["shortname"]}\n'
                f'Описание: {data["descr"]}\n'
                f'Фото: на которое отвечаю')
    if message.text:
        await state.update_data(image=None,
                                filename=None,
                                image_id=None)
        text = (f'Теперь проверим как это выглядит:\n'
                f'Название: {data["title"]}\n'
                f'Короткое название: {data["shortname"]}\n'
                f'Описание: {data["descr"]}\n'
                f'Фото: Без фото')
    await message.reply(text=text,
                        reply_markup=admin_add_dish_check_kb())
    await state.set_state(AdminState.wait_admin_confirm_add_dish_data)


async def admin_confirm_add_dish_data(message: types.Message,
                                      state: FSMContext):
    """Сохранение блюда в базу данных в случае подтверждения, возврат в
    начало добавления блюда в случае отказа."""
    data = await state.get_data()
    if message.text == 'Да, все верно':
        image = None
        if data["image"]:
            image_path = data["image"]
            image = (await bot.download_file(image_path)).read()
        dish_data = {
            'title': data["title"],
            'shortname': data["shortname"],
            'description': data["descr"],
            'image': image,
            'image_id': data["image_id"],
            'filename': data["filename"],
        }
        await add_dish(dish_data)
        await bot.send_message(text=ADD_TO_DB,
                               chat_id=message.from_user.id)
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)

    elif message.text == 'Нужно исправить':
        await bot.send_message(text=DISH_REPAIR,
                               chat_id=message.from_user.id)
        await bot.send_message(text=DISH_REPAIR_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(AdminState.wait_admin_add_dish_title)


# исправление блюда
async def admin_repair_dish(message: types.Message, state: FSMContext):
    """Исправление блюда. Ввод ID блюда из базы."""
    dishes = await admin_list_dishes()
    text = (f'{dishes}\n'
            f'{DISHES_TO_REPAIR}')
    await bot.send_message(text=text,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_start_repair_dish)


async def admin_check_id_dish_value(message: types.Message):
    """Проверка введенного ID блюда на валидность"""
    dish_id = message.text
    response = await get_dish(dish_id)
    try:
        int(dish_id)
    except ValueError:
        await bot.send_message(text=CHECK_ID_ERR,
                               chat_id=message.from_user.id)
        return response['json'], False
    if response['status'] == 404:
        await bot.send_message(text=ID_DISH_404,
                               chat_id=message.from_user.id)
        return response['json'], False
    elif response['status'] == 200:
        return response['json'], True
    else:
        await bot.send_message(text=ID_DISH_OTHER_ERR,
                               chat_id=message.from_user.id)
        return response['json'], False


async def admin_get_formalized_dish(message: types.Message, dish_instance):
    """Стилизованный вывод блюда."""
    dish = dish_instance
    dish_title = dish['title']
    dish_shortname = dish['shortname']
    dish_descr = dish['description']
    dish_image = dish['image']
    dish_filename = f"{BASE_URL}/{dish['filename']}"
    dish_image_id = dish['image_id']
    formalized_dish = (f'<b>Название</b>\n{dish_title}\n'
                       f'<b>Краткое название</b>\n{dish_shortname}\n'
                       f'<b>Описание</b>\n{dish_descr}')
    if dish_image is None:
        formalized_dish += '\n<b>Фото</b>\nБез фото'
        await bot.send_message(text=formalized_dish,
                               chat_id=message.from_user.id)
    else:
        if dish_image_id is None:
            await bot.send_photo(message.from_user.id, dish_filename,
                                 formalized_dish)
        else:
            try:
                await bot.send_photo(message.from_user.id, dish_image_id,
                                     formalized_dish)
            except TelegramBadRequest:
                await bot.send_photo(message.from_user.id,
                                     dish_filename,
                                     formalized_dish)


async def admin_start_repair_dish(message: types.Message, state: FSMContext):
    """Вывод стилизованного меню админу и выбор параметра блюда, который
    нужно изменить."""
    dish_instance, is_correct_digit = await admin_check_id_dish_value(
        message)
    if not is_correct_digit:
        await state.set_state(AdminState.wait_admin_repair_dish)
        return await admin_repair_dish(message, state)
    await state.update_data(dish_instance=dish_instance)
    await bot.send_message(text=START_REPAIR_DISH,
                           chat_id=message.from_user.id)
    await admin_get_formalized_dish(message, dish_instance)
    await bot.send_message(text=START_REPAIR_DISH_2,
                           chat_id=message.from_user.id,
                           reply_markup=admin_start_repair_dish_kb())
    await state.set_state(AdminState.wait_admin_repair_dish_choose_field)


async def admin_repair_dish_choose_field(message: types.Message,
                                         state: FSMContext):
    """Запрос нового значения для выбранного параметра блюда."""
    db_key_to_change = None
    if message.text == 'Название':
        db_key_to_change = 'title'
        await bot.send_message(text=DISH_EDIT_DATA,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
    elif message.text == 'Краткое название':
        db_key_to_change = 'shortname'
        await bot.send_message(text=DISH_EDIT_DATA_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
    elif message.text == 'Описание':
        db_key_to_change = 'description'
        await bot.send_message(text=DISH_EDIT_DATA_3,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
    elif message.text == 'Фотография':
        db_key_to_change = 'image'
        await bot.send_message(text=DISH_EDIT_DATA_4,
                               chat_id=message.from_user.id,
                               reply_markup=admin_add_dish_noimage_kb())
    await state.update_data(db_key_to_change=db_key_to_change)
    await state.set_state(AdminState.wait_admin_repair_dish_fields)


async def admin_repair_dish_fields(message: types.Message, state: FSMContext):
    """Внесение изменений в указанный параметр блюда, его сохранение в базе
    данных."""
    new_dish_data = {}
    data = await state.get_data()
    dish_id = data['dish_instance']['id']
    key = data['db_key_to_change']
    if message.photo:
        mes_img = message.photo[-1]
        file_id = mes_img.file_id
        file = await bot.get_file(file_id)
        filename = mes_img.file_id
        image = (await bot.download_file(file.file_path)).read()
        new_dish_data['image'] = image
        new_dish_data['filename'] = filename
        new_dish_data['image_id'] = file_id
    if message.text:
        if message.text == 'Без фото':
            new_dish_data['image'] = None
            new_dish_data['filename'] = None
            new_dish_data['image_id'] = None
        else:
            new_dish_data[key] = message.text
    response = await edit_dish(new_dish_data, dish_id)
    if response['status'] == 200:
        await bot.send_message(text=DISH_EDIT_SUCCESS,
                               chat_id=message.from_user.id,
                               reply_markup=admin_work_with_dishes_kb())
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)
    else:
        await bot.send_message(text=DISH_EDIT_ERR,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)


# удаление блюда
async def admin_remove_dish(message: types.Message, state: FSMContext):
    """Удаление блюда. Запрос ID блюда для удаления."""
    await bot.send_message(text=DISH_RM_ENTER_ID,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(AdminState.wait_admin_remove_dish_choose)


async def admin_remove_dish_choose(message: types.Message, state: FSMContext):
    """Проверка введенного ID блюда на валидность, вывод админу блюда,
    запрос подтверждения удаления этого блюда."""
    dish_instance, is_correct_digit = await admin_check_id_dish_value(
        message)
    if not is_correct_digit:
        await state.set_state(AdminState.wait_admin_repair_dish)
        return await admin_repair_dish(message, state)
    await state.update_data(dish_id=message.text)
    await admin_get_formalized_dish(message, dish_instance)
    await bot.send_message(text=DISH_RM_ACCEPT,
                           chat_id=message.from_user.id,
                           reply_markup=admin_remove_dish_choose_kb())
    await state.set_state(AdminState.wait_admin_remove_dish_confirm)


async def admin_remove_dish_confirm(message: types.Message, state: FSMContext):
    """Обработка подтверждения / отмены для удаления блюда."""
    if message.text == 'Да, уверен':
        data = await state.get_data()
        dish_id = data['dish_id']
        response = await remove_dish(dish_id)
        if response['status'] == 204:
            text = DISH_RM_CONFIRM
        elif response['status'] == 404:
            text = DISH_RM_CONFIRM_2.format(response)
        else:
            text = DISH_RM_CONFIRM_3.format(response)
        await bot.send_message(text=text,
                               chat_id=message.from_user.id,
                               reply_markup=admin_work_with_dishes_kb())
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)

    elif message.text == 'Отмена!!':
        await bot.send_message(text=DISH_RM_CANCEL,
                               chat_id=message.from_user.id,
                               reply_markup=admin_work_with_dishes_kb())
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)


async def client_get_formalized_dish(dish_instance, client_id):
    """Красивое представление меню для пользователя."""
    dish = dish_instance
    dish_title = dish['title']
    dish_descr = dish['description']
    dish_image = dish['image']
    dish_filename = f"{BASE_URL}/{dish['filename']}"
    dish_image_id = dish['image_id']
    formalized_dish = (f'<b>Блюдо:</b>\n{dish_title}\n'
                       f'<b>Описание: </b>\n{dish_descr}')
    if dish_image is None:
        formalized_dish += '\n<b>Фото</b>\nБез фото'
        await bot.send_message(text=formalized_dish,
                               chat_id=client_id)
    else:
        if dish_image_id is None:
            await bot.send_photo(client_id, dish_filename,
                                 formalized_dish)
        else:
            try:
                await bot.send_photo(client_id, dish_image_id,
                                     formalized_dish)
            except TelegramBadRequest:
                print(dish_filename)
                await bot.send_photo(client_id,
                                     dish_filename,
                                     formalized_dish)
