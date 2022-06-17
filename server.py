import os
from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
from model import connect_to_db, db
import crud
import queries
from jinja2 import StrictUndefined
import requests

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


app = Flask(__name__)




@app.route('/')
def home():
    """Display search boxes."""

    return render_template('home.html')

@app.route('/search/userinput', methods=['POST'])
def get_user_inputs():
    """Collect search criteria and show results. """

    location = request.form.get('location', '')
    min_years_of_experience = int(request.form.get('min_experience', '0'))
    max_years_of_experience = int(request.form.get('max_experience', '14'))
    print("*******************************************************" +location)
    print(min_years_of_experience)
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++" ,max_years_of_experience)
    #Call the crud function for recruiter query.  If it exists, query db. 
    # fetch programmers from db.
    # if not insert this query to the db. Queries.call function.  
    # write a new db query in CRUD. 
    # github user foreign key to map to gender 
    #Check if I have programmers in the database and then check the gender table if to find female matches. 
    #If not, call the queries that call functions
    #if location in postgresql:///fwwcdb:
    does_exist = crud.does_querie_exist(location, min_years_of_experience,max_years_of_experience)
    print(does_exist)
    if does_exist:
        output_programmers = crud.return_results_from_db(location, min_years_of_experience,max_years_of_experience)
     
    else:
        crud.create_recruiter_querie(None, location, min_years_of_experience, max_years_of_experience)
        output_programmers = queries.call_functions(location, min_years_of_experience, max_years_of_experience)
        
    return render_template('search_results.html', data=output_programmers)

@app.route('/add_your_data', methods=['GET'])
def enter_add_your_data():
    """Supports navigation from home to add your data."""

    return render_template('input.html')

@app.route('/add_your_data', methods=['POST'])
def add_your_data():
    """Collect user input and add to the database. """
    # name = request.form.get('name', '')
    git_hub_login = request.form.get('git_hub_login', '')
    gender = request.form.get('gender', '')
    # company = request.form.get('company', '')
    # location = request.form.get('location', '')
    # years_experience = request.form.get('years_experience', '')
    # email = request.form.get('email', '')
    # twitter_handle = request.form.get('twitter_handle', '')
    print('****************************************')
    print(git_hub_login)
    gh_profile = queries.get_user_profile(git_hub_login)
    user_added_data = crud.create_prog_frm_user_input(gh_profile, gender)
    crud.update_programer_gender(user_added_data[2], gender)
    #profile_created_at = queries.create_github_created_at_date(years_experience)

    return render_template('input.html', data=user_added_data)

@app.route('/favorite_programmers/<programmer_id>', methods=['POST'])
def add_favorite_programmers(programmer_id):
    """Show favorite programmer profiles."""
    #to do: save user_id in session
    user = crud.get_first_user()
    crud.create_fav(user.user_id, programmer_id)

    return 'success', 200

if __name__ == '__main__':
    connect_to_db(app)
    app.run('0.0.0.0', debug=True)