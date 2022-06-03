"""CRUD operations."""

from model import User, RecruiterQuery, RecruiterQueryLanguages, Gender, Languages, ProgrammerLanguages, Programmer, connect_to_db

from model import db, connect_to_db 

import datetime

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
   

def create_programmer(named_user):
    """Insert a new programmer in the database"""

    programmer = Programmer(login=named_user.login,
                            full_name=named_user.name,
                            company_name= named_user.company,
                            profile_created_at= named_user.created_at,
                            location=named_user.location,
                            email=named_user.email,
                            twitter_handle=named_user.twitter_username)
    # add check of login to see if in the db

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
    
    return recruiter_query
#working



if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)