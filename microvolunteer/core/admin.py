# core/admin.py
from django.contrib import admin
from django.db.models import Count, Sum
from tasks.models import Task, Participation, Category
from users.models import User
from django.urls import path
from django.template.response import TemplateResponse


class CoreAdminSite(admin.AdminSite):
    site_header = 'Мікро-Волонтерство - Адміністрування'
    site_title = 'Мікро-Волонтерство'
    index_title = 'Панель адміністратора'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Статистика користувачів
        total_users = User.objects.count()
        volunteers = User.objects.filter(user_type='volunteer').count()
        vulnerable = User.objects.filter(user_type='vulnerable').count()

        # Статистика завдань
        total_tasks = Task.objects.count()
        active_tasks = Task.objects.filter(status__in=['open', 'in_progress']).count()
        completed_tasks = Task.objects.filter(status='completed').count()

        # Категорії завдань
        categories = Category.objects.annotate(tasks_count=Count('tasks')).order_by('-tasks_count')

        # Останні завдання
        latest_tasks = Task.objects.order_by('-created_at')[:10]

        # Останні користувачі
        latest_users = User.objects.order_by('-date_joined')[:10]

        context = {
            'title': 'Панель адміністратора',
            'total_users': total_users,
            'volunteers': volunteers,
            'vulnerable': vulnerable,
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'categories': categories,
            'latest_tasks': latest_tasks,
            'latest_users': latest_users,
        }

        return TemplateResponse(request, 'admin/dashboard.html', context)

# Використання кастомного адмін-сайту (закоментовано, можна розкоментувати за потреби)
# admin_site = CoreAdminSite(name='custom_admin')
# admin_site.register(User, CustomUserAdmin)
# admin_site.register(Category, CategoryAdmin)
# admin_site.register(Task, TaskAdmin)
# admin_site.register(Participation, ParticipationAdmin)