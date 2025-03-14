# tasks/admin.py
from django.contrib import admin
from .models import Category, Task, TaskImage, Participation


class TaskImageInline(admin.TabularInline):
    model = TaskImage
    extra = 1


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'category', 'creator', 'status', 'location', 'start_date', 'participants_count', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TaskImageInline, ParticipationInline]
    date_hierarchy = 'created_at'

    def participants_count(self, obj):
        return obj.participants.count()

    participants_count.short_description = 'Кількість учасників'


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status', 'joined_at')
    list_filter = ('status', 'joined_at')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('joined_at',)
    date_hierarchy = 'joined_at'