from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add/<int:listing_id>",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<str:title>", views.getpage, name="getpage")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
