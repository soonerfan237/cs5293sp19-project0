import urllib.request
#import PyPDF2.PdfFileReader
from PyPDF2 import PdfFileReader
import tempfile
from bs4 import BeautifulSoup
import re

links = []
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
        print(page1)

def createdb():
    print("creating db")

def populatedb(db, incidents):
    print("populating db")

def status(db):
    print("status: getting random row")
