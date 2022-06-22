"""CRUD operations."""

from model import GenderEnum, User, RecruiterQuery, RecruiterQueryLanguages, Gender, Languages, ProgrammerLanguages, Programmer, connect_to_db, Favorite

from model import db, connect_to_db 
from sqlalchemy import and_
import datetime
from dateutil.relativedelta import relativedelta

# def create_user():
#     """Establish new recruiter site user."""

#     user = User()

#     return user

# def create_recruiter_query_languages():
#     """Add to relationship table."""
    
#     recruiter_query_languages = RecruiterQueryLanguages(recruiter_query_languages_id=recruiter_query_languages_id,
#                                 recruiter_query_id=recruiter_query_id,
#                                 programming_languages_id=programming_languages_id)
 
#     return recruiter_query_languages


def create_programmer_languages(programmer, languages): 
    """Connect multiple languages to multiple programmers."""

    programmer_languages = []
    for language in languages:
        programmer_languages.append(ProgrammerLanguages(programmer=programmer,language=language))

    return programmer_languages
   
def create_prog_frm_user_input(gh_profile, gender):
    """Insert a new programmer in the database, based on user input."""

    programmer = create_programmer(gh_profile)
    name = gh_profile.name
    first_name = name.split(" ", 1)
    create_gender(first_name, gender, probability=None, count=None)
 
    return first_name, gender, programmer 

def create_programmer(named_user):
    """Insert a new programmer in the database"""

    programmer = Programmer(login=named_user.login,
                            full_name=named_user.name,
                            company_name= named_user.company,
                            profile_created_at= named_user.created_at,
                            location=named_user.location,
                            email=named_user.email,
                            twitter_handle=named_user.twitter_username)
    # check via login to see if programmer already in the db
    
    coder_login = Programmer.query.filter_by(login=named_user.login).first()
    
    if coder_login is None:
        db.session.add(programmer)
        db.session.commit()
        
    return programmer


def create_programmers(named_users):
    """Takes in list of programmer objects and returns list of programmers."""
    output_list = []
    
    for named_user in named_users:
        coder = create_programmer(named_user)
        output_list.append(coder)

    return output_list

def update_programer_gender(named_user, gender):
    """takes in named user and adds gender field to programmer."""
    print("*****************************")
    print("made it to update programer gender")
    print(named_user, gender)
    
    named_user.gender = gender
    db.session.add(named_user)
    db.session.commit() 
    

def return_all_programmers():
    """Return all programmers."""
    

    return Programmer.query.all()
#working

def get_programmer_by_login(login):
    """Return programmers by github login."""
    
    coder = Programmer.query.filter_by(login = login).all()
    
    return coder


def create_gender(first_name, assumed_gender, probability, count):
    """Insert new gender information"""

    gender = Gender(first_name=first_name,
                    assumed_gender=assumed_gender,
                    probability=probability,
                    count=count)
    
    db.session.add(gender)
    db.session.commit()
    
    return gender
#working

def create_genders(gen_response):
    """Takes in list of gender objects and commits them to db."""

    output_list = []
    for lst in gen_response:
        for dic in lst:
            output = create_gender(dic['name'], dic['gender'], dic['probability'], dic['count'])
            output_list.append(output)
    
    return output_list


def get_gender(first_name):
    """Return assumed geneder, frequency of name, and probability."""

    return Gender.query.filter_by(first_name) #use filter or filter by


def create_languages(language_name):
    """Insert new programming languages."""

    language = Languages(language_name=language_name)

    return language
#working


def create_recruiter_querie(language_name, location, min_years_of_experience, max_years_of_experience): 
    """Create a search."""

    recruiter_query = RecruiterQuery(language_name=language_name,
                                    location=location, 
                                    min_years_of_experience=min_years_of_experience,
                                    max_years_of_experience=max_years_of_experience) 
    db.session.add(recruiter_query)
    db.session.commit()

    return recruiter_query
#working

def does_querie_exist(location, min_years_of_experience, max_years_of_experience): 
    "find if there is an existing query"

    return RecruiterQuery.query.filter(RecruiterQuery.location.like(f'{location}%'), 
    RecruiterQuery.min_years_of_experience<=min_years_of_experience,
    RecruiterQuery.max_years_of_experience>=max_years_of_experience).first() is not None


def return_results_from_db(location, min_years_of_experience, max_years_of_experience):
    "find querie results from the database"
    
    now = datetime.datetime.now()
    min_years_of_experience = now - relativedelta(years=min_years_of_experience)
    print(min_years_of_experience)
    max_years_of_experience = now - relativedelta(years=max_years_of_experience)
    print(max_years_of_experience)
    return Programmer.query.filter(Programmer.gender==GenderEnum.female.value,
                            Programmer.location.like(f'{location}%'), 
                            and_(Programmer.profile_created_at<= min_years_of_experience,
                            Programmer.profile_created_at>= max_years_of_experience))
#Create a read query takes in location, experience to see if the query exists.
# Return True if it exists
# Return False if it does not
#2022-06-08 03:19:55.953109
#2017-06-08 03:19:55.953109
def create_fav(user_id, programmer_id):
    """Create fav programmer."""

    fav = Favorite(user_id=user_id, programmer_id=programmer_id)
    db.session.add(fav)
    db.session.commit()

    return fav

def get_first_user(): 

    return User.query.first()

def get_fav(programmer_id):
    """Get favorited programmer from the database."""

    fav_coder = Programmer.query.filter_by(programmer_id = programmer_id).all()

    return fav_coder

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)