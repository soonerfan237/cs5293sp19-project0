import pytest
import os
import sqlite3
from sqlite3 import Error

import project0
from project0 import main
from project0 import project0

url = "http://normanpd.normanok.gov/content/daily-activity"

def test_createdb():
    db = project0.createdb()
    assert os.path.isfile(os.getcwd() + "/" + db)

def test_schema():
    db = project0.createdb()
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = curs.fetchone()
        curs.execute("PRAGMA table_info('arrests');")
        columns = curs.fetchall()
        curs.close()
        conn.close()
    except Error as e:
        print(e)
    assert tables[0] == 'arrests'
    assert len(columns) == 9
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
    project0.fetchincidents_test('test1')
    incidents = project0.extractincidents()
    db = project0.createdb()
    project0.populatedb(db, incidents)
    assert project0.status(db) is not None
