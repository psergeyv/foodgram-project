# foodgram-project

**Дипломный проект**

# Описание
Сайт кулинарных рецептов

# Установка
 - клонируйте проект 
# Создайте .env с настройками для подключения к БД
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=Имя БД
- POSTGRES_USER=пользователь
- POSTGRES_PASSWORD=пароль
- DB_HOST=db
- DB_PORT=5432
**Насатройки NGINX находятся в nginx/conf.d/local.conf**
# Создание docker контейнера
 - запуск проекта выполняется командой **docker-compose up**
# следующий шаги
 - открываем терминал **docker-compose exec foodgram bash**
 - миграция **python manage.py makemigrations users** (для расширения модели User)
 - миграция **python manage.py migrate users** (для расширения модели User)
 - миграция **python manage.py migrate**
 - создание администратора **python manage.py createsuperuser**
 # настройка
 - Войдите в админку сайта, Управление сайтом - Настройки сайта и добавьте настройки для текущего сайта.
 - Войдите в админку сайта, Простые страницы, добавте 2 страницы с адресами (/about/ и /technology/).

# Сайт готов к наполнению и использованию!
- при желании можно заполнить таблицу с Ингредиентами
**python manage.py loaddata db.json**