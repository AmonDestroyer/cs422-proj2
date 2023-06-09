"""
The URL patterns for the forecast model, with paths to 
    - the user's dashboard 
    - previously generated saved forecasts
    - a page to view the courses that a user still needs to take 
    - a page to generate a new degree plan 
    - a page to save a forecast 
    - a page to confirm that a forecast has been saved 

2023-05-22 - Josh Sawyer     : add dashboard url path
2023-05-30 - Nathaniel Mason : add edit_interests url path

"""

from django.urls import path

from . import views

app_name = "forecast"

urlpatterns = [
    # Health URL
    path("health", views.health),
    # ex: /forecast/dashboard
    path("dashboard", views.index, name="dashboard"),
    path("retrieve_forecast", views.dshbrd_retrieve_forecast, name="retrieve_forecast"),
    # ex: /forecast/edit_courses
    # path("edit_courses", views.edit_courses, name="edit_courses"),
    path("courses_left", views.courses_left, name="courses_left"),
    path("new_forecast", views.new_forecast, name="new_forecast"),
    path("save_forecast", views.save_forecast, name="save_forecast"),
    path("save_confirmation", views.save_confirmation, name="save_confirmation"),
]

