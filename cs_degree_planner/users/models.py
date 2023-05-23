"""
TODO: file description

2023-05-21 - Zane Globus-O'Harra : add Profile model and add import to 
    get the User model. For in-depth look at the User model's fields and 
    methods, see:
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model
2023-05-23 - Zane Globus-O'Harra : add Forecast model, and imports from 
    forecast.models. The Forecast model needed to be defined here to 
    avoid circular imports. 
"""

from django.db import models
from django.contrib.auth.models import User
from forecast.models import Major, Course, Keyword


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
    major = models.ManyToManyField(Major)           # bridge table to majors
    courses_taken = models.ManyToManyField(Course)  # bridge table to courses
    interests = models.ManyToManyField(Keyword)     # bridge table to keywords

    def __str__(self):
        return self.user.username


class Forecast(models.Model):
    """
    Forecast model class. Each forecast is associated with a user such 
    that a user can have multiple forecasts that they have generated. 

    This model needs to be in users.models because if it were in 
    forecast.models, there would be circular imports. 
    """
    courses_in_fc = models.ManyToManyField(Course)  # bridge table to courses
    user = models.ForeignKey(                       # related to a user profile
        Profile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user
