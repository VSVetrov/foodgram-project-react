# praktikum_new_diplom

## Стек технологий
Python, Django, Django REST Framework, NGINX, Docker

## Описание проекта
Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в pdf формате.

## Установка проекта
- скопировать репозиторий на локальную машину
- запустить виртуальное окружение 
    python -m venv env
    . venv/scripts/activate
- Cоздайте файл .env в директории /infra/ с содержанием:
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

- Перейти в директирию и установить зависимости из файла requirements.txt:
    pip install -r requirements.txt 
- Выполните миграции:
    python manage.py makemigrations
    python manage.py migrate

## Запуск проекта в Docker контейнере

- Установите Docker
Параметры запуска описаны в файлах docker-compose.yml и nginx.conf которые находятся в директории infra/.
При необходимости добавьте/измените адреса проекта в файле nginx.conf

- Запустите docker compose
    docker-compose up -d --build

-После сборки появляются 3 контейнера:
    контейнер базы данных db
    контейнер приложения backend
    контейнер web-сервера nginx

## Автор
Ветров В.С. - Python разработчик. Трудился над backend. 