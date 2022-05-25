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
import crud
import model


from github import Github

import os 



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

programmer_experience = minimum_created_at_date(1, 1)


def loop_to_collect_programmers(programmer_experience): 
    """Github API allows 5,000 responses per hour w/ 30 responses per request or 166 queries. 
    This loop is designed to make these queries."""

    
    payload = {'q': {'location': 'San%20Francisco*','created': programmer_experience}}
    headers = {'Authorization': f'token {os.environ["GITHUB_KEY"]}'}

    
    req = requests.get('https://api.github.com/search/users', params=payload, headers=headers)
    read_resp = req.json()
    additional_pages = {}
    output = {**read_resp,  **additional_pages}

    while 'next' in req.links.keys():
        res = requests.get(req.links['next']['url'],headers=headers)
        additional_pages.update(res.json())
    
    return output

passing_programmer_objects = loop_to_collect_programmers(programmer_experience)


# url = "https://api.github.com/XXXX?simple=yes&per_page=100&page=1"
# res=requests.get(url,headers={"Authorization": git_token})
# repos=res.json()
# while 'next' in res.links.keys():
#   res=requests.get(res.links['next']['url'],headers={"Authorization": git_token})
#   repos.extend(res.json())

# some_repos = user.get_repos().get_page(0)
# some_other_repos = user.get_repos().get_page(3)

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
    for item in passing_programmer_objects['items']:
        login_list.append(item['login'])
      
    
    return login_list

login_vist_var = get_logins_from_API_response(passing_programmer_objects)

def using_querie_functions(login_vist_var):
    """Take logins and get programmer objects."""
    programmer = []
    for login in login_vist_var:
        user_profile = g.get_user(login)
        programmer.append(user_profile)

    return programmer

list_of_named_users = using_querie_functions(login_vist_var)


#list_of_named_users is a list of programmer objects
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

#first_list_of_ten = list_of_first_names[0:10]

# Define a function that takes in a list of names
# takes the names in 10 unit increments 
# and makes a query and saves the results
# until there are no more names

def get_gender(list_of_first_names): 
    """Takes in a list of names and makes queries in batches of 10 to generizer."""
    
    i = 0
    list_of_ten = []
    output_list = []

    for i in list_of_first_names: 
        if i <= 10:
            list_of_ten.append(list_of_first_names[i])
            i += 1
        elif i > 10:
            name_list = {'name': [list_of_ten]}
            r = requests.get('https://api.genderize.io/', params=name_list)
            gen_response = r.json()
            output_list.append(gen_response)
            i = 0

    return output_list

    # https://api.genderize.io/?name[]=peter&name[]=lois&name[]=stevie

#gen_payload = {'name': 'peter', 'gender': 'male, 'probability': '.99', 'count': '1234'}


#gen_req = requests.get('https://api.genderize.io/?', params=gen_payload)

#payload = {'name': 'peter'}
#r = requests.get('https://httpbin.org/get', params=first_list_of_ten)

#python.sleep(.5)

#name_list = {'name': [first_list_of_ten]}
#r = requests.get('https://api.genderize.io/', params=name_list)

#gen_response = r.json()

#model.db.session.add_all(gen_response)  
#model.db.session.commit() 


# inputs: genderizer: Name, gender, programmer objects 
# output: combination
def find_women(gen_response):
    output = []
    for item in gen_response:
        for key in item:
            if key == 'gender' and item[key] == 'male':
                output.append(item['name'])

    return output

women_names = find_women(gen_response)

def search_response(women_names, list_of_named_users):
    identified_profiles = []

     
    for named_user in list_of_named_users: 
        print(named_user.name)
        if named_user.name and named_user.name.split(" ", 1)[0] in women_names: 
            identified_profiles.append(named_user)


    return identified_profiles


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
