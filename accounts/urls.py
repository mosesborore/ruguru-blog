from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("new", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.user_profile, name="profile")

]
