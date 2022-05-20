"""Models for find women who code app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A recruiter"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    #email = db.Column(db.String(25), unique=True)
    #password = db.Column(db.String(25))
    #saved_profiles = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id}>'

class RecruiterQuery(db.Model):
    """Search input from user."""

    __tablename__ = "recruiter_queries"
    
    recruiter_query_id = db.Column(db.Integer, 
        autoincrement=True,
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    language_name = db.Column(db.String)
    location = db.Column(db.String)
    country_code = db.Column(db.Integer)
    min_years_of_experience = db.Column(db.Integer)
    max_years_of_experience = db.Column(db.Integer)
    #save_profiles = db.Column(db.String)

    def __repr__(self):
        return f'<RecruiterQuery recruiter_query_id={self.recruiter_query_id}>'

class RecruiterQueryLanguages(db.Model):
    """Many to many association table to handle queries that include multiple languages."""

    __tablename__ = "recruiter_query_languages"

    recruiter_query_languages_id = db.Column(db.Integer, 
    autoincrement=True,
    primary_key=True)
    recruiter_query_id = (db.Integer, db.ForeignKey("recruiter_queries.recruiter_query_id"))
    programming_languages_id = (db.Integer, db.ForeignKey("programming_languages.programming_languages_id"))

    def __repr__(self):
        return f'<RecruiterQueryLanguages recruiter_query_languages_id={self.recruiter_query_languages_id}>'

class Gender(db.Model):
    """Name, assumed gender, probability, count."""

    __tablename__ = "gender"

    gender_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    programmer_id = db.Column(db.Integer, 
                        db.ForeignKey("programmers.programmer_id"))
    first_name = db.Column(db.String)
    assumed_gender = db.Column(db.String)
    count = db.Column(db.Integer)
    probability = db.Column(db.Integer)

    def __repr__(self):
        return f'<Gender programmer_id={self.programmer_id} first_name={self.first_name} assumed_gender={self.assumed_gender}>'

class Languages(db.Model):
    """Id for each language ."""

    __tablename__ = "languages"

    language_id = db.Column(db.Integer,
                            autoincrement= True,
                            primary_key = True)
    language_name = db.Column(db.String)
    # magic attribute:
        # ProgrammerLanguages creates list of ProgrammerLanguages objects

    def __repr__(self):
        return f'<Languages programming_languages_id={self.language_id} language_name={self.language_name}>'

class ProgrammerLanguages(db.Model):
    """Connects multiple languages to multiple programmers
    who may have experience in multiple languages"""

    __tablename__ = "programmer_languages"

    programmer_languages_id = db.Column(db.Integer,
                            autoincrement= True,
                            primary_key = True)
    programmer_id = db.Column(db.Integer, db.ForeignKey("programmers.programmer_id"))
    languages_id = db.Column(db.Integer, db.ForeignKey("languages.language_id"))
    # Relationship tables: 
    programmer = db.relationship("Programmer", backref="programmer_languages")
    language = db.relationship("Languages", backref="programmer_languages")

    def __repr__(self):
        return f'<programmer_languages programmer_languages_id={self.programmer_languages_id} programmer_id={self.programmer_id} languages_id={self.languages_id}>'

class Programmer(db.Model): 
    """Github profile information."""

    __tablename__ = "programmers"

    programmer_id = db.Column(db.Integer,
                            autoincrement= True,
                            primary_key = True)
    login = db.Column(db.String)
    full_name = db.Column(db.String)
    company_name = db.Column(db.String)
    profile_created_at = db.Column(db.DateTime)
    location = db.Column(db.String)
    country = db.Column(db.Integer)
    email = db.Column(db.String)
    twitter_handle = db.Column(db.String)
    # magic attributes:
        # programmer_languages = list of ProgrammerLanguages objects

    def __repr__(self):
        return (f'<programmers programmer_id={self.programmer_id} login={self.login} full_name={self.full_name} profile_created_at={self.profile_created_at} \
        location= {self.location} country= {self.country} email={self.email} twitter_handle={self.twitter_handle}>')


def connect_to_db(flask_app, db_uri="postgresql:///fwwcdb", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)