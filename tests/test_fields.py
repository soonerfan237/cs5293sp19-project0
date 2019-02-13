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
        for field in incidents:
            print(field)
    db = project0.createdb()
    project0.populatedb(db, incidents)
    assert len(incidents) == 14

