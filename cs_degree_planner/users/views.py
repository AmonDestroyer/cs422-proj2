"""
users/views.py 

This file contains the views that are related to the user, specifically those
involving 
    - login 
    - account creation 
    - logout 
    - user account management 

2023-05-19 - Nathaniel mason : add create_user view
2023-05-22 - Josh Sawyer     : add login view
2023-05-24 - Josh Sawyer     : made it so form isn't refreshed when invalid
2023-05-26 - Josh Sawyer     : added update user account information (includes updating username and password)
2023-05-29 - Adam Case       : added update user account email
2023-06-08 - Josh Sawyer     : added login module and account management module

"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import JEANZUserCreationForm, JEANZUserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cs_degree_planner.decorators import anonymous_required

from .login import create_account, login_account
from .account_management import update_account


@anonymous_required
def index(request):
    """The view for the index, or home page. The home page displays information
    about the website, as well as a form to accept the user's login
    information. The home page and the login page are essentially the same,
    thus the redirection to the login view.
    """
    return redirect('users:login')


@anonymous_required
def create_user(request):
    """View to create a new user account, getting the form information from the
    `JEANZUserCreationForm`, and saving the user information in the database.
    This view also checks if there were any errors when the user created their
    account (e.g., invalid password, etc.), and handles those errors correctly.
    """
    # Form will be set with the POST data if it's a POST request
    # otherwise it'll be a blank UserCreationForm
    form = JEANZUserCreationForm(request.POST or None) 
    
    if create_account(form):
        messages.success(request, "Account created successfully!", extra_tags='success')
        return redirect('users:login')
    
    return render(request, 'users/create_user.html', {'userform': form})


@anonymous_required
def login_user(request):
    """This view logs in a user, getting their login information from the
    `JEANZUserLoginForm` and creating a session for that user. Create a blank
    form when the user is requesting the page
    """
    # If POST request, then create a form with the POST data
    # otherwise create a blank form
    form = JEANZUserLoginForm(data=request.POST or None) 
    
    if login_account(request, form): # If login successful
        return redirect('forecast:dashboard')

    return render(request, 'users/login.html', {'form': form})


@login_required(redirect_field_name='', login_url='users:login')
def update_account_information(request):
    """View to redirect the user to the correct account management pages, with
    the correct account management forms. For more information on each of these
    forms, see the docstrings in users/forms.py 
    """
    form_wrapper = [] # Create form wrapper so we can pass it by reference
    if (update_account(request, form_wrapper)):
        return redirect('users:update_account')
    
    return render(request, 'users/update_account.html', context=form_wrapper[0])


def logout_user(request):
    """Logout a user, clearing their session data. Then redirect to the home
    page (a.k.a., login page), with a logout successful message.
    """
    logout(request)
    messages.success(request, "Logout Successful!")
    return redirect('users:login')