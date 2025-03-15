from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Реєстрація нового користувача
    path('register/', views.register, name='register'),

    # Вхід користувача
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # Вихід користувача
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Профіль користувача
    path('profile/', views.profile, name='profile'),

    # Особистий кабінет користувача
    path('dashboard/', views.dashboard, name='dashboard'),
]