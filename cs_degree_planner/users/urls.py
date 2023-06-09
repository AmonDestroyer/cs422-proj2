"""
The URL paths for 
    - the root (homepage) of the webapp
    - the account creation form
    - the login form 
    - the logout page 
    - user account management, including 
        - the general account update page, where the user can select which part
          of their account they want to update 
        - the edit courses page, where the user can edit their course history 
        - the edit interests page, where the user can edit their interests

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
    
    # Account mangement views
    path("update-account", views.update_account_information, name='update_account'),
    path("edit_courses", views.edit_courses, name="edit_courses"),
    path("edit_interests", views.edit_interests, name="edit_interests"),
]

