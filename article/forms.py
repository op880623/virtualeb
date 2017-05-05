from django import forms
from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['commenter', 'text']
        widgets = {
            'commenter': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }
        labels = {
            'commenter': 'Your name',
            'text': 'comment',
        }
        max_lengths = {
            'commenter': 60,
        }
