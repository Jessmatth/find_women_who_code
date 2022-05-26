import os
from flask import (Flask, render_template, request, flash, session,
                   redirect)
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



@app.route('/search')
def show_results():
    """Display search results"""

    location = request.args.get('location', '')
    min_years_of_experience = request.args.get('min_years_of_experience', '')
    max_years_of_experience = request.args.get('max_years_of_experience', '')

    programmer_experience = queries.minimum_created_at_date(min_years_of_experience, max_years_of_experience)
    passing_programmer_objects = queries.loop_to_collect_programmers(programmer_experience, location)
    login_vist_var = queries.get_logins_from_API_response(passing_programmer_objects)
    list_of_named_users = queries.using_querie_functions(login_vist_var)
    list_of_first_names = queries.get_first_name(login_vist_var)
    gen_response = queries.get_gender(list_of_first_names)
    women_names = queries.find_women(gen_response)
    output_programmers = queries.search_response(women_names, list_of_named_users)


    return render_template('search_results.html', data=output_programmers)




if __name__ == '__main__':
    connect_to_db(app)
    app.run('0.0.0.0', debug=True)