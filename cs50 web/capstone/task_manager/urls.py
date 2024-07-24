from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_future_list/<str:date>', views.create_future_list, name='create_future_list'),
    path('see_passed_list/<str:date>', views.see_passed_list, name='see_passed_list'),

    # api routes
    path('create_task', views.create_task, name='create_task'),
    path('load_tasks/<str:list>', views.load_tasks, name='load_tasks'),
    path('edit_and_complete_task', views.edit_and_complete_task, name='edit_and_complete_task'),
    path('edit_and_complete_task', views.edit_and_complete_task, name='edit_and_complete_task'),
]