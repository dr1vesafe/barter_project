# barter_project
Платформа для обмена вещами (бартерная система)

# Установка:

1. Клонируйте репозиторий:
```bash
git clone https://github.com/dr1vesafe/barter_project.git
```

2. Создайте вирутальное окружение:
Создание на Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Создание на Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте подключение к базе данных PostgreSQL:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barter_db',
        'USER': 'user', ## Введите Ваше имя пользователя
        'PASSWORD': 'password', ## Введите Ваш пароль 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Примените миграции
```bash
python manage.py migrate
```

6. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

7. Запустите сервер
```bash
python manage.py runserver
```

# Стек
- Python 3.8+
- Django 4+
- PostgreSQL