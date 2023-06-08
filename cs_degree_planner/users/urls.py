"""
TODO: file description

2023-05-19 - Nathaniel mason : add create_user url path
2023-05-22 - Josh Sawyer     : add login url path

"""

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    # ex: /users/
    path("", views.index, name="index"),
    # ex: /users/createuser/
    path("create-user/", views.create_user, name="create_user"),
    # ex: /users/login/
    path("login/", views.login_user, name="login"),
    # ex: /users/logout/
    path("logout/", views.logout_user, name="logout"),
    
    path("update-account", views.update_account_information, name='update_account'),
    
    path("edit_courses", views.edit_courses, name="edit_courses"),
]

