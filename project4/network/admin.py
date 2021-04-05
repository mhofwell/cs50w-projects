from django.contrib import admin
from .models import Post, User, Follow

# Register your models here.
admin.site.register(User)
admin.site.regiser(Follow)
admin.site.resgister(Post)
