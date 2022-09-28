import asyncio
import os
from datetime import date, timedelta

import aioschedule
from aiogram import types
from dotenv import load_dotenv

from bot_app.bot_create import bot, WEBHOOK_URL
from bot_app.data_exchanger import list_menus, list_users
from bot_app.phrases.common_phrases import EVERYDAY_CHECK_TEXT

load_dotenv()
IS_WEBHOOK = os.getenv('IS_WEBHOOK')


async def admin_check_everyday_tomorrow_menu():
    """Расписание. Ежедневное напоминание"""
    menus = await list_menus()
    tomorrow = date.today() + timedelta(days=1)
    all_users = await list_users()
    admins = []
    ([admins.append(user['user_id']) for user in all_users if user[
        'is_admin'] is True])
    if not any(menu['date_of_menu'] == str(tomorrow) for menu in menus):
        for admin in admins:
            await bot.send_message(text=EVERYDAY_CHECK_TEXT,
                                   chat_id=admin)
            await asyncio.sleep(1)


async def reminder():
    """Напоминалка установить меню на завтра"""
    await admin_check_everyday_tomorrow_menu()
    aioschedule.every().day.at("15:00").do(admin_check_everyday_tomorrow_menu)
    # aioschedule.every(10).seconds.do(admin_check_everyday_tomorrow_menu)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


async def on_startup() -> None:
    """Действия, которые нужно выполнить до старта бота"""

    await bot.delete_webhook()
    if IS_WEBHOOK.lower() in ['true', '1', 'yes']:
        await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(reminder())
    await bot.delete_my_commands()
    bot_commands = {
        'start': 'Запустить бота 🚀',
        'help': 'Помощь ℹ️',
        'admin': 'Админка 👥️',
        'stop': 'Остановить бота',
    }
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command=command, description=description)
            for command, description in bot_commands.items()
        ]
    )
