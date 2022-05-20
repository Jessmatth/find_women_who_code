#import queries
#import crud
from queries import *
from crud import *
import model
from server import app

model.connect_to_db(app)
model.db.create_all()


def commit_programmer(programmer_objects):

    programmer_in_db = []
    for programmer in programmer_objects: 
        if get_programmer_by_login(Programmer.login) is None: 
            programmer_in_db.append(programmer)
        
    return programmer_in_db

seed_programmer = commit_programmer(programmer_objects)
model.db.session.add_all(seed_programmer)  
model.db.session.commit() 


