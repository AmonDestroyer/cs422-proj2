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
    keyword = models.CharField(max_length=100)  # the name of the keyword
    desc = models.CharField(max_length=100)     # the description of the keyword 

    def __str__(self):
        return self.kw_name


class Course(models.Model):
    """
    A Course is defined by its subject and number. Some (subject, number)
    combinations are repeated, so a course_name is needed. Some courses 
    also have a prerequisite(s), so we need a bridge table to get those
    prerequisites.
    """
    # attributes
    name = models.CharField(max_length=100)     # e.g., 'Software Methodologies'
    subject = models.CharField(max_length=10)   # e.g., 'CS' or 'MATH'
    number = models.IntegerField(default=0)              # e.g., 415 or 422
    credits = models.IntegerField(default=0)             # number of credits

    # bridge table to get course prereqs
    has_prereq = models.ManyToManyField("self")     # prereqs that the course has
    is_prereq_for = models.ManyToManyField("self")  # courses this course is a prereq for (NOTE: might not be necessary because it is a repetition of info?)

    # bridge table to get course keywords
    has_kw = models.ManyToManyField(Keyword)    # what keywords are associated with this course

    def __str__(self):
        return self.course_name


class Major(models.Model):
    """
    A Major is defined by a the name of the major, as well as a the 
    shortform subject. A minor is similar to a major, but with a reduced 
    set of classes, and is indicated by the `is_minor` indicator.
    """
    # attributes
    name = models.CharField(max_length=100)         # e.g., 'Computer Science'
    subject = models.CharField(max_length=10)       # e.g., 'CS' or 'MATH'
    desc = models.CharField(max_length=512)         # a longform description of the major
    is_minor = models.BooleanField(default=False)   # indicate if this defines a minor instead

    # bridge table to get the courses in a major
    has_course = models.ManyToManyField(Course)
    
    def __str__(self):
        return self.name 


class OfferTimes(models.Model):
    """
    A table to indicate when classes are offered, whether in Fall, 
    Winter, Spring, or Summer, and whether they are offered yearly, or 
    every other year (odd or even years).
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
