from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexListView.as_view(), name="home"),
    path("about-me", views.about_me, name='about_me'),
    path("category/<slug:slug>", views.CategoryList.as_view(), name="category-list"),
    path('article/<slug:slug>/',
         views.post_detail, name='article_details'),
    
]
