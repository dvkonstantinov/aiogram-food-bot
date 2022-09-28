import json

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.bot_create import bot
from bot_app.data_exchanger import add_user
from bot_app.keyboards.common_kb import start_kb, remove_kb
from bot_app.phrases.common_phrases import (START_TEXT_201, START_TEXT_400,
                                            STOP_TEXT, HELP_TEXT)
from bot_app.states import RegState


async def start_command(message: types.Message, state: FSMContext):
    """Команда старт."""
    user_id = message.from_user.id
    user_data = {
        'user_id': user_id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
    }
    json_data = json.loads(json.dumps(user_data))
    response = await add_user(json_data)
    print(response)
    if response['status'] == 201:
        await bot.send_message(text=START_TEXT_201,
                               chat_id=message.from_user.id,
                               reply_markup=start_kb())
    elif response['status'] == 400:
        await bot.send_message(text=START_TEXT_400,
                               chat_id=message.from_user.id,
                               reply_markup=start_kb())
    await state.set_state(RegState.wait_check_registration)


async def stop_command(message: types.Message, state: FSMContext):
    """Команда стоп."""
    await bot.send_message(text=STOP_TEXT,
                           chat_id=message.from_user.id,
                           reply_markup=remove_kb())
    await state.clear()


async def help_command(message: types.Message):
    """Команда помощи."""
    await bot.send_message(text=HELP_TEXT,
                           chat_id=message.from_user.id)
