from django.contrib import admin

from .models import User, Menu, Dishes, Orders


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id',
                    'username',
                    'input_firstname',
                    'input_lastname',
                    'input_phone',
                    'is_register',
                    'is_blocked_bot',
                    'is_allow_mail']
    list_display_links = ['user_id', 'username']


class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_of_menu']
    list_display_links = ['id', 'title']


class DishesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'shortname', 'description', 'image_tag']
    list_display_links = ['id', 'title', 'shortname']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'id_of_menu',
                    'menu_title',
                    'menu_date',
                    'id_of_user',
                    'created_at']

    def menu_title(self, obj):
        return obj.menu.title

    def id_of_menu(self, obj):
        return obj.menu.pk

    def menu_date(self, obj):
        return obj.menu.date_of_menu

    def id_of_user(self, obj):
        return obj.user.pk

    id_of_menu.short_description = 'ID меню'
    id_of_user.short_description = 'ID клиента'
    menu_date.short_description = 'Дата меню'
    menu_title.short_description = 'Название меню'


admin.site.register(User, UserAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Dishes, DishesAdmin)
admin.site.register(Orders, OrdersAdmin)
