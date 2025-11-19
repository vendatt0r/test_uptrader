# Запуск:
- склонировать репозиторий
- установить зависимости: ```pip install -r requirements.txt```
- миграции:
```
python manage.py makemigrations
python manage.py migrate
```
- cоздать суперпользователя: ```python manage.py createsuperuser```
- запуск: ```python manage.py runserver```

Сервер будет доступен по адресу http://localhost:8000/

Сейчас есть возможность создать 2 меню на странице, при желании можно увеличить количество, добавив в templates/index.html дополнительную строку: 

```{% draw_menu "название меню" %}```
