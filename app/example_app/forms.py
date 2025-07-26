from django import forms
from django.forms import ModelForm

from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'priority', 'due_date', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input is-large',
                'placeholder': 'What needs to be done?',
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea',
                'placeholder': 'Add more details about this task (optional)',
                'rows': 3
            }),
            'priority': forms.Select(attrs={
                'class': 'select is-fullwidth'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'input',
                'type': 'datetime-local'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'checkbox'
            })
        }
        labels = {
            'title': 'Task Title',
            'description': 'Description',
            'priority': 'Priority Level',
            'due_date': 'Due Date',
            'completed': 'Mark as completed'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make title field required
        self.fields['title'].required = True
        self.fields['description'].required = False
        self.fields['due_date'].required = False
