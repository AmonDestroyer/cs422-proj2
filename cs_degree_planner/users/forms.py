"""
users/forms.py 

Forms for user account creation, logging in, and user management. Specifically,
    - `JEANZUserCreationForm`, where the user creates an account,
    - `JEANZUserLoginForm`, where a user enters their account information to
      log in,
    - `UpdateUserNameForm`, part of the user management where a user can update
      their username,
    - `UserEmailChangeForm`, part of the user management where a user can
      update their email,
    - `UserNameChangeForm`, part of the user management where a user can update
      their first and last name.

2023-05-19 - Nathaniel mason : add JEANZUserCreationForm
2023-05-22 - Josh Sawyer     : add JEANZUserLoginForm
2023-05-25 - Erin Stone      : minor changes to usercreationform and loginform for styling
2023-05-29 - Adam Case       : added email change form
2023-05-30 - Nathaniel Mason : made it so username must be entered as lowercase (helps prevent case of Joe vs joe vs joE etc)
2023-06-03 - Zane Globus-O'Harra : Add file header description and class docstrings
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator

# For reference:
# https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
# Ref for validating: https://www.javatpoint.com/django-usercreationform


class JEANZUserCreationForm(UserCreationForm):
    """UserCreationForm is a ModelForm class that has password validation and
    can be saved Will create a custom version of UserCreationForm to add some
    other fields
    """
    username = forms.CharField(
        label='Username', 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'username', 
                'placeholder': 'USERNAME',
                'autofocus': 'True', 
                'oninput': 'this.value=this.value.toLowerCase()'
            }), 
        max_length=50,
        help_text="50 characters max and can contain letters, digits and @/./+/-/_"
    )
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(
            attrs={
                'class': 'fld', 
                'id': 'email', 
                'placeholder': 'EMAIL ADDRESS'
            }), 
        max_length=254, 
        help_text="254 characters max"
    )
    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'fld', 
                'id': 'password1', 
                'placeholder': 'PASSWORD'
            }), 
        min_length=8, 
        help_text="At least 8 characters"
    )
    password2 = forms.CharField( # 2nd password used to check and match the 1st one
        label="Confirm password", 
        widget=forms.PasswordInput(
            attrs={
                'class': 'fld', 
                'id': 'password2', 
                'placeholder': 'CONFIRM PASSWORD'
            }), 
        help_text="Enter same password to confirm"
    )
    first_name = forms.CharField(
        label="First Name", 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'first_name', 
                'placeholder': 'FIRST NAME'
            }), 
        max_length=50, 
        help_text="50 characters max"
    )
    last_name = forms.CharField(
        label="Last Name", 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'last_name', 
                'placeholder': 'LAST NAME'
            }), 
        max_length=50, 
        help_text="50 characters max"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)

    # methods for validating certain fields

    def clean_username(self):
        """Check that username has not been taken
        """
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("Username already taken")
        return username
    
    def clean_email(self):
        """Check that email has not been taken
        """
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email already taken")
        return email
    
    def clean_password2(self):
        """Check that passwords match
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2
    
    # first_name and last_name could theoretically be the same for multiple
    # users, so don't need to check if already used
    
    def save(self, commit = False):
        """Save user to database
        """
        user = User.objects.create_user(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']
        )
        if(commit):
            user.save()

        return user


class JEANZUserLoginForm(AuthenticationForm):
    """Form to get the user's username and password when they attempt to login
    """
    username = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'username', 
                'placeholder': 'USERNAME', 
                'autofocus': 'True'
            })
    ) # max_length matches length of username field given for account creation
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'fld', 
                'id': 'password', 
                'placeholder': 'PASSWORD'
            })
    ) # widget=forms.PasswordInput hides password as it is typed


class UpdateUserNameForm(UserChangeForm):
    """Form to allow the user to change their user name
    """
    class Meta:
        model = User
        fields = ('username',)
        labels = { 'username': 'New Username' } # What's displayed on the form
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = 'New Username'


class UserEmailChangeForm(forms.ModelForm):
    """Form to allow the user to change their email. 
    """
    email = forms.EmailField(
        label='New Email', 
        widget=forms.EmailInput(
            attrs={
                'class': 'fld', 
                'id': 'email', 
                'placeholder': 'NEW EMAIL'
            }), 
        max_length=254
    )

    class Meta:
        model = User
        fields = ['email']


class UserNameChangeForm(forms.ModelForm):
    """Form to allow the user to change their Name (first and last, not username)
    """
    first_name = forms.CharField(   # field for first name
        label="First Name", 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'first_name', 
                'placeholder': 'FIRST NAME'
            }), 
        max_length=50
    )
    last_name = forms.CharField(    # field for last name
        label="Last Name", 
        widget=forms.TextInput(
            attrs={
                'class': 'fld', 
                'id': 'last_name', 
                'placeholder': 'LAST NAME'
            }), 
        max_length=50
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name'] 

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial =  user.last_name
