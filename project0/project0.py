import urllib.request

def fetchincidents(url):
    print("fetching incidents for " + url)
    data = urllib.request.urlopen(url).read()
    print(data)

def extractincidents():
    print("extracting incidents")

def createdb():
    print("creating db")

def populatedb(db, incidents):
    print("populating db")

def status(db):
    print("status: getting random row")
