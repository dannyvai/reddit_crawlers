import cPickle as pickle
import secret_keys

db_name =  'db.p'


database = None

def load_database():
    global database,db_name
    try:
        database = pickle.load( open(db_name , 'rb') )
    except:
        database = []


def save_database():
    global database,db_name
    pickle.dump(database , open(db_name , 'wb'))

def add_to_database(key):
    global database
    database.append(key)

def is_in_db(key):
    return key in database
