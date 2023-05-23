"""
TODO: file description

2023-05-19 - Nathaniel mason : add create_user view
2023-05-22 - Josh Sawyer     : add login view

"""

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import JEANZUserCreationForm, JEANZUserLoginForm
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "users/index.html")

def create_user(request):
    if request.method != 'POST':
        form = JEANZUserCreationForm()
    else:
        form = JEANZUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Account Created Successfully!")
            form.save(True) # commit defined as True, so will immediately store in the DB
            return redirect('users:index')
        else:
            for field in form:
                if field.errors:
                    print(field.errors) 
            messages.error(request, "User information not valid")
            return redirect('users:create_user')

    context = {'userform': form}

    return render(request, 'users/create_user.html', context)


def login_user(request):
    if request.method == 'POST': # if the form has been submitted
        form = JEANZUserLoginForm(data=request.POST)
        if form.is_valid(): # Check for valid input, and then checks if a user exists with that username and password
            user = form.get_user() # get_user is a method of AuthenticationForm to get user_cache which was created during authentication (is_valid method)
            login(request, user)
            return redirect('forecast:dashboard') # redirect to the dashboard page  
        else:
            print(form.errors)
            messages.error(request, "User information not valid")
            return redirect('users:login')
    else: # if the form has not been submitted, the user is requesting the page
        form = JEANZUserLoginForm() # create a blank form
        return render(request, 'users/login.html', {'form': form})
    
    
def logout_user(request):
    logout(request)
    messages.success(request, "Logout Successful!")
    return redirect('users:index')