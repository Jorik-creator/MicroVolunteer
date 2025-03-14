from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Task, Category, Participation, TaskImage
from .forms import TaskForm, TaskImageForm, TaskSearchForm, ParticipationForm


def task_list(request):
    """
    View for displaying the list of tasks with filtering options
    """
    tasks = Task.objects.filter(status='open').order_by('-created_at')
    form = TaskSearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        status = form.cleaned_data.get('status')

        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        if category:
            tasks = tasks.filter(category=category)

        if date_from:
            tasks = tasks.filter(start_date__gte=date_from)

        if date_to:
            tasks = tasks.filter(start_date__lte=date_to)

        if status:
            tasks = tasks.filter(status=status)

    paginator = Paginator(tasks, 12)  # Show 12 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    is_participant = False
    can_join = False

    if request.user.is_authenticated:
        is_participant = Participation.objects.filter(task=task, user=request.user).exists()
        can_join = (not is_participant and
                    task.status == 'open' and
                    task.available_spots > 0 and
                    not task.is_past_due)

    context = {
        'task': task,
        'is_participant': is_participant,
        'can_join': can_join,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()

            images = request.FILES.getlist('images')
            for image in images:
                TaskImage.objects.create(task=task, image=image)

            messages.success(request, 'Завдання успішно створено!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()

    context = {
        'form': form,
        'image_form': TaskImageForm(),
    }
    return render(request, 'tasks/task_create.html', context)


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Ensure only the creator can update the task
    if request.user != task.creator:
        messages.error(request, 'У вас немає дозволу на редагування цього завдання.')
        return redirect('task_detail', pk=task.pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

            images = request.FILES.getlist('images')
            for image in images:
                TaskImage.objects.create(task=task, image=image)

            messages.success(request, 'Завдання успішно оновлено!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,
        'image_form': TaskImageForm(),
    }
    return render(request, 'tasks/task_update.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Ensure only the creator can delete the task
    if request.user != task.creator:
        messages.error(request, 'У вас немає дозволу на видалення цього завдання.')
        return redirect('task_detail', pk=task.pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Завдання успішно видалено!')
        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_join(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Check if user can join
    if task.status != 'open':
        messages.error(request, 'Це завдання не є відкритим для участі.')
        return redirect('task_detail', pk=task.pk)

    if task.available_spots <= 0:
        messages.error(request, 'На жаль, усі місця для цього завдання вже зайняті.')
        return redirect('task_detail', pk=task.pk)

    if task.is_past_due:
        messages.error(request, 'Це завдання вже минуло.')
        return redirect('task_detail', pk=task.pk)

    # Check if already joined
    if Participation.objects.filter(task=task, user=request.user).exists():
        messages.info(request, 'Ви вже приєдналися до цього завдання.')
        return redirect('task_detail', pk=task.pk)

    # Join the task
    Participation.objects.create(task=task, user=request.user)

    # If all spots are filled, change status to in_progress
    if task.available_spots == 0:
        task.status = 'in_progress'
        task.save()

    messages.success(request, 'Ви успішно приєдналися до завдання!')
    return redirect('task_detail', pk=task.pk)


@login_required
def task_leave(request, pk):
    task = get_object_or_404(Task, pk=pk)
    participation = get_object_or_404(Participation, task=task, user=request.user)

    # Check if the task has already started
    if task.is_past_due:
        messages.error(request, 'Ви не можете покинути завдання, яке вже розпочалося.')
        return redirect('task_detail', pk=task.pk)

    participation.delete()

    # If task was in_progress, change back to open
    if task.status == 'in_progress':
        task.status = 'open'
        task.save()

    messages.success(request, 'Ви успішно покинули завдання.')
    return redirect('task_detail', pk=task.pk)


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Ensure only the creator can complete the task
    if request.user != task.creator:
        messages.error(request, 'У вас немає дозволу на завершення цього завдання.')
        return redirect('task_detail', pk=task.pk)

    task.status = 'completed'
    task.save()

    messages.success(request, 'Завдання успішно завершено!')
    return redirect('task_detail', pk=task.pk)


@login_required
def task_cancel(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Ensure only the creator can cancel the task
    if request.user != task.creator:
        messages.error(request, 'У вас немає дозволу на скасування цього завдання.')
        return redirect('task_detail', pk=task.pk)

    task.status = 'cancelled'
    task.save()

    messages.success(request, 'Завдання успішно скасовано!')
    return redirect('task_detail', pk=task.pk)