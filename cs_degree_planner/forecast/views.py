"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard view
2023-05-23 - Nathaniel mason : add edit_courses view and courses_left view
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:index')
def index(request):
    return render(request, "forecast/dashboard.html")


def edit_courses(request):
    return render(request, "forecast/edit_courses.html")


def courses_left(request):
    return render(request, "forecast/courses_left.html")
