
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.get_profile, name="profile"),



    # API Routes
    path("post", views.post, name="post"),
    path("posts/<str:group>", views.load_posts, name="posts"),
    path("follow/<str:username>", views.follow, name="follow"),
    # path("unfollow/<str:username>", views.unfollow, name="unfollow"),
]
