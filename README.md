# Train Project — FastAPI + PostgreSQL + Vite

Pet-проект: бэкенд на FastAPI (SQLAlchemy async), база PostgreSQL, фронтенд на Vite. Все сервисы управляются через Docker Compose.

## 🚀 Быстрый старт

### 1. Настройка окружения

Создай файл `.env` в корне проекта (рядом с `docker-compose.yml`) и заполни его:

```env
POSTGRES_DB_NAME=db
POSTGRES_DB_USER=postgres
POSTGRES_DB_PASSWORD=postgres

PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/db

APP_HOST_PORT=8001
FRONTEND_HOST_PORT=3000
```

> ⚠️ **Важно:** не коммить `.env` в git — в нём хранятся пароли. Файл уже добавлен в `.gitignore`.

### 2. Запуск проекта

```bash
docker compose up -d --build
```

### 3. Проверка статуса

```bash
docker compose ps
```

Все контейнеры должны быть в статусе `Up`. Бэкенд (backend) со временем станет `Up (healthy)`.

---

## 🌐 Адреса сервисов

| Сервис | Адрес | Примечание |
|---|---|---|
| **Бэкенд (FastAPI)** | `http://localhost:8001` | Endpoints: `/health`, `/api/items` |
| **Фронтенд (dev, Vite)** | `http://localhost:5173` | Для разработки; прокси настроен на бэкенд |
| **Фронтенд (prod, nginx)** | `http://localhost:3000` | Доступен, если раскомментирован сервис `frontend` в `docker-compose.yml` |
| **PostgreSQL** | Внутри сети: `db:5432` | |
| **PostgreSQL (с хоста)** | `localhost:5431` | Для клиентов (DBeaver, pgcli) используй `localhost:5431` |
| **pgAdmin** | `http://localhost:5050` | Логин: `admin@example.com`, пароль: `admin` |

---

## 🧪 Быстрые проверки

### Проверить здоровье бэкенда

```bash
curl http://localhost:8001/health
```

Ожидается:
```json
{"status":"ok"}
```

### Создать и получить элемент

```bash
# Создать
curl -X POST http://localhost:8001/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test item", "price": 99.99}'

# Получить все
curl http://localhost:8001/api/items

# Получить по ID
curl http://localhost:8001/api/items/1

# Удалить по ID
curl -X DELETE http://localhost:8001/api/items/1
```

---

## 🗄️ Работа с базой данных (pgAdmin)

1. Открой `http://localhost:5050`
2. Войди: логин `admin@example.com`, пароль `admin`
3. Добавь сервер:
   - **Host name/address:** `db` (или `localhost`, если подключаешься с хоста)
   - **Port:** `5432` (внутри сети) / `5431` (с хоста)
   - **Maintenance database:** `users`
   - **Username:** `postgres`
   - **Password:** `postgres` (из `.env`)
4. В дереве серверов найди базу `users` → таблицы → `items`

---

## 🛠️ Разработка

### Бэкенд

Код в папке `backend/`. Hot reload включён через volume: изменения в `backend/app` подхватываются без пересборки.

### Фронтенд (dev)

Запусти отдельно в папке `frontend`:

```bash
cd frontend
npm run dev
```

Открой `http://localhost:5173`.

### Миграции

Текущая схема создаётся через `Base.metadata.create_all` в `lifespan`. Позже будет подключён Alembic.

---

## 📂 Структура проекта

```
├── backend/          # FastAPI, SQLAlchemy, модели, схемы, зависимости
│   ├── app/
│   │   ├── main.py       # Приложение, маршруты, lifespan
│   │   ├── models.py     # SQLAlchemy модели (Item)
│   │   ├── schemas.py    # Pydantic схемы (ItemCreate, ItemOut)
│   │   ├── database.py   # Подключение к БД, сессии
│   │   └── config.py     # Настройки из .env
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React + Vite, vite.config.ts с прокси на бэкенд
├── postgres/         # Init-скрипты для PostgreSQL (пока пусто)
├── docker-compose.yml    # Описание сервисов
├── .env              # Переменные окружения (не коммитить!)
├── .gitignore        # Исключения для git
└── README.md         # Эта инструкция
```

---

## ⚠️ Важные нюансы

### .env не должен попадать в git

Если случайно закоммитил — удали из истории или сбрось репозиторий для pet-проекта.

### Сброс всех данных (включая БД)

```bash
docker compose down -v
```

> ⚠️ **Эта команда удалит все данные из volume.** Используй только для полной очистки.

### Если бэкенд в статусе `(unhealthy)`

Проверь, что эндпоинт `/health` существует и отвечает `200 OK`.

---

## 📦 Зависимости

### Бэкенд

| Пакет | Версия |
|---|---|
| fastapi | 0.115.6 |
| uvicorn[standard] | 0.32.1 |
| sqlalchemy[asyncio] | 2.0.36 |
| asyncpg | 0.30.0 |
| pydantic-settings | 2.7.0 |
