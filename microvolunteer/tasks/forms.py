from django import forms
from .models import Task, TaskImage, Participation, Category
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'location', 'start_date',
                  'end_date', 'max_participants']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and timezone.now() > start_date:
            raise forms.ValidationError("Дата початку не може бути в минулому.")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("Дата завершення не може бути раніше дати початку.")

        return cleaned_data


class TaskImageForm(forms.ModelForm):
    class Meta:
        model = TaskImage
        fields = ['image']


class TaskSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Пошук')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категорія'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата від'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата до'
    )
    status = forms.ChoiceField(
        choices=[('', '---')] + list(Task.STATUS_CHOICES),
        required=False,
        label='Статус'
    )


class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['feedback']