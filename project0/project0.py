import urllib.request
from PyPDF2 import PdfFileReader
import tempfile
from bs4 import BeautifulSoup
import re
import sqlite3
from sqlite3 import Error
import re

#links = []
#incidents = []
normanpd_domain = "http://normanpd.normanok.gov"

def fetchincidents(url):
    print("fetching incidents for " + url)
    links = []
    html = urllib.request.urlopen(url).read()
    #print(html)
    soup = BeautifulSoup(html,features="html.parser")
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.find('.pdf') != -1 and href.find('Arrest') != -1:
            links.append(normanpd_domain + href)
    return links
    #for link in links:
    #    print(link)

def extractincidents(links):
    print("extracting incidents")
    incidents = []
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
            line_split = tuple(line.splitlines()) #splitting on line breaks
            arrest_time = line_split[1] #this element corresponds to arrest time column
            case_number = line_split[2] #this element corresponds to case number
            #status = line_split[-2] #second to last element is usually status
            #if status.find("Citation") != -1: #citation status goes onto 2 lines, so we need to handle that separately
                #status = line_split[-3] + line_split[-2]
            officer_search = re.search(r'(\d{4} - \n?\w+)',line)
            if officer_search:
                officer = officer_search.group(1)
            else:
                officer = line_split[-1] #defualt to last column
            if officer.find('\n') != -1: #if officer takes up 2 lines
                status = line_split[-3]
                if status.find("Citation") != -1:
                    status = line_split[-4] + line_split[-3]
            else:
                status = line_split[-2]
                if status.find("Citation") != -1:
                    status = line_split[-3] + line_split[-2]
            officer = officer.replace('\n'," ")
            arrest_location = ''
            offense = ''
            arrestee_birthday = re.search(r'\n(\d+/\d+/\d{4})\n',line).group(1)
            arrestee_address = line[line.find(arrestee_birthday) + len(arrestee_birthday):line.find(status[0:5])] #only using a substring of status here because things break when status is multiline
            arrestee_address = arrestee_address.replace('\n'," ")
            arrestee_address = arrestee_address.strip()
            arrest_location_offense_name = line[line.find(case_number) + len(case_number):line.find(arrestee_birthday)]
            arrest_location_offense_name = arrest_location_offense_name.strip('\n')
            arrest_location_offense_name_split = arrest_location_offense_name.splitlines()
            if len(arrest_location_offense_name_split) == 3: #if there are only 3 fields here, we know what each one is
                arrest_location = arrest_location_offense_name_split[0]
                offense  = arrest_location_offense_name_split[1]
                arrestee_name = arrest_location_offense_name_split[2]
            else: #if more than 3 fields, we have to find which lines correspond to which field
                if ' ' in arrest_location_offense_name_split[-2][-1:]: #if a line ends in a space we know it is because it bleeds over into the next line. so if the second to last line ends in a space we know the name is contained in the two columns here.
                    arrestee_name = arrest_location_offense_name_split[-2] + arrest_location_offense_name_split[-1]
                else: #the name is just one line in length
                    arrestee_name = arrest_location_offense_name_split[-1]
                if ' ' in arrest_location_offense_name_split[0][-1:]:
                    arrest_location = arrest_location_offense_name_split[0] + arrest_location_offense_name_split[1]
                    offense = arrest_location_offense_name[len(arrest_location_offense_name_split[0]) + len(arrest_location_offense_name_split[1]) + 1:arrest_location_offense_name.find(arrestee_name[:5])]
                else:
                    arrest_location = arrest_location_offense_name_split[0]
                    offense = arrest_location_offense_name[arrest_location_offense_name.find(arrest_location) + len(arrest_location):arrest_location_offense_name.find(arrestee_name[:5])]
            offense = offense.strip('\n')
            offense = offense.replace('\n'," ")
            arrest_location = arrest_location.replace('\n'," ")
            incident = (arrest_time, case_number, arrest_location, offense, arrestee_name, arrestee_birthday, arrestee_address, status, officer)
            incidents.append(incident)
    return incidents

def createdb():
    print("creating db")
    db = "normanpd.db"
    try:
        conn = sqlite3.connect(db)
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
    return db

def populatedb(db, incidents):
    print("populating db")
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    try:
        curs = conn.cursor()
        for incident in incidents:
            curs.execute("INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?)", incident)

        conn.commit()
        conn.close()
    except Error as e:
        print(e)

def status(db):
    print("status: getting random row")
    result = ''
    try:
        conn = sqlite3.connect(db)
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
    return result
