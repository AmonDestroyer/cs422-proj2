"""
forecast/models.py 

Database table definitions for the Keywords, Courses, and Majors, as well as a
bridge table between Course and Major indicating if a course is required for
that major (e.g., CS 432 is a course in the CS major, but it is not required,
where CS 415 is required)

2023-05-23 - Zane Globus-O'Harra : Add Keyword, Course, Major, and
    OfferTimes models. The order that the models are written in matters.
    The Forecast model is defined in users.models to avoid circular
    imports. 
2023-05-24 - Zane Globus-O'Harra : Remove OfferedTimes table because it 
    was unecessary, added the information it held to the Course table. 
    Add a `Major_Has_Course` table that is bridged through, containing
    additional info about whether a course is required or elective for a
    Major.
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
        return self.keyword


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
    number = models.IntegerField(default=0)     # e.g., 415 or 422
    credits = models.IntegerField(default=0)    # number of credits

    # bridge table to get course prereqs
    has_prereq = models.ManyToManyField("self", symmetrical=False)     # prereqs that the course has - set symmetrical to false to avoid bidirectional relationship

    # bridge table to get course keywords
    has_kw = models.ManyToManyField(Keyword)    # what keywords are associated with this course

    # information about when a course is offered.
    fall = models.BooleanField(default=False);
    winter = models.BooleanField(default=False);
    spring = models.BooleanField(default=False);
    summer = models.BooleanField(default=False);
    every_year = models.BooleanField(default=False);
    every_year_odd = models.BooleanField(default=False);
    every_year_even = models.BooleanField(default=False);

    def __str__(self):
        """:return: string identifying the course by the subject code (e.g., 
       'CS') and the number
        """
        return f"{self.subject} {self.number}"

    @property 
    def full_name(self):
        """:return: string identifying the course by the subject code (e.g., 
       'CS'), the number, and the full course name 
        """
        return f"{self.subject} {self.number} {self.name}"


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
    courses = models.ManyToManyField(
        Course,
        through="Major_Has_Course"
    )
    
    def __str__(self):
        """:return: string identifying the major by its long name
        """
        return self.name 


class Major_Has_Course(models.Model):
    """
    Because we need to know if a course in a major is required or not 
    (an elective), we need a bridge table to add the `is_required` info.
    """
    course = models.ForeignKey(     # ForeighnKey to course
        Course,
        on_delete=models.CASCADE
    )
    major = models.ForeignKey(      # ForeignKey to major
        Major,
        on_delete=models.CASCADE
    )
    is_required = models.BooleanField(default=False) # is the course required or elective?

    def __str__(self):
        """:return: string identifying the table row by the related major's
        name and the course's short name
        """
        return f"Major {str(self.major)} Has Course {str(self.course)}"
