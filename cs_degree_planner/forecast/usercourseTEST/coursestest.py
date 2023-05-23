import pandas as pd
from itertools import repeat
df = pd.read_excel('recommendcourses.xlsx', index_col="id")
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

    def is_offered(self, target_term, target_year):
        '''

        :param target_term: char 'F' or 'W' or 'S' or 'U'
        :param target_year: int
        :return: bool
        '''
        return self.term == target_term and (target_year % 2 == 1 or self.annual)


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

def id_to_title(course)


class User:
    '''
    user must have defined start term, start year, max credits per term, set of past courses (with passing grades), degree (BS/BA)
    '''
    def __init__(self, start_term, start_year, max_credits_per_term, course_history): # TODO add interests, degree
        self.start_term = start_term
        self.start_year = start_year
        self.max_credits_per_term = max_credits_per_term
        self.course_history = course_history
        #TODO add summer options

    def remaining_requirements(self, course_history):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        REQUIRED_CREDITS = 180

        # general requirements
        # TODO need more gen ed areas
        arts_and_letters_done = 1 #TODO
        social_science_done = 1 #TODO

        # CS major requirements
        calc_done = {2511, 2521} in course_history or {2611, 2621} in course_history or {2461, 2471} in course_history
        math1 = {2531, 2631, 3471, 3511, 3911, 3411, 3431, 4251} & course_history # taken classes from math1 requirement
        math1_done = len(math1) >= 2 and math1 != {2531, 2631} and math1 != {3431, 4251}
        cs_electives_done = 1 # TODO
        math2_done = 1 #TODO
        science_done = 1 #TODO
        writing_done = 1 #TODO WR320 or WR321

        remaining = set()
        # UNUSED if not all((arts_and_letters_done, social_science_done, calc_done, math1_done, cs_electives_done, math2_done, science_done, writing_done)):
        # TODO gen ed checks

        #CS checks
        remaining.update({2100, 2110, 2120, 3130, 3140, 3150, 3300, 2311, 2321, 4220, 4150, 4250}.difference(course_history)) # cs core

        if not calc_done:
            if 2511 in course_history:
                remaining.add(2521)
            elif 2611 in course_history:
                remaining.add(2621)
            elif 2461 in course_history:
                remaining.add(2471)
            else:
                remaining.add("One from (2511 and 2521), (2611 and 2621), (2461 and 2471)")
        if not math1_done:
            math1_req = {2531, 2631, 3471, 3511, 3911, 3411, 3431, 4251}
            if 2531 in math1 or 2631 in math1:
                remaining.add("One from " + str(math1_req.difference({2531, 2631})))
            if 3431 in math1 or 4251 in math1:
                remaining.add("One from " + str(math1_req.difference({3431, 4251})))
        #TODO all other checks

        return remaining




    def has_remaining_requirements(self, course_history):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        return len(self.remaining_requirements(course_history)) != 0


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
            for course in remaining: #TODO course methods/attributes will not work since courses have not been defined as Course objects. they are just in the .xlsx
                if course.is_offered(this_term, this_year) and get_prereq(course) in self.course_history and credits + course.credits <= self.max_credits_per_term:
                    course_hist.add(course)
                    term_forecast.add(course)
            this_term = terms[terms.index(this_term)+1]
            forecast.append(term_forecast)import pandas as pd
from itertools import repeat
df = pd.read_excel('recommendcourses.xlsx', index_col="id")
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
        title = df['subject'].loc[course] + ' ' + str(course)[:3]
        title_set.add(title)
    return title_set

class User:
    '''
    user must have defined start term, start year, max credits per term, set of past courses (with passing grades), degree (BS/BA)
    '''
    def __init__(self, start_term, start_year, max_credits_per_term, course_history): # TODO add interests, degree
        self.start_term = start_term
        self.start_year = start_year
        self.max_credits_per_term = max_credits_per_term
        self.course_history = course_history
        #TODO add summer options

    def remaining_requirements(self, course_history):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        REQUIRED_CREDITS = 180

        # general requirements
        # TODO need more gen ed areas
        arts_and_letters_done = 1 #TODO
        social_science_done = 1 #TODO

        # CS major requirements
        calc_done = {25101, 25201} in course_history or {26101, 26201} in course_history or {24601, 24701} in course_history
        math1 = {25301, 26301, 34701, 35101, 39101, 34101, 34301, 42501} & course_history # taken classes from math1 requirement
        math1_done = len(math1) >= 2 and math1 != {25301, 26301} and math1 != {34301, 42501}
        cs_electives_done = 1 # TODO
        math2_done = 1 #TODO
        science_done = 1 #TODO
        writing_done = 1 #TODO WR320 or WR321

        remaining = set()
        # UNUSED if not all((arts_and_letters_done, social_science_done, calc_done, math1_done, cs_electives_done, math2_done, science_done, writing_done)):
        # TODO gen ed checks

        #CS checks
        remaining.update({21000, 21100, 21200, 31300, 31400, 31500, 33000, 23101, 23201, 42200, 41500, 42500}.difference(course_history)) # cs core

        if not calc_done:
            if 25101 in course_history:
                remaining.add(25201)
            elif 26101 in course_history:
                remaining.add(26201)
            elif 24601 in course_history:
                remaining.add(24701)
            else:
                remaining.add("One from (2511 and 2521), (2611 and 2621), (2461 and 2471)")
        if not math1_done:
            math1_req = {25301, 26301, 34701, 35101, 39101, 34101, 34301, 42501}
            if 25301 in math1 or 26301 in math1:
                remaining.add("One from " + str(math1_req.difference({25301, 26301})))
            if 34301 in math1 or 42501 in math1:
                remaining.add("One from " + str(math1_req.difference({34301, 42501})))
        #TODO all other checks

        return remaining




    def has_remaining_requirements(self, course_history):
        '''
        ASSUMPTIONS: user will satisfy location-specific requirements and P/NP/Graded requirements on their own
        untested code below'''
        return len(self.remaining_requirements(course_history)) != 0


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
    course_history = {21000, 21100, 25101}
    rupert = User(start_term, start_year, max_credits_per_term, course_history)
    barbara = User('F', 2023, 16, {26101, 21000, 21100, 31400, 21200, 33000, 34101})
    #print(is_offered(21000, 'F', 2023))
    #print(df['term'].loc[21100])
    print("Rupert's remaining courses: ", id_to_title(rupert.remaining_requirements(rupert.course_history)))
    print("Barbara's remaining courses: ", id_to_title(barbara.remaining_requirements(barbara.course_history)))
    # print("Rupert's forecast: ", rupert.generate_forecast(start_term, start_year)) TODO infinite loop bc excel table not filled out i think

    #print({df['prereq'].loc[31300]})
    #for index, row in df.iterrows():
        #print(df[2100]['prereq'])
    #print(21000 in course_history)


if __name__ == '__main__':
    __main__()


def __main__():
    start_term = 'F'
    start_year = 2023
    max_credits_per_term = 16
    course_history = {2100, 2110, 2511}
    rupert = User(start_term, start_year, max_credits_per_term, course_history)
    print("Rupert's remaining courses: ", rupert.remaining_requirements(rupert.course_history))
    print({df['prereq'].loc[3130]})
    #for index, row in df.iterrows():
        #print(df[2100]['prereq'])
    print(2100 in course_history)


if __name__ == '__main__':
    __main__()