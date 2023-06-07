"""
TODO: file description

2023-05-24 - Nathaniel mason : add EditCoursesForm and code to pull course options
2023-05-25 - Erin Stone      : add global perspectives and US requirements
2023-05-30 - Nathaniel Mason : added PresetForm for when a user will request a new forecast
2023-06-06 - Nathaniel Mason : edited PresetForm and options and added UserChoicesForm
"""

import os
import pandas as pd
from django import forms
from .models import Keyword

current_dir = os.path.dirname(__file__)
file_path = current_dir + '/recommendcourses.xlsx'

df = pd.read_excel(file_path, index_col="id")

COURSE_OPTIONS = []

for index, row in df.iterrows():
    list_option_display = str(row['subject']) + ' ' + str(row['number']) + ' ' + str(row['name'])
    list_option_val = str(index)
    #print(list_option)
    list_option = (list_option_val, list_option_display)
    COURSE_OPTIONS.append(list_option)

#print(COURSE_OPTIONS)

# create multiple select Django form using the array of options
class EditCoursesForm(forms.Form):
    major_courses = forms.MultipleChoiceField(
        label='', choices=COURSE_OPTIONS, widget=forms.SelectMultiple(
            attrs={'id': 'course_select','class': 'chzn-select'}), required=False)
    
    sci_cred = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'science_cred', 'class': 'input-number', 
                'type': 'number', 'value': '0', 'min': '0'}))
    
    soc_sci_cred = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'social_science_cred', 'class': 'input-number', 
               'type': 'number', 'value': '0', 'min': '0'}))
    
    arts_letters_cred = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'arts_letters_cred', 'class': 'input-number', 
               'type': 'number', 'value': '0', 'min': '0'}))

    gp_cred = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'gp_cred', 'class': 'input-number', 
               'type': 'number', 'value': '0', 'min': '0'}))

    us_cred = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'us_cred', 'class': 'input-number', 
               'type': 'number', 'value': '0', 'min': '0'}))
    

CREDIT_OPTIONS = [(20, "20 credits per term"),
                  (16, "16 credits per term"),
                  (12, "12 credits per term"),
                  (8, "8 credits per term"),
                  (4, "4 credits per term"),
                  ]

TERM_OPTIONS = [("F", "Fall"),
                  ("W", "Winter"),
                  ("S", "Spring"),
                  #("U", "Summer"), # not working with the generate_forecast fxn rn
                  ]

YEAR_OPTIONS = [(2023, "2023"),
                  (2024, "2024"),
                  (2025, "2025"),
                  (2026, "2026"),
                  (2027, "2027"),
                  (2028, "2028"),
                  (2029, "2029"),
                  (2030, "2030"),
                  (2031, "2031"),
                  (2032, "2032"),
                  (2033, "2033"),
                  (2034, "2034"),
                  ]


class PresetForm(forms.Form):
    credits_choice = forms.ChoiceField(
        label='', choices=CREDIT_OPTIONS, widget=forms.Select(
            attrs={'id': 'credits_choice', 'class': 'chzn-select'}))
    
    term_choice = forms.ChoiceField(
        label='', choices=TERM_OPTIONS, widget=forms.Select(
            attrs={'id': 'term_choice', 'class': 'chzn-select'}))
    
    year_choice = forms.ChoiceField(
        label='', choices=YEAR_OPTIONS, widget=forms.Select(
            attrs={'id': 'year_choice', 'class': 'chzn-select'}))


# Alternative form where user would type in field values instead of choosing presets
class UserChoicesForm(forms.Form):
    credits_per_term = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'cred_per_term', 'class': 'input-number', 
               'type': 'number', 'value': '16', 'min': '0'}))
    
    target_term = forms.CharField(max_length=6, help_text="e.g. Fall", label='', widget=forms.TextInput(
        attrs={'id': 'target_term', 'class': 'input-text', 
               'type': 'text'}))
    
    target_year = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={'id': 'target_year', 'class': 'input-number', 
               'type': 'number', 'value': '', 'min': '2023'}))


INTEREST_OPTIONS = []

keyword_arr = list(Keyword.objects.all())

for option in keyword_arr:
    list_option = (option.keyword, option.keyword)
    INTEREST_OPTIONS.append(list_option)

print('INTEREST_OPTIONS:')
print(INTEREST_OPTIONS)

class EditInterestsForm(forms.Form):
    user_interests = forms.MultipleChoiceField(
        label='', choices=INTEREST_OPTIONS, widget=forms.SelectMultiple(
            attrs={'id': 'interest_select','class': 'chzn-select'}), required=False)