"""
Author: Erin Stone
"""

import pandas as pd
df = pd.read_excel('recommendcourses.xlsx', index_col="id")

REQUIRED_CREDITS = 180
ALL_REQUIRED_CS = {210000, 211000, 212000, 313000, 314000, 315000, 330000, 231001, 232001, 422000, 415000, 425000, 121008, 122008, 112001, 111001, 101001}

aal_left = "Arts and Letters"
ssc_left = "Social Science"
sc_left = "General Science"
gp_left = "Global Perspectives"
us_left = "US Difference"
math2_left = "252 or higher"
sc_path_left = "science path"
wr_left = "320 or WR"
calc_left = "252) or (MATH"
cs_elec_left = "credits from {"

ph1_left = "of PHYS 201"  # user has begun PHYS 201-203
ph2_left = "of PHYS 251"  # user has begun PHYS 251-253
ch_left = "of CH 221"  # user has begun CH 221-223
ge_left = "from {GEOG 321"  # user has begun GEOG path
er_left = "of ERTH 201"  # user has begun ERTH 201-203
ps_left = "from {PSY 348"  # user has begun PSY path
bi_left = "of {BI 211"  # user has begun BI path (unused because of else condition)


class Course:
    '''
    course should be identifiable by type (CS, MATH, ANTH, etc)
    course should optionally be identifiable by interest keywords (Software, AI, etc)
    course should be identifiable by credits (4, 2, etc)

    example Course:
        subject="CS", number=422, list of direct prerequisites=[
        credits=4, term="FWS", annual=True

    '''
    def __init__(self, subject, number, prereq, credits, term, annual): # TODO deal with interests as a parameter or external grouping?
        self.subject = subject
        self.number = number
        self.prereq = prereq
        self.title = str(subject) + ' ' + str(number)
        self.credits = credits
        self.term = term  # note: course offered fall,winter,spring,summer represented by "FWSU" respectively
        self.annual = annual  # note: True = annual course    False = biennial course

    '''def is_offered(self, target_term, target_year):
        

        :param target_term: char 'F' or 'W' or 'S' or 'U'
        :param target_year: int
        :return: bool
        
        return self.term == target_term and (target_year % 2 == 1 or self.annual)'''

def is_offered(course, target_term, target_year): # get whether offered ignoring Course object
    '''
    return whether course is offered during the target term and year
    :param course: int course id
    :param target_term: char 'F' or 'W' or 'S' or 'U'
    :param target_year: int
    :return: bool
    '''
    t = df['term'].loc[course]
    return target_term in df['term'].loc[course] and (target_year % 2 == 1 or bool(df['annual'].loc[course]))


def get_prereq(course): # get course prereq ignoring Course object
    '''
    return prerequisite courses associated with a course
    :param course: course id int
    :return: set of course id ints
    '''
    if isinstance(df['prereq'].loc[course], str):
        p = {eval(i) for i in (df['prereq'].loc[313000]).split(", ")}
    else:
        p = {df['prereq'].loc[course]}
    return p

def get_credits(course): # get course credits ignoring Course object
    '''
    return number of credits a course is worth
    :param course: course id int
    :return: int credits
        '''
    return int(df['credits'].loc[course])

def id_to_title(course_set):
    title_set = set()
    for course in course_set:
        title = course
        if(str(course) != course):
            title = df['subject'].loc[course] + ' ' + str(df['number'].loc[course])
            if(len(str(course)) > 6):
                title += ' ' + df['name'].loc[course]
        title_set.add(title)
    return title_set

def id_to_title_list(course_list):
    title_set = []
    for course in course_list:
        title = course
        if(str(course) != course):
            title = df['subject'].loc[course] + ' ' + str(df['number'].loc[course])
            if(len(str(course)) > 6):
                title += ' ' + df['name'].loc[course]
        title_set.append(title)
    return title_set

def total_credits(course_set):
    total = 0
    for course in course_set:
        if isinstance(course, int):
            total += int(df['credits'].loc[course])
    return total

class User:
    '''
    user must have defined start term, start year, max credits per term, set of past courses (with passing grades), degree (BS/BA), number of completed credits for each gen ed area

    parameters
    start_term: char 'F' or 'W' or 'S' or 'U' representing Fall or Winter or Spring or Summer respectively, for plan generation
    start_year: int representing desired start year for plan generation
    max_credits_per_term: int
    course_history: set of ints where each int is a course id
    aal_credits: int, arts and letters credits completed by user, default 0
    ssc_credits: int, social science credits completed by user, default 0
    sc_credits: int, science credits completed by user, default 0
    gp_credits: int, global perspectives credits completed by user, default 0
    us_credits: int, US difference inequality and agency credits completed by user, default 0

    example instances of User
    rupert = User('F', 2023, 16, {210000, 121008}, 4, 8, 4, 12, 4)
    barbara = User('S', 2028, 12, {231001})
    '''
    def __init__(self, start_term, start_year, max_credits_per_term, course_history, aal_credits=0, ssc_credits=0, sc_credits=0, gp_credits=0, us_credits=0): # TODO add interests, degree
        self.start_term = start_term # user's desired start term for plan generation
        self.start_year = start_year # user's desired start year for plan generation
        self.max_credits_per_term = max_credits_per_term # user's desired maximum credits per term
        self.course_history = course_history # all courses taken and passed by user

        # areas of inquiry and cultural literacy (general degree required credits)
        self.aal_credits = aal_credits
        self.ssc_credits = ssc_credits
        self.sc_credits = sc_credits
        self.gp_credits = gp_credits
        self.us_credits = us_credits

        #TODO add summer options
        #TODO add BA/BS (math/language) credits


    def remaining_requirements(self, course_history, aal=0, ssc=0, sc=0, gp=0, us=0, misc=0):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''

        # initialize some useful variables
        math2_taken = {413000, 420000, 427000, 473000, 253001, 281001, 256001, 282001, 307001, 316001, 317001, 320001, 345001, 347001, 348001, 351001, 352001, 391001, 392001, 394001, 395001, 397001, 411001, 412001, 413001, 414001, 415001, 421001, 422001, 431001, 432001, 433001, 434001, 441001, 444001, 445001, 446001, 461001, 462001, 463001, 467001} & course_history
        #math2_shared = len(math2_taken) > 0 and len({253001, 281001, 256001, 282001, 307001, 316001, 317001, 320001, 345001, 347001, 348001, 351001, 352001, 391001, 392001, 394001, 395001, 397001, 411001, 412001, 413001, 414001, 415001, 421001, 422001, 431001, 432001, 433001, 434001, 441001, 444001, 445001, 446001, 461001, 462001, 463001, 467001} & math2_taken) == 0
        cs_electives_taken_under = set()
        cs_electives_taken_over = set()
        cs_electives_over = set()
        cs_electives_under = set()
        skipped_shared = False
        skipped_shared_course = set()
        for id, row in df.iterrows():
            if "cselectiveover" in row['satisfyarea']:
                cs_electives_over.add(id)
            elif "cselectiveunder" in row['satisfyarea']:
                cs_electives_under.add(id)

        for course in course_history: # create taken cs electives set EXCLUDING any shared with math elective area
            if isinstance(course, int):
                if "cselectiveunder" in df['satisfyarea'].loc[course] or "cselectiveover" in df['satisfyarea'].loc[course]: # course is cs elective
                    if course in {413000, 420000, 427000, 473000} and not skipped_shared:
                        skipped_shared = True
                        skipped_shared_course.add(course)
                    else:
                        if "cselectiveunder" in df['satisfyarea'].loc[course]:
                            cs_electives_taken_under.add(course)
                        else:
                            cs_electives_taken_over.add(course)

        # areas of inquiry and cultural literacy
        # TODO need more gen ed areas? i dont think so
        aal_done = aal >= 15 #TODO maybe specifics later
        ssc_done = ssc >= 15
        sc_done = sc >= 15
        gp_done = gp >= 4
        us_done = us >= 4
        #TODO BA/BS

        # CS major requirements
        calc_done = {251001, 252001}.issubset(course_history) or {261001, 262001}.issubset(course_history) or {246001, 247001}.issubset(course_history)
        math1_taken = {253001, 263001, 347001, 351001, 391001, 341001, 343001, 425001} & course_history # taken classes from math1 requirement
        math1_done = len(math1_taken) >= 2 and math1_taken != {253001, 263001} and math1_taken != {343001, 425001}
        cs_electives_done = total_credits(cs_electives_taken_under | cs_electives_taken_over) >= 20 and total_credits(cs_electives_taken_over) >= 12
        math2_done = len(math2_taken) >= 1
        # note math2_done includes CS courses that may be used for either math or cs elective requirement!
        science_taken = {201002, 202002, 203002, 251002, 252002, 253002, 221003, 222003, 223003, 141004, 321004, 322004, 323004, 201005, 202005, 203005, 201006, 348006, 301006, 304006, 305006, 211007, 111003, 113003, 221003, 212007, 213007} & course_history  # taken classes from science requirement
        #ph1=[201002, 202002, 203002]
        #ph2=[251002, 252002, 253002]
        #ch=[141004, {321004, 322004, 323004}]
        #geog=[]
        #geol=[]
        #psy=[]
        #bi=[]
        science_done = {201002, 202002, 203002}.issubset(course_history) or {251002, 252002, 253002}.issubset(course_history) or \
                       {221003, 222003, 223003}.issubset(course_history) or \
                       (141004 in course_history and len({321004, 322004, 323004} & course_history) >= 2) or \
                       {201005, 202005, 203005}.issubset(course_history) or \
                       (201006 in course_history and len({348006, 301006, 304006, 305006} & course_history) >= 2) or \
                       (211007 in course_history and len({111003, 113003, 221003} & course_history) >= 1 and len({212007, 213007} & course_history) >= 1)#TODO
        writing_done = total_credits(course_history) >= 90 and len({320008, 321008} & course_history) >= 1

        remaining = set()
        # UNUSED if not all((arts_and_letters_done, social_science_done, calc_done, math1_done, cs_electives_done, math2_done, science_done, writing_done)):
        # TODO gen ed checks

        #CS major requirement checks
        remaining.update(ALL_REQUIRED_CS.difference(course_history)) # cs core

        if not calc_done:
            if 251001 in course_history:
                remaining.add(252001)
            elif 261001 in course_history:
                remaining.add(262001)
            elif 246001 in course_history:
                remaining.add(247001)
            else:
                # remaining.add("One from (2511 and 2521), (2611 and 2621), (2461 and 2471)")
                # remaining.add("(2511 and 2521) or (2461 and 2471)")
                remaining.add("(MATH 251 and MATH 252) or (MATH 246 and MATH 247)")

        if not math1_done:
            math1_req = {253001, 263001, 347001, 351001, 391001, 341001, 343001, 425001}
            if 253001 in math1_taken or 263001 in math1_taken:
                remaining.add("One from " + str(math1_req.difference({253001, 263001})))
            if 343001 in math1_taken or 425001 in math1_taken:
                remaining.add("One from " + str(math1_req.difference({343001, 425001})))

        if not cs_electives_done:
            alttxt = ""
            if total_credits(cs_electives_taken_under) < 8:
                alttxt =  " or (" + str(8 - total_credits(cs_electives_taken_under)) + " credits from " + str(id_to_title(cs_electives_under.difference(cs_electives_taken_under))) + " and " + str(12 - total_credits(cs_electives_taken_over)) + " credits from " + str(id_to_title((cs_electives_over.difference(cs_electives_taken_over)).difference(skipped_shared_course))) + ")"
            remaining.add("(" + str(20 - total_credits(cs_electives_taken_over | cs_electives_taken_under)) + " credits from " + str(id_to_title((cs_electives_under | cs_electives_over).difference(cs_electives_taken_under | cs_electives_taken_over))) + ")" + alttxt)

        if not math2_done:
            remaining.add("MATH course with a prerequisite of MATH 252 or higher, or one of CS 413, CS 420, CS 427, CS 473")

        if not science_done:
            sciencepaths = ""
            if len(science_taken) > 0:
                if 201002 in course_history: # physics 200s
                    sciencepaths += "Complete remainder of PHYS 201-203 sequence"
                if 251002 in course_history:  # physics 250s
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of PHYS 251-253 sequence"
                if 221003 in course_history:  # chem
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of CH 221-223 sequence"
                if 141004 in course_history:  # geog
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of 2 courses from {GEOG 321, GEOG 322, GEOG 323}"
                if 201005 in course_history:  # erth
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of ERTH 201-203 sequence"
                if 201006 in course_history:  # psy
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of 2 courses from {PSY 348, PSY 301, PSY 304, PSY 305}"
                if 111003 in course_history:  # bio
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of {BI 211 and one from {BI 212, BI 213}}"
            else:
                sciencepaths = "Begin one science path from {PHYS General, PHYS Foundations, CH, GEOG, ERTH, PSY, BI}"
            remaining.add(sciencepaths)

        if not writing_done:
            remaining.add("WR 320 or WR 321")


        # areas of inquiry and cultural literacy checks
        if not aal_done:
            remaining.add(str(15-aal) + " Arts and Letters credits")
        if not ssc_done:
            remaining.add(str(15-ssc) + " Social Science credits")
        if not sc_done:
            remaining.add(str(15-sc) + " General Science credits")
        if not gp_done:
            remaining.add(str(4-gp) + " Global Perspectives credits")
        if not us_done:
            remaining.add(str(4-us) + " US Difference/Inequality/Agency credits")

        return remaining


    def cs_electives_msg_to_ids(self, msg):
        '''
        convert a message (msg) about what cs electives the user has left to take into a set of course ids

        example input:
            "(20 credits from {'CS 423', 'CS 413', 'CS 443', 'CS 420',
            'CS 433', 'CS 410 Game Programming', 'CS 410 Computational Science',
            'CS 427', 'CS 441', 'CS 333', 'CS 451', 'CS 461', 'CS 322',
            'CS 436', 'CS 434', 'CS 410 Multi-agent Systems', 'CS 473', 'CS 453',
            'CS 431', 'CS 471', 'CS 472', 'CS 445', 'CS 429', 'CS 432'})
            or (8 credits from {'CS 322', 'CS 333'} and 12 credits from {'CS 423',
            'CS 413', 'CS 443', 'CS 420', 'CS 433', 'CS 410 Game Programming',
            'CS 410 Computational Science', 'CS 427', 'CS 441', 'CS 451', 'CS 461',
            'CS 436', 'CS 434', 'CS 410 Multi-agent Systems', 'CS 473', 'CS 453',
            'CS 431', 'CS 471', 'CS 472', 'CS 445', 'CS 429', 'CS 432'})"
        example output for above input:
            {432000, 453000, 431000, 420000, 4100001, 4100002, 436000, 4100003, 441000,
            473000, 451000, 472000, 413000, 333000, 461000, 445000, 429000, 322000, 434000,
            423000, 471000, 433000, 443000, 427000}

        :param msg: any str message with an embedded set of CS elective titles that you want to extract
        :return: set of ints (course ids)
        '''
        msg = set((msg[msg.index("{") + 1:msg.index("}")]).split(', '))
        msg = {eval(i) for i in msg}
        j = set()  # will be new set of courses converted to ids
        for i in msg:  # convert from title to id (CS 210 -> 210000)
            tmp = i.split()[1] + "000"
            if len(i) > 6:  # course has a special Topic
                if i[7] == 'C':  # computational science
                    tmp += "1"
                elif i[7] == 'G':  # game programming
                    tmp += "2"
                else:  # multi-agent systems
                    tmp += "3"
            tmp = int(tmp)
            j.add(tmp)
        return j


    def has_remaining_requirements(self, course_history, aal=0, ssc=0, sc=0, gp=0, us=0, misc=0):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        return len(self.prioritize_requirements(self.remaining_requirements(course_history, aal, ssc, sc, gp, us, misc))) != 0 | \
               REQUIRED_CREDITS - (total_credits(course_history) + aal + ssc + sc + gp + us + misc) > 0

    def prioritize_requirements(self, remaining):
        """
        optional function that uses your remaining courses set or list and converts to a prioritized list from most
        important courses (required CS...) to least important (general credits)
        the order of addition to the list (priority) is the following:
            cs_req + calc + cs_elec + math2 + other + sc + wr + areas
        :param remaining: should probably be a set of remaining courses (including strings like "One from ...")
        :return: list of the same elements from the input set but ordered from most to least priority
        """
        cs_req = []
        cs_elec = []
        calc = []
        math2 = []
        sc = []
        wr = []
        areas = []
        other = []
        for req in remaining:
            if isinstance(req, str):
                if calc_left in req:
                    calc.append(req)
                elif cs_elec_left in req:
                    cs_elec.append(req)
                elif math2_left in req:
                    math2.append(req)
                elif ph1_left in req or ph2_left in req or ch_left in req or ge_left in req or er_left in req \
                        or ps_left in req or bi_left in req or sc_path_left in req:
                    sc.append(req)
                elif wr_left in req:
                    wr.append(req)
                elif aal_left in req or ssc_left in req or sc_left in req or gp_left in req or us_left in req:
                    areas.append(req)
                #TODO elif generic filler credit in req:
            elif req in ALL_REQUIRED_CS:
                cs_req.append(req)
            else: # other things user must finish that they started
                other.append(req)
        return cs_req + calc + cs_elec + math2 + other + sc + wr + areas



    def generate_forecast(self, course_history, max_credits_per_term=16, target_term='F', target_year=2023, aal=0, ssc=0, sc=0, gp=0, us=0, misc=0):
        """
        '16 credits per term' preset. Completes all required courses for the CS major and then completes general areas and then overall credits.

        :param course_history: set of course ids (ex: {210000, 211000, 231001})
        :param max_credits_per_term: int representing the number of credits the user does not want to exceed per term
        :param target_term: char 'F' or 'W' or 'S' or 'U' representing Fall or Winter or Spring or Summer respectively, representing when the user wants the
            first term of the degree plan to start
        :param target_year: int year representing the year the user wants heir degree plan to start
        :param aal: int representing the user's completed arts and letters credits
        :param ssc: int representing the user's completed social science credits
        :param sc: int representing the user's completed (general) science credits
        :param gp: int representing the user's completed global perspectives credits
        :param us: int representing the user's completed US difference/inequality/agency credits
        :return: TODO
        """
        forecast = []  # entire degree plan
        # remaining = remaining_requirements(course_history, aal, ssc, sc, gp, us)
        course_hist = course_history.copy()
        last_course_hist = course_history.copy()
        aal2 = aal
        ssc2 = ssc
        sc2 = sc
        gp2 = gp
        us2 = us
        misc2 = misc
        term_credits = 0
        terms = "FWSF" #TODO deal with summer "FWSUF"
        this_term = target_term
        this_year = target_year


        while self.has_remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2, misc2):  # runs each term
            term_forecast = []  # single term
            for course in self.prioritize_requirements(self.remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2, misc2)):
                #print("prio: ",self.prioritize_requirements(self.remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2)))
                #print("course:",course, "term:", term_forecast, "forecast:", forecast)
                #print(self.remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2))
                #print(course, type(course))
                if isinstance(course, str):
                    if calc_left in course: # suggest MATH 251 to start the calculus path (TODO tailor to interest in case user wants 246 instead)
                        course = 251001
                    elif cs_elec_left in course: # suggest an available cs elective TODO tailor to interest
                        course = self.cs_electives_msg_to_ids(course) # course is now actually a set of course ids
                        match_not_found = True
                        for i in course: # i is a cs elective the user hasn't yet taken
                            if (get_prereq(i)).issubset(last_course_hist) and is_offered(i, this_term, this_year) and match_not_found:
                                course = i # choose this cs elective to see if we can add it to this term
                                match_not_found = False # match has been found!

                        if match_not_found: # the check to add the course to the term later will fail since no takeable cs elective exists for this term
                            course = list(course)[0] # so we at least set the course to a valid id so it is no longer a string
                    elif wr_left in course: # suggest writing (TODO tailor to interest in case user wants 321 instead)
                        if total_credits(course_hist) >= 90: # user is junior standing
                            course = 320008
                        else: # user cannot take WR 3XX, do not try writing course
                            course = 261001
                    elif sc_path_left in course: # suggest science path to begin (TODO tailor to interest)
                        course = 201005 # ERTH
                    elif math2_left in course: # suggest MATH 300+ elective (TODO tailor to interest)
                        course = 253001
                    elif us_left in course:
                        course = 261001 # this course is never offered so the following checks will fail and no specific course will be added
                        if term_credits + 4 <= max_credits_per_term:
                            term_forecast.append("4 (US) credits") # us difference/inequality/agency
                            term_credits += 4
                            us2 += 4
                    elif gp_left in course:
                        course = 261001 # this course is never offered so the following checks will fail and no specific course will be added
                        if term_credits + 4 <= max_credits_per_term:
                            term_forecast.append("4 (GP) credits") # global perspectives
                            term_credits += 4
                            gp2 += 4
                    elif sc_left in course:
                        course = 261001 # this course is never offered so the following checks will fail and no specific course will be added
                        if term_credits + 4 <= max_credits_per_term:
                            term_forecast.append("4 (>3) credits") # science general area
                            term_credits += 4
                            sc2 += 4
                    elif ssc_left in course:
                        course = 261001 # this course is never offered so the following checks will fail and no specific course will be added
                        if term_credits + 4 <= max_credits_per_term:
                            term_forecast.append("4 (>2) credits") # social science area
                            term_credits += 4
                            ssc2 += 4
                    elif aal_left in course:
                        course = 261001 # this course is never offered so the following checks will fail and no specific course will be added
                        if term_credits + 4 <= max_credits_per_term:
                            term_forecast.append("4 (>1) credits") # arts and letters area
                            term_credits += 4
                            aal2 += 4
                    elif "Complete remainder" in course: # user has begun at least one science path.
                        paths = course.split(" or ") # get all science paths the user has started
                        level_2 = []
                        level_3 = []
                        for path in paths: # find out whether the user needs to take the second or third part of the path
                            if ph1_left in path: # user started PHYS20X path
                                if 202002 in course_hist: # user only needs to take third part of path
                                    level_3.append(203002)
                                else: # user still needs to take second part of path
                                    level_2.append(202002)
                            elif ph2_left in path: # user started PHYS25X path
                                if 252002 in course_hist:
                                    level_3.append(253002) # TODO be careful about 253001 requirement
                                else:
                                    level_2.append(252002)
                            elif ch_left in path: # user started CH path
                                if 222003 in course_hist:
                                    level_3.append(223003)
                                else:
                                    level_2.append(222003)
                            elif ge_left in path: # user started GEOG path
                                taken_ge = {321004, 322004, 323004} & course_hist
                                if len(taken_ge == 1): # user only needs one more GEOG class
                                    level_3.append(list(taken_ge)[0]) # add user's remaining options
                                    level_3.append(list(taken_ge)[1])
                                else: # user only took GEOG 141, needs 2
                                    level_2.append(321004) # add user's options
                                    level_2.append(322004)
                                    level_2.append(323004)
                            elif er_left in path: # user started ERTH path
                                if 202005 in course_hist:
                                    level_3.append(203005)
                                else:
                                    level_2.append(202005)
                            elif ps_left in path: # user started PSY path
                                taken_ps = {348006, 301006, 304006, 305006} & course_hist
                                if len(taken_ps) == 1: # user only needs one more PSY class
                                    level_3.append(list(taken_ps)[0])
                                    level_3.append(list(taken_ps)[1])
                                    level_3.append(list(taken_ps)[2])
                                else: # user only took PSY201, needs 2
                                    level_2.append(348006)
                                    level_2.append(301006)
                                    level_2.append(304006)
                                    level_2.append(305006)
                            else: # user started BI path
                                if 211007 in course_hist:
                                    level_3.append(212007)
                                    level_3.append(213007)
                                elif len({212007, 213007} & course_hist) > 0:
                                    level_3.append(211007)
                                else:
                                    level_2.append(212007)
                                    level_2.append(213007)
                                    level_2.append(211007)
                        if len(level_3) > 0:
                            course = level_3[0] # TODO sort from most to least interesting and tailor to user interests
                        else:
                            course = level_2[0] # TODO sort from most to least interesting ...
                    elif "One from" in course: # user needs MATH 300+ elective
                        options = {eval(i) for i in course[course.index("{") + 1:course.index("}")].split(", ")}
                        match_not_found = True
                        for i in options:  # i is a cs elective the user hasn't yet taken
                            if (get_prereq(i)).issubset(last_course_hist) and is_offered(i, this_term, this_year) and match_not_found: # TODO deal w interests
                                course = i  # choose this math elective to see if we can add it to this term
                                match_not_found = False  # match has been found!
                        if match_not_found:  # the check to add the course to the term later will fail since no takeable math elective exists for this term
                            course = list(options)[0]  # so we at least set the course to a valid id so it is no longer a string



                # check that the identified course may be added to the current term. if not, continue to next course or msg in remaining list
                if term_credits + get_credits(course) <= max_credits_per_term and ({df['prereq'].loc[course]} == {False} or (get_prereq(course)).issubset(last_course_hist)) and is_offered(course, this_term, this_year):
                    #if course == 210000:

                    #    print((get_prereq(course)), last_course_hist, (get_prereq(course)).issubset(last_course_hist))
                    #print(last_course_hist)
                    course_hist.add(course)
                    term_forecast.append(course)
                    term_credits += get_credits(course)


            while term_credits + 4 <= max_credits_per_term and \
                    len(self.prioritize_requirements(self.remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2, misc2))) == 0 and \
                    self.has_remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2, misc2):
                term_forecast.append("4 credits")  # any credits
                term_credits += 4
                misc2 += 4
            # reset stuff to go on to the next term
            this_term = terms[terms.index(this_term)+1]
            term_credits = 0
            if(this_term == 'W'):
                this_year += 1
            forecast.append(term_forecast)
            for c in term_forecast:
                last_course_hist.add(c)
            #print("last",last_course_hist)
            #print("forecast: ",forecast)

            #print("prioreq: ",self.prioritize_requirements(self.remaining_requirements(course_hist, aal2, ssc2, sc2, gp2, us2, misc2)))
        return forecast

    def print_forecast(self, start_term, start_year, forecast):
        terms = "FWSF" #TODO deal with summer "FWSUF"
        this_term = start_term
        this_year = start_year
        for term in forecast:
            print(this_term,this_year,":",id_to_title_list(term))
            this_term = terms[terms.index(this_term) + 1]
            if (this_term == 'W'):
                this_year += 1


def __main__():
    start_term = 'F'
    start_year = 2023
    max_credits_per_term = 16
    course_history = {210000, 211000, 251001}
    rupert = User(start_term, start_year, max_credits_per_term, course_history)
    barbara = User('F', 2023, 16, {111003, 210000, 211000, 314000, 212000, 330000, 341001, 420000})
    boo = User('F', 2023, 16, {101001, 111001, 112001, 210000})
    #print(is_offered(21000, 'F', 2023))
    #print(df['term'].loc[21100])
    #for index, row in df.iterrows():
    #    print(str(index) + ' ' + str(row['number']) + ' ' + row['name'])
    print("Rupert's remaining courses: ", id_to_title(rupert.remaining_requirements(rupert.course_history)))
    print("Barbara's remaining courses: ", id_to_title(barbara.remaining_requirements(barbara.course_history)))
    print("Boo's remaining courses: ", id_to_title(boo.remaining_requirements(boo.course_history)))
    print("Boo's remaining course ids: ", boo.remaining_requirements(boo.course_history))
    #generate_forecast(self, course_history, max_credits_per_term=16, target_term='F', target_year=2023, aal=0, ssc=0, sc=0, gp=0, us=0):
    boos_forecast = boo.generate_forecast(boo.course_history, max_credits_per_term, start_term, start_year)
    print("Boo's forecast: ", boos_forecast)
    print("Boo's printed forecast: \n")
    boo.print_forecast(start_term, start_year, boos_forecast)
    #course = "One from {312333, 218238, 222000, 101010}"
    #print({eval(i) for i in course[course.index("{") + 1:course.index("}")].split(", ")})
    '''d = {
    "CS Core Requirements": [
        "CS 415",
        "CS 314",
        "CS 425",
        "CS 313",
        "WR 122",
        "WR 121",
        "MATH 231",
        "CS 315",
        "MATH 232",
        "CS 330",
        "MATH 112",
        "CS 422"
    ],
    "General Education Requirements": [
        "4 US Difference/Inequality/Agency credits",
        "15 Arts and Letters credits",
        "15 Social Science credits",
        "4 Global Perspectives credits",
        "15 Science credits"
    ],
    "CS Elective Requirements": [
        "20 credits from {'CS 441', 'CS 410', 'CS 453', 'CS 433', 'CS 471', 'CS 423', 'CS 445', 'CS 473', 'CS 420', 'CS 472', 'CS 333', 'CS 429', 'CS 432', 'CS 413', 'CS 443', 'CS 322', 'CS 451', 'CS 461', 'CS 436', 'CS 431', 'CS 427', 'CS 434'}",
        "8 credits from {'CS 333', 'CS 322'} and 12 credits from {'CS 441', 'CS 410', 'CS 453', 'CS 433', 'CS 471', 'CS 423', 'CS 445', 'CS 473', 'CS 420', 'CS 472', 'CS 429', 'CS 432', 'CS 413', 'CS 443', 'CS 451', 'CS 461', 'CS 436', 'CS 431', 'CS 427', 'CS 434'}"
    ],
    "CS Math and Writing Requirements": [
        "MATH course with a prerequisite of MATH 252 or higher, or one of CS 413, CS 420, CS 427, CS 473",
        "WR 320 or WR 321",
        "(MATH 251 and MATH 252) or (MATH 246 and MATH 247)"
    ],
    "Science Path Requirements": [
        "Begin one science path from {PHYS General, PHYS Foundations, CH, GEOG, GEOL, PSY, BI}"
    ]
}
    s = d["CS Elective Requirements"][0] # 20 credits of ....
    s = [eval(i) for i in (s[s.index("{")+1:s.index("}")]).split(", ")]
    print(s)

    s2 = d["CS Elective Requirements"][1] # 8 credits of ....
    s3 = [eval(i) for i in (s2[s2.index("{")+1:s2.index("}")]).split(", ")]
    s4 = s2[s2.index("}")+1:]
    s5 = [eval(i) for i in (s4[s4.index("{")+1:s4.index("}")]).split(", ")]
    print(s3, s5)'''

    '''course = "(20 credits from {'CS 420', 'CS 410 Game Programming', 'CS 431', 'CS 451', 'CS 436', 'CS 333', 'CS 434', 'CS 443', 'CS 429', 'CS 473', 'CS 410 Computational Science', 'CS 445', 'CS 441', 'CS 461', 'CS 427', 'CS 410 Multi-agent Systems', 'CS 471', 'CS 472', 'CS 453', 'CS 432', 'CS 433', 'CS 423', 'CS 413', 'CS 322'}) or (8 credits from {'CS 322', 'CS 333'} and 12 credits from {'CS 420', 'CS 410 Game Programming', 'CS 431', 'CS 451', 'CS 436', 'CS 434', 'CS 443', 'CS 429', 'CS 473', 'CS 410 Computational Science', 'CS 445', 'CS 441', 'CS 461', 'CS 427', 'CS 410 Multi-agent Systems', 'CS 471', 'CS 472', 'CS 453', 'CS 432', 'CS 433', 'CS 423', 'CS 413'})"
    course = set((course[course.index("{")+1:course.index("}")]).split(', '))
    course = {eval(i) for i in course}
    j = set()
    for i in course:  # convert from title to id (CS 210 -> 210000)
        tmp = i.split()[1] + "000"
        if len(i) > 6:  # course has a special Topic
            if i[7] == 'C':  # computational science
                tmp += "1"
            elif i[7] == 'G':  # game programming
                tmp += "2"
            else:  # multi-agent systems
                tmp += "3"
        tmp = int(tmp)
        j.add(tmp)
    print(j)'''
    #for i in course:
    #    print(i.split()[0])
    #    print(i.split()[1])


    # print("Rupert's forecast: ", rupert.generate_forecast(start_term, start_year)) # TODO infinite loop bc excel table not filled out i think

    #print({df['prereq'].loc[31300]})
    #for index, row in df.iterrows():
        #print(df[2100]['prereq'])
    #print(21000 in course_history)

    #for index, row in df.iterrows():
        #print(row['subject'] + ' ' + str(row['number']) + ' ' + row['name'])
    #print(len({23, 2, 565} & {34, 2, 565}))
        #print(df[row].loc['subject'] + ' ' + str(df[row].loc['number']) + ' ' + df[row].loc['name'])



if __name__ == '__main__':
    __main__()