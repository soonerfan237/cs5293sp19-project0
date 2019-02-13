import pytest
import os
import project0
from project0 import main
from project0 import project0

def test_extract_request():
    test_str = ''
    with open(os.getcwd() + '/tests/files/test1.txt','r') as testfile:
        test_str = testfile.read()
    incidents = project0.parseincidents(test_str)
    for incident in incidents:
        print("----------------INCIDENT-----------------")
        for field in incident:
            print("FIELD: " + field)
    print(" ")
    print("NUMBER OF INCIDENTS: " + str(len(incidents)))
    db = project0.createdb()
    project0.populatedb(db, incidents)
    assert 1 == 2

