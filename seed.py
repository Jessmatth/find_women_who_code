import os

import queries
import crud
#from queries import *
#from crud import *
import model
from server import app


os.system("dropdb fwwcdb")
os.system("createdb fwwcdb")

model.connect_to_db(app)
model.db.create_all()

#crud.create_programmers(queries.list_of_named_users)


#crud.create_genders(queries.gen_response)


