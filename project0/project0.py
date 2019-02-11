import urllib.request
from PyPDF2 import PdfFileReader
import tempfile
from bs4 import BeautifulSoup
import re
import sqlite3
from sqlite3 import Error

links = []
incidents = []
normanpd_domain = "http://normanpd.normanok.gov"

def fetchincidents(url):
    print("fetching incidents for " + url)
    html = urllib.request.urlopen(url).read()
    #print(html)
    soup = BeautifulSoup(html)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.find('.pdf') != -1 and href.find('Arrest') != -1:
            links.append(normanpd_domain + href)

    #for link in links:
    #    print(link)

def extractincidents():
    print("extracting incidents")
    for link in links:
        print(link)
        fp = tempfile.TemporaryFile()

        # Write the pdf data to a temp file
        data = urllib.request.urlopen(link).read()
        #print(data)
        fp.write(data)

        # Set the curser of the file back to the begining
        fp.seek(0)

        # Read the PDF
        pdfReader = PdfFileReader(fp)
        pdfReader.getNumPages()

        # Get the first page
        page1 = pdfReader.getPage(0).extractText()
        page1_incidents = page1.split(";")
        for line in page1_incidents:
            print(line)
            #incidenttuple
        #for incident in page1_incidents:
        #    print(incident)
        #    incident_tuple = tuple(incident.splitlines())
        #    incident_tuple_fix = (incident_tuple[1],incident_tuple[2],incident_tuple[3],incident_tuple[4],incident_tuple[5],incident_tuple[6],incident_tuple[7] + incident_tuple[8] + incident_tuple[9] + incident_tuple[10],incident_tuple[11],incident_tuple[12])
        #    incidents.append(incident_tuple_fix)
        #print(page1)
    #for incident in incidents:
    #    print(incident)
        

def createdb():
    print("creating db")
    try:
        conn = sqlite3.connect("normanpd.db")
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        #curs.execute("DROP TABLE arrests")
        curs.execute("""CREATE TABLE arrests (arrest_time TEXT,case_number TEXT,arrest_location TEXT,offense TEXT,arrestee_name TEXT,arrestee_birthday TEXT,arrestee_address TEXT,status TEXT,officer TEXT);""")
        conn.close()
    except Error as e:
        print(e)

def populatedb():
    print("populating db")
    try:
        conn = sqlite3.connect("normanpd.db")
    except Error as e:
        print(e)
    
    try:
        curs = conn.cursor()
        curs.execute("INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?)", ("1","1","1","1","1","1","1","1","1"))
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


def status():
    print("status: getting random row")
    try:
        conn = sqlite3.connect("normanpd.db")
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        curs.execute("SELECT * FROM arrests;")
        rows = curs.fetchall()
        conn.close()
        for row in rows:
            print(row)
    except Error as e:
        print(e)
