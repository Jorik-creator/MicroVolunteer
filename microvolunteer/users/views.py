from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from .models import User
from tasks.models import Task, Participation


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ви успішно зареєструвалися!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль було оновлено!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user

    if user.user_type == 'volunteer':
        active_participations = Participation.objects.filter(
            user=user,
            task__status__in=['open', 'in_progress']
        ).select_related('task')

        past_participations = Participation.objects.filter(
            user=user,
            task__status__in=['completed', 'cancelled']
        ).select_related('task')

        context = {
            'active_participations': active_participations,
            'past_participations': past_participations,
        }
    else:  # vulnerable user
        created_tasks = Task.objects.filter(creator=user)
        active_tasks = created_tasks.filter(status__in=['open', 'in_progress'])
        past_tasks = created_tasks.filter(status__in=['completed', 'cancelled'])

        context = {
            'active_tasks': active_tasks,
            'past_tasks': past_tasks,
        }

    return render(request, 'users/dashboard.html', context)