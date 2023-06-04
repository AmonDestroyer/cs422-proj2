"""
Views that are related to courses and forecast generation (a.k.a., degree plan 
generation). There are functions that allow the user to 
    - edit their course history (`edit_courses`),
    - see what courses they have remaining in the CS major (`courses_left`),
    - edit their interests (`edit_interests`),
    - generate a new forecast (`new_forecast`),
    - save the forecast that was generated (`save_forecast`),
    - confirm that a forecast was saved (`save_confirmation`),
as well as helper functions
    - `add_forecast_model_data` creates the bridge tables between the Course
      model and Forecast model based on the forecast that was generated, 
    - `recursive_add_prereqs` recursively gets the prereqs of a course.

2023-05-22 - Josh Sawyer     : add dashboard view
2023-05-23 - Nathaniel mason : add edit_courses view and courses_left view
2023-05-24 - Nathaniel mason : update edit_courses view
2023-05-25 - Erin Stone      : add global perspectives and US requirements
2023-05-26 - Josh Sawyer     : added courses_left view and added @login_required for all views
2023-05-26 - Josh Sawyer     : form now loads saved general credits
2023-05-30 - Nathaniel Mason : added edit_interests and new_forecast view
2023-05-31 - Nathaniel Mason : edited new_forecast view
2023-06-02 - Josh Sawyer     : added recursive_add_prereqs function, also made it so courses already in form aren't added again
2023-06-03 - Nathaniel Mason : added save_forecast view
2023-06-03 - Zane Globus-O'Harra : add saved forecasts to the DB, add docstrings and file header description
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditCoursesForm, PresetForm
from django.contrib import messages
from .models import Course
from .forecast import remaining_requirements, categorize_courses, generate_forecast, list_forecast, split_forecast
from users.models import Profile, Forecast, Forecast_Has_Course
import ast


# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:login')
def index(request):
    return render(request, "forecast/dashboard.html")


@login_required(redirect_field_name='', login_url='users:login')
def edit_courses(request):
    """View that allows the user to dynamically edit the courses that they have
    taken, pulling their previous changes from the database and displaying
    them, as well as updating the database based on the user's added changes
    """
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

        general_credits = {'sci_cred': user_profile.sci_credits,
                           'soc_sci_cred': user_profile.ssci_credits,
                           'arts_letters_cred': user_profile.aal_credits,
                           'gp_cred': user_profile.gp_credits, 
                           'us_cred': user_profile.us_credits}
        
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
            saved_courses_taken = list(map(str, user_profile.courses_taken.values_list('id', flat=True)))
            user_courses_taken = form.cleaned_data.get('major_courses')
            if ((len(saved_courses_taken) > 0) or (len(user_courses_taken) > 0)):
                # once the form is valid, we must save their chosen courses in the DB
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

                # Get courses to remove (if anything was removed from list)
                courses_to_remove = [course for course in saved_courses_taken if course not in user_courses_taken]
                user_profile.courses_taken.remove(*courses_to_remove)

                for course_id in user_courses_taken:
                    try:
                        course_model = Course.objects.get(id=int(course_id))
                        
                        # Check if this course has been added yet, if it has,
                        # no need to add it again if not course_model in
                        # user_profile.courses_taken.all(): -- want to do
                        # something like this, but will fix later
                      
                        # once have course_model save in courses_taken
                        user_profile.courses_taken.add(course_model) 
                        print("found course_model with the id!")
                        
                        ## add any courses that are a prereq to this course ##
                        prereqs = recursive_add_prereqs(course_model) # returns a list of courses
                        user_profile.courses_taken.add(*prereqs) # add all the prereqs for this course to the user's courses_taken 
                        
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
                
                # next will need to take the user_courses_taken and save them
                # in the DB for that user. For now, just send messages back to
                # notify that Django obtained the data correctly
                messages.info(request, user_courses_taken)
                messages.info(request, user_sci)
                messages.info(request, user_soc_sci)
                messages.info(request, user_arts_lett)
                messages.info(request, user_gp)
                messages.info(request, user_us)

                messages.success(request, "Changes Saved Successfully!")
                
                return redirect('forecast:edit_courses')
            
            else:
                messages.error(request, "Nothing to save!")
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
    """View that displays a list of courses that the user needs to take to
    graduate with a CS Major. This list is updated based on the courses that
    the user has taken according to their user profile
    """
    user = request.user
    # values_list returns a query set, and flat=true flattens it to 1d
    courses_taken = request.user.profile.courses_taken.values_list('id', flat=True)
    courses_taken_set = set(courses_taken) # Convert query set to a regular set

    aal_taken = int(request.user.profile.aal_credits)
    ssci_taken = int(request.user.profile.ssci_credits)
    sci_taken = int(request.user.profile.sci_credits)
    gp_taken = int(request.user.profile.gp_credits)
    us_taken = int(request.user.profile.us_credits)

    remaining_courses = remaining_requirements(
        course_history=courses_taken_set, 
        aal=aal_taken,
        ssc=ssci_taken, 
        sc=sci_taken, 
        gp=gp_taken,
        us=us_taken,
    )
    remaining_courses = categorize_courses(remaining_courses)
        
    credits_remain = False    
    if (int(remaining_courses["CS Elective Requirements"][2][1][1]) > 0):
        credits_remain = True

    context = {
        "remaining_courses": remaining_courses, 
        "400CreditsRemaining": credits_remain
    }
    
    return render(request, "forecast/courses_left.html", context)


@login_required(redirect_field_name='', login_url='users:login')
def edit_interests(request):
    """View to allow the user to edit their interests, allowing forecasts to be
    tailored to fit what the user is most interested in. 
    """
    context = {}
    
    return render(request, "forecast/edit_interests.html", context)


@login_required(redirect_field_name='', login_url='users:login')
def new_forecast(request):
    """View that allows the user to generate a new forecast (called a 'degree 
    plan' in the HTML). This forecast is displayed to the user, with an option
    for the user to save their forecast, so that they will be able to retrieve
    it in the future.
    """
    if request.method != 'POST':
        form = PresetForm() 

        context = {'preset_form': form}
    
        return render(request, "forecast/new_forecast.html", context)
            
    else:
        form = PresetForm(request.POST)

        if form.is_valid():
            preset_choice = form.cleaned_data.get('preset_choice')
            # in future version, will need to take this preset choice into account and call the fxn
            # with the appropriate choice, but for now the default call
            # is used to get the generated forecast
            
            messages.success(request, f"Got your choice: {preset_choice}")

            # will need to call the function to get the forecast which is list of lists and then will send to template
            # either need to send to redirected new_forecast template page, 
            # or could use a separate forecast display template to show the result of the fxn
            courses_taken = request.user.profile.courses_taken.values_list('id', flat=True)
            courses_taken_set = set(courses_taken) # Convert query set to a regular set
            forecast = generate_forecast(course_history=courses_taken_set) # for now, just calls the fxn with default vals

            request.session['forecast_raw'] = forecast # store as a session variable so it can be easily gotten if it needs to be saved
            
            #fcst_to_display = list_forecast("F", 2023, forecast)
            #context = {'forecast_result': fcst_to_display}
            #return render(request, "forecast/forecast_display.html", context)

            fcst_to_display = split_forecast('F', 2023, forecast) #TODO user defined target term/year
            context = {
                'forecast_result': fcst_to_display,
            }
            return render(request, "forecast/forecast_display.html", context)
    

@login_required(redirect_field_name='', login_url='users:login')
def save_forecast(request):
    """If the user decides that they want to save their forecast, the data that
    was generated by the forecasting algorithm must be saved. This view creates
    a new Forecast model, attaches it to the user's Profile, and calls a
    function, `add_forecast_model_data()`, to add the course data to the
    forecast via bridge table
    """
    if request.method == 'POST':
        fcst_rslt_str = request.POST['forecast_result']
        # fcst rslt is str which is similar to: [['1','2','3'], ['4','5'], ...]
        
        # use ast.literal_eval to convert to list of lists
        forecast_data = ast.literal_eval(fcst_rslt_str) # retrieve the same forecast result data that was displayed
        # use json loads to make sure we get it as a list of lists and not a string

        # store as a session var in case want to show on the save confirmation template
        request.session['forecast_data'] = forecast_data

        ###### now save it in the DB #####
        user = request.user
        user_profile = Profile.objects.get(user=user) # get the user's profile
        forecast = Forecast(user=user_profile)
        forecast.save() # save the forecast model linked to the user's profile
        
        forecast_raw_data = request.session['forecast_raw'] # get the session data
        
        add_forecast_model_data(forecast_raw_data, forecast_data, forecast) # call helper function to generate the bridge tables

        return redirect('forecast:save_confirmation')


def add_forecast_model_data(forecast_raw_data, forecast_str_data, forecast_model):
    """A helper function that creates the bridge tables, `Forecast_Has_Course`,
    attaching courses to a forecast for a given year and term. The tables are
    saved in the database.
    """
    term_li = []
    year = 0
    course_in_term = []

    seasons_shorthand = {
        "Fall": 'F',
        "Winter": 'W',
        "Spring": 'S',
        "Summer": 'U',
    }

    general_credits = {
        'US': 100009,   # (US)
        'GP': 100010,   # (GP)
        'SCI': 100011,  # (>3)
        'SO': 100012,   # (>2)
        'AAL': 100013,  # (>1)
        'CRE': 100014,  # 4 credits
    }

    for term in forecast_str_data:
        term_li.append(term[0])
    
    for i, courses in enumerate(forecast_raw_data):
        # get the year and season that the user is taking these courses
        season = seasons_shorthand[term_li[i].split()[0]]
        year = int(term_li[i].split()[1])

        for course in courses:
            # get the courses they are taking in that term, and make a bridge table
            if isinstance(course, int): # the course is a int (course_id), and a valid course can be fetched from the DB
                course_model = Course.objects.get(id=course)
            else: # the course is a string, and needs to be parsed
                if "(US)" in course:
                    course_id = general_credits['US']
                elif "(GP)" in course:
                    course_id = general_credits['GP']
                elif "(>3)" in course:
                    course_id = general_credits['SCI']
                elif "(>2)" in course:
                    course_id = general_credits['SO']
                elif "(>1)" in course:
                    course_id = general_credits['AAL']
                elif "4 credits" in course:
                    course_id = general_credits['CRE']

                course_model = Course.objects.get(id=course_id)
            
            through_table = Forecast_Has_Course(
                forecast=forecast_model,
                course=course_model,
                year=year,
                term=season,
            )
            through_table.save()
    return

        
@login_required(redirect_field_name='', login_url='users:login')
def save_confirmation(request):
    """View to display a confirmation page confirming that the Forecast has
    been successfully saved in the database.
    """
    if request.method != 'POST': #only should be getting GET requests to this view fxn
        if 'forecast_data' in request.session:
            forecast_data = request.session['forecast_data']

            messages.success(request, f"Got the data and will save it in DB: {forecast_data}")
            context = {'saved_forecast': forecast_data}
            return render(request, "forecast/save_confirmation.html", context)
        else:
            messages.error(request, 'No forecast data found')
            context = {'saved_forecast': [[]]}
            return render(request, "forecast/save_confirmation.html", context)


def recursive_add_prereqs(course):
    """
    Recursive function that gets all the prereqs of a course 
    Must return a list of courses (-> List[Course])
    """
    if not course.has_prereq.exists():
        return [course] # Must return a list
    
    else:
        # Get all the prereqs for this course
        prereqs = course.has_prereq.all()
        sub_prereqs = []
            
        for prereq in prereqs:
            # Find all prereqs of this prereq
            sub_prereqs.extend(recursive_add_prereqs(prereq)) # Extend used to add each prereq item of the list returned from recurisve call     
            
        sub_prereqs.append(course) # Make sure to append this course as well since it's also a prereq
        return sub_prereqs
