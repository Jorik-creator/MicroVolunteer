from django.db import models
from django.utils import timezone
from users.models import User


def task_image_path(instance, filename):
    import os
    import time
    from uuid import uuid4

    # Отримує розширення файлу
    ext = filename.split('.')[-1]

    # Генерує унікальне ім'я файлу
    filename = f"{uuid4().hex}_{int(time.time())}.{ext}"

    # Якщо task_id ще не існує (новостворене завдання), використовує тимчасову папку
    if instance.task_id:
        return os.path.join('task_images', f'task_{instance.task_id}', filename)
    else:
        return os.path.join('task_images', 'temp', filename)

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Назва категорії')
    description = models.TextField(blank=True, null=True, help_text='Опис категорії')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Task(models.Model):
    STATUS_CHOICES = (
        ('open', 'Відкрито'),
        ('in_progress', 'В процесі'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    )

    title = models.CharField(max_length=255, help_text='Назва завдання')
    description = models.TextField(help_text='Детальний опис завдання')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks',
                               help_text='Категорія завдання')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks',
                              help_text='Користувач, який створив завдання')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата створення завдання')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата останнього оновлення')
    location = models.CharField(max_length=255, help_text='Місце проведення завдання')
    start_date = models.DateTimeField(help_text='Дата та час початку завдання')
    end_date = models.DateTimeField(blank=True, null=True, help_text='Дата та час закінчення завдання (необов\'язково)')
    max_participants = models.PositiveIntegerField(default=1, help_text='Максимальна кількість учасників')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open',
                            help_text='Статус завдання')

    def __str__(self):
        return self.title

    @property
    def is_past_due(self):
        return timezone.now() > self.start_date

    @property
    def available_spots(self):
        taken_spots = self.participants.count()
        return max(0, self.max_participants - taken_spots)


class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images',
                           help_text='Завдання, до якого відноситься зображення')
    image = models.ImageField(upload_to=task_image_path, help_text='Зображення завдання')
    upload_date = models.DateTimeField(auto_now_add=True, help_text='Дата завантаження зображення')

    def __str__(self):
        return f"Зображення для {self.task.title}"


class Participation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='participants',
                           help_text='Завдання, в якому бере участь користувач')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations',
                           help_text='Користувач, який бере участь у завданні')
    joined_at = models.DateTimeField(auto_now_add=True, help_text='Дата приєднання до завдання')
    status = models.CharField(max_length=20, default='active', help_text='Статус участі')
    feedback = models.TextField(blank=True, null=True, help_text='Відгук користувача про завдання')

    class Meta:
        unique_together = ('task', 'user')

    def __str__(self):
        return f"{self.user.username} у завданні {self.task.title}"