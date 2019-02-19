import pytest
import os
import project0
from project0 import main
from project0 import project0

def test_extract_request():
    project0.fetchincidents_test('test1') #fetching local test file
    incidents = project0.extractincidents() #extracting incidents
    db = project0.createdb() #creating database
    project0.populatedb(db, incidents) #populating database
    assert len(incidents) == 15 #verifying correct number of incidents is extracted
    assert incidents[14][8][0:4] == '1813' #verifying the correct fields are parsed from the file
    assert incidents[14][5] == '8/31/1977'
    assert incidents[0][0][0:9] == '2/14/2019'
    assert incidents[0][8][0:4] == '1827'
