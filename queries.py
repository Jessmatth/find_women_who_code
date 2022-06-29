"""Python Github queries for programmer data."""
from imaplib import _Authenticator
from operator import mod
from re import L
from socket import TCP_NODELAY
from urllib import response

import requests
import json

import datetime
import pickle
import time

import crud
import model
import server
import numpy


from github import Github

import os 

import pdb

# using an access token
g = Github(os.environ["GITHUB_KEY"])



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

def create_github_created_at_date(years_experience):
    """This function takes user input for number of years of experience and creates a github creation date."""
    
    now = datetime.datetime.now().isoformat()
    now = now[:10]
    year_digits = now[2:4]
    
    
    if years_experience:
        year_digits = int(year_digits)
        output_github_date = year_digits - years_experience
        output_github_date = now[0:2]+ str(output_github_date) + now[4:]
        
    return (f"{output_github_date}")

def loop_to_collect_programmers(location, language): 
    """Github API allows 5,000 responses per hour w/ 100 responses per page or  queries. 
    This loop is designed to make these queries."""
    
    crud.create_language(language)
    page = 1
    headers = {'Authorization': f'token {os.environ["GITHUB_KEY"]}'}
    output = []
    
    req = requests.get(f'https://api.github.com/search/users?q=location:{location}+language:{language}&page={page}&per_page=100', headers=headers)
    read_resp = req.json()
    
    total_count = read_resp["total_count"]

    if total_count == 0: 
        return output
    else: 
        total_pages = numpy.ceil(total_count/100)
        if 'items' not in read_resp: 
                print(read_resp['message'])
                return output
        output.append(read_resp)
        

        while len(output) < total_pages:
        #req = requests.get('https://api.github.com/search/users', params=payload, headers=headers) since=100000000&per_page=100
            page += 1
            req = requests.get(f'https://api.github.com/search/users?q=location:{location}&page={page}&per_page=100', headers=headers)       
            read_resp = req.json()
            if 'items' not in read_resp: 
                break
            output.append(read_resp)
            
        

    return output




# def collect_programmers(payload, headers):
#     another_page = True
#     results = []
#     api = 'https://api.github.com/search/users'
#     while another_page: #the list of teams is paginated
#         r = requests.get(api, params=payload, auth=headers)
#         json_response = json.loads(r.text)
#         results.append(json_response)
#         if 'next' in r.links: #check if there is another page of organisations
#             api = r.links['next']['url']
#         else:
#             another_page=False

#     return results


def get_logins_from_API_response(passing_programmer_objects):
    """Loops through the response text to generate a list of logins that match the search criteria."""

    login_list =[]
    for page in passing_programmer_objects:
        for item in page['items']:
            login_list.append(item['login'])
      
    
    return login_list



def using_querie_functions(login_vist_var, min_years_of_experience, max_years_of_experience):
    """Take logins and get programmer objects."""
    programmers = []
    output = []
    for login in login_vist_var:
        user_profile = g.get_user(login)
        programmers.append(user_profile)

    programmer_objects = crud.create_programmers(programmers)
    
    now = datetime.datetime.now().isoformat()
    now = now[:10]
    year_digits = now[2:4]
    num_year_digits = int(year_digits)
    print("This is the programmer_objects", programmer_objects)

    for programmer_object in programmer_objects: 
        print("this is the programmer_object", programmer_object)
        experience = programmer_object.profile_created_at
        experience = experience.strftime("%Y")
        experience = experience[2:4]
        num_experience = int(experience)
        
        num_experience = num_year_digits - num_experience
        print(num_experience)

        if min_years_of_experience <= num_experience <= max_years_of_experience: 
            print(num_experience)
            print(type(num_experience))
            output.append(programmer_object)
    print("filered by experience:", output)
    return output

def get_user_profile(git_hub_login):
    """Takes in git_hub login and returns git_hub programmer object."""
    print(git_hub_login)
    user_profile = g.get_user(git_hub_login)

    return user_profile


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



def get_gender(list_of_first_names): 
    """Takes in a list of names and makes queries in batches of 10 to generizer."""
    
    #headers = {'Authorization': f'token {os.environ["GENDERIZER_KEY"]}'}
    authorization = f'&apikey={os.environ["GENDERIZER_KEY"]}'

    i = 0
    list_of_ten = []
    output_list = []
   
    for i in range(len(list_of_first_names)): 
        list_of_ten.append(list_of_first_names[i])

        if len(list_of_ten) == 10:
            params = {'name': list_of_ten, 'apikey': os.environ["GENDERIZER_KEY"]}
            r = requests.get('https://api.genderize.io/', params=params)
            gen_response = r.json()
            output_list.append(gen_response)
            list_of_ten = []
    
    crud.create_genders(output_list)

    return output_list

    # https://api.genderize.io/?name[]=peter&name[]=lois&name[]=stevie

#gen_payload = {'name': 'peter', 'gender': 'male, 'probability': '.99', 'count': '1234'}



#model.db.session.add_all(gen_response)  
#model.db.session.commit() 


#db.session.add(gen_response)     
#db.session.commit() 
# def committ_prog_gen_info():
#     """Calls crud functions to insert data into db."""
#     with app.app_context():
#         crud.create_genders(gen_response)
#         crud.create_programmers(list_of_named_users)

#     return "data inserted in gender and programmer tables"

# committ_prog_gen_info()
# # inputs: genderizer: Name, gender, programmer objects 
# # output: combination
def find_women(gen_response):
    output = []
    for batch in gen_response:
        for item in batch:
            if item['gender'] == 'female':
                output.append(item['name'])

    return output



def search_response(women_names, list_of_programmer_objects, language):
    """initialize a new list and append with users."""
    print("women's names:", women_names)


    output= []
    for programmer_object in list_of_programmer_objects: 
        print(programmer_object.full_name)
        if programmer_object.full_name and programmer_object.full_name.split(" ", 1)[0] in women_names: 
            output.append(programmer_object)
            crud.update_programer_gender(programmer_object, model.GenderEnum.female.value)    
            crud.create_programmer_language(programmer_object, language)

    return output

def call_functions(location, language, min_years_of_experience, max_years_of_experience):
    """Calls all functions in queries"""
    #programmer_experience = minimum_created_at_date(min_years_of_experience, max_years_of_experience)
    passing_programmer_objects = loop_to_collect_programmers(location, language)
    login_vist_var = get_logins_from_API_response(passing_programmer_objects)
    list_of_programmer_objects = using_querie_functions(login_vist_var, min_years_of_experience, max_years_of_experience)
    list_of_first_names = get_first_name(login_vist_var)
    gen_response = get_gender(list_of_first_names)
    women_names = find_women(gen_response)
    output_programmers = search_response(women_names, list_of_programmer_objects, language)
    #output = optional_print(output_programmers)
    #print(output)

    return output_programmers

# def optional_print(ouput_programmers): 
#     list_of_output_str = []

#     for named_user in output_programmers:
#         profile = (f'name: {named_user.name} email:{named_user.email} company: {named_user.company} login: {named_user.login} location: {named_user.location} twitter: {named_user.twitter_username}')
#         list_of_output_str.append(profile)
    
#     return list_of_output_str

#Create a function to add programmer_id to gender table for programmers in DB.




# def return_search_results(list_of_named_users, identified_profiles): 
#     """Takes in a list of full names and returns programmer information."""
#     #match = any(profile.name in name for profile.name in list_of_named_users for name in identified_profiles)

#     for i in list_of_named_users: 
#         name = i.name
#         for profile in identified_profiles: 
#             if name == profile: 
#                 return (f'name: {profile.name} email:{profile.email} company: {profile.company} login: {profile.login} location: {profile.location} twitter: {profile.twitter_username}')
#             else: 
#                 return ("No results")


#search_results = return_search_results(list_of_named_users, output)
#print(search_results)
        # for key, value in gen_response.item: 
        #     if key == 'gender' and value == 'male': 
        #         print(item['name'])
    #         if gen_response[key] == 'male': 
    #             output.append(gen_response['name'])
    # return output
# for d in my_list:
#     for key in d:
#         print d[key]

    # login_list =[]
    # for item in passing_programmer_objects[0]['items']:
    #     login_list.append(item['login'])

# Genderizer rate limit is 1,000 names per day, each query can contain 10 names. 
# Github rate limit 5,000 requests per hour, default is to return 30.  I believe there is a way to change it to 100. 


# Match the genderizer responses to github data. 
# Filter out the presumed women. 
# create query to get languages
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    model.connect_to_db(app)