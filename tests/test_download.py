import pytest
import project0
from project0 import main
from project0 import project0

def test_fetchincidents():
    project0.fetchincidents_test('test1') #passing local test file to fetch incidents
    incidents = project0.extractincidents() #extracting incidents
    assert incidents is not None #checking that incidents are extracted
