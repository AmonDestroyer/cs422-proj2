import pandas as pd
df = pd.read_excel('recommendcourses.xlsx', index_col="id")

REQUIRED_CREDITS = 180


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
    return {df['prereq'].loc[course]}

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
        title_set.add(title)
    return title_set

def total_credits(course_set):
    total = 0
    for course in course_set:
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


    def remaining_requirements(self, course_history, aal=0, ssc=0, sc=0, gp=0, us=0):
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
        skipped_shared_course = {}
        for id, row in df.iterrows():
            if "cselectiveover" in row['satisfyarea']:
                cs_electives_over.add(id)
            elif "cselectiveunder" in row['satisfyarea']:
                cs_electives_under.add(id)
        for course in course_history: # create taken cs electives set EXCLUDING any shared with math elective area
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
        calc_done = {251001, 252001} in course_history or {261001, 262001} in course_history or {246001, 247001} in course_history
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
        science_done = {201002, 202002, 203002} in course_history or {251002, 252002, 253002} in course_history or \
                       {221003, 222003, 223003} in course_history or \
                       ({141004} in course_history and len({321004, 322004, 323004} & course_history) >= 2) or \
                       {201005, 202005, 203005} in course_history or \
                       ({201006} in course_history and len({348006, 301006, 304006, 305006} & course_history) >= 2) or \
                       ({211007} in course_history and len({111003, 113003, 221003} & course_history) >= 1 and len({212007, 213007} & course_history) >= 1)#TODO
        writing_done = total_credits(course_history) >= 90 and len({320008, 321008} & course_history) >= 1

        remaining = set()
        # UNUSED if not all((arts_and_letters_done, social_science_done, calc_done, math1_done, cs_electives_done, math2_done, science_done, writing_done)):
        # TODO gen ed checks

        #CS major requirement checks
        remaining.update({210000, 211000, 212000, 313000, 314000, 315000, 330000, 231001, 232001, 422000, 415000, 425000, 121008, 122008, 112001}.difference(course_history)) # cs core

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
                alttxt =  " or (" + str(8 - total_credits(cs_electives_taken_under)) + " credits from " + str(cs_electives_under.difference(cs_electives_taken_under)) + " and " + str(12 - total_credits(cs_electives_taken_over)) + " credits from " + str((cs_electives_over.difference(cs_electives_taken_over)).difference(skipped_shared_course)) + ")"
            remaining.add("(" + str(20 - total_credits(cs_electives_taken_over | cs_electives_taken_under)) + " credits from " + str((cs_electives_under | cs_electives_over).difference(cs_electives_taken_under | cs_electives_taken_over)) + ")" + alttxt)

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
                if 201005 in course_history:  # geol
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of GEOL 201-203 sequence"
                if 201006 in course_history:  # psy
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of 2 courses from {PSY 348, PSY 301, PSY 304, PSY 305}"
                if 111003 in course_history:  # bio
                    if sciencepaths != "":
                        sciencepaths += " or "
                    sciencepaths += "Complete remainder of {BI 211 and one from {BI 212, BI 213}}"
            else:
                sciencepaths = "Begin one science path from {PHYS General, PHYS Foundations, CH, GEOG, GEOL, PSY, BI}"
            remaining.add(sciencepaths)

        if not writing_done:
            remaining.add("WR 320 or WR 321")


        # areas of inquiry and cultural literacy checks
        if not aal_done:
            remaining.add(str(15-aal) + " Arts and Letters credits")
        if not ssc_done:
            remaining.add(str(15-ssc) + " Social Science credits")
        if not sc_done:
            remaining.add(str(15-sc) + " Science credits")
        if not gp_done:
            remaining.add(str(4-gp) + " Global Perspectives credits")
        if not us_done:
            remaining.add(str(4-us) + " US Difference/Inequality/Agency credits")

        return remaining




    def has_remaining_requirements(self, course_history, aal=0, ssc=0, sc=0, gp=0, us=0):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        return len(self.remaining_requirements(course_history)) != 0 | REQUIRED_CREDITS - total_credits(course_history) > 0


    def generate_forecast(self, target_term, target_year):
        '''
        '''
        forecast = []  # entire degree plan
        remaining = self.remaining_requirements(self.course_history)
        course_hist = self.course_history
        credits = 0
        terms = "FWSF" #TODO deal with summer "FWSUF"
        this_term = target_term
        this_year = target_year
        while self.has_remaining_requirements(course_hist):  # runs each term
            term_forecast = {}  # single term
            for course in self.remaining_requirements(course_hist): #TODO course methods/attributes will not work since courses have not been defined as Course objects. they are just in the .xlsx
                if is_offered(course, this_term, this_year) and get_prereq(course) in self.course_history and credits + get_credits(course) <= self.max_credits_per_term:
                    course_hist.add(course)
                    term_forecast.add(course)
            this_term = terms[terms.index(this_term)+1]
            if(this_term == 'W'):
                this_year += 1
            forecast.append(term_forecast)
        return forecast


def __main__():
    start_term = 'F'
    start_year = 2023
    max_credits_per_term = 16
    course_history = {210000, 211000, 251001}
    rupert = User(start_term, start_year, max_credits_per_term, course_history)
    barbara = User('F', 2023, 16, {111003, 210000, 211000, 314000, 212000, 330000, 341001})
    #print(is_offered(21000, 'F', 2023))
    #print(df['term'].loc[21100])
    #for index, row in df.iterrows():
    #    print(str(index) + ' ' + str(row['number']) + ' ' + row['name'])
    print("Rupert's remaining courses: ", id_to_title(rupert.remaining_requirements(rupert.course_history)))
    print("Barbara's remaining courses: ", id_to_title(barbara.remaining_requirements(barbara.course_history)))
    # print("Rupert's forecast: ", rupert.generate_forecast(start_term, start_year)) TODO infinite loop bc excel table not filled out i think

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
