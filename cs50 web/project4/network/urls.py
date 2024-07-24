
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_post", views.create_post, name="create_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # apis
    path("load_posts/<str:content>/<int:page>/<int:profile>", views.load_posts, name="load_posts"),
    path("profile/<int:profile>", views.profile, name="profile"),
    path("edit_post/<int:post>", views.change_post, name="edit_post")
]
