from django.db import models

# RECEIVING_CHOICES = (
#     ('delivery', 'Доставка по адресу'),
#     ('pickup', 'Самовывоз'),
# )
from django.utils.safestring import mark_safe


class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True,
                                          verbose_name='Telegram ID')
    username = models.CharField(max_length=100, null=True, blank=True,
                                verbose_name='Username')
    input_firstname = models.CharField(max_length=256, null=True,
                                       blank=True, verbose_name='Имя')
    input_lastname = models.CharField(max_length=256, null=True, blank=True,
                                      verbose_name='Фамилия')
    input_phone = models.CharField(max_length=32, null=True, blank=True,
                                   verbose_name='Телефон')
    first_name = models.CharField(max_length=256, null=True, blank=True,
                                  verbose_name='Имя Tg')
    last_name = models.CharField(max_length=256, null=True, blank=True,
                                 verbose_name='Фамилия Tg')
    is_register = models.BooleanField(default=False,
                                      verbose_name='Зарегистрирован ли')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлен')
    is_blocked_bot = models.BooleanField(default=False,
                                         verbose_name='Заблокирвал бота')
    is_admin = models.BooleanField(default=False,
                                   verbose_name='Права админа')
    is_allow_mail = models.BooleanField(default=False,
                                        verbose_name='Разрешена ли рассылка')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return (f'@{self.username}' if self.username is not None
                else f'{self.user_id}')


class Dishes(models.Model):
    title = models.CharField(max_length=300,
                             verbose_name='Название')
    shortname = models.CharField(max_length=50,
                                 verbose_name='Краткое название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/dishes/',
                              blank=True,
                              null=True,
                              verbose_name='Фото')
    filename = models.CharField(max_length=300, verbose_name='Путь к файлу',
                                blank=True, null=True)
    image_id = models.CharField(max_length=300, blank=True, null=True,
                                verbose_name='ID фото в TG')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлено')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(
                f'<div width="100%" padding="10px">'
                f'<img style="height: 150px; width: 250px; object-fit: '
                f'cover; object-position: center" src="/media'
                f'/{self.image}"></div>')
        else:
            return 'Нет фотографии'

    image_tag.short_description = 'Фото'


class Menu(models.Model):
    title = models.CharField(max_length=300,
                             verbose_name='Название')
    dishes = models.ManyToManyField(Dishes,
                                    verbose_name='Блюда')
    date_of_menu = models.DateField(blank=True,
                                    verbose_name='Дата меню')
    created_at = models.DateTimeField(auto_now_add=True,
                                      db_index=True,
                                      verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлено')

    class Meta:
        ordering = ['date_of_menu']
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class Orders(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='orders',
                             verbose_name='Пользователь')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True,
                             related_name='orders',
                             verbose_name='Меню')
    num_of_servings = models.PositiveIntegerField(verbose_name='Количество '
                                                               'порций')
    payment_type = models.CharField(max_length=30,
                                    verbose_name='Тип оплаты')
    cash_change = models.PositiveIntegerField(blank=True, null=True,
                                              verbose_name='Сдача с')
    delivery = models.CharField(max_length=30,
                                verbose_name='Тип получения')
    delivery_address = models.CharField(max_length=300, blank=True, null=True,
                                        verbose_name='Адрес получения')
    comment = models.CharField(max_length=400, blank=True, null=True,
                               verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Обновлен')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №' + str(self.pk)
