"""
TODO: file description

2023-05-23 - Zane Globus-O'Harra : Add Keyword, Course, Major, and
    OfferTimes models. The order that the models are written in matters.
    The Forecast model is defined in users.models to avoid circular
    imports. 
"""

from django.db import models


class Keyword(models.Model):
    """
    A Keyword is a word that is related to a class. For example, CS 422,
    Software Methodologies I, might have the keywords "software", 
    "software design", "group projects", etc. A user can select the
    keywords that interest them so that the forecasting algorithm can 
    tailor a schedule to their interests.
    """
    # attributes
    kw_name = models.CharField(max_length=100)
    kw_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.kw_name


class Course(models.Model):
    # TODO: docstring
    """
    """
    # attributes
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()

    # bridge table to get course prereqs
    has_prereq = models.ManyToManyField("self")
    is_prereq_for = models.ManyToManyField("self")

    # bridge table to get course keywords
    has_kw = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.course_name


class Major(models.Model):
    # TODO: docstring
    """
    """
    # attributes
    major_name = models.CharField(max_length=100)
    major_desc = models.CharField(max_length=512)
    is_minor = models.BooleanField(default=False)

    # bridge table to get the courses in a major
    has_course = models.ManyToManyField(Course)
    
    def __str__(self):
        return self.name 


class OfferTimes(models.Model):
    # TODO: docstring
    """
    """
    # the offer times are identified by the course that is offered
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE
    )
    # attributes
    fall = models.BooleanField(default=False);
    winter = models.BooleanField(default=False);
    spring = models.BooleanField(default=False);
    summer = models.BooleanField(default=False);
    every_year = models.BooleanField(default=False);
    every_year_odd = models.BooleanField(default=False);
    every_year_even = models.BooleanField(default=False);

    def __str__(self):
        return self.course
