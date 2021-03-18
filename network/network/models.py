from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django import forms


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name='posts')
    posted_by = models.ForeignKey(
        "User", on_delete=models.PROTECT, related_name='posted_by')
    body = models.TextField(max_length=350, blank=True)
    likes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "posted_by": self.posted_by.post,
            "body": self.body,
            "likes": self.likes,
            "timestamp":  self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


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
