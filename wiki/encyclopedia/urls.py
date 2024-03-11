from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("random", views.show_random_article, name="random_article"),
    path("search", views.find_article, name="find_article"),
    path("<str:topic>", views.load_article, name="load_article"),
    path("<str:topic>/edit", views.edit_article, name="edit_article")
]
