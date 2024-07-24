from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing>", views.listings, name="listings"),
    path("categories", views.categories, name="categories"),
    path("watchlist/<int:listing>", views.watchlist, name="watchlist"),
    path("bid/<int:listing>", views.bid, name="bid"),
    path("comment/<int:listing>", views.comment, name="comment"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("close_listing/<int:listing>", views.close_listing, name="close_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("not_found/<str:message>", views.not_found, name="not_found")
]
