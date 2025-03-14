from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/join/', views.task_join, name='task_join'),
    path('<int:pk>/leave/', views.task_leave, name='task_leave'),
    path('<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('<int:pk>/cancel/', views.task_cancel, name='task_cancel'),
]