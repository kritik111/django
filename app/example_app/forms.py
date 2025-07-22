from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input is-large input-modern',
                'placeholder': 'What needs to be done?',
                'required': True,
            })
        }
        labels = {
            'title': 'Task Title'
        }
