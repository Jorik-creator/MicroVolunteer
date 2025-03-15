FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Встановлення залежностей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання коду проекту
COPY . /app/

# Відкриваємо порт
EXPOSE 8000

# Створення каталогів для медіа та статичних файлів
RUN mkdir -p /app/media /app/static

# Команда для запуску
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]