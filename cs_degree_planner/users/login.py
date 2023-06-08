"""


2023-06-08 - Josh Sawyer     : moved functionality from views.py to login module functions


"""

from django.contrib.auth import login


def create_account(form):
    """This method is used to create a new user account. In the case that the form
    sent is valid, then it will save the form and return True. Otherwise, if the form
    isn't valid, then it will return False indicating the account could not be created.

    Args:
        form (JEANZUserCreationForm): A form used for creating a user account

    Returns:
        bool: True or False
                -True: Account created successfully
                -False: Account not created
    """
    if form.is_valid():
        form.save(True) # commit defined as True, so will immediately store in the DB
        return True # Successful save and account creation
    else:
        if 'password2' in form.errors:
            form.errors['password1'] = form.errors['password2']
            del form.errors['password2']
  
    return False # Account not created

def login_account(request, form):
    """Logs a user into their account if the form submitted is valid. That is,
    if the username and password exist in the database.

    Args:
        request (_type_): the request sent to the calling view function
        form (JEANZUserLoginForm): The form submitted by the user to login

    Returns:
        bool: True or False
            -True: Account login successful
            -False: Account login unsuccessful
    """
    if form.is_valid(): # If Username and PW exist in the DB
        user = form.get_user()
        login(request, user)
        return True # Account login successful
    else:
        if (form.non_field_errors()):
            for error in form.non_field_errors():
                form.add_error('username', error)
    
    return False # Account login failed