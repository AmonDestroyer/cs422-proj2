"""
TODO: file description

2023-05-21 - Zane Globus-O'Harra : add Profile model and add import to 
    get the User model. For in-depth look at the User model's fields and 
    methods, see:
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model

"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model class associated with a single user. The User model is 
    'private' while the Profile model is 'public', and is accessed by 
    the other models. The User model only interfaces with the Profile 
    model and some of the login functionality.
    """

    # 1:1 foreign key to the user model
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username
