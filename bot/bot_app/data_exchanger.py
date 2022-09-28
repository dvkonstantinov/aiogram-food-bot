import json
import os

import aiohttp
from aiohttp import FormData, connector
from dotenv import load_dotenv

from bot_app.bot_create import bot

load_dotenv()

USERS_URL = os.getenv('USERS_URL')
DISHES_URL = os.getenv('DISHES_URL')
MENUS_URL = os.getenv('MENUS_URL')
ADMIN_IDS = [os.getenv('ADMIN_IDS')]
ORDERS_URL = os.getenv('ORDERS_URL')


async def send_error_to_admin(exception):
    for admin in ADMIN_IDS:
        text = (f'Возникла ошибка при отправке запроса  на сервер.\n'
                f' {exception}')
        await bot.send_message(text=text,
                               chat_id=admin)


async def list_users():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(USERS_URL) as response:
                return await response.json()
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def get_user_info(user_id):
    url = USERS_URL + str(user_id) + '/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def add_user(user_data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(USERS_URL, json=user_data) as response:
                return {
                    'response': response,
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def user_registration(user_id, user_data):
    url = USERS_URL + user_id + '/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=user_data) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def list_dishes():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DISHES_URL) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def get_dish(dish_id):
    url = DISHES_URL + str(dish_id) + '/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def add_dish(dish_data):
    try:
        async with aiohttp.ClientSession() as session:
            if dish_data['image'] is not None:
                form = FormData()
                for key, value in dish_data.items():
                    form.add_field(key, value)
                form.add_field('image', dish_data['image'],
                               filename=str(dish_data['filename']) + '.jpg')
                async with session.post(DISHES_URL,
                                        data=form) as response:
                    return {
                        'status': response.status,
                        'json': await response.json()
                    }
            else:
                json_data = json.loads(json.dumps(dish_data))
                async with session.post(DISHES_URL,
                                        json=json_data) as response:
                    return {
                        'status': response.status,
                        'json': await response.json()
                    }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def edit_dish(dish_data, dish_id):
    url = DISHES_URL + str(dish_id) + '/'
    try:
        async with aiohttp.ClientSession() as session:
            if 'image' in dish_data.keys() and dish_data['image'] is not None:
                form = FormData()
                for key, value in dish_data.items():
                    form.add_field(key, value)
                form.add_field('image', dish_data['image'],
                               filename=str(dish_data['filename']) + '.jpg')
                async with session.patch(url, data=form) as response:
                    return {
                        'status': response.status,
                        'json': await response.json()
                    }
            else:
                json_data = json.loads(json.dumps(dish_data))
                async with session.patch(url, json=json_data) as response:
                    return {
                        'status': response.status,
                        'json': await response.json()
                    }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def remove_dish(dish_id):
    url = DISHES_URL + str(dish_id) + '/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                return {
                    'status': response.status
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def get_menu(menu_id):
    url = MENUS_URL + str(menu_id) + '/'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def list_menus():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(MENUS_URL) as response:
                return await response.json()
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def add_new_menu(menu_data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(MENUS_URL, json=menu_data) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def remove_menu(menu_id):
    try:
        url = MENUS_URL + str(menu_id) + '/'
        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                return {
                    'status': response.status
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def add_order(data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(ORDERS_URL, json=data) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)


async def list_orders(date):
    try:
        url = f'{ORDERS_URL}?date={date}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return {
                    'status': response.status,
                    'json': await response.json()
                }
    except connector.ClientConnectorError as e:
        await send_error_to_admin(e)
