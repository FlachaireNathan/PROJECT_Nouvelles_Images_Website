from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.



class UserProfil(models.Model):
    username = models.CharField(max_length=200)
    img = models.ImageField()
    modo = models.BooleanField(default=False)
    class Meta:
        managed = True
    def __str__(self):
        return self.username

class Thread(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
    user_op = models.ForeignKey(User,related_name='thread_user_op',on_delete=models.CASCADE, default=None)
    creation_date = models.DateField()
    user_modo = models.ForeignKey(User,related_name='thread_user_modo',on_delete=models.CASCADE, null=True, blank=True)
    modification_date = models.DateField(null=True, blank=True)
    modification = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Threads"
        managed = True
    
    def __str__(self):
        return self.title
    

class Post(models.Model):
    body = RichTextField()
    thread_id = models.ForeignKey(Thread,on_delete=models.CASCADE)
    user_op = models.ForeignKey(User,related_name='post_user_op',on_delete=models.CASCADE, default=None)
    creation_date = models.DateField(default=datetime.now, blank=True)
    user_modo = models.ForeignKey(User,related_name='post_user_modo',on_delete=models.CASCADE, default=None, null=True, blank=True)
    modification_date = models.DateField(default=datetime.now, blank=True, null=True)
    modification = models.BooleanField(default=False)
    beingChild = models.BooleanField(default=False)
    is_pin = models.BooleanField(default=False)
    have_child = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Posts"
        managed = True
    


class ChildPost(models.Model):
    body = RichTextField()
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_op = models.ForeignKey(User,related_name='childpost_user_op',on_delete=models.CASCADE, default=None)
    creation_date = models.DateField(default=datetime.now, blank=True)
    user_modo = models.ForeignKey(User,related_name='childpost_user_modo',on_delete=models.CASCADE, default=None, null=True, blank=True)
    modification_date = models.DateField(default=datetime.now, null=True, blank=True)
    modification = models.BooleanField(default=False)
    beingChild = models.BooleanField(default=True)
    is_last = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "ChildPosts"
        managed = True
