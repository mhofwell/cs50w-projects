from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name='posts')
    posted_by = models.ForeignKey(
        "User", on_delete=models.PROTECT, related_name='posted_by')
    body = models.TextField(max_length=350, blank=True)
    likes = models.PositiveIntegerField(default=0)
    likedby = models.ManyToManyField(
        "User", related_name="liked", default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "posted_by": self.posted_by.username,
            "body": self.body,
            "likes": self.likes,
            "timestamp":  self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class Likes(models.Model):
    user = models.ForeignKey("User", related_name='user_likes',
                             on_delete=models.CASCADE)
    liked_posts = models.ManyToManyField(
        "Post", related_name='liked_posts', default=None)


class Follow(models.Model):
    user = models.ForeignKey("User", related_name='user',
                             on_delete=models.CASCADE)
    following = models.ManyToManyField(
        "User", related_name='following', default=None)
    followers = models.ManyToManyField(
        "User", related_name='followers', default=None)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body': 'body',
        }
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'id': 'post-body', 'placeholder': 'Write something new!'}),
        }
