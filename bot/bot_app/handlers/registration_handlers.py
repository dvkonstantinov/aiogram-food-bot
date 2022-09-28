import json

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.bot_create import bot
from bot_app.data_exchanger import get_user_info, user_registration
from bot_app.handlers.user_handlers import client_msg_before_start
from bot_app.handlers.utils import (validate_phone, get_data_to_validate,
                                    validate_name)
from bot_app.keyboards.common_kb import (start_using, reg_kb, remove_kb,
                                         ready_repair_reg_kb,
                                         confirm_reg_kb)
from bot_app.phrases.user_phrases import (CHECK_REG_1, CHECK_REG_2,
                                          START_REG_1,
                                          START_REG_2, INPUT_NAME_1,
                                          INPUT_NAME_2, INPUT_LASTNAME_1,
                                          INPUT_LASTNAME_2, INPUT_PHONE_1,
                                          INPUT_PHONE_2, CONFIRM_REG_1,
                                          CONFIRM_REG_ERR, CONFIRM_REG_2)
from bot_app.states import UserState, RegState


async def check_registration(message: types.Message, state: FSMContext):
    """Проверка на регистрацию."""
    user_id = message.from_user.id
    response = await get_user_info(user_id)
    if response['json']['is_register'] and response['json']['is_allow_mail']:
        await state.set_state(UserState.wait_to_waiting_order_info)
        return await client_msg_before_start(message)
    elif (response['json']['is_register']
          and not response['json']['is_allow_mail']):
        await bot.send_message(text=CHECK_REG_1,
                               chat_id=message.from_user.id,
                               reply_markup=start_using())
        await state.set_state(UserState.wait_to_enter_client_section)
    else:
        await bot.send_message(text=CHECK_REG_2,
                               chat_id=message.from_user.id,
                               reply_markup=reg_kb())
        await state.set_state(RegState.wait_start_registration)


async def start_registration(message: types.Message, state: FSMContext):
    """Начало регистрации."""
    await bot.send_message(text=START_REG_1,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await bot.send_message(text=START_REG_2,
                           chat_id=message.from_user.id)
    await state.set_state(RegState.wait_input_firstname)


async def input_firstname(message: types.Message, state: FSMContext):
    """Ввод имени."""
    name = validate_name(message)
    if not name:
        await bot.send_message(text=INPUT_NAME_1,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        return await get_data_to_validate(state)
    await state.update_data(input_firstname=name)
    await bot.send_message(text=INPUT_NAME_2,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(RegState.wait_input_lastname)


async def input_lastname(message: types.Message, state: FSMContext):
    """Ввод фамилии."""
    surname = validate_name(message)
    if not surname:
        await bot.send_message(text=INPUT_LASTNAME_1,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        return await get_data_to_validate(state)
    await state.update_data(input_lastname=surname)
    await bot.send_message(text=INPUT_LASTNAME_2,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.set_state(RegState.wait_input_phone)


async def input_phone(message: types.Message, state: FSMContext):
    """Ввод номера телефона."""
    phone = validate_phone(message)
    if not phone:
        await bot.send_message(text=INPUT_PHONE_1,
                               chat_id=message.from_user.id,
                               reply_markup=remove_kb())
        return await get_data_to_validate(state)
    await state.update_data(input_phone=phone)
    data = await state.get_data()
    text = (f'{INPUT_PHONE_2}\n'
            f'Имя: {data["input_firstname"]}\n'
            f'Фамилия: {data["input_lastname"]}\n'
            f'Телефон: {data["input_phone"]}\n')
    await bot.send_message(text=text,
                           chat_id=message.from_user.id,
                           reply_markup=confirm_reg_kb())
    await state.set_state(RegState.wait_confirm_registration)


async def confirm_registration(message: types.Message, state: FSMContext):
    """Подтверждение регистрации."""
    if message.text == 'Да, все верно':
        data = await state.get_data()
        user_id = str(message.from_user.id)
        user_data = {
            'input_firstname': data["input_firstname"],
            'input_lastname': data["input_lastname"],
            'input_phone': data["input_phone"],
            'is_register': True,
        }
        json_data = json.loads(json.dumps(user_data))
        response = await user_registration(user_id, json_data)
        data.clear()
        if response['status'] == 200:
            await bot.send_message(text=CONFIRM_REG_1,
                                   chat_id=message.from_user.id,
                                   reply_markup=start_using())
            await state.set_state(UserState.wait_to_enter_client_section)
        else:
            await bot.send_message(text=CONFIRM_REG_ERR,
                                   chat_id=message.from_user.id)
            await bot.send_message(text=str(json_data),
                                   chat_id=message.from_user.id)
    if message.text == 'Есть ошибки':
        await bot.send_message(text=CONFIRM_REG_2,
                               chat_id=message.from_user.id,
                               reply_markup=ready_repair_reg_kb())
        await state.set_state(RegState.wait_start_registration)
