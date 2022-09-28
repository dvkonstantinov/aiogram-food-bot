import logging
import os

from dotenv import load_dotenv

from bot_app.bot_create import start_webhook
from bot_app.dispatcher import run_pooling

load_dotenv()
IS_WEBHOOK = os.getenv('IS_WEBHOOK')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    if IS_WEBHOOK.lower() in ['true', '1', 'yes']:
        start_webhook()
    else:
        run_pooling()
