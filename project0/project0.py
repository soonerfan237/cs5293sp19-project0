import urllib.request
from PyPDF2 import PdfFileReader
import tempfile
import re
import sqlite3
from sqlite3 import Error
import re
import os

def fetchincidents(url): #method takes url of single pdf as argument
    print("fetching incidents for " + url)
    data = urllib.request.urlopen(url).read() #reading bytes from url
    with open(os.getcwd() + '/tmp/output', 'wb') as output:
        output.write(data) #writing bytes to tmp folder

def fetchincidents_test(test_file): #this method is only used for testing the subsequent methods
    os.popen('cp /tests/files/' + test_file + ' /tmp/output') #copies a local test pdf to the output folder to be used in later methods

def extractincidents(): #method to extract incidents
    print("extracting incidents")
    fp = tempfile.TemporaryFile()

    # Write the pdf data to a temp file
    data = open(os.getcwd() + '/tmp/output', 'rb').read()
    fp.write(data)

    # Set the curser of the file back to the begining
    fp.seek(0)

    # Read the PDF
    pdfReader = PdfFileReader(fp)
    pdfReader.getNumPages()

    # Get the first page
    page1 = pdfReader.getPage(0).extractText()

#def parseincidents(page1):
    incidents = [] #initializing list of incidents
    page1_incidents = page1.split(";") #splitting rows on semicolon
    for line in page1_incidents[0:-1]: #excluding last element which is a header in the pdf
        if line.find('Officer') > 0: #if i find Officer in the line, I know it is part of a header line
            line = line[line.find('Officer') + len('Officer'):] #taking substring to remove the header portion of the line
        line_split = tuple(line.splitlines()) #splitting on line breaks
        arrest_time = line_split[1] #this element corresponds to arrest time column
        case_number = line_split[2] #this element corresponds to case number
        officer_search = re.search(r'(\d{4} - \n?\w+)',line) #regex to look for officer code - name
        if officer_search: #if it finds officer
            officer = officer_search.group(1) #save string to officer
        else: #if officer not found with regex
            officer = line_split[-1] #defualt to last column
        if officer.find('\n') != -1: #if officer takes up 2 lines
            status = line_split[-3] #then get status here
            if status.find("Citation") != -1: #if status includes Citation it will spill onto mutliple lines
                status = line_split[-4] + line_split[-3] #grab contents at both locations
        else: #if officer only takes up 1 line
            status = line_split[-2] #then get status here
            if status.find("Citation") != -1: #if status includes Citation it will spill onto multiple lines
                status = line_split[-3] + line_split[-2] #grab status at both locations
        officer = officer.replace('\n'," ") #replace new lines with space
        arrest_location = '' #initialize arrest location
        offense = '' #initialize offense
        arrestee_birthday = re.search(r'\n(\d+/\d+/\d{4})\n',line).group(1) #regex to parse for birthday date
        arrestee_address = line[line.find(arrestee_birthday) + len(arrestee_birthday):line.find(status[0:5])] #only using a substring of status here because things break when status is multiline
        arrestee_address = arrestee_address.replace('\n'," ") #replacing new line with space
        arrestee_address = arrestee_address.strip() #removing unnecessary spaces
        arrest_location_offense_name = line[line.find(case_number) + len(case_number):line.find(arrestee_birthday)] #this variable holds the portion of the string that contains arrest location, offense and arrestee name
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
            if ' ' in arrest_location_offense_name_split[0][-1:]: #if it contains a space at the end of the line we know it bleeds onto next line
                arrest_location = arrest_location_offense_name_split[0] + arrest_location_offense_name_split[1]
                offense = arrest_location_offense_name[len(arrest_location_offense_name_split[0]) + len(arrest_location_offense_name_split[1]) + 1:arrest_location_offense_name.find(arrestee_name[:5])]
            else: #only on one line
                arrest_location = arrest_location_offense_name_split[0]
                offense = arrest_location_offense_name[arrest_location_offense_name.find(arrest_location) + len(arrest_location):arrest_location_offense_name.find(arrestee_name[:5])]
        offense = offense.strip('\n')
        offense = offense.replace('\n'," ")
        arrest_location = arrest_location.replace('\n'," ")
        incident = (arrest_time, case_number, arrest_location, offense, arrestee_name, arrestee_birthday, arrestee_address, status, officer)
        incidents.append(incident) #appending the incident to the list
    return incidents #return the list of incidents

def createdb():
    print("creating db")
    db = "normanpd.db" #setting db name
    try:
        conn = sqlite3.connect(db) #connecting to db
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        curs.execute("DROP TABLE arrests;") #dropping old table if it previously existed
        conn.commit() #commiting drop
        curs.execute("""CREATE TABLE arrests (arrest_time TEXT,case_number TEXT,arrest_location TEXT,offense TEXT,arrestee_name TEXT,arrestee_birthday TEXT,arrestee_address TEXT,status TEXT,officer TEXT);""") #creating fresh table
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
    return db

def populatedb(db, incidents): #populating database with incidents
    print("populating db")
    try:
        conn = sqlite3.connect(db) #connecting to database
    except Error as e:
        print(e)
    
    try:
        curs = conn.cursor()
        for incident in incidents: #looping through incidents
            curs.execute("INSERT INTO arrests VALUES (?,?,?,?,?,?,?,?,?)", incident) #inserting incident values
        conn.commit()
        conn.close()
    except Error as e:
        print(e)

def status(db):
    print("status: getting random row")
    result = ''
    try:
        conn = sqlite3.connect(db) #connecting to database
    except Error as e:
        print(e)

    try:
        curs = conn.cursor()
        curs.execute("SELECT * FROM arrests ORDER BY RANDOM();") #selecting random arrest record
        rows = curs.fetchone()
        conn.close()
        result = ""
        for row in rows:
            result = result + 'þ' + row #saving results with proper separator
        result = result[1:]
        print(result) #printing result
    except Error as e:
        print(e)
    return result #return result string
