"""
TODO: file description

2023-05-24 - Nathaniel mason : add EditCoursesForm and code to pull course options
2023-05-25 - Erin Stone      : add global perspectives and US requirements
2023-05-30 - Nathaniel Mason : added PresetForm for when a user will request a new forecast
2023-06-06 - Nathaniel Mason : edited PresetForm and options and added UserChoicesForm
2023-06-07 - Nathaniel Mason : small bug fix for edit_courses options
2023-06-08 - Josh Sawyer     : Moved EditCoursesForm to user app forms.py
"""

from django import forms
from .models import Keyword

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