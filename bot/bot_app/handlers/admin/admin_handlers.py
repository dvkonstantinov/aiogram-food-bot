# ==================админский доступ=========================
from datetime import date, timedelta

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.bot_create import bot
from bot_app.data_exchanger import get_user_info, list_menus
from bot_app.keyboards.admin_kb import admin_main_menu_kb
from bot_app.phrases.admin_phrases import ADM_ENTER_ERR, ADM_MENU
from bot_app.states import AdminState


async def enter_admin_section(message: types.Message, state: FSMContext):
    """Вход в раздел админа."""
    user_id = message.from_user.id
    response = await get_user_info(user_id)
    if not response['json']['is_admin']:
        await bot.send_message(text=ADM_ENTER_ERR,
                               chat_id=message.from_user.id)
    else:
        await state.set_state(AdminState.wait_admin_check_today_menu)
        return await admin_check_today_menu(message, state)


async def admin_check_today_menu(message: types.Message, state: FSMContext):
    """Проверка на заполненность меню на завтра. Происходит каждый раз при
    входе в раздел админа."""
    menus = await list_menus()
    tomorrow = date.today() + timedelta(days=1)
    text = 'Произвожу проверку наполненности меню на завтра...'
    if not any(menu['date_of_menu'] == tomorrow for menu in menus):
        text += '\nМеню на завтра НЕ ЗАПОЛНЕНО!!!'
    else:
        text += '\nВы уже наполнили меню на завтра, все ОК'
    await bot.send_message(text=text,
                           chat_id=message.from_user.id)
    await state.set_state(AdminState.wait_admin_main_menu)
    return await admin_main_menu(message, state)


async def admin_main_menu(message: types.Message, state: FSMContext):
    """Главное меню администратора."""
    await bot.send_message(text=ADM_MENU,
                           chat_id=message.from_user.id,
                           reply_markup=admin_main_menu_kb())
    await state.set_state(AdminState.wait_admin_choose_main_menu)



