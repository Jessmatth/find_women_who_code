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
def create_language(language): 
    """Insert language into languages table."""
    languages_in_db = Languages.query.filter_by(language_name=language).first()
    
    if languages_in_db is None:
        language_object = Languages(language_name=language)
        db.session.add(language_object)
        db.session.commit()

    return Languages.query.filter_by(language_name=language).first()


def create_programmer_language(programmer, language): 
    """Connect multiple languages to multiple programmers."""

    language_object = Languages.query.filter_by(language_name=language).first()
    programmer_languages = ProgrammerLanguages(programmer_id=programmer.programmer_id,languages_id=language_object.language_id)
    db.session.add(programmer_languages)
    db.session.commit()

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

# def get_language_id(language):
#     """Get language id from language table"""
#     current_language = Languages.query.filter(Languages.language_name == language)

#     return Languages.language_id(current_language)

def does_querie_exist(location, language, min_years_of_experience, max_years_of_experience): 
    "find if there is an existing query"
    db_querie = RecruiterQuery.query.filter(RecruiterQuery.location.like(f'{location}%'),(RecruiterQuery.min_years_of_experience<=min_years_of_experience),(RecruiterQuery.max_years_of_experience>=max_years_of_experience))
    
    if language != '': 
        db_querie = db_querie.filter(RecruiterQuery.language_name == language)
    

    return db_querie.first() is not None
    

def return_results_from_db(location, language, min_years_of_experience, max_years_of_experience):
    "find querie results from the database"
    
    now = datetime.datetime.now()
    min_years_of_experience = now - relativedelta(years=min_years_of_experience)
    print(min_years_of_experience)
    max_years_of_experience = now - relativedelta(years=max_years_of_experience)
    print(max_years_of_experience)

    db_querie = Programmer.query.filter(Programmer.gender==GenderEnum.female.value,
                            Programmer.location.like(f'{location}%'), 
                            and_(Programmer.profile_created_at<= min_years_of_experience,
                            Programmer.profile_created_at>= max_years_of_experience))

    if language != '':
        programmers_matching_language = db.session.query(Programmer).join(ProgrammerLanguages).join(Languages).filter(Languages.language_name == language).all()
        output = []
        for programmer in programmers_matching_language:
            if programmer in db_querie:
                output.append(programmer)
        return set(output)
                            
                          
    return db_querie
  

#   session.query(
#     User
# ).join(
#     Document
# ).join(
#     DocumentsPermissions
# ).filter(
#     User.email == "user@email.com"
# ).all()

# (Programmer, ProgrammerLanguages, Languages
#                             ).filter(Programmer.programmer_id == ProgrammerLanguages.programmer_id
#                             ).filter(ProgrammerLanguages.languages_id == Languages.language_id
#                             ).filter(Languages.language_name == language).group_by(Programmer.programmer_id).subquery()
# session.query(
#     User, 
#     Document, 
#     DocumentsPermissions
# ).filter(
#     User.email == Document.author
# ).filter(
#     Document.name == DocumentsPermissions.document
# ).filter(
#     User.email == "user@email.com"
# ).all()

# SELECT 'all the columns'
# FROM user
# JOIN document ON document.author_id = user.id AND document.author == User.email
# JOIN document_permissions ON document_permissions.document_id = document.id AND document_permissions.document = document.name

# session.query(
#     User
# ).join(
#     Document
# ).join(
#     DocumentsPermissions
# ).filter(
#     User.email == "user@email.com"
# ).all()

# x = db.session.query(
#     Programmer
# ).join(ProgrammerLanguages
# ).join(Languages
# ).filter(Languages.language_name == "language"
# ).all()



    #  humans = set()
    # for animal in (
    #     Animal.query.options(db.joinedload("human"))
    #     .filter_by(animal_species=animal_species)
    #     .all()
    # ):
    #     humans.add(animal.human)

    # return list(humans)

# billing_address = relationship("Address", foreign_keys="Customer.billing_address_id")
# Programmer.programmer_id = Programmer.query(Languages.language_name == language) & (ProgrammerLanguages.languages_id == Languages.language_id)

# emps = db.session.query(Employee,
#                         Department).join(Department).all()
# emps = db.session.query(Employee.name,
#                         Department.dept_name,
#                         Department.phone).join(Department).all()

# rows = session
#     .query(Entity1, Entity2)
#     .join(Entity2, (Entity1.col1==Entity2.col1) & (Entity1.col2==Entity2.col2))
#     .all()

# for name, dept_name, phone in emps:      # [(n, d, p), (n, d, p)]
#     print(name, dept_name, phone)

# select * from programmers p
# left joins programmer_languages pl on p.programmer_id = pl.programmer_id
# left joins languages l on l.language_id = pl.language_id
# where l.language_name = 'Go';


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

def get_fav(user_id):
    """Get favorited programmer objects from the database, given a user id."""

    #lst_of_fav = Favorite.query.filter_by(user_id = user_id).all()
    #join programmers on favorite and return programmer models .query.joinby
    

    return db.session.query(Programmer).join(Favorite, Favorite.programmer_id == Programmer.programmer_id).filter(Favorite.user_id == user_id)

def get_user_by_user_id(user_id):
    """Get user by user id."""

    return User.query.get(user_id)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)