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

    #Check if I have programmers in the database and return them if I do. 
    #If not, call the queries that call functions
 
    output_programmers = queries.call_functions(location, min_years_of_experience, max_years_of_experience)

    return render_template('search_results.html', data=output_programmers)





if __name__ == '__main__':
    connect_to_db(app)
    app.run('0.0.0.0', debug=True)