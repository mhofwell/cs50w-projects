from network.models import UserFollowers, User, Post
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserFollowers)
