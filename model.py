"""Models for find women who code app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A recruiter"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    saved_profiles = db.Column(db.String)

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
    years_of_experience = db.Column(db.Range)
    save_profiles = db.Column(db.String)
    