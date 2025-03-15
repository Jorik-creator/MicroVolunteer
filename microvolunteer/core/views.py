from django.shortcuts import render
from django.db.models import Count, Sum
from tasks.models import Task, Participation
from users.models import User


def home(request):
    # останні активні завдання
    active_tasks = Task.objects.filter(status='open').order_by('-created_at')[:6]

    # статистика для відображення
    volunteer_count = User.objects.filter(user_type='volunteer').count()
    vulnerable_count = User.objects.filter(user_type='vulnerable').count()
    tasks_count = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()

    context = {
        'active_tasks': active_tasks,
        'volunteer_count': volunteer_count,
        'vulnerable_count': vulnerable_count,
        'tasks_count': tasks_count,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')