import os

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.dispatcher.webhook.aiohttp_server import (SimpleRequestHandler,
                                                       setup_application)
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
REDIS_DSN = os.getenv('REDIS_DSN')

BASE_URL = os.getenv('BASE_URL')
WEB_SERVER_HOST = os.getenv('WEB_SERVER_HOST')
WEB_SERVER_PORT = os.getenv('WEB_SERVER_PORT')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'
IS_REDIS_STORAGE = os.getenv('IS_REDIS_STORAGE')

session = AiohttpSession()
bot_settings = {
    "session": session,
    "parse_mode": "HTML"
}
bot = Bot(token=TELEGRAM_TOKEN, **bot_settings)

if IS_REDIS_STORAGE.lower() in ['true', '1', 'yes']:
    storage = RedisStorage.from_url(REDIS_DSN)
else:
    storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def start_webhook():
    """ Запускает бота в режиме webhook"""
    app = web.Application()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
