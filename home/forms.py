"""
from django import forms
from .models import Thread

class ThreadForm(Thread):
    class Meta:
        model = Thread
        fields = ['body']
"""

from django.db import models
from django.forms import ModelForm
from .models import *
from ckeditor.fields import RichTextField

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ['body']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']

class ChildPostForm(ModelForm):
    class Meta:
        model = ChildPost
        fields = ['body']


"""
class ThreadForm(models.Model):
    content = RichTextField()
"""