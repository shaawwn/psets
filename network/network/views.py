import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import forms

from .models import User, Post, Profile


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

        # Create user profile (to allow for following)
        profile = Profile()
        profile.profile_name = user
        profile.save()
        print(profile)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def react(request):
    """Test react page"""
    form = forms.PostForm
    return render(request, "network/react.html", {
        "form": form
    })


def profile(request, username):
    """Load a users profile, where their profile information will be displayed, as well as any posts they have made.
    Clicking a post should bring up the post itself via JS (Like loading a message in mailbox)
    """
    current_user = request.user.username
    # If it is the current user's profile page, allow posts to be made via form directly from profile page
    if username == current_user:
        form = forms.PostForm
        return render(request, "network/profile.html", {
            "form": form,
            "username": username
        })
    else:
        # Disable form if profile page is not current user
        # current_user = request.user.username
        return render(request, "network/profile.html", {
            "current_user": current_user,
            "username": username
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
    body = data.get("body", "")

    new_post = Post(
        user=request.user,
        body=body
    )
    new_post.save()
    return JsonResponse({"message": "Post successfully uploaded"}, status=201)


# @login_required ### Turning this off/on changes whether posts will display if logged in or not (Keep posts displayed even if not logged in)
def display_posts(request, url_address):
    """Display user posts in pages, type of post depends on which page. All displays all user posts, profile
    displays only the posts by that user, and following displays posts from users that the User is following
    """
    if url_address == f'{request.user.username}':
        # Display user specific posts (Profile)
        posts = Post.objects.filter(
            user=request.user
        )

    elif url_address == 'all':
        posts = Post.objects.all()

    else:
        # Display Followed User Posts (Following). Currently WIP, so placeholder All posts.
        user = User.objects.filter(username=url_address)[0]
        # posts = Post.objects.all() # Guess I don't need this, I don't know why it wasn't working earlier then
        posts = Post.objects.filter(
            user=user
        )
    # Moved this out of the if-conditionals for streamlining (Should only need to be at the end anyways since it is same for all conditions.)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def follow(request, profile_name):
    username = request.user.username
    user = User.objects.get(username=username) # Filter or get? See above
    to_follow = User.objects.get(username=profile_name)
    following = Profile.objects.get(
        profile_name = user
    )

    if to_follow in following.following.all():
        print("Unfollowing", to_follow.username)
        following.following.remove(to_follow)
        print(following.following.all())
        return JsonResponse({'message': "Unfollowed"})
    else:
        print("Following user", to_follow.username)
        following.following.add(to_follow)
        following.save()
        print(following.following.all())
        
        return JsonResponse({"message": "User followed"}, status=201)



