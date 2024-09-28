# Тестовое задание

## Программа для вывода "n" первых элементов последовательности 122333444455555… (число повторяется столько раз, чему оно равно).

### Запуск программы

1. В корневой директории запускаем команду:
    ```bash
    python Task_1.py
    ```
2. Следуем дальнейшим инструкциям, отображающимся на экране

## Django проект магазина продуктов:

Стек: Python 3.11.8, Django 3.2.3, DRF, SQLite.

### Запуск проекта

Клонировать репозиторий:
```
git clone git@github.com:voven007/InMagDjango_EA_Test.git
```
В директории InMagDjango_EA_Test создать и активировать виртуальное окружение:
```
python -m venv venv
source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```
В директории InMagDjango_EA_Test создать и заполнить файл .env:
```
touch .env

SECRET_KEY='Секретный ключ'
ALLOWED_HOSTS='Имя или IP хоста'
DEBUG=True
```
Далее переходим в директорию с backend
```
cd backend
```
Выполнить миграции:
```
python manage.py migrate
```
Создать суперпользователя:
```
python manage.py createsuperuser
```
Запустить проект:
```
python manage.py runserver
```


Админ панель: http://127.0.0.1:8000/admin/ 

Документация для API доступна по адресу http://127.0.0.1:8000/api/redoc/. 
Документация представлена в формате Redoc.

Документация для API доступна по адресу http://127.0.0.1:8000/api/swagger/. 
Документация представлена в формате Swagger.


## Автор
[Бабенко Владимир](https://github.com/voven007)
