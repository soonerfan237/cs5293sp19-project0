# cs5293sp19-project0
Alexander Sullivan-Wilson

You can run the code with the following command:
pipenv run python project0/main.py --arrests <url>

The fetchincidents(url) function takes the url of a single pdf as a parameter.  The url is retrieved through the --arrests command line argument.  This will download the bytes of the pdf and store it in the tmp/output file.  I used the urllib module to read the contents of the url.

The fetchincidents_test(test_file) function is only used for testing.  This function will copy a local test file into the output directory to emulate the function of fetchincidents(url).

The extractincidents() function will read the bytes from the tmp/output file and extract into a string using tempfile and PyPDF2 modules.  It will then parse the string for incidents.  It will first separate the rows by semicolon and filter out the column header data.  For the remaining columns I use a combination of regex (using re module) and other logic to parse out the data.
arrest_time is hard-coded to be the first column in each row.  
case_number is hard-coded to be the second column in each row.
arrestee_birthday is parsed by using regex to search for a date field that comes after the arrest_time in the row.
Officer is generally the last column, except when I can detect a space at the end of the line.
Status is generally one column, except when it includes the word Citation - in which case it spills onto 2 lines.
arrestee_address is everything in between the arrestee_birthday and the status.
Parsing arrest_location, offense, and arrestee was more complicated because they can all be variable line lengths and there is inconsistent formatting that can be picked up by regex.  The pattern I used to identify these is that when a line ends with a space character, it means that the contents of that item continue on the next line.  I used this method to detect if arrestee_name and arrest_location were multiple lines.
Parsing assumes that arrestee_name is never more than 2 lines in length.  
It also assumes that arrest_location is never more than 2 lines in length.When parsing status it will assume 1 line in length unless it is a status containing the string "Citation" in which case it will parse 2 lines for status.

The createdb() function will create the schema in the normanpd.db.  I use the sqlite3 module to create the db and insert/select data in other methods.  It will drop any arrests tables that previously existed and create a new arrests table with the schema:
CREATE TABLE arrests (
    arrest_time TEXT,
    case_number TEXT,
    arrest_location TEXT,
    offense TEXT,
    arrestee_name TEXT,
    arrestee_birthday TEXT,
    arrestee_address TEXT,
    status TEXT,
    officer TEXT
);

The populatedb(db, incidents) function will add the newly parsed incidents to the table.

The status() function will return a random row from the arrests table.

I also have several test functions using pytest.
test_createdb() will test that the normanpd.db gets created successfully.
test_schema() will verify that the arrests table gets created and with the expected schema.
test_status() will verify that a random record can be retrieved from the database.  This test is run by extracting incidents from a local test pdf.
test_fetchincidents() will verify that incidents can be parsed from the test file.
test_extract_request() will verify that the correct number of incidents is parsed from the test file.  It will also verify that the correct fields are parsed from various incidents in the file.
