"""
TODO: file description

2023-05-21 - Zane Globus-O'Harra : add Profile model and add import to 
    get the User model. For in-depth look at the User model's fields and 
    methods, see:
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model
2023-05-23 - Zane Globus-O'Harra : add Forecast model, and imports from 
    forecast.models. The Forecast model needed to be defined here to 
    avoid circular imports. 
    Add credit counters to the Profile model... it is somewhat uncertain 
    how the separate credit tallies will be counted (for gened courses,
    major specific courses, etc.)
2023-05-29 - Zane Globus-O'Harra : Update Forecast model to have a 
    timestamp for when that forecast was generated.
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

    total_credits = models.IntegerField(default=0)  # user's total credits taken
    major_credits = models.IntegerField(default=0)  # credits towards the user's major

    #  FIXME: do we assume that the user is getting a BS?
    bs_credits = models.IntegerField(default=0)     # bachelor of science credits

    # area of inquiry credits: includes arts and letters, social science, and science credits
    aoi_credits = models.IntegerField(default=0)        
    # includes U.S. and global perspectives credits
    cultural_credits = models.IntegerField(default=0)

    #   areas of inquiry separated
    #arts and letters
    aal_credits = models.IntegerField(default=0)
    #social science
    ssci_credits = models.IntegerField(default=0)
    #science
    sci_credits = models.IntegerField(default=0)
    #   cultural literacy separated
    #global perspectives
    gp_credits = models.IntegerField(default=0)
    #us difference inequality agency
    us_credits = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Forecast(models.Model):
    """
    Forecast model class. Each forecast is associated with a user such 
    that a user can have multiple forecasts that they have generated. 

    This model needs to be in users.models because if it were in 
    forecast.models, there would be circular imports. 
    """
    # bridge table to courses
    courses_in_fc = models.ManyToManyField(Course)  
    user = models.ForeignKey(                       # Foreign Key to a user profile
        Profile,
        on_delete=models.CASCADE
    )
    # date and time the model was created, set to now upon model creation
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
