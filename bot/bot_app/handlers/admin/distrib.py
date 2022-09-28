from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot_app.handlers.admin.dishes_handlers import admin_work_with_dishes
from bot_app.handlers.admin.menus_handlers import admin_work_with_menus
from bot_app.handlers.admin.orders_handlers import admin_work_with_orders
from bot_app.states import AdminState


async def admin_choose_main_menu(message: types.Message, state: FSMContext):
    """Главное меню администратора. Распределение по разделам."""
    if message.text == 'Работа с меню':
        await state.set_state(AdminState.wait_admin_work_with_menus)
        return await admin_work_with_menus(message, state)
    elif message.text == 'Работа с блюдами':
        await state.set_state(AdminState.wait_admin_work_with_dishes)
        return await admin_work_with_dishes(message, state)
    elif message.text == 'Работа с заказами':
        await state.set_state(AdminState.wait_admin_work_with_orders)
        return await admin_work_with_orders(message, state)
