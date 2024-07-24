from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post

def index(request):
    return render(request, "network/index.html")

def load_posts(request, content, page, profile):
    last_page = page * 10
    first_page = last_page - 10

    any_previous_pages = first_page > 0

    if content == 'all':
        posts = Post.objects.order_by("-timestamp").all()[first_page:last_page]
        any_more_posts = Post.objects.count() > last_page

    elif content == 'profile':
        posts = Post.objects.filter(poster=profile).order_by('-timestamp')[first_page:last_page]
        any_more_posts = Post.objects.filter(poster=profile).order_by('-timestamp').count() > last_page

    elif content == 'following':
        if request.user.is_authenticated:
            following_profiles = request.user.following.all()
            posts = Post.objects.filter(poster__in=following_profiles).order_by("-timestamp")[first_page:last_page]
            any_more_posts = Post.objects.filter(poster__in=following_profiles).count() > last_page

    user_liked_post = [post.id for post in posts if post.liked_by.filter(id=request.user.id).exists()]

    response = {
    'user': request.user.id,
    'posts': [post.serialize() for post in posts],
    'user_liked_post': user_liked_post,
    'is_authenticated' : request.user.is_authenticated,
    'any_more_posts': any_more_posts,
    'any_previous_pages': any_previous_pages
    }
    return JsonResponse(response, safe=False)

@csrf_exempt
@login_required
def profile(request, profile):
    if request.method == "GET":
        profile_user = User.objects.get(pk=profile)
        data = profile_user.serialize()

        is_following = request.user in profile_user.followers.all()

        data["is_following"] = is_following

        return JsonResponse(data, safe=False)

    elif request.method == "PUT":
        profile_user = User.objects.get(pk=profile)
        is_following = request.user in profile_user.followers.all()

        if is_following:
            profile_user.followers.remove(request.user)
            return JsonResponse({"message": "unfollowed successfully"})
        else:
            profile_user.followers.add(request.user)
            return JsonResponse({"message": "followed successfully"})



@login_required
def create_post(request):
    if request.method == "POST":
        post_text = request.POST.get('post_text')

        if post_text != '':
            new_post = Post(
                poster = request.user,
                text = post_text
            )

            new_post.save()

        return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def change_post(request, post):
    fullPost = Post.objects.get(pk=post)


    if request.method == 'GET':

        if fullPost.poster != request.user:
            response = {
                "permission": False,
                "message": "you cant edit a post thats not yours"
            }
            return JsonResponse(response, safe=False)
        else:
            response = {
                "permission": True,
                "post": fullPost.serialize()
            }
            return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        body = json.loads(request.body)

        action = body.get('action')

        if action == 'edit':

            text = body.get('text')

            if fullPost.poster != request.user:
                response = {
                    "permission": False,
                    "message": "you cant edit a post thats not yours"
                }
                return JsonResponse(response, safe=False)

            else:
                fullPost.text = text
                fullPost.save()
                response = {
                    "permission": True,
                    "message": "post udated successfully"
                }

                return JsonResponse(response, safe=False)

        elif action == 'like':

            if fullPost.liked_by.filter(id=request.user.id).exists():
                response = {
                    "got_liked": False
                }

                fullPost.liked_by.remove(request.user)
            else:
                response = {
                    "got_liked": True
                }

                fullPost.liked_by.add(request.user)

            return JsonResponse(response, safe=False)

