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

"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import JEANZUserCreationForm, JEANZUserLoginForm, UpdateUserNameForm, UserEmailChangeForm, UserNameChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cs_degree_planner.decorators import anonymous_required


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
    if request.method != 'POST':
        form = JEANZUserCreationForm()
    else:
        form = JEANZUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Account created successfully!", extra_tags='success')
            form.save(True) # commit defined as True, so will immediately store in the DB
            return redirect('users:login')
        else:
            if 'password2' in form.errors:
                form.errors['password1'] = form.errors['password2']
                del form.errors['password2']

    context = {'userform': form}

    return render(request, 'users/create_user.html', context)


@anonymous_required
def login_user(request):
    """This view logs in a user, getting their login information from the
    `JEANZUserLoginForm` and creating a session for that user. Create a blank
    form when the user is requesting the page
    """
    if request.method == 'POST': # if the form has been submitted
        form = JEANZUserLoginForm(data=request.POST)
        if form.is_valid(): # Check for valid input, and then checks if a user exists with that username and password
            user = form.get_user() # get_user is a method of AuthenticationForm to get user_cache which was created during authentication (is_valid method)
            login(request, user) # https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.login
            return redirect('forecast:dashboard') # redirect to the dashboard page  
        else:
            if (form.non_field_errors()):
                for error in form.non_field_errors():
                    form.add_error('username', error)
    
    else: # if the form has not been submitted, the user is requesting the page
        form = JEANZUserLoginForm() # create a blank form

    return render(request, 'users/login.html', {'form': form})
    

def logout_user(request):
    """Logout a user, clearing their session data. Then redirect to the home
    page (a.k.a., login page), with a logout successful message.
    """
    logout(request)
    messages.success(request, "Logout Successful!")
    return redirect('users:login')


@login_required(redirect_field_name='', login_url='users:login')
def update_account_information(request):
    """View to redirect the user to the correct account management pages, with
    the correct account management forms. For more information on each of these
    forms, see the docstrings in users/forms.py 
    """
    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UpdateUserNameForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully!", extra_tags='success')
                return redirect('users:update_account')
   
        if 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!", extra_tags='success')
                return redirect('users:update_account')
            
        if 'update_email' in request.POST:
            email_form = UserEmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully!")
                return redirect('users:update_account')
    
        if 'update_name' in request.POST:
            name_form = UserNameChangeForm(request.user, request.POST, instance=request.user)
            if name_form.is_valid():
                name_form.save()
                messages.success(request, "Name updated successfully!")
                return redirect('users:update_account')
        
        if 'back' in request.POST:
            return redirect('users:update_account')
    
    forms = {
        "username_form": UpdateUserNameForm(),
        "password_form": PasswordChangeForm(request.user),
        "email_form": UserEmailChangeForm(),
        "name_form": UserNameChangeForm(request.user),
    }

    return render(request, 'users/update_account.html', context=forms)
