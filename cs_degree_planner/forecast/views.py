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
2023-06-04 - Josh Sawyer     : fixed bug with cs electives + added pop up for saved changes + added reset/restore course history button
2023-06-05 - Zane Globus-O'Harra : add helper fxn to get a list of creation times of a user's forecasts and a fxn to get a forecast based on a creation time
2023-06-06 - Josh Sawyer     : fixed generic credits not being saved when there was nothing in the course history drop down
2023-06-06 - Nathaniel Mason : edited new_forecast view to pass user's choices to generate_forecast()
"""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PresetForm
from django.contrib import messages
from .models import Course, Keyword
from .forecast import remaining_requirements, categorize_courses, generate_forecast, list_forecast, split_forecast
from users.models import Profile, Forecast, Forecast_Has_Course
import ast
from datetime import datetime
from django.utils.timezone import make_aware
import pytz

def get_user_profile(user):
    """helper function to easily get a user's profile
    """
    return Profile.objects.get(user=user)

def health(request):
    return HttpResponse('')

# login is required to see the dashboard
# if user is not logged in, redirect them to the index/landing page 
@login_required(redirect_field_name='', login_url='users:login')
def index(request):
    # need to retrieve all timestamps for forecasts associated with the current user
    fcst_timestamps = get_forecast_timestamps(request)

    timestamp_strs = []
    for timestamp in fcst_timestamps:
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        timestamp_strs.append(timestamp_str)

    ts_raw_display = zip(timestamp_strs, fcst_timestamps)

    context = {'ts_raw_and_display': ts_raw_display,
               }

    return render(request, "forecast/dashboard.html", context)


@login_required(redirect_field_name='', login_url='users:login')
def dshbrd_retrieve_forecast(request):
    timestamp_from_user = request.POST['timestamp_str']
    
    # timestamp = timezone.make_aware(
    timestamp_naive = datetime.strptime(timestamp_from_user, '%Y-%m-%d %H:%M:%S.%f')
    timestamp = make_aware(timestamp_naive, timezone=pytz.timezone('UTC'))
    print("TIMESTAMP", timestamp)

    pst_timezone = pytz.timezone('US/Pacific')
    timestamp_pst = timestamp.astimezone(pst_timezone)
    ts_pst_str = timestamp_pst.strftime('%B %d, %Y, %I:%M %p')
    
    fcst = get_forecast_from_timestamp(request, timestamp)
    split_fcst = None

    if(fcst is not None):
        # fcst is the forecast model object, but need to split it
        split_fcst = fcst.split_forecast()

    #print("PRINT SPLIT_FCST", split_fcst)
    context = {'selected_timestamp': ts_pst_str,
            'dshbrd_retrieval': True,
            'forecast_result': split_fcst}
    #messages.info(request, "Selected timestamp: " + timestamp_from_user)

    return render(request, "forecast/forecast_display.html", context)


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
    
    # Used to determine if the second CS credit option is still available
    credits_remain = False    
    if (len(remaining_courses["CS Elective Requirements"]) > 0 and len(remaining_courses["CS Elective Requirements"][2][1]) > 0):
        credits_remain = True

    context = {
        "remaining_courses": remaining_courses, 
        "400CreditsRemaining": credits_remain
    }
    
    return render(request, "forecast/courses_left.html", context)


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
            credits_choice = form.cleaned_data.get('credits_choice')
            term_choice = form.cleaned_data.get('term_choice')
            year_choice = form.cleaned_data.get('year_choice')

            credits_choice = int(credits_choice)
            term_choice = str(term_choice)
            year_choice = int(year_choice)
            
            messages.success(request, f"Got your choices: {credits_choice}, {term_choice}, {year_choice}")

            # will need to call the function to get the forecast which is list of lists and then will send to template
            # either need to send to redirected new_forecast template page, 
            # or could use a separate forecast display template to show the result of the fxn
            courses_taken = request.user.profile.courses_taken.values_list('id', flat=True)
            courses_taken_set = set(courses_taken) # Convert query set to a regular set
            
            interests = set(request.user.profile.interests.values_list('keyword', flat=True))
            print(interests)
            forecast = generate_forecast(course_history=courses_taken_set, max_credits_per_term=credits_choice, target_term=term_choice, target_year=year_choice, interests=interests)

            request.session['forecast_raw'] = forecast # store as a session variable so it can be easily gotten if it needs to be saved

            fcst_to_display = split_forecast(term_choice, year_choice, forecast)
            context = {
                'forecast_result': fcst_to_display,
                'dshbrd_retrieval': False,
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
        print("Forecast Save Time:", forecast.time_created)
        print('Saved the forecast!')
        
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


def get_forecast_timestamps(request):
    """Return a list of the timestamps that are generated for forecasts. Return
    all of the timestamps associated with one user.
    """
    profile = get_user_profile(request.user)

    try:
        # get forecasts related to the user's profile and order by creation time
        forecasts = Forecast.objects.filter(user=profile).order_by('time_created')   
        forecast_li = list(forecasts)
    except:
        print(f"user {request.user} does not have any saved forecasts!")
        forecast_li = []

    timestamp_li = []

    for fc in forecast_li:
        timestamp_li.append(fc.time_created)
    
    return timestamp_li


def get_forecast_from_timestamp(request, timestamp):
    """Return a forecast for a user based on a given time stamp (creation time)
    """
    profile = get_user_profile(request.user)
    try:
        # get forecasts related to a user's profile, filter for the time, and get the actual model object
        forecast = Forecast.objects.filter(user=profile).filter(time_created=timestamp).first()                         
    except:
        print(f"user {request.user} does not have any saved forecasts!")
        forecast = None

    return forecast
