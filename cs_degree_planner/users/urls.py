"""
TODO: file description

2023-05-19 - Nathaniel mason : add create_user url path

"""

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    # ex: /users/
    path("", views.index, name="index"),
    # ex: /users/createuser/
    path("create_user/", views.create_user, name="create_user"),
]

