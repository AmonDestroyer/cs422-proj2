#!/bin/bash

python manage.py migrate
python manage.py import_courses forecast/recommendcourses.xlsx
python manage.py runserver "0.0.0.0:8080"