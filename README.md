# Мікро-Волонтерство

![Статус проекту](https://img.shields.io/badge/Статус-В%20розробці-yellow)
![Версія Django](https://img.shields.io/badge/Django-5.1.7-green)
![Docker](https://img.shields.io/badge/Docker-✓-blue)

Веб-платформа для "мікро-волонтерства", призначена для об'єднання волонтерів та людей, які потребують допомоги. Проект полегшує координацію волонтерської діяльності, пошук і створення завдань.

## 📋 Зміст

- [Особливості](#особливості)
- [Технології](#технології)
- [Запуск проекту](#запуск-проекту)
- [Структура проекту](#структура-проекту)
- [Скріншоти](#скріншоти)
- [Внесок у проект](#внесок-у-проект)
- [Ліцензія](#ліцензія)

## ✨ Особливості

- **Реєстрація користувачів** з різними ролями (волонтери, вразливі люди)
- **Управління завданнями** (створення, редагування, видалення)
- **Пошук та фільтрація завдань** за категоріями, датами, статусом
- **Участь у завданнях** і відстеження прогресу
- **Особистий кабінет** з історією активності
- **Статистика волонтерської діяльності**
- **Адаптивний дизайн** для мобільних пристроїв

## 🛠 Технології

- **Бекенд**: Python, Django 5.1
- **Фронтенд**: HTML, CSS, JavaScript, Bootstrap 5
- **База даних**: SQLite (розробка)
- **Розгортання**: Docker
- **Інше**: Django Crispy Forms

## 🚀 Запуск проекту

### За допомогою Docker (рекомендовано)

1. **Клонуйте репозиторій**

```bash
git clone https://github.com/Jorik-creator/MicroVolunteer.git
cd microvolunteer
```

2. **Запустіть з Docker Compose**

```bash
docker-compose up -d --build
```

3. **Застосуйте міграції**

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

4. **Створіть суперкористувача (опціонально)**

```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Відкрийте проект у браузері**

```
http://localhost:8000
```

### Традиційний спосіб (без Docker)

1. **Клонуйте репозиторій**

```bash
git clone https://github.com/ваш-логін/microvolunteer.git
cd microvolunteer
```

2. **Створіть віртуальне середовище та активуйте його**

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```

3. **Встановіть залежності**

```bash
pip install -r requirements.txt
```

4. **Застосуйте міграції**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Запустіть сервер розробки**

```bash
python manage.py runserver
```

6. **Відкрийте проект у браузері**

```
http://localhost:8000
```

## 📁 Структура проекту

```
microvolunteer/
├── core/                  # Основний додаток
├── tasks/                 # Управління завданнями
├── users/                 # Управління користувачами
├── static/                # Статичні файли (CSS, JS, зображення)
├── media/                 # Завантажені медіафайли
├── microvolunteer/        # Конфігурація проекту
├── requirements.txt       # Залежності Python
├── docker-compose.yml     # Конфігурація Docker
├── Dockerfile             # Інструкції для Docker
└── manage.py              # Скрипт управління Django
```

## 📸 Скріншоти

(Додайте скріншоти вашого проекту)

## 📜 Ліцензія

Цей проект поширюється під ліцензією MIT. Дивіться файл `LICENSE` для детальнішої інформації.

---

Розроблено з ❤️ для допомоги іншим.