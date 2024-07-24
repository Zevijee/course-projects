import json
from datetime import date
from django.utils import timezone
from django.shortcuts import HttpResponseRedirect, render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import User, Task

import logging

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


def index(request):
    logger.info('hello')
    if request.user.is_authenticated:
        return render(request, "task_manager/index.html", {})

    else:
        return HttpResponseRedirect(reverse("login"))


def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    task = data.get('task')
    time = data.get('time')
    urgency = data.get('urgency')
    date_todo_on = data.get('dayToDo')

    if date_todo_on == 'today':
        date_todo_on = date.today()

    else:
        date_todo_on = data.get('dayToDo')


    if data == '':
        return JsonResponse({'message': 'The task box must contain a task.'})

    if time == '':
        return JsonResponse({'message': 'The task box must contain a task.'})


    new_task = Task(
        user = request.user,
        text = task,
        time = time,
        date_todo_on = date_todo_on,
        urgency = urgency
    )

    new_task.save()

    return JsonResponse({'message': 'Task created successfully'})


def load_tasks(request, list):
    if list == 'today':
        current_date = timezone.now().date()

    else:
        current_date = list

    task_list = Task.objects.filter(date_todo_on=current_date).order_by('time')
    return JsonResponse({'list': [task.serialize() for task in task_list]})


def edit_and_complete_task(request):
    if request.method != "PUT":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    task_id = data.get('task')
    action = data.get('action')
    edited_text = data.get('editedTask')

    task = Task.objects.get(pk=task_id)

    if action == 'edit':
        if edited_text != None:
            task.text = edited_text
            task.save()

        else:
            return HttpResponse(status=304)

    elif action == 'complete':
        task.completed = not task.completed
        task.save()

    elif action == 'delete':
        task.delete()

    return JsonResponse({'message': action})

def create_future_list(request, date):
    return render(request, 'task_manager/create_future_list.html', {
        "date": date
    })


def see_passed_list(request, date):
    return render(request, 'task_manager/see_passed_list.html', {
        "date": date
    })

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]

        # checking if the password and confirmation match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "task_manager/register.html", {
                "message" : "Passwords must match."
            })

        # checking if theres a user with the username already
        current_users = User.objects.all()

        for user in current_users:
            if user.username == username:
                return render(request, "task_manager/register.html", {
                    "message" : "Username is already taken."
                })

        # creating the new user
        user = User.objects.create_user(username, None, password)
        user.save()

        login(request, user)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "task_manager/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempts to sign in the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if user signed in successfully
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "task_manager/login.html", {
                "message" : "Invalid username and/or password."
            })

    else:
        return render(request, "task_manager/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

