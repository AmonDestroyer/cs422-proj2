"""
TODO: file description

2023-05-22 - Josh Sawyer     : add dashboard view
2023-05-23 - Nathaniel mason : add edit_courses view and courses_left view
2023-05-24 - Nathaniel mason : update edit_courses view
2023-05-25 - Erin Stone      : add global perspectives and US requirements
2023-05-26 - Josh Sawyer     : added courses_left view and added @login_required for all views
2023-05-26 - Josh Sawyer     : form now loads saved general credits

"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditCoursesForm
from django.contrib import messages
from .models import Course
from .forecast import remaining_requirements
from users.models import Profile

# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:login')
def index(request):
    return render(request, "forecast/dashboard.html")

@login_required(redirect_field_name='', login_url='users:login')
def edit_courses(request):
    user_model = request.user # user that is currently logged in
    user_profile = user_model.profile
    prev_choices = {}
    course_options = []
    
    if request.method != 'POST':
        form = EditCoursesForm()
        # user is just requesting the page
        # just display the form for them to choose options from
        # get course selections of the user and update the list with them
        course_selections = user_profile.courses_taken.all()

        general_credits = {'sci_cred': user_profile.sci_credits, 'soc_sci_cred': user_profile.ssci_credits, 'arts_letters_cred': user_profile.aal_credits, 'gp_cred': user_profile.gp_credits, 'us_cred': user_profile.us_credits}
        
        if(course_selections is not None):
            course_options = form.fields['major_courses'].choices

            for selection in course_selections:
                selection_id = selection.id # ex 210000
                for option_val, option_display in course_options:
                    if int(option_val) == selection_id: # found a match, set as selected for that list option
                        print('found a match for: ', selection_id)
                        prev_choices[str(selection_id)] = True

            print(prev_choices)
        
        for general in general_credits:
            if general_credits[general] is not None:
                form.fields[general].initial = general_credits[general]
    
    else:
        form = EditCoursesForm(request.POST)
        if form.is_valid():
            # once the form is valid, we must save their chosen courses in the DB
            user_courses_taken = form.cleaned_data.get('major_courses')
            print(user_courses_taken)
            user_sci = form.cleaned_data.get('sci_cred')
            user_soc_sci = form.cleaned_data.get('soc_sci_cred')
            user_arts_lett = form.cleaned_data.get('arts_letters_cred')
            user_gp = form.cleaned_data.get('gp_cred')
            user_us = form.cleaned_data.get('us_cred')

            # Each course model will have an id (e.g. 210000) so need to retrieve
            # the appropriate course models, then add those to the instance of the user profile model
            

            un = user_model.username
            print(un)

            for course_id in user_courses_taken:
                try:
                    course_model = Course.objects.get(id=int(course_id))
                    # once have course_model save in courses_taken
                    user_profile.courses_taken.add(course_model)
                    print("found course_model with the id!")
                except:
                    print("course_model not found")


            # update area of inquiry credits, 
            # which includes science credits, social science, arts and letters
            new_aoi = int(user_sci) + int(user_soc_sci) + int(user_arts_lett)
            current_aoi = user_profile.aoi_credits
            updated_aoi = current_aoi + new_aoi
            user_profile.aoi_credits = updated_aoi

            # update U.S. and global perspectives credits
            new_cultural = int(user_gp) + int(user_us)
            current_cultural = user_profile.cultural_credits
            updated_cultural = current_cultural + new_cultural
            user_profile.cultural_credits = updated_cultural

            # update total amount of credits
            new_credits = new_aoi + new_cultural
            current_total_credits = user_profile.total_credits
            updated_total = current_total_credits + new_credits 
            user_profile.total_credits = updated_total
            #update specific credit areas
            user_profile.aal_credits = int(user_arts_lett)
            user_profile.ssci_credits = int(user_soc_sci)
            user_profile.sci_credits = int(user_sci)
            user_profile.gp_credits = int(user_gp)
            user_profile.us_credits = int(user_us)
            
            
            user_profile.save()
            print("user prof saved with new changes!")
            
            # next will need to take the user_courses_taken and save them in the DB for that user
            # for now, just send messages back to notify that Django obtained the data correctly
            messages.info(request, user_courses_taken)
            messages.info(request, user_sci)
            messages.info(request, user_soc_sci)
            messages.info(request, user_arts_lett)
            messages.info(request, user_gp)
            messages.info(request, user_us)

            messages.success(request, "Changes Saved Successfully!")
            
            return redirect('forecast:edit_courses')
        else:
            for field in form:
                if field.errors:
                    print(field.errors) 
            messages.error(request, "Error While Attempting to Save Changes")
            
            return redirect('forecast:edit_courses')

    context = {'courseform': form,
               'course_options': course_options,
               'prev_choices': prev_choices}
    
    return render(request, "forecast/edit_courses.html", context)

@login_required(redirect_field_name='', login_url='users:login')
def courses_left(request):
    user = request.user
    # values_list returns a query set, and flat=true flattens it to 1d
    courses_taken = request.user.profile.courses_taken.values_list('id', flat=True)
    courses_taken_set = set(courses_taken) # Convert query set to a regular set

    aal_taken = int(request.user.profile.aal_credits)
    ssci_taken = int(request.user.profile.ssci_credits)
    sci_taken = int(request.user.profile.sci_credits)
    gp_taken = int(request.user.profile.gp_credits)
    us_taken = int(request.user.profile.us_credits)

    remaining_courses = remaining_requirements(course_history=courses_taken_set, aal=aal_taken, ssc=ssci_taken, sc=sci_taken, gp=gp_taken, us=us_taken)

    return render(request, "forecast/courses_left.html", {"remaining_courses": remaining_courses})
