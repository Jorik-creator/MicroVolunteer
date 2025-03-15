from django.urls import path
from . import views

urlpatterns = [
    # Список усіх завдань
    path('', views.task_list, name='task_list'),
    # Деталі завдання
    path('<int:pk>/', views.task_detail, name='task_detail'),

    # Створення нового завдання
    path('create/', views.task_create, name='task_create'),

    # Оновлення існуючого завдання
    path('<int:pk>/update/', views.task_update, name='task_update'),

    # Видалення завдання
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Приєднання до завдання (для волонтерів)
    path('<int:pk>/join/', views.task_join, name='task_join'),
    # Відмова від участі у завданні
    path('<int:pk>/leave/', views.task_leave, name='task_leave'),

    # Позначення завдання як завершене
    path('<int:pk>/complete/', views.task_complete, name='task_complete'),

    # Скасування завдання
    path('<int:pk>/cancel/', views.task_cancel, name='task_cancel'),
]