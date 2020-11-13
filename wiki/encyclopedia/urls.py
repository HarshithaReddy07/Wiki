from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),
    path("create", views.create, name="create"),
    path("wiki/", views.random_Page, name="random"),
    path("edit/<str:title>", views.edit, name="edit")
]
