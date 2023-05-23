"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard view

"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:index')
def index(request):
    return render(request, "dashboard.html")
