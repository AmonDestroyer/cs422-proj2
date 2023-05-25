"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard view
2023-05-23 - Nathaniel mason : add edit_courses view and courses_left view
2023-05-24 - Nathaniel mason : update edit_courses view
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditCoursesForm
from django.contrib import messages

# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:index')
def index(request):
    return render(request, "forecast/dashboard.html")


def edit_courses(request):
    if request.method != 'POST':
        form = EditCoursesForm()
        # user is just requesting the page
        # just display the form for them to choose options from
    
    else:
        form = EditCoursesForm(request.POST)
        if form.is_valid():
            # once the form is valid, we must save their chosen courses in the DB
            user_courses_taken = form.cleaned_data.get('major_courses')
            user_sci = form.cleaned_data.get('sci_cred')
            user_soc_sci = form.cleaned_data.get('soc_sci_cred')
            user_arts_lett = form.cleaned_data.get('arts_letters_cred')
            
            # next will need to take the user_courses_taken and save them in the DB for that user
            # for now, just send messages back to notify that Django obtained the data correctly
            messages.info(request, user_courses_taken)
            messages.info(request, user_sci)
            messages.info(request, user_soc_sci)
            messages.info(request, user_arts_lett)

            messages.success(request, "Changes Saved Successfully!")
            
            return redirect('forecast:edit_courses')
        else:
            for field in form:
                if field.errors:
                    print(field.errors) 
            messages.error(request, "Error While Attempting to Save Changes")
            
            return redirect('forecast:edit_courses')

    context = {'courseform': form}
    
    return render(request, "forecast/edit_courses.html", context)


def courses_left(request):
    return render(request, "forecast/courses_left.html")
