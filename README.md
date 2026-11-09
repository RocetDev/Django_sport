# Sport base list

Django-приложение для учёта спортсменов. Данные можно сохранять либо в базу данных (PostgreSQL), либо в файл JSON, выбрав хранилище прямо на форме. Для записей в БД реализованы дубликаты-проверка, AJAX-поиск, редактирование и удаление.

Приложение упаковано в Docker-контейнеры (Django + PostgreSQL) и переведено с SQLite на PostgreSQL.

## Quick Start (Docker)

Требуется: Docker и Docker Compose.

    git clone https://github.com/RocetDev/Django_sport.git
    cd Django_sport

    # 1. Создать .env с реальными значениями (шаблон — .env.example)
    cp .env.example .env
    nano .env   # заполнить POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, DJANGO_SECRET_KEY

    # 2. Собрать и запустить контейнеры
    docker compose up -d --build

    # 3. Открыть приложение
    http://localhost:8081

Миграции и сбор статики выполняются автоматически при старте контейнера (ENTRYPOINT в Dockerfile):
`migrate` → `collectstatic` → gunicorn.

Полезные команды:

    docker compose logs -f webapp    # логи приложения
    docker compose stop              # остановить
    docker compose down              # остановить и удалить контейнеры
    docker compose exec webapp python manage.py createsuperuser  # админка (/admin/)

## Запуск в режиме разработки

Для разработки используйте `DJANGO_DEBUG=1` в `.env`. Контейнеры работают так же, но доступны подробные страницы ошибок Django, а шаблоны и статика смонтированы как volume — правки применяются без пересборки образа (требуется только перезапуск страницы; для изменения кода Python — `docker compose restart webapp`).

Для продакшена: `DJANGO_DEBUG=0`, секретный ключ сгенерировать через:

    python -c "import secrets; print(secrets.token_urlsafe(50))"

## Переменные окружения (.env)

| Переменная | Описание |
|---|---|
| `POSTGRES_USER` | пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | пароль PostgreSQL |
| `POSTGRES_DB` | имя базы данных |
| `DJANGO_SECRET_KEY` | секретный ключ Django |
| `DJANGO_DEBUG` | `1` — разработка, `0` — продакшен |
| `DJANGO_ALLOWED_HOSTS` | разрешённые хосты через запятую |

`.env` не хранится в репозитории (в `.gitignore`). Реальные значения — только в локальном `.env`, в репозитории лежит `.env.example` с примерами.

## Миграция данных с SQLite на PostgreSQL

Данные переносятся штатными средствами Django — через dumpdata/loaddata:

    # 1. Выгрузка данных из старой SQLite (с хоста)
    python manage.py dumpdata athletes_base --database=legacy_sqlite --indent 2 -o data_backup.json

    # 2. Запуск контейнеров (миграции в PostgreSQL применятся автоматически)
    docker compose up -d --build

    # 3. Копирование fixture внутрь контейнера
    docker compose cp data_backup.json webapp:/tmp/data_backup.json

    # 4. Загрузка данных в PostgreSQL
    docker compose exec webapp python manage.py loaddata /tmp/data_backup.json

    # 5. Проверка
    docker compose exec webapp python manage.py shell -c "from athletes_base.models import Athlete; print(Athlete.objects.count())"

После успешного переноса файл `data_backup.json` и `db.sqlite3` можно удалить.
Примечание: в SQLite-базе этого проекта не было записей, поэтому fixture пуст — процесс описан и протестирован на случай наличия данных.

## Структура проекта

    Dockerfile                     # образ Django-приложения
    docker-compose.yaml            # Django + PostgreSQL
    .dockerignore / .env.example   # исключения для сборки / шаблон секретов
    athletes_base/static/athletes_base/   # статика (CSS, JS)
    athletes_base/templates/       # HTML-шаблоны
    athletes_base/models.py        # модель спортсмена
    athletes_base/storage.py       # JSON-хранилище

## Структура загружаемого JSON файла
Загружаемый фаил json должен иметь определенный формат иначе возникнет ошибка при загрузке:

    [
	    {
		    "first_name": "adfa",
		    "last_name": "asdf",
		    "middle_name": "asdf",
		    "birth_date": "2026-09-01",
		    "sex": "M",
		    "sport": "swimming",
		    "rank": "1y",
		    "city": "Магнитогорск",
		    "team": "tema"
	    },
	    ...
    ]
