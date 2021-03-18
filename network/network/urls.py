
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("all", views.all, name="all"),
    path("react", views.react, name="react"),

    # API ROUTES
    path("posts", views.create_post, name="posts"),
    path("posts/<str:url_address>", views.display_posts, name="display_posts"),
    path("profile/posts/<str:url_address>", views.display_posts, name="display_posts"),
    path("follow/<str:profile_name>", views.follow, name="follow")
    # Old one
    # path("follow", views.follow, name="follow")

    # path("posts/<str:username>", views.display_posts, name="user_profile")
]

