from aiogram.dispatcher.filters.state import State, StatesGroup


class CommonState(StatesGroup):
    wait_validate = State()


class RegState(StatesGroup):
    wait_check_registration = State()
    wait_start_registration = State()
    wait_input_firstname = State()
    wait_input_lastname = State()
    wait_input_phone = State()
    wait_confirm_registration = State()


class UserState(StatesGroup):
    wait_to_enter_client_section = State()
    wait_client_handling_rules = State()
    wait_to_waiting_order_info = State()
    # Заказ
    wait_client_if_order = State()
    wait_client_start_order = State()
    wait_client_cancel_order = State()
    wait_client_count_of_serv = State()
    wait_client_sel_payment = State()
    wait_client_payment_cash = State()
    wait_client_sel_delivery = State()
    wait_client_address = State()
    wait_client_check_address = State()
    wait_client_comment = State()
    wait_client_check_order = State()
    wait_client_save_order = State()
    wait_client_fail_order = State()


class AdminState(StatesGroup):
    wait_admin_check_today_menu = State()
    wait_admin_main_menu = State()
    wait_admin_choose_main_menu = State()
    # Работа с заказами
    wait_admin_work_with_orders = State()
    wait_admin_choose_orders = State()
    wait_admin_list_orders = State()
    wait_admin_list_orders_by_date = State()
    wait_admin_list_orders_by_date_execute = State()
    # Работа с блюлами
    wait_admin_work_with_dishes = State()
    # Добавление нового блюда
    wait_admin_choose_dishes = State()
    wait_admin_add_dish_title = State()
    wait_admin_add_dish_shortname = State()
    wait_admin_add_dish_descr = State()
    wait_admin_add_dish_photo = State()
    wait_admin_confirm_add_dish_data = State()
    # Исправление блюда
    wait_admin_check_id_dish_value = State()
    wait_admin_repair_dish = State()
    wait_admin_start_repair_dish = State()
    wait_admin_repair_dish_choose_field = State()
    wait_admin_repair_dish_fields = State()
    # Удаление блюда
    wait_admin_remove_dish = State()
    wait_admin_remove_dish_choose = State()
    wait_admin_remove_dish_confirm = State()
    # Работа с ежедневными меню
    wait_admin_work_with_menus = State()
    wait_admin_work_with_menus_choose = State()
    wait_admin_list_menus = State()
    wait_admin_create_menus_start = State()
    wait_admin_create_menus_validate_date = State()
    wait_admin_create_menus_title = State()
    wait_admin_create_menus_dishes = State()
    wait_admin_create_menus_dishes_check = State()
    wait_admin_create_menus_confirm = State()
    wait_admin_remove_menus = State()
    wait_admin_remove_menu_choose = State()
    wait_admin_remove_menu_confirm = State()
    wait_admin_send_menu = State()
    wait_admin_confirm_choose_send_menu = State()
    wait_admin_send_menu_run = State()





