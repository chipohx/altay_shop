# Altay Shop

Интернет-магазина на FastAPI и PostgreSQL.

## Описание

Altay Shop - веб-приложение для интернет-магазина, которое предоставляет следующие возможности:
- Аутентификация и авторизация пользователей
- Управление товарами
- Работа с корзиной покупок
- Оформление заказов

## Технологии

- FastAPI - современный веб-фреймворк для создания API
- PostgreSQL - реляционная база данных
- SQLAlchemy - ORM для работы с базой данных
- Alembic - система миграций базы данных
- Docker - запуск БД

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd altay_shop
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
# Для Windows:
.venv\Scripts\activate
# Для Linux/Mac:
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта и настройте переменные окружения:
```
DATABASE_URL=postgresql://user:password@localhost:5435/altay_shop_db
SECRET_KEY=your-secret-key

DATABASE_URL=postgresql://user:password@localhost:5436/auth_db
SECRET_KEY=your-secret-key
```

5. Запустите базу данных с помощью Docker:
```bash
docker-compose up -d
```

6. Примените миграции базы данных:
```bash
alembic -c app/alembic.ini init migration
alembic -c app/alembic.ini revision --autogenerate -m "init"
alembic -c app/alembic.ini upgrade head

alembic -c auth/alembic.ini init migration
alembic -c auth/alembic.ini revision --autogenerate -m "init"
alembic -c auth/alembic.ini upgrade head
```

7. Запустите приложение:
```bash
uvicorn app.main:app --port 8003
uvicorn auth.main:app --port 8004
```

После запуска приложение будет доступно по адресу: http://localhost:8003

## Документация API

После запуска приложения, документация API доступна по следующим адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Скриншоты приложения

### Главная страница
![Главная страница](examples/main.png)

### Страница аутентификации
![Страница аутентификации](examples/auth.png)

### Панель администратора
![Панель администратора](examples/admin.png)