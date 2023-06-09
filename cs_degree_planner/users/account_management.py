"""


2023-06-08 - Josh Sawyer     : moved functionality from views.py to login account_management functions



"""

from .forms import UpdateUserNameForm, UserEmailChangeForm, UserNameChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import EditCoursesForm, EditInterestsForm
from forecast.models import Course, Keyword

def update_account(request, form_wrapper):
    """Updates a user's personal information. This includes updating the username,
    password, email, and name. In the case that the form submitted is not valid, an update
    will not be done.

    Args:
        request (_type_): request that was sent to the calling view function
        form_wrapper (_type_): a wrapper that is used to pass by reference the forms

    Returns:
        bool: True or False
            -True: Account update successful or back button pressed
            -False: Account update unsuccessful or GET request
    """
    if request.method == 'POST':
        if 'update_username' in request.POST:
            username_form = UpdateUserNameForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Username updated successfully!", extra_tags='success')
                return True
            else:
                messages.error(request, "Username already taken", extra_tags='fail')
            
   
        if 'update_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!", extra_tags='success')
                return True
            else:
                messages.error(request, "Password update failed!", extra_tags='fail')
              
        if 'update_email' in request.POST:
            email_form = UserEmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Email updated successfully!")
                return True
    
        if 'update_name' in request.POST:
            name_form = UserNameChangeForm(request.user, request.POST, instance=request.user)
            if name_form.is_valid():
                name_form.save()
                messages.success(request, "Name updated successfully!")
                return True
        
        if 'back' in request.POST:
            return True

    forms = {
        "username_form": UpdateUserNameForm(),
        "password_form": PasswordChangeForm(request.user),
        "email_form": UserEmailChangeForm(),
        "name_form": UserNameChangeForm(request.user),
    }
    
    form_wrapper.append(forms)
    
    return False
  

def update_user_profile(request, user_section, context):
    """Handles the editing of a user's course history or the user's interests. 

    Args:
        request: request that was sent to the calling view function
        user_section (str): Either 'major_courses' or 'user_interests'
                - 'major_courses': indicates that the user is editing their course history
                - 'user_interests': indicates that the user is editing their interests
        context (dict): context is a list that is passed by reference, and is used in the calling function to render the page with the appropriate context

    Returns:
        bool: True or False
                -True: Indicates to the view function to redirect to the same page
                -False: Indicates to the view function to render the page with the appropriate context
    """
    
    user_model = request.user # user that is currently logged in
    user_profile = user_model.profile
    prev_choices = {}
    options = []
    reset = False
    course_section = (user_section == 'major_courses')
    
    if request.method != 'POST':
        if (course_section):
            form = EditCoursesForm()
        else:
            form = EditInterestsForm()
            
        if 'reset' not in request.GET:
            if (course_section):
                load_user_courses(user_profile, prev_choices, options, form)
            else:
                load_user_interests(user_profile, prev_choices, options, form)
        
        else:
            options = form.fields[user_section].choices
            reset = True
    else:
        if (course_section):
            form = EditCoursesForm(request.POST)
        else:
            form = EditInterestsForm(request.POST)
        
        if form.is_valid():
            if (course_section):
                add_core_courses(request, user_profile, user_model, form)
                add_generic_credits(request, user_profile, form)
            else:
                add_interests(request, user_profile, user_model, form)
            
            if (len(messages.get_messages(request)) == 0):
                messages.info(request, "No changes submitted!")
            
            user_profile.save()
            print("user prof saved with new changes!")
            
            return True
        else:
            for field in form:
                if field.errors:
                    print(field.errors) 
            messages.error(request, "Error While Attempting to Save Changes")
        
            return True
    
    context.append({
        'form': form,
        'options': options,
        'prev_choices': prev_choices,
        'reset': reset,
    })
    
    return False
            

#################################################
### Helper functions for editing user courses ###
#################################################
def load_user_courses(user_profile, prev_choices, course_options_ref, form):
    """A helper function used for edit_course_history.
    Used to load any saved courses into the form.

    Args:
        user_profile (request.user.profile): The profile of the user that is currently logged in
        prev_choices (dict): A dict containing the previous choices of the user, passed by reference and used in the calling function to return as context
        course_options_ref (list): A list containing the courses the user can choose from, passed by reference and used in the calling function to return as context
        form (EditCoursesForm): An empty form that will be filled with the user's saved courses
    """
    
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
        course_options_ref.extend(course_options)
        
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
    
    
def add_core_courses(request, user_profile, user_model, form):
    """A helper function used for edit_course_history.
    Useed to add core courses to the user's course history. These are the courses that show up in the dropdown menu.

    Args:
        request: The request that was sent to the calling view function
        user_profile (request.user.profile): The profile of the user that is currently logged in
        user_model (request.user): The user that is currently logged in
        form (EditCoursesForm): The form that was submitted by the user
    """
    
    saved_courses_taken = list(map(str, user_profile.courses_taken.values_list('id', flat=True)))
    user_courses_taken = form.cleaned_data.get('major_courses')

    # Check if the box has data in it or if it's empty but the user removed all courses from the list
    if ((len(saved_courses_taken) > 0) or (len(user_courses_taken) > 0)):
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
                if (course_model not in user_profile.courses_taken.all()):
                    user_profile.courses_taken.add(course_model)
                    messages.info(request, "Added course: " + course_model.name)
                    print("found course_model with the id!")
                
                ## add any courses that are a prereq to this course ##
                prereqs = recursive_add_prereqs(course_model) # returns a list of courses
                for prereq in prereqs:
                    if (prereq not in user_profile.courses_taken.all()):
                        user_profile.courses_taken.add(prereq) # add all the prereqs for this course to the user's courses_taken 
                        messages.info(request, f"Added {prereq.name} as a prerequisite for {course_model.name}")
                    else:
                        print("prereq: ", prereq)
                        print("courses_taken: ", user_profile.courses_taken.all())
                
            except:
                print("course_model not found")
        
        # Add any removed courses to the messages if they were not added back (weren't a prereq for a class in course history)
        for removed_course in courses_to_remove:
            removed_course = Course.objects.get(id=int(removed_course))
            if removed_course not in user_profile.courses_taken.all(): # If it was NOT added back (it was NOT a prereq for another course)
                messages.info(request, "Removed course: " + removed_course.name)


def add_generic_credits(request, user_profile, form):
    """A helper function used for edit_course_history.
    Used to add generic credits to the user's profile.

    Args:
        request: The request that was sent to the calling view function
        user_profile (request.user.profile): The profile of the user that is currently logged in
        form (EditCoursesForm): The form that was submitted by the user
    """
    
    # Add any general credits 
    user_sci = form.cleaned_data.get('sci_cred')
    user_soc_sci = form.cleaned_data.get('soc_sci_cred')
    user_arts_lett = form.cleaned_data.get('arts_letters_cred')
    user_gp = form.cleaned_data.get('gp_cred')
    user_us = form.cleaned_data.get('us_cred')
                
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
    if (user_profile.aal_credits != int(user_arts_lett)):
        user_profile.aal_credits = int(user_arts_lett)
        messages.info(request, f"Updated Arts and Letters to {user_arts_lett} credits taken")
    if (user_profile.ssci_credits != int(user_soc_sci)):
        user_profile.ssci_credits = int(user_soc_sci)
        messages.info(request, f"Updated Social Science to {user_soc_sci} credits taken")
    if (user_profile.sci_credits != int(user_sci)):
        user_profile.sci_credits = int(user_sci)
        messages.info(request, f"Updated Science to {user_sci} credits taken")
    if (user_profile.gp_credits != int(user_gp)):
        user_profile.gp_credits = int(user_gp)
        messages.info(request, f"Updated Global Perspectives to {user_gp} credits taken")
    if (user_profile.us_credits != int(user_us)):
        user_profile.us_credits = int(user_us)
        messages.info(request, f"Updated US to {user_us} credits taken")
        

###################################################
### Helper functions for editing user interests ###
###################################################
def load_user_interests(user_profile, prev_choices, interest_options_ref, form):
    int_selections = user_profile.interests.all()
    
    if(int_selections is not None):
        interest_options = form.fields['user_interests'].choices
        interest_options_ref.extend(interest_options)
        
        for selection in int_selections:
            for interest_val, interest_display in interest_options:
                if interest_val == selection.keyword: # found a match, set as selected for that list option
                    print('found a match for: ', selection)
                    prev_choices[str(selection)] = True


def add_interests(request, user_profile, user_model, form):
    saved_interests = list(map(str, user_profile.interests.values_list('keyword', flat=True)))
    user_interests = form.cleaned_data.get('user_interests')
    
    # Check if the box has data in it or if it's empty but the user removed all interests from the list
    if ((len(saved_interests) > 0) or (len(user_interests) > 0)):
        # Each Keyword model will have an id so need to retrieve
        # the appropriate Keyword models, then add those to the instance of the user profile model

        un = user_model.username
        print(un)

        # Get interests to remove (if anything was removed from list)
        int_strs_to_remove = [interest for interest in saved_interests if interest not in user_interests]
        # Now this is array of strings, go through string and delete
        for interest_str in int_strs_to_remove:
            keyword_model = Keyword.objects.get(keyword=interest_str)
            user_profile.interests.remove(keyword_model)
            messages.info(request, "Removed interest: " + keyword_model.keyword)

        for interest_kw in user_interests:
            try:
                keyword_model = Keyword.objects.get(keyword=interest_kw)
                if (keyword_model not in user_profile.interests.all()):
                    user_profile.interests.add(keyword_model)
                    messages.info(request, "Added interest: " + keyword_model.keyword)
                    print("found keyword_model with the id!")                        
                
            except:
                print("keyword_model not found")


################################################################
# Separated code in the case that update_user_profile has bugs #
### Should be removed once we confirm everything is working. ###
################################################################

# def edit_course_history(request, context):
#     """
#     Handles the editing of a user's course history. This includes adding and removing core courses, and generic credits.

#     Args:
#         request: request that was sent to the calling view function
#         context (dict): context is a list that is passed by reference, and is used in the calling function to render the page with the appropriate context

#     Returns:
#         bool: True or False
#                 -True: Indicates to the view function to redirect to the same page
#                 -False: Indicates to the view function to render the page with the appropriate context
#     """
#     user_model = request.user # user that is currently logged in
#     user_profile = user_model.profile
#     prev_choices = {}
#     options = []
#     reset = False
    
#     if request.method != 'POST':
#         form = EditCoursesForm()
        
#         if 'reset_courses' not in request.GET:
#             load_user_courses(user_profile, prev_choices, course_options, form)
#         else: # reset courses button was pressed, load empty form
#             course_options = form.fields['major_courses'].choices
#             courses_reset = True

#     else:
#         form = EditCoursesForm(request.POST)
#         if form.is_valid():
#             add_core_courses(request, user_profile, user_model, form)
#             add_generic_credits(request, user_profile, form)
            
#             if (len(messages.get_messages(request)) == 0):
#                 messages.info(request, "No changes submitted!")
#                 messages.info(request, "Please update your course history to see saved changes.")
            
#             user_profile.save()
#             print("user prof saved with new changes!")
            
#             return True
#         else:
#             for field in form:
#                 if field.errors:
#                     print(field.errors) 
#             messages.error(request, "Error While Attempting to Save Changes")
            
#             return True


#     context.append({'form': form,
#                'options': course_options,
#                'prev_choices': prev_choices,
#                'reset': courses_reset,
#                })
    
#     return False
    

# def edit_user_interests(request, context):
#     user_model = request.user # user that is currently logged in
#     user_profile = user_model.profile
#     prev_choices = {}
#     options = []
#     reset = False
    
#     if request.method != 'POST':
#         form = EditInterestsForm()
        
#         if 'reset_interests' not in request.GET:
#             load_user_interests(user_profile, prev_choices, interest_options, form) 
#         else:
#             interest_options = form.fields['user_interests'].choices
#             interests_reset = True

#     else:
#         form = EditInterestsForm(request.POST)
#         if form.is_valid():
#             add_interests(request, user_profile, user_model, form) 

#             if (len(messages.get_messages(request)) == 0):
#                 messages.info(request, "No changes submitted!")
#                 messages.info(request, "Please update your interests to see saved changes.")

#             user_profile.save()
#             print("user prof saved with new changes!")
            
#             return True
#         else:
#             for field in form:
#                 if field.errors:
#                     print(field.errors) 
#             messages.error(request, "Error While Attempting to Save Changes")
            
#             return True


#     context.append({'form': form,
#                'options': interest_options,
#                'prev_choices': prev_choices,
#                'reset': interests_reset,
#                }) 
    
#     return False
