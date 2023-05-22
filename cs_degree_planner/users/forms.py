"""
TODO: file description

2023-05-19 - Nathaniel mason : add JEANZUserCreationForm

"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# For reference: https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
# Ref for validating: https://www.javatpoint.com/django-usercreationform

# UserCreationForm is a ModelForm class that has password validation and can be saved
# Will create a custom version of UserCreationForm to add some other fields
class JEANZUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Enter Username'}), max_length=50, help_text="50 characters max and can contain letters, digits and @/./+/-/_")
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Email'}), max_length=254, help_text="254 characters max")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'id': 'password1', 'placeholder': 'Enter Password'}), min_length=8, help_text="At least 8 characters")
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'id': 'password2', 'placeholder': 'Enter Password Again'}), help_text="Enter same password to confirm") # 2nd password used to check and match the 1st one
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'id': 'first_name', 'placeholder': 'Enter First Name'}), max_length=50, help_text="50 characters max")
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'id': 'last_name', 'placeholder': 'Enter Last Name'}), max_length=50, help_text="50 characters max")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)

    # methods for validating certain fields

    def clean_username(self):
        # Check that username has not been taken
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username = username)
        if new.count():
            raise ValidationError("User Already Used")
        return username
    
    def clean_email(self):
        # Check that email has not been taken
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Used")
        return email
    
    def clean_password2(self):
        # Check that passwords match
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords Do Not Match")
        return password2
    
    # first_name and last_name could theoretically be the same for multiple users, so don't need to check if already used
    
    def save(self, commit = False):
        # Save user to database
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