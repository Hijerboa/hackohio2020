from configparser import ConfigParser
import os
import psycopg2

from flask import current_app, g

filename = os.path.join(os.getcwd(), 'rona-election', 'db.ini')
# create a parser
parser = ConfigParser()
# read config file
parser.read(filename)

# get section, default to postgresql
section = 'postgresql'
dbconfig = {}
if parser.has_section(section):
    params = parser.items(section)
    for param in params:
        dbconfig[param[0]] = param[1]
else:
    raise Exception('Section {0} not found in the {1} file'.format(section, filename))

def get_db():
    if 'db' not in g:        
        # create the database
        g.db = psycopg2.connect(
            host=dbconfig['host'],
            database=dbconfig['database'],
            user=dbconfig['user'],
            password=dbconfig['password']
        )
        print(g.db)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()