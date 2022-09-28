# ======================раздел пользователя======================
import json
import re

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.bot_create import bot
from bot_app.data_exchanger import add_order, user_registration
from bot_app.handlers.utils import check_case_serving
from bot_app.keyboards.common_kb import remove_kb
from bot_app.keyboards.user_kb import (enter_client_section_kb,
                                       client_sel_payment_kb,
                                       client_sel_delivery_kb,
                                       client_comment_kb,
                                       client_yes_no_kb,
                                       client_check_order_kb,
                                       client_try_again)
from bot_app.phrases.user_phrases import (ENTER_CLIENT_1, ENTER_CLIENT_2,
                                          CLIENT_ACCEPT, CLIENT_START_MSG,
                                          CL_CANCEL, CL_START_ORDER, CL_COUNT,
                                          CL_COUNT_2, CL_VALIDATE_COUNT,
                                          CL_PAYMENT, CL_PAYMENT_2,
                                          CL_PAYMENT_CACHE_2, CL_PAYMENT_CACHE,
                                          CL_DELIVERY, CL_DELIVERY_2,
                                          CL_ADDRESS, CL_CHECK_ADDRESS,
                                          CL_CHECK_ADDRESS_2, CL_ORDER,
                                          CL_ORDER_ERR)
from bot_app.states import UserState


async def enter_client_section(message: types.Message, state: FSMContext):
    """Приветствие в клиентском разделе, правила."""
    await bot.send_message(text=ENTER_CLIENT_1,
                           chat_id=message.from_user.id)
    await bot.send_message(text=ENTER_CLIENT_2,
                           chat_id=message.from_user.id,
                           reply_markup=enter_client_section_kb())
    await state.set_state(UserState.wait_client_handling_rules)


async def client_handling_rules(message: types.Message, state: FSMContext):
    if message.text == 'Согласен':
        user_data = {
            'is_allow_mail': True,
        }
        json_data = json.loads(json.dumps(user_data))
        await user_registration(str(message.from_user.id), json_data)
        await state.set_state(UserState.wait_to_waiting_order_info)
        return await client_msg_before_start(message)

    elif message.text == 'Отказаться':
        await state.clear()
        await bot.send_message(text=CLIENT_ACCEPT,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())


async def client_msg_before_start(message: types.Message):
    await bot.send_message(text=CLIENT_START_MSG,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())


# Пользовательская часть, создание заказа==================================
async def client_if_order(message: types.Message, state: FSMContext):
    """Получение ответа от клиента, будет ли он заказывать еду на завтра."""
    if message.text == 'Да':
        data = await state.get_data()
        for item in data:
            if item != 'menu':
                data[item] = None
        await state.set_state(UserState.wait_client_start_order)
        return await client_start_order(message, state)
    if message.text == 'Нет':
        await state.set_state(UserState.wait_client_cancel_order)
        return await client_cancel_order(message, state)


async def client_cancel_order(message: types.Message, state: FSMContext):
    """Обработка отказа от заказа на завтра."""
    await bot.send_message(text=CL_CANCEL,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(UserState.wait_to_waiting_order_info)


async def client_start_order(message: types.Message, state: FSMContext):
    """В случае согласия на заказ, запрос сколько порций блюд нужно."""
    await bot.send_message(text=CL_START_ORDER,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(UserState.wait_client_count_of_serv)


async def client_count_of_serv(message: types.Message, state: FSMContext):
    """Обработка количества порций, запрос по типу оплаты (карта/нал)."""
    count = await check_count_of_servings(message, state)
    if int(count) > 100:
        await bot.send_message(text=CL_COUNT,
                               chat_id=message.from_user.id)
        await state.set_state(UserState.wait_client_start_order)
        return await client_start_order(message, state)
    else:
        mes_count = check_case_serving(count)
        await state.update_data(count=count, mes_count=mes_count)
        await bot.send_message(text=CL_COUNT_2.format(count, mes_count),
                               chat_id=message.from_user.id,
                               reply_markup=client_sel_payment_kb())
        await state.set_state(UserState.wait_client_sel_payment)


async def check_count_of_servings(message: types.Message, state: FSMContext):
    """Валидация количества порций."""
    count = message.text
    pattern = re.compile(r'^[1-9]\d*$')
    if not re.match(pattern, count):
        await bot.send_message(text=CL_VALIDATE_COUNT,
                               chat_id=message.from_user.id)
        await state.set_state(UserState.wait_client_start_order)
        return await client_start_order(message, state)
    else:
        return int(count)


async def client_sel_payment(message: types.Message, state: FSMContext):
    """Обработка выбора между оплатой по карте и наличными."""
    if message.text == 'Оплата по карте':
        await state.update_data(cash_change=None)
        await bot.send_message(text=CL_PAYMENT,
                               chat_id=message.from_user.id,
                               reply_markup=client_sel_delivery_kb())
        await state.set_state(UserState.wait_client_sel_delivery)
    elif message.text == 'Оплата наличными':
        await bot.send_message(text=CL_PAYMENT_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(UserState.wait_client_payment_cash)
    await state.update_data(payment=message.text)


async def client_payment_cash(message: types.Message, state: FSMContext):
    """Валидация введенной суммы в рублях, в случае наличной оплаты. Запрос
    типа получения (доставка/самомвывоз)."""
    change = message.text
    pattern = re.compile(r'^[1-9]\d*$')
    if not re.match(pattern, change):
        await bot.send_message(text=CL_PAYMENT_CACHE,
                               chat_id=message.from_user.id)
        await state.set_state(UserState.wait_client_payment_cash)
    else:
        await state.update_data(cash_change=change)
        await bot.send_message(text=CL_PAYMENT_CACHE_2.format(change),
                               chat_id=message.from_user.id,
                               reply_markup=client_sel_delivery_kb())
        await state.set_state(UserState.wait_client_sel_delivery)


async def client_sel_delivery(message: types.Message, state: FSMContext):
    """Обработка ответа по типу получения. Если доставка - то запрос адреса
    доставки."""
    if message.text == 'Самовывоз':
        await state.update_data(delivery_address=None)

        await bot.send_message(text=CL_DELIVERY.format(message.text),
                               chat_id=message.from_user.id,
                               reply_markup=client_comment_kb())
        await state.set_state(UserState.wait_client_comment)
    elif message.text == 'Доставка':
        await bot.send_message(text=CL_DELIVERY_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(UserState.wait_client_address)
    await state.update_data(delivery=message.text)


async def client_address(message: types.Message, state: FSMContext):
    """Проверка адреса доставки."""
    address = message.text

    await state.update_data(delivery_address=address)
    await bot.send_message(text=CL_ADDRESS.format(address),
                           chat_id=message.from_user.id,
                           reply_markup=client_yes_no_kb())
    await state.set_state(UserState.wait_client_check_address)


async def client_check_address(message: types.Message, state: FSMContext):
    """Обработка адреса, запрос комментария к заказу."""
    if message.text == 'Да':
        data = await state.get_data()
        address = data['delivery_address']
        await bot.send_message(
            text=CL_CHECK_ADDRESS.format(data["delivery"], address),
            chat_id=message.from_user.id,
            reply_markup=client_comment_kb())
        await state.set_state(UserState.wait_client_comment)
    elif message.text == 'Нет':
        await bot.send_message(text=CL_CHECK_ADDRESS_2,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        await state.set_state(UserState.wait_client_address)


async def client_comment(message: types.Message, state: FSMContext):
    """ОБработка комментария, проверка пользователем всех введенных данных."""
    if message.text == 'Пропустить':
        await state.update_data(comment=None)
    else:
        await state.update_data(comment=message.text)
    data = await state.get_data()
    text = (f'Теперь давайте еще раз все проверим.\n'
            f'Меню: {data["menu"]["title"]}\n'
            f'Количество порций: {data["count"]} {data["mes_count"]}\n'
            f'Способ оплаты: {data["payment"]}\n')
    if data["cash_change"] == 'Оплата наличными':
        text += f'Сдача: с {data["cash_change"]} рублей\n'
    if data["delivery"] == 'Самовывоз':
        text += f'Способ получения: {data["delivery"]}\n'
        text += f'Адрес получения: АДРЕС\n'
    else:
        text += f'Способ получения: {data["delivery"]}\n'
        text += f'Адрес доставки: {data["delivery_address"]}\n'
    if data["comment"] is not None:
        text += f'Комментарий: {data["comment"]}\n'
    await bot.send_message(text=text,
                           chat_id=message.from_user.id,
                           reply_markup=client_check_order_kb())
    await state.set_state(UserState.wait_client_check_order)


async def client_check_order(message: types.Message, state: FSMContext):
    """Сохранение заказа в базе данных, если все данные верны. Вовзрат к
    началу в противном случае."""
    if message.text == 'Да, все верно':
        data = await state.get_data()
        order_data = {
            'user_id': message.from_user.id,
            'menu_id': data['menu']['id'],
            'num_of_servings': data['count'],
            'payment_type': data['payment'],
            'cash_change': data['cash_change'],
            'delivery': data['delivery'],
            'delivery_address': data['delivery_address'],
            'comment': data['comment']
        }
        response = await add_order(order_data)
        if response['status'] == 201:
            order_id = response['json']['id']
            data.clear()
            await bot.send_message(text=CL_ORDER.format(order_id),
                                   chat_id=message.from_user.id,
                                   reply_markup=remove_kb())
            await state.set_state(UserState.wait_to_waiting_order_info)
        else:
            await bot.send_message(text=CL_ORDER_ERR,
                                   chat_id=message.from_user.id,
                                   reply_markup=client_try_again())
            await state.set_state(UserState.wait_client_if_order)
    elif message.text == 'Нет, исправить':
        await state.set_state(UserState.wait_client_start_order)
        return await client_start_order(message, state)


async def client_fail_order(message: types.Message, state: FSMContext):
    """Сообщение клиенту в случае неудачного создания заказа в базе данных."""
    if message.text == 'Попробовать снова':
        await state.set_state(UserState.wait_client_start_order)
        return await client_start_order(message, state)
