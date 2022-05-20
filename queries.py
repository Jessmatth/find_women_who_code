"""Python Github queries for programmer data."""
from imaplib import _Authenticator
from socket import TCP_NODELAY
from urllib import response

import requests
import json

import datetime
import pickle
import time

import jwt
import requests

from github import Github

# using an access token
g = Github("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")



def minimum_created_at_date(min_experience, max_experience):
    """This function takes a range of years of experience from the query and creates the search parameter for created_at."""
    
    now = datetime.datetime.now().isoformat()
    now = now[:10]
    year_digits = now[2:4]

    
    if max_experience and min_experience:
        year_digits = int(year_digits)
        min_year_digits = year_digits - min_experience   
        max_year_digits = year_digits - max_experience
        min_query_date = now[0:2]+ str(min_year_digits) + now[4:]
        max_query_date = now[0:2]+ str(max_year_digits) + now[4:]
        

        return (f"{max_query_date}..{min_query_date}")

programmer_experience = minimum_created_at_date(1, 14)



def loop_to_collect_programmers(programmer_experience): 
    """Github API allows 5,000 responses per hour w/ 30 responses per request or 166 queries. 
    This loop is designed to make these queries."""

    response_output = []
    payload = {'q': {'location': 'San Francisco','created': programmer_experience}}
    
    for i in range(0,10): 
        req = requests.get('https://api.github.com/search/users', params=payload) 
        read_resp = req.json()
        response_output.append(read_resp)
    
    return response_output

passing_programmer_objects = loop_to_collect_programmers(programmer_experience)

def get_logins_from_API_response(passing_programmer_objects):
    """Loops through the response text to generate a list of logins that match the search criteria."""

    i = 1
    login_list = []

    while i < len(passing_programmer_objects):
        import pdb;pdb.set_trace() 
        l = passing_programmer_objects['items'][i]['login']
        login_list.append(l)
        i += 1
    
    return login_list

login_vist_var = get_logins_from_API_response(passing_programmer_objects)

def using_querie_functions(login_vist_var):
    """Take logins and get programmer objects."""
    programmer = []
    for login in login_vist_var:
        user_profile = g.get_user(login)
        programmer.append(user_profile)

    return programmer

programmer_objects = using_querie_functions(login_vist_var)
#req = requests.get('https://api.github.com/search/users', params=payload) 

#response = req.json()


def get_first_name(login_vist_var): 
    full_names = []
    first_name = []
    for item in login_vist_var:
        user = g.get_user(item)
        if user is not None: 
            full_names.append(user.name)
    
    for name in full_names:
        if name: 
            get_first_name = name.split(" ", 1)
            first_name.append(get_first_name[0])
    
    return first_name


list_of_first_names = get_first_name(login_vist_var)

first_list_of_ten = list_of_first_names[0:10]
    # https://api.genderize.io/?name[]=peter&name[]=lois&name[]=stevie

#gen_payload = {'name': 'peter', 'gender': 'male, 'probability': '.99', 'count': '1234'}


#gen_req = requests.get('https://api.genderize.io/?', params=gen_payload)

#payload = {'name': 'peter'}
#r = requests.get('https://httpbin.org/get', params=first_list_of_ten)

#python.sleep(.5)

name_list = {'name': [first_list_of_ten]}
r = requests.get('https://api.genderize.io/', params=name_list)

gen_response = r.json()

# Genderizer rate limit is 1,000 names per day, each query can contain 10 names. 
# Github rate limit 5,000 requests per hour, default is to return 30.  I believe there is a way to change it to 100. 


# Match the genderizer responses to github data. 
# Filter out the presumed women. 
# create query to get languages
