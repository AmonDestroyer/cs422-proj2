"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard url path
2023-05-30 - Nathaniel Mason : add edit_interests url path

"""

from django.urls import path

from . import views

app_name = "forecast"

urlpatterns = [
    # ex: /forecast/dashboard
    path("dashboard", views.index, name="dashboard"),
    # ex: /forecast/edit_courses
    path("edit_courses", views.edit_courses, name="edit_courses"),
    path("courses_left", views.courses_left, name="courses_left"),
    path("edit_interests", views.edit_interests, name="edit_interests"),
    path("new_forecast", views.new_forecast, name="new_forecast"),
    path("save_forecast", views.save_forecast, name="save_forecast"),
    path("save_confirmation", views.save_confirmation, name="save_confirmation"),
]

