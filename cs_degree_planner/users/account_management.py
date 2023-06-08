"""


2023-06-08 - Josh Sawyer     : moved functionality from views.py to login account_management functions



"""

from .forms import UpdateUserNameForm, UserEmailChangeForm, UserNameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def update_account(request, form_wrapper):
    """Updates a user's personal information. This includes updating the username,
    password, email, and name. In the case that the form submitted is not valid, an update
    will not be done.

    Args:
        request (_type_): request that was sent to the calling view function
        form_wrapper (_type_): a wrapper that is used to pass by reference the forms

    Returns:
        bool: True or False
            -True: Account update successful or back button pressed
            -False: Account update unsuccessful or GET request
    """
    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UpdateUserNameForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully!", extra_tags='success')
                return True
            else:
                messages.error(request, "Username already taken", extra_tags='fail')
            
   
        if 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!", extra_tags='success')
                return True
            else:
                messages.error(request, "Password update failed!", extra_tags='fail')
              
        if 'update_email' in request.POST:
            email_form = UserEmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully!")
                return True
    
        if 'update_name' in request.POST:
            name_form = UserNameChangeForm(request.user, request.POST, instance=request.user)
            if name_form.is_valid():
                name_form.save()
                messages.success(request, "Name updated successfully!")
                return True
        
        if 'back' in request.POST:
            return True

    forms = {
        "username_form": UpdateUserNameForm(),
        "password_form": PasswordChangeForm(request.user),
        "email_form": UserEmailChangeForm(),
        "name_form": UserNameChangeForm(request.user),
    }
    
    form_wrapper.append(forms)
    
    return False
  

