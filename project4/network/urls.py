
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
    path("save/<int:id>", views.save, name="save"),
    path("profile/save/<int:id>", views.save, name="save_profile"),
    path("likedposts", views.liked_posts, name="liked_posts"),
    path("posts/<str:group>", views.load_posts, name="posts"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("followcount/<str:username>", views.count, name="count"),
    path("like/<int:postid>", views.like, name="like"),
    path("likecount/<int:postid>", views.like_count, name="count"),
]
