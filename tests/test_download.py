import pytest

import project0
from project0 import main
from project0 import project0

url = "http://normanpd.normanok.gov/content/daily-activity"

def test_fetchincidents():
    links = project0.fetchincidents(url)
    incidents = project0.extractincidents(links) 
    assert links is not None
    assert incidents is not None
