import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import forms

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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


def profile(request, username):
    """Load a users profile, where their profile information will be displayed, as well as any posts they have made.
    Clicking a post should bring up the post itself via JS (Like loading a message in mailbox)
    """

    if username == request.user.username:
        print("Username matches")
        form = forms.PostForm
        return render(request, "network/profile.html", {
            "form": form
        })
    else:
        print("Else", username)
        current_user = request.user.username
        profile_username = username
        return render(request, "network/profile.html", {
            "current_user": current_user,
            "profile_username": profile_username
        })


def user_profile(request, username):
    """Direct to user's profile page when clicked on a post"""
    pass


def following(request):
    """Load the page displaying the posts form users that a User is following, visually identical to all_posts(), except restricted
    to only users that are being followed.  Posts should be clicked to bring up a detailed view with JS (like loading a message in mailbox)
    """
    return render(request, "network/following.html")


def all(request):
    """Visually and functionally identical to following except not limited to only followed users, should display all posts on the site, in descending order
    As profile() and following(), clicking on a post should bring up a detailed view similar to loading a message in mailbox project.
    """
    form = forms.PostForm
    return render(request, "network/all.html", {
        "form": form
    })


@csrf_exempt
@login_required
def create_post(request):
    """Submit a post"""
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    print("request", data, "request.POST: ", request.POST, "request.GET", request.GET)
    body = data.get("body", "")

    new_post = Post(
        user=request.user,
        body=body
    )
    new_post.save()
    return JsonResponse({"message": "Post successfully uploaded"}, status=201)


@login_required
def display_posts(request, url_address):
    if url_address == f'{request.user.username}':
        # Display user specific posts (Profile)
        print("Url address: Request user",request.user.username)
        posts = Post.objects.filter(
            user=request.user
        )
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)
    elif url_address == 'all':
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)
    else:

        # Display Followed User Posts (Following)
        user = User.objects.filter(username=url_address)[0]
        posts = Post.objects.all()
        posts = Post.objects.filter(
            user=user
        )
        posts = posts.order_by("-timestamp").all()
        return JsonResponse([post.serialize() for post in posts], safe=False)

# @login_required
# def mailbox(request, mailbox):

#     # Filter emails returned based on mailbox
#     if mailbox == "inbox":
#         emails = Email.objects.filter(
#             user=request.user, recipients=request.user, archived=False
#         )
#     elif mailbox == "sent":
#         emails = Email.objects.filter(
#             user=request.user, sender=request.user
#         )
#     elif mailbox == "archive":
#         emails = Email.objects.filter(
#             user=request.user, recipients=request.user, archived=True
#         )
#     else:
#         return JsonResponse({"error": "Invalid mailbox."}, status=400)

#     # Return emails in reverse chronologial order (This also gets the emails associated with the user from the DB, and serializes them to JSON)
#     emails = emails.order_by("-timestamp").all()
#     return JsonResponse([email.serialize() for email in emails], safe=False) # Each email is serialized to a JSON object readable by JS

