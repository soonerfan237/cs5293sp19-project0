import pytest
import os
import sqlite3
from sqlite3 import Error
import project0
from project0 import main
from project0 import project0

url = "http://normanpd.normanok.gov/content/daily-activity"

def test_createdb():
    db = project0.createdb() #creating database
    assert os.path.isfile(os.getcwd() + "/" + db) #checking if database exists

def test_schema():
    db = project0.createdb() #creating database
    try:
        conn = sqlite3.connect(db) #connecting to database
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table';")#selecting list of tables
        tables = curs.fetchone()
        curs.execute("PRAGMA table_info('arrests');") #getting schema of arrests
        columns = curs.fetchall()
        curs.close()
        conn.close()
    except Error as e:
        print(e)
    assert tables[0] == 'arrests' #checking if arrests table exists
    assert len(columns) == 9 #checking schema
    assert columns[0][1] == 'arrest_time'
    assert columns[1][1] == 'case_number'
    assert columns[2][1] == 'arrest_location'
    assert columns[3][1] == 'offense'
    assert columns[4][1] == 'arrestee_name'
    assert columns[5][1] == 'arrestee_birthday'
    assert columns[6][1] == 'arrestee_address'
    assert columns[7][1] == 'status'
    assert columns[8][1] == 'officer'

def test_status():
    project0.fetchincidents_test('test1') #passing local test pdf file
    incidents = project0.extractincidents() #extracting incidents
    db = project0.createdb() #creating db
    project0.populatedb(db, incidents) #inserting incidents into db
    assert project0.status(db) is not None #checking that status correctly returns a random incident
