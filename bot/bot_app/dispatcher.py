from magic_filter import F
from aiogram.types import ContentType
from aiogram.dispatcher.filters.text import Text

from .bot_create import dp, bot
from .handlers.admin.admin_handlers import (enter_admin_section,
                                            admin_main_menu)
from .handlers.admin.dishes_handlers import (admin_work_with_dishes,
                                             admin_choose_dishes,
                                             admin_add_dish_title,
                                             admin_add_dish_shortname,
                                             admin_add_dish_descr,
                                             admin_add_dish_photo,
                                             admin_confirm_add_dish_data,
                                             admin_repair_dish,
                                             admin_start_repair_dish,
                                             admin_repair_dish_choose_field,
                                             admin_repair_dish_fields,
                                             admin_remove_dish,
                                             admin_remove_dish_choose,
                                             admin_remove_dish_confirm)
from .handlers.admin.distrib import admin_choose_main_menu
from .handlers.admin.menus_handlers import (admin_work_with_menus,
                                            admin_work_with_menus_choose,
                                            admin_create_menus_start,
                                            admin_create_menus_validate_date,
                                            admin_create_menus_title,
                                            admin_create_menus_dishes,
                                            admin_create_menus_dishes_check,
                                            admin_create_menus_confirm,
                                            admin_remove_menus,
                                            admin_remove_menu_choose,
                                            admin_remove_menu_confirm,
                                            admin_send_menu,
                                            admin_confirm_choose_send_menu,
                                            admin_send_menu_run)
from .handlers.admin.orders_handlers import (admin_choose_orders,
                                             admin_list_orders,
                                             admin_list_orders_by_date_execute)
from .handlers.common import start_command, stop_command, help_command
from .handlers.registration_handlers import (check_registration,
                                             start_registration,
                                             input_firstname, input_lastname,
                                             input_phone,
                                             confirm_registration)
from .handlers.schedule import on_startup
from .handlers.user_handlers import (enter_client_section, client_if_order,
                                     client_count_of_serv, client_sel_payment,
                                     client_payment_cash,
                                     client_sel_delivery, client_address,
                                     client_check_address, client_comment,
                                     client_check_order, client_handling_rules)
from .states import RegState, UserState, AdminState

dp.message.register(check_registration, text='Начать',
                    state=RegState.wait_check_registration)
# ==================регистрация=========================
dp.message.register(start_registration,
                    text=['Зарегистрироваться', 'Давай исправим'],
                    state=RegState.wait_start_registration)

dp.message.register(input_firstname,
                    ~F.text.startswith('/'),
                    state=RegState.wait_input_firstname)
dp.message.register(input_lastname,
                    ~F.text.startswith('/'),
                    state=RegState.wait_input_lastname)
dp.message.register(input_phone,
                    ~F.text.startswith('/'),
                    state=RegState.wait_input_phone)
dp.message.register(confirm_registration,
                    text=['Да, все верно', 'Есть ошибки'],
                    state=RegState.wait_confirm_registration)
dp.message.register(enter_client_section,
                    text='Начать пользоваться',
                    state=UserState.wait_to_enter_client_section)

# ==================админский доступ=========================
dp.message.register(enter_admin_section,
                    commands='admin')
# ==================работа с блюдами=========================
dp.message.register(admin_main_menu,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_main_menu)
dp.message.register(admin_choose_main_menu,
                    text=['Работа с блюдами', 'Работа с меню',
                          'Работа с заказами'],
                    state=AdminState.wait_admin_choose_main_menu)
dp.message.register(admin_work_with_dishes,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_work_with_dishes)
dp.message.register(admin_choose_dishes,
                    text=['Список блюд', 'Добавить блюдо',
                          'Изменить блюдо', 'Удалить блюдо', 'Главное меню'],
                    state=AdminState.wait_admin_choose_dishes)
dp.message.register(admin_add_dish_title,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_add_dish_title)
dp.message.register(admin_add_dish_shortname,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_add_dish_shortname)
dp.message.register(admin_add_dish_descr,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_add_dish_descr)
# один на фото, другой на текст
dp.message.register(admin_add_dish_photo,
                    content_types=ContentType.PHOTO,
                    state=AdminState.wait_admin_add_dish_photo)
dp.message.register(admin_add_dish_photo,
                    text='Без фото',
                    state=AdminState.wait_admin_add_dish_photo)
dp.message.register(admin_confirm_add_dish_data,
                    text=['Да, все верно', 'Нужно исправить'],
                    state=AdminState.wait_admin_confirm_add_dish_data)
# ==================исправление блюда=========================
dp.message.register(admin_repair_dish,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_repair_dish)
dp.message.register(admin_start_repair_dish,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_start_repair_dish)
dp.message.register(admin_repair_dish_choose_field,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_repair_dish_choose_field)
# один на фото, другой на текст
dp.message.register(admin_repair_dish_fields,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_repair_dish_fields)
dp.message.register(admin_repair_dish_fields,
                    content_types=ContentType.PHOTO,
                    state=AdminState.wait_admin_repair_dish_fields)
# ==================удаление блюда=========================
dp.message.register(admin_remove_dish,
                    text=['Удалить блюдо'],
                    state=AdminState.wait_admin_remove_dish)
dp.message.register(admin_remove_dish_choose,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_remove_dish_choose)
dp.message.register(admin_remove_dish_confirm,
                    text=['Да, уверен', 'Отмена!!'],
                    state=AdminState.wait_admin_remove_dish_confirm)

# ==================Работа с меню=========================
dp.message.register(admin_work_with_menus,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_work_with_menus)
dp.message.register(admin_work_with_menus_choose,
                    text=['Новое меню', 'Удалить меню', 'Созданные меню',
                          'Разослать меню', 'Главное меню'],
                    state=AdminState.wait_admin_work_with_menus_choose)
dp.message.register(admin_create_menus_start,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_create_menus_start)
dp.message.register(admin_create_menus_validate_date,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_create_menus_validate_date)
dp.message.register(admin_create_menus_title,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_create_menus_title)
dp.message.register(admin_create_menus_dishes,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_create_menus_dishes)
dp.message.register(admin_create_menus_dishes_check,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_create_menus_dishes_check)
dp.message.register(admin_create_menus_confirm,
                    text=['Да, все верно', 'Нужно исправить'],
                    state=AdminState.wait_admin_create_menus_confirm)
# ==================удаление меню=========================
dp.message.register(admin_remove_menus,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_remove_menus)
dp.message.register(admin_remove_menu_choose,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_remove_menu_choose)
dp.message.register(admin_remove_menu_confirm, text=['Да, уверен', 'Отмена!!'],
                    state=AdminState.wait_admin_remove_menu_confirm)
# ==================отправка меню=========================
dp.message.register(admin_send_menu,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_send_menu)
dp.message.register(admin_confirm_choose_send_menu,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_confirm_choose_send_menu)
dp.message.register(admin_send_menu_run, text=['Да', 'Нет, отмена!'],
                    state=AdminState.wait_admin_send_menu_run)

# ==================Клиентский раздел=========================
dp.message.register(enter_client_section,
                    text=['Что за правила?'],
                    state=UserState.wait_to_enter_client_section)
dp.message.register(client_handling_rules,
                    text=['Согласен', 'Отказаться'],
                    state=UserState.wait_client_handling_rules)
# ==================Клиентский раздел заказ блюда==============
dp.message.register(client_if_order,
                    text=['Да', 'Нет'],
                    state=UserState.wait_client_if_order)
dp.message.register(client_count_of_serv,
                    ~F.text.startswith('/'),
                    state=UserState.wait_client_count_of_serv)
dp.message.register(client_sel_payment,
                    text=['Оплата по карте', 'Оплата наличными'],
                    state=UserState.wait_client_sel_payment)
dp.message.register(client_payment_cash,
                    state=UserState.wait_client_payment_cash)
dp.message.register(client_sel_delivery,
                    text=['Самовывоз', 'Доставка'],
                    state=UserState.wait_client_sel_delivery)
dp.message.register(client_address,
                    ~F.text.startswith('/'),
                    state=UserState.wait_client_address)
dp.message.register(client_check_address,
                    text=['Да', 'Нет'],
                    state=UserState.wait_client_check_address)
dp.message.register(client_comment,
                    ~F.text.startswith('/'),
                    state=UserState.wait_client_comment)
dp.message.register(client_check_order,
                    text=['Да, все верно', 'Нет, исправить'],
                    state=UserState.wait_client_check_order)
# ==================Управление заказами=========================
dp.message.register(admin_choose_orders,
                    text=['Список заказов', 'Главное меню'],
                    state=AdminState.wait_admin_choose_orders)
dp.message.register(admin_list_orders,
                    text=['На сегодня', 'На завтра',
                          'На дату', 'Главное меню'],
                    state=AdminState.wait_admin_list_orders)
dp.message.register(admin_list_orders_by_date_execute,
                    ~F.text.startswith('/'),
                    state=AdminState.wait_admin_list_orders_by_date_execute)

dp.message.register(start_command, commands='start', state='*')
dp.message.register(stop_command, commands='stop', state='*')
dp.message.register(help_command, commands='help', state='*')

dp.startup.register(on_startup)


def run_pooling():
    """ Запускает бота """
    dp.run_polling(bot, skip_updates=True)