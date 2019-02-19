import pytest
import os
import project0
from project0 import main
from project0 import project0

def test_extract_request():
    project0.fetchincidents_test('test1') #fetching local test file
    incidents = project0.extractincidents() #extracting incidents
    for incident in incidents:
        for field in incidents:
            print(field)
    db = project0.createdb() #creating database
    project0.populatedb(db, incidents) #populating database
    assert len(incidents) == 15 #verifying correct number of incidents is extracted

