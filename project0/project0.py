import urllib.request
from PyPDF2 import PdfFileReader
import tempfile
from bs4 import BeautifulSoup
import re
import sqlite3
from sqlite3 import Error
import re

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
        #print(page1)
        page1_incidents = page1.split(";")
        for line in page1_incidents[1:-1]: #excluding first element which is null and last element which is a header in the pdf
            line_withoutheader = re.search(r'Officer()',line)
            if line_withoutheader:
                line = line_withoutheader.group(1)
            print("LINE: " + line)
            line_split = tuple(line.splitlines())
            arrest_time = line_split[1]
            case_number = ''
            arrest_location = ''
            offense = ''
            arrestee_name = ''
            arrestee_birthday = ''
            arrestee_address = ''
            status = ''
            officer = ''
            incident = (arrest_time, case_number, arrest_location, offense, arrestee_name, arrestee_birthday, arrestee_address, status, officer)
            incidents.append(incident)
            #populatedb(incident)
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
        curs.execute("DROP TABLE arrests;")
        conn.commit()
        curs.execute("""CREATE TABLE arrests (arrest_time TEXT,case_number TEXT,arrest_location TEXT,offense TEXT,arrestee_name TEXT,arrestee_birthday TEXT,arrestee_address TEXT,status TEXT,officer TEXT);""")
        conn.commit()
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
        #curs.execute("INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?)", ("1","1","1","1","1","1","1","1","1"))
        for incident in incidents:
            curs.execute("INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?)", incident)

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
        curs.execute("SELECT * FROM arrests ORDER BY RANDOM();")
        rows = curs.fetchone()
        conn.close()
        result = ""
        for row in rows:
            result = result + 'þ' + row
        result = result[1:]
        print(result)
    except Error as e:
        print(e)
