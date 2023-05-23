"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard url path

"""

from django.urls import path

from . import views

app_name = "forecast"

urlpatterns = [
    # ex: /dashboard/
    path("", views.index, name="dashboard"),
]

