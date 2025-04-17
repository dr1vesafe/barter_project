# barter_project
Платформа для обмена вещами (бартерная система)

# Установка:

1. Клонируйте репозиторий:
```bash
git clone https://github.com/dr1vesafe/barter_project.git
cd barter_project
```

2. Запустите docker контейнеры:
```bash
docker-compose up --build
```

3. Примените миграции:
```bash
docker-compose exec web python manage.py migrate
```

4. Создайте суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

Проект доступен по адресу: http://localhost:8000

Запуск тестов:
```bash
docker-compose exec pytest
```

# Стек
- Python 3.8+
- Django 4+
- PostgreSQL
- Redis
- Docker / Docker Compose
- Pytest / pytest-django