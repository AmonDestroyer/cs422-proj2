"""
TODO: file description

2023-05-24 - Nathaniel mason : add EditCoursesForm and code to pull course options
2023-05-25 - Erin Stone      : add global perspectives and US requirements
2023-05-30 - Nathaniel Mason : added PresetForm for when a user will request a new forecast
"""

import os
import pandas as pd
from django import forms

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
    

PRESET_OPTIONS = [("16_cr", "16 credits per term"),
                  ("other", "Other preset test choice")
                  ]

class PresetForm(forms.Form):
    preset_choice = forms.ChoiceField(
        label='', choices=PRESET_OPTIONS, widget=forms.Select(
            attrs={'id': 'preset_choice', 'class': 'chzn-select'}))
