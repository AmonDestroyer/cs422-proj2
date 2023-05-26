"""
TODO: Custom django admin command to load UO courses into the database 

2023-05-25 - Josh Sawyer : Created course loading class

"""

from django.core.management.base import BaseCommand, CommandError
from forecast.models import Course, Keyword
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
import pandas as pd

class Command(BaseCommand):
    help = """Imports courses from an Excel file.
          The excel file must contain the following fields: 
          id, subject, number, credits, term, annual, name, required, and keywords
          """
    
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to excel file")
    
    def handle(self, *args, **options):
        # Get the path to the excel sheet (that was provided by the user)
        file = options['file_path']
        
        try:
            workbook = load_workbook(file)
            sheet = workbook.active
            
            ID = 0
            NAME = 7
            SUBJECT = 1
            NUMBER = 2
            PREREQ = 3
            CREDITS = 4
            TERM = 5
            ANNUAL = 6
            
            courses = []

            for row in sheet.iter_rows(min_row=2, values_only=True):
                terms = {'F': False, 'W': False, 'S': False}
                for term in terms:
                    if (row[TERM] is not None):
                        if term in row[TERM]:
                            terms[term] = True
                
                every_year = False
                if type(row[ANNUAL]) is type(bool):
                    every_year = True
                
                if row[ID] != None:
                  course = Course(
                      id = int(row[ID]),
                      name = str(row[NAME]),
                      subject = row[SUBJECT],
                      number = row[NUMBER],
                      credits = row[CREDITS],
                      fall = terms['F'],
                      winter = terms['W'],
                      spring = terms['S'],
                      every_year = every_year
                  )
                
                  courses.append(course)
            
            Course.objects.bulk_create(courses)
            
            self.stdout.write(f"Courses added, now adding prereqs.")
            
            # Courses have now been created, now add prereqs in
            for row in sheet.iter_rows(min_row=2, values_only=True):
                prereqs = row[PREREQ]
                if prereqs is not None:
                    prereq_ids = []
                    if type(prereqs) is str:
                        prereqs_list = row[PREREQ].split(', ')
                        for prereq in prereqs_list:
                            prereq_ids.append(int(prereq))
                    else:
                        if (int(prereqs) != 0):
                            prereq_ids.append(int(prereqs))
                  
                    course = Course.objects.get(id=row[ID])
                    
                    for prereq_id in prereq_ids:
                        try:
                            prereq_course = Course.objects.get(id=prereq_id)
                            course.has_prereq.add(prereq_course)
                            
                        except Course.DoesNotExist:
                            self.stderr.write(f"Course doesn't exist: prereq_id [{prereq_id}]")
            
            self.stdout.write(f"Prereqs added, course import now complete.")
            
        except InvalidFileException:
            self.stderr.write("Invalid Excel file.")
