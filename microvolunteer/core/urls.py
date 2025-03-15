from django.urls import path
from . import views

urlpatterns = [
    # Головна сторінка
    path('', views.home, name='home'),

    # Сторінка "Про нас"
    path('about/', views.about, name='about'),

    # Сторінка контактів
    path('contact/', views.contact, name='contact'),
]