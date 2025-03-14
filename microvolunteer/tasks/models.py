from django.db import models
from django.utils import timezone
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

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

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

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
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='task_images/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.task.title}"


class Participation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('task', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.task.title}"