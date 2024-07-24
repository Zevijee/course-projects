from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name='title'),
    path("search", views.search, name='search'),
    path('addNewPage', views.addNewPage, name='addNewPage'),
    path('edit/<str:title>', views.edit, name='edit'),
    path("not_found/<str:title>", views.not_found, name='not_found'),
    path("Random_Page>", views.Random_Page, name='Random_Page')
]

