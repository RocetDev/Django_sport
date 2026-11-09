FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

ENTRYPOINT python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn athletes_app.wsgi:application --bind 0.0.0.0:8081
