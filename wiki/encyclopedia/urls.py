from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:title>", views.getpage, name="getpage")
]
