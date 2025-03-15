from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm
from .models import User
from tasks.models import Task, Participation


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Створює та зберігаємо нового користувача
            user = form.save()
            # Логінитти користувача після реєстрації
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

    # Загальна статистика для всіх користувачів
    user_joined_date = user.date_joined.strftime('%d.%m.%Y')
    days_as_member = (timezone.now().date() - user.date_joined.date()).days

    # Базовий контекст для всіх типів користувачів
    context = {
        'user_joined_date': user_joined_date,
        'days_as_member': days_as_member,
    }

    # Різний контекст для волонтерів та вразливих людей
    if user.user_type == 'volunteer':
        all_participations = Participation.objects.filter(user=user).select_related('task')

        # Розділяємо на активні та минулі
        active_participations = all_participations.filter(
            task__status__in=['open', 'in_progress']
        )

        completed_participations = all_participations.filter(
            task__status='completed'
        )

        cancelled_participations = all_participations.filter(
            task__status='cancelled'
        )

        # Статистика для волонтерів
        total_hours_helped = sum(
            (p.task.end_date - p.task.start_date).total_seconds() / 3600
            for p in completed_participations
            if p.task.end_date
        )

        unique_categories = set(
            p.task.category.name for p in all_participations
            if p.task.category
        )

        # Статистика за місяцями (останні 6 місяців)
        from django.db.models import Count
        from django.db.models.functions import TruncMonth

        monthly_stats = Participation.objects.filter(
            user=user,
            joined_at__gte=timezone.now() - timezone.timedelta(days=180)
        ).annotate(
            month=TruncMonth('joined_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        # Форматуємо дані для графіка
        months = []
        counts = []

        for stat in monthly_stats:
            months.append(stat['month'].strftime('%b %Y'))
            counts.append(stat['count'])

        context.update({
            'active_participations': active_participations,
            'completed_participations': completed_participations,
            'cancelled_participations': cancelled_participations,
            'total_participations': all_participations.count(),
            'completed_count': completed_participations.count(),
            'cancelled_count': cancelled_participations.count(),
            'total_hours_helped': round(total_hours_helped, 1),
            'categories_helped': len(unique_categories),
            'categories_list': list(unique_categories),
            'chart_months': months,
            'chart_counts': counts,
        })
    else:  # для вразливих людей
        # Отримує всі завдання
        all_tasks = Task.objects.filter(creator=user)

        # Розділяє на активні та скасоавні
        active_tasks = all_tasks.filter(status__in=['open', 'in_progress'])
        completed_tasks = all_tasks.filter(status='completed')
        cancelled_tasks = all_tasks.filter(status='cancelled')

        # Статистика для вразливих людей
        total_volunteers = Participation.objects.filter(
            task__creator=user
        ).values('user').distinct().count()

        # Статистика участі за завданнями
        task_participation_stats = []
        for task in all_tasks:
            participants_count = task.participants.count()
            task_stat = {
                'task': task,
                'participants_count': participants_count,
                'max_participants': task.max_participants,
                'participation_rate': (
                            participants_count / task.max_participants * 100) if task.max_participants > 0 else 0
            }
            task_participation_stats.append(task_stat)

        # Статистика за категоріями
        from django.db.models import Count

        category_stats = all_tasks.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')

        # Формуємо дані для графіка
        categories = []
        category_counts = []

        for stat in category_stats:
            if stat['category__name']:  # Перевіряємо, що категорія не None
                categories.append(stat['category__name'])
                category_counts.append(stat['count'])

        context.update({
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'cancelled_tasks': cancelled_tasks,
            'total_created_tasks': all_tasks.count(),
            'completed_tasks_count': completed_tasks.count(),
            'cancelled_tasks_count': cancelled_tasks.count(),
            'total_volunteers_helped': total_volunteers,
            'task_participation_stats': task_participation_stats,
            'chart_categories': categories,
            'chart_category_counts': category_counts,
        })

    return render(request, 'users/dashboard.html', context)