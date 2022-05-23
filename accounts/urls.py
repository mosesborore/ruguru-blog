from django.urls import path

from . import views

urlpatterns = [
    path("new", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.user_profile, name="profile"),
]
