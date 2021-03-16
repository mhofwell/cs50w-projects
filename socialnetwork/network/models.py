from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", related_name='posts',
                             on_delete=models.CASCADE)
    body = models.TextField(max_length=350, blank=True)
    likes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "body": self.body,
            "likes": self.likes,
            "timestamp":  self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

    def __str__(self):
        return f"{self.user} on {self.timestamp}"


class UserFollowers(models.Model):
    user = models.ForeignKey("User", related_name='user',
                             on_delete=models.CASCADE)
    followers = models.ManyToManyField("User", related_name='followers')

    def __str__(self):
        return f"{self.followers}"


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
