# Django Aiogram Telegram Bot - бот по доставке готовых обедов

Телеграм бот для упрощения процесса по сбору заявок на самомывоз и доставку готовых обедов.

## Описание проекта

Бот работает по умолчанию в режиме webhook. Сменить режим на polling 
возможно, прописав переменные в .env файлах. Для режима webhook телеграм 
требует свой домен с выпущенным ssl сертификатом (подробнее расписано на 
https://core.telegram.org/bots/webhooks).

Данный проект является проверкой полученных знаний и писался во время 
прохождения Яндекс Практикума, в то же время создавался для решения 
конкретной задачи и был внедрен в бизнес-процессы реальной компании. 
Возможно содержит ошибки в логике программы и исполняемом коде.

## Технологический стек
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django rest framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Gunicorn](https://gunicorn.org/)
- [Nginx](https://www.nginx.com/)
- [Ubuntu](https://ubuntu.com/)
- [Aiogram 3](https://docs.aiogram.dev/en/dev-3.x/)
- [Redis](https://redis.io/)
- [Postgresql](https://www.postgresql.org/)


## Реализованные функции
- Регистрация пользователя через telegram с добавлением в БД
- База для хранения данных django - postgresql, для хранения состояний 
  aiogram - redis
- Администрирование через telegram или админку django
- примерная логика работы бота и схема БД тут (xmind): https://disk.yandex.ru/d/f0JdQp4kFanXIQ

### Администрирование
- Добавление блюд (Название, описание, фото/без фото)
- Составление меню на определенный день (добавление блюд в меню)
- Удаление/исправление блюд и меню
- Рассылка меню на конкретную дату пользователям
- Выгрузка списка заказов на выборанную дату в csv-файле
- Ежедневное напоминание о заполнении меню

### Клиентская часть
- Регистрация (имя, фамилия, телефон)
- Форма заказа (количество порций, доставка/самовывоз, форма оплаты и т.д.)
- Возможность согласиться, отказаться от заказа на конкретную дату

  
## Разворачивание образа на личном или vps сервере

## Настройка Nignx

Предполагается, что есть готовый настроенный vps сервер с установленным 
docker, docker-compose и nginx.

1. Перейти в каталог sites-available
```sh
cd /etc/nginx/sites-available/
```
2. Создать файл с именем вашего домена
```sh
nano example.com
```
3. Внутри написать
```sh
server {
    listen 80;

    server_name example.com;

    location /static/ {
      # Абсолютный до каталога с  django_files
        root /var/www/aiogram-food-bot/django_files/;
    }

    location /media/ {
      # Абсолютный до каталога с  django_files
        root /var/www/aiogram-food-bot/django_files/;
    }

    location /api/ {
        allow 127.0.0.1;
        deny all;
    }

    location /webhook/main/ {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:7771;
    }

	location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }

}
```
4. Создать ярлык в каталоге sites-enabled
```sh
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
```
5. Проверить что нет ошибок в конфигурации nginx
```sh
sudo nginx -t
```
6. Перезапустить службу nginx
```sh
sudo systemctl restart nginx
```
7. Установить https соединение, выпустив ssl сертификат с помощью certbot для вашего домена
```sh
sudo certbot --nginx 
```

## Настройка бота
1. Cкопировать этот гит на сервер любым удобным способом
2. Создать .env файл в /backend со следующим содержанием:
```sh
SECRET_KEY=<секретный_ключ_django>
IS_POSTGRES_DB=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<ваше_имя_пользователя>
POSTGRES_PASSWORD=<ваш_пароль>
DB_HOST=db
DB_PORT=5432
```
3. Создать .env файл в /bot со следующим содержанием:
```sh
TELEGRAM_TOKEN=<токен_телеграм_бота>
USERS_URL=http://web:8000/api/users/
DISHES_URL=http://web:8000/api/dishes/
MENUS_URL=http://web:8000/api/menus/
ORDERS_URL=http://web:8000/api/orders/
ADMIN_IDS=<ваш_id_телеграм>
IS_REDIS_STORAGE=True
IS_WEBHOOK=True
REDIS_DSN=redis://redis:6379/0
BASE_URL=https://<ваш_домен>.<доменная_зона>
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 7771
WEBHOOK_PATH = "/webhook/main/"
```
4. В django, файле settings.py добавить ваш домен в ALLOWED_HOSTS в формате 
   example.com и CSRF_TRUSTED_ORIGINS в формате https://example.com
5. Изменить права доступа к каталогу, если нужно(nginx использует по умолчанию пользователя www-data)
6. Удалить файл .gitkeep из папки postgres (postgres ругается, если каталог не пустой)
7. Запустить установку из файла docker-compose.
```sh
sudo docker-compose up -d --build
```
8. Сделать миграции в базе данных
```sh
sudo docker-compose exec backend python manage.py migrate
```
9. Создать суперпользователя
```sh
sudo docker-compose exec backend python manage.py createsuperuser
```
10. Скопировать файлы статики
```sh
sudo docker-compose exec backend python manage.py collectstatic
```
## Разворачивние на локальной машине, режим разработки и другое
## Внимание:
Нижеприведенная инструкция написана не совсем корректно, как и, возможно, вышеприведенная. Когда-нибудь я ее перепишу, а пока записал видос с запуском на локалке в винде. https://www.youtube.com/watch?v=SzVwEmaOzYA
### Запуск в режиме polling
в файле ./bot/.env переменную IS_WEBHOOK заменить на False или 0
```sh
IS_WEBHOOK=True
```

### Локальный запуск (не в docker-контейнере) с базой данных sqlite
1. Запустить виртуальное окружение, установить зависимости из .
   /bot/requirements.txt  и ./backend/requirements.txt
2. Перевести бота в режим polling
3. В файле ./backend/.env заменить базу данных на sqlite3:
```sh
IS_POSTGRES_DB=False
```
4. В файле ./bot/.env заменить хранилище redis на оперативную память:
```sh
IS_REDIS_STORAGE=False
```
5. В файле ./backend/tgbot/settings.py 
6. Запустить локальный сервер из каталога ./backend командой ```python 
   manage.py runserver```
7. В ./bot/.env файле для переменных USERS_URL, DISHES_URL, MENUS_URL, 
   ORDERS_URL заменить значения ```http://web:8000``` на соответствующие
   ```http://127.0.0.1:8000```
   
8. Запустить .bot/main.py в исполнение
9. Готово

## Автор
dvkonstantinov
telegram: https://t.me/Dvkonstantinov

